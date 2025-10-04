import typing as t

from yui import Kernel

from modules.cmd.api import CommandTree
from modules.toram.commands.food_buff import addr
from modules.toram.commands.info import info


async def load(kernel: Kernel):
    # LEGACY CMD FOR NOW
    root = t.cast(CommandTree, kernel.cache["__LEGACY_CMD_API__"])
    root.add_tree(addr)
    root.add_tree(info)


async def unload(kernel: Kernel):
    # TODO: ADD REMOVE TREE MECHANISM
    pass
