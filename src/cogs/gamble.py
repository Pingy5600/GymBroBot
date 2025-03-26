import asyncio
import math
import os
import random

import discord
from discord.ext import commands

from autocomplete import getMetaFromExercise
import checks
import embeds
from helpers import db_manager
from validations import validateAndCleanWeight

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


    @pushup_group.command(name="gamble", description="Give someone pushups", extras={'cog': 'gamble'})
    @discord.app_commands.describe(user="Which user")
    @discord.app_commands.checks.cooldown(rate=100, per=2700, key=lambda i: (i.guild_id, i.user.id))
    @checks.not_in_dm()
    @checks.in_correct_server()
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
            value=f"This is a 50/50. Either you ({interaction.user.mention}) or {user.mention} are banned.",
            inline=True
        )
        gamble_explanation_embed.add_field(
            name="✂️ Rock Paper Scissors",
            value=f"Play Rock Paper Scissors against each other. Loser gets banned."
        )
        gamble_explanation_embed.add_field(
            name="💣 Mines",
            value=f"25 possible mines. You have to guess where they are. If you hit one, you lose."
        )

        await interaction.followup.send(embed=gamble_explanation_embed, view=PushupTypeView(user, interaction.user, self.bot))


class PushupTypeView(discord.ui.View):
    def __init__(self, user, gamble_starter, bot, timeout=180):
        super().__init__(timeout=timeout)
        self.user = user
        self.gamble_starter = gamble_starter
        self.bot = bot

    @discord.ui.button(label="50/50", style=discord.ButtonStyle.blurple, emoji='🎰')
    async def gamble_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        async def callback_func(amount, interaction):
            urls = [
                "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExczV5enBkbTVoNGZoZHUwdmdzdDdjbzFoZ3VoMDA4MTVxdDY2Ymo2byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6jqfXikz9yzhS/giphy.gif",
                "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExemNibW9ra2Njemh5Zm4wZDB4bWQzemhmM2lodjd3cXhyNXZjeXM5eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26uf2YTgF5upXUTm0/giphy.gif",
                "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWVqeXV3OHRpcHNtemx0ODJ4aHh1ZXdhejZ2aXQwN2o0Z21sdHJ3eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qNCtzhsWCc7q4D2FB5/giphy.gif",
                "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmM0am03ejVudHkzejkyODMwaWNjaXg1emtyYThrNGttd2J1cTByYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26ufjXhjqhpFgcONq/giphy.gif",
                "https://media0.giphy.com/media/l2SqgVwLpAmvIfMCA/giphy.gif?cid=ecf05e47mfvwpbejd07zq4l2jyv74wyppg4ik3wnstsra73d&ep=v1_gifs_related&rid=giphy.gif&ct=g",
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
                name="📊 Total pushups",
                value=f"```{total_pushups}```",
                inline=True
            )

            # **Leeg veld om layout consistent te houden**
            result_embed.add_field(name="\u200b", value="\u200b", inline=True)

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
        async def callback_func(amount, interaction):
            view = MinesView(self.gamble_starter, self.user, amount)
            await interaction.response.edit_message(embed=embeds.DefaultEmbed("💣 Mines!", f"Mines left: {view.transform_value(amount)}"), view=view)

        await interaction.response.edit_message(
            embed=embeds.DefaultEmbed(
                "Choose pushup amount!",  
                "10 pushups = click 5 safe spots\n25 pushups = click 10 safe spots\n50 pushups = click 20 safe spots"
            ), 
            view=Amount(self.gamble_starter, self.bot, callback_func)
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
            await interaction.response.send_message(random.choice(responses))
        
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

    @discord.ui.button(label="25", style=discord.ButtonStyle.blurple, row=2, emoji='💪')
    async def amount_25(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_game(interaction, 25)

    @discord.ui.button(label="50", style=discord.ButtonStyle.blurple, row=2, emoji='💪')
    async def amount_50(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.start_game(interaction, 50)

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
                name="📊 Total pushups",
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
    def __init__(self, player1, player2, amount):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.amount = amount
        self.tiles_left = self.transform_value(amount)
        
          # Randomly select 5 positions for mines
        self.buttons = []

        # Create 25 buttons for the grid
        mines = random.sample(range(25), 5)
        for i in range(25):
            is_mine = i in mines
            button = discord.ui.Button(label="❓", style=discord.ButtonStyle.blurple, row=i//5, custom_id=f"button_{i}_mine_{is_mine}")
            button.callback = self.button_click
            self.buttons.append(button)
            self.add_item(button)


    async def button_click(self, interaction: discord.Interaction):
        # check if button is a mine
        custom_id = interaction.data['custom_id']
        button_index = int(custom_id.split('_')[1])  # Extract button index from the custom_id
        is_mine = custom_id.split('_')[3] == 'True'

        for button in self.buttons:
            if button.custom_id == custom_id:
                button.disabled = True

        button = self.buttons[button_index]

        self.tiles_left -= 1
        if self.tiles_left == 0 and not is_mine:
            # End the game
            return await self.end_game(interaction, win=True)

        if is_mine:
            # If it's a mine, turn the button red (bomb)
            button.style = discord.ButtonStyle.danger
            button.label = "💣"
            return await self.end_game(interaction, win=False)
        
        else:
            # If it's not a mine, turn it green (safe) and disable it
            button.style = discord.ButtonStyle.success
            button.label = "🏳️"

        embed = interaction.message.embeds[0]
        embed.description = f"Mines left: {self.tiles_left}"
        await interaction.response.edit_message(embed=embed, view=self)


    async def end_game(self, interaction, win):
        # Disable all buttons
        for button in self.buttons:
            button.disabled = True

        winner = self.player1 if win else self.player2
        loser = self.player2 if win else self.player1

        embed = embeds.DefaultEmbed(
            f"🏅 {winner} won!", 
            f"{loser.mention} has pushups to do", 
            user=winner,
        )
        embed.add_field(
            name="💪 Added pushups",
            value=f"```{self.amount}```",
            inline=True
        )

        await interaction.response.edit_message(embed=embed, view=self)

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

    def transform_value(self, value):
        # Define the transformation rules
        if value == 10:
            return 5
        elif value == 25:
            return 10
        elif value == 50:
            return 15
        else:
            return value  # If no rule applies, return the value as is


async def setup(bot):
    await bot.add_cog(Gamble(bot))