import asyncio
import logging
import os
import platform
import random
from datetime import datetime, timedelta

import discord
import psycopg2
from discord.ext import tasks
from discord.ext.commands import AutoShardedBot
from dotenv import load_dotenv

import embeds
from helpers import db_manager

load_dotenv()

intents = discord.Intents.default()

bot = AutoShardedBot(command_prefix='',
    intents=intents,
    help_command=None,)

bot.loaded = set()
bot.unloaded = set()

def save_ids_func(cmds):
    """Saves the ids of commands

    Args:
        cmds (Command)
    """
    for cmd in cmds:
        try:
            if cmd.guild_id is None:  # it's a global slash command
                bot.logger.info(f"Synced globally")
                bot.tree._global_commands[cmd.name].id = cmd.id
            else:  # it's a guild specific command
                bot.logger.info(f"Synced guild")
                bot.tree._guild_commands[cmd.guild_id][cmd.name].id = cmd.id
        except:
            pass

bot.save_ids = save_ids_func


class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
bot.logger = logger


def init_db():
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        with con.cursor() as cursor:

            with open(
                f"{os.path.realpath(os.path.dirname(__file__))}/databank/schema.sql"
            ) as file:
                cursor.execute(file.read())

    bot.logger.info(f"initializing db")


@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info("-------------------")

    try:
        check_remindme.start()
        change_status_loop.start()

    except Exception as e:
        bot.logger.warning(e)

    cmds = await bot.tree.sync()
    bot.save_ids(cmds)


@tasks.loop(seconds=30)
async def check_remindme():
    bot.logger.info("Running reminder check...")

    # Haal reminders op uit de database
    reminders = await db_manager.get_reminders()

    # Controleer of er reminders zijn
    if not reminders:
        bot.logger.info("No reminders to process.")  # Geen reminders gevonden
        return
    elif reminders[0] == -1:
        bot.logger.warning(f"Could not fetch reminders: {reminders[1]}")
        return

    # Verwerk reminders
    for reminder in reminders:
        id, user_id, subject, time = tuple(reminder)

        # Controleer of de reminder-tijd is bereikt of overschreden
        if time <= datetime.now() + timedelta(hours=1):  # Compensatie voor UTC+1
            try:
                # Stuur een bericht naar de gebruiker
                user = await bot.fetch_user(int(user_id))
                embed = embeds.DefaultEmbed(
                    "⏰ Reminder!",
                    f"```{subject}```",
                )
                await user.send(embed=embed)

                # Verplaats de reminder met 5 minuten vooruit
                new_time = time + timedelta(days=1)
                succes = await db_manager.update_reminder_time(id, new_time)
                if succes:
                    bot.logger.info(f"Successfully rescheduled reminder ({subject}) to {new_time}")
                else:
                    bot.logger.warning(f"Failed to update reminder with ID {id} in database")

            except discord.Forbidden:
                bot.logger.warning(f"Cannot send DM to user {user_id}. They might have DMs disabled.")
            except Exception as e:
                bot.logger.error(f"Failed to send reminder: {e}")


async def load_cogs() -> None:
    """
    The code in this function is executed whenever the bot will start.
    """
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                bot.logger.info(f"Loaded extension '{extension}'")
                bot.loaded.add(extension)

            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(f"Failed to load extension {extension}\n{exception}")
                bot.unloaded.add(extension)


@tasks.loop(minutes=1.0)
async def change_status_loop() -> None:
    """
    Setup the game status task of the bot.
    """

    statuses = [
        f"🦾 Lifting heavy!",
        f"💪 Getting stronger!",
        f"🏋️‍♂️ Powerlifting!",
    ]

    picked_status = random.choice(statuses)
    await bot.change_presence(activity=discord.CustomActivity(name=picked_status))


init_db()
asyncio.run(load_cogs())
bot.run(os.environ.get("BOT_TOKEN"))