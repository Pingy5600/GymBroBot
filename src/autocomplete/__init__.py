from typing import List

from discord import Interaction, app_commands
from exceptions import InvalidExercise


async def exercise_autocomplete(
    interaction: Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    
    # bench, deadlift, squat are displayed by default
    if current is None or current == "":
        return EXERCISE_CHOICES[:4]
    
    # get the best matches otherwise
    matches = [
        exc for exc in EXERCISE_CHOICES if current.lower() in exc.name.lower()
    ]

    # select max. the first 10 matches
    return matches[:10]

EXERCISE_CHOICES = [
    app_commands.Choice(name="Bench Press", value="bench"),
    app_commands.Choice(name="Deadlift", value="deadlift"),
    app_commands.Choice(name="Squats", value="squats"),
    app_commands.Choice(name="Barbell Military Press (Overhead press)", value="barbell-military-press-overhead-press"),
	app_commands.Choice(name="Weighted Lateral Neck Flexion", value="weighted-lateral-neck-flexion"),
	app_commands.Choice(name="Weighted Lying Neck Extension (Neck Harness)", value="weighted-lying-neck-extension-neck-harness"),
	app_commands.Choice(name="Weighted Lying Neck Flexion (Neck Harness)", value="weighted-lying-neck-flexion-neck-harness"),
	app_commands.Choice(name="Gittleson Shrug", value="gittleson-shrug"),
	app_commands.Choice(name="Diagonal Neck Stretch", value="diagonal-neck-stretch"),
	app_commands.Choice(name="Neck Rotation Stretch", value="neck-rotation-stretch"),
	app_commands.Choice(name="Neck Flexion Stretch", value="neck-flexion-stretch"),
	app_commands.Choice(name="Neck Extension Stretch", value="neck-extension-stretch"),
	app_commands.Choice(name="Side Neck Stretch", value="side-neck-stretch"),
	app_commands.Choice(name="Side Push Neck Stretch", value="side-push-neck-stretch"),
	app_commands.Choice(name="Front and Back Neck Stretch", value="front-and-back-neck-stretch"),
	app_commands.Choice(name="Chin Tuck", value="chin-tuck"),
	app_commands.Choice(name="Prone Cervical Extension", value="prone-cervical-extension"),
	app_commands.Choice(name="Kneeling Neck Stretch", value="kneeling-neck-stretch"),
	app_commands.Choice(name="Weighted Neck Harness Extension", value="weighted-neck-harness-extension"),
	app_commands.Choice(name="Lying Weighted Neck Flexion", value="lying-weighted-neck-flexion"),
	app_commands.Choice(name="Lying Weighted Neck Extension", value="lying-weighted-neck-extension"),
	app_commands.Choice(name="Lever Neck Right Side Flexion (plate loaded)", value="lever-neck-right-side-flexion-plate-loaded"),
	app_commands.Choice(name="Lever Neck Extension (plate loaded)", value="lever-neck-extension-plate-loaded"),
	app_commands.Choice(name="Cable Seated Neck Flexion with head harness", value="cable-seated-neck-flexion-with-head-harness"),
	app_commands.Choice(name="Cable Seated Neck Extension with head harness", value="cable-seated-neck-extension-with-head-harness"),
	app_commands.Choice(name="Sphinx Stretch", value="sphinx-stretch"),
	app_commands.Choice(name="Floor Hyperextension", value="floor-hyperextension"),
	app_commands.Choice(name="Bhujangasana | Cobra Abdominal Stretch", value="bhujangasana-cobra-abdominal-stretch"),
	app_commands.Choice(name="Fish Pose", value="fish-pose"),
	app_commands.Choice(name="Superman", value="superman"),
	app_commands.Choice(name="Overhead Shrug", value="overhead-shrug"),
	app_commands.Choice(name="45 Degree Incline Row", value="45-degree-incline-row"),
	app_commands.Choice(name="Dumbbell Shrug", value="dumbbell-shrug"),
	app_commands.Choice(name="Cable Shrug", value="cable-shrug"),
	app_commands.Choice(name="Barbell Shrug", value="barbell-shrug"),
	app_commands.Choice(name="Behind The Back Barbell Shrug", value="behind-the-back-barbell-shrug"),
	app_commands.Choice(name="Dumbbell Incline Shrug", value="dumbbell-incline-shrug"),
	app_commands.Choice(name="Prone Incline Shrug", value="prone-incline-shrug"),
	app_commands.Choice(name="Lever Shrug", value="lever-shrug"),
	app_commands.Choice(name="Rear Delt Fly Machine", value="rear-delt-fly-machine"),
	app_commands.Choice(name="Lever Gripless Shrug", value="lever-gripless-shrug"),
	app_commands.Choice(name="Cable Rear Delt Fly", value="cable-rear-delt-fly"),
	app_commands.Choice(name="Bent Over Lateral Raise", value="bent-over-lateral-raise"),
	app_commands.Choice(name="Cable Upright Row", value="cable-upright-row"),
	app_commands.Choice(name="Face Pull", value="face-pull"),
	app_commands.Choice(name="Half Kneeling High Cable Row Rope", value="half-kneeling-high-cable-row-rope"),
	app_commands.Choice(name="Dumbbell Raise", value="dumbbell-raise"),
	app_commands.Choice(name="Dumbbell Upright Row", value="dumbbell-upright-row"),
	app_commands.Choice(name="Bodyweight Military Press", value="bodyweight-military-press"),
	app_commands.Choice(name="Kneeling High Pulley Row", value="kneeling-high-pulley-row"),
	app_commands.Choice(name="Ez Bar Upright Row", value="ez-bar-upright-row"),
	app_commands.Choice(name="Band Pull-Apart", value="band-pullapart"),
	app_commands.Choice(name="Bent Over Reverse Cable Fly", value="bent-over-reverse-cable-fly"),
	app_commands.Choice(name="Bent-Over Barbell Reverse Raise", value="bentover-barbell-reverse-raise"),
	app_commands.Choice(name="Barbell Rear Delt Raise", value="barbell-rear-delt-raise"),
	app_commands.Choice(name="Smith Machine Shrug", value="smith-machine-shrug"),
	app_commands.Choice(name="Incline Dumbbell Reverse Fly", value="incline-dumbbell-reverse-fly"),
	app_commands.Choice(name="Incline Dumbbell Y-Raise", value="incline-dumbbell-yraise"),
	app_commands.Choice(name="Dumbbell Incline T-Raise", value="dumbbell-incline-traise"),
	app_commands.Choice(name="Swimming", value="swimming"),
	app_commands.Choice(name="Bent Over Rear Delt Fly | Gymstick", value="bent-over-rear-delt-fly-gymstick"),
	app_commands.Choice(name="Scapular Protraction and Retraction", value="scapular-protraction-and-retraction"),
	app_commands.Choice(name="Cross Cable Face Pull", value="cross-cable-face-pull"),
	app_commands.Choice(name="Elbow Reverse Push-Up", value="elbow-reverse-pushup"),
	app_commands.Choice(name="Scapula Dips", value="scapula-dips"),
	app_commands.Choice(name="Push-Up Plus", value="pushup-plus"),
	app_commands.Choice(name="Seated Ballerina Exercise", value="seated-ballerina-exercise"),
	app_commands.Choice(name="Seated Scapular Retraction Exercise", value="seated-scapular-retraction-exercise"),
	app_commands.Choice(name="Foam Roller Rhomboids", value="foam-roller-rhomboids"),
	app_commands.Choice(name="Foam Roller Upper Back", value="foam-roller-upper-back"),
	app_commands.Choice(name="Scapula Pull-up", value="scapula-pullup"),
	app_commands.Choice(name="Serratus Wall Slide With Foam Roller", value="serratus-wall-slide-with-foam-roller"),
	app_commands.Choice(name="Dip Shrugs (Serratus Shrugs)", value="dip-shrugs-serratus-shrugs"),
	app_commands.Choice(name="Wide Grip Barbell Bent Over Row Plus", value="wide-grip-barbell-bent-over-row-plus"),
	app_commands.Choice(name="Wide Grip Alternate Barbell Bent Over Row Plus", value="wide-grip-alternate-barbell-bent-over-row-plus"),
	app_commands.Choice(name="One-Arm Dumbbell Upright Row", value="onearm-dumbbell-upright-row"),
	app_commands.Choice(name="Cable Y Raise", value="cable-y-raise"),
	app_commands.Choice(name="Barbell Upright Row", value="barbell-upright-row"),
	app_commands.Choice(name="Resistance Band Bent Over Rear Delt Fly", value="resistance-band-bent-over-rear-delt-fly"),
	app_commands.Choice(name="Resistance Band Pull Apart", value="resistance-band-pull-apart"),
	app_commands.Choice(name="Single Arm Upright Row | Gymstick", value="single-arm-upright-row-gymstick"),
	app_commands.Choice(name="Face Pull With Resistance Band", value="face-pull-with-resistance-band"),
	app_commands.Choice(name="Seated Barbell Shoulder Press", value="seated-barbell-shoulder-press"),
	app_commands.Choice(name="Dumbbell Push Press", value="dumbbell-push-press"),
	app_commands.Choice(name="Standing Dumbbell Shoulder Press", value="standing-dumbbell-shoulder-press"),
	app_commands.Choice(name="Arm Scissors", value="arm-scissors"),
	app_commands.Choice(name="Side Arm Raises", value="side-arm-raises"),
	app_commands.Choice(name="Arm Circles", value="arm-circles"),
	app_commands.Choice(name="Dumbbell Lateral Raise", value="dumbbell-lateral-raise"),
	app_commands.Choice(name="Dumbbell Shoulder Press", value="dumbbell-shoulder-press"),
	app_commands.Choice(name="Smith Machine Behind Neck Press", value="smith-machine-behind-neck-press"),
	app_commands.Choice(name="Smith Machine Shoulder Press", value="smith-machine-shoulder-press"),
	app_commands.Choice(name="Cable Lateral Raise", value="cable-lateral-raise"),
	app_commands.Choice(name="Lever Shoulder Press", value="lever-shoulder-press"),
	app_commands.Choice(name="Standing Close Grip Military Press", value="standing-close-grip-military-press"),
	app_commands.Choice(name="Dumbbell Chest Supported Lateral Raises", value="dumbbell-chest-supported-lateral-raises"),
	app_commands.Choice(name="Dumbbell 6 Way Raise", value="dumbbell-6-way-raise"),
	app_commands.Choice(name="Dumbbell 4 Way Lateral Raise", value="dumbbell-4-way-lateral-raise"),
	app_commands.Choice(name="Alternating Dumbbell Front Raise", value="alternating-dumbbell-front-raise"),
	app_commands.Choice(name="Two Arm Cable Front Raise", value="two-arm-cable-front-raise"),
	app_commands.Choice(name="Two Arm Dumbbell Front Raise", value="two-arm-dumbbell-front-raise"),
	app_commands.Choice(name="Dumbbell Front Raise", value="dumbbell-front-raise"),
	app_commands.Choice(name="Cable Front Raise", value="cable-front-raise"),
	app_commands.Choice(name="Leaning Single Arm Dumbbell Lateral Raise", value="leaning-single-arm-dumbbell-lateral-raise"),
	app_commands.Choice(name="Seated Behind Neck Press", value="seated-behind-neck-press"),
	app_commands.Choice(name="Seated Rear Lateral Dumbbell Raise", value="seated-rear-lateral-dumbbell-raise"),
	app_commands.Choice(name="Half Arnold Press", value="half-arnold-press"),
	app_commands.Choice(name="Arnold Press", value="arnold-press"),
	app_commands.Choice(name="Seated Dumbbell Lateral Raise", value="seated-dumbbell-lateral-raise"),
	app_commands.Choice(name="Bent Arm Lateral Raise", value="bent-arm-lateral-raise"),
	app_commands.Choice(name="Leaning Cable Lateral Raise", value="leaning-cable-lateral-raise"),
	app_commands.Choice(name="Push Press", value="push-press"),
	app_commands.Choice(name="Dumbbell Lying One-Arm Rear Lateral Raise", value="dumbbell-lying-onearm-rear-lateral-raise"),
	app_commands.Choice(name="Lateral Raise Machine", value="lateral-raise-machine"),
	app_commands.Choice(name="Scott Press", value="scott-press"),
	app_commands.Choice(name="Weighted Round Arm", value="weighted-round-arm"),
	app_commands.Choice(name="Weight Plate Front Raise", value="weight-plate-front-raise"),
	app_commands.Choice(name="Two Arm Cable Lateral Raise", value="two-arm-cable-lateral-raise"),
	app_commands.Choice(name="Landmine Squat to Press", value="landmine-squat-to-press"),
	app_commands.Choice(name="Cable Shoulder Press", value="cable-shoulder-press"),
	app_commands.Choice(name="Double Cable Front Raise", value="double-cable-front-raise"),
	app_commands.Choice(name="Standing Smith Machine Shoulder Press", value="standing-smith-machine-shoulder-press"),
	app_commands.Choice(name="Dumbbell W Press", value="dumbbell-w-press"),
	app_commands.Choice(name="Dumbbell One Arm Shoulder Press", value="dumbbell-one-arm-shoulder-press"),
	app_commands.Choice(name="Dumbbell Scaption", value="dumbbell-scaption"),
	app_commands.Choice(name="Barbell Clean and Press", value="barbell-clean-and-press"),
	app_commands.Choice(name="Dumbbell Cuban Press", value="dumbbell-cuban-press"),
	app_commands.Choice(name="Dumbbell Cuban External Rotation", value="dumbbell-cuban-external-rotation"),
	app_commands.Choice(name="Standing Alternating Dumbbell Shoulder Press", value="standing-alternating-dumbbell-shoulder-press"),
	app_commands.Choice(name="Cable External Shoulder Rotation", value="cable-external-shoulder-rotation"),
	app_commands.Choice(name="Cable Internal Shoulder Rotation", value="cable-internal-shoulder-rotation"),
	app_commands.Choice(name="Across Chest Shoulder Stretch", value="across-chest-shoulder-stretch"),
	app_commands.Choice(name="Standing Reach Up Back rotation Stretch", value="standing-reach-up-back-rotation-stretch"),
	app_commands.Choice(name="Shoulder Stretch Behind The Back", value="shoulder-stretch-behind-the-back"),
	app_commands.Choice(name="Incline Dumbbell Side Lateral Raise", value="incline-dumbbell-side-lateral-raise"),
	app_commands.Choice(name="Dumbbell Side Lying Rear Delt Raise", value="dumbbell-side-lying-rear-delt-raise"),
	app_commands.Choice(name="Lying Cable Reverse Fly", value="lying-cable-reverse-fly"),
	app_commands.Choice(name="Single Arm Circles", value="single-arm-circles"),
	app_commands.Choice(name="Dumbbell Lateral to Front Raise", value="dumbbell-lateral-to-front-raise"),
	app_commands.Choice(name="One-Arm Bent Over Cable Lateral Raise", value="onearm-bent-over-cable-lateral-raise"),
	app_commands.Choice(name="Handstand Push-Up", value="handstand-pushup"),
	app_commands.Choice(name="EZ Bar Underhand Press", value="ez-bar-underhand-press"),
	app_commands.Choice(name="Dumbbell Lying External Shoulder Rotation", value="dumbbell-lying-external-shoulder-rotation"),
	app_commands.Choice(name="Bench Supported Dumbbell External Rotation", value="bench-supported-dumbbell-external-rotation"),
	app_commands.Choice(name="Dumbbell Seated Bent Over Rear Delt Row", value="dumbbell-seated-bent-over-rear-delt-row"),
	app_commands.Choice(name="Dumbbell Standing Palms In Press", value="dumbbell-standing-palms-in-press"),
	app_commands.Choice(name="Lying Shoulder Press", value="lying-shoulder-press"),
	app_commands.Choice(name="Dumbbell Rear Delt Row", value="dumbbell-rear-delt-row"),
	app_commands.Choice(name="Lever Lateral Raise", value="lever-lateral-raise"),
	app_commands.Choice(name="Kettlebell One-Arm Military Press", value="kettlebell-onearm-military-press"),
	app_commands.Choice(name="Kettlebell Split Snatch", value="kettlebell-split-snatch"),
	app_commands.Choice(name="Kettlebell Windmill", value="kettlebell-windmill"),
	app_commands.Choice(name="Kettlebell Swings", value="kettlebell-swings"),
	app_commands.Choice(name="Kettlebell Arnold Press", value="kettlebell-arnold-press"),
	app_commands.Choice(name="Cable Seated Shoulder Internal Rotation", value="cable-seated-shoulder-internal-rotation"),
	app_commands.Choice(name="Half Kneeling Cable External Rotation", value="half-kneeling-cable-external-rotation"),
	app_commands.Choice(name="Landmine Lateral Raise", value="landmine-lateral-raise"),
	app_commands.Choice(name="Seated Dumbbell Front Raise", value="seated-dumbbell-front-raise"),
	app_commands.Choice(name="One Arm Kettlebell Snatch", value="one-arm-kettlebell-snatch"),
	app_commands.Choice(name="One Arm Landmine Row", value="one-arm-landmine-row"),
	app_commands.Choice(name="Resistance Band Seated Shoulder Press", value="resistance-band-seated-shoulder-press"),
	app_commands.Choice(name="Bench Pike Push-up", value="bench-pike-pushup"),
	app_commands.Choice(name="Pike Push-up", value="pike-pushup"),
	app_commands.Choice(name="Tall Kneeling One Arm Kettlebell Press", value="tall-kneeling-one-arm-kettlebell-press"),
	app_commands.Choice(name="Kettlebell Clean and Jerk", value="kettlebell-clean-and-jerk"),
	app_commands.Choice(name="Full Range Of Motion Lat Pulldown", value="full-range-of-motion-lat-pulldown"),
	app_commands.Choice(name="Lever Shoulder Press (Hammer Grip)", value="lever-shoulder-press-hammer-grip"),
	app_commands.Choice(name="Dumbbell Lying Rear Lateral Raise", value="dumbbell-lying-rear-lateral-raise"),
	app_commands.Choice(name="Lever Reverse Shoulder Press", value="lever-reverse-shoulder-press"),
	app_commands.Choice(name="Side Lying Rear Delt Dumbbell Raise", value="side-lying-rear-delt-dumbbell-raise"),
	app_commands.Choice(name="Ez-Bar Incline Front Raise", value="ezbar-incline-front-raise"),
	app_commands.Choice(name="Back Lever", value="back-lever"),
	app_commands.Choice(name="Barbell Front Raise Twist", value="barbell-front-raise-twist"),
	app_commands.Choice(name="Kettlebell Shoulder Press", value="kettlebell-shoulder-press"),
	app_commands.Choice(name="Wall-Supported Handstand Push-Ups", value="wallsupported-handstand-pushups"),
	app_commands.Choice(name="Towel Shoulder Stretch", value="towel-shoulder-stretch"),
	app_commands.Choice(name="Kettlebell Thruster", value="kettlebell-thruster"),
	app_commands.Choice(name="One Arm Dumbbell Snatch", value="one-arm-dumbbell-snatch"),
	app_commands.Choice(name="Band Front Lateral Raise", value="band-front-lateral-raise"),
	app_commands.Choice(name="Shoulder Pendulum", value="shoulder-pendulum"),
	app_commands.Choice(name="90-Degree Cable External Rotation", value="90degree-cable-external-rotation"),
	app_commands.Choice(name="90-degree Cable Internal Rotation", value="90degree-cable-internal-rotation"),
	app_commands.Choice(name="Foam Roller Posterior Shoulder", value="foam-roller-posterior-shoulder"),
	app_commands.Choice(name="Foam Roller Front Shoulder and Chest", value="foam-roller-front-shoulder-and-chest"),
	app_commands.Choice(name="Rotator Cuff Stretch", value="rotator-cuff-stretch"),
	app_commands.Choice(name="Assisted Reverse Stretch (Chest And Shoulder)", value="assisted-reverse-stretch-chest-and-shoulder"),
	app_commands.Choice(name="Lying Upper Body Rotation", value="lying-upper-body-rotation"),
	app_commands.Choice(name="Kneeling Back Rotation", value="kneeling-back-rotation"),
	app_commands.Choice(name="Wall Supported Arm Raises", value="wall-supported-arm-raises"),
	app_commands.Choice(name="Backhand Raise", value="backhand-raise"),
	app_commands.Choice(name="Dumbbell Seated Cuban Press", value="dumbbell-seated-cuban-press"),
	app_commands.Choice(name="Kneeling Cable Shoulder Press", value="kneeling-cable-shoulder-press"),
	app_commands.Choice(name="Wall Slides", value="wall-slides"),
	app_commands.Choice(name="Kneeling T-spine Rotation", value="kneeling-tspine-rotation"),
	app_commands.Choice(name="Plate Loaded Shoulder Press", value="plate-loaded-shoulder-press"),
	app_commands.Choice(name="Chest Supported Dumbbell Front Raises", value="chest-supported-dumbbell-front-raises"),
	app_commands.Choice(name="Single Arm Arnold Press", value="single-arm-arnold-press"),
	app_commands.Choice(name="Kneeling Landmine Press", value="kneeling-landmine-press"),
	app_commands.Choice(name="Pike Push-Up Between Chairs", value="pike-pushup-between-chairs"),
	app_commands.Choice(name="Kettlebell Clean and Press", value="kettlebell-clean-and-press"),
	app_commands.Choice(name="Dumbbell Z Press", value="dumbbell-z-press"),
	app_commands.Choice(name="Alternate Dumbbell Lateral Raise", value="alternate-dumbbell-lateral-raise"),
	app_commands.Choice(name="Back Slaps Wrap Around Stretch", value="back-slaps-wrap-around-stretch"),
	app_commands.Choice(name="Reaction Ball Throw", value="reaction-ball-throw"),
	app_commands.Choice(name="Front Rack PVC Stretch", value="front-rack-pvc-stretch"),
	app_commands.Choice(name="Lever High Row", value="lever-high-row"),
	app_commands.Choice(name="Cable Half Kneeling Pallof Press", value="cable-half-kneeling-pallof-press"),
	app_commands.Choice(name="Chest and Front of Shoulder Stretch", value="chest-and-front-of-shoulder-stretch"),
	app_commands.Choice(name="Shoulder External Rotation", value="shoulder-external-rotation"),
	app_commands.Choice(name="Shoulder Internal Rotation", value="shoulder-internal-rotation"),
	app_commands.Choice(name="Lateral Raise with Towel on Wall", value="lateral-raise-with-towel-on-wall"),
	app_commands.Choice(name="Alternating Shoulder Flexion", value="alternating-shoulder-flexion"),
	app_commands.Choice(name="Banded Shoulder External Rotation", value="banded-shoulder-external-rotation"),
	app_commands.Choice(name="Banded Shoulder Flexion", value="banded-shoulder-flexion"),
	app_commands.Choice(name="Banded Shoulder Extension", value="banded-shoulder-extension"),
	app_commands.Choice(name="Band Single Arm Shoulder Press", value="band-single-arm-shoulder-press"),
	app_commands.Choice(name="Handstand Push-ups Between Benches", value="handstand-pushups-between-benches"),
	app_commands.Choice(name="Kipping Handstand Push-up", value="kipping-handstand-pushup"),
	app_commands.Choice(name="Bent-Over Dumbbell Rear Delt Raise With Head On Bench", value="bentover-dumbbell-rear-delt-raise-with-head-on-bench"),
	app_commands.Choice(name="Hindu Push-ups", value="hindu-pushups"),
	app_commands.Choice(name="Barbell Front Raise", value="barbell-front-raise"),
	app_commands.Choice(name="Corner Wall Stretch", value="corner-wall-stretch"),
	app_commands.Choice(name="Barbell Thruster", value="barbell-thruster"),
	app_commands.Choice(name="One Arm Kettlebell Swing", value="one-arm-kettlebell-swing"),
	app_commands.Choice(name="Standing Reverse Shoulder Stretch", value="standing-reverse-shoulder-stretch"),
	app_commands.Choice(name="Medicine ball Overhead Slam", value="medicine-ball-overhead-slam"),
	app_commands.Choice(name="Doorway Pec and Shoulder Stretch", value="doorway-pec-and-shoulder-stretch"),
	app_commands.Choice(name="Wall Ball", value="wall-ball"),
	app_commands.Choice(name="Kettlebell Lateral Raise", value="kettlebell-lateral-raise"),
	app_commands.Choice(name="Dumbbell Windmill", value="dumbbell-windmill"),
	app_commands.Choice(name="Dumbbell Iron Cross", value="dumbbell-iron-cross"),
	app_commands.Choice(name="Incline Landmine Press", value="incline-landmine-press"),
	app_commands.Choice(name="Medicine Ball Overhead Throw", value="medicine-ball-overhead-throw"),
	app_commands.Choice(name="One Arm Medicine Ball Slam", value="one-arm-medicine-ball-slam"),
	app_commands.Choice(name="Dumbbell Single Arm Lateral Raise", value="dumbbell-single-arm-lateral-raise"),
	app_commands.Choice(name="Dumbbell Seated Alternate Front Raise", value="dumbbell-seated-alternate-front-raise"),
	app_commands.Choice(name="Swing | Gymstick", value="swing-gymstick"),
	app_commands.Choice(name="Side Bend Press | Gymstick", value="side-bend-press-gymstick"),
	app_commands.Choice(name="Behind the Head Military Press | Gymstick", value="behind-the-head-military-press-gymstick"),
	app_commands.Choice(name="Skier | Gymstick", value="skier-gymstick"),
	app_commands.Choice(name="Bent Over Row | Gymstick", value="bent-over-row-gymstick"),
	app_commands.Choice(name="Battle Rope", value="battle-rope"),
	app_commands.Choice(name="Incline Chest Fly Machine", value="incline-chest-fly-machine"),
	app_commands.Choice(name="Pec Deck Fly", value="pec-deck-fly"),
	app_commands.Choice(name="Dumbbell Pullover", value="dumbbell-pullover"),
	app_commands.Choice(name="Low Cable Crossover", value="low-cable-crossover"),
	app_commands.Choice(name="High Cable Crossover", value="high-cable-crossover"),
	app_commands.Choice(name="Cable Upper Chest Crossovers", value="cable-upper-chest-crossovers"),
	app_commands.Choice(name="Incline Bench", value="incline-bench"),
	app_commands.Choice(name="Dumbbell Fly", value="dumbbell-fly"),
	app_commands.Choice(name="Dumbbell Bench Press", value="dumbbell-bench-press"),
	app_commands.Choice(name="Cable Crossover", value="cable-crossover"),
	app_commands.Choice(name="One-Arm Cable Chest Press", value="onearm-cable-chest-press"),
	app_commands.Choice(name="Single-Arm Cable Crossover", value="singlearm-cable-crossover"),
	app_commands.Choice(name="Incline Dumbbell Fly", value="incline-dumbbell-fly"),
	app_commands.Choice(name="Incline Dumbbell Press", value="incline-dumbbell-press"),
	app_commands.Choice(name="Reverse Grip Incline Dumbbell Press", value="reverse-grip-incline-dumbbell-press"),
	app_commands.Choice(name="Machine Fly", value="machine-fly"),
	app_commands.Choice(name="Decline Dumbbell Press", value="decline-dumbbell-press"),
	app_commands.Choice(name="Lever Incline Chest Press", value="lever-incline-chest-press"),
	app_commands.Choice(name="Chest Dips", value="dips"),
	app_commands.Choice(name="Assisted Chest Dip", value="assisted-chest-dip"),
	app_commands.Choice(name="Lying Cable Fly", value="lying-cable-fly"),
	app_commands.Choice(name="Drop Push-Up", value="drop-pushup"),
	app_commands.Choice(name="Inner Chest Press Machine", value="inner-chest-press-machine"),
	app_commands.Choice(name="Decline Dumbbell Fly", value="decline-dumbbell-fly"),
	app_commands.Choice(name="Incline Dumbbell Hammer Press", value="incline-dumbbell-hammer-press"),
	app_commands.Choice(name="Dumbbell Upward Fly", value="dumbbell-upward-fly"),
	app_commands.Choice(name="Narrow Grip Wall Push-Up", value="narrow-grip-wall-pushup"),
	app_commands.Choice(name="Decline Chest Press Machine", value="decline-chest-press-machine"),
	app_commands.Choice(name="Lying Chest Press Machine", value="lying-chest-press-machine"),
	app_commands.Choice(name="Wall Push-up", value="wall-pushup"),
	app_commands.Choice(name="Smith Machine Hex Press", value="smith-machine-hex-press"),
	app_commands.Choice(name="Close-grip Incline Dumbbell Press", value="closegrip-incline-dumbbell-press"),
	app_commands.Choice(name="Kneeling Push-up", value="kneeling-pushup"),
	app_commands.Choice(name="Decline Cable Fly", value="decline-cable-fly"),
	app_commands.Choice(name="Smith Machine Bench Press", value="smith-machine-bench-press"),
	app_commands.Choice(name="Smith Machine Incline Bench Press", value="smith-machine-incline-bench-press"),
	app_commands.Choice(name="Parallel Bar Dips", value="parallel-bar-dips"),
	app_commands.Choice(name="Back And Pec Stretch", value="back-and-pec-stretch"),
	app_commands.Choice(name="Lever Incline Hammer Chest Press", value="lever-incline-hammer-chest-press"),
	app_commands.Choice(name="Lever Crossovers", value="lever-crossovers"),
	app_commands.Choice(name="Reverse Grip Dumbbell Bench Press", value="reverse-grip-dumbbell-bench-press"),
	app_commands.Choice(name="Lever Chest Press", value="lever-chest-press"),
	app_commands.Choice(name="Incline Push-up", value="incline-pushup"),
	app_commands.Choice(name="Svend Press", value="svend-press"),
	app_commands.Choice(name="Reverse Push-up", value="reverse-pushup"),
	app_commands.Choice(name="Alternate Dumbbell Bench Press", value="alternate-dumbbell-bench-press"),
	app_commands.Choice(name="Close-Grip Dumbbell Press", value="closegrip-dumbbell-press"),
	app_commands.Choice(name="Clap Push-Up", value="clap-pushup"),
	app_commands.Choice(name="Above Head Chest Stretch", value="above-head-chest-stretch"),
	app_commands.Choice(name="Dynamic Chest Stretch", value="dynamic-chest-stretch"),
	app_commands.Choice(name="Single Dumbbell Close-grip Press", value="single-dumbbell-closegrip-press"),
	app_commands.Choice(name="Kneeling Diamond Push-Up", value="kneeling-diamond-pushup"),
	app_commands.Choice(name="Dips Between Chairs", value="dips-between-chairs"),
	app_commands.Choice(name="Push-up Bars", value="pushup-bars"),
	app_commands.Choice(name="Smith Machine Decline Bench Press", value="smith-machine-decline-bench-press"),
	app_commands.Choice(name="One Arm Decline Cable Fly", value="one-arm-decline-cable-fly"),
	app_commands.Choice(name="Korean Dips", value="korean-dips"),
	app_commands.Choice(name="Straight Bar Dip", value="straight-bar-dip"),
	app_commands.Choice(name="Dumbbell One Arm Reverse Grip Press", value="dumbbell-one-arm-reverse-grip-press"),
	app_commands.Choice(name="Lever One Arm Chest Press", value="lever-one-arm-chest-press"),
	app_commands.Choice(name="Standing One Arm Chest Stretch", value="standing-one-arm-chest-stretch"),
	app_commands.Choice(name="Single Arm Medicine Ball Push-Up", value="single-arm-medicine-ball-pushup"),
	app_commands.Choice(name="Stability Ball Decline Push-Up", value="stability-ball-decline-pushup"),
	app_commands.Choice(name="Dumbbell Pullover On Stability Ball", value="dumbbell-pullover-on-stability-ball"),
	app_commands.Choice(name="Stability Ball Push-Up", value="stability-ball-pushup"),
	app_commands.Choice(name="Dumbbell Decline One-Arm Hammer Press", value="dumbbell-decline-onearm-hammer-press"),
	app_commands.Choice(name="Weighted Push-up", value="weighted-pushup"),
	app_commands.Choice(name="Single-Arm Push-Up", value="singlearm-pushup"),
	app_commands.Choice(name="One-Arm Kettlebell Chest Press", value="onearm-kettlebell-chest-press"),
	app_commands.Choice(name="Kettlebell Chest Press on the Floor", value="kettlebell-chest-press-on-the-floor"),
	app_commands.Choice(name="Wide Grip Bench Press", value="wide-grip-bench-press"),
	app_commands.Choice(name="Decline Barbell Bench Press", value="decline-barbell-bench-press"),
	app_commands.Choice(name="One Arm Push Ups With Support", value="one-arm-push-ups-with-support"),
	app_commands.Choice(name="Band Standing Chest Press", value="band-standing-chest-press"),
	app_commands.Choice(name="Seated Chest Stretch", value="seated-chest-stretch"),
	app_commands.Choice(name="Foam Roller Chest Stretch", value="foam-roller-chest-stretch"),
	app_commands.Choice(name="Lever Decline Chest Press", value="lever-decline-chest-press"),
	app_commands.Choice(name="Incline Chest Press Machine", value="incline-chest-press-machine"),
	app_commands.Choice(name="Incline Cable Fly", value="incline-cable-fly"),
	app_commands.Choice(name="Reverse Chest Stretch", value="reverse-chest-stretch"),
	app_commands.Choice(name="Seated Cable Chest Press", value="seated-cable-chest-press"),
	app_commands.Choice(name="Seated Cable Close Grip Chest Press", value="seated-cable-close-grip-chest-press"),
	app_commands.Choice(name="Forearm Push-up", value="forearm-pushup"),
	app_commands.Choice(name="Banded Shoulder Adduction", value="banded-shoulder-adduction"),
	app_commands.Choice(name="Band Alternate Incline Chest Press", value="band-alternate-incline-chest-press"),
	app_commands.Choice(name="Incline Close-Grip Bench Press", value="incline-closegrip-bench-press"),
	app_commands.Choice(name="Close Grip Bench Press", value="close-grip-bench-press"),
	app_commands.Choice(name="Diamond Push-up", value="diamond-pushup"),
	app_commands.Choice(name="Pushups", value="pushups"),
	app_commands.Choice(name="Hammer Press", value="hammer-press"),
	app_commands.Choice(name="Chest Press Machine", value="chest-press-machine"),
	app_commands.Choice(name="Barbell Floor Press", value="barbell-floor-press"),
	app_commands.Choice(name="Landmine Floor Chest Fly", value="landmine-floor-chest-fly"),
	app_commands.Choice(name="Decline Hammer Press", value="decline-hammer-press"),
	app_commands.Choice(name="Close-Grip Reverse Bench Press", value="closegrip-reverse-bench-press"),
	app_commands.Choice(name="Wide-Grip Reverse Bench Press", value="widegrip-reverse-bench-press"),
	app_commands.Choice(name="Straddle Planche", value="straddle-planche"),
	app_commands.Choice(name="Close Grip Knee Push-up", value="close-grip-knee-pushup"),
	app_commands.Choice(name="Push-up With Rotation", value="pushup-with-rotation"),
	app_commands.Choice(name="Supine Medicine Ball Chest Throw", value="supine-medicine-ball-chest-throw"),
	app_commands.Choice(name="Reverse Dips", value="reverse-dips"),
	app_commands.Choice(name="Trx Chest Press", value="trx-chest-press"),
	app_commands.Choice(name="Dumbbell Straight Arm Pullover (knees at 90 degrees)", value="dumbbell-straight-arm-pullover-knees-at-90-degrees"),
	app_commands.Choice(name="Trx Chest Fly", value="trx-chest-fly"),
	app_commands.Choice(name="Kettlebell Renegade Row", value="kettlebell-renegade-row"),
	app_commands.Choice(name="Push-Up to Renegade Row", value="pushup-to-renegade-row"),
	app_commands.Choice(name="Modified Hindu Push-up", value="modified-hindu-pushup"),
	app_commands.Choice(name="Knuckle Push-Up", value="knuckle-pushup"),
	app_commands.Choice(name="Planche Push-Up", value="planche-pushup"),
	app_commands.Choice(name="Finger Push-up", value="finger-pushup"),
	app_commands.Choice(name="Chest Tap Push-up", value="chest-tap-pushup"),
	app_commands.Choice(name="Kettlebell Deep Push-Up", value="kettlebell-deep-pushup"),
	app_commands.Choice(name="Archer Push-Up", value="archer-pushup"),
	app_commands.Choice(name="One Leg Push-Up", value="one-leg-pushup"),
	app_commands.Choice(name="Bosu Ball Push-Up", value="bosu-ball-pushup"),
	app_commands.Choice(name="Resistance Band Alternating Chest Fly", value="resistance-band-alternating-chest-fly"),
	app_commands.Choice(name="Dumbbell Reverse Grip 30 Degrees Incline Bench Press", value="dumbbell-reverse-grip-30-degrees-incline-bench-press"),
	app_commands.Choice(name="Ring Dips", value="ring-dips"),
	app_commands.Choice(name="Cobra Push-up", value="cobra-pushup"),
	app_commands.Choice(name="Shoulder Tap Push-up", value="shoulder-tap-pushup"),
	app_commands.Choice(name="Single Arm Raise Push-up", value="single-arm-raise-pushup"),
	app_commands.Choice(name="Suspended Push-Up", value="suspended-pushup"),
	app_commands.Choice(name="Close-grip Dumbbell Push-Up", value="closegrip-dumbbell-pushup"),
	app_commands.Choice(name="Medicine Ball Push-Up", value="medicine-ball-pushup"),
	app_commands.Choice(name="Single Arm Push-Up on Medicine Ball", value="single-arm-pushup-on-medicine-ball"),
	app_commands.Choice(name="Weighted Vest Push-up", value="weighted-vest-pushup"),
	app_commands.Choice(name="Standing Medicine Ball Chest Pass", value="standing-medicine-ball-chest-pass"),
	app_commands.Choice(name="Standing incline chest press With Resistance Band", value="standing-incline-chest-press-with-resistance-band"),
	app_commands.Choice(name="Middle Chest fly With Resistance Band", value="middle-chest-fly-with-resistance-band"),
	app_commands.Choice(name="Kneeling Incline Press | Gymstick", value="kneeling-incline-press-gymstick"),
	app_commands.Choice(name="Low Chest Fly With Resistance Band", value="low-chest-fly-with-resistance-band"),
	app_commands.Choice(name="High Chest Fly With Resistance Band", value="high-chest-fly-with-resistance-band"),
	app_commands.Choice(name="Decline Push-up", value="decline-pushup"),
	app_commands.Choice(name="Rowing Machine", value="rowing-machine"),
	app_commands.Choice(name="Lever Front Pulldown", value="lever-front-pulldown"),
	app_commands.Choice(name="Pull-ups", value="pullups"),
	app_commands.Choice(name="Cable Rear Pulldown", value="cable-rear-pulldown"),
	app_commands.Choice(name="Lat Pulldown", value="lat-pulldown"),
	app_commands.Choice(name="Rows", value="rows"),
	app_commands.Choice(name="Barbell Bent Over Row", value="barbell-bent-over-row"),
	app_commands.Choice(name="Cable Straight Arm Pulldown", value="cable-straight-arm-pulldown"),
	app_commands.Choice(name="Legless Rope Climb", value="legless-rope-climb"),
	app_commands.Choice(name="Lever T-Bar Row", value="lever-tbar-row"),
	app_commands.Choice(name="Dumbbell Row", value="dumbbell-row"),
	app_commands.Choice(name="Bent Over Dumbbell Row", value="bent-over-dumbbell-row"),
	app_commands.Choice(name="Dumbbell Bent Over Reverse Grip Row", value="dumbbell-bent-over-reverse-grip-row"),
	app_commands.Choice(name="Reverse Lat-Pulldown", value="reverse-latpulldown"),
	app_commands.Choice(name="Muscle-Up", value="muscleup"),
	app_commands.Choice(name="Seated Row Machine", value="seated-row-machine"),
	app_commands.Choice(name="One Arm Cable Row", value="one-arm-cable-row"),
	app_commands.Choice(name="Reverse Grip Barbell Row", value="reverse-grip-barbell-row"),
	app_commands.Choice(name="Romanian Deadlift", value="romanian-deadlift"),
	app_commands.Choice(name="Upper Back Stretch", value="upper-back-stretch"),
	app_commands.Choice(name="Sumo Deadlift", value="sumo-deadlift"),
	app_commands.Choice(name="Half Kneeling Lat Pulldown", value="half-kneeling-lat-pulldown"),
	app_commands.Choice(name="Dumbbell Straight Leg Deadlift", value="dumbbell-straight-leg-deadlift"),
	app_commands.Choice(name="Smith Machine Bent Over Row", value="smith-machine-bent-over-row"),
	app_commands.Choice(name="Incline Reverse Grip Dumbbell Row", value="incline-reverse-grip-dumbbell-row"),
	app_commands.Choice(name="Barbell Pullover", value="barbell-pullover"),
	app_commands.Choice(name="Cable Pullover", value="cable-pullover"),
	app_commands.Choice(name="Weighted Pull-up", value="weighted-pullup"),
	app_commands.Choice(name="Reverse grip Pull-up", value="reverse-grip-pullup"),
	app_commands.Choice(name="Close Grip Chin Up", value="close-grip-chin-up"),
	app_commands.Choice(name="Assisted Pull-up", value="assisted-pullup"),
	app_commands.Choice(name="Table Inverted Row", value="table-inverted-row"),
	app_commands.Choice(name="Cable One Arm Lat Pulldown", value="cable-one-arm-lat-pulldown"),
	app_commands.Choice(name="Reverse Grip Machine Row", value="reverse-grip-machine-row"),
	app_commands.Choice(name="Close Grip Cable Row", value="close-grip-cable-row"),
	app_commands.Choice(name="Rope Straight Arm Pulldown", value="rope-straight-arm-pulldown"),
	app_commands.Choice(name="V-bar Lat Pulldown", value="vbar-lat-pulldown"),
	app_commands.Choice(name="One-Arm Barbell Row", value="onearm-barbell-row"),
	app_commands.Choice(name="T-Bar Row", value="tbar-row"),
	app_commands.Choice(name="Incline Cable Row", value="incline-cable-row"),
	app_commands.Choice(name="Cable Bent Over Row", value="cable-bent-over-row"),
	app_commands.Choice(name="Standing Side Bend Stretch", value="standing-side-bend-stretch"),
	app_commands.Choice(name="Double Cable Neutral Grip Lat Pulldown On Floor", value="double-cable-neutral-grip-lat-pulldown-on-floor"),
	app_commands.Choice(name="Incline Barbell Row", value="incline-barbell-row"),
	app_commands.Choice(name="Kneeling Single Arm High Pulley Row", value="kneeling-single-arm-high-pulley-row"),
	app_commands.Choice(name="Upside Down Pull-up", value="upside-down-pullup"),
	app_commands.Choice(name="Brachialis Pull-up", value="brachialis-pullup"),
	app_commands.Choice(name="Close Grip Lat-Pulldown", value="close-grip-latpulldown"),
	app_commands.Choice(name="Seated Cable Rope Row", value="seated-cable-rope-row"),
	app_commands.Choice(name="Cable Seated Pullover", value="cable-seated-pullover"),
	app_commands.Choice(name="Ring Inverted Row", value="ring-inverted-row"),
	app_commands.Choice(name="Inverted Row", value="inverted-row"),
	app_commands.Choice(name="Lever Cable Rear Pulldown", value="lever-cable-rear-pulldown"),
	app_commands.Choice(name="Shotgun Row", value="shotgun-row"),
	app_commands.Choice(name="Weighted One Arm Pull-up", value="weighted-one-arm-pullup"),
	app_commands.Choice(name="Cable Crossover Lat Pulldown", value="cable-crossover-lat-pulldown"),
	app_commands.Choice(name="Lever Reverse T-Bar Row", value="lever-reverse-tbar-row"),
	app_commands.Choice(name="Kettlebell Bent Over Row", value="kettlebell-bent-over-row"),
	app_commands.Choice(name="Chin-Up", value="chinup"),
	app_commands.Choice(name="Seated Toe Touches", value="seated-toe-touches"),
	app_commands.Choice(name="L-Sit Pull-Up", value="lsit-pullup"),
	app_commands.Choice(name="Swing 360", value="swing-360"),
	app_commands.Choice(name="Front Lever Pull-up", value="front-lever-pullup"),
	app_commands.Choice(name="Foam Roller Back Stretch", value="foam-roller-back-stretch"),
	app_commands.Choice(name="Foam Roller Lat Stretch", value="foam-roller-lat-stretch"),
	app_commands.Choice(name="Lever Pullover", value="lever-pullover"),
	app_commands.Choice(name="One Arm Chin-Up", value="one-arm-chinup"),
	app_commands.Choice(name="Archer Pull-up", value="archer-pullup"),
	app_commands.Choice(name="Jumping Pull-up", value="jumping-pullup"),
	app_commands.Choice(name="Commando Pull-up", value="commando-pullup"),
	app_commands.Choice(name="Behind The Neck Pull-up", value="behind-the-neck-pullup"),
	app_commands.Choice(name="Cable One-Arm Pulldown", value="cable-onearm-pulldown"),
	app_commands.Choice(name="Barbell Decline Bent Arm Pullover", value="barbell-decline-bent-arm-pullover"),
	app_commands.Choice(name="Dead Hang", value="dead-hang"),
	app_commands.Choice(name="Isometric Pull-Up", value="isometric-pullup"),
	app_commands.Choice(name="Climbing Monkey Bars", value="climbing-monkey-bars"),
	app_commands.Choice(name="Supine Spinal Twist", value="supine-spinal-twist"),
	app_commands.Choice(name="Bodyweight Row in Doorway", value="bodyweight-row-in-doorway"),
	app_commands.Choice(name="Incline Dumbbell Hammer Row", value="incline-dumbbell-hammer-row"),
	app_commands.Choice(name="Plate Loaded Seated Row", value="plate-loaded-seated-row"),
	app_commands.Choice(name="Chin Up Around the Bar", value="chin-up-around-the-bar"),
	app_commands.Choice(name="EZ-Bar Bent Arm Pullover", value="ezbar-bent-arm-pullover"),
	app_commands.Choice(name="Landmine T-Bar Row", value="landmine-tbar-row"),
	app_commands.Choice(name="Cable Twisting Standing High Row", value="cable-twisting-standing-high-row"),
	app_commands.Choice(name="Single Arm Twisting Seated Cable Row", value="single-arm-twisting-seated-cable-row"),
	app_commands.Choice(name="Band Alternating Lat Pulldown", value="band-alternating-lat-pulldown"),
	app_commands.Choice(name="Band Alternating Low Row with Twist", value="band-alternating-low-row-with-twist"),
	app_commands.Choice(name="Band Seated Row", value="band-seated-row"),
	app_commands.Choice(name="Barbell Pendlay Row", value="barbell-pendlay-row"),
	app_commands.Choice(name="Standing side bend", value="standing-side-bend"),
	app_commands.Choice(name="Neutral Grip Pull-up", value="neutral-grip-pullup"),
	app_commands.Choice(name="Dumbbell Seal Row", value="dumbbell-seal-row"),
	app_commands.Choice(name="Dumbbell Renegade Row", value="dumbbell-renegade-row"),
	app_commands.Choice(name="Band Assisted Pull-up", value="band-assisted-pullup"),
	app_commands.Choice(name="Standing Banded Row", value="standing-banded-row"),
	app_commands.Choice(name="Kneeling Pulldown With Resistance Band", value="kneeling-pulldown-with-resistance-band"),
	app_commands.Choice(name="Dumbbell Good Morning", value="dumbbell-good-morning"),
	app_commands.Choice(name="Dumbbell Deadlift", value="dumbbell-deadlift"),
	app_commands.Choice(name="Dumbbell Sumo Deadlift", value="dumbbell-sumo-deadlift"),
	app_commands.Choice(name="Seated Back Extension", value="seated-back-extension"),
	app_commands.Choice(name="Good Morning", value="good-morning"),
	app_commands.Choice(name="Weighted Back Extension", value="weighted-back-extension"),
	app_commands.Choice(name="Dumbbell Romanian Deadlift", value="dumbbell-romanian-deadlift"),
	app_commands.Choice(name="Seated Hamstring Stretch", value="seated-hamstring-stretch"),
	app_commands.Choice(name="Kettlebell Single Leg Deadlift", value="kettlebell-single-leg-deadlift"),
	app_commands.Choice(name="Hyperextension", value="hyperextension"),
	app_commands.Choice(name="Flat Bench Hyperextension", value="flat-bench-hyperextension"),
	app_commands.Choice(name="Reverse Hyperextension Machine", value="reverse-hyperextension-machine"),
	app_commands.Choice(name="Smith Machine Good Morning", value="smith-machine-good-morning"),
	app_commands.Choice(name="Cable Pull Through", value="cable-pull-through"),
	app_commands.Choice(name="Twisting Hyperextension", value="twisting-hyperextension"),
	app_commands.Choice(name="Frog Reverse Hyperextension", value="frog-reverse-hyperextension"),
	app_commands.Choice(name="Bird Dog", value="bird-dog"),
	app_commands.Choice(name="Kettlebell Deadlift", value="kettlebell-deadlift"),
	app_commands.Choice(name="Standing Toe Touches", value="standing-toe-touches"),
	app_commands.Choice(name="Stiff Leg Deadlift", value="stiff-leg-deadlift"),
	app_commands.Choice(name="Bow Pose", value="bow-pose"),
	app_commands.Choice(name="Cat Cow Pose", value="cat-cow-pose"),
	app_commands.Choice(name="Arm Leg Raises", value="arm-leg-raises"),
	app_commands.Choice(name="Dumbbell Pull Through", value="dumbbell-pull-through"),
	app_commands.Choice(name="Glute Ham Raise", value="glute-ham-raise"),
	app_commands.Choice(name="Side Plank Rotation", value="side-plank-rotation"),
	app_commands.Choice(name="Kettlebell Figure 8", value="kettlebell-figure-8"),
	app_commands.Choice(name="Barbell Single Leg Deadlift", value="barbell-single-leg-deadlift"),
	app_commands.Choice(name="Dumbbell Single Leg Deadlift", value="dumbbell-single-leg-deadlift"),
	app_commands.Choice(name="Good Morning With Resistance Band", value="good-morning-with-resistance-band"),
	app_commands.Choice(name="Rolling Like a Ball", value="rolling-like-a-ball"),
	app_commands.Choice(name="Dhanurasana | Rocking Bow Pose", value="dhanurasana-rocking-bow-pose"),
	app_commands.Choice(name="Single Leg Reverse Hyperextension | Gymstick", value="single-leg-reverse-hyperextension-gymstick"),
	app_commands.Choice(name="Seated Zottman Curl", value="seated-zottman-curl"),
	app_commands.Choice(name="Standing Barbell Concentration Curl", value="standing-barbell-concentration-curl"),
	app_commands.Choice(name="Waiter Curl", value="waiter-curl"),
	app_commands.Choice(name="Double Arm Dumbbell Curl", value="double-arm-dumbbell-curl"),
	app_commands.Choice(name="Dumbbell Curl", value="dumbbell-curl"),
	app_commands.Choice(name="Barbell Curl", value="barbell-curl"),
	app_commands.Choice(name="Concentration Curl", value="concentration-curl"),
	app_commands.Choice(name="Dumbbell Preacher Curl", value="dumbbell-preacher-curl"),
	app_commands.Choice(name="EZ Bar Preacher Curl", value="ez-bar-preacher-curl"),
	app_commands.Choice(name="Hammer Curl", value="hammer-curl"),
	app_commands.Choice(name="Incline Dumbbell Curl", value="incline-dumbbell-curl"),
	app_commands.Choice(name="Lever Preacher Curl", value="lever-preacher-curl"),
	app_commands.Choice(name="High Cable Single Arm Bicep Curl", value="high-cable-single-arm-bicep-curl"),
	app_commands.Choice(name="One Arm Cable Curl", value="one-arm-cable-curl"),
	app_commands.Choice(name="Lying Cable Curl", value="lying-cable-curl"),
	app_commands.Choice(name="Zottman Curl", value="zottman-curl"),
	app_commands.Choice(name="Dumbbell Reverse Curl", value="dumbbell-reverse-curl"),
	app_commands.Choice(name="Seated Close-Grip Concentration Curl", value="seated-closegrip-concentration-curl"),
	app_commands.Choice(name="Biceps Leg Concentration Curl", value="biceps-leg-concentration-curl"),
	app_commands.Choice(name="Prone Incline Barbell Curl", value="prone-incline-barbell-curl"),
	app_commands.Choice(name="Overhead Cable Curl", value="overhead-cable-curl"),
	app_commands.Choice(name="Seated Hammer Curl", value="seated-hammer-curl"),
	app_commands.Choice(name="Seated Biceps Curl", value="seated-biceps-curl"),
	app_commands.Choice(name="Single Arm Cable Preacher Curl", value="single-arm-cable-preacher-curl"),
	app_commands.Choice(name="Cable Concentration Curl", value="cable-concentration-curl"),
	app_commands.Choice(name="Reverse Grip EZ-Bar Curl", value="reverse-grip-ezbar-curl"),
	app_commands.Choice(name="Dumbbell Scott Hammer Curl", value="dumbbell-scott-hammer-curl"),
	app_commands.Choice(name="Lying High Bench Barbell Curl", value="lying-high-bench-barbell-curl"),
	app_commands.Choice(name="Cable Rope Hammer Curl", value="cable-rope-hammer-curl"),
	app_commands.Choice(name="Biceps Curl Machine", value="biceps-curl-machine"),
	app_commands.Choice(name="Dumbbell High Curl", value="dumbbell-high-curl"),
	app_commands.Choice(name="Close Grip Z-Bar Curl", value="close-grip-zbar-curl"),
	app_commands.Choice(name="Dumbbell Scott Curl", value="dumbbell-scott-curl"),
	app_commands.Choice(name="Barbell Curl On Arm Blaster", value="barbell-curl-on-arm-blaster"),
	app_commands.Choice(name="Arm Blaster Hammer Curl", value="arm-blaster-hammer-curl"),
	app_commands.Choice(name="Dumbbell Curl On Arm Blaster", value="dumbbell-curl-on-arm-blaster"),
	app_commands.Choice(name="One Arm Biceps Curl", value="one-arm-biceps-curl"),
	app_commands.Choice(name="Lever Biceps Curl", value="lever-biceps-curl"),
	app_commands.Choice(name="Cable Incline Biceps Curl", value="cable-incline-biceps-curl"),
	app_commands.Choice(name="Dumbbell Preacher Hammer (Scott) Curl", value="dumbbell-preacher-hammer-scott-curl"),
	app_commands.Choice(name="One Arm Prone Dumbbell Curl", value="one-arm-prone-dumbbell-curl"),
	app_commands.Choice(name="Dumbbell Alternate Preacher Curl", value="dumbbell-alternate-preacher-curl"),
	app_commands.Choice(name="Two Dumbbell Preacher Curl", value="two-dumbbell-preacher-curl"),
	app_commands.Choice(name="Barbell Alternate Biceps Curl", value="barbell-alternate-biceps-curl"),
	app_commands.Choice(name="Cable Kneeling Biceps Curl", value="cable-kneeling-biceps-curl"),
	app_commands.Choice(name="Cable Two Arm Curl on Incline Bench", value="cable-two-arm-curl-on-incline-bench"),
	app_commands.Choice(name="Elbow Flexion", value="elbow-flexion"),
	app_commands.Choice(name="Cable Pulldown Biceps Curl", value="cable-pulldown-biceps-curl"),
	app_commands.Choice(name="Band Biceps Curl", value="band-biceps-curl"),
	app_commands.Choice(name="Single Dumbbell Spider Hammer Curl", value="single-dumbbell-spider-hammer-curl"),
	app_commands.Choice(name="Cable Curl", value="cable-curl"),
	app_commands.Choice(name="Z-Bar Curl", value="zbar-curl"),
	app_commands.Choice(name="Hammer Curl with Resistance Band", value="hammer-curl-with-resistance-band"),
	app_commands.Choice(name="Cable Reverse Grip EZ-bar Biceps Curl", value="cable-reverse-grip-ezbar-biceps-curl"),
	app_commands.Choice(name="Barbell Drag Curl", value="barbell-drag-curl"),
	app_commands.Choice(name="Close Grip Barbell Curl", value="close-grip-barbell-curl"),
	app_commands.Choice(name="One Arm Cable Bicep Curl", value="one-arm-cable-bicep-curl"),
	app_commands.Choice(name="Single Arm Reverse Grip Cable Bicep Curl", value="single-arm-reverse-grip-cable-bicep-curl"),
	app_commands.Choice(name="Water Bottle Hammer Curl", value="water-bottle-hammer-curl"),
	app_commands.Choice(name="Seated Alternating Dumbbell Curl", value="seated-alternating-dumbbell-curl"),
	app_commands.Choice(name="Seated Bicep Curl With Resistance Band", value="seated-bicep-curl-with-resistance-band"),
	app_commands.Choice(name="One-Arm Biceps Curl With Resistance Band", value="onearm-biceps-curl-with-resistance-band"),
	app_commands.Choice(name="Barbell JM Press", value="barbell-jm-press"),
	app_commands.Choice(name="One Arm Triceps Pushdown", value="one-arm-triceps-pushdown"),
	app_commands.Choice(name="Dumbbell Kickback", value="dumbbell-kickback"),
	app_commands.Choice(name="One Arm Reverse Pushdown", value="one-arm-reverse-pushdown"),
	app_commands.Choice(name="Tricep Rope Pushdown", value="tricep-rope-pushdown"),
	app_commands.Choice(name="Bench Dips", value="bench-dips"),
	app_commands.Choice(name="Triceps Dips", value="triceps-dips"),
	app_commands.Choice(name="One Arm Lying Triceps Extension", value="one-arm-lying-triceps-extension"),
	app_commands.Choice(name="Cable Rope Overhead Triceps Extension", value="cable-rope-overhead-triceps-extension"),
	app_commands.Choice(name="Lever Triceps Dip", value="lever-triceps-dip"),
	app_commands.Choice(name="Lying Barbell Triceps Extension", value="lying-barbell-triceps-extension"),
	app_commands.Choice(name="Cable Tricep Kickback", value="cable-tricep-kickback"),
	app_commands.Choice(name="Triceps Dips on Floor", value="triceps-dips-on-floor"),
	app_commands.Choice(name="Dumbbell Seated Front and Back Tate Press", value="dumbbell-seated-front-and-back-tate-press"),
	app_commands.Choice(name="Kneeling Cable Triceps Extension", value="kneeling-cable-triceps-extension"),
	app_commands.Choice(name="Cable Rear Drive", value="cable-rear-drive"),
	app_commands.Choice(name="Body Ups", value="body-ups"),
	app_commands.Choice(name="Cable Lying Triceps Extensions", value="cable-lying-triceps-extensions"),
	app_commands.Choice(name="Chair Dips", value="chair-dips"),
	app_commands.Choice(name="Seated One-Arm Dumbbell Triceps Extension", value="seated-onearm-dumbbell-triceps-extension"),
	app_commands.Choice(name="Seated Dumbbell Triceps Extension", value="seated-dumbbell-triceps-extension"),
	app_commands.Choice(name="Lever Triceps Extension", value="lever-triceps-extension"),
	app_commands.Choice(name="Bench Dips on Floor", value="bench-dips-on-floor"),
	app_commands.Choice(name="Dumbbell Skull Crusher", value="dumbbell-skull-crusher"),
	app_commands.Choice(name="Dumbbell Incline Two Arm Extension", value="dumbbell-incline-two-arm-extension"),
	app_commands.Choice(name="One Arm Pronated Dumbbell Triceps Extension", value="one-arm-pronated-dumbbell-triceps-extension"),
	app_commands.Choice(name="Seated EZ-Bar Overhead Triceps Extension", value="seated-ezbar-overhead-triceps-extension"),
	app_commands.Choice(name="Cable Incline Triceps Extension", value="cable-incline-triceps-extension"),
	app_commands.Choice(name="Cable Side Triceps Extension", value="cable-side-triceps-extension"),
	app_commands.Choice(name="Incline EZ-Bar Triceps Extension", value="incline-ezbar-triceps-extension"),
	app_commands.Choice(name="High Pulley Overhead Tricep Extension", value="high-pulley-overhead-tricep-extension"),
	app_commands.Choice(name="Rope Pushdown", value="rope-pushdown"),
	app_commands.Choice(name="Reverse Grip Pushdown", value="reverse-grip-pushdown"),
	app_commands.Choice(name="Cross Arm Push-up", value="cross-arm-pushup"),
	app_commands.Choice(name="Cable Concentration Extension on Knee", value="cable-concentration-extension-on-knee"),
	app_commands.Choice(name="Cable One-Arm Overhead Triceps Extension", value="cable-onearm-overhead-triceps-extension"),
	app_commands.Choice(name="Standing Barbell Triceps Extension", value="standing-barbell-triceps-extension"),
	app_commands.Choice(name="Impossible Dips", value="impossible-dips"),
	app_commands.Choice(name="Exercise Ball Triceps Extension", value="exercise-ball-triceps-extension"),
	app_commands.Choice(name="Triceps Extension Machine", value="triceps-extension-machine"),
	app_commands.Choice(name="Triceps Dip Machine", value="triceps-dip-machine"),
	app_commands.Choice(name="Decline Close-Grip Bench To Skull Crusher", value="decline-closegrip-bench-to-skull-crusher"),
	app_commands.Choice(name="Barbell One Arm Floor Press", value="barbell-one-arm-floor-press"),
	app_commands.Choice(name="Asisted Triceps Dips", value="asisted-triceps-dips"),
	app_commands.Choice(name="Standing Triceps Stretch", value="standing-triceps-stretch"),
	app_commands.Choice(name="Low Cable Tricep Kickback", value="low-cable-tricep-kickback"),
	app_commands.Choice(name="Band Skull Crusher", value="band-skull-crusher"),
	app_commands.Choice(name="Band Pushdown", value="band-pushdown"),
	app_commands.Choice(name="Decline Dumbbell Triceps Extension", value="decline-dumbbell-triceps-extension"),
	app_commands.Choice(name="Dumbbell Tate Press", value="dumbbell-tate-press"),
	app_commands.Choice(name="Bent Over Kickback", value="bent-over-kickback"),
	app_commands.Choice(name="Dumbbell Triceps Extension", value="dumbbell-triceps-extension"),
	app_commands.Choice(name="Triceps Extension with Resistance Bands", value="triceps-extension-with-resistance-bands"),
	app_commands.Choice(name="Alternating Lying Dumbbell Triceps Extension", value="alternating-lying-dumbbell-triceps-extension"),
	app_commands.Choice(name="Barbell Reverse Grip Skullcrusher", value="barbell-reverse-grip-skullcrusher"),
	app_commands.Choice(name="Barbell Lying Back of the Head Tricep Extension", value="barbell-lying-back-of-the-head-tricep-extension"),
	app_commands.Choice(name="EZ Bar Lying Close Grip Triceps Extension Behind Head", value="ez-bar-lying-close-grip-triceps-extension-behind-head"),
	app_commands.Choice(name="One Arm High Pulley Overhead Tricep Extension", value="one-arm-high-pulley-overhead-tricep-extension"),
	app_commands.Choice(name="Cable Crossover Triceps Extension", value="cable-crossover-triceps-extension"),
	app_commands.Choice(name="Side One Arm Reverse Pushdown", value="side-one-arm-reverse-pushdown"),
	app_commands.Choice(name="Bodyweight Skull Crushers", value="bodyweight-skull-crushers"),
	app_commands.Choice(name="V-bar Pushdown", value="vbar-pushdown"),
	app_commands.Choice(name="Cable Rope Lying Tricep Extension", value="cable-rope-lying-tricep-extension"),
	app_commands.Choice(name="Cable Lying Triceps Extension", value="cable-lying-triceps-extension"),
	app_commands.Choice(name="Rear Drive With Resistance Band", value="rear-drive-with-resistance-band"),
	app_commands.Choice(name="Standing Triceps Extension | Gymstick", value="standing-triceps-extension-gymstick"),
	app_commands.Choice(name="Banded Overhead Triceps Extension", value="banded-overhead-triceps-extension"),
	app_commands.Choice(name="Overhead Triceps Extension | Gymstick", value="overhead-triceps-extension-gymstick"),
	app_commands.Choice(name="Wrist Roller", value="wrist-roller"),
	app_commands.Choice(name="Dumbbell Seated Neutral Wrist Curl", value="dumbbell-seated-neutral-wrist-curl"),
	app_commands.Choice(name="Dumbbell Wrist Curl", value="dumbbell-wrist-curl"),
	app_commands.Choice(name="Barbell Reverse Wrist Curl", value="barbell-reverse-wrist-curl"),
	app_commands.Choice(name="Wrist Circles Stretch", value="wrist-circles-stretch"),
	app_commands.Choice(name="Barbell Reverse Curl", value="barbell-reverse-curl"),
	app_commands.Choice(name="Cable One-Arm Wrist Curl On Floor", value="cable-onearm-wrist-curl-on-floor"),
	app_commands.Choice(name="Hand Gripper", value="hand-gripper"),
	app_commands.Choice(name="Behind The Back Barbell Wrist Curl", value="behind-the-back-barbell-wrist-curl"),
	app_commands.Choice(name="Wrist Ulnar Deviator And Extensor Stretch", value="wrist-ulnar-deviator-and-extensor-stretch"),
	app_commands.Choice(name="Reverse Wrist Stretch", value="reverse-wrist-stretch"),
	app_commands.Choice(name="Wrist Stretch", value="wrist-stretch"),
	app_commands.Choice(name="Weighted Neutral Wrist Curl", value="weighted-neutral-wrist-curl"),
	app_commands.Choice(name="Reverse Wrist Curl", value="reverse-wrist-curl"),
	app_commands.Choice(name="Wrist Curl", value="wrist-curl"),
	app_commands.Choice(name="Barbell Finger Curl", value="barbell-finger-curl"),
	app_commands.Choice(name="Dumbbell Finger Curl", value="dumbbell-finger-curl"),
	app_commands.Choice(name="Barbell Reverse Wrist Curl Over a Bench", value="barbell-reverse-wrist-curl-over-a-bench"),
	app_commands.Choice(name="Medicine Ball Rotational Throw", value="medicine-ball-rotational-throw"),
	app_commands.Choice(name="Dragon Flag", value="dragon-flag"),
	app_commands.Choice(name="Ab Coaster Machine", value="ab-coaster-machine"),
	app_commands.Choice(name="Cross Crunch", value="cross-crunch"),
	app_commands.Choice(name="Standing Cable Crunch", value="standing-cable-crunch"),
	app_commands.Choice(name="Seated Bench Leg Pull-in", value="seated-bench-leg-pullin"),
	app_commands.Choice(name="Cross Body Mountain Climber", value="cross-body-mountain-climber"),
	app_commands.Choice(name="Alternate Leg Raises", value="alternate-leg-raises"),
	app_commands.Choice(name="Crunches", value="crunches"),
	app_commands.Choice(name="Mountain Climber", value="mountain-climber"),
	app_commands.Choice(name="Bicycle Crunch", value="bicycle-crunch"),
	app_commands.Choice(name="Lying Scissor Kick", value="lying-scissor-kick"),
	app_commands.Choice(name="Leg Raise", value="leg-raise"),
	app_commands.Choice(name="Oblique Floor Crunches", value="oblique-floor-crunches"),
	app_commands.Choice(name="T-Cross Sit-up", value="tcross-situp"),
	app_commands.Choice(name="Dead Bug", value="dead-bug"),
	app_commands.Choice(name="Decline Sit-up", value="decline-situp"),
	app_commands.Choice(name="Reverse Crunch", value="reverse-crunch"),
	app_commands.Choice(name="Kneeling Cable Crunch", value="kneeling-cable-crunch"),
	app_commands.Choice(name="Heel Touch", value="heel-touch"),
	app_commands.Choice(name="Standing Rotation", value="standing-rotation"),
	app_commands.Choice(name="Standing Toe Touch", value="standing-toe-touch"),
	app_commands.Choice(name="Crunch With Leg Raise", value="crunch-with-leg-raise"),
	app_commands.Choice(name="Alternate Lying Floor Leg Raise", value="alternate-lying-floor-leg-raise"),
	app_commands.Choice(name="Weighted Crunch", value="weighted-crunch"),
	app_commands.Choice(name="Seated Side Crunch", value="seated-side-crunch"),
	app_commands.Choice(name="Incline Leg Hip Raise", value="incline-leg-hip-raise"),
	app_commands.Choice(name="Bodyweight Windmill", value="bodyweight-windmill"),
	app_commands.Choice(name="Front to Side Plank", value="front-to-side-plank"),
	app_commands.Choice(name="Tuck Crunch", value="tuck-crunch"),
	app_commands.Choice(name="Dumbbell Side Bend", value="dumbbell-side-bend"),
	app_commands.Choice(name="Double Leg Stretch", value="double-leg-stretch"),
	app_commands.Choice(name="Spider Plank", value="spider-plank"),
	app_commands.Choice(name="Captains Chair Leg Raise", value="captains-chair-leg-raise"),
	app_commands.Choice(name="Bench Side Bend", value="bench-side-bend"),
	app_commands.Choice(name="Crab Twist Toe Touch", value="crab-twist-toe-touch"),
	app_commands.Choice(name="Quarter Sit-up", value="quarter-situp"),
	app_commands.Choice(name="Weighted Sit-ups", value="weighted-situps"),
	app_commands.Choice(name="Lying Knee Raise", value="lying-knee-raise"),
	app_commands.Choice(name="Floor Crunch", value="floor-crunch"),
	app_commands.Choice(name="Reverse Plank", value="reverse-plank"),
	app_commands.Choice(name="Stability Ball Knee Tuck", value="stability-ball-knee-tuck"),
	app_commands.Choice(name="Hanging Knee Raises", value="hanging-knee-raises"),
	app_commands.Choice(name="Hanging Side Knee Raises", value="hanging-side-knee-raises"),
	app_commands.Choice(name="Hanging Windshield Wiper", value="hanging-windshield-wiper"),
	app_commands.Choice(name="Toes to Bar", value="toes-to-bar"),
	app_commands.Choice(name="Weighted Hanging Knee Raises", value="weighted-hanging-knee-raises"),
	app_commands.Choice(name="Teaser Pilates", value="teaser-pilates"),
	app_commands.Choice(name="Seated Oblique Twist", value="seated-oblique-twist"),
	app_commands.Choice(name="Side Bridge", value="side-bridge"),
	app_commands.Choice(name="Plank With Arm And Leg Lift", value="plank-with-arm-and-leg-lift"),
	app_commands.Choice(name="Weighted Front Plank", value="weighted-front-plank"),
	app_commands.Choice(name="Cable Side Bend", value="cable-side-bend"),
	app_commands.Choice(name="Barbell Side Bend", value="barbell-side-bend"),
	app_commands.Choice(name="Seated Barbell Twist", value="seated-barbell-twist"),
	app_commands.Choice(name="Bent Over Twist", value="bent-over-twist"),
	app_commands.Choice(name="Dumbbell V-up", value="dumbbell-vup"),
	app_commands.Choice(name="Lever Lying Crunch", value="lever-lying-crunch"),
	app_commands.Choice(name="Ab Roller Crunch", value="ab-roller-crunch"),
	app_commands.Choice(name="Standing Cable High-To-Low Twist", value="standing-cable-hightolow-twist"),
	app_commands.Choice(name="Standing Cable Low-To-High Twist", value="standing-cable-lowtohigh-twist"),
	app_commands.Choice(name="Standing Cable Twist", value="standing-cable-twist"),
	app_commands.Choice(name="L-Sit", value="lsit"),
	app_commands.Choice(name="High Knee Squat", value="high-knee-squat"),
	app_commands.Choice(name="Full Crunch Machine", value="full-crunch-machine"),
	app_commands.Choice(name="Front Plank with Arm Lift", value="front-plank-with-arm-lift"),
	app_commands.Choice(name="Ab Straps Leg Raise", value="ab-straps-leg-raise"),
	app_commands.Choice(name="Boat Pose", value="boat-pose"),
	app_commands.Choice(name="Seated Twist Machine", value="seated-twist-machine"),
	app_commands.Choice(name="Inchworm", value="inchworm"),
	app_commands.Choice(name="Front Plank With Arm And Leg Lift", value="front-plank-with-arm-and-leg-lift"),
	app_commands.Choice(name="Weighted Lying Twist", value="weighted-lying-twist"),
	app_commands.Choice(name="Swiss Ball Rollout", value="swiss-ball-rollout"),
	app_commands.Choice(name="Weighted Side Bend On Stability Ball", value="weighted-side-bend-on-stability-ball"),
	app_commands.Choice(name="Stability Ball V-Up", value="stability-ball-vup"),
	app_commands.Choice(name="Exercise Ball Frog Crunch", value="exercise-ball-frog-crunch"),
	app_commands.Choice(name="Cable Seated Cross Arm Twist", value="cable-seated-cross-arm-twist"),
	app_commands.Choice(name="Burpees", value="burpees"),
	app_commands.Choice(name="Standing Twist Machine", value="standing-twist-machine"),
	app_commands.Choice(name="Seated Crunch Machine", value="seated-crunch-machine"),
	app_commands.Choice(name="Barbell Rollout", value="barbell-rollout"),
	app_commands.Choice(name="Landmine Twist", value="landmine-twist"),
	app_commands.Choice(name="Frog Crunch", value="frog-crunch"),
	app_commands.Choice(name="Ab Wheel Rollout", value="ab-wheel-rollout"),
	app_commands.Choice(name="Bicycle Twisting Crunch", value="bicycle-twisting-crunch"),
	app_commands.Choice(name="Hands In Air Dead Bug", value="hands-in-air-dead-bug"),
	app_commands.Choice(name="4 Point Tummy Vacuum Exercise", value="4-point-tummy-vacuum-exercise"),
	app_commands.Choice(name="Seated Flutter Kick", value="seated-flutter-kick"),
	app_commands.Choice(name="Seated Cable Twist", value="seated-cable-twist"),
	app_commands.Choice(name="Bodyweight Kneeling Sissy Squat", value="bodyweight-kneeling-sissy-squat"),
	app_commands.Choice(name="Standing Barbell Rollout", value="standing-barbell-rollout"),
	app_commands.Choice(name="Side Plank Oblique Crunch", value="side-plank-oblique-crunch"),
	app_commands.Choice(name="Medicine Ball-Sit-up Throw", value="medicine-ballsitup-throw"),
	app_commands.Choice(name="Side Bent", value="side-bent"),
	app_commands.Choice(name="Leg Scissors", value="leg-scissors"),
	app_commands.Choice(name="Abdominal Bracing", value="abdominal-bracing"),
	app_commands.Choice(name="Lying Toe Touches", value="lying-toe-touches"),
	app_commands.Choice(name="Dumbbell Floor Wipers", value="dumbbell-floor-wipers"),
	app_commands.Choice(name="Side Bridge Hip Abduction", value="side-bridge-hip-abduction"),
	app_commands.Choice(name="Snap Jumps", value="snap-jumps"),
	app_commands.Choice(name="Side Plank Leg Raises", value="side-plank-leg-raises"),
	app_commands.Choice(name="Reverse Plank Kicks", value="reverse-plank-kicks"),
	app_commands.Choice(name="Bear Crawl", value="bear-crawl"),
	app_commands.Choice(name="High Knee Skips", value="high-knee-skips"),
	app_commands.Choice(name="Double Crunches", value="double-crunches"),
	app_commands.Choice(name="Toe Reaches", value="toe-reaches"),
	app_commands.Choice(name="Sit-ups", value="situps"),
	app_commands.Choice(name="Side Plank", value="side-plank"),
	app_commands.Choice(name="Plank Leg Lift", value="plank-leg-lift"),
	app_commands.Choice(name="Plank Knee to Elbow", value="plank-knee-to-elbow"),
	app_commands.Choice(name="Russian Twist", value="russian-twist"),
	app_commands.Choice(name="Plank", value="plank"),
	app_commands.Choice(name="Leg Pull-in Knee-ups", value="leg-pullin-kneeups"),
	app_commands.Choice(name="Glute Bridge", value="glute-bridge"),
	app_commands.Choice(name="Hollow Hold", value="hollow-hold"),
	app_commands.Choice(name="Long Arm Crunch", value="long-arm-crunch"),
	app_commands.Choice(name="Half Wipers", value="half-wipers"),
	app_commands.Choice(name="Jackknife Sit-ups (V-Up)", value="jackknife-situps-vup"),
	app_commands.Choice(name="Flutter Kick", value="flutter-kick"),
	app_commands.Choice(name="Suspended Ab Fall-out", value="suspended-ab-fallout"),
	app_commands.Choice(name="TRX Mountain Climber", value="trx-mountain-climber"),
	app_commands.Choice(name="Side Plank Knee to Elbow", value="side-plank-knee-to-elbow"),
	app_commands.Choice(name="Half Cross Crunch", value="half-cross-crunch"),
	app_commands.Choice(name="Cable Seated Twist on Floor", value="cable-seated-twist-on-floor"),
	app_commands.Choice(name="Butterfly Sit-up", value="butterfly-situp"),
	app_commands.Choice(name="Prone Abdominal Hollowing", value="prone-abdominal-hollowing"),
	app_commands.Choice(name="Hell Slide", value="hell-slide"),
	app_commands.Choice(name="Half Frog Pose", value="half-frog-pose"),
	app_commands.Choice(name="Medicine Ball Crunch", value="medicine-ball-crunch"),
	app_commands.Choice(name="Ball Russian Twist throw with partner", value="ball-russian-twist-throw-with-partner"),
	app_commands.Choice(name="Seated Ab Crunch Machine", value="seated-ab-crunch-machine"),
	app_commands.Choice(name="Side Lying Feet Raise", value="side-lying-feet-raise"),
	app_commands.Choice(name="Seated Twist With Resistance Band", value="seated-twist-with-resistance-band"),
	app_commands.Choice(name="Twist With Resistance Band", value="twist-with-resistance-band"),
	app_commands.Choice(name="Twist down up With Resistance Band", value="twist-down-up-with-resistance-band"),
	app_commands.Choice(name="Standing Side Bend | Gymstick", value="standing-side-bend-gymstick"),
	app_commands.Choice(name="Banded Lying leg and hip raise", value="banded-lying-leg-and-hip-raise"),
	app_commands.Choice(name="Banded Jack knife sit-up", value="banded-jack-knife-situp"),
	app_commands.Choice(name="Down to Up Twist |Gymstick", value="down-to-up-twist-gymstick"),
	app_commands.Choice(name="Bicycle Crunch | Gymstick", value="bicycle-crunch-gymstick"),
	app_commands.Choice(name="Plank Jacks / Extended Leg", value="plank-jacks-extended-leg"),
	app_commands.Choice(name="Smith Machine Squat", value="smith-machine-squat"),
	app_commands.Choice(name="Dumbbell Cossack Squat", value="dumbbell-cossack-squat"),
	app_commands.Choice(name="Dumbbell Goblet Squat", value="dumbbell-goblet-squat"),
	app_commands.Choice(name="Curtsy Lunge", value="curtsy-lunge"),
	app_commands.Choice(name="5 Dot Drills", value="5-dot-drills"),
	app_commands.Choice(name="High Knee Lunge on Bosu Ball", value="high-knee-lunge-on-bosu-ball"),
	app_commands.Choice(name="Standing Leg Circles", value="standing-leg-circles"),
	app_commands.Choice(name="Static Lunge", value="static-lunge"),
	app_commands.Choice(name="Dumbbell Walking Lunge", value="dumbbell-walking-lunge"),
	app_commands.Choice(name="Dumbbell Squat", value="dumbbell-squat"),
	app_commands.Choice(name="Depth Jump to Hurdle Hop", value="depth-jump-to-hurdle-hop"),
	app_commands.Choice(name="Power Lunge", value="power-lunge"),
	app_commands.Choice(name="Bodyweight Lunge", value="bodyweight-lunge"),
	app_commands.Choice(name="Bulgarian Split Squat Jump", value="bulgarian-split-squat-jump"),
	app_commands.Choice(name="Leg Press", value="leg-press"),
	app_commands.Choice(name="Plie Dumbbell Squat", value="plie-dumbbell-squat"),
	app_commands.Choice(name="Leg Curl", value="leg-curl"),
	app_commands.Choice(name="Seated Leg Curl", value="seated-leg-curl"),
	app_commands.Choice(name="Leg Extension", value="leg-extension"),
	app_commands.Choice(name="Barbell Hack Squats", value="barbell-hack-squats"),
	app_commands.Choice(name="Barbell Sumo Squat", value="barbell-sumo-squat"),
	app_commands.Choice(name="Dumbbell Bulgarian Split Squat", value="dumbbell-bulgarian-split-squat"),
	app_commands.Choice(name="Hack Squats Machine", value="hack-squats-machine"),
	app_commands.Choice(name="Pistol Squat", value="pistol-squat"),
	app_commands.Choice(name="Dumbbell Lunge", value="dumbbell-lunge"),
	app_commands.Choice(name="Lever Side Hip Abduction", value="lever-side-hip-abduction"),
	app_commands.Choice(name="Bodyweight Sumo Squat", value="bodyweight-sumo-squat"),
	app_commands.Choice(name="Hawaiian Squat", value="hawaiian-squat"),
	app_commands.Choice(name="Lever Standing Leg Raise", value="lever-standing-leg-raise"),
	app_commands.Choice(name="Lever Side Hip Adduction", value="lever-side-hip-adduction"),
	app_commands.Choice(name="Barbell Bulgarian Split Squat", value="barbell-bulgarian-split-squat"),
	app_commands.Choice(name="Lever Deadlift", value="lever-deadlift"),
	app_commands.Choice(name="Dumbbell Rear Lunge", value="dumbbell-rear-lunge"),
	app_commands.Choice(name="Barbell Lunge", value="barbell-lunge"),
	app_commands.Choice(name="Barbell Lateral Lunge", value="barbell-lateral-lunge"),
	app_commands.Choice(name="Side Lunge", value="side-lunge"),
	app_commands.Choice(name="Cable Hip Adduction", value="cable-hip-adduction"),
	app_commands.Choice(name="Zig Zag Hops Plyometric", value="zig-zag-hops-plyometric"),
	app_commands.Choice(name="Bodyweight Squat", value="bodyweight-squat"),
	app_commands.Choice(name="Upavistha Konasana", value="upavistha-konasana"),
	app_commands.Choice(name="Kneeling Quad Stretch", value="kneeling-quad-stretch"),
	app_commands.Choice(name="Lateral Speed Step", value="lateral-speed-step"),
	app_commands.Choice(name="Seated Groin / Adductor Stretch", value="seated-groin-adductor-stretch"),
	app_commands.Choice(name="Reverse Lunge Knee Lift", value="reverse-lunge-knee-lift"),
	app_commands.Choice(name="Lying Hamstring Stretch", value="lying-hamstring-stretch"),
	app_commands.Choice(name="Curtsy Squat", value="curtsy-squat"),
	app_commands.Choice(name="Cable Goblet Squat", value="cable-goblet-squat"),
	app_commands.Choice(name="Thigh fly (Adductor Magnus Stretch)", value="thigh-fly-adductor-magnus-stretch"),
	app_commands.Choice(name="Split Jump Squat", value="split-jump-squat"),
	app_commands.Choice(name="Cossack Squat", value="cossack-squat"),
	app_commands.Choice(name="Standing Cross Leg Hamstring Stretch", value="standing-cross-leg-hamstring-stretch"),
	app_commands.Choice(name="Backward Jump", value="backward-jump"),
	app_commands.Choice(name="Jumping jack", value="jumping-jack"),
	app_commands.Choice(name="Single Leg Broad Jump", value="single-leg-broad-jump"),
	app_commands.Choice(name="Jump Squats", value="jump-squats"),
	app_commands.Choice(name="Dumbbell Lateral Step Up", value="dumbbell-lateral-step-up"),
	app_commands.Choice(name="Lateral Step-up", value="lateral-stepup"),
	app_commands.Choice(name="Step Up + Opposite Elbow to Knee Twist", value="step-up-opposite-elbow-to-knee-twist"),
	app_commands.Choice(name="Barbell Step-Up", value="barbell-stepup"),
	app_commands.Choice(name="Lying Glute Stretch", value="lying-glute-stretch"),
	app_commands.Choice(name="Lying Dumbbell Leg Curl", value="lying-dumbbell-leg-curl"),
	app_commands.Choice(name="Bodyweight Walking Lunge", value="bodyweight-walking-lunge"),
	app_commands.Choice(name="Wall Sit", value="wall-sit"),
	app_commands.Choice(name="Kettlebell Pistol Squats", value="kettlebell-pistol-squats"),
	app_commands.Choice(name="Bodyweight Box Squat", value="bodyweight-box-squat"),
	app_commands.Choice(name="Step Up Single Leg Balance with Bicep Curl", value="step-up-single-leg-balance-with-bicep-curl"),
	app_commands.Choice(name="Dumbbell Step-Up", value="dumbbell-stepup"),
	app_commands.Choice(name="Belt Squat", value="belt-squat"),
	app_commands.Choice(name="Lever Single Leg Curl", value="lever-single-leg-curl"),
	app_commands.Choice(name="Reverse Lunge", value="reverse-lunge"),
	app_commands.Choice(name="Single Leg Step Down", value="single-leg-step-down"),
	app_commands.Choice(name="Long Jump", value="long-jump"),
	app_commands.Choice(name="Lever Assisted Single Leg Press", value="lever-assisted-single-leg-press"),
	app_commands.Choice(name="Nordic Hamstring Curl", value="nordic-hamstring-curl"),
	app_commands.Choice(name="Horizontal Leg Press", value="horizontal-leg-press"),
	app_commands.Choice(name="Resistance Band Toe Touch", value="resistance-band-toe-touch"),
	app_commands.Choice(name="Kneeling Hip Flexor Stretch", value="kneeling-hip-flexor-stretch"),
	app_commands.Choice(name="Standing Quadriceps Stretch", value="standing-quadriceps-stretch"),
	app_commands.Choice(name="Exercise Ball Wall Squat", value="exercise-ball-wall-squat"),
	app_commands.Choice(name="Leg Curl On Stability Ball", value="leg-curl-on-stability-ball"),
	app_commands.Choice(name="Kettlebell Goblet Squat", value="kettlebell-goblet-squat"),
	app_commands.Choice(name="Barbell Bench Front Squat", value="barbell-bench-front-squat"),
	app_commands.Choice(name="Standing Side Toe Touching", value="standing-side-toe-touching"),
	app_commands.Choice(name="Dumbbell Split Jump", value="dumbbell-split-jump"),
	app_commands.Choice(name="Banded Step-up", value="banded-stepup"),
	app_commands.Choice(name="Barbell Curtsey Lunge", value="barbell-curtsey-lunge"),
	app_commands.Choice(name="Dumbbell Jump Squat", value="dumbbell-jump-squat"),
	app_commands.Choice(name="Barbell Split Squat", value="barbell-split-squat"),
	app_commands.Choice(name="All Fours Squad Stretch", value="all-fours-squad-stretch"),
	app_commands.Choice(name="Lever Kneeling Leg Curl", value="lever-kneeling-leg-curl"),
	app_commands.Choice(name="Reverse Hack Squat", value="reverse-hack-squat"),
	app_commands.Choice(name="Duck Walk", value="duck-walk"),
	app_commands.Choice(name="Trap Bar Deadlift", value="trap-bar-deadlift"),
	app_commands.Choice(name="Zercher Squat", value="zercher-squat"),
	app_commands.Choice(name="Front Squat", value="front-squat"),
	app_commands.Choice(name="Standing Hamstring Stretch", value="standing-hamstring-stretch"),
	app_commands.Choice(name="Single Leg Press", value="single-leg-press"),
	app_commands.Choice(name="Landmine Lunge", value="landmine-lunge"),
	app_commands.Choice(name="Single Leg Extension", value="single-leg-extension"),
	app_commands.Choice(name="Smith Machine Leg Press", value="smith-machine-leg-press"),
	app_commands.Choice(name="Smith Machine Lunge", value="smith-machine-lunge"),
	app_commands.Choice(name="Skater Squat", value="skater-squat"),
	app_commands.Choice(name="Shrimp Squat", value="shrimp-squat"),
	app_commands.Choice(name="Towel Leg Curl", value="towel-leg-curl"),
	app_commands.Choice(name="Foam Roller IT (iliotibial Band) Stretch", value="foam-roller-it-iliotibial-band-stretch"),
	app_commands.Choice(name="Foam Roller Quads", value="foam-roller-quads"),
	app_commands.Choice(name="Foam Roller Inner Thigh Adductor Stretch", value="foam-roller-inner-thigh-adductor-stretch"),
	app_commands.Choice(name="Foam Roller Hamstrings", value="foam-roller-hamstrings"),
	app_commands.Choice(name="Foam Roller Plantar Fasciitis", value="foam-roller-plantar-fasciitis"),
	app_commands.Choice(name="90/90 Hip Stretch", value="9090-hip-stretch"),
	app_commands.Choice(name="Dumbbell Goblet Curtsey Lunge", value="dumbbell-goblet-curtsey-lunge"),
	app_commands.Choice(name="Cable Forward Lunge", value="cable-forward-lunge"),
	app_commands.Choice(name="Cable Lunge", value="cable-lunge"),
	app_commands.Choice(name="Cable Front Squat", value="cable-front-squat"),
	app_commands.Choice(name="Trap Bar Jump Squat", value="trap-bar-jump-squat"),
	app_commands.Choice(name="Box Jump to Pistol Squat", value="box-jump-to-pistol-squat"),
	app_commands.Choice(name="Box Jump 2 to 1", value="box-jump-2-to-1"),
	app_commands.Choice(name="Box Jump 1 to 2", value="box-jump-1-to-2"),
	app_commands.Choice(name="Single Leg Box Jump", value="single-leg-box-jump"),
	app_commands.Choice(name="Seated Straight Leg Calf Stretch", value="seated-straight-leg-calf-stretch"),
	app_commands.Choice(name="Crouching Heel Back Calf Stretch", value="crouching-heel-back-calf-stretch"),
	app_commands.Choice(name="Barbell Jump Squat", value="barbell-jump-squat"),
	app_commands.Choice(name="Frog Pose", value="frog-pose"),
	app_commands.Choice(name="ATG Split Squat", value="atg-split-squat"),
	app_commands.Choice(name="Seated Piriformis Stretch", value="seated-piriformis-stretch"),
	app_commands.Choice(name="Barbell Pin Front Squat", value="barbell-pin-front-squat"),
	app_commands.Choice(name="Heel Touch Side Kick Squat", value="heel-touch-side-kick-squat"),
	app_commands.Choice(name="Decline Bench Dumbbell Lunge", value="decline-bench-dumbbell-lunge"),
	app_commands.Choice(name="Lateral Leg Swings", value="lateral-leg-swings"),
	app_commands.Choice(name="Banded Walk", value="banded-walk"),
	app_commands.Choice(name="Resistance Band Lateral Walk", value="resistance-band-lateral-walk"),
	app_commands.Choice(name="Kneeling Jump Squat", value="kneeling-jump-squat"),
	app_commands.Choice(name="Banded Split Squat", value="banded-split-squat"),
	app_commands.Choice(name="Banded Kettlebell Goblet Squat", value="banded-kettlebell-goblet-squat"),
	app_commands.Choice(name="Banded Lunge", value="banded-lunge"),
	app_commands.Choice(name="Banded Leg Curl", value="banded-leg-curl"),
	app_commands.Choice(name="Standing Single Leg Curl Machine", value="standing-single-leg-curl-machine"),
	app_commands.Choice(name="Decline Dumbbell Leg Curl", value="decline-dumbbell-leg-curl"),
	app_commands.Choice(name="Kettlebell Front Squat", value="kettlebell-front-squat"),
	app_commands.Choice(name="Single Knee To Chest", value="single-knee-to-chest"),
	app_commands.Choice(name="Pistol Squat to Box", value="pistol-squat-to-box"),
	app_commands.Choice(name="Landmine Deadlift", value="landmine-deadlift"),
	app_commands.Choice(name="Landmine Squat", value="landmine-squat"),
	app_commands.Choice(name="Sissy Squat", value="sissy-squat"),
	app_commands.Choice(name="Rack Pull", value="rack-pull"),
	app_commands.Choice(name="Standing Knee Hugs", value="standing-knee-hugs"),
	app_commands.Choice(name="Step Up with Knee Raises", value="step-up-with-knee-raises"),
	app_commands.Choice(name="Piriformis Stretch", value="piriformis-stretch"),
	app_commands.Choice(name="Half Kneeling Hip Flexor Stretch", value="half-kneeling-hip-flexor-stretch"),
	app_commands.Choice(name="High Knee Run", value="high-knee-run"),
	app_commands.Choice(name="Inner Thigh Side Stretch", value="inner-thigh-side-stretch"),
	app_commands.Choice(name="Skater", value="skater"),
	app_commands.Choice(name="Butterfly Stretch", value="butterfly-stretch"),
	app_commands.Choice(name="Dumbbell Forward Leaning Lunge", value="dumbbell-forward-leaning-lunge"),
	app_commands.Choice(name="Dumbbell Reverse Lunge", value="dumbbell-reverse-lunge"),
	app_commands.Choice(name="Dumbbell Pistol Squat", value="dumbbell-pistol-squat"),
	app_commands.Choice(name="Bodyweight Bulgarian Split Squat", value="bodyweight-bulgarian-split-squat"),
	app_commands.Choice(name="Dumbbell Sumo Squat", value="dumbbell-sumo-squat"),
	app_commands.Choice(name="Hip Adduction Machine", value="hip-adduction-machine"),
	app_commands.Choice(name="Hip Abduction Machine", value="hip-abduction-machine"),
	app_commands.Choice(name="Seated Banded Leg Extension", value="seated-banded-leg-extension"),
	app_commands.Choice(name="Zercher Deadlift", value="zercher-deadlift"),
	app_commands.Choice(name="Supported Pistol Squat", value="supported-pistol-squat"),
	app_commands.Choice(name="Jefferson Squat", value="jefferson-squat"),
	app_commands.Choice(name="TRX Pistol Squat", value="trx-pistol-squat"),
	app_commands.Choice(name="Sitting Wide Leg Adductor Stretch", value="sitting-wide-leg-adductor-stretch"),
	app_commands.Choice(name="Standing Wide Knees Adductor Stretch", value="standing-wide-knees-adductor-stretch"),
	app_commands.Choice(name="Standing Wide Leg Adductor Stretch", value="standing-wide-leg-adductor-stretch"),
	app_commands.Choice(name="Knee Circles", value="knee-circles"),
	app_commands.Choice(name="Resistance Band Overhead Squat", value="resistance-band-overhead-squat"),
	app_commands.Choice(name="Kneeling Leg Out Adductor Stretch", value="kneeling-leg-out-adductor-stretch"),
	app_commands.Choice(name="Happy Baby Pose", value="happy-baby-pose"),
	app_commands.Choice(name="Seated Leg Extension with Resistance Band", value="seated-leg-extension-with-resistance-band"),
	app_commands.Choice(name="Dumbbell Bench Squat", value="dumbbell-bench-squat"),
	app_commands.Choice(name="Pendulum Squat", value="pendulum-squat"),
	app_commands.Choice(name="Box Pistol Squat", value="box-pistol-squat"),
	app_commands.Choice(name="Sitting Rotation Hip Stretch", value="sitting-rotation-hip-stretch"),
	app_commands.Choice(name="Supported One Leg Standing Hip Flexor And Knee Extensor Stretch", value="supported-one-leg-standing-hip-flexor-and-knee-extensor-stretch"),
	app_commands.Choice(name="Squat mobility Complex", value="squat-mobility-complex"),
	app_commands.Choice(name="Standing Straight Leg Raise With Resistance Band", value="standing-straight-leg-raise-with-resistance-band"),
	app_commands.Choice(name="Standing Leg Raise With Resistance Band", value="standing-leg-raise-with-resistance-band"),
	app_commands.Choice(name="Standing Leg Extension With Resistance Band", value="standing-leg-extension-with-resistance-band"),
	app_commands.Choice(name="Standing Leg Curl With Resistance Band", value="standing-leg-curl-with-resistance-band"),
	app_commands.Choice(name="Split Squat | Gymstick", value="split-squat-gymstick"),
	app_commands.Choice(name="Squat | Gymstick", value="squat-gymstick"),
	app_commands.Choice(name="Banded Lying Leg Curl", value="banded-lying-leg-curl"),
	app_commands.Choice(name="Lying Alternate Leg Press | Gymstick", value="lying-alternate-leg-press-gymstick"),
	app_commands.Choice(name="Pin Squat", value="pin-squat"),
	app_commands.Choice(name="The Box Jump", value="the-box-jump"),
	app_commands.Choice(name="Standing Calf Raise", value="standing-calf-raise"),
	app_commands.Choice(name="Calf Raise", value="calf-raise"),
	app_commands.Choice(name="Calf Raise with Resistance Band", value="calf-raise-with-resistance-band"),
	app_commands.Choice(name="Barbell Seated Calf Raise", value="barbell-seated-calf-raise"),
	app_commands.Choice(name="Leg Press Calf Raise", value="leg-press-calf-raise"),
	app_commands.Choice(name="Hack Squat Calf Raise", value="hack-squat-calf-raise"),
	app_commands.Choice(name="Lever Seated Calf Raise", value="lever-seated-calf-raise"),
	app_commands.Choice(name="Single Leg Calf Raise", value="single-leg-calf-raise"),
	app_commands.Choice(name="Hack Machine One-Leg Calf Raise", value="hack-machine-oneleg-calf-raise"),
	app_commands.Choice(name="Donkey Calf Raise", value="donkey-calf-raise"),
	app_commands.Choice(name="Lever Donkey Calf Raise", value="lever-donkey-calf-raise"),
	app_commands.Choice(name="Bench Press Machine Standing Calf Raise", value="bench-press-machine-standing-calf-raise"),
	app_commands.Choice(name="Standing Barbell Calf Raise", value="standing-barbell-calf-raise"),
	app_commands.Choice(name="Weighted Donkey Calf Raise", value="weighted-donkey-calf-raise"),
	app_commands.Choice(name="Squat Hold Calf Raise", value="squat-hold-calf-raise"),
	app_commands.Choice(name="Weighted Seated Calf Raise", value="weighted-seated-calf-raise"),
	app_commands.Choice(name="Foam Roller Calves", value="foam-roller-calves"),
	app_commands.Choice(name="Band Foot External Rotation", value="band-foot-external-rotation"),
	app_commands.Choice(name="Toe Extensor Stretch", value="toe-extensor-stretch"),
	app_commands.Choice(name="Standing Dorsiflexion", value="standing-dorsiflexion"),
	app_commands.Choice(name="Standing Wall Calf Stretch", value="standing-wall-calf-stretch"),
	app_commands.Choice(name="Standing Toe Up Achilles Stretch", value="standing-toe-up-achilles-stretch"),
	app_commands.Choice(name="Standing Toe Flexor Stretch", value="standing-toe-flexor-stretch"),
	app_commands.Choice(name="Standing Gastrocnemius Calf Stretch", value="standing-gastrocnemius-calf-stretch"),
	app_commands.Choice(name="Single Heel Drop Calf Stretch", value="single-heel-drop-calf-stretch"),
	app_commands.Choice(name="Lunging Straight Leg Calf Stretch", value="lunging-straight-leg-calf-stretch"),
	app_commands.Choice(name="Posterior Tibialis Stretch", value="posterior-tibialis-stretch"),
	app_commands.Choice(name="Foot and Ankles Stretches", value="foot-and-ankles-stretches"),
	app_commands.Choice(name="Foot and Ankle Rotation", value="foot-and-ankle-rotation"),
	app_commands.Choice(name="Calves Stretch Static Position", value="calves-stretch-static-position"),
	app_commands.Choice(name="Single Leg Calves Stretch", value="single-leg-calves-stretch"),
	app_commands.Choice(name="Calf Stretch With Rope", value="calf-stretch-with-rope"),
	app_commands.Choice(name="Seated Calf Press on Leg Press Machine", value="seated-calf-press-on-leg-press-machine"),
	app_commands.Choice(name="Single Calf Raise on Leg Press Machine", value="single-calf-raise-on-leg-press-machine"),
	app_commands.Choice(name="Single Leg Donkey Calf Raise", value="single-leg-donkey-calf-raise"),
	app_commands.Choice(name="Barbell Glute Bridge Two Legs on Bench", value="barbell-glute-bridge-two-legs-on-bench"),
	app_commands.Choice(name="Barbell Hip Thrusts", value="barbell-hip-thrusts"),
	app_commands.Choice(name="Smith Machine Reverse Kickback", value="smith-machine-reverse-kickback"),
	app_commands.Choice(name="Lever Standing Rear Kick", value="lever-standing-rear-kick"),
	app_commands.Choice(name="Standing Hip Abduction", value="standing-hip-abduction"),
	app_commands.Choice(name="Side Lying Clam", value="side-lying-clam"),
	app_commands.Choice(name="Cable Donkey Kickback", value="cable-donkey-kickback"),
	app_commands.Choice(name="Bridge Hip Abduction", value="bridge-hip-abduction"),
	app_commands.Choice(name="Glute Kickback Machine", value="glute-kickback-machine"),
	app_commands.Choice(name="Standing Hip Extension", value="standing-hip-extension"),
	app_commands.Choice(name="Bench Glute Flutter Kicks", value="bench-glute-flutter-kicks"),
	app_commands.Choice(name="Bodyweight Hip Thrust", value="bodyweight-hip-thrust"),
	app_commands.Choice(name="Single Leg Bridge", value="single-leg-bridge"),
	app_commands.Choice(name="Bodyweight Single Leg Deadlift", value="bodyweight-single-leg-deadlift"),
	app_commands.Choice(name="Dumbbell Glute Bridge", value="dumbbell-glute-bridge"),
	app_commands.Choice(name="Resistance Band Reverse Hyperextension", value="resistance-band-reverse-hyperextension"),
	app_commands.Choice(name="Band Lying Hip External Rotation", value="band-lying-hip-external-rotation"),
	app_commands.Choice(name="Single Leg Hip Thrust Jump", value="single-leg-hip-thrust-jump"),
	app_commands.Choice(name="Foam Roller Glutes", value="foam-roller-glutes"),
	app_commands.Choice(name="Kneeling Cable Pull Through", value="kneeling-cable-pull-through"),
	app_commands.Choice(name="Hip Extension On Bench", value="hip-extension-on-bench"),
	app_commands.Choice(name="Donkey Kick on Smith Machine", value="donkey-kick-on-smith-machine"),
	app_commands.Choice(name="Glute Bridge on Bench", value="glute-bridge-on-bench"),
	app_commands.Choice(name="Donkey Kick on Leg Extension Machine", value="donkey-kick-on-leg-extension-machine"),
	app_commands.Choice(name="Hip Thrust on The Leg Extension Machine", value="hip-thrust-on-the-leg-extension-machine"),
	app_commands.Choice(name="Hip Thrust Machine", value="hip-thrust-machine"),
	app_commands.Choice(name="Squat on The Abductor Machine", value="squat-on-the-abductor-machine"),
	app_commands.Choice(name="Barbell Single Leg Hip Thrust", value="barbell-single-leg-hip-thrust"),
	app_commands.Choice(name="Pelvic Tilt", value="pelvic-tilt"),
	app_commands.Choice(name="Glute Bridge One Leg on Bench", value="glute-bridge-one-leg-on-bench"),
	app_commands.Choice(name="Unilateral Bridge", value="unilateral-bridge"),
	app_commands.Choice(name="Straight Leg Kickback", value="straight-leg-kickback"),
	app_commands.Choice(name="Banded Standing Glute Kickback", value="banded-standing-glute-kickback"),
	app_commands.Choice(name="Banded Seated Hip Abduction", value="banded-seated-hip-abduction"),
	app_commands.Choice(name="Banded Single Leg Glute Bridge", value="banded-single-leg-glute-bridge"),
	app_commands.Choice(name="Banded Glute Bridge", value="banded-glute-bridge"),
	app_commands.Choice(name="Band Side Lying Clam", value="band-side-lying-clam"),
	app_commands.Choice(name="Banded Glute Kickbacks", value="banded-glute-kickbacks"),
	app_commands.Choice(name="Banded Donkey Kicks", value="banded-donkey-kicks"),
	app_commands.Choice(name="Banded Thigh Fly", value="banded-thigh-fly"),
	app_commands.Choice(name="Band Side Lying Leg Lift", value="band-side-lying-leg-lift"),
	app_commands.Choice(name="Banded Fire Hydrant", value="banded-fire-hydrant"),
	app_commands.Choice(name="Frog Pump", value="frog-pump"),
	app_commands.Choice(name="Band Seated Hip External Rotation", value="band-seated-hip-external-rotation"),
	app_commands.Choice(name="Band Seated Hip Internal Rotation", value="band-seated-hip-internal-rotation"),
	app_commands.Choice(name="Fire Hydrant", value="fire-hydrant"),
	app_commands.Choice(name="Barbell Glute Bridge", value="barbell-glute-bridge"),
	app_commands.Choice(name="Cable Hip Extension", value="cable-hip-extension"),
	app_commands.Choice(name="Cable Hip Abduction", value="cable-hip-abduction"),
	app_commands.Choice(name="Donkey Kicks", value="donkey-kicks"),
	app_commands.Choice(name="Hip Circles", value="hip-circles"),
	app_commands.Choice(name="Lever Standing Hip Extension", value="lever-standing-hip-extension"),
	app_commands.Choice(name="Kicks Leg Bent", value="kicks-leg-bent"),
	app_commands.Choice(name="Smith Machine Hip Thrust", value="smith-machine-hip-thrust"),
	app_commands.Choice(name="Resistance Band Hip Thrust", value="resistance-band-hip-thrust"),
	app_commands.Choice(name="Resistance Band Hip Thrusts on Knees", value="resistance-band-hip-thrusts-on-knees"),
	app_commands.Choice(name="Side Lying Hip Adduction", value="side-lying-hip-adduction"),
	app_commands.Choice(name="Side Hip Abduction", value="side-hip-abduction"),
	app_commands.Choice(name="Single Stiff Leg Deadlift With Resistance Band", value="single-stiff-leg-deadlift-with-resistance-band"),
	app_commands.Choice(name="Pull through With Resistance Band", value="pull-through-with-resistance-band"),
	app_commands.Choice(name="Kneeling Single Leg Kick | Gymstick", value="kneeling-single-leg-kick-gymstick"),
	app_commands.Choice(name="Navy Seal Burpee", value="navy-seal-burpee"),
	app_commands.Choice(name="Shadow Boxing", value="shadow-boxing"),
	app_commands.Choice(name="Riding Outdoor Bicycle", value="riding-outdoor-bicycle"),
	app_commands.Choice(name="Walking", value="walking"),
	app_commands.Choice(name="Briskly Walking", value="briskly-walking"),
	app_commands.Choice(name="Running", value="running"),
	app_commands.Choice(name="Sprint", value="sprint"),
	app_commands.Choice(name="Walk Wave Machine", value="walk-wave-machine"),
	app_commands.Choice(name="Jump Rope", value="jump-rope"),
	app_commands.Choice(name="Bike", value="bike"),
	app_commands.Choice(name="Treadmill", value="treadmill"),
	app_commands.Choice(name="Incline Treadmill", value="incline-treadmill"),
	app_commands.Choice(name="Manual Treadmill", value="manual-treadmill"),
	app_commands.Choice(name="Elliptical Machine", value="elliptical-machine"),
	app_commands.Choice(name="Stair Climber Machine", value="stair-climber-machine"),
	app_commands.Choice(name="Elbow To Knee Twists", value="elbow-to-knee-twists"),
	app_commands.Choice(name="Push-up Toe Touch", value="pushup-toe-touch"),
	app_commands.Choice(name="Power Skips", value="power-skips"),
	app_commands.Choice(name="Plyo Jacks", value="plyo-jacks"),
	app_commands.Choice(name="Split Jacks", value="split-jacks"),
	app_commands.Choice(name="Butt Kicks", value="butt-kicks"),
	app_commands.Choice(name="Fast Feet Run", value="fast-feet-run"),
	app_commands.Choice(name="Wheel Run", value="wheel-run"),
	app_commands.Choice(name="Run in Place", value="run-in-place"),
	app_commands.Choice(name="Short Stride Run", value="short-stride-run"),
	app_commands.Choice(name="Band Assisted Sprinter Run", value="band-assisted-sprinter-run"),
	app_commands.Choice(name="Backward Running", value="backward-running"),
	app_commands.Choice(name="Side Shuttle", value="side-shuttle"),
	app_commands.Choice(name="Tuck Jump", value="tuck-jump"),
	app_commands.Choice(name="Boxer Shuffle Cardio", value="boxer-shuffle-cardio"),
	app_commands.Choice(name="Jab Boxing", value="jab-boxing"),
	app_commands.Choice(name="Punches", value="punches"),
	app_commands.Choice(name="Right Uppercut", value="right-uppercut"),
	app_commands.Choice(name="Right Cross", value="right-cross"),
	app_commands.Choice(name="Hook Kick", value="hook-kick"),
	app_commands.Choice(name="Boxing Right Cross", value="boxing-right-cross"),
	app_commands.Choice(name="Walking High Knee Lunges", value="walking-high-knee-lunges"),
	app_commands.Choice(name="High Knees Lift Run", value="high-knees-lift-run"),
	app_commands.Choice(name="Jack Burpees", value="jack-burpees"),
	app_commands.Choice(name="Astride Jumps", value="astride-jumps"),
	app_commands.Choice(name="Dumbbell Burpees", value="dumbbell-burpees"),
	app_commands.Choice(name="Ski Step", value="ski-step"),
	app_commands.Choice(name="Vibration Plate", value="vibration-plate"),
	app_commands.Choice(name="High Knees Against Wall", value="high-knees-against-wall"),
	app_commands.Choice(name="Vertical Mountain Climber", value="vertical-mountain-climber"),
	app_commands.Choice(name="Cross Body Push-up", value="cross-body-pushup"),
	app_commands.Choice(name="Stationary Bike Run", value="stationary-bike-run"),
	app_commands.Choice(name="Hands Bike", value="hands-bike"),
	app_commands.Choice(name="Squat Tuck Jump", value="squat-tuck-jump"),
	app_commands.Choice(name="1-2 Stick Drill", value="12-stick-drill"),
	app_commands.Choice(name="Assault AirBike", value="assault-airbike"),
	app_commands.Choice(name="Recumbent Exercise Bike", value="recumbent-exercise-bike"),
	app_commands.Choice(name="Backward Medicine Ball Throw", value="backward-medicine-ball-throw"),
	app_commands.Choice(name="Zercher Carry", value="zercher-carry"),
	app_commands.Choice(name="Wall Walk", value="wall-walk"),
	app_commands.Choice(name="Kettlebell Hang Clean", value="kettlebell-hang-clean"),
	app_commands.Choice(name="Dumbbell Power Clean", value="dumbbell-power-clean"),
	app_commands.Choice(name="Dumbbell Devil Press", value="dumbbell-devil-press"),
	app_commands.Choice(name="Overhead Squat", value="overhead-squat"),
	app_commands.Choice(name="Ski Ergometer", value="ski-ergometer"),
	app_commands.Choice(name="Human Flag", value="human-flag"),
	app_commands.Choice(name="Farmer's Walk", value="farmers-walk"),
	app_commands.Choice(name="Log Lift", value="log-lift"),
	app_commands.Choice(name="Tire Sledge Hammer", value="tire-sledge-hammer"),
	app_commands.Choice(name="Tire Flip", value="tire-flip"),
	app_commands.Choice(name="Barbell Snatch", value="barbell-snatch"),
	app_commands.Choice(name="Power Snatch", value="power-snatch"),
	app_commands.Choice(name="Muscle Snatch", value="muscle-snatch"),
	app_commands.Choice(name="Heaving Snatch Balance", value="heaving-snatch-balance"),
	app_commands.Choice(name="Barbell Hang Clean", value="barbell-hang-clean"),
	app_commands.Choice(name="Power Clean", value="power-clean"),
	app_commands.Choice(name="Turkish Get-up", value="turkish-getup"),
	app_commands.Choice(name="Handstand Walk", value="handstand-walk"),
	app_commands.Choice(name="Handstand", value="handstand"),
]

EXERCISE_META = {
	"weighted-lateral-neck-flexion": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Lying-Weighted-Lateral-Neck-Flexion.gif",
		"pretty-name": "Weighted Lateral Neck Flexion",
	},
	"weighted-lying-neck-extension-neck-harness": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Weighted-Lying-Neck-Extension.gif",
		"pretty-name": "Weighted Lying Neck Extension (Neck Harness)",
	},
	"weighted-lying-neck-flexion-neck-harness": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Weighted-Lying-Neck-Flexion.gif",
		"pretty-name": "Weighted Lying Neck Flexion (Neck Harness)",
	},
	"gittleson-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Dumbbell-Seated-Gittleson-Shrug.gif",
		"pretty-name": "Gittleson Shrug",
	},
	"diagonal-neck-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/07/Diagonal-Neck-Stretch-360x360.png",
		"pretty-name": "Diagonal Neck Stretch",
	},
	"neck-rotation-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/07/Rotating-Neck-Stretch.gif",
		"pretty-name": "Neck Rotation Stretch",
	},
	"neck-flexion-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/07/Neck-Flexion-Stretch-360x360.png",
		"pretty-name": "Neck Flexion Stretch",
	},
	"neck-extension-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/07/Neck-Extension-Stretching-360x360.png",
		"pretty-name": "Neck Extension Stretch",
	},
	"side-neck-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Side-Neck-Stretch.gif",
		"pretty-name": "Side Neck Stretch",
	},
	"side-push-neck-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Side-Push-Neck-Stretch.gif",
		"pretty-name": "Side Push Neck Stretch",
	},
	"front-and-back-neck-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Front-and-Back-Neck-Stretch.gif",
		"pretty-name": "Front and Back Neck Stretch",
	},
	"chin-tuck": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Chin-Tuck.gif",
		"pretty-name": "Chin Tuck",
	},
	"prone-cervical-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Prone-Cervical-Extension.gif",
		"pretty-name": "Prone Cervical Extension",
	},
	"kneeling-neck-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Kneeling-Neck-Stretch.gif",
		"pretty-name": "Kneeling Neck Stretch",
	},
	"weighted-neck-harness-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Weighted-Neck-Harness-Extension.gif",
		"pretty-name": "Weighted Neck Harness Extension",
	},
	"lying-weighted-neck-flexion": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Lying-Weighted-Neck-Flexion.gif",
		"pretty-name": "Lying Weighted Neck Flexion",
	},
	"lying-weighted-neck-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Lying-Weighted-Neck-Extension.gif",
		"pretty-name": "Lying Weighted Neck Extension",
	},
	"lever-neck-right-side-flexion-plate-loaded": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Lever-Neck-Right-Side-Flexion-plate-loaded.gif",
		"pretty-name": "Lever Neck Right Side Flexion (plate loaded)",
	},
	"lever-neck-extension-plate-loaded": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Lever-Neck-Extension-plate-loaded.gif",
		"pretty-name": "Lever Neck Extension (plate loaded)",
	},
	"cable-seated-neck-flexion-with-head-harness": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Seated-Neck-Flexion-with-head-harness.gif",
		"pretty-name": "Cable Seated Neck Flexion with head harness",
	},
	"cable-seated-neck-extension-with-head-harness": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Seated-Neck-Extension-with-head-harness.gif",
		"pretty-name": "Cable Seated Neck Extension with head harness",
	},
	"sphinx-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Sphinx-Stretch.gif",
		"pretty-name": "Sphinx Stretch",
	},
	"floor-hyperextension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Floor-Hyperextension-1.gif",
		"pretty-name": "Floor Hyperextension",
	},
	"bhujangasana-cobra-abdominal-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/abdominal-stretch.gif",
		"pretty-name": "Bhujangasana | Cobra Abdominal Stretch",
	},
	"fish-pose": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Fish-Pose-Matsyasana.gif",
		"pretty-name": "Fish Pose",
	},
	"superman": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Superman-exercise.gif",
		"pretty-name": "Superman",
	},
	"overhead-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/overhead-shrug.gif",
		"pretty-name": "Overhead Shrug",
	},
	"45-degree-incline-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/45-Degree-Incline-Row.gif",
		"pretty-name": "45 Degree Incline Row",
	},
	"dumbbell-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Dumbbell-Shrug.gif",
		"pretty-name": "Dumbbell Shrug",
	},
	"cable-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Cable-Shrug.gif",
		"pretty-name": "Cable Shrug",
	},
	"barbell-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Shrug.gif",
		"pretty-name": "Barbell Shrug",
	},
	"behind-the-back-barbell-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/03/Behind-The-Back-Barbell-Shrug-Reverse-Barbell-Shrug.gif",
		"pretty-name": "Behind The Back Barbell Shrug",
	},
	"dumbbell-incline-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Dumbbell-Incline-Shrug.gif",
		"pretty-name": "Dumbbell Incline Shrug",
	},
	"prone-incline-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Dumbbell-Decline-Shrug.gif",
		"pretty-name": "Prone Incline Shrug",
	},
	"lever-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Lever-Shrug.gif",
		"pretty-name": "Lever Shrug",
	},
	"rear-delt-fly-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Rear-Delt-Machine-Flys.gif",
		"pretty-name": "Rear Delt Fly Machine",
	},
	"lever-gripless-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Lever-Gripless-Shrug.gif",
		"pretty-name": "Lever Gripless Shrug",
	},
	"cable-rear-delt-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/cable-rear-delt-fly.gif",
		"pretty-name": "Cable Rear Delt Fly",
	},
	"bent-over-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bent-Over-Lateral-Raise.gif",
		"pretty-name": "Bent Over Lateral Raise",
	},
	"cable-upright-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Cable-Upright-Row.gif",
		"pretty-name": "Cable Upright Row",
	},
	"face-pull": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Face-Pull.gif",
		"pretty-name": "Face Pull",
	},
	"half-kneeling-high-cable-row-rope": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Half-Kneeling-High-Cable-Row-Rope.gif",
		"pretty-name": "Half Kneeling High Cable Row Rope",
	},
	"dumbbell-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Dumbbell-Raise.gif",
		"pretty-name": "Dumbbell Raise",
	},
	"dumbbell-upright-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Dumbbell-Upright-Row.gif",
		"pretty-name": "Dumbbell Upright Row",
	},
	"bodyweight-military-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Bodyweight-Military-Press.gif",
		"pretty-name": "Bodyweight Military Press",
	},
	"kneeling-high-pulley-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Kneeling-High-Pulley-Row.gif",
		"pretty-name": "Kneeling High Pulley Row",
	},
	"ez-bar-upright-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Upright-Row.gif",
		"pretty-name": "Ez Bar Upright Row",
	},
	"band-pullapart": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Band-pull-apart.gif",
		"pretty-name": "Band Pull-Apart",
	},
	"bent-over-reverse-cable-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/bent-over-reverse-cable-fly.gif",
		"pretty-name": "Bent Over Reverse Cable Fly",
	},
	"bentover-barbell-reverse-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Bent-Over-Barbell-Reverse-Raise.gif",
		"pretty-name": "Bent-Over Barbell Reverse Raise",
	},
	"barbell-rear-delt-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Barbell-Rear-Delt-Raise.gif",
		"pretty-name": "Barbell Rear Delt Raise",
	},
	"smith-machine-shrug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/smith-machine-shrug.gif",
		"pretty-name": "Smith Machine Shrug",
	},
	"incline-dumbbell-reverse-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Reverse-Fly.gif",
		"pretty-name": "Incline Dumbbell Reverse Fly",
	},
	"incline-dumbbell-yraise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Incline-Dumbbell-Y-Raise.gif",
		"pretty-name": "Incline Dumbbell Y-Raise",
	},
	"dumbbell-incline-traise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Dumbbell-Incline-T-Raise.gif",
		"pretty-name": "Dumbbell Incline T-Raise",
	},
	"swimming": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Swimming.gif",
		"pretty-name": "Swimming",
	},
	"bent-over-rear-delt-fly-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Bent-Over-Rear-Delt-Fly-Gymstick.gif",
		"pretty-name": "Bent Over Rear Delt Fly | Gymstick",
	},
	"scapular-protraction-and-retraction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Scapular-Protraction-and-Retraction.gif",
		"pretty-name": "Scapular Protraction and Retraction",
	},
	"cross-cable-face-pull": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Cross-Cable-Face-Pull.gif",
		"pretty-name": "Cross Cable Face Pull",
	},
	"elbow-reverse-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Elbow-Reverse-Push-Up.gif",
		"pretty-name": "Elbow Reverse Push-Up",
	},
	"scapula-dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Scapula-Dips.gif",
		"pretty-name": "Scapula Dips",
	},
	"pushup-plus": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Push-Up-Plus.gif",
		"pretty-name": "Push-Up Plus",
	},
	"seated-ballerina-exercise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Seated-Ballerina.gif",
		"pretty-name": "Seated Ballerina Exercise",
	},
	"seated-scapular-retraction-exercise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Seated-Scapular-Retraction-Exercise.gif",
		"pretty-name": "Seated Scapular Retraction Exercise",
	},
	"foam-roller-rhomboids": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Roll-Rhomboids.gif",
		"pretty-name": "Foam Roller Rhomboids",
	},
	"foam-roller-upper-back": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-Upper-Back.gif",
		"pretty-name": "Foam Roller Upper Back",
	},
	"scapula-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Scapula-Pull-up.gif",
		"pretty-name": "Scapula Pull-up",
	},
	"serratus-wall-slide-with-foam-roller": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Serratus-Wall-Slide-With-Foam-Roller.gif",
		"pretty-name": "Serratus Wall Slide With Foam Roller",
	},
	"dip-shrugs-serratus-shrugs": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Dip-Shrugs.gif",
		"pretty-name": "Dip Shrugs (Serratus Shrugs)",
	},
	"wide-grip-barbell-bent-over-row-plus": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/02/Wide-Grip-Barbell-Bent-Over-Row-Plus.gif",
		"pretty-name": "Wide Grip Barbell Bent Over Row Plus",
	},
	"wide-grip-alternate-barbell-bent-over-row-plus": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/02/Wide-Grip-Alternate-Barbell-Bent-Over-Row-Plus.gif",
		"pretty-name": "Wide Grip Alternate Barbell Bent Over Row Plus",
	},
	"onearm-dumbbell-upright-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/One-Arm-Dumbbell-Upright-Row.gif",
		"pretty-name": "One-Arm Dumbbell Upright Row",
	},
	"cable-y-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/cable-y-raise.gif",
		"pretty-name": "Cable Y Raise",
	},
	"barbell-upright-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/barbell-uprightrow.gif",
		"pretty-name": "Barbell Upright Row",
	},
	"resistance-band-bent-over-rear-delt-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/Resistance-Band-Bent-Over-Rear-Delt-Fly.gif",
		"pretty-name": "Resistance Band Bent Over Rear Delt Fly",
	},
	"resistance-band-pull-apart": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Resistance-Band-Pull-Apart.gif",
		"pretty-name": "Resistance Band Pull Apart",
	},
	"single-arm-upright-row-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Standing-Single-Arm-Upright-Row.gif",
		"pretty-name": "Single Arm Upright Row | Gymstick",
	},
	"face-pull-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Face-pull.gif",
		"pretty-name": "Face Pull With Resistance Band",
	},
	"seated-barbell-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Shoulder-Press.gif",
		"pretty-name": "Seated Barbell Shoulder Press",
	},
	"dumbbell-push-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/10/Dumbbell-Push-Press.gif",
		"pretty-name": "Dumbbell Push Press",
	},
	"standing-dumbbell-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/Standing-Dumbbell-Overhead-Press.gif",
		"pretty-name": "Standing Dumbbell Shoulder Press",
	},
	"arm-scissors": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Arm-Scissors.gif",
		"pretty-name": "Arm Scissors",
	},
	"side-arm-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/arm-circles.gif",
		"pretty-name": "Side Arm Raises",
	},
	"arm-circles": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/07/Arm-Circles_Shoulders.gif",
		"pretty-name": "Arm Circles",
	},
	"dumbbell-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lateral-Raise.gif",
		"pretty-name": "Dumbbell Lateral Raise",
	},
	"dumbbell-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Shoulder-Press.gif",
		"pretty-name": "Dumbbell Shoulder Press",
	},
	"smith-machine-behind-neck-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Smith-Machine-Behind-Neck-Press.gif",
		"pretty-name": "Smith Machine Behind Neck Press",
	},
	"smith-machine-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Smith-Machine-Shoulder-Press.gif",
		"pretty-name": "Smith Machine Shoulder Press",
	},
	"cable-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Cable-Lateral-Raise.gif",
		"pretty-name": "Cable Lateral Raise",
	},
	"lever-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Lever-Shoulder-Press.gif",
		"pretty-name": "Lever Shoulder Press",
	},
	"standing-close-grip-military-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Standing-Barbell-Close-Grip-Military-Press.gif",
		"pretty-name": "Standing Close Grip Military Press",
	},
	"barbell-military-press-overhead-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/07/Barbell-Standing-Military-Press.gif",
		"pretty-name": "Barbell Military Press (Overhead press)",
	},
	"dumbbell-chest-supported-lateral-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Dumbbell-Chest-Supported-Lateral-Raises.gif",
		"pretty-name": "Dumbbell Chest Supported Lateral Raises",
	},
	"dumbbell-6-way-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Dumbbell-6-Ways-Raise.gif",
		"pretty-name": "Dumbbell 6 Way Raise",
	},
	"dumbbell-4-way-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Dumbbell-4-Ways-Lateral-Raise.gif",
		"pretty-name": "Dumbbell 4 Way Lateral Raise",
	},
	"alternating-dumbbell-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Alternating-Dumbbell-Front-Raise.gif",
		"pretty-name": "Alternating Dumbbell Front Raise",
	},
	"two-arm-cable-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Two-Arm-Cable-Front-Raise.gif",
		"pretty-name": "Two Arm Cable Front Raise",
	},
	"two-arm-dumbbell-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Two-Arm-Dumbbell-Front-Raise.gif",
		"pretty-name": "Two Arm Dumbbell Front Raise",
	},
	"dumbbell-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Front-Raise.gif",
		"pretty-name": "Dumbbell Front Raise",
	},
	"cable-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Cable-Front-Raise.gif",
		"pretty-name": "Cable Front Raise",
	},
	"leaning-single-arm-dumbbell-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Leaning-Single-Arm-Dumbbell-Lateral-Raise.gif",
		"pretty-name": "Leaning Single Arm Dumbbell Lateral Raise",
	},
	"seated-behind-neck-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Seated-Behind-the-Neck-Press.gif",
		"pretty-name": "Seated Behind Neck Press",
	},
	"seated-rear-lateral-dumbbell-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Rear-Lateral-Dumbbell-Raise.gif",
		"pretty-name": "Seated Rear Lateral Dumbbell Raise",
	},
	"half-arnold-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Half-Arnold-Press.gif",
		"pretty-name": "Half Arnold Press",
	},
	"arnold-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Arnold-Press.gif",
		"pretty-name": "Arnold Press",
	},
	"seated-dumbbell-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Seated-Dumbbell-Lateral-Raise.gif",
		"pretty-name": "Seated Dumbbell Lateral Raise",
	},
	"bent-arm-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Bent-Arm-Laterl-Raise.gif",
		"pretty-name": "Bent Arm Lateral Raise",
	},
	"leaning-cable-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Leaning-Cable-Lateral-Raise.gif",
		"pretty-name": "Leaning Cable Lateral Raise",
	},
	"push-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/push-press-1.gif",
		"pretty-name": "Push Press",
	},
	"dumbbell-lying-onearm-rear-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Lying-One-Arm-Rear-Lateral-Raise.gif",
		"pretty-name": "Dumbbell Lying One-Arm Rear Lateral Raise",
	},
	"lateral-raise-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Lateral-Raise-Machine.gif",
		"pretty-name": "Lateral Raise Machine",
	},
	"scott-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/scott-press.gif",
		"pretty-name": "Scott Press",
	},
	"weighted-round-arm": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/weighted-round-arm.gif",
		"pretty-name": "Weighted Round Arm",
	},
	"weight-plate-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Weight-Plate-Front-Raise-1.gif",
		"pretty-name": "Weight Plate Front Raise",
	},
	"two-arm-cable-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Two-Arm-Cable-Lateral-Raise.gif",
		"pretty-name": "Two Arm Cable Lateral Raise",
	},
	"landmine-squat-to-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Landmine-Press.gif",
		"pretty-name": "Landmine Squat to Press",
	},
	"cable-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Cable-Shoulder-Press.gif",
		"pretty-name": "Cable Shoulder Press",
	},
	"double-cable-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Double-Cable-Front-Raise.gif",
		"pretty-name": "Double Cable Front Raise",
	},
	"standing-smith-machine-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Standing-Smith-Machine-Shoulder-Press.gif",
		"pretty-name": "Standing Smith Machine Shoulder Press",
	},
	"dumbbell-w-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Dumbbell-W-Press.gif",
		"pretty-name": "Dumbbell W Press",
	},
	"dumbbell-one-arm-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Dumbbell-One-Arm-Shoulder-Press.gif",
		"pretty-name": "Dumbbell One Arm Shoulder Press",
	},
	"dumbbell-scaption": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Dumbbell-Scaption.gif",
		"pretty-name": "Dumbbell Scaption",
	},
	"barbell-clean-and-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Barbell-Clean-and-Press-.gif",
		"pretty-name": "Barbell Clean and Press",
	},
	"dumbbell-cuban-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/dumbbell-cuban-press-.gif",
		"pretty-name": "Dumbbell Cuban Press",
	},
	"dumbbell-cuban-external-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Dumbbell-Cuban-External-Rotation.gif",
		"pretty-name": "Dumbbell Cuban External Rotation",
	},
	"standing-alternating-dumbbell-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Standing-Alternating-Dumbbell-Shoulder-Press.gif",
		"pretty-name": "Standing Alternating Dumbbell Shoulder Press",
	},
	"cable-external-shoulder-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Cable-External-Shoulder-Rotation.gif",
		"pretty-name": "Cable External Shoulder Rotation",
	},
	"cable-internal-shoulder-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Cable-Internal-Shoulder-Rotation.gif",
		"pretty-name": "Cable Internal Shoulder Rotation",
	},
	"across-chest-shoulder-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Across-Chest-Shoulder-Stretch.gif",
		"pretty-name": "Across Chest Shoulder Stretch",
	},
	"standing-reach-up-back-rotation-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Standing-Reach-Up-Back-rotation-Stretch.gif",
		"pretty-name": "Standing Reach Up Back rotation Stretch",
	},
	"shoulder-stretch-behind-the-back": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Shoulder-Stretch-Behind-Back.gif",
		"pretty-name": "Shoulder Stretch Behind The Back",
	},
	"incline-dumbbell-side-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Dumbbell-Side-Lateral-Raise.gif",
		"pretty-name": "Incline Dumbbell Side Lateral Raise",
	},
	"dumbbell-side-lying-rear-delt-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Dumbbell-Side-Lying-Rear-Delt-Raise.gif",
		"pretty-name": "Dumbbell Side Lying Rear Delt Raise",
	},
	"lying-cable-reverse-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Lying-Cable-Reverse-Fly.gif",
		"pretty-name": "Lying Cable Reverse Fly",
	},
	"single-arm-circles": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Single-Arm-Circles.gif",
		"pretty-name": "Single Arm Circles",
	},
	"dumbbell-lateral-to-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Dumbbell-Lateral-to-Front-Raise.gif",
		"pretty-name": "Dumbbell Lateral to Front Raise",
	},
	"onearm-bent-over-cable-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/One-Arm-Bent-Over-Cable-Lateral-Raise.gif",
		"pretty-name": "One-Arm Bent Over Cable Lateral Raise",
	},
	"handstand-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/handstand-push-up.gif",
		"pretty-name": "Handstand Push-Up",
	},
	"ez-bar-underhand-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/EZ-Bar-Underhand-Press.gif",
		"pretty-name": "EZ Bar Underhand Press",
	},
	"dumbbell-lying-external-shoulder-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Dumbbell-Lying-External-Shoulder-Rotation.gif",
		"pretty-name": "Dumbbell Lying External Shoulder Rotation",
	},
	"bench-supported-dumbbell-external-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Bench-Supported-Dumbbell-External-Rotation.gif",
		"pretty-name": "Bench Supported Dumbbell External Rotation",
	},
	"dumbbell-seated-bent-over-rear-delt-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Dumbbell-Seated-Bent-Over-Rear-Delt-Row.gif",
		"pretty-name": "Dumbbell Seated Bent Over Rear Delt Row",
	},
	"dumbbell-standing-palms-in-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Dumbbell-Standing-Palms-In-Press.gif",
		"pretty-name": "Dumbbell Standing Palms In Press",
	},
	"lying-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Lying-Shoulder-Press.gif",
		"pretty-name": "Lying Shoulder Press",
	},
	"dumbbell-rear-delt-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Dumbbell-Rear-Delt-Row.gif",
		"pretty-name": "Dumbbell Rear Delt Row",
	},
	"lever-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Lever-Lateral-Raise.gif",
		"pretty-name": "Lever Lateral Raise",
	},
	"kettlebell-onearm-military-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Kettlebell-One-Arm-Military-Press.gif",
		"pretty-name": "Kettlebell One-Arm Military Press",
	},
	"kettlebell-split-snatch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Kettlebell-Split-Snatch.gif",
		"pretty-name": "Kettlebell Split Snatch",
	},
	"kettlebell-windmill": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Kettlebell-Windmill.gif",
		"pretty-name": "Kettlebell Windmill",
	},
	"kettlebell-swings": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Kettlebell-Swings.gif",
		"pretty-name": "Kettlebell Swings",
	},
	"kettlebell-arnold-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Kettlebell-Arnold-Press.gif",
		"pretty-name": "Kettlebell Arnold Press",
	},
	"cable-seated-shoulder-internal-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Cable-Seated-Shoulder-Internal-Rotation.gif",
		"pretty-name": "Cable Seated Shoulder Internal Rotation",
	},
	"half-kneeling-cable-external-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Half-Kneeling-Cable-External-Rotation.gif",
		"pretty-name": "Half Kneeling Cable External Rotation",
	},
	"landmine-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Landmine-Lateral-Raise.gif",
		"pretty-name": "Landmine Lateral Raise",
	},
	"seated-dumbbell-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/seated-dumbbell-front-raise.gif",
		"pretty-name": "Seated Dumbbell Front Raise",
	},
	"one-arm-kettlebell-snatch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/03/One-Arm-Kettlebell-Snatch-exercise.gif",
		"pretty-name": "One Arm Kettlebell Snatch",
	},
	"one-arm-landmine-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/One-Arm-Landmine-Row.gif",
		"pretty-name": "One Arm Landmine Row",
	},
	"resistance-band-seated-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Resistance-Band-Seated-Shoulder-Press.gif",
		"pretty-name": "Resistance Band Seated Shoulder Press",
	},
	"bench-pike-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Bench-Pike-Push-up.gif",
		"pretty-name": "Bench Pike Push-up",
	},
	"pike-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Pike-Push-up.gif",
		"pretty-name": "Pike Push-up",
	},
	"tall-kneeling-one-arm-kettlebell-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Half-Kneeling-One-Arm-Kettlebell-Press.gif",
		"pretty-name": "Tall Kneeling One Arm Kettlebell Press",
	},
	"kettlebell-clean-and-jerk": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Kettlebell-Clean-and-Jerk.gif",
		"pretty-name": "Kettlebell Clean and Jerk",
	},
	"full-range-of-motion-lat-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Full-Range-Of-Motion-Lat-Pulldown.gif",
		"pretty-name": "Full Range Of Motion Lat Pulldown",
	},
	"lever-shoulder-press-hammer-grip": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Lever-Shoulder-Press-Hammer-Grip.gif",
		"pretty-name": "Lever Shoulder Press (Hammer Grip)",
	},
	"dumbbell-lying-rear-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/03/Dumbbell-Lying-Rear-Lateral-Raise.gif",
		"pretty-name": "Dumbbell Lying Rear Lateral Raise",
	},
	"lever-reverse-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Lever-Reverse-Shoulder-Press.gif",
		"pretty-name": "Lever Reverse Shoulder Press",
	},
	"side-lying-rear-delt-dumbbell-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Side-Lying-Rear-Delt-Dumbbell-Raise.gif",
		"pretty-name": "Side Lying Rear Delt Dumbbell Raise",
	},
	"ezbar-incline-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Incline-Front-Raise.gif",
		"pretty-name": "Ez-Bar Incline Front Raise",
	},
	"back-lever": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Back-Lever.gif",
		"pretty-name": "Back Lever",
	},
	"barbell-front-raise-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Barbell-Front-Raise-Twist.gif",
		"pretty-name": "Barbell Front Raise Twist",
	},
	"kettlebell-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/11/Kettlebell-Shoulder-Press.gif",
		"pretty-name": "Kettlebell Shoulder Press",
	},
	"wallsupported-handstand-pushups": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/07/wall-supported-handstand-push-up.gif",
		"pretty-name": "Wall-Supported Handstand Push-Ups",
	},
	"towel-shoulder-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Stretch-With-Towel.gif",
		"pretty-name": "Towel Shoulder Stretch",
	},
	"kettlebell-thruster": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Kettlebell-Thruster.gif",
		"pretty-name": "Kettlebell Thruster",
	},
	"one-arm-dumbbell-snatch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/One-Arm-Dumbbell-Snatch.gif",
		"pretty-name": "One Arm Dumbbell Snatch",
	},
	"band-front-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Band-Front-Lateral-Raise.gif",
		"pretty-name": "Band Front Lateral Raise",
	},
	"shoulder-pendulum": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/02/pendulum.gif",
		"pretty-name": "Shoulder Pendulum",
	},
	"90degree-cable-external-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/90-Degree-Cable-External-Rotation-.gif",
		"pretty-name": "90-Degree Cable External Rotation",
	},
	"90degree-cable-internal-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Cable-Shoulder-90-degrees-Internal-Rotation.gif",
		"pretty-name": "90-degree Cable Internal Rotation",
	},
	"foam-roller-posterior-shoulder": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-Posterior-Shoulder.gif",
		"pretty-name": "Foam Roller Posterior Shoulder",
	},
	"foam-roller-front-shoulder-and-chest": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Roll-Front-Shoulder-and-Chest-Lying-on-Floor.gif",
		"pretty-name": "Foam Roller Front Shoulder and Chest",
	},
	"rotator-cuff-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Rotator-Cuff-Stretch.gif",
		"pretty-name": "Rotator Cuff Stretch",
	},
	"assisted-reverse-stretch-chest-and-shoulder": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Reverse-Shoulder-Stretch.gif",
		"pretty-name": "Assisted Reverse Stretch (Chest And Shoulder)",
	},
	"lying-upper-body-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Lying-Upper-Body-Rotation.gif",
		"pretty-name": "Lying Upper Body Rotation",
	},
	"kneeling-back-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Kneeling-Back-Rotation-Stretch.gif",
		"pretty-name": "Kneeling Back Rotation",
	},
	"wall-supported-arm-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Wall-Supported-Arm-Raises.gif",
		"pretty-name": "Wall Supported Arm Raises",
	},
	"backhand-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Backhand-Raise.gif",
		"pretty-name": "Backhand Raise",
	},
	"dumbbell-seated-cuban-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Dumbbell-Seated-Cuban-Press.gif",
		"pretty-name": "Dumbbell Seated Cuban Press",
	},
	"kneeling-cable-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Kneeling-Cable-Shoulder-Press.gif",
		"pretty-name": "Kneeling Cable Shoulder Press",
	},
	"wall-slides": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/wall-slide.gif",
		"pretty-name": "Wall Slides",
	},
	"kneeling-tspine-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Kneeling-T-spine-Rotation.gif",
		"pretty-name": "Kneeling T-spine Rotation",
	},
	"plate-loaded-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Plate-Loaded-Shoulder-Press.gif",
		"pretty-name": "Plate Loaded Shoulder Press",
	},
	"chest-supported-dumbbell-front-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Chest-Supported-Dumbbell-Front-Raises.gif",
		"pretty-name": "Chest Supported Dumbbell Front Raises",
	},
	"single-arm-arnold-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Single-Arm-Arnold-Press.gif",
		"pretty-name": "Single Arm Arnold Press",
	},
	"kneeling-landmine-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Kneeling-Landmine-Press.gif",
		"pretty-name": "Kneeling Landmine Press",
	},
	"pike-pushup-between-chairs": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Pike-Push-Up-Between-Chairs.gif",
		"pretty-name": "Pike Push-Up Between Chairs",
	},
	"kettlebell-clean-and-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Kettlebell-Clean-and-Press.gif",
		"pretty-name": "Kettlebell Clean and Press",
	},
	"dumbbell-z-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Dumbbell-Z-Press.gif",
		"pretty-name": "Dumbbell Z Press",
	},
	"alternate-dumbbell-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Alternate-Dumbbell-Lateral-Raise.gif",
		"pretty-name": "Alternate Dumbbell Lateral Raise",
	},
	"back-slaps-wrap-around-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Back-Slaps-Wrap-Around-Stretch.gif",
		"pretty-name": "Back Slaps Wrap Around Stretch",
	},
	"reaction-ball-throw": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/08/Reaction-Ball-Throw-Agility-Ball-Drill-.gif",
		"pretty-name": "Reaction Ball Throw",
	},
	"front-rack-pvc-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/PVC-Front-Rack-Stretch.gif",
		"pretty-name": "Front Rack PVC Stretch",
	},
	"lever-high-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Lever-High-Row.gif",
		"pretty-name": "Lever High Row",
	},
	"cable-half-kneeling-pallof-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Half-Kneeling-Pallof-Press.gif",
		"pretty-name": "Cable Half Kneeling Pallof Press",
	},
	"chest-and-front-of-shoulder-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Chest-and-Front-of-Shoulder-Stretch.gif",
		"pretty-name": "Chest and Front of Shoulder Stretch",
	},
	"shoulder-external-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/shoulder-external-rotation-stretch.gif",
		"pretty-name": "Shoulder External Rotation",
	},
	"shoulder-internal-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/shoulder-internal-rotation-stretch.gif",
		"pretty-name": "Shoulder Internal Rotation",
	},
	"lateral-raise-with-towel-on-wall": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Lateral-Raise-with-Towel-on-Wall.gif",
		"pretty-name": "Lateral Raise with Towel on Wall",
	},
	"alternating-shoulder-flexion": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Back-to-Wall-Alternating-Shoulder-Flexion.gif",
		"pretty-name": "Alternating Shoulder Flexion",
	},
	"banded-shoulder-external-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Banded-Shoulder-External-Rotation.gif",
		"pretty-name": "Banded Shoulder External Rotation",
	},
	"banded-shoulder-flexion": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Banded-Shoulder-Flexion.gif",
		"pretty-name": "Banded Shoulder Flexion",
	},
	"banded-shoulder-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Banded-Shoulder-Extension.gif",
		"pretty-name": "Banded Shoulder Extension",
	},
	"band-single-arm-shoulder-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Single-Arm-Shoulder-Press.gif",
		"pretty-name": "Band Single Arm Shoulder Press",
	},
	"handstand-pushups-between-benches": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/07/Handstand-Push-ups-Between-Benches.gif",
		"pretty-name": "Handstand Push-ups Between Benches",
	},
	"kipping-handstand-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/07/kipping-handstand-push-up.gif",
		"pretty-name": "Kipping Handstand Push-up",
	},
	"bentover-dumbbell-rear-delt-raise-with-head-on-bench": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bent-Over-Dumbbell-Rear-Delt-Raise-With-Head-On-Bench.gif",
		"pretty-name": "Bent-Over Dumbbell Rear Delt Raise With Head On Bench",
	},
	"hindu-pushups": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pike-to-Cobra.gif",
		"pretty-name": "Hindu Push-ups",
	},
	"barbell-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Front-Raise.gif",
		"pretty-name": "Barbell Front Raise",
	},
	"corner-wall-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Corner-Wall-Stretch.gif",
		"pretty-name": "Corner Wall Stretch",
	},
	"barbell-thruster": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/thruster.gif",
		"pretty-name": "Barbell Thruster",
	},
	"one-arm-kettlebell-swing": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/One-Arm-Kettlebell-Swing.gif",
		"pretty-name": "One Arm Kettlebell Swing",
	},
	"standing-reverse-shoulder-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Standing-Reverse-Shoulder-Stretch.gif",
		"pretty-name": "Standing Reverse Shoulder Stretch",
	},
	"medicine-ball-overhead-slam": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Medicine-ball-Overhead-Slam-exercise.gif",
		"pretty-name": "Medicine ball Overhead Slam",
	},
	"doorway-pec-and-shoulder-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/01/Doorway-chest-and-sshoulder-stretch.gif",
		"pretty-name": "Doorway Pec and Shoulder Stretch",
	},
	"wall-ball": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/wall-ball.gif",
		"pretty-name": "Wall Ball",
	},
	"kettlebell-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Kettlebell-Lateral-Raise.gif",
		"pretty-name": "Kettlebell Lateral Raise",
	},
	"dumbbell-windmill": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Dumbbell-Windmill.gif",
		"pretty-name": "Dumbbell Windmill",
	},
	"dumbbell-iron-cross": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Dumbbell-Iron-Cross.gif",
		"pretty-name": "Dumbbell Iron Cross",
	},
	"incline-landmine-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Incline-Landmine-Press.gif",
		"pretty-name": "Incline Landmine Press",
	},
	"medicine-ball-overhead-throw": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/Medicine-Ball-Overhead-Throw.gif",
		"pretty-name": "Medicine Ball Overhead Throw",
	},
	"one-arm-medicine-ball-slam": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2024/06/One-Arm-Medicine-Ball-Slam.gif",
		"pretty-name": "One Arm Medicine Ball Slam",
	},
	"dumbbell-single-arm-lateral-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Dumbbell-Single-Arm-Lateral-Raise.gif",
		"pretty-name": "Dumbbell Single Arm Lateral Raise",
	},
	"dumbbell-seated-alternate-front-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Dumbbell-Seated-Alternate-Front-Raises.gif",
		"pretty-name": "Dumbbell Seated Alternate Front Raise",
	},
	"swing-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Swing-Gymstick.gif",
		"pretty-name": "Swing | Gymstick",
	},
	"side-bend-press-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Side-Bend-Press.gif",
		"pretty-name": "Side Bend Press | Gymstick",
	},
	"behind-the-head-military-press-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Standing-Behind-Head-Military-Press.gif",
		"pretty-name": "Behind the Head Military Press | Gymstick",
	},
	"skier-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Skier-Gymstick.gif",
		"pretty-name": "Skier | Gymstick",
	},
	"bent-over-row-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Bent-Over-Row-Gymstick.gif",
		"pretty-name": "Bent Over Row | Gymstick",
	},
	"battle-rope": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2015/07/Battle-Rope.gif",
		"pretty-name": "Battle Rope",
	},
	"bench": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bench-Press.gif",
		"pretty-name": "Bench Press",
	},
	"incline-chest-fly-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Incline-Chest-Fly-Machine.gif",
		"pretty-name": "Incline Chest Fly Machine",
	},
	"pec-deck-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pec-Deck-Fly.gif",
		"pretty-name": "Pec Deck Fly",
	},
	"dumbbell-pullover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Pullover.gif",
		"pretty-name": "Dumbbell Pullover",
	},
	"low-cable-crossover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Low-Cable-Crossover.gif",
		"pretty-name": "Low Cable Crossover",
	},
	"high-cable-crossover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/High-Cable-Crossover.gif",
		"pretty-name": "High Cable Crossover",
	},
	"cable-upper-chest-crossovers": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Cable-Upper-Chest-Crossovers.gif",
		"pretty-name": "Cable Upper Chest Crossovers",
	},
	"incline-bench": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Incline-Barbell-Bench-Press.gif",
		"pretty-name": "Incline Bench Press",
	},
	"dumbbell-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Fly.gif",
		"pretty-name": "Dumbbell Fly",
	},
	"dumbbell-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Press-1.gif",
		"pretty-name": "Dumbbell Bench Press",
	},
	"cable-crossover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Cable-Crossover.gif",
		"pretty-name": "Cable Crossover",
	},
	"onearm-cable-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/12/One-Arm-Cable-Chest-Press.gif",
		"pretty-name": "One-Arm Cable Chest Press",
	},
	"singlearm-cable-crossover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Single-Arm-Cable-Crossover.gif",
		"pretty-name": "Single-Arm Cable Crossover",
	},
	"incline-dumbbell-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Incline-dumbbell-Fly.gif",
		"pretty-name": "Incline Dumbbell Fly",
	},
	"incline-dumbbell-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Incline-Dumbbell-Press.gif",
		"pretty-name": "Incline Dumbbell Press",
	},
	"reverse-grip-incline-dumbbell-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Reverse-Grip-Incline-Dumbbell-Press.gif",
		"pretty-name": "Reverse Grip Incline Dumbbell Press",
	},
	"machine-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/10301301-Lever-Pec-Deck-Fly_Chest_720.gif",
		"pretty-name": "Machine Fly",
	},
	"decline-dumbbell-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Decline-Dumbbell-Press.gif",
		"pretty-name": "Decline Dumbbell Press",
	},
	"lever-incline-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Lever-Incline-Chest-Press.gif",
		"pretty-name": "Lever Incline Chest Press",
	},
	"dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Chest-Dips.gif",
		"pretty-name": "Chest Dips",
	},
	"assisted-chest-dip": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Assisted-Chest-Dip.gif",
		"pretty-name": "Assisted Chest Dip",
	},
	"lying-cable-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Lying-Cable-Fly.gif",
		"pretty-name": "Lying Cable Fly",
	},
	"drop-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Drop-Push-Up.gif",
		"pretty-name": "Drop Push-Up",
	},
	"inner-chest-press-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Inner-Chest-Press-Machine.gif",
		"pretty-name": "Inner Chest Press Machine",
	},
	"decline-dumbbell-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Decline-Dumbbell-Fly.gif",
		"pretty-name": "Decline Dumbbell Fly",
	},
	"incline-dumbbell-hammer-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Dumbbel-Hammer-Press.gif",
		"pretty-name": "Incline Dumbbell Hammer Press",
	},
	"dumbbell-upward-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Dumbbell-Upward-Fly.gif",
		"pretty-name": "Dumbbell Upward Fly",
	},
	"narrow-grip-wall-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Narrow-Grip-Wall-Push-Up.gif",
		"pretty-name": "Narrow Grip Wall Push-Up",
	},
	"decline-chest-press-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Decline-Chest-Press-Machine.gif",
		"pretty-name": "Decline Chest Press Machine",
	},
	"lying-chest-press-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Lying-Chest-Press-Machine.gif",
		"pretty-name": "Lying Chest Press Machine",
	},
	"wall-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Wall-Push-ups.gif",
		"pretty-name": "Wall Push-up",
	},
	"smith-machine-hex-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Smith-Machine-Hex-Press.gif",
		"pretty-name": "Smith Machine Hex Press",
	},
	"closegrip-incline-dumbbell-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Close-grip-Incline-Dumbbell-Press.gif",
		"pretty-name": "Close-grip Incline Dumbbell Press",
	},
	"kneeling-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Kneeling-Push-up.gif",
		"pretty-name": "Kneeling Push-up",
	},
	"decline-cable-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Decline-Cable-Fly.gif",
		"pretty-name": "Decline Cable Fly",
	},
	"smith-machine-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Smith-Machine-Bench-Press.gif",
		"pretty-name": "Smith Machine Bench Press",
	},
	"smith-machine-incline-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Smith-Machine-Incline-Bench-Press.gif",
		"pretty-name": "Smith Machine Incline Bench Press",
	},
	"parallel-bar-dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/parallel-bar-dip.gif",
		"pretty-name": "Parallel Bar Dips",
	},
	"back-and-pec-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Back-Pec-Stretch.gif",
		"pretty-name": "Back And Pec Stretch",
	},
	"lever-incline-hammer-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Lever-Incline-Hammer-Chest-Press.gif",
		"pretty-name": "Lever Incline Hammer Chest Press",
	},
	"lever-crossovers": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Lever-Crossovers.gif",
		"pretty-name": "Lever Crossovers",
	},
	"reverse-grip-dumbbell-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Reverse-Grip-Dumbbell-Bench-Press.gif",
		"pretty-name": "Reverse Grip Dumbbell Bench Press",
	},
	"lever-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Lever-Chest-Press.gif",
		"pretty-name": "Lever Chest Press",
	},
	"incline-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Push-Up.gif",
		"pretty-name": "Incline Push-up",
	},
	"svend-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Svend-Press.gif",
		"pretty-name": "Svend Press",
	},
	"reverse-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Reverse-Push-up.gif",
		"pretty-name": "Reverse Push-up",
	},
	"alternate-dumbbell-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Alternate-Dumbbell-Bench-Press.gif",
		"pretty-name": "Alternate Dumbbell Bench Press",
	},
	"closegrip-dumbbell-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Close-Grip-Dumbbell-Press.gif",
		"pretty-name": "Close-Grip Dumbbell Press",
	},
	"clap-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Clap-Push-Up.gif",
		"pretty-name": "Clap Push-Up",
	},
	"above-head-chest-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Above-Head-Chest-Stretch.gif",
		"pretty-name": "Above Head Chest Stretch",
	},
	"dynamic-chest-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Dynamic-Chest-Stretch.gif",
		"pretty-name": "Dynamic Chest Stretch",
	},
	"single-dumbbell-closegrip-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Single-Dumbbell-Close-grip-Press.gif",
		"pretty-name": "Single Dumbbell Close-grip Press",
	},
	"kneeling-diamond-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Knee-Push-Up.gif",
		"pretty-name": "Kneeling Diamond Push-Up",
	},
	"dips-between-chairs": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Dips-Between-Chairs.gif",
		"pretty-name": "Dips Between Chairs",
	},
	"pushup-bars": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Push-up-With-Push-up-Bars.gif",
		"pretty-name": "Push-up Bars",
	},
	"smith-machine-decline-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Smith-Machine-Decline-Bench-Press.gif",
		"pretty-name": "Smith Machine Decline Bench Press",
	},
	"one-arm-decline-cable-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/One-Arm-Decline-Cable-Fly.gif",
		"pretty-name": "One Arm Decline Cable Fly",
	},
	"korean-dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Korean-Dips.gif",
		"pretty-name": "Korean Dips",
	},
	"straight-bar-dip": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Straight-Bar-Dip.gif",
		"pretty-name": "Straight Bar Dip",
	},
	"dumbbell-one-arm-reverse-grip-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Dumbbell-One-Arm-Reverse-Grip-Press.gif",
		"pretty-name": "Dumbbell One Arm Reverse Grip Press",
	},
	"lever-one-arm-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Lever-One-Arm-Chest-Press.gif",
		"pretty-name": "Lever One Arm Chest Press",
	},
	"standing-one-arm-chest-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Standing-one-arm-chest-stretch.gif",
		"pretty-name": "Standing One Arm Chest Stretch",
	},
	"single-arm-medicine-ball-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Push-Up-Medicine-Ball.gif",
		"pretty-name": "Single Arm Medicine Ball Push-Up",
	},
	"stability-ball-decline-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/stability-ball-decline-push-ups.gif",
		"pretty-name": "Stability Ball Decline Push-Up",
	},
	"dumbbell-pullover-on-stability-ball": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Dumbbell-Pullover-On-Stability-Ball.gif",
		"pretty-name": "Dumbbell Pullover On Stability Ball",
	},
	"stability-ball-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/stability-ball-push-up.gif",
		"pretty-name": "Stability Ball Push-Up",
	},
	"dumbbell-decline-onearm-hammer-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Dumbbell-Decline-One-Arm-Hammer-Press.gif",
		"pretty-name": "Dumbbell Decline One-Arm Hammer Press",
	},
	"weighted-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Weighted-Push-up.gif",
		"pretty-name": "Weighted Push-up",
	},
	"singlearm-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Single-Arm-Push-up.gif",
		"pretty-name": "Single-Arm Push-Up",
	},
	"onearm-kettlebell-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/One-Arm-Kettlebell-Chest-Press-on-the-Bench.gif",
		"pretty-name": "One-Arm Kettlebell Chest Press",
	},
	"kettlebell-chest-press-on-the-floor": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Kettlebell-Chest-Press-on-the-Floor.gif",
		"pretty-name": "Kettlebell Chest Press on the Floor",
	},
	"wide-grip-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/07/Wide-Grip-Barbell-Bench-Press.gif",
		"pretty-name": "Wide Grip Bench Press",
	},
	"decline-barbell-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/03/Decline-Barbell-Bench-Press.gif",
		"pretty-name": "Decline Barbell Bench Press",
	},
	"one-arm-push-ups-with-support": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/One-Arm-Push-Ups-With-Support.gif",
		"pretty-name": "One Arm Push Ups With Support",
	},
	"band-standing-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Band-Standing-Chest-Press.gif",
		"pretty-name": "Band Standing Chest Press",
	},
	"seated-chest-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Seated-Chest-Stretch.gif",
		"pretty-name": "Seated Chest Stretch",
	},
	"foam-roller-chest-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-Chest-Stretch.gif",
		"pretty-name": "Foam Roller Chest Stretch",
	},
	"lever-decline-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Lever-Decline-Chest-Press.gif",
		"pretty-name": "Lever Decline Chest Press",
	},
	"incline-chest-press-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Incline-Chest-Press-Machine.gif",
		"pretty-name": "Incline Chest Press Machine",
	},
	"incline-cable-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/incline-cable-fly-1.gif",
		"pretty-name": "Incline Cable Fly",
	},
	"reverse-chest-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/11/Reverse-Chest-Stretch.gif",
		"pretty-name": "Reverse Chest Stretch",
	},
	"seated-cable-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Seated-Cable-Chest-Press.gif",
		"pretty-name": "Seated Cable Chest Press",
	},
	"seated-cable-close-grip-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Seated-Cable-Close-Grip-Chest-Press.gif",
		"pretty-name": "Seated Cable Close Grip Chest Press",
	},
	"forearm-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Forearm-Push-up.gif",
		"pretty-name": "Forearm Push-up",
	},
	"banded-shoulder-adduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Banded-Shoulder-Adduction.gif",
		"pretty-name": "Banded Shoulder Adduction",
	},
	"band-alternate-incline-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Alternate-Incline-Chest-Press-.gif",
		"pretty-name": "Band Alternate Incline Chest Press",
	},
	"incline-closegrip-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Incline-Close-Grip-Bench-Press.gif",
		"pretty-name": "Incline Close-Grip Bench Press",
	},
	"close-grip-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Close-Grip-Bench-Press.gif",
		"pretty-name": "Close Grip Bench Press",
	},
	"diamond-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Diamond-Push-up.gif",
		"pretty-name": "Diamond Push-up",
	},
	"pushups": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif",
		"pretty-name": "Pushups",
	},
	"hammer-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Hammer-Press.gif",
		"pretty-name": "Hammer Press",
	},
	"chest-press-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Chest-Press-Machine.gif",
		"pretty-name": "Chest Press Machine",
	},
	"barbell-floor-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Barbell-Floor-Press.gif",
		"pretty-name": "Barbell Floor Press",
	},
	"landmine-floor-chest-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Landmine-Floor-Chest-Fly.gif",
		"pretty-name": "Landmine Floor Chest Fly",
	},
	"decline-hammer-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Decline-hammer-press.gif",
		"pretty-name": "Decline Hammer Press",
	},
	"closegrip-reverse-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Barbell-Reverse-Close-grip-Bench-Press.gif",
		"pretty-name": "Close-Grip Reverse Bench Press",
	},
	"widegrip-reverse-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Wide-Grip-Reverse-Bench-Press.gif",
		"pretty-name": "Wide-Grip Reverse Bench Press",
	},
	"straddle-planche": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Straddle-planche.gif",
		"pretty-name": "Straddle Planche",
	},
	"close-grip-knee-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Close-Grip-Knee-Push-up.gif",
		"pretty-name": "Close Grip Knee Push-up",
	},
	"pushup-with-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/push-up-with-rotation.gif",
		"pretty-name": "Push-up With Rotation",
	},
	"supine-medicine-ball-chest-throw": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Supine-Medicine-Ball-Chest-Throw-exercise.gif",
		"pretty-name": "Supine Medicine Ball Chest Throw",
	},
	"reverse-dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Reverse-Dips.gif",
		"pretty-name": "Reverse Dips",
	},
	"trx-chest-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Trx-Chest-Press.gif",
		"pretty-name": "Trx Chest Press",
	},
	"dumbbell-straight-arm-pullover-knees-at-90-degrees": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/11/Dumbbell-Straight-Arm-Pullover-knees-at-90-degrees.gif",
		"pretty-name": "Dumbbell Straight Arm Pullover (knees at 90 degrees)",
	},
	"trx-chest-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Trx-Chest-Flyes.gif",
		"pretty-name": "Trx Chest Fly",
	},
	"kettlebell-renegade-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Kettlebell-Renegade-Row.gif",
		"pretty-name": "Kettlebell Renegade Row",
	},
	"pushup-to-renegade-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Push-Up-to-Renegade-Row.gif",
		"pretty-name": "Push-Up to Renegade Row",
	},
	"modified-hindu-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Modified-Hindu-Push-up.gif",
		"pretty-name": "Modified Hindu Push-up",
	},
	"knuckle-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Knuckle-Push-Up.gif",
		"pretty-name": "Knuckle Push-Up",
	},
	"planche-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Planche-Push-Up.gif",
		"pretty-name": "Planche Push-Up",
	},
	"finger-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Finger-Push-up.gif",
		"pretty-name": "Finger Push-up",
	},
	"chest-tap-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Chest-Tap-Push-up.gif",
		"pretty-name": "Chest Tap Push-up",
	},
	"kettlebell-deep-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Kettlebell-Deep-Push-Up.gif",
		"pretty-name": "Kettlebell Deep Push-Up",
	},
	"archer-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Archer-Push-Up.gif",
		"pretty-name": "Archer Push-Up",
	},
	"one-leg-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/One-Leg-Push-Up.gif",
		"pretty-name": "One Leg Push-Up",
	},
	"bosu-ball-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Bosu-Ball-Push-Up.gif",
		"pretty-name": "Bosu Ball Push-Up",
	},
	"resistance-band-alternating-chest-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Resistance-Band-Alternating-Chest-Fly.gif",
		"pretty-name": "Resistance Band Alternating Chest Fly",
	},
	"dumbbell-reverse-grip-30-degrees-incline-bench-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Dumbbell-Reverse-Grip-30-Degrees-Incline-Bench-Press.gif",
		"pretty-name": "Dumbbell Reverse Grip 30 Degrees Incline Bench Press",
	},
	"ring-dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Ring-Dips.gif",
		"pretty-name": "Ring Dips",
	},
	"cobra-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Cobra-Push-up.gif",
		"pretty-name": "Cobra Push-up",
	},
	"shoulder-tap-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Shoulder-Tap-Push-up.gif",
		"pretty-name": "Shoulder Tap Push-up",
	},
	"single-arm-raise-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Single-Arm-Raise-Push-up.gif",
		"pretty-name": "Single Arm Raise Push-up",
	},
	"suspended-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Suspended-Push-Up.gif",
		"pretty-name": "Suspended Push-Up",
	},
	"closegrip-dumbbell-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Close-grip-Dumbbell-Push-Up.gif",
		"pretty-name": "Close-grip Dumbbell Push-Up",
	},
	"medicine-ball-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Medicine-Ball-Push-Up.gif",
		"pretty-name": "Medicine Ball Push-Up",
	},
	"single-arm-pushup-on-medicine-ball": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Single-Arm-Push-Up-on-Medicine-Ball.gif",
		"pretty-name": "Single Arm Push-Up on Medicine Ball",
	},
	"weighted-vest-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Weighted-Vest-Push-up.gif",
		"pretty-name": "Weighted Vest Push-up",
	},
	"standing-medicine-ball-chest-pass": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/08/Standing-Medicine-Ball-Chest-Pass.gif",
		"pretty-name": "Standing Medicine Ball Chest Pass",
	},
	"standing-incline-chest-press-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Standing-incline-chest-press.gif",
		"pretty-name": "Standing incline chest press With Resistance Band",
	},
	"middle-chest-fly-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Middle-fly.gif",
		"pretty-name": "Middle Chest fly With Resistance Band",
	},
	"kneeling-incline-press-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Kneeling-Incline-Press-Gymstick.gif",
		"pretty-name": "Kneeling Incline Press | Gymstick",
	},
	"low-chest-fly-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Low-fly.gif",
		"pretty-name": "Low Chest Fly With Resistance Band",
	},
	"high-chest-fly-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/High-Chest-Fly-With-Resistance-Band.gif",
		"pretty-name": "High Chest Fly With Resistance Band",
	},
	"decline-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2015/07/Decline-Push-Up.gif",
		"pretty-name": "Decline Push-up",
	},
	"rowing-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Rowing-Machine.gif",
		"pretty-name": "Rowing Machine",
	},
	"lever-front-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Front-Pulldown.gif",
		"pretty-name": "Lever Front Pulldown",
	},
	"pullups": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pull-up.gif",
		"pretty-name": "Pull-ups",
	},
	"cable-rear-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Cable-Rear-Pulldown.gif",
		"pretty-name": "Cable Rear Pulldown",
	},
	"lat-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Lat-Pulldown.gif",
		"pretty-name": "Lat Pulldown",
	},
	"rows": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Cable-Row.gif",
		"pretty-name": "Rows",
	},
	"barbell-bent-over-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bent-Over-Row.gif",
		"pretty-name": "Barbell Bent Over Row",
	},
	"cable-straight-arm-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Cable-Straight-Arm-Pulldown.gif",
		"pretty-name": "Cable Straight Arm Pulldown",
	},
	"legless-rope-climb": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Rope-Climb.gif",
		"pretty-name": "Legless Rope Climb",
	},
	"lever-tbar-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Lever-T-bar-Row.gif",
		"pretty-name": "Lever T-Bar Row",
	},
	"dumbbell-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Row.gif",
		"pretty-name": "Dumbbell Row",
	},
	"bent-over-dumbbell-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bent-Over-Dumbbell-Row.gif",
		"pretty-name": "Bent Over Dumbbell Row",
	},
	"dumbbell-bent-over-reverse-grip-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Dumbbell-Bent-Over-Reverse-Row.gif",
		"pretty-name": "Dumbbell Bent Over Reverse Grip Row",
	},
	"reverse-latpulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Reverse-Lat-Pulldown.gif",
		"pretty-name": "Reverse Lat-Pulldown",
	},
	"muscleup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Muscle-up-vertical-bar.gif",
		"pretty-name": "Muscle-Up",
	},
	"seated-row-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Row-Machine.gif",
		"pretty-name": "Seated Row Machine",
	},
	"one-arm-cable-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/One-arm-Cable-Row.gif",
		"pretty-name": "One Arm Cable Row",
	},
	"reverse-grip-barbell-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Reverse-Grip-Barbell-Row.gif",
		"pretty-name": "Reverse Grip Barbell Row",
	},
	"deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Deadlift.gif",
		"pretty-name": "Deadlift",
	},
	"romanian-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Romanian-Deadlift.gif",
		"pretty-name": "Romanian Deadlift",
	},
	"upper-back-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Upper-Back-Stretch.gif",
		"pretty-name": "Upper Back Stretch",
	},
	"sumo-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Barbell-Sumo-Deadlift.gif",
		"pretty-name": "Sumo Deadlift",
	},
	"half-kneeling-lat-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Half-Kneeling-Lat-Pulldown.gif",
		"pretty-name": "Half Kneeling Lat Pulldown",
	},
	"dumbbell-straight-leg-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Dumbbell-Straight-Leg-Deadlift.gif",
		"pretty-name": "Dumbbell Straight Leg Deadlift",
	},
	"smith-machine-bent-over-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Smith-Machine-Bent-Over-Row.gif",
		"pretty-name": "Smith Machine Bent Over Row",
	},
	"incline-reverse-grip-dumbbell-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Reverse-Grip-Dumbbell-Row.gif",
		"pretty-name": "Incline Reverse Grip Dumbbell Row",
	},
	"barbell-pullover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Barbell-Bent-Arm-Pullover.gif",
		"pretty-name": "Barbell Pullover",
	},
	"cable-pullover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Lying-Extension-Pullover.gif",
		"pretty-name": "Cable Pullover",
	},
	"weighted-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Weighted-Pull-up.gif",
		"pretty-name": "Weighted Pull-up",
	},
	"reverse-grip-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Reverse-grip-Pull-up.gif",
		"pretty-name": "Reverse grip Pull-up",
	},
	"close-grip-chin-up": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Close-Grip-Chin-Up.gif",
		"pretty-name": "Close Grip Chin Up",
	},
	"assisted-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Assisted-Pull-up.gif",
		"pretty-name": "Assisted Pull-up",
	},
	"table-inverted-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Table-Inverted-Row.gif",
		"pretty-name": "Table Inverted Row",
	},
	"cable-one-arm-lat-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Cable-One-Arm-Lat-Pulldown.gif",
		"pretty-name": "Cable One Arm Lat Pulldown",
	},
	"reverse-grip-machine-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Reverse-Grip-Machine-Row.gif",
		"pretty-name": "Reverse Grip Machine Row",
	},
	"close-grip-cable-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/close-grip-cable-row.gif",
		"pretty-name": "Close Grip Cable Row",
	},
	"rope-straight-arm-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Rope-Straight-Arm-Pulldown.gif",
		"pretty-name": "Rope Straight Arm Pulldown",
	},
	"vbar-lat-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/V-bar-Lat-Pulldown.gif",
		"pretty-name": "V-bar Lat Pulldown",
	},
	"onearm-barbell-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/One-Arm-Barbell-Row-.gif",
		"pretty-name": "One-Arm Barbell Row",
	},
	"tbar-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/t-bar-rows.gif",
		"pretty-name": "T-Bar Row",
	},
	"incline-cable-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Incline-Cable-Row.gif",
		"pretty-name": "Incline Cable Row",
	},
	"cable-bent-over-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Cable-Bent-Over-Row.gif",
		"pretty-name": "Cable Bent Over Row",
	},
	"standing-side-bend-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Standing-Side-Bend-Stretch.gif",
		"pretty-name": "Standing Side Bend Stretch",
	},
	"double-cable-neutral-grip-lat-pulldown-on-floor": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Double-Cable-Neutral-Grip-Lat-Pulldown-On-Floor.gif",
		"pretty-name": "Double Cable Neutral Grip Lat Pulldown On Floor",
	},
	"incline-barbell-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Barbell-Row.gif",
		"pretty-name": "Incline Barbell Row",
	},
	"kneeling-single-arm-high-pulley-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Kneeling-Single-Arm-High-Pulley-Row.gif",
		"pretty-name": "Kneeling Single Arm High Pulley Row",
	},
	"upside-down-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Upside-Down-Pull-up.gif",
		"pretty-name": "Upside Down Pull-up",
	},
	"brachialis-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Brachialis-Pull-up.gif",
		"pretty-name": "Brachialis Pull-up",
	},
	"close-grip-latpulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Close-Grip-Lat-Pulldown.gif",
		"pretty-name": "Close Grip Lat-Pulldown",
	},
	"seated-cable-rope-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Seated-Cable-Rope-Row.gif",
		"pretty-name": "Seated Cable Rope Row",
	},
	"cable-seated-pullover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Cable-Seated-Pullover.gif",
		"pretty-name": "Cable Seated Pullover",
	},
	"ring-inverted-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Ring-Inverted-Row.gif",
		"pretty-name": "Ring Inverted Row",
	},
	"inverted-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Inverted-Row.gif",
		"pretty-name": "Inverted Row",
	},
	"lever-cable-rear-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Lever-Cable-Rear-Pulldown.gif",
		"pretty-name": "Lever Cable Rear Pulldown",
	},
	"shotgun-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/shotgun-row.gif",
		"pretty-name": "Shotgun Row",
	},
	"weighted-one-arm-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Weighted-One-Arm-Pull-up.gif",
		"pretty-name": "Weighted One Arm Pull-up",
	},
	"cable-crossover-lat-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Cable-Crossover-Lat-Pulldown.gif",
		"pretty-name": "Cable Crossover Lat Pulldown",
	},
	"lever-reverse-tbar-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Lever-Reverse-T-Bar-Row.gif",
		"pretty-name": "Lever Reverse T-Bar Row",
	},
	"kettlebell-bent-over-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Kettlebell-Bent-Over-Row.gif",
		"pretty-name": "Kettlebell Bent Over Row",
	},
	"chinup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/03/Chin-Up.gif",
		"pretty-name": "Chin-Up",
	},
	"seated-toe-touches": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Seated-Toe-Touches.gif",
		"pretty-name": "Seated Toe Touches",
	},
	"lsit-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/L-Pull-Up.gif",
		"pretty-name": "L-Sit Pull-Up",
	},
	"swing-360": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Swing-360.gif",
		"pretty-name": "Swing 360",
	},
	"front-lever-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Front-Lever-Pull-up.gif",
		"pretty-name": "Front Lever Pull-up",
	},
	"foam-roller-back-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Roll-Upper-Back.gif",
		"pretty-name": "Foam Roller Back Stretch",
	},
	"foam-roller-lat-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-Lat-Stretch.gif",
		"pretty-name": "Foam Roller Lat Stretch",
	},
	"lever-pullover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Lever-Pullover-plate-loaded.gif",
		"pretty-name": "Lever Pullover",
	},
	"one-arm-chinup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/One-Arm-Chin-Up.gif",
		"pretty-name": "One Arm Chin-Up",
	},
	"archer-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Archer-Pull-up.gif",
		"pretty-name": "Archer Pull-up",
	},
	"jumping-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/jumping-pull-up.gif",
		"pretty-name": "Jumping Pull-up",
	},
	"commando-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/commander-pull-up.gif",
		"pretty-name": "Commando Pull-up",
	},
	"behind-the-neck-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Behind-The-Neck-Pull-up.gif",
		"pretty-name": "Behind The Neck Pull-up",
	},
	"cable-onearm-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Cable-One-Arm-Pulldown.gif",
		"pretty-name": "Cable One-Arm Pulldown",
	},
	"barbell-decline-bent-arm-pullover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Barbell-Decline-Bent-Arm-Pullover.gif",
		"pretty-name": "Barbell Decline Bent Arm Pullover",
	},
	"dead-hang": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/dead-hang-360x360.png",
		"pretty-name": "Dead Hang",
	},
	"isometric-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Isometric-Pull-Up.gif",
		"pretty-name": "Isometric Pull-Up",
	},
	"climbing-monkey-bars": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Climbing-Monkey-Bars.gif",
		"pretty-name": "Climbing Monkey Bars",
	},
	"supine-spinal-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Supine-Spinal-Twist.gif",
		"pretty-name": "Supine Spinal Twist",
	},
	"bodyweight-row-in-doorway": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Bodyweight-Row-in-Doorway.gif",
		"pretty-name": "Bodyweight Row in Doorway",
	},
	"incline-dumbbell-hammer-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Incline-Dumbbell-Hammer-Row.gif",
		"pretty-name": "Incline Dumbbell Hammer Row",
	},
	"plate-loaded-seated-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Plate-Loaded-Seated-Row.gif",
		"pretty-name": "Plate Loaded Seated Row",
	},
	"chin-up-around-the-bar": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Chin-Up-Around-the-Bar.gif",
		"pretty-name": "Chin Up Around the Bar",
	},
	"ezbar-bent-arm-pullover": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/EZ-Bar-Bent-Arm-Pullover.gif",
		"pretty-name": "EZ-Bar Bent Arm Pullover",
	},
	"landmine-tbar-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/t-bar-rows.gif",
		"pretty-name": "Landmine T-Bar Row",
	},
	"cable-twisting-standing-high-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Twisting-Standing-high-Row.gif",
		"pretty-name": "Cable Twisting Standing High Row",
	},
	"single-arm-twisting-seated-cable-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Single-Arm-Twisting-Seated-Cable-Row.gif",
		"pretty-name": "Single Arm Twisting Seated Cable Row",
	},
	"band-alternating-lat-pulldown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Alternating-Lat-Pulldown.gif",
		"pretty-name": "Band Alternating Lat Pulldown",
	},
	"band-alternating-low-row-with-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Alternating-Low-Row-with-Twist.gif",
		"pretty-name": "Band Alternating Low Row with Twist",
	},
	"band-seated-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Seated-Row.gif",
		"pretty-name": "Band Seated Row",
	},
	"barbell-pendlay-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Barbell-Pendlay-Row.gif",
		"pretty-name": "Barbell Pendlay Row",
	},
	"standing-side-bend": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/standing-side-bend.gif",
		"pretty-name": "Standing side bend",
	},
	"neutral-grip-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/neutral-grip-pull-up.gif",
		"pretty-name": "Neutral Grip Pull-up",
	},
	"dumbbell-seal-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/11/Dumbbell-Seal-Row.gif",
		"pretty-name": "Dumbbell Seal Row",
	},
	"dumbbell-renegade-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/01/dumbbell-renegade-row-1.gif",
		"pretty-name": "Dumbbell Renegade Row",
	},
	"band-assisted-pullup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/band-assisted-pull-up.gif",
		"pretty-name": "Band Assisted Pull-up",
	},
	"standing-banded-row": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Straight_Back-back-standing-row.gif",
		"pretty-name": "Standing Banded Row",
	},
	"kneeling-pulldown-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Kneeling-pulldown.gif",
		"pretty-name": "Kneeling Pulldown With Resistance Band",
	},
	"dumbbell-good-morning": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/10/Dumbbell-Good-Morning.gif",
		"pretty-name": "Dumbbell Good Morning",
	},
	"dumbbell-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/dumbbell-deadlifts.gif",
		"pretty-name": "Dumbbell Deadlift",
	},
	"dumbbell-sumo-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/dumbbell-sumo-deadlift.gif",
		"pretty-name": "Dumbbell Sumo Deadlift",
	},
	"seated-back-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/seated-back-extension.gif",
		"pretty-name": "Seated Back Extension",
	},
	"good-morning": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Good-Morning.gif",
		"pretty-name": "Good Morning",
	},
	"weighted-back-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Weighted-Back-Extension.gif",
		"pretty-name": "Weighted Back Extension",
	},
	"dumbbell-romanian-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Romanian-Deadlift.gif",
		"pretty-name": "Dumbbell Romanian Deadlift",
	},
	"seated-hamstring-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Seated-Hamstring-Stretch.gif",
		"pretty-name": "Seated Hamstring Stretch",
	},
	"kettlebell-single-leg-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Kettlebell-Single-Leg-Deadlift.gif",
		"pretty-name": "Kettlebell Single Leg Deadlift",
	},
	"hyperextension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/hyperextension.gif",
		"pretty-name": "Hyperextension",
	},
	"flat-bench-hyperextension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Flat-Bench-Hyperextension.gif",
		"pretty-name": "Flat Bench Hyperextension",
	},
	"reverse-hyperextension-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Reverse-Hyperextension-Machine.gif",
		"pretty-name": "Reverse Hyperextension Machine",
	},
	"smith-machine-good-morning": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Smith-Machine-Good-Morning.gif",
		"pretty-name": "Smith Machine Good Morning",
	},
	"cable-pull-through": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Cable-Pull-Through.gif",
		"pretty-name": "Cable Pull Through",
	},
	"twisting-hyperextension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Twisting-Hyperextension.gif",
		"pretty-name": "Twisting Hyperextension",
	},
	"frog-reverse-hyperextension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Reverse-Hyperextensions.gif",
		"pretty-name": "Frog Reverse Hyperextension",
	},
	"bird-dog": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Bird-Dog.gif",
		"pretty-name": "Bird Dog",
	},
	"kettlebell-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/kettlebell-deadlift.gif",
		"pretty-name": "Kettlebell Deadlift",
	},
	"standing-toe-touches": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Standing-Toe-Touches.gif",
		"pretty-name": "Standing Toe Touches",
	},
	"stiff-leg-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Stiff-Leg-Deadlift.gif",
		"pretty-name": "Stiff Leg Deadlift",
	},
	"bow-pose": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bow-Yoga-Pose.gif",
		"pretty-name": "Bow Pose",
	},
	"cat-cow-pose": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/cat-cow.gif",
		"pretty-name": "Cat Cow Pose",
	},
	"arm-leg-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/arm-leg-raise.gif",
		"pretty-name": "Arm Leg Raises",
	},
	"dumbbell-pull-through": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Dumbbell-Pull-Through.gif",
		"pretty-name": "Dumbbell Pull Through",
	},
	"glute-ham-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/07/Glute-Ham-Raise.gif",
		"pretty-name": "Glute Ham Raise",
	},
	"side-plank-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/Side-Plank-Rotation.gif",
		"pretty-name": "Side Plank Rotation",
	},
	"kettlebell-figure-8": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Kettlebell-Figure-8.gif",
		"pretty-name": "Kettlebell Figure 8",
	},
	"barbell-single-leg-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Barbell-Single-Leg-Deadlift.gif",
		"pretty-name": "Barbell Single Leg Deadlift",
	},
	"dumbbell-single-leg-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Dumbbell-Single-Leg-Deadlift.gif",
		"pretty-name": "Dumbbell Single Leg Deadlift",
	},
	"good-morning-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Good-Morning-With-Resistance-Band.gif",
		"pretty-name": "Good Morning With Resistance Band",
	},
	"rolling-like-a-ball": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Rolling-Like-a-Ball-crab.gif",
		"pretty-name": "Rolling Like a Ball",
	},
	"dhanurasana-rocking-bow-pose": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Dhanurasana-Rocking-Bow-Pose.gif",
		"pretty-name": "Dhanurasana | Rocking Bow Pose",
	},
	"single-leg-reverse-hyperextension-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Single-Leg-Reverse-Hyperextension.gif",
		"pretty-name": "Single Leg Reverse Hyperextension | Gymstick",
	},
	"seated-zottman-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/10/Seated-Zottman-Curl.gif",
		"pretty-name": "Seated Zottman Curl",
	},
	"standing-barbell-concentration-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/10/Standing-Barbell-Concentration-Curl.gif",
		"pretty-name": "Standing Barbell Concentration Curl",
	},
	"waiter-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/waiter-curl.gif",
		"pretty-name": "Waiter Curl",
	},
	"double-arm-dumbbell-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Double-Arm-Dumbbell-Curl.gif",
		"pretty-name": "Double Arm Dumbbell Curl",
	},
	"dumbbell-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Curl.gif",
		"pretty-name": "Dumbbell Curl",
	},
	"barbell-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Curl.gif",
		"pretty-name": "Barbell Curl",
	},
	"concentration-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Concentration-Curl.gif",
		"pretty-name": "Concentration Curl",
	},
	"dumbbell-preacher-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Preacher-Curl.gif",
		"pretty-name": "Dumbbell Preacher Curl",
	},
	"ez-bar-preacher-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Z-Bar-Preacher-Curl.gif",
		"pretty-name": "EZ Bar Preacher Curl",
	},
	"hammer-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Hammer-Curl.gif",
		"pretty-name": "Hammer Curl",
	},
	"incline-dumbbell-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Incline-Dumbbell-Curl.gif",
		"pretty-name": "Incline Dumbbell Curl",
	},
	"lever-preacher-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Lever-Preacher-Curl.gif",
		"pretty-name": "Lever Preacher Curl",
	},
	"high-cable-single-arm-bicep-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/High-Cable-Single-Arm-Bicep-Curl.gif",
		"pretty-name": "High Cable Single Arm Bicep Curl",
	},
	"one-arm-cable-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/One-Arm-Cable-Curl.gif",
		"pretty-name": "One Arm Cable Curl",
	},
	"lying-cable-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/lying-cable-curl.gif",
		"pretty-name": "Lying Cable Curl",
	},
	"zottman-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/zottman-curl.gif",
		"pretty-name": "Zottman Curl",
	},
	"dumbbell-reverse-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/dumbbell-reverse-curl.gif",
		"pretty-name": "Dumbbell Reverse Curl",
	},
	"seated-closegrip-concentration-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Seated-close-grip-concentration-curl.gif",
		"pretty-name": "Seated Close-Grip Concentration Curl",
	},
	"biceps-leg-concentration-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Biceps-Leg-Concentration-Curl.gif",
		"pretty-name": "Biceps Leg Concentration Curl",
	},
	"prone-incline-barbell-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Prone-Incline-Biceps-Curl.gif",
		"pretty-name": "Prone Incline Barbell Curl",
	},
	"overhead-cable-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/overhead-cable-curl.gif",
		"pretty-name": "Overhead Cable Curl",
	},
	"seated-hammer-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Seated-Hammer-Curl.gif",
		"pretty-name": "Seated Hammer Curl",
	},
	"seated-biceps-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/seated-biceps-curl.gif",
		"pretty-name": "Seated Biceps Curl",
	},
	"single-arm-cable-preacher-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/cable-preacher-curls.gif",
		"pretty-name": "Single Arm Cable Preacher Curl",
	},
	"cable-concentration-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Cable-Concentration-Curl.gif",
		"pretty-name": "Cable Concentration Curl",
	},
	"reverse-grip-ezbar-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Reverse-Grip-EZ-Bar-Curl.gif",
		"pretty-name": "Reverse Grip EZ-Bar Curl",
	},
	"dumbbell-scott-hammer-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Dumbbell-Scott-Hammer-Curl.gif",
		"pretty-name": "Dumbbell Scott Hammer Curl",
	},
	"lying-high-bench-barbell-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Lying-High-Bench-Barbell-Curl.gif",
		"pretty-name": "Lying High Bench Barbell Curl",
	},
	"cable-rope-hammer-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/rope-bicep-curls.gif",
		"pretty-name": "Cable Rope Hammer Curl",
	},
	"biceps-curl-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Bicep-Curl-Machine.gif",
		"pretty-name": "Biceps Curl Machine",
	},
	"dumbbell-high-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Dumbbell-High-Curl.gif",
		"pretty-name": "Dumbbell High Curl",
	},
	"close-grip-zbar-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Close-Grip-Z-Bar-Curl.gif",
		"pretty-name": "Close Grip Z-Bar Curl",
	},
	"dumbbell-scott-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/dumbbell-scot-curl.gif",
		"pretty-name": "Dumbbell Scott Curl",
	},
	"barbell-curl-on-arm-blaster": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Barbell-Curl-On-Arm-Blaster.gif",
		"pretty-name": "Barbell Curl On Arm Blaster",
	},
	"arm-blaster-hammer-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Arm-Blaster-Hammer-Curl.gif",
		"pretty-name": "Arm Blaster Hammer Curl",
	},
	"dumbbell-curl-on-arm-blaster": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Dumbbell-Curl-On-Arm-Blaster.gif",
		"pretty-name": "Dumbbell Curl On Arm Blaster",
	},
	"one-arm-biceps-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/One-Arm-Biceps-Curl-1.gif",
		"pretty-name": "One Arm Biceps Curl",
	},
	"lever-biceps-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Lever-Biceps-Curl.gif",
		"pretty-name": "Lever Biceps Curl",
	},
	"cable-incline-biceps-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Cable-Incline-Biceps-Curl.gif",
		"pretty-name": "Cable Incline Biceps Curl",
	},
	"dumbbell-preacher-hammer-scott-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Dumbbell-Preacher-Hammer-Curl.gif",
		"pretty-name": "Dumbbell Preacher Hammer (Scott) Curl",
	},
	"one-arm-prone-dumbbell-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/One-Arm-Prone-Dumbbell-Curl.gif",
		"pretty-name": "One Arm Prone Dumbbell Curl",
	},
	"dumbbell-alternate-preacher-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Dumbbell-Alternate-Preacher-Curl.gif",
		"pretty-name": "Dumbbell Alternate Preacher Curl",
	},
	"two-dumbbell-preacher-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Two-dumbbell-preacher-curl.gif",
		"pretty-name": "Two Dumbbell Preacher Curl",
	},
	"barbell-alternate-biceps-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Barbell-Alternate-Biceps-Curl.gif",
		"pretty-name": "Barbell Alternate Biceps Curl",
	},
	"cable-kneeling-biceps-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Cable-Kneeling-Biceps-Curl.gif",
		"pretty-name": "Cable Kneeling Biceps Curl",
	},
	"cable-two-arm-curl-on-incline-bench": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Two-Arm-Curl-on-Incline-Bench.gif",
		"pretty-name": "Cable Two Arm Curl on Incline Bench",
	},
	"elbow-flexion": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/elbow-flexion.gif",
		"pretty-name": "Elbow Flexion",
	},
	"cable-pulldown-biceps-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Pulldown-Bicep-Curl.gif",
		"pretty-name": "Cable Pulldown Biceps Curl",
	},
	"band-biceps-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Biceps-Curl.gif",
		"pretty-name": "Band Biceps Curl",
	},
	"single-dumbbell-spider-hammer-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Single-Dumbbell-Spider-Hammer-Curl.gif",
		"pretty-name": "Single Dumbbell Spider Hammer Curl",
	},
	"cable-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/cable-curl.gif",
		"pretty-name": "Cable Curl",
	},
	"zbar-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Z-Bar-Curl.gif",
		"pretty-name": "Z-Bar Curl",
	},
	"hammer-curl-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Hammer-Curl-with-Resistance-Band.gif",
		"pretty-name": "Hammer Curl with Resistance Band",
	},
	"cable-reverse-grip-ezbar-biceps-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Reverse-Grip-EZ-bar-Biceps-Curl.gif",
		"pretty-name": "Cable Reverse Grip EZ-bar Biceps Curl",
	},
	"barbell-drag-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Barbell-Drag-Curl.gif",
		"pretty-name": "Barbell Drag Curl",
	},
	"close-grip-barbell-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/close-grip-barbell-curl.gif",
		"pretty-name": "Close Grip Barbell Curl",
	},
	"one-arm-cable-bicep-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/One-Arm-Cable-Bicep-Curl.gif",
		"pretty-name": "One Arm Cable Bicep Curl",
	},
	"single-arm-reverse-grip-cable-bicep-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Single-Arm-Reverse-Grip-Cable-Bicep-Curl.gif",
		"pretty-name": "Single Arm Reverse Grip Cable Bicep Curl",
	},
	"water-bottle-hammer-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Water-Bottle-Hammer-Curl.gif",
		"pretty-name": "Water Bottle Hammer Curl",
	},
	"seated-alternating-dumbbell-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Seated-dumbbell-alternating-curl.gif",
		"pretty-name": "Seated Alternating Dumbbell Curl",
	},
	"seated-bicep-curl-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Seated-Bicep-Curl-With-Resistance-Band.gif",
		"pretty-name": "Seated Bicep Curl With Resistance Band",
	},
	"onearm-biceps-curl-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/One-Arm-Biceps-Curl.gif",
		"pretty-name": "One-Arm Biceps Curl With Resistance Band",
	},
	"barbell-jm-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2024/12/Barbell-JM-Press.gif",
		"pretty-name": "Barbell JM Press",
	},
	"one-arm-triceps-pushdown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/11/One-arm-triceps-pushdown.gif",
		"pretty-name": "One Arm Triceps Pushdown",
	},
	"dumbbell-kickback": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Kickback.gif",
		"pretty-name": "Dumbbell Kickback",
	},
	"one-arm-reverse-pushdown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/One-Arm-Reverse-Push-Down.gif",
		"pretty-name": "One Arm Reverse Pushdown",
	},
	"tricep-rope-pushdown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pushdown.gif",
		"pretty-name": "Tricep Rope Pushdown",
	},
	"bench-dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bench-Dips.gif",
		"pretty-name": "Bench Dips",
	},
	"triceps-dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Triceps-Dips.gif",
		"pretty-name": "Triceps Dips",
	},
	"one-arm-lying-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/One-Arm-Lying-Triceps-Extension.gif",
		"pretty-name": "One Arm Lying Triceps Extension",
	},
	"cable-rope-overhead-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Cable-Rope-Overhead-Triceps-Extension.gif",
		"pretty-name": "Cable Rope Overhead Triceps Extension",
	},
	"lever-triceps-dip": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Lever-Overhand-Triceps-Dip.gif",
		"pretty-name": "Lever Triceps Dip",
	},
	"lying-barbell-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Triceps-Extension.gif",
		"pretty-name": "Lying Barbell Triceps Extension",
	},
	"cable-tricep-kickback": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Cable-Tricep-Kickback.gif",
		"pretty-name": "Cable Tricep Kickback",
	},
	"triceps-dips-on-floor": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Triceps-dips-on-floors.gif",
		"pretty-name": "Triceps Dips on Floor",
	},
	"dumbbell-seated-front-and-back-tate-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Dumbbell-Seated-Front-and-Back-Tate-Press.gif",
		"pretty-name": "Dumbbell Seated Front and Back Tate Press",
	},
	"kneeling-cable-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Kneeling-Cable-Triceps-Extension.gif",
		"pretty-name": "Kneeling Cable Triceps Extension",
	},
	"cable-rear-drive": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Cable-Rear-Drive.gif",
		"pretty-name": "Cable Rear Drive",
	},
	"body-ups": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Body-Ups.gif",
		"pretty-name": "Body Ups",
	},
	"cable-lying-triceps-extensions": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Cable-Lying-Triceps-Extensions.gif",
		"pretty-name": "Cable Lying Triceps Extensions",
	},
	"chair-dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/CHAIR-DIPS.gif",
		"pretty-name": "Chair Dips",
	},
	"seated-onearm-dumbbell-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Seated-One-Arm-Dumbbell-Triceps-Extension.gif",
		"pretty-name": "Seated One-Arm Dumbbell Triceps Extension",
	},
	"seated-dumbbell-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Seated-Dumbbell-Triceps-Extension.gif",
		"pretty-name": "Seated Dumbbell Triceps Extension",
	},
	"lever-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Lever-Tricep-Extension.gif",
		"pretty-name": "Lever Triceps Extension",
	},
	"bench-dips-on-floor": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Triceps-Dips-on-Floor.gif",
		"pretty-name": "Bench Dips on Floor",
	},
	"dumbbell-skull-crusher": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Skull-Crusher.gif",
		"pretty-name": "Dumbbell Skull Crusher",
	},
	"dumbbell-incline-two-arm-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Incline-Two-Arm-Extension.gif",
		"pretty-name": "Dumbbell Incline Two Arm Extension",
	},
	"one-arm-pronated-dumbbell-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/One-Arm-Pronated-Dumbbell-Triceps-Extension-.gif",
		"pretty-name": "One Arm Pronated Dumbbell Triceps Extension",
	},
	"seated-ezbar-overhead-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Seated-EZ-Bar-Overhead-Triceps-Extension.gif",
		"pretty-name": "Seated EZ-Bar Overhead Triceps Extension",
	},
	"cable-incline-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Cable-Incline-Triceps-Extension.gif",
		"pretty-name": "Cable Incline Triceps Extension",
	},
	"cable-side-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Cable-Side-Triceps-Extension.gif",
		"pretty-name": "Cable Side Triceps Extension",
	},
	"incline-ezbar-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/EZ-Barbell-Incline-Triceps-Extension.gif",
		"pretty-name": "Incline EZ-Bar Triceps Extension",
	},
	"high-pulley-overhead-tricep-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/High-Pulley-Overhead-Tricep-Extension.gif",
		"pretty-name": "High Pulley Overhead Tricep Extension",
	},
	"rope-pushdown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Rope-Pushdown.gif",
		"pretty-name": "Rope Pushdown",
	},
	"reverse-grip-pushdown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Reverse-Grip-Pushdown.gif",
		"pretty-name": "Reverse Grip Pushdown",
	},
	"cross-arm-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Cross-Arm-Push-up.gif",
		"pretty-name": "Cross Arm Push-up",
	},
	"cable-concentration-extension-on-knee": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Cable-Concentration-Extension-on-knee.gif",
		"pretty-name": "Cable Concentration Extension on Knee",
	},
	"cable-onearm-overhead-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Cable-One-Arm-Overhead-Triceps-Extension.gif",
		"pretty-name": "Cable One-Arm Overhead Triceps Extension",
	},
	"standing-barbell-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Standing-Barbell-Triceps-Extension.gif",
		"pretty-name": "Standing Barbell Triceps Extension",
	},
	"impossible-dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Impossible-Dips.gif",
		"pretty-name": "Impossible Dips",
	},
	"exercise-ball-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Exercise-Ball-Supine-Triceps-Extension.gif",
		"pretty-name": "Exercise Ball Triceps Extension",
	},
	"triceps-extension-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Triceps-Extension-Machine.gif",
		"pretty-name": "Triceps Extension Machine",
	},
	"triceps-dip-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Triceps-Dip-Machine.gif",
		"pretty-name": "Triceps Dip Machine",
	},
	"decline-closegrip-bench-to-skull-crusher": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Decline-Close-Grip-Bench-To-Skull-Crusher.gif",
		"pretty-name": "Decline Close-Grip Bench To Skull Crusher",
	},
	"barbell-one-arm-floor-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Barbell-One-Arm-Floor-Press.gif",
		"pretty-name": "Barbell One Arm Floor Press",
	},
	"asisted-triceps-dips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/11/Asisted-Triceps-Dips.gif",
		"pretty-name": "Asisted Triceps Dips",
	},
	"standing-triceps-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Triceps-Stretch.gif",
		"pretty-name": "Standing Triceps Stretch",
	},
	"low-cable-tricep-kickback": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Low-Cable-Tricep-Kickback.gif",
		"pretty-name": "Low Cable Tricep Kickback",
	},
	"band-skull-crusher": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Skull-Crusher.gif",
		"pretty-name": "Band Skull Crusher",
	},
	"band-pushdown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Pushdown.gif",
		"pretty-name": "Band Pushdown",
	},
	"decline-dumbbell-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Decline-Dumbbell-Triceps-Extension.gif",
		"pretty-name": "Decline Dumbbell Triceps Extension",
	},
	"dumbbell-tate-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Dumbbell-Tate-Press.gif",
		"pretty-name": "Dumbbell Tate Press",
	},
	"bent-over-kickback": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bent-Over-Triceps-Kickback.gif",
		"pretty-name": "Bent Over Kickback",
	},
	"dumbbell-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Triceps-Extension.gif",
		"pretty-name": "Dumbbell Triceps Extension",
	},
	"triceps-extension-with-resistance-bands": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Triceps-Extension-with-Resistance-Bands.gif",
		"pretty-name": "Triceps Extension with Resistance Bands",
	},
	"alternating-lying-dumbbell-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Alternating-Lying-Dumbbell-Triceps-Extension.gif",
		"pretty-name": "Alternating Lying Dumbbell Triceps Extension",
	},
	"barbell-reverse-grip-skullcrusher": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Barbell-Reverse-Grip-Skullcrusher-1.gif",
		"pretty-name": "Barbell Reverse Grip Skullcrusher",
	},
	"barbell-lying-back-of-the-head-tricep-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Barbell-Lying-Back-of-the-Head-Tricep-Extension.gif",
		"pretty-name": "Barbell Lying Back of the Head Tricep Extension",
	},
	"ez-bar-lying-close-grip-triceps-extension-behind-head": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/EZ-Bar-Lying-Close-Grip-Triceps-Extension-Behind-Head.gif",
		"pretty-name": "EZ Bar Lying Close Grip Triceps Extension Behind Head",
	},
	"one-arm-high-pulley-overhead-tricep-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-One-Arm-High-Pulley-Overhead-Tricep-Extension.gif",
		"pretty-name": "One Arm High Pulley Overhead Tricep Extension",
	},
	"cable-crossover-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Crossover-Triceps-Extension.gif",
		"pretty-name": "Cable Crossover Triceps Extension",
	},
	"side-one-arm-reverse-pushdown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Side-One-Arm-Reverse-Pushdown.gif",
		"pretty-name": "Side One Arm Reverse Pushdown",
	},
	"bodyweight-skull-crushers": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Bodyweight-Skull-Crushers.gif",
		"pretty-name": "Bodyweight Skull Crushers",
	},
	"vbar-pushdown": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/V-bar-Pushdown.gif",
		"pretty-name": "V-bar Pushdown",
	},
	"cable-rope-lying-tricep-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Rope-Lying-on-Floor-Tricep-Extension.gif",
		"pretty-name": "Cable Rope Lying Tricep Extension",
	},
	"cable-lying-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Lying-Triceps-Extension.gif",
		"pretty-name": "Cable Lying Triceps Extension",
	},
	"rear-drive-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Rear-Drive.gif",
		"pretty-name": "Rear Drive With Resistance Band",
	},
	"standing-triceps-extension-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Standing-Triceps-Extension.gif",
		"pretty-name": "Standing Triceps Extension | Gymstick",
	},
	"banded-overhead-triceps-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2020/05/Banded-Triceps-Extension.gif",
		"pretty-name": "Banded Overhead Triceps Extension",
	},
	"overhead-triceps-extension-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Overhead-Triceps-Extension.gif",
		"pretty-name": "Overhead Triceps Extension | Gymstick",
	},
	"wrist-roller": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/wrist-roller.gif",
		"pretty-name": "Wrist Roller",
	},
	"dumbbell-seated-neutral-wrist-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Seated-Neutral-Wrist-Curl.gif",
		"pretty-name": "Dumbbell Seated Neutral Wrist Curl",
	},
	"dumbbell-wrist-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Wrist-Curl.gif",
		"pretty-name": "Dumbbell Wrist Curl",
	},
	"barbell-reverse-wrist-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Barbell-Reverse-Wrist-Curl.gif",
		"pretty-name": "Barbell Reverse Wrist Curl",
	},
	"wrist-circles-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Wrist-Circles-Stretch.gif",
		"pretty-name": "Wrist Circles Stretch",
	},
	"barbell-reverse-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Reverse-Curl.gif",
		"pretty-name": "Barbell Reverse Curl",
	},
	"cable-onearm-wrist-curl-on-floor": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Cable-One-Arm-Wrist-Curl-On-Floor.gif",
		"pretty-name": "Cable One-Arm Wrist Curl On Floor",
	},
	"hand-gripper": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Hand-Gripper.gif",
		"pretty-name": "Hand Gripper",
	},
	"behind-the-back-barbell-wrist-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Behind-The-Back-Barbell-Wrist-Curl.gif",
		"pretty-name": "Behind The Back Barbell Wrist Curl",
	},
	"wrist-ulnar-deviator-and-extensor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/03/Wrist-Ulnar-Deviator-And-Extensor-Stretch.gif",
		"pretty-name": "Wrist Ulnar Deviator And Extensor Stretch",
	},
	"reverse-wrist-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/03/reverse-Wrist-Stretch.gif",
		"pretty-name": "Reverse Wrist Stretch",
	},
	"wrist-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/03/Wrist-Stretch.gif",
		"pretty-name": "Wrist Stretch",
	},
	"weighted-neutral-wrist-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Weighted-Wrist-Curl.gif",
		"pretty-name": "Weighted Neutral Wrist Curl",
	},
	"reverse-wrist-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Reverse-Wrist-Curl.gif",
		"pretty-name": "Reverse Wrist Curl",
	},
	"wrist-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/barbell-Wrist-Curl.gif",
		"pretty-name": "Wrist Curl",
	},
	"barbell-finger-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Barbell-Finger-Curl.gif",
		"pretty-name": "Barbell Finger Curl",
	},
	"dumbbell-finger-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Dumbbell-Finger-Curl.gif",
		"pretty-name": "Dumbbell Finger Curl",
	},
	"barbell-reverse-wrist-curl-over-a-bench": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Barbell-Reverse-Wrist-Curl-Over-a-Bench.gif",
		"pretty-name": "Barbell Reverse Wrist Curl Over a Bench",
	},
	"medicine-ball-rotational-throw": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/12/Medicine-Ball-Rotational-Throw.gif",
		"pretty-name": "Medicine Ball Rotational Throw",
	},
	"dragon-flag": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Leg-Raise-Dragon-Flag.gif",
		"pretty-name": "Dragon Flag",
	},
	"ab-coaster-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Ab-Coaster-Machine.gif",
		"pretty-name": "Ab Coaster Machine",
	},
	"cross-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Cross-Crunch.gif",
		"pretty-name": "Cross Crunch",
	},
	"standing-cable-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Standing-Cable-Crunch.gif",
		"pretty-name": "Standing Cable Crunch",
	},
	"seated-bench-leg-pullin": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Bench-Leg-Pull-in.gif",
		"pretty-name": "Seated Bench Leg Pull-in",
	},
	"cross-body-mountain-climber": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Cross-Body-Mountain-Climber.gif",
		"pretty-name": "Cross Body Mountain Climber",
	},
	"alternate-leg-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Alternate-Leg-Raises.gif",
		"pretty-name": "Alternate Leg Raises",
	},
	"crunches": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2015/11/Crunch.gif",
		"pretty-name": "Crunches",
	},
	"mountain-climber": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Mountain-climber.gif",
		"pretty-name": "Mountain Climber",
	},
	"bicycle-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bicycle-Crunch.gif",
		"pretty-name": "Bicycle Crunch",
	},
	"lying-scissor-kick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Lying-Scissor-Kick.gif",
		"pretty-name": "Lying Scissor Kick",
	},
	"leg-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Lying-Leg-Raise.gif",
		"pretty-name": "Leg Raise",
	},
	"oblique-floor-crunches": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Oblique-Floor-Crunches.gif",
		"pretty-name": "Oblique Floor Crunches",
	},
	"tcross-situp": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/T-Cross-Sit-up.gif",
		"pretty-name": "T-Cross Sit-up",
	},
	"dead-bug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Dead-Bug.gif",
		"pretty-name": "Dead Bug",
	},
	"decline-situp": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Decline-Sit-up.gif",
		"pretty-name": "Decline Sit-up",
	},
	"reverse-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Reverse-Crunch-1.gif",
		"pretty-name": "Reverse Crunch",
	},
	"kneeling-cable-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Kneeling-Cable-Crunch.gif",
		"pretty-name": "Kneeling Cable Crunch",
	},
	"heel-touch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Heel-Touch.gif",
		"pretty-name": "Heel Touch",
	},
	"standing-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Standing-Rotation.gif",
		"pretty-name": "Standing Rotation",
	},
	"standing-toe-touch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Standing-Toe-Touch.gif",
		"pretty-name": "Standing Toe Touch",
	},
	"crunch-with-leg-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Crunch-With-Leg-Raise.gif",
		"pretty-name": "Crunch With Leg Raise",
	},
	"alternate-lying-floor-leg-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Alternate-Lying-Floor-Leg-Raise.gif",
		"pretty-name": "Alternate Lying Floor Leg Raise",
	},
	"weighted-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Weighted-Crunch.gif",
		"pretty-name": "Weighted Crunch",
	},
	"seated-side-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Seated-Side-Crunches.gif",
		"pretty-name": "Seated Side Crunch",
	},
	"incline-leg-hip-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Incline-Leg-Hip-Raise.gif",
		"pretty-name": "Incline Leg Hip Raise",
	},
	"bodyweight-windmill": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Bodyweight-Windmill.gif",
		"pretty-name": "Bodyweight Windmill",
	},
	"front-to-side-plank": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Front-to-Side-Plank.gif",
		"pretty-name": "Front to Side Plank",
	},
	"tuck-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Tuck-Crunch.gif",
		"pretty-name": "Tuck Crunch",
	},
	"dumbbell-side-bend": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Dumbbell-Side-Bend.gif",
		"pretty-name": "Dumbbell Side Bend",
	},
	"double-leg-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Double-Leg-Stretch.gif",
		"pretty-name": "Double Leg Stretch",
	},
	"spider-plank": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Spider-Plank.gif",
		"pretty-name": "Spider Plank",
	},
	"captains-chair-leg-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Captains-Chair-Leg-Raise.gif",
		"pretty-name": "Captains Chair Leg Raise",
	},
	"bench-side-bend": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Bench-Side-Bend.gif",
		"pretty-name": "Bench Side Bend",
	},
	"crab-twist-toe-touch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Crab-Twist-Toe-Touch.gif",
		"pretty-name": "Crab Twist Toe Touch",
	},
	"quarter-situp": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Quarter-Sit-up.gif",
		"pretty-name": "Quarter Sit-up",
	},
	"weighted-situps": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/weightedsitups.gif",
		"pretty-name": "Weighted Sit-ups",
	},
	"lying-knee-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Lying-Knee-Raise.gif",
		"pretty-name": "Lying Knee Raise",
	},
	"floor-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Floor-Crunch.gif",
		"pretty-name": "Floor Crunch",
	},
	"reverse-plank": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Reverse-plank.gif",
		"pretty-name": "Reverse Plank",
	},
	"stability-ball-knee-tuck": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Stability-Ball-Knee-Tuck.gif",
		"pretty-name": "Stability Ball Knee Tuck",
	},
	"hanging-knee-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Hanging-Knee-Raises.gif",
		"pretty-name": "Hanging Knee Raises",
	},
	"hanging-side-knee-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Hanging-Side-Knee-Raises.gif",
		"pretty-name": "Hanging Side Knee Raises",
	},
	"hanging-windshield-wiper": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Hanging-Windshield-Wiper.gif",
		"pretty-name": "Hanging Windshield Wiper",
	},
	"toes-to-bar": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Toes-to-Bar.gif",
		"pretty-name": "Toes to Bar",
	},
	"weighted-hanging-knee-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/weighted-hanging-knee-raises.gif",
		"pretty-name": "Weighted Hanging Knee Raises",
	},
	"teaser-pilates": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Teaser-Pilates.gif",
		"pretty-name": "Teaser Pilates",
	},
	"seated-oblique-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Seated-Oblique-Twist.gif",
		"pretty-name": "Seated Oblique Twist",
	},
	"side-bridge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Side-Bridge.gif",
		"pretty-name": "Side Bridge",
	},
	"plank-with-arm-and-leg-lift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Plank-with-Arm-and-Leg-Lift.gif",
		"pretty-name": "Plank With Arm And Leg Lift",
	},
	"weighted-front-plank": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Weighted-Front-Plank.gif",
		"pretty-name": "Weighted Front Plank",
	},
	"cable-side-bend": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Cable-Side-Bend.gif",
		"pretty-name": "Cable Side Bend",
	},
	"barbell-side-bend": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Barbell-Side-Bend.gif",
		"pretty-name": "Barbell Side Bend",
	},
	"seated-barbell-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Barbell-Seated-Twist.gif",
		"pretty-name": "Seated Barbell Twist",
	},
	"bent-over-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Bent-Over-Twist.gif",
		"pretty-name": "Bent Over Twist",
	},
	"dumbbell-vup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Dumbbell-V-up.gif",
		"pretty-name": "Dumbbell V-up",
	},
	"lever-lying-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Lever-Lying-Crunch.gif",
		"pretty-name": "Lever Lying Crunch",
	},
	"ab-roller-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/12/Ab-Roller-Crunch.gif",
		"pretty-name": "Ab Roller Crunch",
	},
	"standing-cable-hightolow-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Standing-Cable-High-To-Low-Twist.gif",
		"pretty-name": "Standing Cable High-To-Low Twist",
	},
	"standing-cable-lowtohigh-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Standing-Cable-low-to-high-Twist.gif",
		"pretty-name": "Standing Cable Low-To-High Twist",
	},
	"standing-cable-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/standing-cable-twist.gif",
		"pretty-name": "Standing Cable Twist",
	},
	"lsit": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/L-Sit.gif",
		"pretty-name": "L-Sit",
	},
	"high-knee-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/11/High-Knee-Squat.gif",
		"pretty-name": "High Knee Squat",
	},
	"full-crunch-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Full-Crunch-Machine.gif",
		"pretty-name": "Full Crunch Machine",
	},
	"front-plank-with-arm-lift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Front-Plank-with-Arm-Lift.gif",
		"pretty-name": "Front Plank with Arm Lift",
	},
	"ab-straps-leg-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Ab-Straps-Leg-Raise.gif",
		"pretty-name": "Ab Straps Leg Raise",
	},
	"boat-pose": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Boat-Pose-Stretch.gif",
		"pretty-name": "Boat Pose",
	},
	"seated-twist-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Lever-Seated-Twist.gif",
		"pretty-name": "Seated Twist Machine",
	},
	"inchworm": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Inchworm.gif",
		"pretty-name": "Inchworm",
	},
	"front-plank-with-arm-and-leg-lift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Front-Plank-With-Arm-And-Leg-Lift.gif",
		"pretty-name": "Front Plank With Arm And Leg Lift",
	},
	"weighted-lying-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/weighted-lying-twist.gif",
		"pretty-name": "Weighted Lying Twist",
	},
	"swiss-ball-rollout": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/swiss-ball-rollout.gif",
		"pretty-name": "Swiss Ball Rollout",
	},
	"weighted-side-bend-on-stability-ball": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Weighted-Side-Bend-on-stability-ball.gif",
		"pretty-name": "Weighted Side Bend On Stability Ball",
	},
	"stability-ball-vup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/V-Up-Down-with-Stability-ball.gif",
		"pretty-name": "Stability Ball V-Up",
	},
	"exercise-ball-frog-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Exercise-Ball-Frog-Crunch.gif",
		"pretty-name": "Exercise Ball Frog Crunch",
	},
	"cable-seated-cross-arm-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Cable-Seated-Cross-Arm-Twist.gif",
		"pretty-name": "Cable Seated Cross Arm Twist",
	},
	"burpees": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/burpees.gif",
		"pretty-name": "Burpees",
	},
	"standing-twist-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Standing-Twist-Machine.gif",
		"pretty-name": "Standing Twist Machine",
	},
	"seated-crunch-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Seated-Crunch-Machine.gif",
		"pretty-name": "Seated Crunch Machine",
	},
	"barbell-rollout": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Barbell-Rollout.gif",
		"pretty-name": "Barbell Rollout",
	},
	"landmine-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Landmine-Twist.gif",
		"pretty-name": "Landmine Twist",
	},
	"frog-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/frog-crunch.gif",
		"pretty-name": "Frog Crunch",
	},
	"ab-wheel-rollout": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Ab-Wheel-Rollout.gif",
		"pretty-name": "Ab Wheel Rollout",
	},
	"bicycle-twisting-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Bicycle-Twisting-Crunch.gif",
		"pretty-name": "Bicycle Twisting Crunch",
	},
	"hands-in-air-dead-bug": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dead-Bug.gif",
		"pretty-name": "Hands In Air Dead Bug",
	},
	"4-point-tummy-vacuum-exercise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/4-Point-Tummy-Vacuum-Exercise.gif",
		"pretty-name": "4 Point Tummy Vacuum Exercise",
	},
	"seated-flutter-kick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Seated-Flutter-Kick.gif",
		"pretty-name": "Seated Flutter Kick",
	},
	"seated-cable-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Seated-Cable-Twist.gif",
		"pretty-name": "Seated Cable Twist",
	},
	"bodyweight-kneeling-sissy-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/02/Bodyweight-Kneeling-Sissy-Squat.gif",
		"pretty-name": "Bodyweight Kneeling Sissy Squat",
	},
	"standing-barbell-rollout": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Standing-Barbell-Rollout.gif",
		"pretty-name": "Standing Barbell Rollout",
	},
	"side-plank-oblique-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/11/Side-Plank-Oblique-Crunch.gif",
		"pretty-name": "Side Plank Oblique Crunch",
	},
	"medicine-ballsitup-throw": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/Medicine-Ball-Sit-up-Throw.gif",
		"pretty-name": "Medicine Ball-Sit-up Throw",
	},
	"side-bent": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Side-Bent.gif",
		"pretty-name": "Side Bent",
	},
	"leg-scissors": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Leg-Scissors.gif",
		"pretty-name": "Leg Scissors",
	},
	"abdominal-bracing": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Abdominal-bracing-exercise-386x386.png",
		"pretty-name": "Abdominal Bracing",
	},
	"lying-toe-touches": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Lying-Toe-Touches.gif",
		"pretty-name": "Lying Toe Touches",
	},
	"dumbbell-floor-wipers": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Dumbbell-Floor-Wipers.gif",
		"pretty-name": "Dumbbell Floor Wipers",
	},
	"side-bridge-hip-abduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Side-Bridge-Hip-Abduction.gif",
		"pretty-name": "Side Bridge Hip Abduction",
	},
	"snap-jumps": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/SNAP-JUMPS.gif",
		"pretty-name": "Snap Jumps",
	},
	"side-plank-leg-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Side-Plank-Leg-Raises.gif",
		"pretty-name": "Side Plank Leg Raises",
	},
	"reverse-plank-kicks": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Reverse-Plank-Kicks.gif",
		"pretty-name": "Reverse Plank Kicks",
	},
	"bear-crawl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bear-Crawl.gif",
		"pretty-name": "Bear Crawl",
	},
	"high-knee-skips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/High-Knee-Skips_Cardio.gif",
		"pretty-name": "High Knee Skips",
	},
	"double-crunches": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Double-Crunches.gif",
		"pretty-name": "Double Crunches",
	},
	"toe-reaches": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Toe-Reaches.gif",
		"pretty-name": "Toe Reaches",
	},
	"situps": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Sit-ups.gif",
		"pretty-name": "Sit-ups",
	},
	"side-plank": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Side-Plank-1-360x360.png",
		"pretty-name": "Side Plank",
	},
	"plank-leg-lift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Plank-Leg-Lift.gif",
		"pretty-name": "Plank Leg Lift",
	},
	"plank-knee-to-elbow": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/PLANK-KNEE-TO-ELBOW.gif",
		"pretty-name": "Plank Knee to Elbow",
	},
	"russian-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Russian-Twist.gif",
		"pretty-name": "Russian Twist",
	},
	"plank": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/plank.gif",
		"pretty-name": "Plank",
	},
	"leg-pullin-kneeups": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Leg-Pull-In-Knee-ups.gif",
		"pretty-name": "Leg Pull-in Knee-ups",
	},
	"glute-bridge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Glute-Bridge-.gif",
		"pretty-name": "Glute Bridge",
	},
	"hollow-hold": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/HollowHold-360x360.png",
		"pretty-name": "Hollow Hold",
	},
	"long-arm-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Long-Arm-Crunch.gif",
		"pretty-name": "Long Arm Crunch",
	},
	"half-wipers": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Half-Wipers.gif",
		"pretty-name": "Half Wipers",
	},
	"jackknife-situps-vup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jackknife-Sit-ups.gif",
		"pretty-name": "Jackknife Sit-ups (V-Up)",
	},
	"flutter-kick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Flutter-Kicks.gif",
		"pretty-name": "Flutter Kick",
	},
	"suspended-ab-fallout": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Suspended-Ab-Fall-out.gif",
		"pretty-name": "Suspended Ab Fall-out",
	},
	"trx-mountain-climber": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/TRX-Mountain-Climber.gif",
		"pretty-name": "TRX Mountain Climber",
	},
	"side-plank-knee-to-elbow": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Side-Plank-Knee-to-Elbow-.gif",
		"pretty-name": "Side Plank Knee to Elbow",
	},
	"half-cross-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Half-Cross-Crunch.gif",
		"pretty-name": "Half Cross Crunch",
	},
	"cable-seated-twist-on-floor": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Cable-Seated-Twist-on-Floor.gif",
		"pretty-name": "Cable Seated Twist on Floor",
	},
	"butterfly-situp": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Butterfly-Sit-up.gif",
		"pretty-name": "Butterfly Sit-up",
	},
	"prone-abdominal-hollowing": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Prone-Abdominal-Hollowing-360x360.png",
		"pretty-name": "Prone Abdominal Hollowing",
	},
	"hell-slide": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Hell-Slide.gif",
		"pretty-name": "Hell Slide",
	},
	"half-frog-pose": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Half-Frog-Pose-ardha-bhekasana.gif",
		"pretty-name": "Half Frog Pose",
	},
	"medicine-ball-crunch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Medicine-Ball-Crunch.gif",
		"pretty-name": "Medicine Ball Crunch",
	},
	"ball-russian-twist-throw-with-partner": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Ball-Russian-Twist-throw-with-partner.gif",
		"pretty-name": "Ball Russian Twist throw with partner",
	},
	"seated-ab-crunch-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Seated-Ab-Crunch-Machine.gif",
		"pretty-name": "Seated Ab Crunch Machine",
	},
	"side-lying-feet-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Side-Lying-Feet-Raise.gif",
		"pretty-name": "Side Lying Feet Raise",
	},
	"seated-twist-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Seated-twist.gif",
		"pretty-name": "Seated Twist With Resistance Band",
	},
	"twist-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Twist.gif",
		"pretty-name": "Twist With Resistance Band",
	},
	"twist-down-up-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Twist-down-up.gif",
		"pretty-name": "Twist down up With Resistance Band",
	},
	"standing-side-bend-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Standing-Side-Bend.gif",
		"pretty-name": "Standing Side Bend | Gymstick",
	},
	"banded-lying-leg-and-hip-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Lying-leg-and-hip-raise.gif",
		"pretty-name": "Banded Lying leg and hip raise",
	},
	"banded-jack-knife-situp": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Jack-knife-sit-up.gif",
		"pretty-name": "Banded Jack knife sit-up",
	},
	"down-to-up-twist-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Down-to-Up-Twist-Gymstick.gif",
		"pretty-name": "Down to Up Twist |Gymstick",
	},
	"bicycle-crunch-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Bicycle-Crunch-Gymstick.gif",
		"pretty-name": "Bicycle Crunch | Gymstick",
	},
	"plank-jacks-extended-leg": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2015/06/Plank-Jacks-Extended-Leg.gif",
		"pretty-name": "Plank Jacks / Extended Leg",
	},
	"smith-machine-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2024/10/smith-machine-squat.gif",
		"pretty-name": "Smith Machine Squat",
	},
	"dumbbell-cossack-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2024/09/dumbbell-cossack-squat.gif",
		"pretty-name": "Dumbbell Cossack Squat",
	},
	"dumbbell-goblet-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/Dumbbell-Goblet-Squat.gif",
		"pretty-name": "Dumbbell Goblet Squat",
	},
	"curtsy-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/curtsy-lunge.gif",
		"pretty-name": "Curtsy Lunge",
	},
	"5-dot-drills": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/12/5-Dot-drills-agility-exercise.gif",
		"pretty-name": "5 Dot Drills",
	},
	"high-knee-lunge-on-bosu-ball": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/High-Knee-Lunge-on-Bosu-Ball.gif",
		"pretty-name": "High Knee Lunge on Bosu Ball",
	},
	"standing-leg-circles": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/10/Standing-Leg-Circles.gif",
		"pretty-name": "Standing Leg Circles",
	},
	"static-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/10/Static-Lunge.gif",
		"pretty-name": "Static Lunge",
	},
	"dumbbell-walking-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/dumbbell-lunges.gif",
		"pretty-name": "Dumbbell Walking Lunge",
	},
	"dumbbell-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/Dumbbell-Squat.gif",
		"pretty-name": "Dumbbell Squat",
	},
	"depth-jump-to-hurdle-hop": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/Depth-Jump-to-Hurdle-Hop.gif",
		"pretty-name": "Depth Jump to Hurdle Hop",
	},
	"power-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/power-lunge.gif",
		"pretty-name": "Power Lunge",
	},
	"bodyweight-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/07/bodyweight-lunges.gif",
		"pretty-name": "Bodyweight Lunge",
	},
	"bulgarian-split-squat-jump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/03/Bulgarian-Jump-Squat.gif",
		"pretty-name": "Bulgarian Split Squat Jump",
	},
	"squats": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/BARBELL-SQUAT.gif",
		"pretty-name": "Squats",
	},
	"leg-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2015/11/Leg-Press.gif",
		"pretty-name": "Leg Press",
	},
	"plie-dumbbell-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/Sumo-Plie-Dumbbell-Squat.gif",
		"pretty-name": "Plie Dumbbell Squat",
	},
	"leg-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Leg-Curl.gif",
		"pretty-name": "Leg Curl",
	},
	"seated-leg-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Seated-Leg-Curl.gif",
		"pretty-name": "Seated Leg Curl",
	},
	"leg-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/LEG-EXTENSION.gif",
		"pretty-name": "Leg Extension",
	},
	"barbell-hack-squats": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Hack-Squat.gif",
		"pretty-name": "Barbell Hack Squats",
	},
	"barbell-sumo-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-sumo-squat.gif",
		"pretty-name": "Barbell Sumo Squat",
	},
	"dumbbell-bulgarian-split-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Dumbbell-Bulgarian-Split-Squat.gif",
		"pretty-name": "Dumbbell Bulgarian Split Squat",
	},
	"hack-squats-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Sled-Hack-Squat.gif",
		"pretty-name": "Hack Squats Machine",
	},
	"pistol-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pistol-Squat.gif",
		"pretty-name": "Pistol Squat",
	},
	"dumbbell-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lunge.gif",
		"pretty-name": "Dumbbell Lunge",
	},
	"lever-side-hip-abduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Lever-Side-Hip-Abduction.gif",
		"pretty-name": "Lever Side Hip Abduction",
	},
	"bodyweight-sumo-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/BODYWEIGHT-SUMO-SQUAT.gif",
		"pretty-name": "Bodyweight Sumo Squat",
	},
	"hawaiian-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Hawaiian-Squat-exercise.gif",
		"pretty-name": "Hawaiian Squat",
	},
	"lever-standing-leg-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Lever-Standing-Leg-Raise.gif",
		"pretty-name": "Lever Standing Leg Raise",
	},
	"lever-side-hip-adduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Lever-Side-Hip-Adduction.gif",
		"pretty-name": "Lever Side Hip Adduction",
	},
	"barbell-bulgarian-split-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Barbell-Bulgarian-Split-Squat.gif",
		"pretty-name": "Barbell Bulgarian Split Squat",
	},
	"lever-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Lever-Deadlift.gif",
		"pretty-name": "Lever Deadlift",
	},
	"dumbbell-rear-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Dumbbell-Rear-Lunge.gif",
		"pretty-name": "Dumbbell Rear Lunge",
	},
	"barbell-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Barbell-Lunge.gif",
		"pretty-name": "Barbell Lunge",
	},
	"barbell-lateral-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Barbell-Lateral-Lunge.gif",
		"pretty-name": "Barbell Lateral Lunge",
	},
	"side-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Side-Lunge-Stretch.gif",
		"pretty-name": "Side Lunge",
	},
	"cable-hip-adduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Cable-Hips-Adduction.gif",
		"pretty-name": "Cable Hip Adduction",
	},
	"zig-zag-hops-plyometric": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Zig-Zag-Hops-Plyometric.gif",
		"pretty-name": "Zig Zag Hops Plyometric",
	},
	"bodyweight-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Bodyweight-Squat.gif",
		"pretty-name": "Bodyweight Squat",
	},
	"upavistha-konasana": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Upavistha-Konasana.gif",
		"pretty-name": "Upavistha Konasana",
	},
	"kneeling-quad-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Kneeling-Quad-Stretch.gif",
		"pretty-name": "Kneeling Quad Stretch",
	},
	"lateral-speed-step": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Lateral-Speed-Step.gif",
		"pretty-name": "Lateral Speed Step",
	},
	"seated-groin-adductor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Seated-Adductor-Groin-Stretch.gif",
		"pretty-name": "Seated Groin / Adductor Stretch",
	},
	"reverse-lunge-knee-lift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Reverse-Lunge-Knee.gif",
		"pretty-name": "Reverse Lunge Knee Lift",
	},
	"lying-hamstring-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Hamstrings-Lying-Stretch.gif",
		"pretty-name": "Lying Hamstring Stretch",
	},
	"curtsy-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Curtsey-Squat.gif",
		"pretty-name": "Curtsy Squat",
	},
	"cable-goblet-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Cable-Squat.gif",
		"pretty-name": "Cable Goblet Squat",
	},
	"thigh-fly-adductor-magnus-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Adductor-Magnus-Stretch.gif",
		"pretty-name": "Thigh fly (Adductor Magnus Stretch)",
	},
	"split-jump-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Split-Squat.gif",
		"pretty-name": "Split Jump Squat",
	},
	"cossack-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Cossack-Squat.gif",
		"pretty-name": "Cossack Squat",
	},
	"standing-cross-leg-hamstring-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Standing-Cross-Leg-Hamstring-Stretch.gif",
		"pretty-name": "Standing Cross Leg Hamstring Stretch",
	},
	"backward-jump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Backward-Jumping.gif",
		"pretty-name": "Backward Jump",
	},
	"jumping-jack": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Jumping-jack.gif",
		"pretty-name": "Jumping jack",
	},
	"single-leg-broad-jump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Single-Leg-Broad-Jump.gif",
		"pretty-name": "Single Leg Broad Jump",
	},
	"jump-squats": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jump-Squat.gif",
		"pretty-name": "Jump Squats",
	},
	"dumbbell-lateral-step-up": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Lateral-Step-Up.gif",
		"pretty-name": "Dumbbell Lateral Step Up",
	},
	"lateral-stepup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Lateral-Step-up.gif",
		"pretty-name": "Lateral Step-up",
	},
	"step-up-opposite-elbow-to-knee-twist": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Step-Up-Opposite-Elbow-to-Knee-Twist.gif",
		"pretty-name": "Step Up + Opposite Elbow to Knee Twist",
	},
	"barbell-stepup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Barbell-Step-Up.gif",
		"pretty-name": "Barbell Step-Up",
	},
	"lying-glute-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Lying-glute-stretch.gif",
		"pretty-name": "Lying Glute Stretch",
	},
	"lying-dumbbell-leg-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Lying-Dumbbell-Leg-Curl.gif",
		"pretty-name": "Lying Dumbbell Leg Curl",
	},
	"bodyweight-walking-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/bodyweight-walking-lunge.gif",
		"pretty-name": "Bodyweight Walking Lunge",
	},
	"wall-sit": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Wall-Sit-238x360.png",
		"pretty-name": "Wall Sit",
	},
	"kettlebell-pistol-squats": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Kettlebell-Pistol-Squats.gif",
		"pretty-name": "Kettlebell Pistol Squats",
	},
	"bodyweight-box-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Bodyweight-Box-Squat.gif",
		"pretty-name": "Bodyweight Box Squat",
	},
	"step-up-single-leg-balance-with-bicep-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Step-Up-Single-Leg-Balance-with-Bicep-Curl.gif",
		"pretty-name": "Step Up Single Leg Balance with Bicep Curl",
	},
	"dumbbell-stepup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/12/Dumbeel-Step-Up.gif",
		"pretty-name": "Dumbbell Step-Up",
	},
	"belt-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/belt-squat.gif",
		"pretty-name": "Belt Squat",
	},
	"lever-single-leg-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Lever-Single-Leg-Curl.gif",
		"pretty-name": "Lever Single Leg Curl",
	},
	"reverse-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/bodyweight-reverse-lunge.gif",
		"pretty-name": "Reverse Lunge",
	},
	"single-leg-step-down": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Single-Leg-Step-Down.gif",
		"pretty-name": "Single Leg Step Down",
	},
	"long-jump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/03/Long-Jump-Plyometrics.gif",
		"pretty-name": "Long Jump",
	},
	"lever-assisted-single-leg-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Lever-Assisted-Leg-Press.gif",
		"pretty-name": "Lever Assisted Single Leg Press",
	},
	"nordic-hamstring-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Nordic-Hamstring-Curl.gif",
		"pretty-name": "Nordic Hamstring Curl",
	},
	"horizontal-leg-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Lever-Horizontal-Leg-Press.gif",
		"pretty-name": "Horizontal Leg Press",
	},
	"resistance-band-toe-touch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Resistance-Band-Toe-Touch.gif",
		"pretty-name": "Resistance Band Toe Touch",
	},
	"kneeling-hip-flexor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Kneeling-Hip-Flexor-Stretch.gif",
		"pretty-name": "Kneeling Hip Flexor Stretch",
	},
	"standing-quadriceps-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Standing-Quadriceps-Stretch.gif",
		"pretty-name": "Standing Quadriceps Stretch",
	},
	"exercise-ball-wall-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Exercise-Ball-Wall-Squat.gif",
		"pretty-name": "Exercise Ball Wall Squat",
	},
	"leg-curl-on-stability-ball": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/leg-curl-on-stability-ball.gif",
		"pretty-name": "Leg Curl On Stability Ball",
	},
	"kettlebell-goblet-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/kettlebell-goblet-squat.gif",
		"pretty-name": "Kettlebell Goblet Squat",
	},
	"barbell-bench-front-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Barbell-Bench-Front-Squat.gif",
		"pretty-name": "Barbell Bench Front Squat",
	},
	"standing-side-toe-touching": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Standing-Side-Toe-Touching.gif",
		"pretty-name": "Standing Side Toe Touching",
	},
	"dumbbell-split-jump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Dumbbell-Split-Jump.gif",
		"pretty-name": "Dumbbell Split Jump",
	},
	"banded-stepup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Banded-Step-up.gif",
		"pretty-name": "Banded Step-up",
	},
	"barbell-curtsey-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Barbell-Curtsey-Lunge.gif",
		"pretty-name": "Barbell Curtsey Lunge",
	},
	"dumbbell-jump-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Dumbbell-Jump-Squat.gif",
		"pretty-name": "Dumbbell Jump Squat",
	},
	"barbell-split-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Barbell-Split-Squat.gif",
		"pretty-name": "Barbell Split Squat",
	},
	"all-fours-squad-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/All-Fours-Squad-Stretch.gif",
		"pretty-name": "All Fours Squad Stretch",
	},
	"lever-kneeling-leg-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Lever-Kneeling-Leg-Curl-.gif",
		"pretty-name": "Lever Kneeling Leg Curl",
	},
	"reverse-hack-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Reverse-Hack-Squat.gif",
		"pretty-name": "Reverse Hack Squat",
	},
	"duck-walk": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Duck-Walk.gif",
		"pretty-name": "Duck Walk",
	},
	"trap-bar-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Trap-Bar-Deadlift.gif",
		"pretty-name": "Trap Bar Deadlift",
	},
	"zercher-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Zercher-Squat.gif",
		"pretty-name": "Zercher Squat",
	},
	"front-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/front-squat.gif",
		"pretty-name": "Front Squat",
	},
	"standing-hamstring-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Standing-Hamstring-Stretch.gif",
		"pretty-name": "Standing Hamstring Stretch",
	},
	"single-leg-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Single-Leg-Press.gif",
		"pretty-name": "Single Leg Press",
	},
	"landmine-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Landmine-Lunge.gif",
		"pretty-name": "Landmine Lunge",
	},
	"single-leg-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Single-Leg-Extension.gif",
		"pretty-name": "Single Leg Extension",
	},
	"smith-machine-leg-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Smith-Machine-Leg-Press.gif",
		"pretty-name": "Smith Machine Leg Press",
	},
	"smith-machine-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Smith-Machine-Lunge.gif",
		"pretty-name": "Smith Machine Lunge",
	},
	"skater-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Skater-Squat.gif",
		"pretty-name": "Skater Squat",
	},
	"shrimp-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/shrimp-squats.gif",
		"pretty-name": "Shrimp Squat",
	},
	"towel-leg-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Towel-Leg-Curl.gif",
		"pretty-name": "Towel Leg Curl",
	},
	"foam-roller-it-iliotibial-band-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-IT-iliotibial-Band-Stretch.gif",
		"pretty-name": "Foam Roller IT (iliotibial Band) Stretch",
	},
	"foam-roller-quads": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-Quads.gif",
		"pretty-name": "Foam Roller Quads",
	},
	"foam-roller-inner-thigh-adductor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-Inner-Thigh-Adductor-Stretch.gif",
		"pretty-name": "Foam Roller Inner Thigh Adductor Stretch",
	},
	"foam-roller-hamstrings": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-Hamstrings.gif",
		"pretty-name": "Foam Roller Hamstrings",
	},
	"foam-roller-plantar-fasciitis": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-Plantar-Fasciitis.gif",
		"pretty-name": "Foam Roller Plantar Fasciitis",
	},
	"9090-hip-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/90-90-Hip-Stretch.gif",
		"pretty-name": "90/90 Hip Stretch",
	},
	"dumbbell-goblet-curtsey-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Dumbbell-Goblet-Curtsey-Lunge.gif",
		"pretty-name": "Dumbbell Goblet Curtsey Lunge",
	},
	"cable-forward-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Forward-Lunge.gif",
		"pretty-name": "Cable Forward Lunge",
	},
	"cable-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Lunge.gif",
		"pretty-name": "Cable Lunge",
	},
	"cable-front-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Front-Squat.gif",
		"pretty-name": "Cable Front Squat",
	},
	"trap-bar-jump-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/02/trap-bar-jump-squat.gif",
		"pretty-name": "Trap Bar Jump Squat",
	},
	"box-jump-to-pistol-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/02/Box-Jump-to-Pistol-Squat.gif",
		"pretty-name": "Box Jump to Pistol Squat",
	},
	"box-jump-2-to-1": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/02/Box-Jump-2-to-1.gif",
		"pretty-name": "Box Jump 2 to 1",
	},
	"box-jump-1-to-2": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/02/Box-Jump-1-to-2.gif",
		"pretty-name": "Box Jump 1 to 2",
	},
	"single-leg-box-jump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/02/Single-Leg-Box-Jump.gif",
		"pretty-name": "Single Leg Box Jump",
	},
	"seated-straight-leg-calf-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Seated-Straight-Leg-Calf-Stretch.gif",
		"pretty-name": "Seated Straight Leg Calf Stretch",
	},
	"crouching-heel-back-calf-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Crouching-Heel-Back-Calf-Stretch.gif",
		"pretty-name": "Crouching Heel Back Calf Stretch",
	},
	"barbell-jump-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/Barbell-Jump-Squat.gif",
		"pretty-name": "Barbell Jump Squat",
	},
	"frog-pose": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Frog-Pose-mandukasana.gif",
		"pretty-name": "Frog Pose",
	},
	"atg-split-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/ATG-Split-Squat.gif",
		"pretty-name": "ATG Split Squat",
	},
	"seated-piriformis-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Seated-Piriformis-Stretch.gif",
		"pretty-name": "Seated Piriformis Stretch",
	},
	"barbell-pin-front-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Barbell-Pin-Squat.gif",
		"pretty-name": "Barbell Pin Front Squat",
	},
	"heel-touch-side-kick-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Heel-Touch-Side-Kick-Squat.gif",
		"pretty-name": "Heel Touch Side Kick Squat",
	},
	"decline-bench-dumbbell-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Decline-Bench-Dumbbell-Lunge.gif",
		"pretty-name": "Decline Bench Dumbbell Lunge",
	},
	"lateral-leg-swings": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Lateral-Leg-Swings.gif",
		"pretty-name": "Lateral Leg Swings",
	},
	"banded-walk": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Banded-Walk.gif",
		"pretty-name": "Banded Walk",
	},
	"resistance-band-lateral-walk": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Resistance-Band-Lateral-Walk.gif",
		"pretty-name": "Resistance Band Lateral Walk",
	},
	"kneeling-jump-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Kneeling-Jump-Squat.gif",
		"pretty-name": "Kneeling Jump Squat",
	},
	"banded-split-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Banded-Split-Squat.gif",
		"pretty-name": "Banded Split Squat",
	},
	"banded-kettlebell-goblet-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Banded-Kettlebell-Goblet-Squat.gif",
		"pretty-name": "Banded Kettlebell Goblet Squat",
	},
	"banded-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Banded-Lunge.gif",
		"pretty-name": "Banded Lunge",
	},
	"banded-leg-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Banded-Leg-Curl.gif",
		"pretty-name": "Banded Leg Curl",
	},
	"standing-single-leg-curl-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Standing-Single-Leg-Curl-Machine.gif",
		"pretty-name": "Standing Single Leg Curl Machine",
	},
	"decline-dumbbell-leg-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Decline-Dumbbell-Leg-Curl.gif",
		"pretty-name": "Decline Dumbbell Leg Curl",
	},
	"kettlebell-front-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Kettlebell-front-squat.gif",
		"pretty-name": "Kettlebell Front Squat",
	},
	"single-knee-to-chest": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Single-Knee-To-Chest-Stretch.gif",
		"pretty-name": "Single Knee To Chest",
	},
	"pistol-squat-to-box": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Pistol-Squat-to-Box.gif",
		"pretty-name": "Pistol Squat to Box",
	},
	"landmine-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Landmine-Deadlift.gif",
		"pretty-name": "Landmine Deadlift",
	},
	"landmine-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Landmine-Squat.gif",
		"pretty-name": "Landmine Squat",
	},
	"sissy-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/sissy-squat.gif",
		"pretty-name": "Sissy Squat",
	},
	"rack-pull": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/08/barbell-rack-pull.gif",
		"pretty-name": "Rack Pull",
	},
	"standing-knee-hugs": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/STANDING-KNEE-HUGS.gif",
		"pretty-name": "Standing Knee Hugs",
	},
	"step-up-with-knee-raises": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Step-up.gif",
		"pretty-name": "Step Up with Knee Raises",
	},
	"piriformis-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Piriformis-Stretch.gif",
		"pretty-name": "Piriformis Stretch",
	},
	"half-kneeling-hip-flexor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Kneeling-Hip-Flexor-Stretch-1-360x360.png",
		"pretty-name": "Half Kneeling Hip Flexor Stretch",
	},
	"high-knee-run": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/High-Knee-Run.gif",
		"pretty-name": "High Knee Run",
	},
	"inner-thigh-side-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/INNER-THIGH-SIDE-STRETCH.gif",
		"pretty-name": "Inner Thigh Side Stretch",
	},
	"skater": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Skater.gif",
		"pretty-name": "Skater",
	},
	"butterfly-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Butterfly-Stretch.gif",
		"pretty-name": "Butterfly Stretch",
	},
	"dumbbell-forward-leaning-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/dumbbell-forward-leaning-lunge.gif",
		"pretty-name": "Dumbbell Forward Leaning Lunge",
	},
	"dumbbell-reverse-lunge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Dumbell-reverse-lunge.gif",
		"pretty-name": "Dumbbell Reverse Lunge",
	},
	"dumbbell-pistol-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Dumbell-Pistol-Squat.gif",
		"pretty-name": "Dumbbell Pistol Squat",
	},
	"bodyweight-bulgarian-split-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Bodyweight-Bulgarian-Split-Squat.gif",
		"pretty-name": "Bodyweight Bulgarian Split Squat",
	},
	"dumbbell-sumo-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/dumbbell-sumo-squat.gif",
		"pretty-name": "Dumbbell Sumo Squat",
	},
	"hip-adduction-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/HIP-ADDUCTION-MACHINE.gif",
		"pretty-name": "Hip Adduction Machine",
	},
	"hip-abduction-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/HiP-ABDUCTION-MACHINE.gif",
		"pretty-name": "Hip Abduction Machine",
	},
	"seated-banded-leg-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Seated-Banded-Leg-Extension.gif",
		"pretty-name": "Seated Banded Leg Extension",
	},
	"zercher-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/zercher-deadlift.gif",
		"pretty-name": "Zercher Deadlift",
	},
	"supported-pistol-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Supported-Pistol-Squat.gif",
		"pretty-name": "Supported Pistol Squat",
	},
	"jefferson-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/jefferson-squat.gif",
		"pretty-name": "Jefferson Squat",
	},
	"trx-pistol-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/TRX-Pistol-Squat.gif",
		"pretty-name": "TRX Pistol Squat",
	},
	"sitting-wide-leg-adductor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Sitting-Wide-Leg-Adductor-Stretch.gif",
		"pretty-name": "Sitting Wide Leg Adductor Stretch",
	},
	"standing-wide-knees-adductor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Standing-Wide-Knees-Adductor-Stretch.gif",
		"pretty-name": "Standing Wide Knees Adductor Stretch",
	},
	"standing-wide-leg-adductor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Standing-Wide-Leg-Adductor-Stretch.gif",
		"pretty-name": "Standing Wide Leg Adductor Stretch",
	},
	"knee-circles": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Knee-Circles.gif",
		"pretty-name": "Knee Circles",
	},
	"resistance-band-overhead-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/Resistance-Band-Overhead-Squat.gif",
		"pretty-name": "Resistance Band Overhead Squat",
	},
	"kneeling-leg-out-adductor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Kneeling-Leg-Out-Adductor-Stretch.gif",
		"pretty-name": "Kneeling Leg Out Adductor Stretch",
	},
	"happy-baby-pose": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Happy-Baby-Pose.gif",
		"pretty-name": "Happy Baby Pose",
	},
	"seated-leg-extension-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Seated-Leg-Extension-with-Resistance-Band.gif",
		"pretty-name": "Seated Leg Extension with Resistance Band",
	},
	"dumbbell-bench-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/dumbbell-bench-squat.gif",
		"pretty-name": "Dumbbell Bench Squat",
	},
	"pendulum-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Pendulum-Squat.gif",
		"pretty-name": "Pendulum Squat",
	},
	"box-pistol-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Box-pistol-Squat.gif",
		"pretty-name": "Box Pistol Squat",
	},
	"sitting-rotation-hip-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Sitting-Rotation-Hip-Stretch.gif",
		"pretty-name": "Sitting Rotation Hip Stretch",
	},
	"supported-one-leg-standing-hip-flexor-and-knee-extensor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Supported-One-Leg-Standing-Hip-Flexor-And-Knee-Extensor-Stretch.gif",
		"pretty-name": "Supported One Leg Standing Hip Flexor And Knee Extensor Stretch",
	},
	"squat-mobility-complex": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Squat-mobility-Complex.gif",
		"pretty-name": "Squat mobility Complex",
	},
	"standing-straight-leg-raise-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Standing-straight-leg-raise.gif",
		"pretty-name": "Standing Straight Leg Raise With Resistance Band",
	},
	"standing-leg-raise-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Standing-Leg-Raise.gif",
		"pretty-name": "Standing Leg Raise With Resistance Band",
	},
	"standing-leg-extension-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Standing-leg-extension.gif",
		"pretty-name": "Standing Leg Extension With Resistance Band",
	},
	"standing-leg-curl-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Standing-leg-curl.gif",
		"pretty-name": "Standing Leg Curl With Resistance Band",
	},
	"split-squat-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Split-Squat-Gymstick.gif",
		"pretty-name": "Split Squat | Gymstick",
	},
	"squat-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Squat-Gymstick.gif",
		"pretty-name": "Squat | Gymstick",
	},
	"banded-lying-leg-curl": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Lying-leg-curl.gif",
		"pretty-name": "Banded Lying Leg Curl",
	},
	"lying-alternate-leg-press-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Lying-Alternate-Leg-Press.gif",
		"pretty-name": "Lying Alternate Leg Press | Gymstick",
	},
	"pin-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/05/Pin-Squat.gif",
		"pretty-name": "Pin Squat",
	},
	"the-box-jump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2015/07/The-Box-Jump.gif",
		"pretty-name": "The Box Jump",
	},
	"standing-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Standing-Calf-Raise.gif",
		"pretty-name": "Standing Calf Raise",
	},
	"calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Calf-Raise.gif",
		"pretty-name": "Calf Raise",
	},
	"calf-raise-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Calf-Raise-with-Resistance-Band.gif",
		"pretty-name": "Calf Raise with Resistance Band",
	},
	"barbell-seated-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Barbell-Seated-Calf-Raise.gif",
		"pretty-name": "Barbell Seated Calf Raise",
	},
	"leg-press-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Leg-Press-Calf-Raise.gif",
		"pretty-name": "Leg Press Calf Raise",
	},
	"hack-squat-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Hack-Squat-Calf-Raise.gif",
		"pretty-name": "Hack Squat Calf Raise",
	},
	"lever-seated-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Lever-Seated-Calf-Raise.gif",
		"pretty-name": "Lever Seated Calf Raise",
	},
	"single-leg-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Single-Leg-Calf-Raises.gif",
		"pretty-name": "Single Leg Calf Raise",
	},
	"hack-machine-oneleg-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Hack-Machine-One-Leg-Calf-Raise.gif",
		"pretty-name": "Hack Machine One-Leg Calf Raise",
	},
	"donkey-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Donkey-Calf-Raise.gif",
		"pretty-name": "Donkey Calf Raise",
	},
	"lever-donkey-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Lever-Donkey-Calf-Raise.gif",
		"pretty-name": "Lever Donkey Calf Raise",
	},
	"bench-press-machine-standing-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Bench-Press-Machine-Standing-Calf-Raise.gif",
		"pretty-name": "Bench Press Machine Standing Calf Raise",
	},
	"standing-barbell-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Standing-Barbell-Calf-Raise.gif",
		"pretty-name": "Standing Barbell Calf Raise",
	},
	"weighted-donkey-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Weighted-Donkey-Calf-Raise.gif",
		"pretty-name": "Weighted Donkey Calf Raise",
	},
	"squat-hold-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/12/Squat-Hold-Calf-Raise.gif",
		"pretty-name": "Squat Hold Calf Raise",
	},
	"weighted-seated-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Weighted-Seated-Calf-Raise.gif",
		"pretty-name": "Weighted Seated Calf Raise",
	},
	"foam-roller-calves": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-Calves.gif",
		"pretty-name": "Foam Roller Calves",
	},
	"band-foot-external-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Resistance-Band-Foot-External-Rotation.gif",
		"pretty-name": "Band Foot External Rotation",
	},
	"toe-extensor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Toe-Extensor-Stretch.gif",
		"pretty-name": "Toe Extensor Stretch",
	},
	"standing-dorsiflexion": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Standing-Dorsiflexion.gif",
		"pretty-name": "Standing Dorsiflexion",
	},
	"standing-wall-calf-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Standing-Wall-Calf-Stretch.gif",
		"pretty-name": "Standing Wall Calf Stretch",
	},
	"standing-toe-up-achilles-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Standing-Toe-Up-Achilles-Stretch.gif",
		"pretty-name": "Standing Toe Up Achilles Stretch",
	},
	"standing-toe-flexor-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Standing-Toe-Flexor-Stretch.gif",
		"pretty-name": "Standing Toe Flexor Stretch",
	},
	"standing-gastrocnemius-calf-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Standing-Gastrocnemius-Calf-Stretch.gif",
		"pretty-name": "Standing Gastrocnemius Calf Stretch",
	},
	"single-heel-drop-calf-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Single-Heel-Drop-Calf-Stretch.gif",
		"pretty-name": "Single Heel Drop Calf Stretch",
	},
	"lunging-straight-leg-calf-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Lunging-Straight-Leg-Calf-Stretch.gif",
		"pretty-name": "Lunging Straight Leg Calf Stretch",
	},
	"posterior-tibialis-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Posterior-Tibialis-Stretch.gif",
		"pretty-name": "Posterior Tibialis Stretch",
	},
	"foot-and-ankles-stretches": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foot-and-Ankles-Stretches.gif",
		"pretty-name": "Foot and Ankles Stretches",
	},
	"foot-and-ankle-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Feet-and-Ankle-Rotation.gif",
		"pretty-name": "Foot and Ankle Rotation",
	},
	"calves-stretch-static-position": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Calves-Stretch-Static-Position.gif",
		"pretty-name": "Calves Stretch Static Position",
	},
	"single-leg-calves-stretch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Single-Leg-Calves-Stretch.gif",
		"pretty-name": "Single Leg Calves Stretch",
	},
	"calf-stretch-with-rope": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Calf-Stretch-with-Rope.gif",
		"pretty-name": "Calf Stretch With Rope",
	},
	"seated-calf-press-on-leg-press-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Seated-Calf-Press-on-Leg-Press-Machine.gif",
		"pretty-name": "Seated Calf Press on Leg Press Machine",
	},
	"single-calf-raise-on-leg-press-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Single-Calf-Raise-on-Leg-Press-Machine.gif",
		"pretty-name": "Single Calf Raise on Leg Press Machine",
	},
	"single-leg-donkey-calf-raise": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Single-Leg-Donkey-Calf-Raise.gif",
		"pretty-name": "Single Leg Donkey Calf Raise",
	},
	"barbell-glute-bridge-two-legs-on-bench": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/03/Barbell-Glute-Bridge-Two-Legs-on-Bench.gif",
		"pretty-name": "Barbell Glute Bridge Two Legs on Bench",
	},
	"barbell-hip-thrusts": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Hip-Thrust.gif",
		"pretty-name": "Barbell Hip Thrusts",
	},
	"smith-machine-reverse-kickback": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Smith-Machine-Reverse-Kickback.gif",
		"pretty-name": "Smith Machine Reverse Kickback",
	},
	"lever-standing-rear-kick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Lever-Standing-Rear-Kick.gif",
		"pretty-name": "Lever Standing Rear Kick",
	},
	"standing-hip-abduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Standing-Hip-Abduction-1.gif",
		"pretty-name": "Standing Hip Abduction",
	},
	"side-lying-clam": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Side-Lying-Clam.gif",
		"pretty-name": "Side Lying Clam",
	},
	"cable-donkey-kickback": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Cable-Donkey-Kickback.gif",
		"pretty-name": "Cable Donkey Kickback",
	},
	"bridge-hip-abduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Bridge-Hip-Abduction.gif",
		"pretty-name": "Bridge Hip Abduction",
	},
	"glute-kickback-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Glute-Kickback-Machine.gif",
		"pretty-name": "Glute Kickback Machine",
	},
	"standing-hip-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Standing-Hip-Extension.gif",
		"pretty-name": "Standing Hip Extension",
	},
	"bench-glute-flutter-kicks": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/12/Bench-Glute-Flutter-Kicks.gif",
		"pretty-name": "Bench Glute Flutter Kicks",
	},
	"bodyweight-hip-thrust": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/bodyweight-hip-thrust.gif",
		"pretty-name": "Bodyweight Hip Thrust",
	},
	"single-leg-bridge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Single-Leg-Bridge.gif",
		"pretty-name": "Single Leg Bridge",
	},
	"bodyweight-single-leg-deadlift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Bodyweight-Single-Leg-Deadlift.gif",
		"pretty-name": "Bodyweight Single Leg Deadlift",
	},
	"dumbbell-glute-bridge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/01/Dumbbell-Glute-Bridge.gif",
		"pretty-name": "Dumbbell Glute Bridge",
	},
	"resistance-band-reverse-hyperextension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Resistance-Band-Reverse-Hyperextension.gif",
		"pretty-name": "Resistance Band Reverse Hyperextension",
	},
	"band-lying-hip-external-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Band-Lying-Hip-External-Rotation.gif",
		"pretty-name": "Band Lying Hip External Rotation",
	},
	"single-leg-hip-thrust-jump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Single-Leg-Hip-Thrust-Jump.gif",
		"pretty-name": "Single Leg Hip Thrust Jump",
	},
	"foam-roller-glutes": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Foam-Roller-Glutes.gif",
		"pretty-name": "Foam Roller Glutes",
	},
	"kneeling-cable-pull-through": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cable-Kneeling-Pull-Through.gif",
		"pretty-name": "Kneeling Cable Pull Through",
	},
	"hip-extension-on-bench": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Hip-Extension-On-Bench.gif",
		"pretty-name": "Hip Extension On Bench",
	},
	"donkey-kick-on-smith-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Donkey-Kick-on-Smith-Machine.gif",
		"pretty-name": "Donkey Kick on Smith Machine",
	},
	"glute-bridge-on-bench": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Glute-Bridge-on-Bench.gif",
		"pretty-name": "Glute Bridge on Bench",
	},
	"donkey-kick-on-leg-extension-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Donkey-Kick-on-Leg-Extension-Machine.gif",
		"pretty-name": "Donkey Kick on Leg Extension Machine",
	},
	"hip-thrust-on-the-leg-extension-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Hip-Thrust-on-The-Leg-Extension-Machine.gif",
		"pretty-name": "Hip Thrust on The Leg Extension Machine",
	},
	"hip-thrust-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Hip-Thrust-Machine.gif",
		"pretty-name": "Hip Thrust Machine",
	},
	"squat-on-the-abductor-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Squat-on-The-Abductor-Machine.gif",
		"pretty-name": "Squat on The Abductor Machine",
	},
	"barbell-single-leg-hip-thrust": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Barbell-Single-Leg-Hip-Thrust.gif",
		"pretty-name": "Barbell Single Leg Hip Thrust",
	},
	"pelvic-tilt": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Pelvic-Tilt.gif",
		"pretty-name": "Pelvic Tilt",
	},
	"glute-bridge-one-leg-on-bench": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Glute-Bridge-One-Leg-on-Bench.gif",
		"pretty-name": "Glute Bridge One Leg on Bench",
	},
	"unilateral-bridge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Unilateral-Bridge.gif",
		"pretty-name": "Unilateral Bridge",
	},
	"straight-leg-kickback": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Straight-Leg-Kickback.gif",
		"pretty-name": "Straight Leg Kickback",
	},
	"banded-standing-glute-kickback": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Banded-Standing-Glute-Kickback.gif",
		"pretty-name": "Banded Standing Glute Kickback",
	},
	"banded-seated-hip-abduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Banded-Seated-Hip-Abduction.gif",
		"pretty-name": "Banded Seated Hip Abduction",
	},
	"banded-single-leg-glute-bridge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Banded-Single-Leg-Glute-Bridge.gif",
		"pretty-name": "Banded Single Leg Glute Bridge",
	},
	"banded-glute-bridge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Banded-Glute-Bridge.gif",
		"pretty-name": "Banded Glute Bridge",
	},
	"band-side-lying-clam": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Side-Lying-Clam.gif",
		"pretty-name": "Band Side Lying Clam",
	},
	"banded-glute-kickbacks": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Banded-Glute-Kickbacks.gif",
		"pretty-name": "Banded Glute Kickbacks",
	},
	"banded-donkey-kicks": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Banded-Donkey-Kicks.gif",
		"pretty-name": "Banded Donkey Kicks",
	},
	"banded-thigh-fly": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Banded-Thigh-Fly.gif",
		"pretty-name": "Banded Thigh Fly",
	},
	"band-side-lying-leg-lift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Side-Lying-Leg-Lift.gif",
		"pretty-name": "Band Side Lying Leg Lift",
	},
	"banded-fire-hydrant": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Banded-Fire-Hydrant.gif",
		"pretty-name": "Banded Fire Hydrant",
	},
	"frog-pump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Frog-Pump.gif",
		"pretty-name": "Frog Pump",
	},
	"band-seated-hip-external-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Seated-Hip-External-Rotation.gif",
		"pretty-name": "Band Seated Hip External Rotation",
	},
	"band-seated-hip-internal-rotation": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Seated-Hip-Internal-Rotation.gif",
		"pretty-name": "Band Seated Hip Internal Rotation",
	},
	"fire-hydrant": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Fire-Hydrant.gif",
		"pretty-name": "Fire Hydrant",
	},
	"barbell-glute-bridge": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/12/Barbell-Glute-Bridge.gif",
		"pretty-name": "Barbell Glute Bridge",
	},
	"cable-hip-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Cable-Hip-Extension.gif",
		"pretty-name": "Cable Hip Extension",
	},
	"cable-hip-abduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Cable-Hip-Abduction.gif",
		"pretty-name": "Cable Hip Abduction",
	},
	"donkey-kicks": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Donkey-Kicks.gif",
		"pretty-name": "Donkey Kicks",
	},
	"hip-circles": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Hip-Circles-Stretch.gif",
		"pretty-name": "Hip Circles",
	},
	"lever-standing-hip-extension": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/11/Lever-Standing-Hip-Extension.gif",
		"pretty-name": "Lever Standing Hip Extension",
	},
	"kicks-leg-bent": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/Kicks-Leg-Bent.gif",
		"pretty-name": "Kicks Leg Bent",
	},
	"smith-machine-hip-thrust": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Smith-Machine-Hip-Thrust.gif",
		"pretty-name": "Smith Machine Hip Thrust",
	},
	"resistance-band-hip-thrust": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Resistance-Band-Hip-Thrust.gif",
		"pretty-name": "Resistance Band Hip Thrust",
	},
	"resistance-band-hip-thrusts-on-knees": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/09/Resistance-Band-Hip-Thrusts-on-Knees.gif",
		"pretty-name": "Resistance Band Hip Thrusts on Knees",
	},
	"side-lying-hip-adduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Side-Lying-Hip-Adduction.gif",
		"pretty-name": "Side Lying Hip Adduction",
	},
	"side-hip-abduction": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Side-Hip-Abduction.gif",
		"pretty-name": "Side Hip Abduction",
	},
	"single-stiff-leg-deadlift-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Single-stiff-leg-deadlift.gif",
		"pretty-name": "Single Stiff Leg Deadlift With Resistance Band",
	},
	"pull-through-with-resistance-band": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Pull-through-Hips.gif",
		"pretty-name": "Pull through With Resistance Band",
	},
	"kneeling-single-leg-kick-gymstick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/05/Kneeling-Single-Leg-Kick.gif",
		"pretty-name": "Kneeling Single Leg Kick | Gymstick",
	},
	"navy-seal-burpee": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/10/Navy-Seal-Burpee.gif",
		"pretty-name": "Navy Seal Burpee",
	},
	"shadow-boxing": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/09/shadow-boxing-workout.gif",
		"pretty-name": "Shadow Boxing",
	},
	"riding-outdoor-bicycle": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Riding-Outdoor-Bicycle.gif",
		"pretty-name": "Riding Outdoor Bicycle",
	},
	"walking": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Walking.gif",
		"pretty-name": "Walking",
	},
	"briskly-walking": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Briskly-Walking.gif",
		"pretty-name": "Briskly Walking",
	},
	"running": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/07/Run.gif",
		"pretty-name": "Running",
	},
	"sprint": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/sprint.gif",
		"pretty-name": "Sprint",
	},
	"walk-wave-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Walk-Wave-Machine.gif",
		"pretty-name": "Walk Wave Machine",
	},
	"jump-rope": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Jump-Rope.gif",
		"pretty-name": "Jump Rope",
	},
	"bike": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Bike.gif",
		"pretty-name": "Bike",
	},
	"treadmill": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Treadmill-.gif",
		"pretty-name": "Treadmill",
	},
	"incline-treadmill": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Treadmill.gif",
		"pretty-name": "Incline Treadmill",
	},
	"manual-treadmill": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Assault-Air-Runner.gif",
		"pretty-name": "Manual Treadmill",
	},
	"elliptical-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Elliptical-Machine.gif",
		"pretty-name": "Elliptical Machine",
	},
	"stair-climber-machine": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Walking-on-Stepmill.gif",
		"pretty-name": "Stair Climber Machine",
	},
	"elbow-to-knee-twists": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Elbow-To-Knee-Twists.gif",
		"pretty-name": "Elbow To Knee Twists",
	},
	"pushup-toe-touch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Push-up-Toe-Touch.gif",
		"pretty-name": "Push-up Toe Touch",
	},
	"power-skips": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Power-Skips.gif",
		"pretty-name": "Power Skips",
	},
	"plyo-jacks": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Plyo-Jacks.gif",
		"pretty-name": "Plyo Jacks",
	},
	"split-jacks": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Split-Jacks.gif",
		"pretty-name": "Split Jacks",
	},
	"butt-kicks": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Butt-Kicks.gif",
		"pretty-name": "Butt Kicks",
	},
	"fast-feet-run": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Fast-Feet-Run.gif",
		"pretty-name": "Fast Feet Run",
	},
	"wheel-run": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Wheel-Run.gif",
		"pretty-name": "Wheel Run",
	},
	"run-in-place": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Run-in-Place-exercise.gif",
		"pretty-name": "Run in Place",
	},
	"short-stride-run": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Short-Stride-Run.gif",
		"pretty-name": "Short Stride Run",
	},
	"band-assisted-sprinter-run": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Band-Assisted-Sprinter-Run.gif",
		"pretty-name": "Band Assisted Sprinter Run",
	},
	"backward-running": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/08/Backwards-Running.gif",
		"pretty-name": "Backward Running",
	},
	"side-shuttle": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Side-Shuttle.gif",
		"pretty-name": "Side Shuttle",
	},
	"tuck-jump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Tuck-Jump.gif",
		"pretty-name": "Tuck Jump",
	},
	"boxer-shuffle-cardio": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Boxer-Shuffle-Cardio.gif",
		"pretty-name": "Boxer Shuffle Cardio",
	},
	"jab-boxing": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/10/Jab-Boxing.gif",
		"pretty-name": "Jab Boxing",
	},
	"punches": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Punches.gif",
		"pretty-name": "Punches",
	},
	"right-uppercut": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Right-Uppercut-Boxing.gif",
		"pretty-name": "Right Uppercut",
	},
	"right-cross": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/08/Right-Cross-Boxing.gif",
		"pretty-name": "Right Cross",
	},
	"hook-kick": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Hook-Kick-Kickboxing-with-boxing-bag.gif",
		"pretty-name": "Hook Kick",
	},
	"boxing-right-cross": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Boxing-Right-Cross-with-boxing-bag.gif",
		"pretty-name": "Boxing Right Cross",
	},
	"walking-high-knee-lunges": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Walking-High-Knee-Lunges.gif",
		"pretty-name": "Walking High Knee Lunges",
	},
	"high-knees-lift-run": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/Run-in-Place.gif",
		"pretty-name": "High Knees Lift Run",
	},
	"jack-burpees": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/10/Jack-Burpees.gif",
		"pretty-name": "Jack Burpees",
	},
	"astride-jumps": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/05/Astride-Jumps.gif",
		"pretty-name": "Astride Jumps",
	},
	"dumbbell-burpees": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Burpees.gif",
		"pretty-name": "Dumbbell Burpees",
	},
	"ski-step": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/04/Ski-Step.gif",
		"pretty-name": "Ski Step",
	},
	"vibration-plate": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/06/Vibrate-Plate-Standing.gif",
		"pretty-name": "Vibration Plate",
	},
	"high-knees-against-wall": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/09/High-Knees-against-wall.gif",
		"pretty-name": "High Knees Against Wall",
	},
	"vertical-mountain-climber": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Vertical-Mountain-Climber.gif",
		"pretty-name": "Vertical Mountain Climber",
	},
	"cross-body-pushup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Cross-Body-Push-up_Plyometric.gif",
		"pretty-name": "Cross Body Push-up",
	},
	"stationary-bike-run": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Stationary-Bike-Run.gif",
		"pretty-name": "Stationary Bike Run",
	},
	"hands-bike": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Hands-Bike.gif",
		"pretty-name": "Hands Bike",
	},
	"squat-tuck-jump": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Squat-Tuck-Jump.gif",
		"pretty-name": "Squat Tuck Jump",
	},
	"12-stick-drill": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/04/1-2-Stick-Drill-Plyometrics.gif",
		"pretty-name": "1-2 Stick Drill",
	},
	"assault-airbike": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Assault-AirBike.gif",
		"pretty-name": "Assault AirBike",
	},
	"recumbent-exercise-bike": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/06/Recumbent-Exercise-Bike.gif",
		"pretty-name": "Recumbent Exercise Bike",
	},
	"backward-medicine-ball-throw": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/05/Backward-Medicine-Ball-Throw.gif",
		"pretty-name": "Backward Medicine Ball Throw",
	},
	"zercher-carry": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2023/01/zercher-carry.gif",
		"pretty-name": "Zercher Carry",
	},
	"wall-walk": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/wall-walk-muscles.gif",
		"pretty-name": "Wall Walk",
	},
	"kettlebell-hang-clean": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Kettlebell-Hang-Clean.gif",
		"pretty-name": "Kettlebell Hang Clean",
	},
	"dumbbell-power-clean": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Dumbbell-Power-Clean.gif",
		"pretty-name": "Dumbbell Power Clean",
	},
	"dumbbell-devil-press": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Dumbbell-Devil-Press.gif",
		"pretty-name": "Dumbbell Devil Press",
	},
	"overhead-squat": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/overhead-squat.gif",
		"pretty-name": "Overhead Squat",
	},
	"ski-ergometer": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Ski-Ergometer.gif",
		"pretty-name": "Ski Ergometer",
	},
	"human-flag": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Human-Flag.gif",
		"pretty-name": "Human Flag",
	},
	"farmers-walk": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Farmers-walk_Cardio.gif",
		"pretty-name": "Farmer's Walk",
	},
	"log-lift": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Log-Lift.gif",
		"pretty-name": "Log Lift",
	},
	"tire-sledge-hammer": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Tire-SledgeHammer.gif",
		"pretty-name": "Tire Sledge Hammer",
	},
	"tire-flip": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/StrongMan-Tire-Flip.gif",
		"pretty-name": "Tire Flip",
	},
	"barbell-snatch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Barbell-Snatch.gif",
		"pretty-name": "Barbell Snatch",
	},
	"power-snatch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Barbell-Power-Snatch.gif",
		"pretty-name": "Power Snatch",
	},
	"muscle-snatch": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Barbell-Muscle-Snatch.gif",
		"pretty-name": "Muscle Snatch",
	},
	"heaving-snatch-balance": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Barbell-Heaving-Snatch-Balance.gif",
		"pretty-name": "Heaving Snatch Balance",
	},
	"barbell-hang-clean": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Barbell-Hang-Clean.gif",
		"pretty-name": "Barbell Hang Clean",
	},
	"power-clean": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Power-Clean-.gif",
		"pretty-name": "Power Clean",
	},
	"turkish-getup": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/04/Turkish-Get-Up-Squat-style.gif",
		"pretty-name": "Turkish Get-up",
	},
	"handstand-walk": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2022/12/handstand-walk.gif",
		"pretty-name": "Handstand Walk",
	},
	"handstand": {
		"image": "https://fitnessprogramer.com/wp-content/uploads/2021/02/handstand-holds.gif",
		"pretty-name": "Handstand",
	},
}


def getMetaFromExercise(exercise: str):
    if exercise not in EXERCISE_META:
        raise InvalidExercise(f"Exercise {exercise} not found!")
    
    return EXERCISE_META[exercise]