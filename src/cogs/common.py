import discord
import embeds
import dateparser

from discord.ext import commands
from embeds import DefaultEmbed
from datetime import datetime
from helpers import db_manager


class Common(commands.Cog, name="common"):
    def __init__(self,bot):
        self.bot = bot

    @discord.app_commands.command(name="info", description="Provides information about the bot")
    async def info(self, interaction: discord.Interaction):
        embed = DefaultEmbed(
            title="Bot Info",
            description="This bot was created to track PRs and help with fitness goals! 🏋️‍♂️"
        )
        embed.add_field(name="Version", value="1.0.0", inline=True)
        embed.add_field(name="Developer", value="Pingy1", inline=True)
        embed.add_field(name="Contributers", value="Solosdv", inline=True)
        await interaction.response.send_message(embed=embed)


    @discord.app_commands.command(name="remindme", description="Remind me when to take my creatine", extras={'cog': 'general'})
    @discord.app_commands.describe(wanneer="When should the bot send you a reminder")
    @discord.app_commands.describe(waarover="What should the bot remind you for")
    async def remindme(self, interaction, wanneer: str, waarover: discord.app_commands.Range[str, 1, 100]) -> None:
        """Sets a reminder

        Args:
            interaction (Interaction): User's Interaction
            wanneer (str): When to send the reminder
            waarover (app_commands.Range[str, 1, 100]): What the reminder is about
        """
        t = dateparser.parse(wanneer, settings={
            'DATE_ORDER': 'DMY',
            'TIMEZONE': 'CET',
            'PREFER_DAY_OF_MONTH': 'first',
            'PREFER_DATES_FROM': 'future',
            'DEFAULT_LANGUAGES': ["en", "nl"]
        })

        if t is None or t < datetime.now():
            return await interaction.response.send_message(embed=embeds.OperationFailedEmbed(
                "Geen geldig tijdstip"
            ))

        # Zet reminder in de database met het juiste datumformaat
        succes = await db_manager.set_reminder(
            interaction.user.id,
            subject=waarover,
            time=t.strftime('%Y-%m-%d %H:%M:%S')  # Correcte ISO 8601 notatie
        )

        desc = f"I will remind you at `{t.strftime('%Y-%m-%d %H:%M:%S')} CEST` for `{waarover}`" if succes else "Something went wrong!"

        await interaction.response.send_message(
            embed=embeds.OperationSucceededEmbed(
                "Reminder set!", desc, emoji="⏳"
            ) if succes else embeds.OperationFailedEmbed(
                "Oops!", desc
            ))
        

async def setup(bot):
    await bot.add_cog(Common(bot))