""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

from abc import ABC, abstractmethod

from discord import app_commands

from embeds import OperationFailedEmbed
from helpers import getClickableCommand


class CustomCheckFailure(app_commands.CheckFailure, ABC):

    @abstractmethod
    def getEmbed(self, command, command_ids):
        pass

    def getClickableCommandString(self, command, command_ids):
        return f"Please try again: {getClickableCommand(command, command_ids)}"
        

class DeletionFailed(CustomCheckFailure):
    """
    Thrown when a user wanted to delete something, but the operation failed
    """

    def __init__(self, message="Failed to delete!"):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="❌"
        )


class InvalidWeight(CustomCheckFailure):
    """
    Thrown when a user inputs an invalid weight value
    """

    def __init__(self, message="You provided an invalid weight. Please use the correct format."):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="⚖️"
        )
    

class InvalidExercise(CustomCheckFailure):
    """
    Thrown when a user inputs an invalid exercise
    """

    def __init__(self, message="Invalid Exercise!"):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="🤔"
        )
    

class InvalidReps(CustomCheckFailure):
    """
    Thrown when a user inputs an invalid rep value
    """

    def __init__(self, message="The number of reps must be greater than 0."):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="🧮"
        )


class InvalidDate(CustomCheckFailure):
    """
    Thrown when a user inputs an invalid date
    """

    def __init__(self, message="Invalid date. Use a format like '2024-11-25' or 'November 25, 2024'."):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="📅"
        )


class InvalidTime(CustomCheckFailure):
    """
    Thrown when a user inputs an invalid time.
    """

    def __init__(self, message="Invalid Time!"):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="⏲️"
        )   


class NoEntries(CustomCheckFailure):
    """
    Thrown when a user doesnt have any entries for a specific exercise.
    """

    def __init__(self, message="No entries found for the specified exercise."):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="📭"
        )


class NoPermission(CustomCheckFailure):
    """
    Thrown when a user is attempting something, but does not have the correct permissions.
    """

    def __init__(self, message="You do not have permission to do that!"):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="🔒"
        )


class TimeoutCommand(CustomCheckFailure):
    """
    Thrown when a user has exceeded a time limit.
    """

    def __init__(self, message="You took too long!"):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="⏲️"
        )

      
class CogLoadError(CustomCheckFailure):
    """
    Thrown when a cog doesnt load correctly.
    """

    def __init__(self, cog, status):
        if status == 0:
            errortype = 'load'
        elif status == 1:
            errortype = 'unload'
        else:
            errortype = 'reload'

        self.message = f"Could not {errortype} cog." if not cog else f"Could not {errortype} the ```{cog}``` cog."
        super().__init__(self.message)
    
    
class BotNotUser(CustomCheckFailure):
    """
    Thrown when a user is attempting to put the bot as an input for an user command.
    """

    def __init__(self, message="A bot can't be given as a user"):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="🤖"
        )


class DuplicateUsers(CustomCheckFailure):
    """
    Thrown when a user is attempting to input the same user multiple times.
    """

    def __init__(self, message="Duplicate users found in the list."):
        self.message = message
        super().__init__(self.message)

    def getEmbed(self, command, command_ids):
        return OperationFailedEmbed(
            self.message,
            self.getClickableCommandString(command, command_ids),
            emoji="‼️"
        )