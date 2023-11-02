import os
import asyncio
import discord
from discord.ext import commands
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "!", intents = intents)

# init 
@bot.event
async def on_ready():
    print(f"Login as --> {bot.user}")

# load extension
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cog.{extension}")
    await ctx.send(f"Loaded {extension} done.")

# unload extension
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cog.{extension}")
    await ctx.send(f"Unloaded {extension} done.")

# reload extension
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cog.{extension}")
    await ctx.send(f"Reloaded {extension} done.")

# init load all extension
@bot.event
async def setup_hook():
    for filename in os.listdir("./cog"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cog.{filename[:-3]}")

bot.run(config["DISCORD"]["token"])