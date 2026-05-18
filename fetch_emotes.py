import requests as req
from time import sleep

import botconfig

proxies = None

#if botconfig.BotConfig.cfg.PROXY_7TV:
#    proxies = {'http': botconfig.BotConfig.cfg.PROXY_7TV, 'https': botconfig.BotConfig.cfg.PROXY_7TV}

def get_7tv_emote(emote_object: dict):
    return {"name": emote_object['name'], "id": emote_object['id'], "platform": "7tv"}
def get_ffz_emote(emote_object: dict):
    return {"name": emote_object['name'], "id": emote_object['id'], "platform": "ffz"}
def get_bttv_emote(emote_object: dict):
    return {"name": emote_object['code'], "id": emote_object['id'], "platform": "bttv"}

def get_name(emote_object: dict): return emote_object['name']
def get_id(emote_object: dict): return emote_object['id']
def get_named_id(emote_object: dict): return {emote_object['name']: emote_object['id']}
def get_named_platform(emote_object: dict): return {emote_object['name']: emote_object['platform']}

def fetch_7tv(twitch_id: int):
    #resp = req.get(f"https://7tv.io/v3/emote-sets/{set_id}").json()
    resp = req.get(f"https://7tv.io/v3/users/twitch/{twitch_id}", proxies=proxies).json()
    return list(map(get_7tv_emote, resp['emote_set']['emotes']))

def fetch_bttv(twitch_id: int):
    bttv =  req.get(f"https://api.betterttv.net/3/cached/users/twitch/{twitch_id}").json()
    if 'message' in bttv.keys(): return []
    return list(map(get_bttv_emote, bttv['channelEmotes']))

def fetch_ffz(twitch_id: int):
    ffzEmotes = req.get(f"https://api.frankerfacez.com/v1/room/id/{twitch_id}").json()
    if 'error' in ffzEmotes.keys(): return []
    ffzEmotes = ffzEmotes['sets'][list(ffzEmotes['sets'].keys())[0]]['emoticons']
    return list(map(get_ffz_emote, ffzEmotes))

async def fetch_channel(bot, twitch_id: int):
    emts = []
    try:
        emts.extend(fetch_7tv(twitch_id))
        emts.extend(fetch_bttv(twitch_id))
        emts.extend(fetch_ffz(twitch_id))
    except Exception as e:
        await bot.logger(f"Не удалось обновить эмоуты {twitch_id}: {e}")
    return emts
    