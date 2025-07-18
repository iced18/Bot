import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Optional: Load .env if you're running locally
load_dotenv()

# Safely load token from environment
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not set")

# Set up bot
intents = discord.Intents.default()
intents.message_content = True  # Needed for commands

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is live as {bot.user}")

# Test command
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! Bot is live.")

# Run bot
bot.run(TOKEN)
