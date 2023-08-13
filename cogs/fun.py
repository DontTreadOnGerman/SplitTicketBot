import discord
import wavelink
import datetime
import pandas as pd
from utils import useful_functions, embeds
from wavelink.ext import spotify
from discord.ext import commands, tasks
from utils.useful_functions import percent_maker


class Fun(commands.Cog, name="Fun \U0001F973"):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.vc_auto_disconnect.start()
        self.recently_connected = None

    @tasks.loop(minutes=2)
    async def vc_auto_disconnect(self):
        clients = self.bot.voice_clients
        if clients != []:
            client = clients[0]
            if client.is_connected() is True:
                equation = (datetime.datetime.now()-self.recently_connected).total_seconds()
                if equation > 120:
                    vc = client.channel.members
                    amount_of_members = len(vc)
                    for member in vc:
                        if member.bot is True:
                            amount_of_members += -1
                    if amount_of_members == 0:
                        await client.disconnect()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loading status...")
        await self.bot.change_presence(activity=discord.Game(name="with a WAR regression"))

    @commands.guild_only()
    @commands.hybrid_command(name="connect", help="Connects to a voice channel.")
    async def connect(self, ctx, *, channel: discord.VoiceChannel = None):
        try:
            channel = channel or ctx.author.channel.voice
        except AttributeError:
            return await ctx.send(embed=embeds.twoembed("No channel found!", "Either join a channel or provide a channel."))
        #await channel.connect(cls=wavelink.Player)
        #await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
        #await ctx.send(embed=embeds.twoembed("Connected!", f"You can find me in <#{channel.id}>."))
        #self.recently_connected = datetime.datetime.now()
        await ctx.send("WIP")

    @commands.guild_only()
    @commands.hybrid_command(name="disconnect", help="Disconnects from the bot's current voice channel.")
    async def disconnect(self, ctx):
        #try:
            #vc = ctx.voice_client
            #await vc.disconnect()
            #await ctx.send(embed=embeds.twoembed("Disconnected.", f"Thanks for listening to my music!"))
    #except Exception:
            #await ctx.send(embed=embeds.twoembed("I'm not in a voice channel!", f"That's just mean..."))
        await ctx.send("WIP")

    @commands.guild_only()
    @commands.hybrid_group(name="play", help="Base play command.")
    async def play(self, ctx):
        await ctx.send("WIP")
        #await ctx.send(embed=embeds.twoembed("This isn't an option!", f"You can play ``youtube``, ``ytplaylist``, ``ytmusic``, ``spotify`` or ``soundcloud``."))

    @commands.guild_only()
    @play.command(name="youtube", help="Plays a YouTube song or playlist.")
    async def youtube(self, ctx, *, track: str):
        not_connected = await useful_functions.not_connected(self, ctx)
        vc = not_connected[-1]
        self.not_connected = not_connected[0]
        tracks = await wavelink.YouTubeTrack.search(track)
        if not tracks:
            return await ctx.send(embed=embeds.twoembed("This isn't a valid search!", f"I need an actual song, video."))
        track = tracks[0]
        if self.queue == []:
            await vc.play(track)
            embed = embeds.twoembed(f"Started playing {track}", "I hope you like it!")
        else:
            self.queue.append(track)
            embed = embeds.twoembed(f"Queued {track}", "I hope you like what's currently on!")
        embed.set_thumbnail(url=await track.fetch_thumbnail())
        #await ctx.send(embed=embed)
        await ctx.send("WIP")

    @commands.guild_only()
    @play.command(name="ytplaylist", help="Plays a YouTube playlist.")
    async def ytplaylist(self, ctx, *, playlist: str):
        not_connected = await useful_functions.not_connected(self, ctx)
        vc = not_connected[-1]
        self.not_connected = not_connected[0]
        playlist = await wavelink.YouTubePlaylist.search(playlist)
        if not playlist:
            return await ctx.send(embed=embeds.twoembed("This isn't a valid search!", f"I need an actual song or playlist."))
        if self.queue == []:
            await vc.play(playlist[0])
            embed = embeds.twoembed(f"Started playing {playlist[0]}", "I hope you like it! The rest of the playlist is yet to come.")
            embed.set_thumbnail(url=await playlist[0].fetch_thumbnail())
        else:
            embed = embeds.twoembed(f"Queued all songs in {playlist}", "I hope you what's currently on!")
        if len(playlist.tracks) != 1 and self.queue != []:
            for track in playlist.tracks:
                self.queue.append(track)
        async for track in wavelink.Queue:
            print(track)
        #await ctx.send(embed=embed)
        await ctx.send("WIP")

    @commands.guild_only()
    @play.command(name="ytmusic", help="Plays a YouTube Music song.")
    async def ytmusic(self, ctx, *, track: str):
        not_connected = await useful_functions.not_connected(self, ctx)
        vc = not_connected[-1]
        self.not_connected = not_connected[0]
        tracks = await wavelink.YouTubeMusicTrack.search(track)
        if not tracks:
            return await ctx.send(embed=embeds.twoembed("This isn't a valid search!", f"I need an actual song."))
        track = tracks[0]
        if self.queue == []:
            await vc.play(track)
            embed = embeds.twoembed(f"Started playing {track}", "I hope you like it!")
        else:
            self.queue.append(track)
            embed = embeds.twoembed(f"Queued {track}", "I hope you like what's currently on!")
        embed.set_thumbnail(url=await track.fetch_thumbnail())
        #await ctx.send(embed=embed)
        await ctx.send("WIP")

    @commands.guild_only()
    @play.command(name="spotify", help="Plays a Spotify song, but you have to link the URL.")
    async def spotify(self, ctx, *, url: str):
        not_connected = await useful_functions.not_connected(self, ctx)
        vc = not_connected[-1]
        self.not_connected = not_connected[0]
        tracks = await spotify.SpotifyTrack.search(query=url)
        if not tracks:
            return await ctx.send(embed=embeds.twoembed("This isn't a valid URL!", f"I need an actual song or playlist."))
        track = tracks[0]
        if self.queue != []:
            await vc.play(track)
            embed = embeds.twoembed(f"Started playing {track}", "I hope you like it!")
        else:
            self.queue.append(track)
            embed = embeds.twoembed(f"Queued {track}", "I hope you like what's currently on!")
        embed.set_thumbnail(url=await track.fetch_thumbnail())
        embed.url = url
        #await ctx.send(embed=embed)
        await ctx.send("WIP")

    @commands.guild_only()
    @commands.hybrid_command(name="cd", help="Gets data about a congressional district (2023-2025).")
    async def cd(self, ctx, *, cd: str):
        cd = (cd.replace("-0", "-")).upper()
        cd_data = pd.read_csv(f"{self.bot.directory}/cd_data.csv")
        cd_data = cd_data[cd_data.District.isin([cd])].to_dict(orient="records")[0]
        total = cd_data['Total Population']
        embed = embeds.twoembed(cd+" Data", f"Here's some info about this district.\n"
                                            f"The total population of this district is {total}.")
        embed_thumbnail = f"{self.bot.directory}/cd_images/{cd}.png"
        file = discord.File(embed_thumbnail, filename="image.png")
        embed.set_image(url=f"attachment://image.png")
        romney_percent = round(100*(0.5+((float(cd_data["2012 Margin"].replace("%", ""))/100)/2)), 2)
        obama_percent = round(100-romney_percent, 2)
        _08_votes = cd_data['Obama Votes']+cd_data['McCain Votes']
        election_data = f"**Biden 2020 Votes**: {cd_data['Biden 20 Votes']} ({await percent_maker(cd_data['Biden 20 Votes'], cd_data['2020 Votes'])}%)\n" \
                        f"**Trump 2020 Votes**: {cd_data['Trump 20 Votes']} ({await percent_maker(cd_data['Trump 20 Votes'], cd_data['2020 Votes'])}%)\n" \
                        f"**Total 2020 Votes**: {cd_data['2020 Votes']}\n" \
                        f"**Clinton 2016 Votes**: {cd_data['Clinton 16 Votes']} ({await percent_maker(cd_data['Clinton 16 Votes'], cd_data['2016 Votes'])}%)\n" \
                        f"**Trump 2016 Votes**: {cd_data['Trump 16 Votes']} ({await percent_maker(cd_data['Trump 16 Votes'], cd_data['2016 Votes'])}%)\n" \
                        f"**Total 2016 Votes**: {cd_data['2016 Votes']}\n" \
                        f"**Obama 2012 %**: {obama_percent}%\n" \
                        f"**Romney 2012 %**: {romney_percent}%\n" \
                        f"**Obama 2008 Votes**: {cd_data['Obama Votes']} ({await percent_maker(cd_data['Obama Votes'], _08_votes)}%)\n" \
                        f"**McCain 2008 Votes**: {cd_data['McCain Votes']} ({await percent_maker(cd_data['McCain Votes'], _08_votes)}%)"
        education_data = f"**High school degree**: {cd_data['High school']} ({await percent_maker(cd_data['High school'], total)}%)\n" \
                         f"**Some college, no degree**: {cd_data['Some college, no degree']} ({await percent_maker(cd_data['Some college, no degree'], total)}%)\n" \
                         f"**Associate's degree**: {cd_data['Associates degree']} ({await percent_maker(cd_data['Associates degree'], total)}%)\n" \
                         f"**Bachelor's degree**: {cd_data['Bachelors degree']} ({await percent_maker(cd_data['Bachelors degree'], total)}%)\n" \
                         f"**Graduate or professional degree**: {cd_data['Graduate or professional degree']} ({await percent_maker(cd_data['Graduate or professional degree'], total)}%)"
        housing_data = f"**Median household income**: ${cd_data['Median household income']}\n" \
                       f"**Mean household income**: ${cd_data['Mean household income']}\n" \
                       f"**Occupied housing units**: {cd_data['Occupied housing units']} ({await percent_maker(cd_data['Occupied housing units'], cd_data['Total housing units'])}%)\n" \
                       f"**Vacant housing units**: {cd_data['Vacant housing units']} ({await percent_maker(cd_data['Vacant housing units'], cd_data['Total housing units'])}%)\n" \
                       f"**Total housing units**: {cd_data['Total housing units']}\n" \
                       f"**Median gross rent**: ${cd_data['Median gross rent']}"
        urbanization_data = f"This data is derived from a 2017 survey, so it's not as up to date.\n" \
                            f"**Urban population**: {cd_data['Urban Population']} ({await percent_maker(cd_data['Urban Population'], cd_data['Total Respondents'])}%)\n" \
                            f"**Suburban population**: {cd_data['Suburban Population']} ({await percent_maker(cd_data['Suburban Population'], cd_data['Total Respondents'])}%)\n" \
                            f"**Rural population**: {cd_data['Rural Population']} ({await percent_maker(cd_data['Rural Population'], cd_data['Total Respondents'])}%)\n" \
                            f"**Total survey respondents**: {cd_data['Total Respondents']}"
        employment_data = f"**Median age**: {cd_data['Median age']} years\n" \
                          f"**One race**: {cd_data['One race']} ({await percent_maker(cd_data['One race'], total)}%)\n" \
                          f"**White/Caucasian**: {cd_data['White']} ({await percent_maker(cd_data['White'], total)}%)\n" \
                          f"**Black/African-American**: {cd_data['Black or African American']} ({await percent_maker(cd_data['Black or African American'], total)}%)\n" \
                          f"**Native American**: {cd_data['American Indian and Alaska Native']} ({await percent_maker(cd_data['American Indian and Alaska Native'], total)}%)\n" \
                          f"**Asian+Pacific Islander**: {cd_data['Asian']+cd_data['Native Hawaiian and Other Pacific Islander']} ({await percent_maker((cd_data['Asian']+cd_data['Native Hawaiian and Other Pacific Islander']), total)}%)\n" \
                          f"**Other**: {cd_data['Some other race']} ({await percent_maker(cd_data['Some other race'], total)}%)\n" \
                          f"**Multiple races**: {cd_data['Two or more races']} ({await percent_maker(cd_data['Two or more races'], total)}%)\n" \
                          f"**Hispanic/Latino %**: {cd_data['Latino']} ({await percent_maker(cd_data['Latino'], total)}%)\n" \
                          f"**Non Hispanic/Latino %**: {total-cd_data['Latino']} ({round(100-await percent_maker(cd_data['Latino'], total), 2)}%)\n"
        commute_data = f"**Employed**: {cd_data['Employed']} ({await percent_maker(cd_data['Employed'], total)}%)\n" \
                       f"**Unemployed**: {cd_data['Unemployed']} ({await percent_maker(cd_data['Unemployed'], total)}%)\n" \
                       f"**Not in labor force**: {cd_data['Not in labor force']} ({await percent_maker(cd_data['Not in labor force'], total)}%)\n" \
                       f"**Commutes alone by car**: {cd_data['Driving alone']} ({await percent_maker(cd_data['Driving alone'], cd_data['Employed'])}%)\n" \
                       f"**Commutes by carpools and taxis**: {cd_data['Carpools and taxis']} ({await percent_maker(cd_data['Carpools and taxis'], cd_data['Employed'])}%)\n" \
                       f"**Commutes by public transportation**: {cd_data['Public transportation (excluding taxis)']} ({await percent_maker(cd_data['Public transportation (excluding taxis)'], cd_data['Employed'])}%)\n" \
                       f"**Commutes by walking**: {cd_data['Walked']} ({await percent_maker(cd_data['Walked'], cd_data['Employed'])}%)\n" \
                       f"**Commutes by other means**: {cd_data['Other means']} ({await percent_maker(cd_data['Other means'], cd_data['Employed'])}%)\n" \
                       f"**Works from home**: {cd_data['Worked from home']} ({await percent_maker(cd_data['Worked from home'], cd_data['Employed'])}%)\n" \
                       f"**Mean travel time to work**: {cd_data['Mean travel time to work (minutes)']} minutes"
        embed.add_field(name="Election Data", value=election_data)
        embed.add_field(name="Education Data", value=education_data)
        embed.add_field(name="Housing Data", value=housing_data)
        embed.add_field(name="Urbanization Data", value=urbanization_data)
        embed.add_field(name="Population Data", value=employment_data)
        embed.add_field(name="Commute Data", value=commute_data)
        embed.set_footer(text="Election data is from DRA and OregonMapGuy. Education, housing, employment and commute data is from the Census/the American Community Survey. Urban data is from the Department of Housing and Urban Development.")
        await ctx.send(file=file, embed=embed)

    @commands.guild_only()
    @commands.hybrid_command(name="embed", help="Posts an embed.")
    async def __embed(self, ctx, title: str, content: str, field1title: str = None, field1content: str = None, field2title: str = None, field2content: str = None, imageurl: str = None):
        embed = embeds.twoembed(title, content)
        if field1title is not None and field1content is not None:
            embed.add_field(name=field1title, value=field1content, inline=False)
        if field2title is not None and field2content is not None:
            embed.add_field(name=field2title, value=field2content, inline=False)
        if imageurl is not None:
            embed.set_image(url=imageurl)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
