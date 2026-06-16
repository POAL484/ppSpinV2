from types_spin.eventable import *
import utils

async def event(msg: dict):
    await Eventable.bot.logger("test ws")
    await (Eventable.bot.get_channel("poal48")).send("test ws")
    await utils.more500send(msg['msg']['text'], Eventable.bot.get_channel("poal48"))

Eventable(Eventable.EventType.TEST, CfgInfo({}, "test", {}, name = "test_ws"), event)