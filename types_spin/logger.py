from twitchio.channel import Channel

class Logger:
    def __init__(self, chnl_inst: Channel):
        self.chnl = chnl_inst
        '''with open("logs.txt", 'w') as wl:
            wl.write("log created")'''

    async def __call__(self, data: str):
        await self.chnl.send(data)
        '''with open("logs.txt", 'a') as wl:
            wl.write("\n" + data)'''