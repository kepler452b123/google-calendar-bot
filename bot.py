from datetime import datetime, time, date
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from googleapiclient.discovery import build
import auth

services = {}

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
    creds = auth.authorize(str(ctx.author.id))
    msg = f"Logged in!\nExpiry: {creds.expiry}\n"

    global services
    services[ctx.author.id] = build("calendar", "v3", credentials=creds)

    await ctx.reply(msg)

# Converts google "datetime" format to a simple 12 hour time format
def get_time(date_str: str):
    i = date_str.find("T")
    time24 = date_str[i+1:i+6]
    hour = int(time24[:2])
    if hour >= 12:
        hour %= 12
        return f"{hour}{time24[2:]} PM"
    else:
        return f"{time24} AM"

@bot.command()
async def today(ctx):
    service = services[ctx.author.id]
    start = datetime.combine(datetime.now(), time.min).isoformat() + "Z" # "Z" indicates UTC time
    end = datetime.combine(datetime.now(), time.max).isoformat() + "Z"
    events_result = (
        service.events().list(
            calendarId="primary",
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
    )
    fields = []
    for e in events_result["items"]:
        time_start = get_time(e['start']['dateTime'])
        time_end = get_time(e['end']['dateTime'])
        field = {
            "name": e["summary"],
            "value": f"{time_start} - {time_end}"
        }
        fields.append(field)
    embed = discord.Embed.from_dict({
      "type": "rich",
      "title": "Today",
      "description": date.today(),
      "color": 0x00FFFF,
      "fields": fields
    })
    await ctx.reply(embed=embed)

bot.run(TOKEN)