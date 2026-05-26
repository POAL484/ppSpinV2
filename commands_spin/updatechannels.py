from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo

async def cmd(ctx: Context):
    if not Cmd.bot.check_mod(ctx.author.id): return
    await ctx.reply("Alright ...")
    await Cmd.bot.update_channels()


Cmd(CfgInfo({}, "Обновить подключение к каналам", {}), name = "updatechannels", func = cmd)