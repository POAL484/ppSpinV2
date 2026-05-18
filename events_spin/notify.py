from ..types_spin.cmd import *
from ..types_spin.eventable import *
import utils

import datetime as dt

async def makeMessage(bot, cfg: dict, chnl: str, eventType: str):
    if not cfg['messages'][eventType]['announce']:
        await bot.get_channel(chnl).send(cfg['messages'][eventType]['msg'].replace("-title", cfg['lastData']['title']).replace("-game", cfg['lastData']['game_name']))
    else:
        pu = bot.create_user(bot.db.configs.chats.find_one({"name": chnl})['id'], chnl)
        await pu.chat_announcement(bot.botConfig.token, bot.botUser.id, cfg['messages'][eventType]['msg'].replace("-title", cfg['lastData']['title']).replace("-game", cfg['lastData']['game_name']))
    if cfg['messages'][eventType]['masspingEnabled']:
        tblk = cfg['messages'][eventType]['massping']
        em1 = cfg['messages'][eventType]['mStart']
        em2 = cfg['messages'][eventType]['mEnd']
        if not em1: em1 = ''
        if not em2: em2 = ''
        await utils.more500send(" ".join(tblk), bot.get_channel(chnl), em1, em2)

async def init_storage(bot, storage):
    storage.timer = dt.datetime.now()

async def tick_event(bot, chnl: str, storage):
    #if (dt.datetime.now() - storage.timer).total_seconds() < 5: return 
    #storage.timer = dt.datetime.now()
    #for chnl in bot.db.getListChannelsEnabled(CfgInfoType.Event, "notify"):
    cfg = bot.db.getCfg(CfgInfoType.Event, "notify", chnl)
    if not cfg: return
    if cfg['eventsEnabled']['title']:
        info = await bot.fetch_channel(chnl)
        if info.title != cfg['lastData']['title']:
            cfg['lastData']['title'] = info.title
            bot.db.updateCfg(CfgInfoType.Event, "notify", chnl, cfg)
            await makeMessage(bot, cfg, chnl, "title")
        if info.game_id != cfg['lastData']['game_id']:
            cfg['lastData']['game_id'] = info.game_id
            cfg['lastData']['game_name'] = info.game_name
            bot.db.updateCfg(CfgInfoType.Event, "notify", chnl, cfg)
            await makeMessage(bot, cfg, chnl, "game")
    if cfg['eventsEnabled']['online'] or cfg['eventsEnabled']['offline']:
        info_chnls = await bot.search_channels(chnl)
        info = None
        for j in info_chnls:
            if j.name == chnl: info = j
        if not info: return
        if info.live and not cfg['lastData']['online']:
            cfg['lastData']['online'] = True
            bot.db.updateCfg(CfgInfoType.Event, "notify", chnl, cfg)
            await makeMessage(bot, cfg, chnl, "online")
        elif not info.live and cfg['lastData']['online']:
            cfg['lastData']['online'] = False
            bot.db.updateCfg(CfgInfoType.Event, "notify", chnl, cfg)
            await makeMessage(bot, cfg, chnl, "offline")



Eventable(Eventable.EventType.TICK,
          CfgInfo({
              "lastData": {"title": "", "online": False, "game_id": "", "game_name": ""}, \
              "eventsEnabled": {"title": False, "online": False, "offline": False, "game": False},
              "messages": {"title": {"msg":"", "masspingEnabled": False, "mStart": "", "mEnd": "", "massping": [], "announce": False},
                           "online": {"msg":"", "masspingEnabled": False, "mStart": "", "mEnd": "", "massping": [], "announce": False},
                           "offline": {"msg":"", "masspingEnabled": False, "mStart": "", "mEnd": "", "massping": [], "announce": False},
                           "game": {"msg":"", "masspingEnabled": False, "mStart": "", "mEnd": "", "massping": [], "announce": False}}},
          "Уведомления о событиях: смена названия стрима, начало/конец стрима, смена категории стрима",
          {
              "lastData": {"title": "Служебное: последнее название стрима", "online": "Служебное: включен ли стрим", "game_id": "Служебное: id последней категории стрима", "game_name": "Служебное: название последней категории стрима"},
              "eventsEnabled": {"title": "Включено ли уведомление о смене названия стрима", "online": "Включено ли уведомление о начале стрима", "offline": "Включено ли уведомление об окончании стрима", "game": "Включено ли уведомление о смене категории"},
              "messages": {"title": {"msg": "Сообщение во время события", "masspingEnabled": "Включено/ны сообщение/ия массового пинга. Также настраивать возможность подписаться на событие в *submassping", "mStart": "Начало сообщения/ий массового пинга", "mEnd": "Окончание сообщения/ий массового пинга", "massping": "Пользователи, подписавшиеся на событие", "announce": "Использовать ли /announce для сообщения оповещения"},
                           "online": {"msg": "Сообщение во время события", "masspingEnabled": "Включено/ны сообщение/ия массового пинга. Также настраивать возможность подписаться на событие в *submassping", "mStart": "Начало сообщения/ий массового пинга", "mEnd": "Окончание сообщения/ий массового пинга", "massping": "Пользователи, подписавшиеся на событие", "announce": "Использовать ли /announce для сообщения оповещения"},
                           "offline": {"msg": "Сообщение во время события", "masspingEnabled": "Включено/ны сообщение/ия массового пинга. Также настраивать возможность подписаться на событие в *submassping", "mStart": "Начало сообщения/ий массового пинга", "mEnd": "Окончание сообщения/ий массового пинга", "massping": "Пользователи, подписавшиеся на событие", "announce": "Использовать ли /announce для сообщения оповещения"},
                           "game": {"msg": "Сообщение во время события", "masspingEnabled": "Включено/ны сообщение/ия массового пинга. Также настраивать возможность подписаться на событие в *submassping", "mStart": "Начало сообщения/ий массового пинга", "mEnd": "Окончание сообщения/ий массового пинга", "massping": "Пользователи, подписавшиеся на событие", "announce": "Использовать ли /announce для сообщения оповещения"}},
          }, name="notify"),
          tick_event, Storage(init_storage))

"""

[events] - title, online, offline, game
[eventData]:
    title - str,
    online - bool,
    game - str

lastData:
    [eventData]
eventsEnabled:
    [events] - bool
messages:
    [events]:
        msg - str
        masspingEnabled - bool
        mStart - str
        mEnd - str
        massping - list[str]
        announce - bool

"""