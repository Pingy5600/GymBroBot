import os
import psycopg2
from typing import Optional
from datetime import datetime, timedelta

""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

### PR ###

async def add_pr(user_id: str, exercise:str, weight:float, lifted_at=None):
    try:
        with psycopg2.connect(
            host='gymbrobot_postgres', dbname='pg_gymbrobot', user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pr(user_id, exercise, weight, lifted_at) VALUES (%s, %s, %s, %s)",
                    (str(user_id), str(exercise), float(weight), lifted_at)
                )
                con.commit()
                return (True, None)
            
    except Exception as err:
        print(err)
        return (False, err)


async def get_prs_from_user(user_id: str, exercise: str) -> list:
    try:
        with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT exercise, weight, lifted_at FROM pr WHERE user_id=%s AND exercise=%s ORDER BY lifted_at DESC", (user_id, exercise,)
                )
                return cursor.fetchall()

    except Exception as err:
        return [-1, err]
    

async def getMaxOfUserWithExercise(user_id: str, exercise: str):
    try:
        with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT weight, lifted_at FROM pr WHERE user_id=%s AND exercise=%s ORDER BY weight DESC LIMIT 1", (user_id, exercise,)
                )
                return (True, cursor.fetchone())

    except Exception as err:
        return [False, err]
    

async def getPositionOfUserWithExercise(user_id: str, exercise: str):
    try:
        with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            with con.cursor() as cursor:
                # Fetch the user's max lift for the given exercise
                cursor.execute(
                    """
                    SELECT weight, lifted_at 
                    FROM pr 
                    WHERE user_id = %s AND exercise = %s 
                    ORDER BY weight DESC 
                    LIMIT 1
                    """,
                    (user_id, exercise,)
                )
                user_lift = cursor.fetchone()

                if not user_lift:
                    # If the user has no lifts for the exercise
                    return (False, None)

                user_max_weight = user_lift[0]

                # Calculate the user's rank by considering only the heaviest lift of each user
                cursor.execute(
                    """
                    SELECT COUNT(*) + 1
                    FROM (
                        SELECT MAX(weight) AS max_weight
                        FROM pr
                        WHERE exercise = %s
                        GROUP BY user_id
                    ) AS grouped_lifts
                    WHERE max_weight > %s
                    """,
                    (exercise, user_max_weight)
                )
                rank = cursor.fetchone()[0]

                # Return the rank and the user's max lift details
                return (True, rank)

    except Exception as err:
        return (False, err)


async def getExerciseProgressionRate(user_id, exercise: str):
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT weight, lifted_at 
                    FROM pr 
                    WHERE user_id = %s AND exercise = %s 
                    ORDER BY lifted_at ASC
                    """, 
                    (user_id, exercise, )
                )
                lifts = cursor.fetchall()

                if len(lifts) < 2:
                    return (False, "Not enough data to calculate progression rate.")

                six_months_ago = datetime.now() - timedelta(days=6 * 30)  # Approximation for 6 months

                # Filter lifts to start from 6 months ago or the earliest record
                relevant_lifts = [lift for lift in lifts if lift[1] <= six_months_ago]

                # If no lifts in the last 6 months, use the first lift
                if not relevant_lifts:
                    relevant_lifts = lifts

                # Extract start and end points
                W_start, T_start = relevant_lifts[0]
                W_end, T_end = relevant_lifts[-1]

                # Calculate time difference in weeks
                time_diff_weeks = (T_end - T_start).days / 7

                if time_diff_weeks == 0:  # Avoid division by zero
                    return (False, "Not enough time between lifts to calculate progression rate.")

                # Calculate average weekly increase
                progression_rate = float(W_end - W_start) / time_diff_weeks

                return (True, round(progression_rate, 2))  # Rounded to 2 decimal places

    except Exception as err:
        return (False, str(err))
    
async def getClosestUsersWithExercise(user_id: str, exercise: str):
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                # Haal het hoogste PR per gebruiker voor de opgegeven oefening
                cursor.execute(
                    """
                    SELECT user_id, MAX(weight) AS weight
                    FROM pr 
                    WHERE exercise = %s
                    GROUP BY user_id
                    ORDER BY weight ASC
                    """,
                    (exercise,)
                )
                users_prs = cursor.fetchall()

                if not users_prs:
                    return [False, "No PRs found for the exercise"]

                # Maak een lijst met gebruikers en hun PR's
                sorted_users = users_prs  # De lijst is al gesorteerd van klein naar groot

                # Zoek de opgegeven gebruiker in de lijst
                user_position = None
                for idx, (user, weight) in enumerate(sorted_users):
                    if user == user_id:
                        user_position = idx
                        break

                if user_position is None:
                    return [False, "User's PR not found in the list"]

                # Haal de gebruiker boven en onder de opgegeven gebruiker
                user_below = sorted_users[user_position - 1] if user_position > 0 else None
                user_above = sorted_users[user_position + 1] if user_position < len(sorted_users) - 1 else None

                # Haal de namen en gewichten van de dichtstbijzijnde gebruikers
                user_below_info = f"{user_below[0]} ({user_below[1]} kg)" if user_below else "No one below"
                user_above_info = f"{user_above[0]} ({user_above[1]} kg)" if user_above else "No one above"

                return [True, {"user_below": user_below_info, "user_above": user_above_info}]

    except Exception as err:
        return [False, err]

    

### SCHEMA ###

async def update_schema(
    monday: Optional[str] = None,
    tuesday: Optional[str] = None,
    wednesday: Optional[str] = None,
    thursday: Optional[str] = None,
    friday: Optional[str] = None,
    saturday: Optional[str] = None,
    sunday: Optional[str] = None
):
    alreadyExists = await schema_exists()
    if alreadyExists is None: return (False, 'Cannot determine if schema already exists')

    fields_to_update = {
        "monday": monday,
        "tuesday": tuesday,
        "wednesday": wednesday,
        "thursday": thursday,
        "friday": friday,
        "saturday": saturday,
        "sunday": sunday,
    }
    update_clauses = [f"{field} = %s" for field, value in fields_to_update.items() if value is not None]
    update_values = [value for value in fields_to_update.values() if value is not None]

    if not update_clauses:
        return (False, "No fields to update")
    
    update_query = f"UPDATE schema SET {', '.join(update_clauses)} WHERE id = 1"

    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    # Update only the specified fields
                    cursor.execute(update_query, update_values)
                else:
                    # Insert a new row with all the values (replacing None with default empty strings)
                    insert_query = """
                    INSERT INTO schema (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        monday or "", tuesday or "", wednesday or "",
                        thursday or "", friday or "", saturday or "", sunday or ""
                    ))

                con.commit()
                return (True, None)
                
        except Exception as err:
            return (False, err)
     
        
async def get_schema():
    with psycopg2.connect( host=os.environ.get("POSTGRES_HOST"), dbname=os.environ.get("POSTGRES_DB"), user=os.environ.get("POSTGRES_USER"), password=os.environ.get("POSTGRES_PASSWORD"),
    ) as con:
        try:
            with con.cursor() as cursor:
                # Query to retrieve the schema
                cursor.execute("SELECT monday, tuesday, wednesday, thursday, friday, saturday, sunday FROM schema WHERE id = 1")
                row = cursor.fetchone()

                if row:
                    schema = {
                        "Monday": row[0],
                        "Tuesday": row[1],
                        "Wednesday": row[2],
                        "Thursday": row[3],
                        "Friday": row[4],
                        "Saturday": row[5],
                        "Sunday": row[6],
                    }
                    return (True, schema)
                else:
                    return (False, "Schema not found")
        except Exception as err:
            return (False, str(err))
        

async def schema_exists():
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM schema",
                )
                result = cursor.fetchall()
                return len(result) > 0
                
        except Exception as err:
            return None
        

async def delete_pr(user_id: str, exercise: str, lifted_at: datetime) -> tuple:
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM pr WHERE user_id=%s AND exercise=%s AND lifted_at=%s",
                    (user_id, exercise, lifted_at)
                )
                con.commit()
                return (True, None)
            
        except Exception as err:
            return (False, err)

