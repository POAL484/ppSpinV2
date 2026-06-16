from enum import Enum
from .storage import Storage
from .cfgInfo import CfgInfo, CfgInfoType

class Eventable:
    insts = []
    bot = None
    class EventType(Enum): MESSAGE = 1; TICK = 2; TEST = 3
    def __init__(self, target: EventType, cfgInfo: CfgInfo, func, storage: Storage|None = None):
        self.__class__.insts.append(self)
        self.target = target
        self.func = func
        self.storage = storage
        cfgInfo.cfgKeys['enabled'] = False
        cfgInfo.helpCfg['enabled'] = "Включен ли ивент"
        cfgInfo.type = CfgInfoType.Event
        if not cfgInfo.name:
            raise Exception("Не указано название для одного из ивентов")
        self.cfgInfo = cfgInfo

async def pingEvent(target: Eventable.EventType, *args):
    for event in Eventable.insts:
        if event.target == target:
            if target == Eventable.EventType.MESSAGE:
                if not Eventable.bot.db.getCfg(CfgInfoType.Event, event.cfgInfo.name, args[1].channel.name)["enabled"]: break
                if event.storage: await event.func(*args, event.storage)
                else: await event.func(*args)
            elif target == Eventable.EventType.TICK:
                for chnl in Eventable.bot.db.getListChannelsEnabled(CfgInfoType.Event, event.cfgInfo.name):
                    if event.storage: await event.func(*args, chnl, event.storage)
                    else: await event.func(*args, chnl)
            elif target == Eventable.EventType.TEST:
                await event.func(*args)