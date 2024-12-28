import asyncio
import math
from concurrent.futures import ThreadPoolExecutor

import dateparser
import discord
from discord.ext import commands

from databank import db_manager
from embeds import DefaultEmbed, DefaultEmbedWithExercise, Paginator, RepFieldGenerator
from exceptions import InvalidDate, TimeoutCommand
from helpers import (EXERCISE_CHOICES, calculate_1rm_table, getDiscordTimeStamp, set3DGraph)
from validations import (validateAndCleanWeight, validateEntryList,validateNotBot, validatePermissions, validateReps, validateUserList)

POOL = ThreadPoolExecutor()

class Rep(commands.Cog, name="rep"):
    def __init__(self,bot):
        self.bot = bot
        self.title = "🥵 Rep"

    command_rep_group = discord.app_commands.Group(name="rep", description="rep Group")


    @command_rep_group.command(name="calculator", description="Calculate the amount of reps you should do for your 1RM")
    @discord.app_commands.describe(exercise="which exercise", user="Which user")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def rep_calc(self, interaction: discord.Interaction, exercise: str, user: discord.User=None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)

        # get 1RM for that exercise for user
        success, resultsOrErr = await db_manager.getMaxOfUserWithExercise(str(user.id), exercise)
        if not success: raise ValueError(resultsOrErr)
        
        one_rep_max, date = resultsOrErr

        table_data = calculate_1rm_table(float(one_rep_max))

        embed = DefaultEmbedWithExercise(
            title="📊 1RM Percentage Table",
            exercise=exercise,
            description=f"Based on a 1RM of **{one_rep_max} kg** achieved on {getDiscordTimeStamp(date)}",
        )
        
        for row in table_data:
            embed.add_field(name=f"{row['reps']} reps at {row['percentage']}", value=row['weight'], inline=False)

        return await interaction.followup.send(embed=embed)
    

    @command_rep_group.command(name="add", description="Adds reps for a specific exercise and weight")
    @discord.app_commands.describe(
        date="The date of the reps",
        reps="The number of reps",
        weight="The weight lifted",
        exercise="Which exercise",
        user="Which user"
    )
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def add_reps(
        self,
        interaction: discord.Interaction,
        reps: int,
        weight: str,
        exercise: str,
        date: str = None,
        user: discord.User = None
    ):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)
        weight = validateAndCleanWeight(weight)
        validateReps(reps)

        if date is None:
            date = "vandaag"
        
        try:
            # Datum verwerken
            date_obj = dateparser.parse(date, settings={
                'DATE_ORDER': 'DMY',
                'TIMEZONE': 'CET',
                'PREFER_DAY_OF_MONTH': 'first',
                'PREFER_DATES_FROM': 'past',
                'DEFAULT_LANGUAGES': ["en", "nl"]
            })

            if date_obj is None:
                raise InvalidDate()

        except ValueError:
            raise InvalidDate()

        # Voeg de reps toe aan de database
        resultaat = await db_manager.add_reps(user.id, exercise, weight, reps, date_obj)

        if not resultaat[0]:
            raise Exception(resultaat[1])
        
        embed = DefaultEmbedWithExercise(
            title="Reps Added!",
            exercise=exercise,
            description=f"Added {reps} reps at {weight}kg for {exercise.capitalize()}."
        )
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Exercise", value=exercise, inline=True)
        embed.add_field(name="Date", value=getDiscordTimeStamp(date_obj), inline=True)

        return await interaction.followup.send(embed=embed)


    @command_rep_group.command(name="list", description="Gives reps of the given user")
    @discord.app_commands.describe(user="Which user", exercise="Which exercise")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def list(self, interaction: discord.Interaction, exercise: str, user: discord.User = None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)

        # Haal de reps op voor de gebruiker en oefening
        reps = await db_manager.get_prs_with_reps(str(user.id), exercise)
        validateEntryList(reps, "No reps found for the specified exercise.")

        paginator = Paginator(
            items=reps,
            user=user,
            title=f"{exercise.capitalize()} Reps of {user.display_name}",
            generate_field_callback=RepFieldGenerator.generate_field,
            exercise=exercise
        )

        embed = paginator.generate_embed()  # Genereer de embed voor de paginatie
        await interaction.followup.send(embed=embed, view=paginator)


    @command_rep_group.command(name="delete", description="Delete specific reps")
    @discord.app_commands.describe(exercise="Exercise", user="User whose reps to delete")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def delete(
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
        
        reps_data = await db_manager.get_prs_with_reps(str(user.id), exercise)
        validateEntryList(reps_data, "No reps found for the specified exercise.")

        paginator = Paginator(
            items=reps_data,
            user=user,
            title=f"{exercise.capitalize()} Reps of {user.display_name}",
            generate_field_callback=RepFieldGenerator.generate_field,
            exercise=exercise
        )

        embed = paginator.generate_embed()
        content = "Reply with the **number** of the rep you want to delete."
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
        
        if index < 0 or index >= len(reps_data):
            raise ValueError("Invalid selection. Please try again.")

        selected_rep = reps_data[index]
        result, err = await db_manager.delete_reps(str(user.id), exercise, selected_rep['weight'], selected_rep['lifted_at'])
        if not result:
            raise Exception(err)

        embed = DefaultEmbed(
            title="Reps Deleted",
            description=f"Successfully deleted **{selected_rep['reps']} reps** of **{int(selected_rep['weight'])} kg** on {getDiscordTimeStamp(selected_rep['lifted_at'])}."
        )
        await interaction.followup.send(embed=embed)


    @command_rep_group.command(name="graph", description="Genereer een 3D-plot van PRs.")
    @discord.app_commands.describe(
        exercise="Which exercise",
        user_a="First user",
        user_b="Second user",
        user_c="Third user",
        user_d="Fourth user",
        user_e="Fifth user"
    )
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def three_d_plot(
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

        # Gebruikers toevoegen aan de lijst
        users = [user for user in [user_a, user_b, user_c, user_d, user_e] if user]
            
        if not users:
            users.append(interaction.user)

        for user in users:
            validateNotBot(user)

        validateUserList(users)

        embed = DefaultEmbed(
            title=f"{exercise.capitalize()} Rep Graph",
            description=f"Here's the 3D graph for {', '.join(user.display_name for user in users)}."
        )
        embed.set_footer(text="This may take a while...")
        message = await interaction.followup.send(embed=embed)

        loop = asyncio.get_event_loop()
        loop.create_task(
            set3DGraph(POOL, loop, message, users, exercise, embed)
        )


async def setup(bot):
    await bot.add_cog(Rep(bot))