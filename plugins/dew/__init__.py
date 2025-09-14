import dew

from bot import Core, Plugin


class DewParserPlugin(Plugin[Core]):
    async def on_load(self, core):
        core.d["dew"] = dew

    async def on_unload(self, core):
        del core.d["dew"]


__plugin__ = DewParserPlugin()
