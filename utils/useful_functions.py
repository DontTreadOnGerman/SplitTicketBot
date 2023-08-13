import datetime
import wavelink


async def not_connected(self, ctx):
    if not ctx.voice_client:
        vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        await ctx.guild.change_voice_state(channel=ctx.author.voice.channel,
                                           self_mute=False, self_deaf=True)
        self.recently_connected = datetime.datetime.now()
    else:
        vc = ctx.voice_client
    return [self.recently_connected, vc]


async def margin_fixer(margin):
    margin = str(margin)
    if "-" in margin:
        return margin.replace("-", "R+")
    else:
        return f"D+{margin}"


async def percent_maker(dividend, divisor):
    return round((dividend / divisor) * 100, 2)
