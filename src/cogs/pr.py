import asyncio
import math
from concurrent.futures import ThreadPoolExecutor

import dateparser
import discord
from discord.ext import commands

from databank import db_manager
from embeds import DefaultEmbed, DefaultEmbedWithExercise
from exceptions import InvalidDate, NoEntries, TimeoutCommand
from helpers import EXERCISE_CHOICES, getDiscordTimeStamp, ordinal, setGraph
from validations import (validateAndCleanWeight, validateEntryList,
                         validateNotBot, validatePermissions, validateUserList)

POOL = ThreadPoolExecutor()

class PR(commands.Cog, name="pr"):
    def __init__(self,bot):
        self.bot = bot

    command_pr_group = discord.app_commands.Group(name="pr", description="pr Group")

    @command_pr_group.command(name="add", description="adds pr to the user's name")
    @discord.app_commands.describe(date="The date of the pr", pr="The personal record value", exercise="Which exercise", user="Which user")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def add_pr(self, interaction: discord.Interaction, pr: str, exercise: str, date: str = None, user: discord.User = None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)
        pr = validateAndCleanWeight(pr)

        if date is None:
            date = 'vandaag'

        try:    
            date_obj = dateparser.parse(date, settings={
                'DATE_ORDER': 'DMY',
                'TIMEZONE': 'CET',
                'PREFER_DAY_OF_MONTH': 'first',
                'PREFER_DATES_FROM': 'past',
                'DEFAULT_LANGUAGES': ["en", "nl"]
            })

            if date_obj is None:
                raise ValueError("Invalid date format")

        except ValueError:
            raise InvalidDate()

        resultaat = await db_manager.add_pr(user.id, exercise, pr, date_obj)

        if not resultaat[0]:
            raise Exception(resultaat[1])

        embed = DefaultEmbedWithExercise(
            title="PR added!",
            exercise=exercise,
            description=f"PR of {pr}kg added"
        )
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Excercise", value=exercise, inline=True)
        embed.add_field(name="Date", value=getDiscordTimeStamp(date_obj), inline=True)

        return await interaction.followup.send(embed=embed)


    @command_pr_group.command(name ="list", description ="Gives pr of the given user")
    @discord.app_commands.describe(user="Which user", exercise="which exercise")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def list(self, interaction: discord.Interaction, exercise: str, user: discord.User=None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)

        prs = await db_manager.get_prs_from_user(str(user.id), exercise)
        validateEntryList(prs, "No PRs found for the specified exercise.")
        
        view = PRPaginator(prs, exercise, user)
        embed = view.generate_embed()

        await interaction.followup.send(embed=embed, view=view)


    @command_pr_group.command(name="delete", description="Delete a specific PR")
    @discord.app_commands.describe(exercise="Exercise for the PR", user="User whose PR to delete")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def delete_pr(
        self, 
        interaction: discord.Interaction, 
        exercise: str, 
        user: discord.User = None
    ):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)
        validatePermissions(user, interaction)
        
        prs = await db_manager.get_prs_from_user(str(user.id), exercise)
        validateEntryList(prs, "No PRs found for the specified exercise.")

        paginator = PRPaginator(prs, exercise, user)
        embed = paginator.generate_embed()
        content = "Reply with the **number** of the PR you want to delete."
        message = await interaction.followup.send(content=content, embed=embed, view=paginator)

        # Save the message_id
        message_id = message.id

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit() and m.reference is not None and m.reference.message_id == message_id

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60.0)
            index = int(msg.content) - 1

        except asyncio.TimeoutError:
            raise TimeoutCommand()
        
        if index < 0 or index >= len(prs):
            raise ValueError("Invalid selection. Please try again.")

        selected_pr = prs[index]
        result, err = await db_manager.delete_pr(str(user.id), exercise, selected_pr[2])
        if not result:
            raise Exception(err)

        embed = DefaultEmbed(
            title="PR Deleted",
            description=f"Successfully deleted the PR: {selected_pr[1]} kg on {getDiscordTimeStamp(selected_pr[2])}."
        )
        await interaction.followup.send(embed=embed)



    @command_pr_group.command(name="graph", description="Generate a graph of PRs for the given users and exercise")
    @discord.app_commands.describe(
        exercise="Which exercise",
        user_a="First user",
        user_b="Second user",
        user_c="Third user",
        user_d="Fourth user",
        user_e="Fifth user"
    )
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def graph(
        self,
        interaction: discord.Interaction,
        exercise: str,
        user_a: discord.User = None,
        user_b: discord.User = None,
        user_c: discord.User = None,
        user_d: discord.User = None,
        user_e: discord.User = None
    ):
        await interaction.response.defer(thinking=True)

        # Maak een lijst van gebruikers
        users = [user for user in [user_a, user_b, user_c, user_d, user_e] if user]

        if not users:
            users.append(interaction.user)  # Voeg de aanvrager toe als geen gebruikers zijn gespecificeerd

        for user in users:
            validateNotBot(user)
            
        if not users:
            users.append(interaction.user)  # Voeg de aanvrager toe als geen gebruikers zijn gespecificeerd
        
        validateUserList(users)

        # Haal PR's op voor elke gebruiker
        users_prs = []
        for user in users:
            prs = await db_manager.get_prs_from_user(str(user.id), exercise)
            if prs and prs[0] != -1:  # Controleer op fouten
                users_prs.append((user, prs))

        if not users_prs:
            raise NoEntries("No PRs found for the specified users and exercise.")
        
        # Stuur de grafiek als bestand
        embed = DefaultEmbed(
            title=f"{exercise.capitalize()} PR Graph",
            description=f"Here's the progress for {', '.join(user.display_name for user, _ in users_prs)}."
        )
        message = await interaction.followup.send(embed=embed)

        # Genereer de grafiek, in task zodat thread niet geblocked is
        loop = asyncio.get_event_loop()
        loop.create_task(
            setGraph(POOL, loop, message, users_prs, embed)
        )


    @discord.app_commands.command(name="statistics", description="Get a detailed analysis about an exercise")
    @discord.app_commands.describe(user="Which user", exercise="Which exercise")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def statistic(self, interaction: discord.Interaction, exercise: str, user: discord.User=None):
        await interaction.response.defer(thinking=True)

        if user == None:
            user = interaction.user

        validateNotBot(user)

        embed = DefaultEmbedWithExercise(
            f"{exercise.capitalize()} analysis for {user}",
            exercise=exercise
        )

        # max of exercise
        try:
            success, resultsOrErr = await db_manager.getMaxOfUserWithExercise(str(user.id), exercise)
            if not success: raise ValueError(resultsOrErr)

            weight, timestamp = resultsOrErr
            embed.add_field(
                name=f"💪 Max Lift",
                value=f"**{weight} kg **({getDiscordTimeStamp(timestamp)})",
                inline=False
            )

        except Exception as err:
            embed.add_field(
                name=f"💪 Max Lift",
                value=f"No lifts registered yet...",
                inline=True
            )

        # position in relation to every user in db
        try:
            success, positionOrErr = await db_manager.getPositionOfUserWithExercise(str(user.id), exercise)
            if not success: raise ValueError(resultsOrErr)

            emoji_map = ["🥇", "🥈", "🥉"]

            weight, timestamp = resultsOrErr
            embed.add_field(
                name=f"{emoji_map[positionOrErr-1] if positionOrErr <= 3 else '🏆'} Position",
                value=f"**{ordinal(positionOrErr)}**",
                inline=True
            )

        except Exception as err:
            self.bot.logger.warning(f"Error in /statistic position: {err}")
            pass
        
        try:
            success, closestOrErr = await db_manager.getClosestUsersWithExercise(str(user.id), exercise)
            if not success:
                raise ValueError(closestOrErr)

            user_below, user_above = closestOrErr
            # Haal de namen en gewichten van de dichtstbijzijnde gebruikers
            user_below_info = f"<@{user_below[0]}> ({user_below[1]} kg)" if user_below else "No one below"
            user_above_info = f"<@{user_above[0]}> ({user_above[1]} kg)" if user_above else "No one above"

            embed.add_field(
                name="⬇️ Closest Below",
                value=user_below_info,
                inline=True
            )

            embed.add_field(
                name="⬆️ Closest Above",
                value=user_above_info,
                inline=True
            )

        except Exception as err:
            self.bot.logger.warning(f"Error in /statistic closest: {err}")

        try:
            success, rateOrErr = await db_manager.getExerciseProgressionRate(str(user.id), exercise)
            if not success: raise ValueError(rateOrErr)

            embed.add_field(
                name=f"📈 Progression rate (past 6 months)",
                value=f"Average weekly rate: **{rateOrErr} kg**",
                inline=True
            )

        except Exception as err:
            self.bot.logger.warning(f"Error in /statistic rate: {err}")
            pass

        message = await interaction.followup.send(embed=embed)

        try:
            prs = await db_manager.get_prs_from_user(str(user.id), exercise)
            if prs and prs[0] != -1:  # Controleer op fouten
                loop = asyncio.get_event_loop()
                loop.create_task(
                    setGraph(POOL, loop, message, [(user, prs)], embed)
                )

        except:
            self.bot.logger.warning(f"Error in /statistic graph: {err}")
            pass


class PRPaginator(discord.ui.View):
    def __init__(self, prs, exercise, user):
        super().__init__()
        self.prs = prs
        self.exercise = exercise
        self.user = user
        self.current_page = 0
        self.items_per_page = 10
        self.max_pages = math.ceil(len(prs) / self.items_per_page)

        if self.max_pages <= 1:
            self.clear_items()  # If only 1 page, remove buttons entirely

    def generate_embed(self):
        embed = DefaultEmbedWithExercise(
            title=f"{self.exercise.capitalize()} PRs of {self.user.display_name}",
            exercise=self.exercise
        )

        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_prs = self.prs[start:end]

        for idx, pr in enumerate(page_prs, start=start + 1):  # Voeg nummers toe aan de PR's
            weight = pr[1]
            # Format weight to two decimal places if it is a decimal number
            if weight % 1 != 0:  # If it is a decimal
                weight = f"{weight:.2f}"
            else:
                weight = f"{int(weight)}"  # Remove decimals if it's an integer

            timestamp = getDiscordTimeStamp(pr[2])
            embed.add_field(
                name=f"{idx}. {timestamp}",  # Nummer voor de datum
                value=f"**Weight:** {weight} kg",
                inline=False
            )

        embed.set_footer(text=f"Page {self.current_page + 1} of {self.max_pages}")
        return embed


    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            embed = self.generate_embed()
            self.update_buttons()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            embed = self.generate_embed()
            self.update_buttons()
            await interaction.response.edit_message(embed=embed, view=self)

    def update_buttons(self):
        # Disable buttons based on the current page
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.max_pages - 1

        # If there's only one page, remove the buttons completely
        if self.max_pages <= 1:
            self.clear_items()  # Remove the buttons if there's only 1 page


async def setup(bot):
    await bot.add_cog(PR(bot))