import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import datetime
import requests
import snscrape.modules.twitter as sntwitter

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Basic Command: Ping ---
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# --- Command: Price (Real-time using Yahoo Finance API) ---
def fetch_price(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        try:
            price = result['chart']['result'][0]['meta']['regularMarketPrice']
            return f"💰 `{symbol.upper()}` price: ${price:.2f}"
        except (KeyError, IndexError, TypeError):
            return "❌ Error parsing price data."
    else:
        return "❌ Failed to fetch data."

@bot.command()
async def price(ctx, symbol: str):
    msg = fetch_price(symbol)
    await ctx.send(msg)

# --- Command: Summary (Mock Placeholder) ---
@bot.command()
async def summary(ctx):
    await ctx.send("📈 Daily Summary (Demo):\n- NVDA breakout detected.\n- BTC bullish momentum confirmed.\n- ETH volume spike > 2x avg.")

# --- Command: Breakout (Mock Placeholder) ---
@bot.command()
async def breakout(ctx):
    await ctx.send("🚨 Breakout candidates:\n- NVDA: RSI > 60, MA Stack\n- BTC: Bullish sentiment > 70%, High Volume")

# --- Command: Plan ---
@bot.command()
async def plan(ctx, symbol: str):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
        response = requests.get(url).json()
        price = response['chart']['result'][0]['meta']['regularMarketPrice']
        entry = price * 1.01
        stop = price * 0.97
        target1 = price * 1.05
        target2 = price * 1.10
        rr_ratio = (target1 - price) / (price - stop)
        await ctx.send(
            f"📊 Trade Plan for `{symbol.upper()}`:\n"
            f"Entry: ${entry:.2f} | Stop: ${stop:.2f}\n"
            f"Targets: ${target1:.2f}, ${target2:.2f}\n"
            f"R:R Ratio: {rr_ratio:.2f}"
        )
    except:
        await ctx.send("❌ Failed to generate trade plan.")

# --- Command: Sentiment (Twitter) ---
@bot.command()
async def sentiment(ctx, symbol: str):
    symbol = symbol.upper()
    query = f"${symbol} OR {symbol} lang:en"
    tweets = list(sntwitter.TwitterSearchScraper(query).get_items())[:50]
    bullish = sum(1 for tweet in tweets if any(word in tweet.content.lower() for word in ["buy", "bull", "mooning", "skyrocketing", "to the moon"]))
    bearish = sum(1 for tweet in tweets if any(word in tweet.content.lower() for word in ["sell", "dump", "bear", "crash", "rekt"]))
    total = len(tweets)
    if total == 0:
        await ctx.send(f"No sentiment data found for `{symbol}`.")
        return
    ratio = bullish / total
    await ctx.send(f"💬 Sentiment for `{symbol}`:\n- Total Mentions: {total}\n- Bullish: {bullish} ({ratio:.2%})\n- Bearish: {bearish}")

# --- Command: Uptime ---
start_time = datetime.datetime.utcnow()

@bot.command()
async def uptime(ctx):
    now = datetime.datetime.utcnow()
    delta = now - start_time
    await ctx.send(f"🕒 Uptime: {str(delta).split('.')[0]}")

# --- Run Bot ---
bot.run(TOKEN)
