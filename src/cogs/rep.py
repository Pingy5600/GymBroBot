import discord
import dateparser
import math
import asyncio

from discord.ext import commands
from databank import db_manager
from embeds import DefaultEmbed, OperationFailedEmbed
from helpers import getDiscordTimeStamp, setGraph, ordinal, create_1rm_table_embed
from concurrent.futures import ThreadPoolExecutor


class Rep(commands.Cog, name="rep"):
    def __init__(self,bot):
        self.bot = bot

    command_rep_group = discord.app_commands.Group(name="rep", description="rep Group")

    # TODO 
    EXERCISE_CHOICES = [
        discord.app_commands.Choice(name="Bench", value="bench"),
        discord.app_commands.Choice(name="Deadlift", value="deadlift"),
        discord.app_commands.Choice(name="Squats", value="squats"),
    ]


    @command_rep_group.command(name="calculator", description="Calculate the amount of reps you should do for your 1RM")
    @discord.app_commands.describe(exercise="which exercise", user="Which user")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def rep_calc(self, interaction: discord.Interaction, exercise: str, user: discord.User=None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        # get 1RM for that exercise for user
        try:
            success, resultsOrErr = await db_manager.getMaxOfUserWithExercise(str(user.id), exercise)
            if not success: raise ValueError(resultsOrErr)

            embed = create_1rm_table_embed(*resultsOrErr)

        except Exception as err:
            embed = OperationFailedEmbed(
                description=f"An error has occurred: {err}"
            )

        return await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Rep(bot))