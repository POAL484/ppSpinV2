from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo

async def cmd(ctx: Context):
    if not Cmd.bot.check_mod(ctx.author.id): return
    await ctx.reply("Alright ...")
    await Cmd.bot.join_channels(['the_il_'])


Cmd(CfgInfo({}, "test", {}), name = "test123", func = cmd)