from ..types_spin.cmd import Cmd, CfgInfo
from twitchio.ext.commands import Context

async def cmd(ctx: Context):
    if not Cmd.bot.check_mod(ctx.author.id): return
    await Cmd.bot.logger("bot off requested")
    await ctx.send("Бот выключен frame145delay007s")
    await Cmd.bot.close()

Cmd(CfgInfo({}, "Служебная команда", {}), name="offpenis", func=cmd)