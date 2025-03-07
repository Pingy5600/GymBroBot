import asyncio
import math
from datetime import datetime
import os
import random

import dateparser
import discord
import pytz
from discord.ext import commands
from reactionmenu import ViewButton, ViewMenu, ViewSelect

import checks
import embeds
from autocomplete import getMetaFromExercise
from embeds import DefaultEmbed, Paginator, ReminderFieldGenerator
from exceptions import DeletionFailed, InvalidTime, TimeoutCommand
from helpers import (COLOR_MAP, date_set, db_manager, getClickableCommand, getDiscordTimeStamp)
from validations import validateEntryList, validateNotBot, validateAndCleanWeight


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
    @discord.app_commands.choices(variant=[  # value is percentage of weight lifted
        discord.app_commands.Choice(name="Regular", value=64),
        discord.app_commands.Choice(name="Feet 30cm elevated", value=70),
        discord.app_commands.Choice(name="Feet 60cm elevated", value=74),  
        discord.app_commands.Choice(name="Hands 30cm elevated", value=55),
        discord.app_commands.Choice(name="Hands 60cm elevated", value=41),
        discord.app_commands.Choice(name="On knees", value=49),
    ])
    async def weight(self, interaction: discord.Interaction, weight: str, variant: discord.app_commands.Choice[int]):
        weight = validateAndCleanWeight(weight)
        
        embed = DefaultEmbed(
            title="⚖️ Weight when performing pushups",
            description=(
                f"Selected variant **'{variant.name}'** requires you to lift **{variant.value}%** of your body weight.\n"
                f"Since you weigh **{weight}kg**, you are lifting **{math.ceil(weight * variant.value / 100)}kg** per pushup."
            )
        )
        embed.set_thumbnail(url=getMetaFromExercise("pushups")["image"])
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


    @discord.app_commands.command(name="goat", description="Need help? ask the goat!")
    async def goat(self, interaction: discord.Interaction):
        await interaction.response.send_message("<@462932133170774036>")


    @pushup_group.command(name="gamble", description="Give someone pushups", extras={'cog': 'common'})
    @discord.app_commands.describe(user="Which user")
    @discord.app_commands.describe(reason="Reason for the pushups")
    @discord.app_commands.checks.cooldown(rate=1, per=2700, key=lambda i: (i.guild_id, i.user.id))
    @checks.not_in_dm()
    @checks.in_correct_server()
    async def pushup(self, interaction, user: discord.Member, reason: str) -> None:
        """Give someone pushups

        Args:
            interaction (Interaction): Users Interaction
            user
        """
        await interaction.response.defer()

        # cant give pushups a bot
        if user.bot:
            return await interaction.followup.send(embed=embeds.OperationFailedEmbed(
                "You can't give pushups to a bot!"
            ))

        ban_explain_embed = embeds.DefaultEmbed("🔨 Pick your ban type")
        ban_explain_embed.add_field(
            name="🎰 Gamble",
            value=f"This is a 50/50. Either you ({interaction.user.mention}) or {user.mention} are banned.",
            inline=True
        )
        ban_explain_embed.add_field(
            name="✂️ Rock Paper Scissors",
            value=f"Play Rock Paper Scissors against each other. Loser gets banned."
        )

        await interaction.followup.send(embed=ban_explain_embed, view=BanTypeView(user, interaction.user, self.bot, reason))


class BanTypeView(discord.ui.View):
    def __init__(self, user, ban_starter, bot, reason, timeout = 180):
        self.user = user
        self.ban_starter = ban_starter
        self.bot = bot
        self.reason = reason
        self.selected_roles = None

        super().__init__(timeout=timeout)

    
    @discord.ui.button(label="Gamble", style=discord.ButtonStyle.blurple, row=3, disabled=False, emoji='🎰')
    async def gamble_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # defer in case processing the selected data takes a while
        await interaction.response.defer()
        urls = [
            "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExczV5enBkbTVoNGZoZHUwdmdzdDdjbzFoZ3VoMDA4MTVxdDY2Ymo2byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6jqfXikz9yzhS/giphy.gif",
            "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExemNibW9ra2Njemh5Zm4wZDB4bWQzemhmM2lodjd3cXhyNXZjeXM5eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26uf2YTgF5upXUTm0/giphy.gif",
            "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWVqeXV3OHRpcHNtemx0ODJ4aHh1ZXdhejZ2aXQwN2o0Z21sdHJ3eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qNCtzhsWCc7q4D2FB5/giphy.gif",
            "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmM0am03ejVudHkzejkyODMwaWNjaXg1emtyYThrNGttd2J1cTByYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26ufjXhjqhpFgcONq/giphy.gif",
            "https://media0.giphy.com/media/l2SqgVwLpAmvIfMCA/giphy.gif?cid=ecf05e47mfvwpbejd07zq4l2jyv74wyppg4ik3wnstsra73d&ep=v1_gifs_related&rid=giphy.gif&ct=g",
        ]

        gamble_embed = embeds.DefaultEmbed(f"**🎰 {self.ban_starter.display_name} vs. {self.user.display_name}**")
        gamble_embed.set_image(url=random.choice(urls))
        await interaction.edit_original_response(embed=gamble_embed, view=None)

        # wait 4 seconds
        await asyncio.sleep(4)

        # determine who to ban
        choices = [self.user, self.ban_starter]
        loser = self.ban_starter if random.randint(0, 100) < 50 else self.user # 50/50 for starter to lose
        choices.remove(loser)
        winner = choices[0]

        # save results to stats
        await db_manager.increment_ban_gamble_wins(winner.id)
        await db_manager.increment_ban_gamble_losses(loser.id)

        # reset the streaks
        await db_manager.reset_ban_gamble_loss_streak(winner.id)
        await db_manager.reset_ban_gamble_win_streak(loser.id)

        # check if current streaks are higher than best streak
        await db_manager.check_ban_gamble_win_streak(winner.id)
        await db_manager.check_ban_gamble_loss_streak(loser.id)


        # create embed to show who won
        result_embed = embeds.DefaultEmbed(
            f"🏅 {winner} won!", f"{loser.mention} has been banned", user=winner
        )

        # get winner current streak
        winner_current_streak = await db_manager.get_current_win_streak(winner.id)
        if winner_current_streak[0] == -1:
            return await interaction.edit_original_response(embed=embeds.OperationFailedEmbed(
                "Something went wrong...", winner_current_streak[1]
            ))
        
        # get winner highest streak
        highest_win_streak = await db_manager.get_highest_win_streak(winner.id)
        if highest_win_streak[0] == -1:
            return await interaction.edit_original_response(embed=embeds.OperationFailedEmbed(
                "Something went wrong...", highest_win_streak[1]
            ))
        
        # get winner total wins
        total_wins = await db_manager.get_ban_total_wins(winner.id)
        if total_wins[0] == -1:
            return await interaction.edit_original_response(embed=embeds.OperationFailedEmbed(
                "Something went wrong...", total_wins[1]
            ))
        
        # add stats field to embed
        result_embed.add_field(
            name="📈 Stats of winner",
            value=f"""{winner.mention} current win streak```{winner_current_streak[0][0]}```
            {winner.mention} highest win streak```{highest_win_streak[0][0]}```
            {winner.mention} total wins```{total_wins[0][0]}```""",
            inline=True
        )
        
        # get loser current streak
        loser_current_streak = await db_manager.get_current_loss_streak(loser.id)
        if loser_current_streak[0] == -1:
            return await interaction.edit_original_response(embed=embeds.OperationFailedEmbed(
                "Something went wrong...", loser_current_streak[1]
            ))
        
        # get loser highest streak
        highest_loss_streak = await db_manager.get_highest_loss_streak(loser.id)
        if highest_loss_streak[0] == -1:
            return await interaction.edit_original_response(embed=embeds.OperationFailedEmbed(
                "Something went wrong...", highest_loss_streak[1]
            ))
        
        # get loser total losses
        total_losses = await db_manager.get_ban_total_losses(loser.id)
        if total_losses[0] == -1:
            return await interaction.edit_original_response(embed=embeds.OperationFailedEmbed(
                "Something went wrong...", total_losses[1]
            ))
        
        # add stats field to embed
        result_embed.add_field(
            name="📉 Stats of loser",
            value=f"""{loser.mention} current loss streak```{loser_current_streak[0][0]}```
            {loser.mention} highest loss streak```{highest_loss_streak[0][0]}```
            {loser.mention} total losses```{total_losses[0][0]}```""",
            inline=True
        )

        # edit embed with results of the 50/50
        await interaction.edit_original_response(embed=result_embed)
        
        # wait one second so loser can still see in channel who won/lost
        await asyncio.sleep(1)

        # ban the user
        await interaction.followup.send("test")

        # send ban message to loser
        banned_embed = embeds.DefaultEmbed(
            f"🔨 You have been given pushups by {interaction.guild.name}!", user=loser
        )

        banned_embed.add_field(
            name="💡 Reason",
            value=f"```{self.reason}```",
        )

        # add field to show you lost a 50/50
        banned_embed.add_field(
            name="🪦 You have lost a 50/50",
            value=f"```You lost to {winner}```",
            inline=False
        )

        await interaction.followup.send(embed=banned_embed)

    # @discord.ui.button(label="Rock Paper Scissors", style=discord.ButtonStyle.blurple, row=3, disabled=False, emoji='✂️')
    # async def RPS_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await interaction.response.defer()

    #     embed = discord.Embed(
    #         title="Rock-Paper-Scissors",
    #         description=f"{self.ban_starter.mention} challenges {self.user.mention} to a game of Rock-Paper-Scissors! (to the death)",
    #         color=discord.Color.blurple(),
    #     )
    #     embed.set_footer(text="Click your choice below to play!")

    #     view = RPSView(self.ban_starter, self.user)

    #     message = await interaction.edit_original_response(embed=embed, view=view)
    #     view.message = message

    async def interaction_check(self, interaction: discord.Interaction):
        """Check that the user is the one who is clicking buttons
        Args:
            interaction (discord.Interaction): Users Interaction

        Returns:
            bool
        """
        responses = [
            f"<@{interaction.user.id}> shatap lil bro",
            f"<@{interaction.user.id}> you are NOT him",
            f"<@{interaction.user.id}> blud thinks he's funny",
            f"<@{interaction.user.id}> it's on sight now",
        ]

        
        # can only be triggered by the profile owner or an owner
        is_possible = (interaction.user.id == self.ban_starter.id) or str(interaction.user.id) in list(os.environ.get("OWNERS").split(","))
        
        # send message if usr cannot interact with button
        if not is_possible:
            await interaction.response.send_message(random.choice(responses))
        
        return is_possible
    

async def setup(bot):
    await bot.add_cog(Common(bot))