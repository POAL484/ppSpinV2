from twitchio.ext.commands import Context
from ..types_spin.cmd import Cmd, CfgInfo
from random import randint

async def cmd(ctx: Context):
    if randint(0, 5):
        await ctx.reply("Ты выжил в русской рулетке! stare")
        return
    await ctx.reply("Ты проиграл в русской рулетке! Tomato")
    await (await ctx.channel.user()).timeout_user(ctx.bot.botConfig.token, ctx.bot.botUser.id, ctx.author.id, 60, "Проиграл в русской рулетке!")

Cmd(CfgInfo({}, "Русская рулетка", {}), name = "rr", func = cmd) # можно добавить кфг времени