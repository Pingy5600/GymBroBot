""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

from abc import ABC, abstractmethod

from discord import app_commands

from embeds import OperationFailedEmbed


class CustomCheckFailure(app_commands.CheckFailure, ABC):

    @abstractmethod
    def getEmbed(self, command):
        pass
    
    def getClickableCommand(self, command):
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

        # TODO: maak dit clickable
        return f"Please try again: ```/{command.qualified_name}```"
        


class DeletionFailed(CustomCheckFailure):
    """
    Thrown when a user wanted to delete something, but the operation failed
    """

    def __init__(self, message="Failed to delete!"):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommand(command),
            emoji="❌"
        )


class InvalidWeight(CustomCheckFailure):
    """
    Thrown when a user inputs an invalid weight value
    """

    def __init__(self, message="You provided an invalid weight. Please use the correct format."):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommand(command),
            emoji="⚖️"
        )


class InvalidDate(CustomCheckFailure):
    """
    Thrown when a user inputs an invalid date
    """

    def __init__(self, message="Invalid date. Use a format like '2024-11-25' or 'November 25, 2024'."):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommand(command),
            emoji="📅"
        )


class InvalidTime(CustomCheckFailure):
    """
    Thrown when a user inputs an invalid time.
    """

    def __init__(self, message="Invalid Time!"):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommand(command),
            emoji="⏲️"
        )   


class NoEntries(CustomCheckFailure):
    """
    Thrown when a user doesnt have any entries for a specific exercise.
    """

    def __init__(self, message="No entries found for the specified exercise."):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommand(command),
            emoji="📭"
        )


class NoPermission(CustomCheckFailure):
    """
    Thrown when a user is attempting something, but does not have the correct permissions.
    """

    def __init__(self, message="You do not have permission to do that!"):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommand(command),
            emoji="🔒"
        )


class TimeoutCommand(CustomCheckFailure):
    """
    Thrown when a user has exceeded a time limit.
    """

    def __init__(self, message="You took too long!"):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommand(command),
            emoji="⏲️"
        )
