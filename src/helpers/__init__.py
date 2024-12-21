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
]

EXERCISE_IMAGES = {
    "bench": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/05/Barbell-Bench-Press-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "incline-bench": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/11/incline-barbell-bench-press-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "deadlift": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/05/Barbell-Deadlift-1.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "squats": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/10/barbell-squat-resized-FIXED-2.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "pushups": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/10/push-up-tall-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "pullups": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/10/pull-up-2-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "dips": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/05/Triceps-Dip-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "dumbbell-curl": "https://cdn-0.weighttraining.guide/wp-content/uploads/2022/06/Two-arm-dumbbell-curl.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "incline-dumbbell-curl": "https://cdn-0.weighttraining.guide/wp-content/uploads/2022/02/Incline-dumbbell-inner-biceps-curl.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "barbell-curl": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/05/barbell-curl-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "hammer-curl": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/11/Dumbbell-Hammer-Curl-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "tricep-rope-pushdown": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/05/Triceps-Rope-Pushdown-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "dumbbell-lateral-raise": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/05/dumbbell-lateral-raise-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "lat-pulldown": "https://cdn-0.weighttraining.guide/wp-content/uploads/2017/01/Lat-pull-down-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "rows": "https://cdn-0.weighttraining.guide/wp-content/uploads/2023/09/Straight-back-seated-cable-row-with-straight-bar.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "leg-extension": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/05/lever-leg-extension-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
    "leg-curl": "https://cdn-0.weighttraining.guide/wp-content/uploads/2016/10/seated-leg-curl-resized.png?ezimgfmt=ng%3Awebp%2Fngcb4",
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
