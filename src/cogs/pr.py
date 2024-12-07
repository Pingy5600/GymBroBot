import discord
import dateparser

from discord.ext import commands
from datetime import datetime
from database import db_manager
from embeds import DefaultEmbed
from embeds import OperationFailedEmbed


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


    @discord.app_commands.command(name="info", description="Provides information about the bot")
    async def info(self, interaction: discord.Interaction):
        embed = DefaultEmbed(
            title="Bot Info",
            description="This bot was created to track PRs and help with fitness goals! 🏋️‍♂️"
        )
        embed.add_field(name="Version", value="1.0.0", inline=True)
        embed.add_field(name="Developer", value="Pingy1", inline=True)
        await interaction.response.send_message(embed=embed)


    @discord.app_commands.command(name = "pr", description = "adds pr to the user's name")
    @discord.app_commands.describe(date="The date of the pr", pr="The personal record value", user="Which user")
    async def add_pr(self, interaction: discord.Interaction, pr: str, date: str = None, user: discord.User = None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        if date is None:
            date = 'vandaag'

        pr_cleaned = pr.replace(',', '.')
        pr_command_ref = f"</pr:{self.bot.tree.get_command('pr').id}>"

        try:
            pr = float(pr_cleaned)

        except ValueError:

            embed = OperationFailedEmbed(
                description=
                "You provided an invalid PR value. Please use the correct format.\n"
                f"Please try again: {pr_command_ref}"
            )
            return await interaction.followup.send(embed=embed)
        
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
            embed = OperationFailedEmbed(
                description=
                "Invalid date. Use a format like '2024-11-25' or 'November 25, 2024'.\n"
                f"Please try again: {pr_command_ref}"
            )
            return await interaction.followup.send(embed=embed)

        except Exception as e:
            embed = OperationFailedEmbed(
                description=f"An error has occurred:{e}"
            )
            return await interaction.followup.send(embed=embed)

        resultaat = await db_manager.add_pr(user.id, "bench", pr, date_obj)

        if resultaat[0]:
            embed = DefaultEmbed(
                title="PR added!",
                description=f"PR of {pr}kg added"
            )
            embed.add_field(name="User", value=user.mention, inline=True)
            embed.add_field(name="Excercise", value="bench", inline=True)
            embed.add_field(name="Date", value=date_obj.strftime('%d/%m/%y'), inline=True)
            return await interaction.followup.send(embed=embed)
        
        embed = OperationFailedEmbed(
            description= f"Something went wrong: {resultaat[1]}"
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(pr(bot))