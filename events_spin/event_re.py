from types_spin.eventable import *

import datetime as dt
from random import choice

# все переписать блять нахуй

async def init_storage(bot, storage):
    storage.activeInChnls = {}
    for i in bot.db.getListChannelsEnabled(CfgInfoType.Event, "re"):
        storage.activeInChnls[i] = True
    storage.emt = True

async def tick_event(bot, chnl: str, storage):
    if dt.datetime.now().minute == 0 and storage.emt:
        for i in storage.activeInChnls.keys():
            if storage.activeInChnls[i]:
                await bot.get_channel(i).send(choice(bot.emts[i]))
                storage.activeInChnls[i] = False
        storage.emt = False
    elif dt.datetime.now().minute != 0: storage.emt = True

async def tick_event_on_message(bot, message, storage):
    pass

strg = Storage(init_storage) # представьте ниже кастомизацию
Eventable(Eventable.EventType.TICK, CfgInfo({}, "Периодическое отправление случайного эмоута", {}, name = "re"), tick_event, strg)
Eventable(Eventable.EventType.MESSAGE, CfgInfo({}, "Служебный ивент для периодического отправления случайного эмоута", {}, name="re_msg"), tick_event_on_message, strg)