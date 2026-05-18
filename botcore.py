from twitchio.ext import commands
from twitchio.ext.commands.core import Context
import twitchio as tio
import datetime as dt
import threading as thrd

import botconfig
import mongo
from types_spin.logger import *
import utils

from types_spin.cmd import *
from types_spin.eventable import *

from commands_spin import *
from events_spin import *

import fetch_emotes

class Bot(commands.Bot):

    def __init__(self, botConfig: botconfig.BotConfig):
        print("Starting...")
        self.botConfig = botConfig
        self.block = True
        print(f"Connecting to mongo at: {botConfig.MONGODB_HOST.split('@')[-1]}")
        self.db = mongo.Db(botConfig.MONGODB_HOST)
        print("Mongo connected")
        super().__init__(token=botConfig.token, prefix="*", initial_channels=["ppspin", "poal48"])
        print("Client inited")
        self.start_time = dt.datetime.now()
        Cmd.bot = self
        Eventable.bot = self
        for cmd in Cmd.insts:
            print(f"registred command: {cmd.name}")
            self.add_command(cmd)

    async def invoke(self, context: Context):
        if not context.command: return
        if not self.db.getCfg(CfgInfoType.Cmd, context.command.name, context.channel.name)['enabled']: return
        await super().invoke(context)

    async def event_message(self, message: tio.Message):
        if self.block: return
        if message.echo: return
        if self.db.configs.banned_users.find_one({"user": message.author.name.lower()}): return
        await pingEvent(Eventable.EventType.MESSAGE, self, message)
        await self.handle_commands(message)

    async def update_channels(self):
        chnls_connected = list(map(utils.get_name_in_Channel, self.connected_channels))
        chnls_config = list(map(lambda chnlCfg: chnlCfg['name'], self.db.configs.chats.find({})))
        chnls_config.append("ppspin")
        for chnl in chnls_config:
            if not chnl in chnls_connected:
                await self.join_channels((chnl, ))
        for chnl in chnls_connected:
            if not chnl in chnls_config:
                await self.part_channels((chnl, ))
        self.db.rebuildChannelsCfg(
            list(map(lambda cmd: cmd.cfgInfo, Cmd.insts)) + list(map(lambda event: event.cfgInfo, Eventable.insts))
        )
        await self.logger("channels updated")

    async def update_channels_emotes(self):
        self.emts = {}
        self.id_emts_by_name = {}
        self.platform_emts_by_name = {}
        for chnl in self.db.configs.chats.find({}):
            await self.logger(f"fetching x{chnl['name']} emotes")
            emts = await fetch_emotes.fetch_channel(self, chnl['id'])
            self.emts[chnl['name']] = list(map(fetch_emotes.get_name, emts))
            self.id_emts_by_name[chnl['name']] = {}
            self.platform_emts_by_name[chnl['name']] = {}
            for emote in list(map(fetch_emotes.get_named_id, emts)):
                self.id_emts_by_name[chnl['name']].update(emote)
            for emote in list(map(fetch_emotes.get_named_platform, emts)):
                self.platform_emts_by_name[chnl['name']].update(emote)
            await self.logger(f"x{chnl['name']}'s emotes fetched")

    async def event_ready(self):
        self.logger = Logger(self.get_channel("ppspin"))
        await self.logger("bot ready, updating the channels")
        await self.update_channels()
        await self.update_channels_emotes()
        for i in Storage.insts: await i.init(self, i)
        self.botUser = (await self.fetch_channel("ppspin")).user
        await self.logger("bot finally ready")
        print("ppSpin forsenRun")
        await self.get_channel("poal48").send("Подключен! ppSpin")
        #await utils.more500send("the_il_ brorAhuel "*500, self.get_channel("poal48"))
        #await utils.more500send("POAL48", self.get_channel("poal48"), "plenk", "plenk")
        self.block = False
        thrd.Thread(target=lambda: asyncio.run_coroutine_threadsafe(self.ticker(), self.loop)).start()

    async def ticker(self):
        while 1:
            await asyncio.sleep(0.05)
            await pingEvent(Eventable.EventType.TICK, self)

    def check_mod(self, twitch_id: int):
        if self.db.configs.mods.find_one({"id": int(twitch_id)}): return True
        return False
    
    """@commands.command(name="test")
    async def cmd_test(self, ctx: commands.Context):
        print(ctx.view.words)"""

print("Created")
bot = Bot(botconfig.BotConfig())
bot.run()