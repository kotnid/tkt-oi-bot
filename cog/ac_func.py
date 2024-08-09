import discord
from discord.ext import commands
import asyncio
from func.query import get_atcoder, get_hkoi, get_codeforces, get_platform_ac_count
import os
from func.database import update_data, remove_data, query_data

class ac_func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.urls = {"cf":"<:cf:1179079517420130314>",
                "at":"<:at:1179079625389916211>",
                "hkoi":"<:hkoi:1262044696918622269>",
                "ac":"<:ac:1171452943988428802>"}

    @commands.command()
    async def ac(self, ctx, *, msg="hkoi sms24112"):
        platform = msg.split()[0]
        username = msg.split()[1]
        await ctx.send(f"Querying user {username} on {platform}...")
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
            await ctx.send(f"User {username} has {self.urls['ac']} {ac_count} tasks on {self.urls[platform]}")
    
    @commands.command()
    async def update(self, ctx, *, msg="hkoi sms24112"):
        try:
            user_id = str(ctx.author.id)
            platform = msg.split()[0]
            username = msg.split()[1]
            update_data(user_id, platform, username)
            await ctx.send("Updated!")
        except Exception as e:
            await ctx.send(f"Fail to update : {e}")

    @commands.command()
    async def remove(self, ctx, *, msg="hkoi"):
        try:
            user_id = str(ctx.author.id)
            platform = msg.split()[0]
            remove_data(user_id, platform)
            await ctx.send("Removed!")
        except Exception as e:
            await ctx.send(f"Fail to remove : {e}")

    @commands.command()
    async def query(self, ctx):
        try:
            user_id = str(ctx.author.id)
            platforms = query_data(user_id)
            msg = ""
            for x in platforms:
                msg += f"{x} : {platforms[x]}\n"
            await ctx.send(msg)
        except Exception as e:
            await ctx.send(f"Fail to query : {e}")

    @commands.command()
    async def queryAC(self, ctx):
        try:    
            await ctx.send("finding...")
            user_id = str(ctx.author.id)
            platform_data = query_data(user_id)
            msg = ""    
            tot = 0
            for platform, username in platform_data.items():
                ac_count = int(get_platform_ac_count(platform, username))
                if ac_count != -1:
                    tot += ac_count
                msg += f"{platform} : {username} - {ac_count}\n"
            msg += f"User has {tot} {self.urls['ac']}"
            await ctx.send(msg)
        except Exception as e:
            await ctx.send(e)

async def setup(bot):
    await bot.add_cog(ac_func(bot))      