from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo

async def cmd(ctx: Context, emt_name: str | None, emt_index: str | None):
    if not emt_name:
        await ctx.reply("Не приведен эмоут")
        return
    emt = list(ctx.bot.db.db.get_collection(f"emts.{ctx.channel.name}").find({"name": emt_name}))
    if not emt:
        await ctx.reply("Информация об эмоуте отсуствует 🤨")
        return
    if len(emt) > 1:
        ind = emt_index if emt_index else 1
        try: ind = int(ind)
        except ValueError:
            await ctx.reply("Ошибка: Индекс не число!")
            return
        if ind-1 > len(emt) or ind < 1:
            await ctx.reply(f"Ошибка: Неправильный индекс эмоута, используй от 1 до {len(emt)}")
            return
        await ctx.reply(f"{emt_name} {emt[ind-1]['platform']} эмоут, использован: {emt[ind-1]['used']}. Найдено несколько эмоутов, используй *estat {emt_name} 1-{len(emt)}" + (". Эмоут на паузе" if emt[ind-1]['pause'] else ""))
    else:
        await ctx.reply(f"{emt_name} {emt[0]['platform']} эмоут, использован: {emt[0]['used']}" + (". Эмоут на паузе" if emt[0]['pause'] else ""))

Cmd(CfgInfo({}, "Идивидуальная статистика эмоута", {}), name="estat", func=cmd)