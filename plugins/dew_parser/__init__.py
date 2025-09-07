from dew import parse

from bot import Bot, Plugin


class DewParserPlugin(Plugin[Bot]):
    async def load(self, client):
        client.pipeline.append(parse)

    async def unload(self, client):
        client.pipeline.remove(parse)


__plugin__ = DewParserPlugin()
