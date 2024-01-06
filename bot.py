import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import auth

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=';', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.reply("pong!")

@bot.command()
async def login(ctx):
    cred = auth.authorize(ctx.author.id)
    msg = f"Logged in!\nExpiry: {cred.expiry}\n"
    await ctx.reply(msg)

bot.run(TOKEN)