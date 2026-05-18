from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo
import datetime as dt
import utils

async def cmd(ctx: Context):
    await ctx.reply(f"plink Плиньк! | Хард ворк уже {utils.timecount(Cmd.bot.start_time)}")

Cmd(CfgInfo({}, "Проверка работоспособности бота", {}), name="ping", func=cmd)