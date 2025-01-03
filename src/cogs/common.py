import asyncio
import math
from datetime import datetime

import dateparser
import discord
import pytz
from discord.ext import commands

import embeds
from embeds import DefaultEmbed, Paginator, ReminderFieldGenerator
from exceptions import DeletionFailed, InvalidTime, TimeoutCommand
from helpers import COLOR_MAP, EXERCISE_IMAGES, date_set, db_manager, getDiscordTimeStamp, getClickableCommand
from validations import validateEntryList, validateNotBot
from reactionmenu import ViewMenu, ViewSelect, ViewButton


class Common(commands.Cog, name="common"):
    def __init__(self,bot):
        self.bot = bot
        self.title = "🤖 Common"

    command_remind_group = discord.app_commands.Group(name="remind", description="remind Group")
    pushup_group = discord.app_commands.Group(name="pushup", description="pushup Group")


    @pushup_group.command(name="weight", description="How much weight are you pushing?")
    @discord.app_commands.describe(
        weight="How much do you weigh?",
        variant="Which variant are you performing?"
    )
    @discord.app_commands.choices(variant=[ # value is percentage of weigt lifted
        discord.app_commands.Choice(name="Regular", value=64),
        discord.app_commands.Choice(name="Feet 30cm elevated", value=70),
        discord.app_commands.Choice(name="Feet 60cm elevated", value=74),  
        discord.app_commands.Choice(name="Hands 30cm elevated", value=55),
        discord.app_commands.Choice(name="Hands 60cm elevated", value=41),
        discord.app_commands.Choice(name="On knees", value=49),
    ])
    async def weight(self, interaction: discord.Interaction, weight: str, variant: discord.app_commands.Choice[int]):
        embed = DefaultEmbed(
            title="⚖️ Weight when performing pushups",
            description=f"Selected variant **'{variant.name}'** requires you to lift **{variant.value}%** of your body weight.\nSince you weigh **{weight}kg**, you are lifting **{math.ceil(weight * variant.value / 100)}kg** per pushup."
        )
        embed.set_thumbnail(url=EXERCISE_IMAGES["pushups"])
        await interaction.response.send_message(embed=embed)
 

    @discord.app_commands.command(name="help", description="List all commands the bot has loaded")
    async def help(self, interaction: discord.Interaction) -> None:
        """Sends info about all available commands."""
        
        menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed)
        page_numbers = {}

        # Specifieke volgorde voor de cogs
        cog_order = ["common", "schema", "pr", "rep", "admin"]
        
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
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)

        # Haal de kleur op uit COLOR_MAP
        user_id = str(user.id)
        user_color = COLOR_MAP.get(user_id, None)
        
        if user_color:
            # Embed met de specifieke kleur van de gebruiker
            embed = discord.Embed(
                title=f"Profile of {user}",
                description="This is your profile! Here is your own color",
                color=discord.Color(int(user_color[1:], 16))  # Hexcode omzetten naar kleur
            )
            embed.add_field(name="A lot more coming soon", value="COMING SOON", inline=True)

        else:
            # Standaard embed als de gebruiker geen kleur heeft
            embed = discord.Embed(
                title=f"Profile of {user}",
                description="You have not set a custom color.",
                color=discord.Color.default()
            )

        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.followup.send(embed=embed)


    @command_remind_group.command(name="me", description="Remind me when to take my creatine")
    @discord.app_commands.describe(wanneer="When should the bot send you a reminder", waarover="What should the bot remind you for")
    async def remindme(self, interaction, wanneer: str, waarover: discord.app_commands.Range[str, 1, 100]) -> None:
        await interaction.response.defer(thinking=True)  # Geeft meer tijd om de interactie te verwerken

        # Stel de tijdzone in op CET (Central European Time)
        tz = pytz.timezone('CET')

        t = dateparser.parse(wanneer, settings=date_set)

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
            exercise=None
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


    @discord.app_commands.command(name="goat", description="Need help? ask the goat!")
    async def goat(self, interaction: discord.Interaction):
        await interaction.response.send_message("<@462932133170774036>")


async def setup(bot):
    await bot.add_cog(Common(bot))