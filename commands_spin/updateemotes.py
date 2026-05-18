from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo

async def cmd(ctx: Context):
    if not Cmd.bot.check_mod(ctx.author.id): return
    await Cmd.bot.update_channels_emotes()
    await ctx.reply("Эмоуты обновлены Chillin")

Cmd(CfgInfo({}, "Служебная команда для обновления эмоутов", {}), name="updateemotes", func=cmd)