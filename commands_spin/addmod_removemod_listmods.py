from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo
from utils import more500send

async def cmd_addmod(ctx: Context, user: str):
    if int(ctx.author.id) != 276061388: return
    us = (await ctx.bot.fetch_channel(user)).user
    if Cmd.bot.db.configs.mods.find_one({"user": user.lower()}):
        await ctx.reply(f"plenk Пользователь {user} уже модератор!")
        return
    Cmd.bot.db.configs.mods.insert_one({"user": user.lower(), "id": int(us.id)})
    await ctx.reply(f"plinkVibe Пользователь {user} теперь модератор")

async def cmd_removemod(ctx: Context, user: str):
    if int(ctx.author.id) != 276061388: return
    if not Cmd.bot.db.configs.mods.find_one({"user": user.lower()}):
        await ctx.reply(f"plenk Пользователь {user} не был модератором!")
        return
    Cmd.bot.db.configs.mods.delete_one({"user": user.lower()})
    await ctx.reply(f"plink Пользователь {user} больше не модератор")

async def cmd_listmods(ctx: Context):
    mods = list(map(lambda us: 'X' + us['user'], Cmd.bot.db.configs.mods.find({})))
    await more500send("Список модераторов бота: " + ", ".join(mods), ctx)


Cmd(CfgInfo({}, "Добавить модератора в бота", {}), name = "addmod", func = cmd_addmod)
Cmd(CfgInfo({}, "Убрать модератора из бота", {}), name = "removemod", func = cmd_removemod)
Cmd(CfgInfo({}, "Посмотреть список модераторов бота", {}), name = "listmods", func = cmd_listmods, aliases=["mods"])