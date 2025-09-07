import os
import typing as t


from bot import Bot, Plugin
from bot.utils import load_env


class Env(dict):
    def __format__(self, format_spec: str, /) -> str:
        return "Env"


class EnvPlugin(Plugin[Bot]):
    async def load(self, client):
        env = load_env()
        client.d["env"] = Env(**env)

    async def unload(self, client):
        del client.d["env"]


__plugin__ = EnvPlugin()
