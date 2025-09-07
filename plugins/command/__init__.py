from __future__ import annotations

import logging

from bot import Bot, Plugin
from plugins.db import Pool
from plugins.command.di import DependencyInjector
from plugins.command.api import CommandClient
from plugins.command.commands import food_buff, info

logging = logging.getLogger(__name__)


class CommandPlugin(Plugin[Bot]):
    async def load(self, client: Bot):
        dependency_manager = DependencyInjector({})
        dependency_manager.set(Pool, client.d["pool"])

        command_client = CommandClient(di=dependency_manager, registry={})
        command_client.register(food_buff.addr)
        command_client.register(info.info)

        client.d["command_client"] = command_client
        client.pipeline.append(command_client.execute)

    async def unload(self, client):
        del client.d["command_client"]


__plugin__ = CommandPlugin()
