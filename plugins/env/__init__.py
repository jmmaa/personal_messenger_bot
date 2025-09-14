import os

import typing as t


from bot import Core, Plugin

from bot.utils import load_env


class Env(dict):
    def __format__(self, format_spec: str, /) -> str:
        return "Env"


class EnvPlugin(Plugin[Core]):
    async def on_load(self, core):
        env = load_env()

        core.d["env"] = Env(**env)

    async def on_unload(self, core):
        del core.d["env"]


__plugin__ = EnvPlugin()
