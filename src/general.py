from discord.ext import commands
import discord
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ID = 1305180509860532264


bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

# Opslaan van PR's in een lijst
pr_records = []  # Lijst die de PR's en data zal opslaan

@bot.event
async def on_ready():
    print("Hello!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello!")

# Command voor het toevoegen van een PR
@bot.command()
async def add_pr(ctx, date: str, pr: int):
    try:
        # Controleer of de datum goed is geformatteerd (bijv. YYYY-MM-DD)
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        # Voeg het PR en de datum toe aan de lijst
        pr_records.append({"date": date_obj, "pr": pr})
        
        # Bevestig dat het PR is toegevoegd
        await ctx.send(f"PR van {pr} op {date} is toegevoegd!")
    except ValueError:
        # Foutmelding als de datum niet goed is geformatteerd
        await ctx.send("Ongeldige datum, gebruik het formaat: YYYY-MM-DD")

bot.run(BOT_TOKEN)
