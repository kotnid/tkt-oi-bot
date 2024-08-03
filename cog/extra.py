import discord
from discord.ext import commands
import asyncio
from func.photo import gen_image
import os

class extra_func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def speech(self, ctx, *, msg="left AK"):
        await ctx.send("fuck you exploded again????")
        # # cnt = 0
        # if(len(msg) > 50):
        #     await ctx.s
        # for char in msg:
        #     if char == ' ':
        #         await ctx.send('\u200B')
        #     else:
        #         await ctx.send(char)
        #     await asyncio.sleep(0.5)

    @commands.command()
    async def prayer(self, ctx):
        await ctx.send("oh left is so genius it is undoubtable that left is always the truth , the myth, the legendary holy left. It is our luck that we are blessed by left and receiving his guidance")

    @commands.command()
    async def clear(self, ctx, limit: int = 5000):
        deleted = await ctx.channel.purge(limit=limit, check=lambda msg: msg.author == self.bot.user)
        await ctx.send(f'Deleted {len(deleted)} messages.', delete_after=5)

    @commands.command()
    async def quote(self, ctx, *, msg="LEFT AK"):
        opt = gen_image(msg)
        with open(opt, 'rb') as file:
            edited_image = discord.File(file)
            await ctx.send(file=edited_image)
        os.remove(opt);
        

async def setup(bot):
    await bot.add_cog(extra_func(bot))