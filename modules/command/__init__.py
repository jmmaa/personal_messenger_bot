from __future__ import annotations

import logging


from modules.command.di import DependencyInjector
from modules.command.api import CommandClient
from modules.command.commands import food_buff, info
from yui.kernel import Kernel


logger = logging.getLogger("yui")


async def load(kernel: Kernel):
    dependency_manager = DependencyInjector({})

    command_client = CommandClient(di=dependency_manager, registry={})

    command_client.register(food_buff.addr)
    command_client.register(info.info)

    kernel.cache["__COMMAND_CLIENT__"] = command_client


async def unload(kernel: Kernel):
    del kernel.cache["__COMMAND_CLIENT__"]
