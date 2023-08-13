import discord
import datetime
from discord.ext import commands


class InfoButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="SplitTicket Website", url="https://split-ticket.org/"))
        self.add_item(discord.ui.Button(label="SplitTicket Twitter/X", url="https://twitter.com/splitticket_"))
        self.add_item(discord.ui.Button(label="SplitTicket Subreddit", url="https://reddit.com/r/splitticket"))
        self.add_item(discord.ui.Button(label="Bot Source Code", url="https://github.com/DontTreadOnGerman/SplitTicketBot"))


class Help(commands.Cog, name="Help \U0001F4D2"):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="info", help="Bot info and SplitTicket info.")
    async def info(self, ctx):
        embed = discord.Embed(colour=0xBF64DB, title="Info", timestamp=datetime.datetime.now())
        embed.add_field(name="SplitTicket Info", value="SplitTicket is a group of political and election enthusiasts who first became interested in mapping and modeling elections through a community on Twitter called #ElectionTwitter."
                                                       "\n[Click here for further info.](https://split-ticket.org/about-us/)\n")
        embed.add_field(name="SplitTicket Partners", value="Don't excessively bother a partner.\n"
                                                           "- <@656342666849812491>/[Lakshya Jain](https://twitter.com/lxeagle17)\n"
                                                           "- Leon Sit (Managing editor and graphics)\n"
                                                           "- <@679078181332058124>/[Harrison Lavelle](https://twitter.com/HWLavelleMaps)\n"
                                                           "- <@1001970059029270649>/[Armin Thomas/Thorongil](https://twitter.com/Thorongil16)\n"
                                                           "- <@1042960326582353941>/Claire Considine\n")
        # if you make a GitHub commit feel free to add yourself
        embed.add_field(name="Bot Info", value="This bot was developed to facilitate the SplitTicket discord server.\n"
                                               "The primary function of this bot is to automatically post SplitTicket articles to <#1042967487827951656>, but this bot also has other cool commands that you can explore using the help command."
                                               "\n**Bot Developers**\n"
                                               "<@720330422726164500>: Owner and hoster",
                        inline=False)
        await ctx.send(embed=embed, view=InfoButtons())

    @commands.guild_only()
    @commands.hybrid_command(name="help", help="Why bother reading about what this is?")
    async def help(self, ctx):
        embed_var = discord.Embed(colour=0xBF64DB, title="Help", timestamp=datetime.datetime.now())
        cogs = {}
        for cog in self.bot.cogs:
            for command in self.bot.get_cog(cog).walk_commands():
                command_name = command.name
                try:
                    command_details = command.help
                except Exception:
                    command_details = command.description
                if cog == "Jishaku":
                    cogs[cog] = f"**``jishaku``**: The Jishaku menu - not available as a slash command." \
                                f" (*This command on its own is a status brief. You can't use the subcommands.*)"
                else:
                    try:
                        command_parent = command.parent.name
                    except Exception:
                        if cog in list(cogs.keys()):
                            cogs[cog] += f"\n**``{command_name}``**: {command_details}"
                        else:
                            cogs[cog] = f"**``{command_name}``**: {command_details}"
                    else:
                        if cog in list(cogs.keys()):
                            cogs[cog] += f"\n**• ``{command_parent} {command_name}``**: {command_details}"
                        else:
                            cogs[cog] = f"**• ``{command_parent} {command_name}``**: {command_details}"
        for cog in list(sorted(cogs.keys())):
            name = cog
            if cog == "Jishaku":
                name = "Jishaku \U0001F9F2"
            embed_var.add_field(name=name, value=cogs[cog], inline=False)
        await ctx.send(embed=embed_var)


async def setup(bot):
    await bot.add_cog(Help(bot))
