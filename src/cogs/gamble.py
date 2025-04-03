import asyncio
import math
import os
import random
import numpy as np

import discord
from discord.ext import commands

from autocomplete import getMetaFromExercise
import checks
import embeds
from exceptions import InvalidPushups
from helpers import db_manager, getClickableCommand
from validations import validateAndCleanWeight, validateNotBot, validatePermissions, validatePushups


class Gamble(commands.Cog, name="gamble"):
    def __init__(self,bot):
        self.bot = bot
        self.title = "🎰 Gamble"

    pushup_group = discord.app_commands.Group(name="pushup", description="Pushup Group")

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
        
        embed = embeds.DefaultEmbed(
            title="⚖️ Weight when performing pushups",
            description=(
                f"Selected variant **'{variant.name}'** requires you to lift **{variant.value}%** of your body weight.\n"
                f"Since you weigh **{weight}kg**, you are lifting **{math.ceil(weight * variant.value / 100)}kg** per pushup."
            )
        )
        embed.set_thumbnail(url=getMetaFromExercise("pushups")["image"])
        await interaction.response.send_message(embed=embed)


    @pushup_group.command(name="done", description="Lowers the Total remaining pushups if you have done them. Be honest!")
    @discord.app_commands.describe(done="The number of pushups you've completed", user="Which user")
    async def done(self, interaction: discord.Interaction, done: int, user: discord.User = None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validatePushups(done)
        validateNotBot(user)
        validatePermissions(user, interaction)

        # Haal het totaal aantal pushups op
        total_pushups = await db_manager.get_pushups(user.id)

        if done > total_pushups:
            raise InvalidPushups()

        # Update de pushups
        new_total = total_pushups - done
        success = await db_manager.add_pushups(user.id, -done)

        # Voeg de voltooide pushups toe
        await db_manager.add_pushups_done(user.id, done)
        total_done = await db_manager.get_pushups_done(user.id)

        if success:
            pushup_embed = embeds.DefaultEmbed(
                f"Great job {user.display_name} 💪",
                f"Successfully removed {done} pushups from your total."
            )

            pushup_embed.add_field(
                name="📊 Total remaining pushups",
                value=f"```{new_total}```",
                inline=True
            )

            pushup_embed.add_field(
                name="🏆 Pushups done",
                value=f"```{total_done}```",
                inline=True
            )

            pushup_embed.set_footer(text="The time to gamble is now!")
            pushup_embed.set_thumbnail(url=user.display_avatar.url)

            await interaction.followup.send(embed=pushup_embed)

        else:
            raise InvalidPushups()


    @pushup_group.command(name="add", description="Adds pushups to a user's total. Admin only!")
    @checks.is_admin_or_has_permissions()  # Zorg ervoor dat alleen admins of gebruikers in de lijst dit kunnen uitvoeren
    @discord.app_commands.describe(add="The number of pushups to add", user="Which user")
    async def add_pushups(self, interaction: discord.Interaction, add: int, user: discord.User):
        await interaction.response.defer(thinking=True)

        # Validaties (zorg ervoor dat de admin geen fout maakt)
        validatePushups(add)
        validateNotBot(user)

        # Haal het totaal aantal pushups voor de gebruiker op
        total_pushups = await db_manager.get_pushups(user.id)

        # Voeg de opgegeven pushups toe
        new_total = total_pushups + add

        # Werk de pushups bij in de database
        success = await db_manager.add_pushups(user.id, add)

        if success:
            pushup_embed = embeds.DefaultEmbed(
                f"Pushups added",
                f"Successfully added {add} pushups to {user.display_name}'s total."
            )

            pushup_embed.add_field(
                name="📊 New Total remaining pushups",
                value=f"```{new_total}```",
                inline=True
            )
            pushup_embed.set_footer(text="Keep pushing yourself!")
            await interaction.followup.send(embed=pushup_embed)

        else:
            raise InvalidPushups()


    @pushup_group.command(name="gamble", description="Give someone pushups", extras={'cog': 'gamble'})
    @discord.app_commands.describe(user="Which user")
    @discord.app_commands.checks.cooldown(rate=3, per=2700, key=lambda i: (i.guild_id, i.user.id))
    @checks.not_in_dm()
    async def pushup(self, interaction, user: discord.Member) -> None:
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
        
        if user == interaction.user:
            return await interaction.followup.send(embed=embeds.OperationFailedEmbed(
                "You can't give pushups to yourself"
            ))

        gamble_explanation_embed = embeds.DefaultEmbed("Pick your type!")
        gamble_explanation_embed.add_field(
            name="🎰 50/50",
            value=f"This is a 50/50. Either you ({interaction.user.mention}) or {user.mention} gets the pushups.",
            inline=True
        )
        gamble_explanation_embed.add_field(
            name="✂️ Rock Paper Scissors",
            value=f"Play Rock Paper Scissors against each other."
        )
        gamble_explanation_embed.add_field(
            name="💣 Mines",
            value=f"25 possible mines. You have to guess where they are. If you hit one, you lose."
        )
        gamble_explanation_embed.add_field(
            name="💥 Russian Roulette",
            value="Choose the amount bullets in the chamber and pull the trigger. If you dare."
        )
        should_explain_double_reset = await db_manager.has_used_double_or_nothing(interaction.user.id)
        don_exlanation = f"Toss a coinflip and double your remaining pushups or make it zero. *You need to complete all your pushups before you can use this again!*" if should_explain_double_reset else "Toss a coinflip and double your remaining pushups or make it zero."
        gamble_explanation_embed.add_field(
            name="💎 Double or Nothing",
            value=don_exlanation
        )

        view = PushupTypeView(user, interaction.user, self.bot)
        await view.setup()

        await interaction.followup.send(embed=gamble_explanation_embed, view=view)


class PushupTypeView(discord.ui.View):
    def __init__(self, user, gamble_starter, bot, timeout=180):
        super().__init__(timeout=timeout)
        self.user = user
        self.gamble_starter = gamble_starter
        self.bot = bot

    async def setup(self):
        """update the double or nothing button's disabled state."""
        should_disable = await db_manager.has_used_double_or_nothing(self.gamble_starter.id)
        self.double_or_nothing_button.disabled = should_disable

    @discord.ui.button(label="50/50", style=discord.ButtonStyle.blurple, emoji='🎰')
    async def gamble_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        async def callback_func(amount, interaction):
            urls = [
                "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExczV5enBkbTVoNGZoZHUwdmdzdDdjbzFoZ3VoMDA4MTVxdDY2Ymo2byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6jqfXikz9yzhS/giphy.gif",
                "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExemNibW9ra2Njemh5Zm4wZDB4bWQzemhmM2lodjd3cXhyNXZjeXM5eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26uf2YTgF5upXUTm0/giphy.gif",
                "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWVqeXV3OHRpcHNtemx0ODJ4aHh1ZXdhejZ2aXQwN2o0Z21sdHJ3eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qNCtzhsWCc7q4D2FB5/giphy.gif",
                "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmM0am03ejVudHkzejkyODMwaWNjaXg1emtyYThrNGttd2J1cTByYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26ufjXhjqhpFgcONq/giphy.gif",
                "https://media0.giphy.com/media/l2SqgVwLpAmvIfMCA/giphy.gif?cid=ecf05e47mfvwpbejd07zq4l2jyv74wyppg4ik3wnstsra73d&ep=v1_gifs_related&rid=giphy.gif&ct=g"
            ]

            gamble_embed = embeds.DefaultEmbed(f"**🎰 {self.gamble_starter.display_name} vs. {self.user.display_name}**")
            gamble_embed.set_image(url=random.choice(urls))
            await interaction.response.edit_message(embed=gamble_embed, view=None)

            # wait 4 seconds
            await asyncio.sleep(4)

            # determine who to give pushups to
            choices = [self.user, self.gamble_starter]
            loser = self.gamble_starter if random.randint(0, 100) < 50 else self.user # 50/50 for starter to lose
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

            # Pushups opslaan en totaal ophalen
            await db_manager.add_pushups(loser.id, amount)
            total_pushups = await db_manager.get_pushups(loser.id)

            # create embed to show who won
            result_embed = embeds.DefaultEmbed(
                f"🏅 {winner} won!", f"{loser.mention} has been given pushups", user=winner
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
                value=f"""{winner.mention} current win streak```{winner_current_streak[0][0]}```\n{winner.mention} highest win streak```{highest_win_streak[0][0]}```\n{winner.mention} total wins```{total_wins[0][0]}```""",
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
                value=f"""{loser.mention} current loss streak```{loser_current_streak[0][0]}```\n{loser.mention} highest loss streak```{highest_loss_streak[0][0]}```\n{loser.mention} total losses```{total_losses[0][0]}```""",
                inline=True
            )

            # **Leeg veld toevoegen om juiste indeling te forceren**
            result_embed.add_field(name="\u200b", value="\u200b", inline=True)

            result_embed.add_field(
                name="💪 added pushups",
                value=f"```{amount}```",
                inline=True
            )

            result_embed.add_field(
                name="📊 Total remaining pushups",
                value=f"```{total_pushups}```",
                inline=True
            )

            # **Leeg veld om layout consistent te houden**
            result_embed.add_field(name="\u200b", value="\u200b", inline=True)
            result_embed.set_thumbnail(url=winner.display_avatar.url)

            # edit embed with results of the 50/50
            await interaction.edit_original_response(embed=result_embed)

        await interaction.response.edit_message(embed=embeds.DefaultEmbed("Choose pushup amount!"), view=Amount(self.gamble_starter, self.bot, callback_func))

    @discord.ui.button(label="Rock Paper Scissors", style=discord.ButtonStyle.blurple, emoji='✂️')
    async def RPS_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        async def callback_func(amount, interaction):
            view = RPSView(self.gamble_starter, self.user, amount)
            await interaction.response.edit_message(embed=embeds.DefaultEmbed(f"Rock Paper Scissors for {amount} pushups!"), view=view)

        await interaction.response.edit_message(embed=embeds.DefaultEmbed("Choose pushup amount!"), view=Amount(self.gamble_starter, self.bot, callback_func))

    @discord.ui.button(label="Mines", style=discord.ButtonStyle.blurple, emoji='💣')
    async def mines_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Verzend het dropdown-menu en de uitleg voor de speler
        await interaction.response.edit_message(
            embed=embeds.DefaultEmbed(
                "With how many mines do you wish to play?",  
                "Select the number of mines (1-23)"
            ), 
            view=MinesSelectView(self.gamble_starter, self.user)
        )

    @discord.ui.button(label="Russian Roulette", style=discord.ButtonStyle.blurple, emoji="💥")
    async def russian_roulette_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        async def callback_func(amount, interaction):
            view = discord.ui.View()
            view.add_item(BulletSelect(self.gamble_starter, self.user, amount))

            embed = embeds.DefaultEmbed(
                "💥 Russian Roulette",
                "There are 6 spots in the chamber"
            )

            embed.add_field(
                name="🎲 **Odds for Winning**",
                value=f"""
 1 Bullet -> {round(amount*0.25)} pushups\n
 2 Bullets -> {round(amount*0.5)} pushups\n
 3 Bullets -> {amount} pushups\n
 4 Bullets -> {round(amount*1.5)} pushups\n
 5 Bullets -> {round(amount*1.75)} pushups\n
 6 Bullets -> {round(amount*2)} pushups\n
                """,
                inline=False
            )

            embed.add_field(
                name="💀 **Odds for Losing**",
                value=f"""
 1 Bullet -> {round(amount*1.75)} pushups\n
 2 Bullets -> {round(amount*1.5)} pushups\n
 3 Bullets -> {amount} pushups\n
 4 Bullets -> {round(amount*0.5)} pushups\n
 5 Bullets -> {round(amount*0.25)} pushups\n
 6 Bullets -> {round(amount*2)} pushups\n
                """,
                inline=False
            )

            embed.set_footer(text="The more bullets, the higher the risk... Choose wisely!")
            embed.color = discord.Color.blurple()  # Set the embed color to match the button color

            await interaction.response.edit_message(embed=embed, view=view)

        await interaction.response.edit_message(embed=embeds.DefaultEmbed("💪 Choose your pushup amount!"), view=Amount(self.gamble_starter, self.bot, callback_func))


    @discord.ui.button(label="💎 Double or Nothing", style=discord.ButtonStyle.danger, custom_id="double_or_nothing_button")
    async def double_or_nothing_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id

        # Haal huidige push-ups op
        current_pushups = await db_manager.get_pushups(user_id)
        if current_pushups == 0:
            await interaction.response.send_message("Je hebt geen push-ups om te gokken!", ephemeral=True)
            return

        # 🎰 Start de gamble animatie
        gifs = [
            "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXh2aHdrOGhteDVtM2twN2N0dDcwZmNrZmhmbWN3bTdqYzR4Y3QyNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bubpLP4o75fmIVukRr/giphy.gif",
            "https://media.giphy.com/media/LRVnPYqM8DLag/giphy.gif?cid=790b7611eb6ynljhvv3ebixlsxwp65dngxtkgsbafx5tgnri&ep=v1_gifs_search&rid=giphy.gif&ct=g",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWI2eW5samh2djNlYml4bHN4d3A2NWRuZ3h0a2dzYmFmeDV0Z25yaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3ohhwF34cGDoFFhRfy/giphy.gif",
            "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHNlc2wzOGdoNW0yemRzY212aGR0OGVldnAxOHR5aWM2Z29oNGJ3biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xUVC1UDpyuwOEPVlue/giphy.gif",
            "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3NrZTRtMG16aWM3ODAwaWZycGo0dXQ3enBjNTBucm0xcWZzcWU1MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Ta3v3I4GI1gH7Rqek6/giphy.gif"
        ]
        gamble_embed = embeds.DefaultEmbed(f"💎 **Double or Nothing**")
        gamble_embed.set_image(url=random.choice(gifs))
        await interaction.response.edit_message(embed=gamble_embed, view=None)

        # ⏳ Wacht 4 seconden
        await asyncio.sleep(4)

        # 50/50 kans
        if random.choice([True, False]):
            await db_manager.add_pushups(user_id, -current_pushups)  # Reset push-ups naar 0
            result_text = f"🎉 **Je hebt gewonnen!**\nJe push-ups zijn gereset naar **0**!"

        else:
            await db_manager.add_pushups(user_id, current_pushups)  # Push-ups verdubbelen
            await db_manager.set_double_or_nothing(user_id, True)
            result_text = f"😬 **Pech!**\nJe push-ups zijn verdubbeld naar **{current_pushups * 2}**!"


        # 📜 Embed met resultaat
        result_embed = embeds.DefaultEmbed(f"💎 **Double or Nothing Resultaat**", result_text)
        result_embed.set_thumbnail(url=interaction.user.display_avatar.url)

        # Stuur resultaat en verwijder knoppen
        await interaction.edit_original_response(embed=result_embed, view=None)


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
        is_possible = (interaction.user.id == self.gamble_starter.id) or str(interaction.user.id) in list(os.environ.get("OWNERS").split(","))

        # send message if usr cannot interact with button
        if not is_possible:
            await interaction.response.send_message(random.choice(responses), ephemeral=True)

        return is_possible


class MinesSelectView(discord.ui.View):
    def __init__(self, gamble_starter, user):
        super().__init__()
        self.gamble_starter = gamble_starter
        self.user = user
      
    @discord.ui.select(placeholder="Select the number of mines", options=[discord.SelectOption(label=str(i), value=str(i)) for i in range(1, 24)])
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        mines_amount = int(select.values[0])
        view =  MinesView(self.gamble_starter, self.user, mines_amount)

        embed = embeds.DefaultEmbed(
            title="💣 Mines!",
        )
        embed.add_field(
            name="*Mines*",
            value=f"```{mines_amount}```"
        )
        embed.add_field(
            name="*Safe Tiles left*",
            value=f"```{24-mines_amount}```",
            inline=True
        )
        embed.add_field(
            name="*Pushups so far*",
            value=f"```1```",
            inline=False
        )
        embed.add_field(
            name="*Next Tile Pushups*",
            value=f"```{round(MinesView.ODDS[mines_amount-1][0], 2)}```",
            inline=True
        )
        
        await interaction.response.edit_message(
            embed=embed,
            view=view
        )

    @discord.ui.button(label="See odds", style=discord.ButtonStyle.blurple, emoji="🃏")
    async def odds(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.send_message(
            embed=MinesOddsView.get_odds_table(1),
            view=MinesOddsView(self.gamble_starter)
        )

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
        is_possible = (interaction.user.id == self.gamble_starter.id) or str(interaction.user.id) in list(os.environ.get("OWNERS").split(","))

        # send message if usr cannot interact with button
        if not is_possible:
            await interaction.response.send_message(random.choice(responses), ephemeral=True)

        return is_possible


class MinesOddsView(discord.ui.View):
    def __init__(self, gamble_starter):
        super().__init__()
        self.gamble_starter = gamble_starter

    def get_odds_table(mines):
        embed = embeds.DefaultEmbed(
            "🃏 Odds",
            f"Odds for Minefield when playing with {mines} mines"
        )
        for (i, odd) in enumerate(MinesView.ODDS[mines-1]):
            embed.add_field(
                name=f"{i+1} flags",
                value=f"```{odd}x```",
            )
        return embed

    @discord.ui.select(placeholder="Select the number of mines", options=[discord.SelectOption(label=str(i), value=str(i)) for i in range(1, 24)])
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        mines_amount = int(select.values[0])

        await interaction.response.edit_message(
            embed=MinesOddsView.get_odds_table(mines_amount),
            view=self
        )
    
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
        is_possible = (interaction.user.id == self.gamble_starter.id) or str(interaction.user.id) in list(os.environ.get("OWNERS").split(","))

        # send message if usr cannot interact with button
        if not is_possible:
            await interaction.response.send_message(random.choice(responses), ephemeral=True)

        return is_possible


class Amount(discord.ui.View):
    def __init__(self, gamble_starter, bot, callback_func):
        super().__init__()
        self.gamble_starter = gamble_starter
        self.bot = bot
        self.callback_func = callback_func

    @discord.ui.button(label="10", style=discord.ButtonStyle.blurple, row=2, emoji='💪')
    async def amount_10(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_game(interaction, 10)

    @discord.ui.button(label="20", style=discord.ButtonStyle.blurple, row=2, emoji='💪')
    async def amount_25(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_game(interaction, 20)

    @discord.ui.button(label="30", style=discord.ButtonStyle.blurple, row=2, emoji='💪')
    async def amount_50(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_game(interaction, 30)

    async def start_game(self, interaction: discord.Interaction, amount):
        await self.callback_func(amount, interaction)

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
        is_possible = (interaction.user.id == self.gamble_starter.id) or str(interaction.user.id) in list(os.environ.get("OWNERS").split(","))
        
        # send message if usr cannot interact with button
        if not is_possible:
            await interaction.response.send_message(random.choice(responses), ephemeral=True)
        
        return is_possible
    

class BulletSelect(discord.ui.Select):
    def __init__(self, gamble_starter, opponent, amount):
        options = [
            discord.SelectOption(label=str(i), value=str(i)) for i in range(1, 7)
        ]
        super().__init__(placeholder="Pick the number of bullets", options=options)

        self.gamble_starter = gamble_starter
        self.opponent = opponent
        self.amount = amount

    async def callback(self, interaction: discord.Interaction):
        bullets = int(self.values[0])
        
        embed = embeds.DefaultEmbed(
            "💥 Pulling the trigger...",
            f"You are playing with **{bullets}** bullets in the chamber"
        )
        images = [
            "https://media.tenor.com/fklGVnlUSFQAAAAM/russian-roulette.gif",
            "https://i.gifer.com/Hmk7.gif",
            "https://media.tenor.com/nDYDbjcSDZMAAAAM/gru-gun-point.gif",
            "https://i.imgur.com/SavjtWP.gif",
            "https://64.media.tumblr.com/6e6bacf4c0410e487dc40fbfe7d77636/6d084d98424e0608-1b/s540x810/b04e0438e043723874956e6d180b263c1b081c02.gifv"
        ]
        embed.set_image(url=random.choice(images))
        await interaction.response.edit_message(embed=embed, view=None)

        await asyncio.sleep(3)

        # Kans berekenen (bullets/6)
        loser = self.gamble_starter if random.randint(0, 5) < bullets else self.opponent
        winner = self.opponent if loser == self.gamble_starter else self.gamble_starter

        # Odds toewijzen
        win_odds = {1: 0.25, 2: 0.5, 3: 1, 4: 1.5, 5: 1.75, 6: 2}
        lose_odds = {1: 1.75, 2: 1.5, 3: 1, 4: 0.5, 5: 0.25, 6: 2}

        pushups_to_add = int(self.amount * (lose_odds[bullets] if loser == self.gamble_starter else win_odds[bullets]))

        # Resultaat embed
        if loser == self.gamble_starter:
            result_embed = embeds.DefaultEmbed(
                f"💀 RIP! You died to {winner.display_name}!",
                f"Well, at least you didn't die as a degenerate gambling addict... right?"
            )
        else:
            result_embed = embeds.DefaultEmbed(
                f"🍀 PHEW! You survived agains {loser.display_name}!",
                "Pussy boy doesn't dare to go again... **(pussyyyyyyyy)**"
            )
        result_embed.set_thumbnail(url=winner.display_avatar.url)

        # Push-ups opslaan
        await db_manager.add_pushups(loser.id, pushups_to_add)
        if loser.id != self.gamble_starter.id:
            await send_dm_pushups(loser, self.gamble_starter, pushups_to_add, 'Russian Roulette')

        # Resultaten weergeven
        result_embed.add_field(
            name="💪 Pushups added",
            value=f"```{loser} has been given {pushups_to_add} pushups```"
        )

        await interaction.edit_original_response(embed=result_embed, view=None)


class RPSView(discord.ui.View):
    def __init__(self, player1, player2, amount):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.amount = amount
        self.choices = {}
        self.add_buttons()

    def add_buttons(self):
        for name, emoji in [("rock", "🪨"), ("paper", "📜"), ("scissors", "✂️")]:
            button = discord.ui.Button(label=name.capitalize(), emoji=emoji, custom_id=name)
            button.callback = self.button_callback
            self.add_item(button)

    async def button_callback(self, interaction: discord.Interaction):
        # Ensure only the participants can play
        if interaction.user not in [self.player1, self.player2]:
            return await interaction.response.send_message(
                "You're not a participant in this game!", ephemeral=True
            )

        # Record the player's choice
        self.choices[interaction.user] = interaction.data["custom_id"]

        # Check if both players have made their choice
        if len(self.choices) == 2:
            await self.process_results(interaction)
        else:
            await interaction.response.send_message(
                f"{interaction.user.mention} has chosen! Waiting for the other player...", ephemeral=True
            )

    async def process_results(self, interaction: discord.Interaction):
        # Disable buttons after the game is decided
        for child in self.children:
            child.disabled = True

        # Get the choices
        p1_choice = self.choices[self.player1]
        p2_choice = self.choices[self.player2]

        # Determine the winner
        winner = self.get_winner(p1_choice, p2_choice)

        if winner == "draw":
            result = "It's a draw! 🤝\nBoth players have to do pushups!"

            # Add pushups to both players
            await db_manager.add_pushups(self.player1.id, self.amount)
            await db_manager.add_pushups(self.player2.id, self.amount)

            total_pushups_p1 = await db_manager.get_pushups(self.player1.id)
            total_pushups_p2 = await db_manager.get_pushups(self.player2.id)

            pushup_embed = embeds.DefaultEmbed(
                "🏅 It's a draw!",
                f"Both {self.player1.mention} and {self.player2.mention} have pushups to do!"
            )

            pushup_embed.add_field(
                name=f"💪 {self.player1.display_name} pushups",
                value=f"```{self.amount}``` \n```Total: {total_pushups_p1}```",
                inline=True
            )

            pushup_embed.add_field(
                name=f"💪 {self.player2.display_name} pushups",
                value=f"```{self.amount}``` \n```Total: {total_pushups_p2}```",
                inline=True
            )

        else:
            loser = self.player1 if winner != self.player1 else self.player2
            result = f"{winner.mention} wins! 🎉\n{loser.mention} gets the pushups!"

            await db_manager.add_pushups(loser.id, self.amount)
            total_pushups = await db_manager.get_pushups(loser.id)

            pushup_embed = embeds.DefaultEmbed(
                f"🏅 {winner} won!", f"{loser.mention} has {total_pushups} pushups to do", user=winner
            )

            pushup_embed.add_field(
                name="💪 Added pushups",
                value=f"```{self.amount}```",
                inline=True
            )

            pushup_embed.add_field(
                name="📊 Total remaining pushups",
                value=f"```{total_pushups}```",
                inline=True
            )

        # Send the results
        embed = discord.Embed(
            title="Rock-Paper-Scissors Results",
            description=(
                f"{self.player1.mention} chose {self.get_emoji(p1_choice)}\n"
                f"{self.player2.mention} chose {self.get_emoji(p2_choice)}\n\n{result}"
            ),
            color=discord.Color.green(),
        )
        await interaction.response.edit_message(embed=embed, view=self)
        await interaction.followup.send(embed=pushup_embed)


    def get_winner(self, p1, p2):
        """Determines the winner based on the game rules."""
        rules = {
            "rock": "scissors",
            "scissors": "paper",
            "paper": "rock",
        }
        if p1 == p2:
            return "draw"
        return self.player1 if rules[p1] == p2 else self.player2

    def get_emoji(self, choice):
        """Returns the emoji for a given choice."""
        return {"rock": "🪨", "paper": "📜", "scissors": "✂️"}.get(choice, "❓")


class MinesView(discord.ui.View):

    ODDS = [
        [1.03, 1.08, 1.12, 1.18, 1.24, 1.3, 1.37, 1.46, 1.55, 1.65, 1.77, 1.9, 2.06, 2.25, 2.47, 2.75, 3.09, 3.54, 4.12, 4.95, 6.19, 8.25, 12.38],
        [1.08, 1.17, 1.29, 1.41, 1.65, 1.74, 1.94, 2.18, 2.47, 2.83, 3.26, 3.81, 4.5, 5.4, 6.6, 8.25, 10.61, 14.14, 19.8, 29.7, 49.5, 99],
        [1.12, 1.29, 1.48, 1.71, 2, 2.35, 2.79, 3.35, 4.07, 5, 6.26, 7.96, 10.35, 13.8, 18.97, 27.11, 40.66, 65.06, 113.85, 227.7, 569.25],
        [1.18, 1.41, 1.71, 2.09, 2.58, 3.23, 4.09, 5.26, 6.88, 9.17, 12.51, 17.52, 25.3, 37.95, 59.64, 99.39, 178.91, 357.81, 834.9, 2504.7],
        [1.24, 1.56, 2, 2.58, 3.39, 4.52, 6.14, 8.5, 12.04, 17.52, 26.27, 40.87, 66.41, 113.85, 208.72, 417.45, 939.26, 2504.7, 8766.45],
        [1.3, 1.74, 2.35, 3.23, 4.52, 6.46, 9.44, 14.17, 21.89, 35.03, 58.38, 102.17, 189.75, 379.5, 834.9, 2087.25, 6261.75, 25047],
        [1.37, 1.94, 2.79, 4.09, 6.14, 9.44, 14.95, 24.47, 41.6, 73.95, 138.66, 277.33, 600.87, 1442.1, 3965.77, 13219.25, 59486.62],
        [1.46, 2.18, 3.35, 5.26, 8.5, 14.17, 24.47, 44.05, 83.2, 166.4, 356.56, 831.98, 2163.15, 6489.45, 23794.65, 118973.25],
        [1.55, 2.47, 4.07, 6.88, 12.04, 21.89, 41.6, 83.2, 176.8, 404.1, 1010.26, 2828.73, 9193.39, 36773.55, 202254.52],
        [1.65, 2.83, 5, 9.17, 17.52, 35.03, 73.95, 166.4, 404.1, 1077.61, 3232.84, 11314.94, 49031.4, 294188.4],
        [1.77, 3.26, 6.26, 12.51, 26.27, 58.38, 138.66, 356.56, 1010.26, 3232.84, 12123.15, 56574.69, 367735.5],
        [1.9, 3.81, 7.96, 17.52, 40.87, 102.17, 277.33, 831.98, 2828.73, 11314.94, 56574.69, 396022.85],
        [2.06, 4.5, 10.35, 25.3, 66.41, 189.75, 600.87, 2163.15, 9193.39, 49031.4, 367735.5],
        [2.25, 5.4, 13.8, 37.95, 113.85, 379.5, 1442.1, 6489.45, 36773.55, 294188.4],
        [2.47, 6.6, 18.97, 59.64, 208.72, 834.9, 3965.77, 23794.65, 202254.52],
        [2.75, 8.25, 27.11, 99.39, 417.45, 2087.25, 13219.25, 118973.25],
        [3.09, 10.61, 40.66, 178.91, 939.26, 6261.75, 59486.62],
        [3.54, 14.14, 65.06, 357.81, 2504.7, 25047],
        [4.12, 19.8, 113.85, 834.9, 8766.45],
        [4.95, 29.7, 277.7, 2504.7],
        [6.19, 49.5, 593.25],
        [8.25, 99],
        [12.37]
    ]
    ODDS = [[round(value * 3, 2) for value in row] for row in ODDS]

    def __init__(self, player1, player2, mines_amount):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.mines_amount = mines_amount
        self.tiles_left = 24 - mines_amount
        self.pushups = 1  # Start multiplier
        self.selected_tiles = 0

        # Randomly select the positions for mines (excluding the last button)
        self.buttons = []
        mines = random.sample(range(24), mines_amount)

        for i in range(24):
            is_mine = i in mines
            button = discord.ui.Button(
                label="❓",
                style=discord.ButtonStyle.blurple,
                row=i // 5,
                custom_id=f"button_{i}_mine_{is_mine}"
            )
            button.callback = self.button_click

            self.buttons.append(button)
            self.add_item(button)

        # The last button is the cashout button
        self.cashout_button = discord.ui.Button(
            label="💰 Cashout", 
            style=discord.ButtonStyle.green, 
            row=i // 5, 
            custom_id="cashout"
        )
        self.cashout_button.callback = self.cashout_click
        self.cashout_button.disabled = True

        self.buttons.append(self.cashout_button)
        self.add_item(self.cashout_button)

    async def button_click(self, interaction: discord.Interaction):
        """Verwerkt een klik op een tegel."""
        custom_id = interaction.data['custom_id']
        button_index = int(custom_id.split('_')[1])
        is_mine = custom_id.split('_')[3] == 'True'

        button = self.buttons[button_index]
        button.disabled = True

        if is_mine:
            button.style = discord.ButtonStyle.danger
            button.label = "💣"
            return await self.end_game(interaction, win=False)

        self.cashout_button.disabled = False

        # Bereken de pushups voor de huidige veilige tegel volgens de formule
        self.pushups = self.calculate_pushups()

        # Field is safe, update button and values
        button.style = discord.ButtonStyle.success
        button.label = "🏳️"
        self.tiles_left -= 1
        self.selected_tiles += 1

        # If no tiles are left, the game ends
        if self.tiles_left == 0:
            return await self.end_game(interaction, win=True)

        # Update embed met de huidige toestand
        embed = interaction.message.embeds[0]

        # Update the 'Next Tile Pushups' field value, if it exists, otherwise add it
        next_pushups= self.calculate_pushups() # we calculate pushups again because the tiles left and selected tiles changed
        embed.clear_fields()
        embed.add_field(
            name="*Mines*",
            value=f"```{self.mines_amount}```"
        )
        embed.add_field(
            name="*Safe Tiles left*",
            value=f"```{self.tiles_left}```",
            inline=True
        )
        embed.add_field(
            name="*Pushups so far*",
            value=f"```{self.pushups:.2f}```",
            inline=False
        )
        embed.add_field(
            name="*Next Tile Pushups*",
            value=f"```{next_pushups}```",
            inline=True
        )

        await interaction.response.edit_message(embed=embed, view=self)

    async def cashout_click(self, interaction: discord.Interaction):
        """Handles the cashout button, stopping the game without penalties."""
        await self.end_game(interaction, win=True, cashout=True)

    async def end_game(self, interaction, win, cashout=False):
        """Einde van het spel."""
        for button in self.buttons:
            button.disabled = True

        self.flip_tiles()

        if cashout:
            embed = embeds.DefaultEmbed(
                "💰 Cashout!", 
                f"{self.player1.mention} chose to cash out safely against {self.player2.mention}!",
            )
            embed.add_field(
                name="💪 Pushups given:",
                value=f"```{round(self.pushups)}```"
            )
            embed.set_thumbnail(url=self.player1.display_avatar.url)
            await db_manager.add_pushups(self.player2.id, round(self.pushups))

        else:
            winner = self.player1 if win else self.player2
            loser = self.player2 if win else self.player1

            await db_manager.add_pushups(loser.id, round(self.pushups))
            total = await db_manager.get_pushups(loser.id)

            # Stuur DM naar loser dat hij pushups heeft gekregen
            if loser.id != self.player1.id:
                await send_dm_pushups(self.player2, self.player1, round(self.pushups), 'Mines')

            embed = embeds.DefaultEmbed(
                f"🏅 {winner} won!", 
                f"{loser.mention} has a total of {total} pushups.", 
                user=winner,
            )
            embed.add_field(
                name="💪 Added pushups",
                value=f"```{int(self.pushups)}```",
                inline=True
            )
            embed.set_thumbnail(url=winner.display_avatar.url)

        await interaction.response.edit_message(embed=embed, view=self)

    def flip_tiles(self):
        for button in self.buttons:
            try:
                is_mine = button.custom_id.split('_')[3] == 'True'
                if is_mine:
                    button.label = "💣"
                else:
                    button.label = "🏳️"
            except:
                pass
    
    def calculate_pushups(self):
        """Calculate the pushups for the current tile."""
        return round(MinesView.ODDS[self.mines_amount-1][self.selected_tiles], 2)
    
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
        is_possible = (interaction.user.id == self.player1.id) or str(interaction.user.id) in list(os.environ.get("OWNERS").split(","))
        
        # send message if usr cannot interact with button
        if not is_possible:
            await interaction.response.send_message(random.choice(responses), ephemeral=True)
        
        return is_possible


class ResetCooldownView(discord.ui.View):
    def __init__(self, image, user, cooldown, bot):
        super().__init__(timeout=None)
        self.image = image
        self.user = user
        self.cooldown = cooldown
        self.bot = bot

    @discord.ui.button(label="Reset Cooldown", style=discord.ButtonStyle.primary, emoji="⏲️")
    async def reset_cooldown_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        await db_manager.add_pushups(self.user.id, 20)
        total = await db_manager.get_pushups(self.user.id)
        self.cooldown.reset()

        pushup_group = self.bot.tree.get_command("pushup")
        gamble_command = pushup_group.get_command("gamble")

        embed = embeds.OperationSucceededEmbed("Cooldown Reset", f"🥳 Congratulations! You are a crippling gambling addict. You also have 20 extra pushups to complete, making a total of {total} pushups.\n\nGamble again: {getClickableCommand(gamble_command, self.bot.command_ids)}")
        embed.set_image(url=self.image)
        await interaction.response.edit_message(
            embed=embed,
            view=None
        )
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
        is_possible = (interaction.user.id == self.user.id) or str(interaction.user.id) in list(os.environ.get("OWNERS").split(","))
        
        # send message if usr cannot interact with button
        if not is_possible:
            await interaction.response.send_message(random.choice(responses), ephemeral=True)
        
        return is_possible

async def send_dm_pushups(user, giver, pushups, game_type):
    """Sends a user a DM that they have been given pushups

    Args:
        user (discord.User): Who has been given pushups
        giver (_type_): Who has given the pushups
        pushups (int): how many pushups
        game_type (str): the game type
    """
    embed = embeds.DefaultEmbed(
        "💪 You have been given pushups!",
    )
    embed.add_field(
        name="👤 Given by",
        value=giver.mention
    )
    embed.add_field(
        name="🎲 Game played",
        value=game_type
    )
    embed.add_field(
        name="🦍 Amount",
        value=str(pushups)
    )

    await user.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Gamble(bot))