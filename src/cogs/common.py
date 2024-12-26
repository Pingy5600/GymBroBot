import asyncio
import math
from datetime import datetime

import dateparser
import discord
import pytz
from discord.ext import commands

import embeds
from embeds import DefaultEmbed
from exceptions import DeletionFailed, InvalidTime, TimeoutCommand
from helpers import COLOR_MAP, db_manager, getDiscordTimeStamp
from validations import validateEntryList, validateNotBot


class Common(commands.Cog, name="common"):
    def __init__(self,bot):
        self.bot = bot

    command_remind_group = discord.app_commands.Group(name="remind", description="remind Group")


    @discord.app_commands.command(name="info", description="Provides information about the bot")
    async def info(self, interaction: discord.Interaction):
        developer = await self.bot.fetch_user(464400950702899211)
        contributer = await self.bot.fetch_user(462932133170774036)
        
        embed = DefaultEmbed(
            title="Bot Info",
            description="This bot was created to track PRs and help with fitness goals! 🏋️‍♂️"
        )
        embed.add_field(name="Version", value="1.0.0", inline=True)
        embed.add_field(name="Developer", value=developer.mention, inline=True)
        embed.add_field(name="Contributers", value=contributer.mention, inline=True)
        await interaction.response.send_message(embed=embed)


    @discord.app_commands.command(name="profile", description="Gives the profile of the given user")
    @discord.app_commands.describe(user="Which user")
    async def profile(self, interaction: discord.Interaction, user: discord.User = None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        validateNotBot(user)

        # Haal de kleur op uit COLOR_MAP
        user_id = str(user.id)
        user_color = COLOR_MAP.get(user_id, None)
        
        if user_color:
            # Embed met de specifieke kleur van de gebruiker
            embed = discord.Embed(
                title=f"Profile of {user}",
                description="Dit is je profiel! Hier is je eigen kleur",
                color=discord.Color(int(user_color[1:], 16))  # Hexcode omzetten naar kleur
            )
            embed.add_field(name="A lot more coming soon", value="COMING SOON", inline=True)

        else:
            # Standaard embed als de gebruiker geen kleur heeft
            embed = discord.Embed(
                title=f"Profile of {user}",
                description="You have not set a custom color.",
                color=discord.Color.default()
            )

        await interaction.followup.send(embed=embed)


    @command_remind_group.command(name="me", description="Remind me when to take my creatine", extras={'cog': 'general'})
    @discord.app_commands.describe(wanneer="When should the bot send you a reminder", waarover="What should the bot remind you for")
    async def remindme(self, interaction, wanneer: str, waarover: discord.app_commands.Range[str, 1, 100]) -> None:
        await interaction.response.defer(thinking=True)  # Geeft meer tijd om de interactie te verwerken

        # Stel de tijdzone in op CET (Central European Time)
        tz = pytz.timezone('CET')

        t = dateparser.parse(wanneer, settings={
            'DATE_ORDER': 'DMY',
            'TIMEZONE': 'CET',
            'PREFER_DAY_OF_MONTH': 'first',
            'PREFER_DATES_FROM': 'future',
            'DEFAULT_LANGUAGES': ["en", "nl"]
        })

        if t is None:
            raise InvalidTime("Geen geldig tijdstip")

        # Controleer of de parsed datetime 't' tijdzone-bewust is
        if t.tzinfo is None:
            t = tz.localize(t)  # Maak het tijdzone-bewust

        # Vergelijk de tijd met de huidige tijd in de juiste tijdzone
        if t < datetime.now(tz):
            raise InvalidTime("De opgegeven tijd is in het verleden")

        # Zet reminder in de database
        succes = await db_manager.set_reminder(
            interaction.user.id,
            subject=waarover,
            time=t.strftime('%Y-%m-%d %H:%M:%S')
        )

        if not succes:
            raise Exception("Could not set reminder...")

        desc = f"I will remind you at {getDiscordTimeStamp(t)} for {waarover}"
        embed = embeds.OperationSucceededEmbed(
            "Reminder set!", desc, emoji="⏳"
        )
        await interaction.followup.send(embed=embed)  # Gebruik followup na een defer

        
    @command_remind_group.command(name="delete", description="Delete a specific reminder")
    async def delete_reminder(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        reminders = await db_manager.get_reminders_by_user(str(interaction.user.id))
        validateEntryList(reminders, "You have no reminders set.")

        paginator = ReminderPaginator(reminders, interaction.user)
        embed = paginator.generate_embed()
        message = await interaction.followup.send(embed=embed, view=paginator)

        message_id = message.id

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit() and m.reference is not None and m.reference.message_id == message_id

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60.0)

        except asyncio.TimeoutError:
            raise TimeoutCommand()
        
        index = int(msg.content) - 1

        if index < 0 or index >= len(reminders):
            raise ValueError("Invalid selection. Please try again.")

        selected_reminder = reminders[index]
        success = await db_manager.delete_reminder(selected_reminder['id'])

        if not success:
            raise DeletionFailed("Failed to delete the reminder.")

        embed = embeds.OperationSucceededEmbed(
            title="Reminder Deleted",
            description=f"Successfully deleted the reminder for {getDiscordTimeStamp(selected_reminder['time'])}."
        )
        await interaction.followup.send(embed=embed)
        

class ReminderPaginator(discord.ui.View):
    def __init__(self, reminders, user):
        super().__init__()
        self.reminders = reminders
        self.user = user
        self.current_page = 0
        self.items_per_page = 10
        self.max_pages = math.ceil(len(reminders) / self.items_per_page)

        if self.max_pages <= 1:
            self.clear_items()  # Remove buttons if only 1 page

    def generate_embed(self):
        embed = DefaultEmbed(
            title=f"Reminders for {self.user.display_name}",
            description="Reply with the **number** of the reminder you want to delete."
        )

        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_reminders = self.reminders[start:end]

        for idx, reminder in enumerate(page_reminders, start=start + 1):
            embed.add_field(
                name=f"{idx}. Reminder for {getDiscordTimeStamp(reminder['time'])}",
                value=f"**Subject:** {reminder['subject']}",
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
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.max_pages - 1

        if self.max_pages <= 1:
            self.clear_items()


async def setup(bot):
    await bot.add_cog(Common(bot))