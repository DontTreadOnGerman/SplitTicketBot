import discord
import datetime
import asyncio
import os
import wavelink
import yaml
from wavelink.ext import spotify
from discord.ext import commands


class splitticketbot(commands.Bot):
    def __init__(self):
        # Constructor
        constructor = {"command_prefix": "s!",
                       "intents": discord.Intents.all(),
                       "help_command": None}
        super().__init__(**constructor)
        self.not_allocated = True
        self.config = yaml.safe_load(open("config.yml"))
        self.lavalink_password = yaml.safe_load(open("lavalink/application.example.yml"))["lavalink"]["server"]["password"]
        self.launch_time = datetime.datetime.now()
        self.directory = os.getcwd()
        # stats
        self.total_message_num = 0
        self.message_num = 0
        self.bot_message_num = 0
        self.webhook_message_num = 0
        self.command_num = 0
        self.message_senders = {}
        self.command_users = {}
        # If you want to add a cog put in "cogs.cog name"
        self.cogs_list = ["fun", "developer", "help", "errors"]

    async def setup_hook(self):
        for cog in self.cogs_list:
            await self.load_extension(f"cogs.{cog}")
            print(f"Loaded cog {cog}...")
        await self.load_extension(f"jishaku")
        print(f"Loaded cog jishaku...")
        # Music stuff
        #self.loop.create_task(self.run_lavalink())
        #print("Started lavalink.jar...")
        #sc = spotify.SpotifyClient(client_id=self.config["spotify_client_id"],
        #                           client_secret=self.config["spotify_client_secret"])
        #node = wavelink.Node(uri='http://localhost:2333', password=self.lavalink_password)
        #await wavelink.NodePool.connect(client=self, nodes=[node], spotify=sc)

    async def run_lavalink(self):
        request = f"cd lavalink & java -jar Lavalink.jar"
        await asyncio.create_subprocess_shell(request, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    def run(self, **kwargs):
        print("Launching bot...")
        super().run(self.config["token"])


asyncio.run(splitticketbot().run())
