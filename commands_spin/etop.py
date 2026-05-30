from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo
from pymongo import DESCENDING

async def cmd(ctx: Context, *args):
    filter_ = {}
    for f in args:
        if len(f.split(":")) < 2:
            await ctx.reply(f"Ошибка: В фильтре {f} нету :")
            return
        if f.split(":")[0] == "search":
            stext = "".join(f.split(":")[1:])
            if "$" in stext: return
            filter_['$text'] = {"$search": stext}
        elif f.split(":")[0] == "platform":
            platforms = "".join(f.split(":")[1:]).split("&")
            for platform in platforms:
                if not Cmd.bot.db.db.get_collection(f"emts.{ctx.channel.name}").find_one({"platform": platform}):
                    await ctx.reply(f"Ошибка: Не найдено ни одного эмоута с платформы {platform} 🤨!")
                    return
            filter_['platform'] = {"$in": platforms}
        else:
            await ctx.reply(f"Ошибка: Фильтр {f.split(':')[0]} не найден!")
            return
    emts = Cmd.bot.db.db.get_collection(f"emts.{ctx.channel.name}").find(filter_, limit=5, sort=[("used", DESCENDING)])
    if not emts:
        await ctx.reply("Ошибка: Эмоутов по фильтрам не найдено!")
        return
    await ctx.reply(f"Топ 5 эмоутов: " + ", ".join(list(map(lambda e: f"#{e[0]+1} - {e[1]['name']} - {e[1]['used']} исп.", enumerate(emts)))))

Cmd(CfgInfo({}, "Топ эмоутов на канале", {}), name="etop", func=cmd)