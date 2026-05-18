from twitchio.ext.commands import Context
from ..types_spin.cmd import Cmd, CfgInfo

from random import choice

async def cmd(ctx: Context):
    await ctx.reply(choice(Cmd.bot.emts[ctx.channel.name]))

Cmd(CfgInfo({}, "Случайный эмоут с канала", {}), name="re", func=cmd)