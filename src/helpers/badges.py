import psycopg2
import os

BADGES = [
    # Bench Press Badges
    ("Novice Bench", "Bench 40kg", "<:500_pushups_badge:1356324823672033580>", "Common"),
    ("Intermediate Bench", "Bench 60kg", "<:500_pushups_badge:1356324823672033580>", "Common"),
    ("Advanced Bench", "Bench 80kg", "<:500_pushups_badge:1356324823672033580>", "Rare"),
    ("Elite Bench", "Bench 100kg", "<:500_pushups_badge:1356324823672033580>", "Epic"),
    ("Master Bench", "Bench 120kg", "<:500_pushups_badge:1356324823672033580>", "Legendary",),

    # Pushup Mastery
    ("Pushup Beginner", "500 pushups done", "<:500_pushups_badge:1356324823672033580>", "Common"),
    ("Pushup Challenger", "1,000 pushups done", "<:500_pushups_badge:1356324823672033580>", "Common"),
    ("Pushup Warrior", "5,000 pushups done", "<:500_pushups_badge:1356324823672033580>", "Rare"),
    ("Pushup God", "10,000 pushups done", "<:500_pushups_badge:1356324823672033580>", "Legendary"),
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
                for name, description, icon_url, rarity in BADGES:
                    cursor.execute("SELECT id FROM badges WHERE name = %s", (name,))
                    if not cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO badges (name, description, icon_url, rarity) VALUES (%s, %s, %s, %s)",
                            (name, description, icon_url, rarity)
                        )
                        print(f"Inserted badge: {name}")
                    else:
                        print(f"Badge already exists: {name}")

    except Exception as err:
        print("Error inserting badges:", err)
