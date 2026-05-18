from twitchio.ext.commands import Context
from ..types_spin.cmd import Cmd, CfgInfo

async def cmd_ban(ctx: Context, user: str):
    if not Cmd.bot.check_mod(ctx.author.id): return
    if Cmd.bot.db.configs.banned_users.find_one({"user": user.lower()}):
        await ctx.reply(f"plenk Пользователь {user} уже в бане!")
        return
    Cmd.bot.db.configs.banned_users.insert_one({"user": user.lower()})
    await ctx.reply(f"plinkVibe Пользователь {user} забанен!")

async def cmd_unban(ctx: Context, user: str):
    if not Cmd.bot.check_mod(ctx.author.id): return
    if not Cmd.bot.db.configs.banned_users.find_one({"user": user.lower()}):
        await ctx.reply(f"plenk Пользователь {user} не был в бане!")
        return
    Cmd.bot.db.configs.banned_users.delete_one({"user": user.lower()})
    await ctx.reply(f"plink Пользователь {user} теперь разбанен!")

Cmd(CfgInfo({}, "Забанить пользователя в боте", {}), name = "ban", func = cmd_ban)
Cmd(CfgInfo({}, "Разбанить пользователя в боте", {}), name = "unban", func = cmd_unban)