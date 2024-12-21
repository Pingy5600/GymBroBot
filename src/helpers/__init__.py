from .graph import *
from .reps_calc import *

# choices can only have 25 elements
EXERCISE_CHOICES = [
    discord.app_commands.Choice(name="Bench", value="bench"),
    discord.app_commands.Choice(name="Incline Bench", value="incline-bench"),
    discord.app_commands.Choice(name="Deadlift", value="deadlift"),
    discord.app_commands.Choice(name="Squats", value="squats"),
    discord.app_commands.Choice(name="Push-ups", value="pushups"),
    discord.app_commands.Choice(name="Pull-ups", value="pullups"),
    discord.app_commands.Choice(name="Dips", value="dips"),
    discord.app_commands.Choice(name="Dumbbell Curl", value="dumbbell-curl"),
    discord.app_commands.Choice(name="Incline Dumbbell Curl", value="incline-dumbbell-curl"),
    discord.app_commands.Choice(name="Barbell Curl", value="barbell-curl"),
    discord.app_commands.Choice(name="Dumbell Hammer Curl", value="hammer-curl"),
    discord.app_commands.Choice(name="Tricep Rope Pushdown", value="tricep-rope-pushdown"),
    discord.app_commands.Choice(name="Dumbbell Lateral Raise", value="dumbbell-lateral-raise"),
    discord.app_commands.Choice(name="Lat Pulldown", value="lat-pulldown"),
    discord.app_commands.Choice(name="Rows", value="rows"),
    discord.app_commands.Choice(name="Leg Extension", value="leg-extension"),
    discord.app_commands.Choice(name="Leg Curl", value="leg-curl"),
    discord.app_commands.Choice(name="Leg Press", value="leg-press"),
]

EXERCISE_IMAGES = {
    "bench": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bench-Press.gif",
    "incline-bench": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Incline-Barbell-Bench-Press.gif",
    "deadlift": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Deadlift.gif",
    "squats": "https://fitnessprogramer.com/wp-content/uploads/2021/02/BARBELL-SQUAT.gif",
    "pushups": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif",
    "pullups": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pull-up.gif",
    "dips": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Chest-Dips.gif",
    "dumbbell-curl": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Curl.gif",
    "incline-dumbbell-curl": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Incline-Dumbbell-Curl.gif",
    "barbell-curl": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Curl.gif",
    "hammer-curl": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Hammer-Curl.gif",
    "tricep-rope-pushdown": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pushdown.gif",
    "dumbbell-lateral-raise": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lateral-Raise.gif",
    "lat-pulldown": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Lat-Pulldown.gif",
    "rows": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Cable-Row.gif",
    "leg-extension": "https://fitnessprogramer.com/wp-content/uploads/2021/02/LEG-EXTENSION.gif",
    "leg-curl": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Seated-Leg-Curl.gif",
    "leg-press": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Lever-Horizontal-Leg-Press.gif",
}

def getImageFromExercise(exercise):
    return EXERCISE_IMAGES[exercise]

def getDiscordTimeStamp(old_timestamp):
    timestamp = int(old_timestamp.timestamp())
    return f"<t:{timestamp}:D>"

# https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix
