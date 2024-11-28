import discord
from discord.ext import commands
from datetime import datetime
import dateparser
import embeds

class pr(commands.Cog, name="pr"):
    def __init__(self,bot):
        self.bot = bot

    @discord.app_commands.command(name = "work", description = "checks to see if i am online")
    async def work(self,interaction):
        await interaction.response.send_message(f"I am just a chill guy! \n\nlatency: {self.bot.latency*1000} ms.")

    @discord.app_commands.command(name = "pr", description = "adds pr to the user's name")
    @discord.app_commands.describe(date= "The date of the pr", pr= "The perdsonal record value", user= "Which user")

    async def add_pr(self, interaction: discord.Interaction, date: str, pr: int, user: discord.User=None):
        pr_records = []

        """View someones bot profile

        Args:
            interaction (Interaction): Users Interaction
            user (discord.User): Which user
        """
        # await interaction.response.defer()

        # # geen gebruiker meegegeven, gaat over zichzelf
        # if user is None:
        #     user = interaction.user

        #   # creeer embed
        # embed = embeds.DefaultEmbed(
        #     f"**{user.display_name}'s Profile**", user=user
        # )

        # embed.set_author(
        #     name=user.name,
        #     icon_url=str(user.avatar.url)
        # )
        
        try:
            # Gebruik dateparser om de datum flexibel te interpreteren
            date_obj = dateparser.parse(date, settings={
                'DATE_ORDER': 'DMY',  # Formaat volgorde Dag, Maand, Jaar
                'TIMEZONE': 'CET',    # Tijdzone instellen
                'PREFER_DAY_OF_MONTH': 'first',  # Gebruik de eerste dag bij onduidelijke input
                'PREFER_DATES_FROM': 'past',    # Accepteer standaard data uit het verleden
                'DEFAULT_LANGUAGES': ["en", "nl"]  # Engels en Nederlands ondersteunen
            })

            # Controleer of de datum correct is geïnterpreteerd
            if date_obj is None:
                raise ValueError("Invalid date format")
            
            # Voeg het PR en de datum toe aan de lijst
            pr_records.append({"date": date_obj, "pr": pr})

            # Bevestig dat het PR is toegevoegd
            await interaction.response.send_message(
                f"PR van {pr}kg op {date_obj.strftime('%d/%m/%y %H:%M:%S')} is toegevoegd!"
            )

        except ValueError:
            # Foutmelding als de datum niet kan worden geïnterpreteerd
            await interaction.response.send_message(
                "Ongeldige datum. Gebruik een formaat zoals '2023-11-25' of '25 november 2023'."
            )
        except Exception as e:
            # Algemene foutafhandeling
            await interaction.response.send_message(
                f"Er is een fout opgetreden: {e}"
            )


async def setup(bot):
    await bot.add_cog(pr(bot))