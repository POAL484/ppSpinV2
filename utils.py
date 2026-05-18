from twitchio.channel import Channel
from twitchio.ext.commands import Context
import datetime as dt
import asyncio

def get_name_in_Channel(chnl: Channel):
    return chnl.name

def get_name_in_massping(massping_dict: dict):
    return massping_dict['name']

def timecount(dte):
    delta = dt.datetime.now() - dte
    sec = int(delta.total_seconds())
    rtrn = ''
    secs = sec//86400
    if secs != 0: rtrn += f'{secs} дней '
    sec -= secs*86400
    secs = sec//3600
    if secs != 0: rtrn += f'{secs} часов '
    sec -= secs*3600
    secs = sec//60
    if secs != 0: rtrn += f'{secs} мин '
    sec -= secs*60
    rtrn += f'{sec} сек'
    return rtrn

def split_by_space(string: str, limit: int = 490):
    m2 = string
    lines = []
    while len(m2) > limit:
        l = 0
        m = ''
        for i in m2.split():
            l += len(i)
            m += i
            m2 = m2[len(i)+1:]
            if l > limit:
                m = m[:-len(i)-1]
                m2 = i + " " + m2
                break
            l += 1
            m += ' '
        lines.append(m)
    return lines + [m2]

async def sendList(list: list, ctx: Context, delay: int = 0):
    for i in list:
        await ctx.send(i)
        await asyncio.sleep(delay)

async def more500send(content: str, ctx: Context, start: str = '', end: str = '', delay: int = 0):
    lines = split_by_space(content, 490-len(start)-len(end)-2)
    for i in range(len(lines)): lines[i] = start + ' ' + lines[i] + ' ' + end
    await sendList(lines, ctx, delay)