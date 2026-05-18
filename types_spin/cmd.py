from twitchio.ext.commands import Command
from .cfgInfo import CfgInfo, CfgInfoType
#from botcore import Bot

class Cmd(Command):
    insts = []
    bot: None = None
    def __init__(self, cfgInfo: CfgInfo, *args, **kwargs):
        cfgInfo.cfgKeys['enabled'] = False
        cfgInfo.helpCfg['enabled'] = "Включена ли команда"
        cfgInfo.name = kwargs['name']
        cfgInfo.type = CfgInfoType.Cmd
        self.cfgInfo = cfgInfo
        self.__class__.insts.append(self)
        super().__init__(*args, **kwargs)