from discord import app_commands

from .graph import *
from .reps_calc import *

date_set = {
    'DATE_ORDER': 'DMY',
    'TIMEZONE': 'CET',
    'PREFER_DAY_OF_MONTH': 'first',
    'PREFER_DATES_FROM': 'past',
    'DEFAULT_LANGUAGES': ["en", "nl"]
}

def getDiscordTimeStamp(old_timestamp, full_time=False):
    timestamp = int(old_timestamp.timestamp())
    if full_time:
        # Return full date and time (day, hour, minute)
        return f"<t:{timestamp}:F>"  # Full date and time (e.g., January 1, 2024 12:00 AM)
    else:
        # Return only the date
        return f"<t:{timestamp}:D>"  # Just the day (e.g., January 1, 2024)


# https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


def getClickableCommand(command, command_ids):
        """Gets clickable command reference

        Args:
            command (Optional[Union[app_commands.Command, app_commands.ContextMenu]]): command

        Returns:
            str: formatted clickable command reference
        """
        if command is None:
            return None
        
        if not isinstance(command, app_commands.Command):
            return None

        try:
            # we split to get the topmost command, or just the command name if not part of group
            command_id = command_ids.get(command.qualified_name.split(' ')[0])
            return f"</{command.qualified_name}:{command_id}>"
        
        except AttributeError:
                return f"/{command.qualified_name}"