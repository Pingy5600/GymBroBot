from typing import List

from discord import Interaction, app_commands


async def exercise_autocomplete(
    interaction: Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    
    # bench, deadlift, squat are displayed by default
    if current is None or current == "":
        return EXERCISE_CHOICES[:3]
    
    # get the best matches otherwise
    matches = [
        exc for exc in EXERCISE_CHOICES if current.lower() in exc.name.lower()
    ]

    # select max. the first 5 matches
    return matches[:5]

# TODO add more exercises
EXERCISE_CHOICES = [
    app_commands.Choice(name="Bench", value="bench"),
    app_commands.Choice(name="Deadlift", value="deadlift"),
    app_commands.Choice(name="Squats", value="squats"),
    app_commands.Choice(name="Incline Bench", value="incline-bench"),
    app_commands.Choice(name="Push-ups", value="pushups"),
    app_commands.Choice(name="Pull-ups", value="pullups"),
    app_commands.Choice(name="Dips", value="dips"),
    app_commands.Choice(name="Dumbbell Curl", value="dumbbell-curl"),
    app_commands.Choice(name="Incline Dumbbell Curl", value="incline-dumbbell-curl"),
    app_commands.Choice(name="Barbell Curl", value="barbell-curl"),
    app_commands.Choice(name="Dumbell Hammer Curl", value="hammer-curl"),
    app_commands.Choice(name="Tricep Rope Pushdown", value="tricep-rope-pushdown"),
    app_commands.Choice(name="Dumbbell Lateral Raise", value="dumbbell-lateral-raise"),
    app_commands.Choice(name="Lat Pulldown", value="lat-pulldown"),
    app_commands.Choice(name="Rows", value="rows"),
    app_commands.Choice(name="Leg Extension", value="leg-extension"),
    app_commands.Choice(name="Leg Curl", value="leg-curl"),
    app_commands.Choice(name="Leg Press", value="leg-press"),
    app_commands.Choice(name="Incline Chest Press Machine", value="incline-chest-press-machine"),
]

EXERCISE_META = {
    "bench": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bench-Press.gif",
        "pretty-name": "Bench Press",
    },
    "deadlift": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Deadlift.gif",
        "pretty-name": "Deadlift",
    },
    "squats": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/BARBELL-SQUAT.gif",
        "pretty-name": "Squats",
    },
    "incline-bench": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Incline-Barbell-Bench-Press.gif",
        "pretty-name": "Incline Bench Press",
    },
    "pushups": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif",
        "pretty-name": "Pushups",
    },
    "pullups": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pull-up.gif",
        "pretty-name": "Pullups",
    },
    "dips": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Chest-Dips.gif",
        "pretty-name": "Dips",
    },
    "dumbbell-curl": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Curl.gif",
        "pretty-name": "Dumbbell Curl",
    },
    "incline-dumbbell-curl": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Incline-Dumbbell-Curl.gif",
        "pretty-name": "Incline Dumbbell Curl",
    },
    "barbell-curl": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Curl.gif",
        "pretty-name": "Barbell Curl",
    },
    "hammer-curl": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Hammer-Curl.gif",
        "pretty-name": "Dumbbell Hammer Curl",
    },
    "tricep-rope-pushdown": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pushdown.gif",
        "pretty-name": "Tricep Rope Pushdown",
    },
    "dumbbell-lateral-raise": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lateral-Raise.gif",
        "pretty-name": "Dumbbell Lateral Raise",
    },
    "lat-pulldown": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Lat-Pulldown.gif",
        "pretty-name": "Lat Pulldown",
    },
    "rows": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Cable-Row.gif",
        "pretty-name": "Rows",
    },
    "leg-extension": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/LEG-EXTENSION.gif",
        "pretty-name": "Leg Extension",
    },
    "leg-curl": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Seated-Leg-Curl.gif",
        "pretty-name": "Leg Curl",
    },
    "leg-press": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Lever-Horizontal-Leg-Press.gif",
        "pretty-name": "Leg Press",
    },
    "incline-chest-press-machine": {
        "image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Incline-Chest-Press-Machine.gif",
        "pretty-name": "Incline Chest Press Machine",
    }
}


def getMetaFromExercise(exercise: str):
    if exercise not in EXERCISE_META:
        # TODO custom error
        raise ValueError(f"Exercise {exercise} not found")
    
    return EXERCISE_META[exercise]