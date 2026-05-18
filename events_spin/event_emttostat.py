from ..types_spin.eventable import *
from twitchio.message import Message

async def event(bot, message: Message):
    chnl_name = message.channel.name
    for word in message.content.split():
        if word in bot.emts[chnl_name]:
            emt = bot.db.db.get_collection(f"emts.{chnl_name}").find_one({"name": word})
            if not emt:# and bot.platform_emts_by_name[chnl_name][word] in cfg['platforms']:
                emt = {
                    "id": bot.id_emts_by_name[chnl_name][word], "name": word,
                    "used": 0, "pause": False, "platform": bot.platform_emts_by_name[chnl_name][word]
                }
                bot.db.db.get_collection(f"emts.{chnl_name}").insert_one(emt)
            if not emt['pause']:# and bot.platform_emts_by_name[chnl_name][word] in cfg['platforms']:
                emt['used'] += 1
                bot.db.db.get_collection(f"emts.{chnl_name}").find_one_and_replace({"name": word}, emt)

Eventable(Eventable.EventType.MESSAGE, CfgInfo({}, "Подсчет эмоутов в статистику", {}, name = "emtstat"), event)