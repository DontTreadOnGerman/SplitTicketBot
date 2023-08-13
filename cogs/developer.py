import time
import discord
import pkg_resources
import sys
import psutil
import humanize
import aiohttp
import yaml
import asyncio
import feedparser
from datetime import datetime
from utils import embeds
from discord.ext import commands, tasks

date_format = "%a, %d %b %Y %H:%M:%S %z"


class Developer(commands.Cog, name="Developer :gear:"):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        self.memory = self.process.memory_full_info()
        self.version = sys.version_info
        super().__init__()

    @tasks.loop(seconds=120)
    async def article_checker(self):
        # get last pub date
        last_pub = datetime.strptime(self.bot.config["last_pub_date"]+"+0000", date_format)
        need_updates = False
        # get text
        async with aiohttp.ClientSession() as session:
            async with session.get('https://split-ticket.org/feed/') as res:
                raw_feed = await res.text()
            rss = feedparser.parse(raw_feed)
            channel = self.bot.get_channel(int(self.bot.config["article_channel"]))
            for entry in rss["entries"]:
                datetime_object = datetime.strptime(entry["published"], date_format)
                is_new = last_pub-datetime_object
                if is_new.total_seconds() < 2:
                    need_updates = True
                    title = entry["title"]
                    link = entry["link"]
                    authors = entry["author"]
                    await channel.send(f"New article! @everyone\n"
                                       f"```{title}```\nIt's written by {authors}."
                                       f"\nCheck it out!\n"
                                       f"{link}")
        if need_updates is True:
            with open("./config.yml", 'w') as file:
                self.bot.config["last_pub_date"] = str(datetime.utcnow().strftime(date_format))
                yaml.dump(self.bot.config, file)

    @commands.Cog.listener()
    async def on_ready(self):
        self.article_checker.start()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.command_num += 1
        for member_dictionary in [self.bot.command_users, self.bot.message_senders]:
            if ctx.author.id in member_dictionary:
                member_dictionary[ctx.author.id] += 1
            else:
                member_dictionary[ctx.author.id] = 1
        self.bot.message_num += 1
        self.bot.total_message_num += 1

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is not None:
            self.bot.bot_message_num += 1
        elif message.webhook_id is not None:
            self.bot.webhook_message_num += 1
        else:
            member_dictionary = self.bot.message_senders
            if message.author.id in member_dictionary:
                member_dictionary[message.author.id] += 1
            else:
                member_dictionary[message.author.id] = 1
            self.bot.message_num += 1
        self.bot.total_message_num += 1

    @commands.guild_only()
    @commands.hybrid_command(name="stats", help="Shows several statistics about the bot.")
    async def stats(self, ctx):
        start = time.perf_counter()
        message = await ctx.send(embed=embeds.twoembed("Measuring...",
                                                       "Sit tight!"))
        end = time.perf_counter()
        message_latency = str(round((end - start) * 1000)) + "ms"
        websocket = str(round(self.bot.latency * 1000)) + "ms"
        embedvar = discord.Embed(title="Bot Statistics", color=0xBF64DB,
                                 description=f"All data is recorded starting from when the bot starts.\n"
                                             f"Bot start: <t:{round(self.bot.launch_time.timestamp())}>")
        embedvar.add_field(name="Messages", value=f"**``Total Messages``**: {self.bot.total_message_num}\n"
                                                  f"**``Human Messages``**: {self.bot.message_num}\n"
                                                  f"**``Bot Messages``**: {self.bot.bot_message_num}\n"
                                                  f"**``Webhook Messages``**: {self.bot.webhook_message_num}\n"
                                                  f"**``Message Senders``**: {len(self.bot.message_senders)}\n"
                                                  f"These figures include commands.", inline=False)
        embedvar.add_field(name="Commands", value=f"**``Total Commands``**: {self.bot.command_num}\n"
                                                  f"**``Command Users``**: {len(self.bot.command_users)}\n",
                           inline=False)
        embedvar.add_field(name="Processing Power", value=f"**``Message Speed``**: {message_latency}\n"
                                                          f"**``Websocket Speed``**: {websocket}\n"
                                                          f"**``Physical Memory Usage``**: {humanize.naturalsize(self.memory.rss)}\n"
                                                          f"**``Virtual Memory Usage``**: {humanize.naturalsize(self.memory.vms)}\n"
                                                          f"**``Dedicated Memory Usage``**: {humanize.naturalsize(self.memory.uss)}\n"
                                                          f"**``CPU Usage``**: {round(self.process.cpu_percent() / psutil.cpu_count(), 1)}%\n",
                           inline=False)
        embedvar.set_footer(text=f"Made in discord.py {pkg_resources.get_distribution('discord.py').version} + "
                                 f"Python {self.version.major}.{self.version.minor}.{self.version.micro}!"
                                 f" Ran on {sys.platform}.")
        await message.edit(embed=embedvar)

    @commands.guild_only()
    @commands.hybrid_command(name="ping", help="Checks the speed of the bot.")
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send(embed=embeds.twoembed("Measuring...",
                                                       "Sit tight!"))
        end = time.perf_counter()
        message_latency = str(round((end - start) * 1000)) + "ms"
        websocket = str(round(self.bot.latency * 1000)) + "ms"
        embedvar = discord.Embed(title="Bot Statistics", color=0xBF64DB, description="Pong!.")
        embedvar.add_field(name="Message Speed", value=message_latency, inline=False)
        embedvar.add_field(name="Websocket Speed", value=websocket, inline=False)
        await message.edit(embed=embedvar)

    @commands.guild_only()
    @commands.is_owner()
    @commands.hybrid_group(name="cog", help="Base command for controlling cogs.")
    async def cog(self, ctx):
        await ctx.send(embed=embeds.twoembed(f"This isn't an option!", f"You can ``reload`` or ``load``"))

    @commands.guild_only()
    @commands.is_owner()
    @cog.command(name="reload", help="Reloads a cog.")
    async def reload(self, ctx, cog: str):
        message = await ctx.send(embed=embeds.twoembed(f"Reloading {cog}...",
                                                       f"Sit tight!"))
        try:
            if cog not in ["JISHAKU", "Jishaku", "jishaku"]:
                await self.bot.reload_extension(f"cogs.{cog}")
            else:
                await self.bot.reload_extension("jishaku")
        except Exception:
            embed = embeds.twoembed("Uh oh.", "This cog doesn't exist.")
        else:
            embed = embeds.twoembed("Success!", f"I've reloaded {cog} for you.")
            print(f"Reloaded {cog}...")
        await message.edit(embed=embed)

    @commands.guild_only()
    @commands.is_owner()
    @cog.command(name="load", help="Loads a cog.")
    async def load(self, ctx, cog: str):
        message = await ctx.send(embed=embeds.twoembed(f"Loading {cog}...",
                                                       f"Sit tight!"))
        try:
            if cog not in ["JISHAKU", "Jishaku", "jishaku"]:
                await self.bot.load_extension(f"cogs.{cog}")
            else:
                await self.bot.load_extension("jishaku")
        except Exception:
            embed = embeds.twoembed("Uh oh.", "This cog doesn't exist.")
        else:
            embed = embeds.twoembed("Success!", f"I've loaded {cog} for you.")
            print(f"Loaded {cog}...")
        await message.edit(embed=embed)

    @commands.guild_only()
    @commands.is_owner()
    @cog.command(name="unload", help="Unloads a cog.")
    async def unload(self, ctx, cog: str):
        message = await ctx.send(embed=embeds.twoembed(f"Unloading {cog}...",
                                                       f"Sit tight!"))
        try:
            if cog not in ["JISHAKU", "Jishaku", "jishaku"]:
                await self.bot.load_extension(f"cogs.{cog}")
            else:
                await self.bot.load_extension("jishaku")
        except Exception:
            embed = embeds.twoembed("Uh oh.", "This cog doesn't exist.")
        else:
            embed = embeds.twoembed("Success!", f"I've unloaded {cog} for you.")
            print(f""
                  f"Unloaded {cog}...")
        await message.edit(embed=embed)

    @commands.guild_only()
    @commands.is_owner()
    @commands.hybrid_command(name="pull", help="Pulls from the GitHub repository.")
    async def pull(self, ctx):
        embed = embeds.twoembed("Pulling...", "Awaiting results from the GitHub repository.")
        message = await ctx.send(embed=embed)
        proc = await asyncio.create_subprocess_shell(f"cd {self.bot.directory} & git pull",
                                                     stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if stdout:
            embed = embeds.twoembed("Pulled - Stdout!", str(stdout.decode()))
        if stderr:
            embed = embeds.twoembed("Pulled - Stderr!", str(stderr.decode()))
        await message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(Developer(bot))
