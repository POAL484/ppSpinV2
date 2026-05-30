from types_spin.eventable import *

import datetime as dt
from random import choice

async def init_storage(bot, storage):
    chnls = bot.db.getListChannelsEnabled(CfgInfoType.Event, "re")
    storage.emt = True
    storage.msg = {}
    for chnl in chnls:
        storage.msg[chnl] = False

async def tick_event(bot, chnl: str, storage):
    if dt.datetime.now().minute == 0 and storage.emt:
        for chnl in storage.msg.keys():
            if storage.msg[chnl]:
                await bot.get_channel(chnl).send(choice(bot.emts[chnl]))
                storage.msg[chnl] = False
        storage.emt = False
    elif dt.datetime.now().minute != 0: storage.emt = True

async def tick_event_on_message(bot, message, storage):
    storage.msg[message.channel.name] = True

strg = Storage(init_storage) # представьте ниже кастомизацию
Eventable(Eventable.EventType.TICK, CfgInfo({}, "Периодическое отправление случайного эмоута", {}, name = "re"), tick_event, strg)
Eventable(Eventable.EventType.MESSAGE, CfgInfo({}, "Служебный ивент для периодического отправления случайного эмоута", {}, name="re_msg"), tick_event_on_message, strg)