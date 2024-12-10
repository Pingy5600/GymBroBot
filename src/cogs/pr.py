import discord
import dateparser
import math

from discord.ext import commands
from datetime import datetime
from databank import db_manager
from embeds import DefaultEmbed
from embeds import OperationFailedEmbed


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
        embed = DefaultEmbed(
            title=f"{self.exercise.capitalize()} PRs of {self.user.display_name}",
        )

        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_prs = self.prs[start:end]

        for pr in page_prs:
            weight = pr[1]
            # Format weight to two decimal places if it is a decimal number
            if weight % 1 != 0:  # If it is a decimal
                weight = f"{weight:.2f}"
            else:
                weight = f"{int(weight)}"  # Remove decimals if it's an integer

            timestamp = int(pr[2].timestamp())
            embed.add_field(
                name=f"Date: <t:{timestamp}:D>",
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
            description="This bot was created to track PRs and help wi      th fitness goals! 🏋️‍♂️"
        )
        embed.add_field(name="Version", value="1.0.0", inline=True)
        embed.add_field(name="Developer", value="Pingy1", inline=True)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name = "pr", description = "adds pr to the user's name")
    @discord.app_commands.describe(date="The date of the pr", pr="The personal record value", exercise="Which exercise", user="Which user")
    @discord.app_commands.choices(
        exercise=[
            discord.app_commands.Choice(name="Bench", value="bench"),
            discord.app_commands.Choice(name="Deadlift", value="deadlift"),
            discord.app_commands.Choice(name="Squats", value="squats"),
        ]
    )
    async def add_pr(self, interaction: discord.Interaction, pr: str, exercise: str, date: str = None, user: discord.User = None):
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

        resultaat = await db_manager.add_pr(user.id, exercise, pr, date_obj)

        if resultaat[0]:
            embed = DefaultEmbed(
                title="PR added!",
                description=f"PR of {pr}kg added"
            )
            embed.add_field(name="User", value=user.mention, inline=True)
            embed.add_field(name="Excercise", value=exercise, inline=True)
            embed.add_field(name="Date", value=date_obj.strftime('%d/%m/%y'), inline=True)
            return await interaction.followup.send(embed=embed)
        
        embed = OperationFailedEmbed(
            description= f"Something went wrong: {resultaat[1]}"
        )
        await interaction.followup.send(embed=embed)

    @discord.app_commands.command(name ="get_pr", description ="Gives pr of the given user")
    @discord.app_commands.describe(user="Which user", exercise="which exercise")
    @discord.app_commands.choices(
        exercise=[
            discord.app_commands.Choice(name="Bench", value="bench"),
            discord.app_commands.Choice(name="Deadlift", value="deadlift"),
            discord.app_commands.Choice(name="Squats", value="squats"),
        ]
    )
    async def get_pr(self, interaction: discord.Interaction, exercise: str, user: discord.User=None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        try:
            prs = await db_manager.get_prs_from_user(str(user.id), exercise)

            if len(prs) == 0:
                embed = OperationFailedEmbed(
                    description= f"No PRs found for the specified exercise."
                )
                return await interaction.followup.send(embed=embed)
            
            elif prs[0] == -1:
                raise Exception(prs[1])
        
        except Exception as e:
            embed = OperationFailedEmbed(
                description=f"An error has occurred: {e}"
            )
            return await interaction.followup.send(embed=embed)
        
        view = PRPaginator(prs, exercise, user)
        embed = view.generate_embed()
        await interaction.followup.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(pr(bot))