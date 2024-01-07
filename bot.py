from datetime import datetime, time
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from googleapiclient.discovery import build
import auth
import asyncio

service = {}

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=';', intents=intents)

@bot.command()
async def ping(ctx):
    print(auth.tokens)
    await ctx.reply("pong!")

@bot.command()
async def login(ctx):
    creds = await auth.authorize(str(ctx.author.id))
    msg = f"Logged in!\nExpiry: {creds.expiry}\n"

    global service
    service = await asyncio.to_thread(build, serviceName ="calendar", version = "v3", credentials=creds)

    await ctx.reply(msg)

@bot.command()
async def today(ctx):
    start = datetime.combine(datetime.now(), time.min).isoformat() + "Z" # "Z" indicates UTC time
    end = datetime.combine(datetime.now(), time.max).isoformat() + "Z"
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start,
        timeMax=end,
    ).execute()
    msg = "" 
    for e in events_result["items"]:
        msg += "- " + e["summary"] + "\n"
    await ctx.reply(msg)

bot.run(TOKEN)