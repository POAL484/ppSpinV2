import os
from dotenv import load_dotenv

ENVKEYS = ['IS_DEV', 'TOKEN', 'TOKEN_DEV', 'MONGODB_HOST', 'PROXY', 'INTERNAL_API', 'IAPI_TOKEN']

class BotConfig:
    cfg = None
    def __init__(self):
        self.__class__.cfg = self
        try:
            os.environ[ENVKEYS[0]]
        except KeyError:
            load_dotenv()
        try:
            for envkey in ENVKEYS:
                self.__setattr__(envkey, os.environ[envkey])
        except KeyError:
            print("ENV VARS ERROR, please check env vars contains all needed parameters")
            exit()
        self.token = self.TOKEN_DEV if self.IS_DEV == "true" else self.TOKEN