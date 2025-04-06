import psycopg2
import os
import embeds
from .__init__ import getDiscordTimeStamp

#TODO icons
structured_badges = [
    {"exercise": "bench", "description": "Earned for achieving a 40kg bench", "threshold": 40, "badge_name": "Novice Bench", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Common"},
    {"exercise": "bench", "description": "Earned for achieving a 60kg bench", "threshold": 60, "badge_name": "Intermediate Bench", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Common"},
    {"exercise": "bench", "description": "Earned for achieving a 80kg bench", "threshold": 80, "badge_name": "Advanced Bench", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Rare"},
    {"exercise": "bench", "description": "Earned for achieving a 100kg bench", "threshold": 100, "badge_name": "Elite Bench", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Epic"},
    {"exercise": "bench", "description": "Earned for achieving a 120kg bench", "threshold": 120, "badge_name": "Master Bench", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Legendary"},
    {"exercise": "squats", "description": "Earned for achieving a 40kg squat", "threshold": 40, "badge_name": "Novice Squat", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Common"},
    {"exercise": "squats", "description": "Earned for achieving a 80kg squat", "threshold": 80, "badge_name": "Intermediate Squat", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Rare"},
    {"exercise": "squats", "description": "Earned for achieving a 100kg squat", "threshold": 100, "badge_name": "Advanced Squat", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Epic"},
    {"exercise": "squats", "description": "Earned for achieving a 120kg squat", "threshold": 120, "badge_name": "Glute Gladiator", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Legendary"},
    {"exercise": "deadlift", "description": "Earned for achieving a 60kg deadlift", "threshold": 60, "badge_name": "First Pull", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Common"},
    {"exercise": "deadlift", "description": "Earned for achieving a 100kg deadlift", "threshold": 100, "badge_name": "Grip Grinder", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Rare"},
    {"exercise": "deadlift", "description": "Earned for achieving a 140kg deadlift", "threshold": 140, "badge_name": "Titan of Tension", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Epic"},
    {"exercise": "deadlift", "description": "Earned for achieving a 180kg deadlift", "threshold": 180, "badge_name": "Barbell Behemoth", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Legendary"},
    {"exercise": "barbell-military-press-overhead-press", "description": "Earned for achieving a 20kg OHP", "threshold": 20, "badge_name": "Novice Presser", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Common"},
    {"exercise": "barbell-military-press-overhead-press", "description": "Earned for achieving a 40kg OHP", "threshold": 40, "badge_name": "Shoulder Soldier", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Rare"},
    {"exercise": "barbell-military-press-overhead-press", "description": "Earned for achieving a 60kg OHP", "threshold": 60, "badge_name": "Deltoid Destroyer", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Epic"},
    {"exercise": "barbell-military-press-overhead-press", "description": "Earned for achieving a 80kg OHP", "threshold": 80, "badge_name": "Overhead Overlord", "icon": "<:10000pushupsbadge:1358166534551507106>", "rarity": "Legendary"},
        
    # TODO: pushups badges
]

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

                    # If the user's PR is greater than or equal to the badge threshold
                    if pr >= badge['threshold'] and badge['badge_name'] not in owned_badges:

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


async def get_user_badges(user_id: int) -> list:
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
                return cursor.fetchall()
    
    except Exception as e:
        print(f"[Get User Badges Error] {e}")
        return []
    
    
def add_badges_field_to_embed(embed, badges, add_timestamp=False):
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

    for idOrTimestamp, name, desc, icon_url, rarity in badges:
        category = categories.get(rarity, [])
        if add_timestamp:
            category.append(f"{icon_url} **{name}** - Earned at {getDiscordTimeStamp(idOrTimestamp, full_time=False)} - {desc}")
        else:
            category.append(f"{icon_url} **{name}** - {desc}")

    for rarity, badge_list in categories.items():
        if badge_list:
            emoji = rarity_emojis.get(rarity)
            embed.add_field(name=f"{emoji} {rarity}", value="\n".join(badge_list), inline=False)

    return embed