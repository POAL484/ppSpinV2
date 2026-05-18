from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo
from momsjokes import jokes
from random import choice

async def cmd(ctx: Context):
    await ctx.reply(choice(jokes))

Cmd(CfgInfo({}, "Случайная шутка про маму", {}), name="YOURMOM", func=cmd)