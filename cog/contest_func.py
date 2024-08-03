import discord
from discord.ext import commands
import datetime
import configparser
import requests
import os
import asyncio
import random

# config = configparser.ConfigParser()
# config.read('config.ini')

url = "https://clist.by/api/v3/contest/"

# get upcoming contests
def get_contests(hosts):
    contests = []
    for host in hosts:
        params = {
            'username': "tkt0506",
            # "api_key": config["contest"]["key"],
            "api_key": os.getenv("key"),
            'upcoming': 'true',
            'host': host
        }

        response = requests.get(url, params=params)
        print(response.text)
        data = response.json()

        if response.status_code == 200 :
            for contest_data in data["objects"]:
                duration = contest_data["duration"] // 60 
                event = contest_data["event"]
                host = contest_data["host"]
                href = contest_data["href"]
                start = contest_data["start"]
                res = contest_data["resource"]
                start_utc = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
                start_utc_plus_8 = start_utc + datetime.timedelta(hours=8)

                contests.append({
                    "duration": duration,
                    "event": event,
                    "host": host,
                    "href": href,
                    "res" : res,
                    "start": start_utc_plus_8
                })

    sorted_contests = sorted(contests, key=lambda x: x["start"])
    return sorted_contests

class contest_func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def contests(self, ctx):
        hosts = ["codeforces.com", "atcoder.jp","codechef.com"]
        upcoming_contests = get_contests(hosts)

        page_size = 4
        total_pages = (len(upcoming_contests) + page_size - 1) // page_size

        emoji_list = ["⏪", "⏩"]  # Emoji for navigating between pages

        current_page = 0

        urls = {"codeforces.com":"<:cf:1179079517420130314>",
                "atcoder.jp":"<:at:1179079625389916211>",
                "codechef.com":"<:cc:1179080237221433454>",
                "ac":"<:ac:1171452943988428802>"}

        def generate_embed(page):
            start_index = page * page_size
            end_index = min((page + 1) * page_size, len(upcoming_contests))
        
            embed = discord.Embed(title=f"Upcoming Contests (Page {page + 1}/{total_pages})", color=discord.Color.blue())

            for i in range(start_index, end_index):
                contest = upcoming_contests[i]
                embed.add_field(name=f"{urls[contest['res']]} {contest['event']}", value=f"Start Time: {contest['start']}\n[Contest Link]({contest['href']})", inline=False)
            
            footer_messages = [f"Left AC blessing", "rating++", "lazy tkt can't think can say what", f"ACACAC"]
            random_message = random.choice(footer_messages)
            embed.set_footer(text=random_message)
            
            return embed

        message = await ctx.send(embed=generate_embed(current_page))

        for emoji in emoji_list:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return (
                user == ctx.message.author
                and reaction.message.id == message.id
                and str(reaction.emoji) in emoji_list
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60.0, check=check
                )

                if str(reaction.emoji) == emoji_list[0]:  # Previous page
                    current_page -= 1
                    if current_page < 0:
                        current_page = total_pages - 1
                    await message.edit(embed=generate_embed(current_page))

                elif str(reaction.emoji) == emoji_list[1]:  # Next page
                    current_page += 1
                    if current_page == total_pages:
                        current_page = 0
                    await message.edit(embed=generate_embed(current_page))

                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                break


async def setup(bot):
    await bot.add_cog(contest_func(bot))