import discord
from discord.ext import commands
from datetime import datetime
import dateparser


class pr(commands.Cog, name="work"):
    def __init__(self,bot):
        self.bot = bot

    @discord.app_commands.command(name = "work", description = "checks to see if i am online")
    async def work(self,interaction):
        await interaction.response.send_message(f"I am just a chill guy! \n\nlatency: {self.bot.latency*1000} ms.")

    @discord.app_commands.command(name = "pr", description = "adds pr to the user's name")
    async def add_pr(self, interaction: discord.Interaction, date: str, pr: int):
        pr_records = []

        """
        Args:
            interaction (Interaction): Gebruikersinteractie.
            date (str): Datum van de PR (bijvoorbeeld in "YYYY-MM-DD" of flexibel).
            pr (int): Het toegevoegde PR-gewicht.
            wanneer (str): Wanneer een herinnering verzonden moet worden.
        """

        # Gebruik dateparser om de datum flexibel te interpreteren
        date_obj = dateparser.parse(date, settings={
            'DATE_ORDER': 'DMY',  # Formaat volgorde Dag, Maand, Jaar
            'TIMEZONE': 'CET',    # Tijdzone instellen
            'PREFER_DAY_OF_MONTH': 'first',  # Gebruik de eerste dag bij onduidelijke input
            'PREFER_DATES_FROM': 'past',    # Accepteer standaard data uit het verleden
            'DEFAULT_LANGUAGES': ["en", "nl"]  # Engels en Nederlands ondersteunen
        })

        if date_obj is None:
            # Foutmelding als de datum niet kan worden geïnterpreteerd
            await interaction.response.send_message(
                "Ongeldige datum. Probeer een formaat zoals '2023-11-25' of een leesbare invoer zoals '25 november 2023'."
            )
            return

        # Voeg het PR en de datum toe aan de lijst
        pr_records.append({"date": date_obj, "pr": pr})
        
        # Bevestig dat het PR is toegevoegd
        await interaction.response.send_message(
            f"PR van {pr}kg op {date_obj.strftime('%d/%m/%y %H:%M:%S')} is toegevoegd!"
        )

async def setup(bot):
    await bot.add_cog(pr(bot))