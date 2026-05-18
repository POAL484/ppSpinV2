from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo

async def cmd(ctx: Context, emt_name: str | None):
    if not emt_name:
        await ctx.reply("Не приведен эмоут")
        return
    emt = ctx.bot.db.db.get_collection(f"emts.{ctx.channel.name}").find_one({"name": emt_name})
    if not emt:
        await ctx.reply("Информация об эмоуте отсуствует 🤨")
        return
    await ctx.reply(f"{emt_name} {emt['platform']} emote, used time: {emt['used']}")

Cmd(CfgInfo({}, "Идивидуальная статистика эмоута", {}), name="estat", func=cmd)