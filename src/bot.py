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
import exceptions
from helpers import db_manager
from cogs.gamble import ResetCooldownView
from helpers.badges import insert_missing_badges

load_dotenv()

intents = discord.Intents.default()

bot = AutoShardedBot(command_prefix='',
    intents=intents,
    help_command=None,)

# Keep track of which cogs are loaded and unloaded
bot.loaded = set()
bot.unloaded = set()

bot.command_ids = {}

def save_ids_func(cmds):
    """Saves the mentions of commands

    Args:
        cmds (Command)
    """
    for cmd in cmds:
        bot.command_ids[cmd.name] = cmd.id


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

    # Start the loops
    try:
        check_remindme.start()
        change_status_loop.start()

    except Exception as e:
        bot.logger.warning(e)

    # Sync the commands
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
        if time <= datetime.now():
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


@bot.event
async def on_app_command_completion(interaction, command) -> None:
    """
    The code in this event is executed every time a command has been *successfully* executed.
    """

    if interaction.guild is not None:
        bot.logger.info(
            f"{interaction.user} (ID: {interaction.user.id}) executed /{command.qualified_name} command in {interaction.guild.name} (ID: {interaction.guild_id})"
        )
    else:
        bot.logger.info(
            f"{interaction.user} (ID: {interaction.user.id}) executed /{command.qualified_name} command in DMs"
        )


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message

    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return
    
    # stuur dm naar owners on prive command
    if message.guild is None:
        owners = [464400950702899211, 462932133170774036]
        for owner in owners:
            user = await bot.fetch_user(owner)
    
            await user.send(content=f"{message.author.display_name} sent: {message.content}")

            for att in message.attachments:
                await user.send(content=att.url)


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


async def on_tree_error(interaction, error):
    """
    The code in this event is executed every time a command catches an error.

    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    
    # check if the error is a custom exception
    if isinstance(error, exceptions.CustomCheckFailure):
        embed = error.getEmbed(interaction.command, bot.command_ids)

    elif isinstance(error, discord.app_commands.CommandOnCooldown):

        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24

        # if the command is /pushup gamble, we need to send a custom message
        if interaction.command and interaction.command.qualified_name == "pushup gamble":
            gambling_images = [
                "https://ip.bitcointalk.org/?u=https%3A%2F%2Ftalkimg.com%2Fimages%2F2023%2F12%2F16%2FEcNR9.jpeg&t=672&c=142sggGpakNc5A",
                "https://cdn.discordapp.com/attachments/1354445408381964349/1354445408599937085/IMG_3122.jpg?ex=67e55115&is=67e3ff95&hm=b5238bb1b084ea03cc60c0f86c1e14afcf0f7d0d3399fd8474651e770c9187b7&",
                "https://media.discordapp.net/attachments/1354445408381964349/1354459284141899787/images.png?ex=67e55e01&is=67e40c81&hm=07ca095246383cfb17443997f5bbdb2b937c50ab03b50183ec63a5d8115f800f&=&format=webp&quality=lossless&width=213&height=370",
                "https://media.discordapp.net/attachments/1354445408381964349/1354460186667913286/screen-shot-2022-11-09-at-5-05-23-pm.png?ex=67e55ed9&is=67e40d59&hm=d613852ce69caa2b5c981674e19d1b1558f8a521e5ec9fdfd6b7c4475b73de72&=&format=webp&quality=lossless&width=1209&height=1050",
                "https://media.discordapp.net/attachments/1354445408381964349/1354459434096791693/612bda234ef378922222ac125f19fdecfe816df0e177cfe0b599a7cc00de6016_1.png?ex=67e55e25&is=67e40ca5&hm=dfff2176c1c1a8d2cd6f878cb11182acb412d4e66215e134dd72e1110398cc05&=&format=webp&quality=lossless&width=851&height=1050",
                "https://media.tenor.com/Qwf2iW-zslMAAAAM/ohnepixel-hobby.gif",
                "https://c.tenor.com/YMJClCmllbYAAAAd/tenor.gif",

            ]
            embed = embeds.OperationFailedEmbed(
                f"**Please slow down** - You can use this command again in {f'{round(hours)} hours ' if round(hours) > 0 else ''}{f'{round(minutes)} minutes ' if round(minutes) > 0 else ''}{f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.\nYou can also be a true gambler and click this button to reset your cooldown*.",
                emoji="⏲️"
            )
            embed.set_footer(text="*This will give you 20 pushups to complete.")
            chosen_image=random.choice(gambling_images)
            embed.set_image(url=chosen_image)

            if interaction.response.is_done():
                return await interaction.followup.send(embed=embed, ephemeral=False, view=ResetCooldownView(chosen_image, interaction.user, error.cooldown, bot))
            return await interaction.response.send_message(embed=embed, ephemeral=False, view=ResetCooldownView(chosen_image, interaction.user, error.cooldown, bot))
    
        #Default message
        embed = embeds.OperationFailedEmbed(
            f"**Please slow down** - You can use this command again in {f'{round(hours)} hours ' if round(hours) > 0 else ''}{f'{round(minutes)} minutes ' if round(minutes) > 0 else ''}{f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            emoji="⏲️"
        )

        # send out response
        if interaction.response.is_done():
            return await interaction.followup.send(embed=embed, ephemeral=True)
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # user missing permissions
    elif isinstance(error, discord.app_commands.MissingPermissions):
        embed = embeds.OperationFailedEmbed(
            "You are missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to execute this command!",
        )

    # bot missing permissions
    elif isinstance(error, discord.app_commands.BotMissingPermissions):
        embed = embeds.OperationFailedEmbed(
            "I am missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to fully perform this command!",
        )

    # daily application command limit reached
    elif isinstance(error, discord.HTTPException):
        embed = embeds.OperationFailedEmbed(
            title="Something went wrong!",
            description="most likely daily application command limits.",
        )

    # other errors
    else:
        embed = embeds.OperationFailedEmbed(
            title="Error!",
            description=str(error).capitalize(),
        )

    bot.logger.warning(error) 
    
    # send out response
    if interaction.response.is_done():
        return await interaction.followup.send(embed=embed)
    await interaction.response.send_message(embed=embed)


bot.tree.on_error = on_tree_error


init_db()
insert_missing_badges()
asyncio.run(load_cogs())
bot.run(os.environ.get("BOT_TOKEN"))