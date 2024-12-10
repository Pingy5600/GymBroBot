import os
import psycopg2
from typing import Optional

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

