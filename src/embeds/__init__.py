import discord
from datetime import datetime

from helpers import getImageFromExercise

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