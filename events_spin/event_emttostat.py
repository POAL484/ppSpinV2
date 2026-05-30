from types_spin.eventable import *
from twitchio.message import Message

async def event(bot, message: Message):
    chnl_name = message.channel.name
    for word in message.content.split():
        if word in bot.emts[chnl_name]:
            for emt in bot.emts_by_name[chnl_name][word]:
                emtDb = bot.db.db.get_collection(f"emts.{chnl_name}").find_one({"pid": emt['pid']})
                if not emtDb:# and bot.platform_emts_by_name[chnl_name][word] in cfg['platforms']:
                    emtDb = {
                        "id": emt['id'], "name": word,
                        "used": 0, "pause": False, "platform": emt['platform'], "pid": emt['pid']
                    }
                    bot.db.db.get_collection(f"emts.{chnl_name}").insert_one(emtDb)
                if not emtDb['pause']:# and bot.platform_emts_by_name[chnl_name][word] in cfg['platforms']:
                    emtDb['used'] += 1
                    bot.db.db.get_collection(f"emts.{chnl_name}").find_one_and_replace({"pid": emt['pid']}, emtDb)

Eventable(Eventable.EventType.MESSAGE, CfgInfo({}, "Подсчет эмоутов в статистику", {}, name = "emtstat"), event)