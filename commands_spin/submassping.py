from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo, CfgInfoType

import types_spin.argsParser as argsParser

async def cmd(ctx: Context, action: str | None, event: str | None):
    for event_type in ["title", "online", "offline", "game"]:
        if ctx.bot.db.configs.chats.find_one({"name": ctx.channel.name, f"cfg.event.notify.massping.{event_type}.id": int(ctx.author.id), f"cfg.event.notify.massping.{event_type}.display": {"$ne": ctx.author.display_name}}):
            ctx.bot.db.configs.chats.find_one_and_update({"name": ctx.channel.name, f"cfg.event.notify.massping.{event_type}.id": int(ctx.author.id)}, {"$set": {f"cfg.event.notify.massping.{event_type}.$.display": ctx.author.display_name}})
    if not action:
        await ctx.reply(f"Ошибка: приведи действие: *notify r / + / -")
        return
    subscriable = []
    for event_type in ["title", "online", "offline", "game"]:
        if ctx.bot.db.getCfg(CfgInfoType.Event, "notify", ctx.channel.name)['messages'][event_type]['masspingEnabled']:
            subscriable.append(event_type)
    match action:
        case "r" | "read" | "get":
            if not event:
                events_subbed = []
                for event_type in ["title", "online", "offline", "game"]:
                    if ctx.bot.db.configs.chats.find_one({"name": ctx.channel.name, f"cfg.event.notify.massping.{event_type}.id": int(ctx.author.id)}):
                        events_subbed.append(event_type)
                if not events_subbed:
                    await ctx.reply("Ты не подписан на события")
                    return
                await ctx.reply(f"Ты подписан на: " + ", ".join(events_subbed))
                return
            if not event in subscriable:
                await ctx.reply(f"Ошибка: На это событие нельзя подписаться!")
                return
            if ctx.bot.db.configs.chats.find_one({"name": ctx.channel.name, f"cfg.event.notify.massping.{event}.id": int(ctx.author.id)}):
                await ctx.reply(f"Ты подписан на событие {event}!")
                return
            await ctx.reply(f"Ты не подписан на событие {event}")
        case "+" | "sub" | "notify" | "subscribe":
            if not event:
                await ctx.reply("Ошибка: событие не представлено. События: " + ", ".join(subscriable))
                return
            if not event in subscriable:
                await ctx.reply("Ошибка: на это событие нельзя подписаться!")
                return
            if ctx.bot.db.configs.chats.find_one({"name": ctx.channel.name, f"cfg.event.notify.massping.{event}.id": int(ctx.author.id)}):
                await ctx.reply("Ты уже подписан на это событие")
                return
            ctx.bot.db.configs.chats.find_one_and_update({"name": ctx.channel.name}, {"$push": {f"cfg.event.notify.massping.{event}": {"id": int(ctx.author.id), "display": ctx.author.display_name}}})
            await ctx.reply(f"Ты подписался на событие {event}!")
        case "-" | "unsub" | "unnotify" | "unsubscribe":
            if not event:
                await ctx.reply("Ошибка: событие не представлено. События: " + ", ".join(subscriable))
                return
            if not event in subscriable:
                await ctx.reply("Ошибка: это событие отлючено!")
                return
            if not ctx.bot.db.configs.chats.find_one({"name": ctx.channel.name, f"cfg.event.notify.massping.{event}.id": int(ctx.author.id)}):
                await ctx.reply("Ты не подписан на это событие")
                return
            ctx.bot.db.configs.chats.find_one_and_update({"name": ctx.channel.name}, {"$pull": {f"cfg.event.notify.massping.{event}": {"id": int(ctx.author.id)}}})
            await ctx.reply(f"Ты отписался от события {event}!")
        case _:
            await ctx.reply("Ошибка: неизвестное действие. Действия: r / + / -")

            

Cmd(CfgInfo({}, "Подписаться на события", {}), name = "submassping", aliases=["notify"], func = cmd)