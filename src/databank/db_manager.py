import os
import psycopg2

""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

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
