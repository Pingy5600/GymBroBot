import os
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import psycopg2
from psycopg2.extras import RealDictCursor

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
                    "SELECT id, exercise, weight, lifted_at FROM pr WHERE user_id=%s AND exercise=%s ORDER BY lifted_at DESC", (user_id, exercise,)
                )
                return cursor.fetchall()

    except Exception as err:
        return [-1, err]
    

async def delete_pr(id) -> tuple:
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM pr WHERE id=%s",
                    (id, )
                )
                con.commit()
                return (True, None)
            
        except Exception as err:
            return (False, err)


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
    

async def get_top_prs(exercise: str) -> list:
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                # Query om top PR's per gebruiker op te halen inclusief timestamp van de PR
                cursor.execute(
                    """
                    SELECT user_id, MAX(weight) AS max_weight, MAX(lifted_at) AS last_lifted
                    FROM pr 
                    WHERE exercise = %s 
                    GROUP BY user_id 
                    ORDER BY max_weight DESC
                    """,
                    (exercise,)
                )
                return cursor.fetchall()
    except Exception as err:
        raise RuntimeError(f"Database error: {err}")
    

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
        with psycopg2.connect(host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
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
        with psycopg2.connect(host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
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
                    return (False, "No PRs found for the exercise")

                # Zoek de opgegeven gebruiker in de lijst
                user_position = None
                for idx, (user, weight) in enumerate(users_prs):
                    if user == user_id:
                        user_position = idx
                        break

                if user_position is None:
                    return (False, "User's PR not found in the list")

                # Haal de gebruiker boven en onder de opgegeven gebruiker
                user_below = users_prs[user_position - 1] if user_position > 0 else None
                user_above = users_prs[user_position + 1] if user_position < len(users_prs) - 1 else None

                return (True, (user_below,  user_above))

    except Exception as err:
        return (False, err)


### REPS ###

async def add_reps(user_id: str, exercise: str, weight: float, reps: int, lifted_at=None):
    try:
        with psycopg2.connect(host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO reps (user_id, exercise, weight, reps, lifted_at)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (str(user_id), str(exercise), float(weight), int(reps), lifted_at)
                )
                con.commit()
                return [True, None]
    except Exception as err:
        return [False, err]


async def get_prs_with_reps(user_id: str, exercise: str):
    try:
        with psycopg2.connect(host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT exercise, weight, reps, lifted_at
                    FROM reps
                    WHERE user_id = %s AND exercise = %s
                    ORDER BY lifted_at DESC
                    """,
                    (user_id, exercise)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [False, err]
    

async def delete_reps(user_id: str, exercise: str, weight: float, lifted_at: str):
    try:
        with psycopg2.connect(host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM reps
                    WHERE user_id = %s AND exercise = %s AND weight = %s AND lifted_at = %s
                    """,
                    (user_id, exercise, weight, lifted_at)
                )
                con.commit()
                
                # Check if any rows were affected (if not, return an error message)
                if cursor.rowcount == 0:
                    return [False, "No matching reps found to delete."]
                
                return [True, None]
            
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


### REMINDERS ###

async def set_reminder(user_id, subject, time):
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        try:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO reminders (user_id, subject, time) VALUES (%s, %s, %s)",
                    (str(user_id), subject, time)
                )
                    
                con.commit()
                return True
                
        except Exception as err:
            print(err)
            return False
    

async def get_reminders() -> list:
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT id, user_id, subject, time FROM reminders"
                )
                return cursor.fetchall()
            
        except Exception as err:
            return [-1, err]
    

async def update_reminder_time(id, new_time):
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "UPDATE reminders SET time = %s WHERE id = %s",
                    (new_time.strftime('%Y-%m-%d %H:%M:%S'), id)
                )
                con.commit()
                return True
        except Exception as err:
            print(err)
            return False


async def get_reminders_by_user(user_id: str) -> list:
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT id, subject, time FROM reminders WHERE user_id = %s ORDER BY time ASC",
                    (user_id,)
                )
                reminders = cursor.fetchall()
                return [{"id": r[0], "subject": r[1], "time": r[2]} for r in reminders]
        except Exception as err:
            return [-1, err]


async def delete_reminder(reminder_id: int) -> bool:
    with psycopg2.connect(host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM reminders WHERE id = %s",
                    (reminder_id,)
                )
                con.commit()
                return cursor.rowcount > 0  # True if a row was deleted, False otherwise
        except Exception as err:
            print(f"Error deleting reminder: {err}")
            return False

### GAMBLE ###

async def increment_ban_gamble_wins(user_id):

    alreadyExists = await is_in_ban_gamble(user_id)

    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    cursor.execute(
                        "UPDATE bangamble SET current_win_streak = current_win_streak + 1 WHERE user_id=%s;UPDATE bangamble SET total_wins = total_wins + 1 WHERE user_id=%s",
                        (str(user_id), str(user_id),)
                    )   
                else:
                    cursor.execute(
                        "INSERT INTO bangamble(user_id, current_win_streak, total_wins) VALUES (%s, %s, %s)",
                        (str(user_id), 1, 1)
                    )

                cursor.commit()
                return True
                
        except:
            return False


async def increment_ban_gamble_losses(user_id):

    alreadyExists = await is_in_ban_gamble(user_id)

    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    cursor.execute(
                        "UPDATE bangamble SET current_loss_streak = current_loss_streak + 1 WHERE user_id=%s;UPDATE bangamble SET total_losses = total_losses + 1 WHERE user_id=%s",
                        (str(user_id), str(user_id))
                    )   
                else:
                    cursor.execute(
                        "INSERT INTO bangamble(user_id, current_loss_streak, total_losses) VALUES (%s, %s, %s)",
                        (str(user_id), 1, 1,)
                    )

                cursor.commit()

                return True
                
        except:
            return False
    

async def is_in_ban_gamble(user_id) -> bool:

    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM bangamble WHERE user_id=%s", (str(user_id),)
                )
                result = cursor.fetchall()
                return len(result) > 0
        # Als er iets misgaat, zeggen we dat user nog niet in ban gamble zit
        except:
            return False
        

async def reset_ban_gamble_win_streak(user_id):

    alreadyExists = await is_in_ban_gamble(user_id)

    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    cursor.execute(
                        "UPDATE bangamble SET current_win_streak = 0 WHERE user_id=%s",
                        (str(user_id),)
                    )   
                else:
                    cursor.execute(
                        "INSERT INTO bangamble(user_id, current_win_streak) VALUES (%s, %s)",
                        (str(user_id), 0,)
                    )

                cursor.commit()
                return True
                
        except:
            return False
        

async def reset_ban_gamble_loss_streak(user_id):

    alreadyExists = await is_in_ban_gamble(user_id)

    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    cursor.execute(
                        "UPDATE bangamble SET current_loss_streak = 0 WHERE user_id=%s",
                        (str(user_id),)
                    )   
                else:
                    cursor.execute(
                        "INSERT INTO bangamble(user_id, current_loss_streak) VALUES (%s, %s)",
                        (str(user_id), 0,)
                    )

                cursor.commit()
                return True
                
        except:
            return False


async def check_ban_gamble_win_streak(user_id):
    # get loser current streak
    current_win_streak = await get_current_win_streak(user_id)
    if current_win_streak[0] == -1:
        return False
    current_win_streak = current_win_streak[0][0]
    
    # get loser highest streak
    highest_win_streak = await get_highest_win_streak(user_id)
    if highest_win_streak[0] == -1:
        return False
    highest_win_streak = highest_win_streak[0][0]

    # do nothing if current streak is not higher than highest streak
    if current_win_streak < highest_win_streak:
        return False

    # update the highest streak
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "UPDATE bangamble SET highest_win_streak = %s WHERE user_id=%s",
                    (current_win_streak, str(user_id),)
                )   
                
                cursor.commit()
                return True
                
        except:
            return False


async def check_ban_gamble_loss_streak(user_id):
    # get loser current streak
    current_loss_streak = await get_current_loss_streak(user_id)
    if current_loss_streak[0] == -1:
        return False
    current_loss_streak = current_loss_streak[0][0]
    
    # get loser highest streak
    highest_loss_streak = await get_highest_loss_streak(user_id)
    if highest_loss_streak[0] == -1:
        return False
    highest_loss_streak = highest_loss_streak[0][0]

    # do nothing if current streak is not higher than highest streak
    if current_loss_streak < highest_loss_streak:
        return False
    
    # update the highest streak
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "UPDATE bangamble SET highest_loss_streak = %s WHERE user_id=%s",
                    (current_loss_streak, str(user_id),)
                )   
                
                cursor.commit()
                return True
                
        except:
            return False
        

async def get_current_win_streak(user_id) -> list:
    try:
        with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT current_win_streak FROM bangamble WHERE user_id=%s ", 
                    (str(user_id),)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]
    

async def get_highest_win_streak(user_id) -> list:
    try:
        with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT highest_win_streak FROM bangamble WHERE user_id=%s ", 
                    (str(user_id),)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]
    

async def get_current_loss_streak(user_id) -> list:
    try:
        with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT current_loss_streak FROM bangamble WHERE user_id=%s ", 
                    (str(user_id),)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]
    

async def get_highest_loss_streak(user_id) -> list:
    try:
        with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT highest_loss_streak FROM bangamble WHERE user_id=%s ", 
                    (str(user_id),)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]
    

async def get_ban_total_wins(user_id) -> list:
    try:
        with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT total_wins FROM bangamble WHERE user_id=%s ", 
                    (str(user_id),)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]


async def get_ban_total_losses(user_id) -> list:
    try:
        with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT total_losses FROM bangamble WHERE user_id=%s ", 
                    (str(user_id),)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]


async def get_pushups(user_id: int):
    try:
        with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
            
            with con.cursor() as cursor:
                cursor.execute("SELECT count FROM pushups WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                return result[0] if result else 0
            
    except Exception as e:
        return 0


async def get_pushups_done(user_id: int):
    """Haalt het totaal aantal voltooide pushups op."""
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'), 
            dbname=os.environ.get('POSTGRES_DB'), 
            user=os.environ.get('POSTGRES_USER'), 
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            
            with con.cursor() as cursor:
                cursor.execute("SELECT count FROM pushups_done WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                return result[0] if result else 0
            
    except Exception:
        return 0


async def add_pushup_event(user_id: int, amount: int, reason: str = "") -> bool:
    """Voegt een push-up event toe of verlaagt de push-ups afhankelijk van de hoeveelheid (positief of negatief)."""
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                # Log het event
                cursor.execute(
                    "INSERT INTO pushup_event (user_id, amount, reason) VALUES (%s, %s, %s)",
                    (str(user_id), amount, reason)
                )

                # Pas de count aan (laat toe om onder 0 te gaan)
                cursor.execute(
                    """
                    UPDATE pushups
                    SET count = count + %s
                    WHERE user_id = %s
                    RETURNING count
                    """,
                    (amount, user_id)
                )
                result = cursor.fetchone()
                if result is None:
                    raise Exception("User ID bestaat niet in de pushups tabel")

                # Als het een pushup 'done' actie is (negatief)
                if amount < 0:
                    cursor.execute(
                        """
                        INSERT INTO pushups_done (user_id, count)
                        VALUES (%s, %s)
                        ON CONFLICT (user_id)
                        DO UPDATE SET count = pushups_done.count + EXCLUDED.count
                        """,
                        (user_id, abs(amount))
                    )

                    new_count = result[0]

                    # Reset Double or Nothing status als count nu 0 is
                    if new_count == 0:
                        cursor.execute(
                            "UPDATE pushups SET double_or_nothing_used = FALSE WHERE user_id = %s",
                            (user_id,)
                        )

                con.commit()

        return True
    except Exception as e:
        print(f"Error adding pushup event: {e}")
        return False


async def add_pushup_done(user_id: int, amount: int, reason: str = "") -> bool:
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                # Verhoog pushups_done zonder een event te loggen
                cursor.execute(
                    """
                    INSERT INTO pushups_done (user_id, count)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id)
                    DO UPDATE SET count = pushups_done.count + EXCLUDED.count
                    """,
                    (user_id, amount)
                )

                con.commit()

        return True
    except Exception as e:
        print(f"Error adding pushup_done: {e}")
        return False


async def get_all_pushup_events(user_id: int) -> List[Tuple[int, str, str]]:
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT amount, reason, date FROM pushup_event WHERE user_id = %s ORDER BY date DESC",
                    (str(user_id),)
                )
                # Fetch all results
                events = cursor.fetchall()
                
                return events
    except Exception as e:
        print(f"Error fetching pushup events: {e}")
        return []


async def has_pushups_in_reserve(user_id: int) -> bool:
    """Controleer of de gebruiker pushups in reserve heeft (d.w.z. count < 0)."""
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                cursor.execute("SELECT count FROM pushups WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                return result[0] < 0 if result else False
    except Exception:
        return False


async def get_pending_pushups(user_id: int) -> int:
    """Geeft het aantal pushups dat de gebruiker nog moet doen voordat ze weer Double or Nothing mogen gebruiken."""
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                cursor.execute("SELECT pushups_to_clear FROM pushups WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                return result[0] if result else 0
    except Exception as e:
        print(f"Error getting pending pushups: {e}")
        return 0


async def set_pending_pushups(user_id: int, amount: int):
    try:
        with psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        ) as con:
            with con.cursor() as cursor:
                if amount == 0:
                    # Zet de pending pushups naar 0
                    cursor.execute(
                        "UPDATE pushups SET pushups_to_clear = 0 WHERE user_id = %s",
                        (user_id,)
                    )
                else:
                    # Haal de huidige waarde van pushups_to_clear op
                    cursor.execute("SELECT pushups_to_clear FROM pushups WHERE user_id = %s", (user_id,))
                    current_pending = cursor.fetchone()[0]

                    # Bereken de nieuwe waarde (controleer of deze niet negatief wordt)
                    new_pending = current_pending + amount
                    if new_pending < 0:
                        new_pending = 0  # Zet het naar 0 als het negatief is

                    # Werk de waarde van pushups_to_clear bij
                    cursor.execute(
                        "UPDATE pushups SET pushups_to_clear = %s WHERE user_id = %s",
                        (new_pending, user_id)
                    )
                con.commit()
    except Exception as e:
        print(f"Fout bij het instellen van pending pushups: {e}")