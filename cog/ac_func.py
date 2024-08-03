import discord
from discord.ext import commands
import asyncio
from func.query import get_atcoder, get_hkoi, get_codeforces
import os

class ac_func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ac(self, ctx, *, msg="hkoi sms24112"):
        platform = msg.split()[0]
        username = msg.split()[1]
        await ctx.send(f"Querying user {username} on {platform}...")

        urls = {"cf":"<:cf:1179079517420130314>",
                "at":"<:at:1179079625389916211>",
                "hkoi":"<:hkoi:1262044696918622269>",
                "ac":"<:ac:1171452943988428802>"}
    
        ac_count = -1
        # get_atcoder(username)
        if platform == "hkoi":
            ac_count = get_hkoi(username)
        elif platform == "cf":
            ac_count = get_codeforces(username)
        elif platform == "at":
            ac_count = get_atcoder(username)

        if ac_count == -1:
            await ctx.send("Runtime error...")
        else:
            await ctx.send(f"User {username} has {urls['ac']} {ac_count} tasks on {urls[platform]}")

async def setup(bot):
    await bot.add_cog(ac_func(bot))      