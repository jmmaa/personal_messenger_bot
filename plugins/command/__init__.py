from __future__ import annotations

import logging


from bot import Core, Plugin

from plugins.db import Pool

from plugins.command.di import DependencyInjector

from plugins.command.api import CommandClient

from plugins.command.commands import food_buff, info


logging = logging.getLogger(__name__)


class CommandPlugin(Plugin[Core]):
    async def on_load(self, core: Core):
        dependency_manager = DependencyInjector({})

        dependency_manager.set(Pool, core.d["pool"])

        command_client = CommandClient(di=dependency_manager, registry={})

        command_client.register(food_buff.addr)
        command_client.register(info.info)

        core.d["command_client"] = command_client

    async def unload(self, core):
        del core.d["command_client"]


__plugin__ = CommandPlugin()
