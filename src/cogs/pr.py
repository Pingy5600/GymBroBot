import discord
import dateparser

from discord.ext import commands
from datetime import datetime
from database import db_manager
from embeds import DefaultEmbed


class pr(commands.Cog, name="pr"):
    def __init__(self,bot):
        self.bot = bot


    @discord.app_commands.command(name="work", description="checks to see if I am online")
    async def work(self, interaction: discord.Interaction):
        embed = DefaultEmbed(
            title="Bot Status",
            description=f"I am just a chill guy! \n\nLatency: {self.bot.latency * 1000:.2f} ms."
        )
        await interaction.response.send_message(embed=embed)


    @discord.app_commands.command(name = "pr", description = "adds pr to the user's name")
    @discord.app_commands.describe(date="The date of the pr", pr="The personal record value", user="Which user")
    async def add_pr(self, interaction: discord.Interaction, pr: int, date: str = None, user: discord.User = None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

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
            return await interaction.followup.send(
                "Ongeldige datum. Gebruik een formaat zoals '2023-11-25' of '25 november 2023'."
            )
        except Exception as e:
            return await interaction.followup.send(
                f"Er is een fout opgetreden: {e}"
            )

        resultaat = await db_manager.add_pr(user.id, "bench", pr, date_obj)
        if resultaat[0]:
            return await interaction.followup.send(
                f"PR van {pr}kg op {date_obj.strftime('%d/%m/%y')} is toegevoegd!"
            )

        await interaction.followup.send(
            f"Er is iets misgegaan: {resultaat[1]}"
        )

async def setup(bot):
    await bot.add_cog(pr(bot))