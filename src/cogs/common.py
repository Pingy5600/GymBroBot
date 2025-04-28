import asyncio
from datetime import datetime
import os
import random

import dateparser
import discord
import pytz
from discord.ext import commands
from reactionmenu import ViewButton, ViewMenu, ViewSelect

import embeds
from embeds import Paginator, ReminderFieldGenerator
from exceptions import DeletionFailed, InvalidTime, TimeoutCommand
from helpers import (db_manager, getClickableCommand, getDiscordTimeStamp)
from helpers import pagination
from validations import validateAndCleanWeight, validateEntryList, validateNotBot


class Common(commands.Cog, name="common"):
    def __init__(self,bot):
        self.bot = bot
        self.title = "🤖 Common"

    command_remind_group = discord.app_commands.Group(name="remind", description="Remind Group")

    @discord.app_commands.command(name="help", description="List all commands the bot has loaded")
    async def help(self, interaction: discord.Interaction) -> None:
        """Sends info about all available commands."""
        
        menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed)
        page_numbers = {}

        # Specifieke volgorde voor de cogs
        cog_order = ["common", "schema", "pr", "rep", "gamble", "admin"]
        
        # Process each cog in de opgegeven volgorde
        for i, cog_name in enumerate(cog_order):
            cog = self.bot.get_cog(cog_name)
            if cog is None:
                continue
            
            # initialize embed
            embed = embeds.DefaultEmbed(
                f"**Help - {cog.title}**"
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)

            # get commands for that cog
            commands = cog.get_app_commands()
            
            # Verwerken van subcommando's
            while any(isinstance(command, discord.app_commands.Group) for command in commands):
                for command in commands:
                    if isinstance(command, discord.app_commands.Group):
                        commands.extend(command.walk_commands())
                        commands.remove(command)

            # generate strings per command
            data = []
            for command in commands:
                clickable_command = getClickableCommand(command, self.bot.command_ids)
                description = command.description.partition("\n")[0]
                data.append(f"{clickable_command} - {description}")

            # als er geen commando's zijn, sla de cog over
            if not data:
                continue

            # voeg de commando's toe aan de embed
            cog_emoji = cog.title.split(" ")[0]
            page_numbers[i + 1] = cog_emoji

            help_text = "\n".join(data)
            embed.add_field(
                name="",
                value=help_text,
                inline=False
            )

            menu.add_page(embed)

        # wijzig de volgorde van de pagina's
        menu.add_go_to_select(ViewSelect.GoTo(
            title="Go to category...",
            page_numbers=page_numbers
        ))
        
        # Voeg navigatieknoppen toe
        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        
        # Start het menu
        return await menu.start()

    @discord.app_commands.command(name="profile", description="Gives the profile of the given user")
    @discord.app_commands.describe(user="Which user")
    async def profile(self, interaction: discord.Interaction, user: discord.User = None):
        await interaction.response.defer(thinking=True)  # Geeft meer tijd voor interactie

        if user is None:
            user = interaction.user

        validateNotBot(user)
        
        user_id = str(user.id)
        user_color = await db_manager.get_user_color(user_id)
        total_pushups = await db_manager.get_pushups_todo(user.id)
        total_done = await db_manager.get_pushups_done(user.id)
        pending = await db_manager.get_pending_pushups(user.id)
        bodyweight = await db_manager.get_bodyweight(user.id)

        # Stel embed kleur in
        if user_color:
            embed = discord.Embed(
                title=f"Profile of {user}",
                description="This is your profile!",
                color=discord.Color(int(user_color[1:], 16))
            )
        else:
            embed = discord.Embed(
                title=f"Profile of {user}",
                description="You have not set a custom color.",
                color=discord.Color.default()
            )

        # Toon ofwel pushups in reserve, ofwel pushups to do
        if total_pushups < 0:
            embed.add_field(name="📦 Pushups in reserve", value=f"```{abs(total_pushups)}```", inline=True)
        else:
            embed.add_field(name="📊 Pushups to do", value=f"```{total_pushups}```", inline=True)
        
        embed.add_field(name="🏆 Pushups done", value=f"```{total_done}```", inline=True)

        if pending > 0:
            embed.add_field(name="⌛ Pending", value=f"```{pending}```", inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)

        if bodyweight is not None:
            embed.add_field(name="⚖️ Bodyweight", value=f"```{bodyweight} kg```", inline=True)

        view = ProfileView(interaction.client, user)
        await view.setup()
        await interaction.followup.send(embed=embed, view=view)


    @command_remind_group.command(name="me", description="Remind me when to take my creatine")
    @discord.app_commands.describe(wanneer="When should the bot send you a reminder", waarover="What should the bot remind you for")
    async def remindme(self, interaction, wanneer: str, waarover: discord.app_commands.Range[str, 1, 100]) -> None:
        await interaction.response.defer(thinking=True)  # Geeft meer tijd om de interactie te verwerken

        # Stel de tijdzone in op CET (Central European Time)
        tz = pytz.timezone('CET')

        t = dateparser.parse(wanneer, settings={
            'DATE_ORDER': 'DMY',
            'TIMEZONE': 'CET',
            'PREFER_DAY_OF_MONTH': 'first',
            'PREFER_DATES_FROM': 'past',
            'DEFAULT_LANGUAGES': ["en", "nl"]
        })

        if t is None:
            raise InvalidTime("Geen geldig tijdstip")

        # Controleer of de parsed datetime 't' tijdzone-bewust is
        if t.tzinfo is None:
            t = tz.localize(t)  # Maak het tijdzone-bewust

        # Vergelijk de tijd met de huidige tijd in de juiste tijdzone
        if t < datetime.now(tz):
            raise InvalidTime("De opgegeven tijd is in het verleden")

        # Zet reminder in de database
        succes = await db_manager.set_reminder(
            interaction.user.id,
            subject=waarover,
            time=t.strftime('%Y-%m-%d %H:%M:%S')
        )

        if not succes:
            raise Exception("Could not set reminder...")

        desc = f"I will remind you at {getDiscordTimeStamp(t, full_time=True)} for {waarover}"
        embed = embeds.OperationSucceededEmbed(
            "Reminder set!", desc, emoji="⏳"
        )
        await interaction.followup.send(embed=embed)
        
    @command_remind_group.command(name="delete", description="Delete a specific reminder")
    async def delete_reminder(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        # Haal de reminders op voor de gebruiker
        reminders = await db_manager.get_reminders_by_user(str(interaction.user.id))
        validateEntryList(reminders, "You have no reminders set.")

        paginator = Paginator(
            items=reminders,
            user=interaction.user,
            title=f"Reminders for {interaction.user.display_name}",
            generate_field_callback=ReminderFieldGenerator.generate_field,
            exercise_url=None
        )
        embed = await paginator.generate_embed()
        content = "Reply with the **number** of the reminder you want to delete."
        # Stuur de embed en koppel de paginator
        message = await interaction.followup.send(content=content, embed=embed, view=paginator)
        message_id = message.id

        # Functie om de invoer te valideren
        def check(m):
            return (
                m.author == interaction.user
                and m.channel == interaction.channel
                and m.content.isdigit()
                and m.reference is not None
                and m.reference.message_id == message_id
            )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60.0)

        except asyncio.TimeoutError:
            raise TimeoutCommand()

        index = int(msg.content) - 1

        if index < 0 or index >= len(reminders):
            raise ValueError("Invalid selection. Please try again.")

        selected_reminder = reminders[index]
        success = await db_manager.delete_reminder(selected_reminder['id'])

        if not success:
            raise DeletionFailed("Failed to delete the reminder.")

        # Stuur een succesbericht
        embed = embeds.OperationSucceededEmbed(
            title="Reminder Deleted",
            description=f"Successfully deleted the reminder for {getDiscordTimeStamp(selected_reminder['time'], full_time=True)}."
        )
        await interaction.followup.send(embed=embed)


class ProfileView(discord.ui.View):
    def __init__(self, bot, user):
        self.bot = bot
        self.user = user
        super().__init__(timeout=500)

    async def setup(self):  
        events = await db_manager.get_all_pushup_events(self.user.id)
        if not events or (events and events[0] == -1):
            self.see_pushup_events.disabled = True

    @discord.ui.button(label="See Pushup Events", emoji='📆', style=discord.ButtonStyle.blurple, custom_id="see_pushup_events")
    async def see_pushup_events(self, interaction: discord.Interaction, button: discord.ui.Button):
        events = await db_manager.get_all_pushup_events(self.user.id)
        async def get_page(page: int):
            L = 5 # elements per page
            embed = embeds.DefaultEmbed(
                f"💥 Pushup Events of {self.user.display_name}",
                " ",
                user=self.user
            )
            offset = (page-1) * L

            for event in events[offset:offset+L]:
                embed.description += f"{'+' if event[0] > 0 else ''}{event[0]} • {event[1]}\n"

            n = pagination.Pagination.compute_total_pages(len(events), L)
            embed.set_footer(text=f"Page {page} from {n}")
            return embed, n

        await pagination.Pagination(interaction, get_page).navegate()

    @discord.ui.button(label="Set Color", emoji='🎨', style=discord.ButtonStyle.blurple, custom_id="set_color")
    async def set_color(self, interaction: discord.Interaction, button: discord.ui.Button):
        #TODO refactor deze interaction check weg, wordt nu overal gebruikt
        responses = [
            f"<@{interaction.user.id}> shatap lil bro",
            f"<@{interaction.user.id}> you are NOT him",
            f"<@{interaction.user.id}> blud thinks he's funny",
            f"<@{interaction.user.id}> it's on sight now",
        ]

        # can only be triggered by the profile owner or an owner
        is_possible = (interaction.user.id == self.user.id) or str(interaction.user.id) in list(os.environ.get("OWNERS").split(","))

        # send message if usr cannot interact with button
        if not is_possible:
            await interaction.response.send_message(random.choice(responses), ephemeral=True)

    
        await interaction.response.send_modal(SetColorModal(self.user))


    @discord.ui.button(label="Set Bodyweight", emoji='⚖️', style=discord.ButtonStyle.blurple, custom_id="set_bodyweight")
    async def set_bodyweight(self, interaction: discord.Interaction, button: discord.ui.Button):
        #TODO refactor deze interaction check weg, wordt nu overal gebruikt
        responses = [
            f"<@{interaction.user.id}> shatap lil bro",
            f"<@{interaction.user.id}> you are NOT him",
            f"<@{interaction.user.id}> blud thinks he's funny",
            f"<@{interaction.user.id}> it's on sight now",
        ]

        # can only be triggered by the profile owner or an owner
        is_possible = (interaction.user.id == self.user.id) or str(interaction.user.id) in list(os.environ.get("OWNERS").split(","))

        # send message if usr cannot interact with button
        if not is_possible:
            await interaction.response.send_message(random.choice(responses), ephemeral=True)
        await interaction.response.send_modal(SetBodyweightModal(self.user))


class SetColorModal(discord.ui.Modal, title="Set Color"):
    def __init__(self, user):
        self.user = user

    color = discord.ui.TextInput(
        label="Color",
        placeholder="Enter a hex color code (e.g. #FF5733)",
        max_length=7,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        color = self.color.value.strip()
        if not color.startswith("#") or len(color) != 7:
            return await interaction.response.send_message("Invalid color format. Please use a hex code (e.g. #FF5733).", ephemeral=True)

        await db_manager.set_color(self.user.id, color)
        embed = embeds.DefaultEmbed(
            title="Color Changed",
            description=f"Your color has been changed to {color}.",
            color=discord.Color(int(color[1:], 16))
        )
        
        #TODO update originele embed met geupdate kleur
        await interaction.response.send_message(embed=embed, ephemeral=True)


class SetBodyweightModal(discord.ui.Modal, title="Set Bodyweight"):
    def __init__(self, user):
        self.user = user

    bodyweight = discord.ui.TextInput(
        label="Bodyweight",
        placeholder="Enter your bodyweight in kg",
        max_length=5,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        weight = validateAndCleanWeight(self.bodyweight.value.strip())
        await db_manager.set_bodyweight(self.user.id, weight)

        embed = embeds.OperationSucceededEmbed(
            title="Bodyweight Set",
            description=f"Your bodyweight has been set to {weight} kg.",
            emoji="⚖️"
        )

        #TODO update originele embed met geupdate bodyweight
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Common(bot))