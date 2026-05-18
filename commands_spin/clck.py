from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo
import requests as req

async def cmd(ctx: Context, url: str | None):
    if not url:
        await ctx.reply("А где ссылка братан")
        return
    await ctx.reply(f"Ссылка сокращена 👉  {req.get('https://clck.ru/--', params={'url': url}).text[:400]}")

Cmd(CfgInfo({}, "Сократить ссылку через кликер", {}), name="clck", func=cmd)