import math
from datetime import datetime

import discord

from helpers import getDiscordTimeStamp

DEFAULT_COLOR = 0x4169E1
ERROR_COLOR = 0xE02B2B
SUCCES_COLOR = 0x39AC39


class DefaultEmbed(discord.Embed):
    def __init__(self, title, description=None, user=None):
        super().__init__(
            title=f"{title}",
            description=description,
            color=DEFAULT_COLOR,
            timestamp=datetime.now(),
        )


class DefaultEmbedWithExercise(DefaultEmbed):
    def __init__(self, title, image_url, description=None):
        super().__init__(title, description)
        self.set_thumbnail(url=image_url)


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
    def __init__(self, items, user, title, generate_field_callback, exercise_url=None, items_per_page=10):
        super().__init__()
        self.items = items
        self.user = user
        self.title = title
        self.generate_field_callback = generate_field_callback  # Function to format each item
        self.exercise_url = exercise_url  # Store the exercise
        self.items_per_page = items_per_page
        self.current_page = 0
        self.max_pages = math.ceil(len(items) / items_per_page)

        if self.max_pages <= 1:
            self.clear_items()  # Remove buttons if only one page

    async def generate_embed(self, client=None):
        # Use DefaultEmbedWithExercise if exercise is provided
        if self.exercise_url:
            embed = DefaultEmbedWithExercise(
                title=self.title,
                image_url=self.exercise_url  # Use the stored exercise
            )
        else:
            embed = DefaultEmbed(
                title=self.title
            )

        # Items of the current page
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_items = self.items[start:end]

        # Add fields asynchronously to the embed
        for idx, item in enumerate(page_items, start=start + 1):
            # Handle the callback based on whether client is passed (for top command)
            if client:
                field_name, field_value = await self.generate_field_callback(idx, item, client)
            else:
                field_name, field_value = self.generate_field_callback(idx, item)
            embed.add_field(name=field_name, value=field_value, inline=False)

        # Set footer with page number
        embed.set_footer(text=f"Page {self.current_page + 1} of {self.max_pages}")
        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            embed = await self.generate_embed()
            self.update_buttons()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            embed = await self.generate_embed()
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
        weight = pr[2]
        if weight % 1 != 0:
            weight = f"{weight:.2f}"
        else:
            weight = f"{int(weight)}"

        timestamp = getDiscordTimeStamp(pr[3])
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


class TopPRFieldGenerator:
    @staticmethod
    async def generate_field(idx, pr, client):
        user_id = pr[0]
        weight = pr[1]
        timestamp = pr[2]

        if weight % 1 != 0:
            weight = f"{weight:.2f}"
        else:
            weight = f"{int(weight)}"

        try:
            user = await client.fetch_user(user_id)
            user_display = user.name
        except Exception:
            user_display = f"User ID {user_id}"

        timestamp_str = getDiscordTimeStamp(timestamp)

        if idx == 1:
            medal = "🥇"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"
        else:
            medal = ""

        return (
            f"{medal} {f'{idx}. ' if idx>3 else ''}{user_display}",
            f"**Weight:** {weight} kg\n**Lifted At:** {timestamp_str}"
        )