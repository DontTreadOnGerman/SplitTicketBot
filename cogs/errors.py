from discord.ext import commands
import discord
import traceback
import sys
from utils import embeds


class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return
        if isinstance(error, commands.DisabledCommand):
            await ctx.send(embed=embeds.twoembed("This command is disabled!", "Sorry."))
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(embed=embeds.twoembed("You can't use this here!", "Sorry."))
            except discord.HTTPException:
                pass
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=embeds.twoembed("Bad argument error!", "Sorry."))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=embeds.twoembed("Missing required argument!", "Sorry."))
        else:
            await ctx.send(embed=embeds.twoembed("Unknown error detected!", str(type(error).__name__)+": "+str(error)))
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


async def setup(bot):
    await bot.add_cog(ErrorHandling(bot))
