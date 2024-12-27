import discord
from datetime import datetime
import math

from helpers import getImageFromExercise, getDiscordTimeStamp

DEFAULT_COLOR = 0x4169E1
ERROR_COLOR = 0xE02B2B
SUCCES_COLOR = 0x39AC39


class DefaultEmbed(discord.Embed):
    def __init__(self, title, description=None):
        super().__init__(
            title=f"{title}",
            description=description,
            color=DEFAULT_COLOR,
            timestamp=datetime.now(),
        )


class DefaultEmbedWithExercise(DefaultEmbed):
    def __init__(self, title, exercise, description=None):
        super().__init__(title, description)
        self.set_thumbnail(url=getImageFromExercise(exercise))


class OperationFailedEmbed(discord.Embed):
    def __init__(self, title="Error", description=None, emoji="❌"):
        super().__init__(
            title=f" {emoji} {title}", 
            description=description,
            color=ERROR_COLOR,
            timestamp=datetime.now()
        )


class OperationSucceededEmbed(discord.Embed):
    def __init__(self, title, description=None, emoji="✅"):
        super().__init__(
            title=f"{emoji} {title}",
            description=description,
            color=SUCCES_COLOR,
            timestamp=datetime.now(),
        )


class Paginator(discord.ui.View):
    def __init__(self, items, user, title, generate_field_callback, items_per_page=10):
        super().__init__()
        self.items = items
        self.user = user
        self.title = title
        self.generate_field_callback = generate_field_callback  # Function to format each item
        self.items_per_page = items_per_page
        self.current_page = 0
        self.max_pages = math.ceil(len(items) / items_per_page)

        if self.max_pages <= 1:
            self.clear_items()  # Remove buttons if only 1 page

    def generate_embed(self):
        embed = discord.Embed(
            title=self.title,
            color=discord.Color.blurple()
        )

        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_items = self.items[start:end]

        for idx, item in enumerate(page_items, start=start + 1):
            field_name, field_value = self.generate_field_callback(idx, item)
            embed.add_field(name=field_name, value=field_value, inline=False)

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


class ReminderFieldGenerator:
    @staticmethod
    def generate_field(idx, reminder):
        return (
            f"{idx}. Reminder for {getDiscordTimeStamp(reminder['time'], full_time=True)}",
            f"**Subject:** {reminder['subject']}"
        )


class PRFieldGenerator:
    @staticmethod
    def generate_field(idx, pr):
        weight = pr[1]
        if weight % 1 != 0:
            weight = f"{weight:.2f}"
        else:
            weight = f"{int(weight)}"

        timestamp = getDiscordTimeStamp(pr[2])
        return (
            f"{idx}. {timestamp}",
            f"**Weight:** {weight} kg"
        )


class RepFieldGenerator:
    @staticmethod
    def generate_field(idx, rep):
        weight = rep['weight']
        reps = rep['reps']
        timestamp = getDiscordTimeStamp(rep['lifted_at'])

        if weight % 1 != 0:
            weight = f"{weight:.2f}"
        else:
            weight = f"{int(weight)}"

        return (
            f"{idx}. {timestamp}",
            f"**Weight:** {weight} kg | **Reps:** {reps}"
        )
