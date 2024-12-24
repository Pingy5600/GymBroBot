import discord
import embeds
import dateparser
import math
import asyncio
import pytz


from discord.ext import commands
from embeds import DefaultEmbed
from datetime import datetime
from helpers import db_manager


class Common(commands.Cog, name="common"):
    def __init__(self,bot):
        self.bot = bot

    command_remind_group = discord.app_commands.Group(name="remind", description="remind Group")

    @discord.app_commands.command(name="info", description="Provides information about the bot")
    async def info(self, interaction: discord.Interaction):
        # Verkrijg de gebruikerobjecten via hun gebruikers-ID
        developer = await self.bot.fetch_user(464400950702899211)
        contributer = await self.bot.fetch_user(462932133170774036)
        
        embed = DefaultEmbed(
            title="Bot Info",
            description="This bot was created to track PRs and help with fitness goals! 🏋️‍♂️"
        )
        embed.add_field(name="Version", value="1.0.0", inline=True)
        embed.add_field(name="Developer", value=developer.mention, inline=True)  # Gebruik .mention
        embed.add_field(name="Contributers", value=contributer.mention, inline=True)  # Gebruik .mention
        await interaction.response.send_message(embed=embed)


    @command_remind_group.command(name="me", description="Remind me when to take my creatine", extras={'cog': 'general'})
    @discord.app_commands.describe(wanneer="When should the bot send you a reminder")
    @discord.app_commands.describe(waarover="What should the bot remind you for")
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
            return await interaction.followup.send(embed=embeds.OperationFailedEmbed("Geen geldig tijdstip"))

        # Controleer of de parsed datetime 't' tijdzone-bewust is
        if t.tzinfo is None:
            t = tz.localize(t)  # Maak het tijdzone-bewust

        # Vergelijk de tijd met de huidige tijd in de juiste tijdzone
        if t < datetime.now(tz):
            return await interaction.followup.send(embed=embeds.OperationFailedEmbed("De opgegeven tijd is in het verleden"))

        # Zet reminder in de database
        succes = await db_manager.set_reminder(
            interaction.user.id,
            subject=waarover,
            time=t.strftime('%Y-%m-%d %H:%M:%S')
        )

        # Gebruik de Discord timestamp (<t:timestamp:F>) voor de herinnering
        timestamp = f"<t:{int(t.timestamp())}:F>"  # Zet de tijd om naar een timestamp

        desc = f"I will remind you at {timestamp} for {waarover}" if succes else "Something went wrong!"
        embed = embeds.OperationSucceededEmbed(
            "Reminder set!", desc, emoji="⏳"
        ) if succes else embeds.OperationFailedEmbed("Oops!", desc)

        await interaction.followup.send(embed=embed)  # Gebruik followup na een defer

        
    @command_remind_group.command(name="delete", description="Delete a specific reminder")
    async def delete_reminder(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        reminders = await db_manager.get_reminders_by_user(str(interaction.user.id))

        if len(reminders) == 0:
            embed = embeds.OperationFailedEmbed(description="You have no reminders set.")
            return await interaction.followup.send(embed=embed)
        elif reminders[0] == -1:
            raise Exception(reminders[1])

        paginator = ReminderPaginator(reminders, interaction.user)
        embed = paginator.generate_embed()
        message = await interaction.followup.send(embed=embed, view=paginator)

        message_id = message.id

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit() and m.reference is not None and m.reference.message_id == message_id

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60.0)
            index = int(msg.content) - 1

            if index < 0 or index >= len(reminders):
                raise ValueError("Invalid selection. Please try again.")

            selected_reminder = reminders[index]
            success = await db_manager.delete_reminder(selected_reminder['id'])

            if success:
                embed = embeds.OperationSucceededEmbed(
                    title="Reminder Deleted",
                    description=f"Successfully deleted the reminder for <t:{int(selected_reminder['time'].timestamp())}:F>."
                )
            else:
                embed = embeds.OperationFailedEmbed(description="Failed to delete the reminder.")
            await interaction.followup.send(embed=embed)

        except asyncio.TimeoutError:
            embed = embeds.OperationFailedEmbed(description="You took too long to respond! Command cancelled.")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = embeds.OperationFailedEmbed(description=f"An error occurred: {e}")
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
            subject = reminder['subject']
            timestamp = int(reminder['time'].timestamp())  # Convert to UNIX timestamp

            embed.add_field(
                name=f"{idx}. Reminder for <t:{timestamp}:F>",  # Use Discord timestamp
                value=f"**Subject:** {subject}",
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