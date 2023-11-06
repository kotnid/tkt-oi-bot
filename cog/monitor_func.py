import discord
from discord.ext import commands
import datetime
import configparser
import requests
import difflib
import asyncio
import urllib

class monitor_func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.monitored_urls = {}
        self.monitored_channels = {}

    @commands.command()
    async def remove_url(self, ctx, url):
        if url in self.monitored_urls:
            del self.monitored_urls[url]
            await ctx.send(f"URL '{url}' has been removed from monitoring.")
        else:
            await ctx.send("This URL is not being monitored.")

    @commands.command()
    async def add_channel(self, ctx, channel: discord.TextChannel):
        if channel.id in self.monitored_channels:
            await ctx.send("This channel is already set up to receive updates.")
        else:
            self.monitored_channels[channel.id] = channel
            await ctx.send(f"Channel '{channel.name}' has been added for receiving updates.")

    @commands.command()
    async def show_urls(self, ctx):
        if self.monitored_urls:
            urls = "\n".join(self.monitored_urls.keys())
            await ctx.send(f"The currently monitored URLs are:\n{urls}")
        else:
            await ctx.send("No URLs are currently being monitored.")


    @commands.command()
    async def add_url(self, ctx, url):
        if url in self.monitored_urls:
            await ctx.send("This URL is already being monitored.")
        else:
            self.monitored_urls[url] = ''

            try:
                response = requests.get(url)
                content = response.text
                self.monitored_urls[url] = content
                await ctx.send(f"URL '{url}' has been added for monitoring.")
            except requests.exceptions.RequestException as e:
                del self.monitored_urls[url]
                await ctx.send(f"Failed to fetch content from URL '{url}'. Error: {e}")

    async def check_website_content_updates(self):
        await self.bot.wait_until_ready()  

        while not self.bot.is_closed():
            for url, stored_content in self.monitored_urls.items():
                try:
                    response = requests.get(url)
                    content = response.text

                    if content != stored_content:
                        self.monitored_urls[url] = content
                        message = f"The website at {url} has been updated."
                        await self._send_updates_to_channels(message)
                except requests.exceptions.RequestException:
                    pass  

            await asyncio.sleep(10)  

    async def _send_updates_to_channels(self, message):
        for channel in self.bot.get_all_channels():
            if channel.id in self.monitored_channels:
                await channel.send(message)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.check_website_content_updates())

async def setup(bot):
   await bot.add_cog(monitor_func(bot))