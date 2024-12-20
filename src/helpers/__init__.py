from .graph import *
from .reps_calc import *


EXERCISE_CHOICES = [
    discord.app_commands.Choice(name="Bench", value="bench"),
    discord.app_commands.Choice(name="Deadlift", value="deadlift"),
    discord.app_commands.Choice(name="Squats", value="squats"),
]

EXERCISE_IMAGES = {
    "bench": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/05/Barbell-Bench-Press-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "deadlift": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/05/Barbell-Deadlift-1.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "squats": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/10/barbell-squat-resized-FIXED-2.png?ezimgfmt=ng%3Awebp%2Fngcb4",
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
