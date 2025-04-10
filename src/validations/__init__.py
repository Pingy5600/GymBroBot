from exceptions import (BotNotUser, DuplicateUsers, InvalidDate, InvalidPushups, InvalidReps, InvalidWeight,
                        NoEntries, NoPermission)
import dateparser


def validateAndCleanWeight(weight):
    weight_cleaned = weight.replace(',', '.')

    try:
        weight = float(weight_cleaned)

    except ValueError:
        raise InvalidWeight(
            "You provided an invalid weight value. Please use the correct format."
        )

    if weight <= 0:
        raise InvalidWeight("The weight must be greater than 0.")

    if weight > 10000:
        raise InvalidWeight("I don't think you can lift that much...")

    return weight


def validateReps(reps):
    if reps <= 0:
        raise InvalidReps() 


def validateNotBot(user):
    if user.bot:
        raise BotNotUser()
    
def validateNotSelf(user, user2):
    if user.id == user2.id:
        raise BotNotUser("You cannot use yourself as a user.")
 

def validateEntryList(entries, message="No entries found for the specified exercise."):
    if len(entries) == 0:
        raise NoEntries(message)
    
    elif entries[0] == -1:
        raise Exception(entries[1])


def validatePermissions(user, interaction):
    user_is_self = user.id == interaction.user.id
    user_is_server_admin = interaction.user.guild_permissions.administrator
    user_is_owner = interaction.user.id in [464400950702899211, 462932133170774036]

    if not (user_is_self or user_is_server_admin or user_is_owner):
        raise NoPermission()


def validateUserList(users):
    if len(users) != len(set(users)):
        raise DuplicateUsers()


def validatePushups(pushups):
    if pushups <= 0:
        raise InvalidPushups()


def validateDate(date):
    date_set = {
        'DATE_ORDER': 'DMY',
        'TIMEZONE': 'CET',
        'PREFER_DAY_OF_MONTH': 'first',
        'PREFER_DATES_FROM': 'past',
        'DEFAULT_LANGUAGES': ["en", "nl"]
    }
    if date is None:
            date = 'vandaag'

    try:    
        date_obj = dateparser.parse(date, settings=date_set)
    except ValueError:
        raise InvalidDate()
    
    if date_obj is None:
        raise ValueError("Invalid date format")

    return date_obj