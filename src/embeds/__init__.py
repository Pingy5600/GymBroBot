import discord
from datetime import datetime


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

class OperationFailedEmbed(discord.Embed):
    def __init__(self, title="Error", description=None, emoji="❌"):
        super().__init__(
            title=f"{title} {emoji}", 
            description=description,
            color=ERROR_COLOR,
            timestamp=datetime.now()
        )