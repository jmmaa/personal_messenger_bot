import dew

from yui import Kernel


async def load(kernel: Kernel):
    kernel.cache["__COMMAND_PARSER__"] = dew.parse


async def unload(kernel: Kernel):
    del kernel.cache["__COMMAND_PARSER__"]
