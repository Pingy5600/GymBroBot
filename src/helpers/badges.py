from typing import List
import psycopg2
import os
import embeds
import discord

from validations import validateDate
from .__init__ import getDiscordTimeStamp, db_manager

structured_badges = [
    {"exercise": "bench", "description": "Earned for achieving a 40kg bench",  "threshold": 40,  "badge_name": "Noobie Bench", "icon": "<:40kgBench:1366393140470222858>", "rarity": "Common"},
    {"exercise": "bench", "description": "Earned for achieving a 50kg bench",  "threshold": 50,  "badge_name": "Starter Bench", "icon": "<:50kgBench:1366393067661426800>", "rarity": "Common"},
    {"exercise": "bench", "description": "Earned for achieving a 60kg bench",  "threshold": 60,  "badge_name": "Novice Bench", "icon": "<:60kgBench:1366393090989883394>", "rarity": "Common"},
    {"exercise": "bench", "description": "Earned for achieving a 40kg bench",  "threshold": 70,  "badge_name": "Intermediate Bench", "icon": "<:70kgBench:1366393152008617985>", "rarity": "Rare"},
    {"exercise": "bench", "description": "Earned for achieving a 80kg bench",  "threshold": 80,  "badge_name": "Advanced Bench", "icon": "<:80kgBench:1366393103560343562>", "rarity": "Rare"},
    {"exercise": "bench", "description": "Earned for achieving a 40kg bench",  "threshold": 90,  "badge_name": "Gymbro Bench", "icon": "<:90kgBench:1366393115686080522>", "rarity": "Epic"},
    {"exercise": "bench", "description": "Earned for achieving a 100kg bench", "threshold": 100, "badge_name": "Elite Bench", "icon": "<:100kgBench:1366393162603429918>", "rarity": "Epic"},
    {"exercise": "bench", "description": "Earned for achieving a 120kg bench", "threshold": 120, "badge_name": "Master Bench", "icon": "<:120kgBench:1366393127681916988>", "rarity": "Legendary"},
    
    {"exercise": "squats", "description": "Earned for achieving a 40kg squat",  "threshold": 40,  "badge_name": "Novice Squat", "icon": "<:40kgSquat:1366388967624147015>", "rarity": "Common"},
    {"exercise": "squats", "description": "Earned for achieving a 80kg squat",  "threshold": 80,  "badge_name": "Intermediate Squat", "icon": "<:80kgSquat:1366389017884496013>", "rarity": "Rare"},
    {"exercise": "squats", "description": "Earned for achieving a 100kg squat", "threshold": 100, "badge_name": "Advanced Squat", "icon": "<:100kgSquat:1366389049560137789>", "rarity": "Epic"},
    {"exercise": "squats", "description": "Earned for achieving a 120kg squat", "threshold": 120, "badge_name": "Glute Gladiator", "icon": "<:120kgSquat:1366389067402575893>", "rarity": "Legendary"},
    
    {"exercise": "deadlift", "description": "Earned for achieving a 60kg deadlift",  "threshold": 60,  "badge_name": "First Pull", "icon": "<:60kgDeadlift:1366388988562243664>", "rarity": "Common"},
    {"exercise": "deadlift", "description": "Earned for achieving a 100kg deadlift", "threshold": 100, "badge_name": "Grip Grinder", "icon": "<:100kgDeadlift:1366389033747615826>", "rarity": "Rare"},
    {"exercise": "deadlift", "description": "Earned for achieving a 140kg deadlift", "threshold": 140, "badge_name": "Titan of Tension", "icon": "<:140kgDeadlift:1366389081491247195>", "rarity": "Epic"},
    {"exercise": "deadlift", "description": "Earned for achieving a 180kg deadlift", "threshold": 180, "badge_name": "Barbell Behemoth", "icon": "<:180kgDeadlift:1366389095302959114>", "rarity": "Legendary"},
    
    {"exercise": "barbell-military-press-overhead-press", "description": "Earned for achieving a 20kg OHP", "threshold": 20, "badge_name": "Novice Presser", "icon": "<:20kgOverhead:1366388935009239060>", "rarity": "Common"},
    {"exercise": "barbell-military-press-overhead-press", "description": "Earned for achieving a 40kg OHP", "threshold": 40, "badge_name": "Shoulder Soldier", "icon": "<:40kgOverhead:1366388953753845862>", "rarity": "Rare"},
    {"exercise": "barbell-military-press-overhead-press", "description": "Earned for achieving a 60kg OHP", "threshold": 60, "badge_name": "Deltoid Destroyer", "icon": "TODO", "rarity": "Epic"},
    {"exercise": "barbell-military-press-overhead-press", "description": "Earned for achieving a 80kg OHP", "threshold": 80, "badge_name": "Overhead Overlord", "icon": "TODO", "rarity": "Legendary"},
    
    {"exercise": "pushups", "threshold": 500,   "badge_name": "Pushup Beginner", "description": "500 pushups done", "icon": "<:500pushupsbadge:1358166213775331509>", "rarity": "Common"},
    {"exercise": "pushups", "threshold": 1000,  "badge_name": "Pushup Challenger", "description": "1,000 pushups done", "icon": "<:100pushupsbadge:1358166112411324598>", "rarity": "Rare"},
    {"exercise": "pushups", "threshold": 5000,  "badge_name": "Pushup Warrior", "description": "5,000 pushups done", "icon": "<:5000pushupsbadge:1358166282230567052>", "rarity": "Epic"},
    {"exercise": "pushups", "threshold": 10000, "badge_name": "Pushup God", "description": "10,000 pushups done", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Legendary"},

    {"exercise": "muscleup", "threshold": 1, "badge_name": "Muscle-up", "description": "Unlock the muscle-up", "icon": "<:MuscleUpBadge:1366389160121733141>", "rarity": "Epic"},
    {"exercise": "lsit", "threshold": 1, "badge_name": "L-sit", "description": "Unlock the L-sit", "icon": "<:LSitBadge:1366389144632426566>", "rarity": "Common"},
    {"exercise": "human-flag", "threshold": 1, "badge_name": "Human flag", "description": "Unlock the human flag", "icon": "<:HumanFlagBadge:1366389129461502052>", "rarity": "Legendary"},
    {"exercise": "plank-knee-to-elbow", "threshold": 1, "badge_name": "Elbow lever", "description": "Unlock the elbow-lever", "icon": "<:ElbowLeverBadge:1366389110704574565>", "rarity": "Rare"},

]

async def badge_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[discord.app_commands.Choice[str]]:
    
    choices = []

    for badge in structured_badges:
        if current.lower() in badge["badge_name"].lower():
            choices.append(discord.app_commands.Choice(name=badge["badge_name"], value=badge["badge_name"]))

    return choices[:25]


def insert_missing_badges():
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            
            with con.cursor() as cursor:
                for badge in structured_badges:
                    badge_name = badge['badge_name']
                    description = badge['description']
                    icon_url = badge['icon']
                    rarity = badge['rarity']
                    
                    cursor.execute("SELECT id FROM badges WHERE name = %s", (badge_name,))
                    if not cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO badges (name, description, icon_url, rarity) VALUES (%s, %s, %s, %s)",
                            (badge_name, description, icon_url, rarity)
                        )
                        print(f"Inserted badge: {badge_name}")
                    else:
                        print(f"Badge already exists: {badge_name}")

    except Exception as err:
        print("Error inserting badges:", err)


async def grant_badge(user, badge_name, date_obj=validateDate(None)):
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:

            with con.cursor() as cursor:
                # 1. Fetch the list of badges the user has already earned
                owned_badges = await get_user_badges(user.id)
                owned_badges = [badge[1] for badge in owned_badges]

                # If the user's PR is greater than or equal to the badge threshold
                if badge_name not in owned_badges:

                    # 3. Get correct badge id
                    cursor.execute("SELECT id FROM badges WHERE name = %s", (badge_name,))
                    badge_id = cursor.fetchone()

                    # 4. Award the badge by inserting it into the database
                    cursor.execute("""
                        INSERT INTO user_badges (user_id, badge_id, earned_at)
                        VALUES (%s, %s, %s)
                    """, (str(user.id), badge_id[0], date_obj))
                    con.commit()

                    return f"Gave user the {badge_name} badge!"

                else:
                    return "User already has this badge"

    except Exception as e:
        print(f"[Badge Check Error] {e}")


async def check_for_badge(user, exercise, pr, date_obj, interaction):
    """Check if a user has earned a badge based on their PR and exercise type."""
    
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:

            with con.cursor() as cursor:
                # 1. Fetch the list of badges the user has already earned
                owned_badges = await get_user_badges(user.id)
                owned_badges = [badge[1] for badge in owned_badges]

                # 2. Check if the badge is available for the given exercise and PR
                for badge in structured_badges:
                    # Ensure the badge matches the exercise type
                    if badge['exercise'].lower() != exercise.lower():
                        continue

                    if badge['exercise'] == "pushups":
                        pushups_done = await db_manager.get_pushups_done(user.id)
                        should_trigger = pushups_done >= badge['threshold']
                    else:
                        should_trigger = pr >= badge['threshold']

                    # If the user's PR is greater than or equal to the badge threshold
                    if should_trigger and badge['badge_name'] not in owned_badges:

                        # 3. Get correct badge id
                        cursor.execute("SELECT id FROM badges WHERE name = %s", (badge['badge_name'],))
                        badge_id = cursor.fetchone()

                        # 4. Award the badge by inserting it into the database
                        cursor.execute("""
                            INSERT INTO user_badges (user_id, badge_id, earned_at)
                            VALUES (%s, %s, %s)
                        """, (str(user.id), badge_id[0], date_obj))
                        con.commit()

                        # 5. Send the embed to the user with the badge info
                        embed = embeds.DefaultEmbed(
                            title=f"{badge['icon']} You've earned a badge!",
                            description=f"**{user.mention}**, you just unlocked the **{badge['badge_name']}** - {badge['description']}\nThis is a badge of *{badge['rarity']}* rarity.",
                        )
                        embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{badge['icon'].split(':')[2][:-1]}.png")

                        if interaction.response.is_done():
                            await interaction.followup.send(embed=embed)
                        else:
                            await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(f"[Badge Check Error] {e}")


badge_lookup = {badge["badge_name"]: badge for badge in structured_badges}

async def get_user_badges(user_id: int, return_all=True) -> list:
    """Returns a list of badges (earned_at, name, description, icon_url, rarity) earned by a given user."""
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:

            with con.cursor() as cursor:
                cursor.execute("""
                    SELECT ub.earned_at, b.name, b.description, b.icon_url, b.rarity
                    FROM user_badges ub
                    JOIN badges b ON ub.badge_id = b.id
                    WHERE ub.user_id = %s
                    ORDER BY b.rarity DESC
                """, (str(user_id),))
                badges = cursor.fetchall()

                if return_all:
                    return badges
                
                best_per_exercise = {}
                for earned_at, name, description, icon_url, rarity in badges:
                    badge_data = badge_lookup[name]
                    exercise = badge_data["exercise"]
                    threshold = badge_data.get("threshold")

                    current = best_per_exercise.get(exercise)
                    if not current or threshold > current["threshold"]:
                        best_per_exercise[exercise] = {
                            "earned_at": earned_at,
                            "name": name,
                            "description": description,
                            "icon_url": icon_url,
                            "rarity": rarity,
                            "threshold": threshold
                        }

                return [
                    (b["earned_at"], b["name"], b["description"], b["icon_url"], b["rarity"])
                    for b in best_per_exercise.values()
                ]

    
    except Exception as e:
        print(f"[Get User Badges Error] {e}")
        return []
    
    
def add_badges_field_to_embed(embed, badges, owned_badges=[], add_timestamp=False):
    categories = {
        "Common": [],
        "Rare": [],
        "Epic": [],
        "Legendary": [],
    }

    rarity_emojis = {
        "Common": "⭐",
        "Rare": "💪",
        "Epic": "⚡",
        "Legendary": "💎",
    }

    owned_badges_titles = [badge[1] for badge in owned_badges]

    for idOrTimestamp, name, desc, icon_url, rarity in badges:
        category = categories.get(rarity, [])
        if add_timestamp:
            category.append(f"{icon_url} **{name}** - Earned at {getDiscordTimeStamp(idOrTimestamp, full_time=False)} - {desc}")
        else:
            
            if name in owned_badges_titles:
                category.append(f"{icon_url} **{name}*** - {desc}")
            else:
                category.append(f"{icon_url} **{name}** - {desc}")

    for rarity, badge_list in categories.items():
        if badge_list:
            emoji = rarity_emojis.get(rarity)
            embed.add_field(name=f"{emoji} {rarity}", value="\n".join(badge_list), inline=False)

    if owned_badges:
        embed.set_footer(text="* Owned badges")

    return embed