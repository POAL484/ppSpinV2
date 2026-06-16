import requests as req
from time import sleep

import botconfig

proxies = None

if botconfig.BotConfig.cfg.PROXY:
    proxies = {'http': botconfig.BotConfig.cfg.PROXY, 'https': botconfig.BotConfig.cfg.PROXY}

def get_7tv_emote(emote_object: dict):
    return {"name": emote_object['name'], "id": emote_object['id'], "platform": "7tv", "pid": "7tv"+str(emote_object['id'])}
def get_ffz_emote(emote_object: dict):
    return {"name": emote_object['name'], "id": emote_object['id'], "platform": "ffz", "pid": "ffz"+str(emote_object['id'])}
def get_bttv_emote(emote_object: dict):
    return {"name": emote_object['code'], "id": emote_object['id'], "platform": "bttv", "pid": "bttv"+str(emote_object['id'])}

def get_name(emote_object: dict): return emote_object['name']
def get_id(emote_object: dict): return emote_object['id']
def get_named_id(emote_object: dict): return {emote_object['name']: emote_object['platform']+str(emote_object['id'])}
def get_named_platform(emote_object: dict): return {emote_object['name']: emote_object['platform']}

async def fetch_7tv(twitch_id: int, bot):
    resp = req.get(f"https://7tv.io/v3/users/twitch/{twitch_id}", proxies=proxies).json()
    if 'error' in resp.keys(): return []
    return list(map(get_7tv_emote, resp['emote_set']['emotes']))

async def fetch_bttv(twitch_id: int, bot):
    bttv =  req.get(f"https://api.betterttv.net/3/cached/users/twitch/{twitch_id}", proxies=proxies).json()
    if 'message' in bttv.keys(): return []
    return list(map(get_bttv_emote, bttv['channelEmotes']))

async def fetch_ffz(twitch_id: int, bot):
    ffzEmotes = req.get(f"https://api.frankerfacez.com/v1/room/id/{twitch_id}", proxies=proxies).json()
    if 'error' in ffzEmotes.keys(): return []
    ffzEmotes = ffzEmotes['sets'][list(ffzEmotes['sets'].keys())[0]]['emoticons']
    return list(map(get_ffz_emote, ffzEmotes))

async def fetch_channel(bot, twitch_id: int):
    emts = []
    try:
        emts.extend(await fetch_7tv(twitch_id, bot))
    except Exception as e:
        await bot.logger(f"Не удалось обновить эмоуты 7tv {twitch_id}")
    try:
        emts.extend(await fetch_bttv(twitch_id, bot))
    except Exception as e:
        await bot.logger(f"Не удалось обновить эмоуты bttv {twitch_id}")
    try:
        emts.extend(await fetch_ffz(twitch_id, bot))
    except Exception as e:
        await bot.logger(f"Не удалось обновить эмоуты ffz {twitch_id}")
    return emts
    