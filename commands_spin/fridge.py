from twitchio.ext.commands import Context
from ..types_spin.cmd import Cmd, CfgInfo
import asyncio

async def cmd(ctx: Context):
    await ctx.send("ВОРУЮ ИЗ ТВОЕГО Fridge")
    await asyncio.sleep(10)
    await ctx.send("СВОРОВАЛ SOLE ИЗ ТВОЕГО Fridge")

Cmd(CfgInfo({}, "Лучшая команда бота", {}), name="Fridge", func=cmd)