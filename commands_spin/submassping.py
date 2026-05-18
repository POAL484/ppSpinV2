from twitchio.ext.commands import Context
from ..types_spin.cmd import Cmd, CfgInfo

import types_spin.argsParser as argsParser

async def cmd(ctx: Context):
    args = argsParser.parse(ctx.message.content)
    if args[0] in Cmd.bot.db.configs.chats.find_one({"name": ctx.channel.name})['submassping']['events']:
        pass
    else:
        await ctx.reply("На этот ивент нельзя записаться!!")

# а где