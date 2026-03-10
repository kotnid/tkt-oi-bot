import discord
from discord.ext import commands
import asyncio
from func.photo import gen_image, gen_image2
import os
import threading
from playwright.sync_api import sync_playwright

class extra_func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msgChannel = set()

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
        os.remove(opt)

    @commands.command()
    async def image(self, ctx, image_name: str = None, *, text: str):
        opt = gen_image2(text, image_name)
        with open(opt, 'rb') as file:
            edited_image = discord.File(file)
            await ctx.send(file=edited_image)
        os.remove(opt)


    # @commands.command()
    # async def addIOI(self, ctx):
    #     self.msgChannel.add(ctx.channel.id)
    #     await ctx.send(f"Channel {ctx.channel.mention} added!")

    # @commands.command()
    # async def rmIOI(self, ctx):
    #     if ctx.channel.id in self.msgChannel:
    #         self.msgChannel.remove(ctx.channel.id)
    #         await ctx.send(f"Channel {ctx.channel.mention} removed!")
    #     else:
    #         await ctx.send(f"Channel {ctx.channel.mention} not in list!")

    # @commands.command()
    # async def listIOI(self, ctx):
    #     if not self.msgChannel:
    #         await ctx.send("No channels in the list!")
    #         return

    #     msg = "Current list:\n"
    #     for channel_id in self.msgChannel:
    #         msg += f"<#{channel_id}>\n"
    #     await ctx.send(msg)

    # def handle_console_message(self, msg):
    #     if "hkg" in msg.text:
    #         message = f"[Console] {msg.text}"
    #         for channel_id in self.msgChannel:
    #             channel = self.bot.get_channel(channel_id)
    #             if channel:
    #                 asyncio.run_coroutine_threadsafe(channel.send(message), self.bot.loop)

    # def run_playwright(self):
    #     with sync_playwright() as p:
    #         browser = p.firefox.launch(headless=True)
    #         page = browser.new_page()
    #         page.on("console", self.handle_console_message)
    #         page.goto("https://ranking.ioi2024.eg/")
    #         page.wait_for_timeout(10000000) 
    #         browser.close()
        

async def setup(bot):
    cog = extra_func(bot)  
    # playwright_thread = threading.Thread(target=cog.run_playwright) 
    # playwright_thread.start()
    await bot.add_cog(cog)