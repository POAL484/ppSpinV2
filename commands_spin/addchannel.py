from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo

async def cmd(ctx: Context, name: str, id: int):
    if not Cmd.bot.check_mod(ctx.author.id): return
    Cmd.bot.db.configs.chats.insert_one({"name": name.lower(), "id": id, "cfg": {}})
    Cmd.bot.db.db.create_collection(f"emts.{name.lower()}")
    Cmd.bot.db.db.get_collection(f"emts.{name.lower()}").create_index({"title": "name", "content": "text"})
    Cmd.bot.emts[name.lower()] = []
    Cmd.bot.emts_by_name[name.lower()] = {}
    await Cmd.bot.update_channels()
    await ctx.reply(f"Канал {name} добавлен! Alright")

Cmd(CfgInfo({}, "Добавить бота на канал", {}), name = "addchannel", func = cmd)