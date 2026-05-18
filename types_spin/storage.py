

class Storage:
    insts = []
    def __init__(self, func_init):
        self.__class__.insts.append(self)
        self.init = func_init