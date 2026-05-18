from twitchio.ext.commands import Context
from types_spin.cmd import Cmd, CfgInfo
from types_spin.argsParser import parse

async def cmd(ctx: Context):
    if int(ctx.author.id) == 276061388:
        print("plenk")
        cnt = " ".join(parse(ctx.message.content))
        try:
            cnt = cnt.replace("=n ", "\n")
            cnt = cnt.replace("=t ", "    ")
            ctx.write = None
            print(f"cnt: {cnt}")
            exec(cnt)
            if ctx.write != None: await ctx.send(str(ctx.write))
        except Exception as e:
            await ctx.send(f"THIS эта ошибка возникла! {e}")

Cmd(CfgInfo({}, "", {}), name="execute", aliases=['exec'], func=cmd)
