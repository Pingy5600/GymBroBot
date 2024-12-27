from exceptions import BotNotUser, DuplicateUsers, InvalidReps, InvalidWeight, NoEntries, NoPermission


def validateAndCleanWeight(weight):
    weight_cleaned = weight.replace(',', '.')

    try:
        weight = float(weight_cleaned)
    
    except ValueError:
        raise InvalidWeight(
            "You provided an invalid PR value. Please use the correct format."
        )
    
    if weight <= 0:
        raise InvalidWeight("The weight must be greater than 0.")
    
    return weight


def validateReps(reps):
    if reps <= 0:
        raise InvalidReps() 

def validateNotBot(user):
    if user.bot:
        raise BotNotUser()
    

def validateEntryList(entries, message="No entries found for the specified exercise."):
    if len(entries) == 0:
        raise NoEntries(message)
    
    elif entries[0] == -1:
        raise Exception(entries[1])
    

def validatePermissions(user, interaction):
    if user != interaction.user and not interaction.user.guild_permissions.administrator:
        raise NoPermission(
            "You do not have permission to delete PRs for other users."
        )
    

def validateUserList(users):
    if len(users) != len(set(users)):
        raise DuplicateUsers()