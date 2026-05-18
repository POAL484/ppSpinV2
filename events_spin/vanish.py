from ..types_spin.eventable import *
from twitchio.message import Message

async def on_message(bot, message: Message):
    if "vanishme" in message.content.lower().split() or "мфтшырьу" in message.content.lower().split():
        pu = bot.create_user(bot.db.configs.chats.find_one({"name": message.channel.name})['id'], message.channel.name)
        await pu.timeout_user(bot.botConfig.token, bot.botUser.id, message.author.id, 1, "пипо ваниш")


Eventable(Eventable.EventType.MESSAGE, CfgInfo({}, "Удаление всех сообщений пользователя", {}, name = "vanish"), on_message)