import discord
import logging
import os
import asyncio
import platform
from dotenv import load_dotenv
from discord.ext.commands import AutoShardedBot
import psycopg2
import time

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
    time.sleep(10)
    with psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'), dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD')
    ) as con:
        
        with con.cursor() as cursor:

            with open(
                f"{os.path.realpath(os.path.dirname(__file__))}/database/schema.sql"
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


    cmds = await bot.tree.sync()
    bot.save_ids(cmds)

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


init_db()
asyncio.run(load_cogs())
bot.run(os.environ.get("BOT_TOKEN"))