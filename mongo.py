import pymongo as mng
from .types_spin.cfgInfo import CfgInfo, CfgInfoType

class Db:
    def __init__(self, host="mongodb://localhost:27017"):
        self.db = mng.MongoClient(host).ppspin
        self.configs = self.db.configs

    def getCfg(self, cfgInfoType: CfgInfoType, name: str, chnl_name: str):
        chnl_name = chnl_name.lower()
        if not self.configs.chats.find_one({"name": chnl_name}): return {"enabled": False}
        if name in self.configs.chats.find_one({"name": chnl_name})['cfg'][cfgInfoType.value].keys():
            return self.configs.chats.find_one({"name": chnl_name})['cfg'][cfgInfoType.value][name]
        return {"enabled": False}
    
    def updateCfg(self, cfgInfoType: CfgInfoType, name: str, chnl_name: str, cfg: dict):
        chnl_name = chnl_name.lower()
        chnlCfg = self.configs.chats.find_one({"name": chnl_name})
        chnlCfg['cfg'][cfgInfoType.value][name] = cfg
        self.configs.chats.find_one_and_replace({"name": chnl_name}, chnlCfg)
        
    
    def getListChannelsEnabled(self, cfgInfoType: CfgInfoType, name: str):
        chnls = []
        for i in self.configs.chats.find({}):
            if not name in i['cfg'][cfgInfoType.value].keys(): continue
            if i['cfg'][cfgInfoType.value][name]['enabled']: chnls.append(i['name'])
        return chnls
    
    def rebuildChannelsCfg(self, cfgInfoList: list[CfgInfo]):

        def recCheck(dictDefs: dict, cfg: dict):
            for key in dictDefs.keys():
                if isinstance(dictDefs[key], dict):
                    if not key in cfg.keys(): cfg[key] = {}
                    if not isinstance(cfg[key], dict): cfg[key] = {}
                    cfg[key] = recCheck(dictDefs[key], cfg[key])
                    continue
                if not key in cfg.keys():
                    cfg[key] = dictDefs[key]
                    continue
                if not type(dictDefs[key]) == type(cfg[key]):
                    cfg[key] = dictDefs[key]
            return cfg

        for chnl in self.configs.chats.find({}):
            if not 'cfg' in chnl.keys():
                chnl['cfg'] = {"cmd": {}, "event": {}}
            if not 'cmd' in chnl['cfg']:
                chnl['cfg']['cmd'] = {}
            if not 'event' in chnl['cfg']:
                chnl['cfg']['event'] = {}
            for cfgInfo in cfgInfoList:
                if not cfgInfo.name in chnl['cfg'][cfgInfo.type.value].keys():
                    chnl['cfg'][cfgInfo.type.value][cfgInfo.name] = {}
                if not isinstance(chnl['cfg'][cfgInfo.type.value][cfgInfo.name], dict):
                    chnl['cfg'][cfgInfo.type.value][cfgInfo.name] = {}
                chnl['cfg'][cfgInfo.type.value][cfgInfo.name] = recCheck(cfgInfo.cfgKeys, chnl['cfg'][cfgInfo.type.value][cfgInfo.name])
            self.configs.chats.find_one_and_replace({"name": chnl['name']}, chnl)


if __name__ == "__main__":
    db = Db()
