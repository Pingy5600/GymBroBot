import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from autocomplete import exercise_autocomplete, getMetaFromExercise
from databank import db_manager
from embeds import (DefaultEmbed, DefaultEmbedWithExercise, Paginator,
                    PRFieldGenerator, TopPRFieldGenerator)
from exceptions import NoEntries, TimeoutCommand
from helpers import getDiscordTimeStamp, ordinal, setGraph
from validations import (validateAndCleanWeight, validateDate,
                         validateEntryList, validateNotBot,
                         validatePermissions, validateUserList)

POOL = ThreadPoolExecutor()

class PR(commands.Cog, name="pr"):
    def __init__(self,bot):
        self.bot = bot
        self.title = "💪 PR"

    command_pr_group = discord.app_commands.Group(name="pr", description="pr Group")


    @command_pr_group.command(name="add", description="adds pr to the user's name")
    @discord.app_commands.describe(date="The date of the pr", pr="The personal record value", exercise="Which exercise", user="Which user")
    @discord.app_commands.autocomplete(exercise=exercise_autocomplete)
    async def add_pr(self, interaction: discord.Interaction, pr: str, exercise: str, date: str = None, user: discord.User = None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)
        pr = validateAndCleanWeight(pr)
        date_obj = validateDate(date)

        resultaat = await db_manager.add_pr(user.id, exercise, pr, date_obj)

        if not resultaat[0]:
            raise Exception(resultaat[1])
        
        exercise_meta = getMetaFromExercise(exercise)

        embed = DefaultEmbedWithExercise(
            title="PR added!",
            image_url=exercise_meta.get('image'),
            description=f"PR of {pr}kg added"
        )
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Excercise", value=exercise_meta.get('pretty-name'), inline=True)
        embed.add_field(name="Date", value=getDiscordTimeStamp(date_obj), inline=True)

        return await interaction.followup.send(embed=embed)


    @command_pr_group.command(name="list", description="Gives PR of the given user")
    @discord.app_commands.describe(user="Which user", exercise="Which exercise")
    @discord.app_commands.autocomplete(exercise=exercise_autocomplete)
    async def list(self, interaction: discord.Interaction, exercise: str, user: discord.User = None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)

        exercise_meta: dict[str, str] = getMetaFromExercise(exercise)

        # Haal de PR's op van de gebruiker voor het opgegeven oefening
        prs = await db_manager.get_prs_from_user(str(user.id), exercise)
        validateEntryList(prs, f"No PRs found for the exercise {exercise_meta.get('pretty-name')}.")

        paginator = Paginator(
            items=prs,
            user=user,
            title=f"{exercise_meta.get('pretty-name')} PRs of {user.display_name}",
            generate_field_callback=PRFieldGenerator.generate_field,
            exercise_url=exercise_meta.get('image')
        )

        # Genereer en stuur de embed
        embed = await paginator.generate_embed()
        await interaction.followup.send(embed=embed, view=paginator)


    @command_pr_group.command(name="delete", description="Delete a specific PR")
    @discord.app_commands.describe(exercise="Exercise for the PR", user="Which user")
    @discord.app_commands.autocomplete(exercise=exercise_autocomplete)
    async def delete_pr(
        self, 
        interaction: discord.Interaction, 
        exercise: str,
        user: discord.Member = None
    ):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)
        validatePermissions(user, interaction)

        exercise_meta = getMetaFromExercise(exercise)
        
        # Haal de PR's op van de gebruiker voor de opgegeven oefening
        prs = await db_manager.get_prs_from_user(str(user.id), exercise)
        validateEntryList(prs, f"No PRs found for the exercise {exercise_meta.get('pretty-name')}.")

        paginator = Paginator(
            items=prs,
            user=user,
            title=f"{exercise_meta.get('pretty-name')} PRs of {user.display_name}",
            generate_field_callback=PRFieldGenerator.generate_field,
            exercise_url=exercise_meta.get('image')
        )
        
        # Genereer de embed asynchroon door await te gebruiken
        embed = await paginator.generate_embed()  # Dit is nu een coroutine
        content = "Reply with the **number** of the PR you want to delete."
        message = await interaction.followup.send(content=content, embed=embed, view=paginator)

        # Bewaar de message_id om de gebruiker te controleren
        message_id = message.id

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit() and m.reference is not None and m.reference.message_id == message_id

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60.0)
            index = int(msg.content) - 1  # Haal de index van de PR uit het bericht

        except asyncio.TimeoutError:
            raise TimeoutCommand()

        if index < 0 or index >= len(prs):
            raise ValueError("Invalid selection. Please try again.")

        # Verkrijg de geselecteerde PR en probeer deze te verwijderen
        selected_pr_index, selected_pr_exercise, selected_pr_weight, selected_pr_time = prs[index]
        result, err = await db_manager.delete_pr(selected_pr_index)
        if not result:
            raise Exception(err)

        # Maak een embed om te bevestigen dat de PR is verwijderd
        embed = DefaultEmbed(
            title="PR Deleted",
            description=f"Successfully deleted the PR: {selected_pr_weight} kg on {getDiscordTimeStamp(selected_pr_time)}."
        )
        await interaction.followup.send(embed=embed)


    @command_pr_group.command(name="graph", description="Generate a graph of PRs for the given users and exercise")
    @discord.app_commands.describe(
        exercise="Which exercise",
        time="How long should the graph show",
        user_a="First user",
        user_b="Second user",
        user_c="Third user",
        user_d="Fourth user",
        user_e="Fifth user",
        user_f="Sixth user",
        user_g="Seventh user",
        user_h="Eight user"
    )
    @discord.app_commands.autocomplete(exercise=exercise_autocomplete)
    @discord.app_commands.choices(time=[
        discord.app_commands.Choice(name="Past Year", value=0),
        discord.app_commands.Choice(name="All Time", value=1)
    ])
    async def graph(
        self,
        interaction: discord.Interaction,
        exercise: str,
        time: discord.app_commands.Choice[int] = None,
        user_a: discord.User = None,
        user_b: discord.User = None,
        user_c: discord.User = None,
        user_d: discord.User = None,
        user_e: discord.User = None,
        user_f: discord.User = None,
        user_g: discord.User = None,
        user_h: discord.User = None
    ):
        await interaction.response.defer(thinking=True)

        # Maak een lijst van gebruikers
        users = [user for user in [user_a, user_b, user_c, user_d, user_e, user_f, user_g, user_h] if user]

        if not users:
            users.append(interaction.user)  # Voeg de aanvrager toe als geen gebruikers zijn gespecificeerd

        for user in users:
            validateNotBot(user)
            
        if not users:
            users.append(interaction.user)  # Voeg de aanvrager toe als geen gebruikers zijn gespecificeerd
        
        validateUserList(users)

        exercise_meta = getMetaFromExercise(exercise)

        if time is None or time.value == 0:
            time_name = "The past year" if time is None else time.name
            time_limit = timedelta(weeks=52)

        elif time.value == 1:
            time_name = time.name
            time_limit = timedelta(weeks=20000)

        threshold_datetime = datetime.now() - time_limit

        # Haal PR's op voor elke gebruiker
        users_prs = []
        for user in users:
            prs = await db_manager.get_prs_from_user(str(user.id), exercise)
            if prs and prs[0] != -1:
                # filter based on selected time
                filtered_prs = [record for record in prs if record[3] >= threshold_datetime]
                if len(filtered_prs) > 0:
                    users_prs.append((user, filtered_prs))                    

        if not users_prs:
            raise NoEntries(f"No PRs found for the specified users and the exercise {exercise_meta.get('pretty-name')} in this timeperiod.")
        
        # Stuur de grafiek als bestand
        embed = DefaultEmbed(
            title=f"{exercise_meta.get('pretty-name')} PR Graph",
            description=f"Here's the progress for {', '.join(user.display_name for user, _ in users_prs)}."
        )
        embed.set_footer(text=f"The PRs are limited to: {time_name}")
        message = await interaction.followup.send(embed=embed)

        # Genereer de grafiek, in task zodat thread niet geblocked is
        loop = asyncio.get_event_loop()
        loop.create_task(
            setGraph(POOL, loop, message, users_prs, embed)
        )


    @discord.app_commands.command(name="top", description="Gives a list of everyone's top PRs")
    @discord.app_commands.describe(exercise="Which exercise")
    @discord.app_commands.autocomplete(exercise=exercise_autocomplete)
    async def top(self, interaction: discord.Interaction, exercise: str):
        await interaction.response.defer(thinking=True)

        exercise_meta = getMetaFromExercise(exercise)

        prs = await db_manager.get_top_prs(exercise)
        validateEntryList(prs, f"No PRs found for the exercise '{exercise_meta.get('pretty-name')}'.")

        paginator = Paginator(
            items=prs,
            user=interaction.user,
            title=f"Top {exercise_meta.get('pretty-name')} PRs",
            generate_field_callback=TopPRFieldGenerator.generate_field,
            exercise_url=exercise_meta.get('image')
        )

        embed = await paginator.generate_embed(interaction.client)  
        await interaction.followup.send(embed=embed, view=paginator)


    @discord.app_commands.command(name="statistics", description="Get a detailed analysis about an exercise")
    @discord.app_commands.describe(user="Which user", exercise="Which exercise")
    @discord.app_commands.autocomplete(exercise=exercise_autocomplete)
    async def statistic(self, interaction: discord.Interaction, exercise: str, user: discord.User=None):
        await interaction.response.defer(thinking=True)

        if user == None:
            user = interaction.user

        validateNotBot(user) 

        exercise_meta = getMetaFromExercise(exercise)

        embed = DefaultEmbedWithExercise(
            f"{exercise_meta.get('pretty-name')} analysis for {user}",
            image_url=exercise_meta.get('image')
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
                name=f"📈 Progression rate (past year)",
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


async def setup(bot):
    await bot.add_cog(PR(bot))