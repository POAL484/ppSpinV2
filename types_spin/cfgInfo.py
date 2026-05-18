from enum import Enum

class CfgInfoType(Enum):
    Cmd = "cmd"
    Event = "event"

class CfgInfo:
    def __init__(self, cfgKeys: dict, help: str, helpCfg: dict, name: str = ""):
        self.name = name
        self.cfgKeys = cfgKeys
        self.help = help
        self.helpCfg = helpCfg
        self.type = CfgInfoType.Cmd