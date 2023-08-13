import discord
import datetime
from discord.ext import commands


class Help(commands.Cog, name="Help \U0001F4D2"):
    def __init__(self, bot):
        self.bot = bot

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
