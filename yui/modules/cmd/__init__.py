import logging
import typing as t

import linkd

from yui.modules.cmd.api import create_root
from yui import Kernel


logger = logging.getLogger("yui.cmd")


def load_cmd_module(kernel: Kernel):
    # TODO: create a variable in cache for root name '/'

    kernel.store["__CMD_API__"] = create_root("/")
    kernel.store["__CMD_DI_API__"] = linkd.DependencyInjectionManager()

    # Default Dependency Injection
    di = t.cast(linkd.DependencyInjectionManager, kernel.store["__CMD_DI_API__"])
    di.registry_for(linkd.Contexts.ROOT).register_value(Kernel, kernel)

    # legacy '>' commands
    kernel.store["__LEGACY_CMD_API__"] = create_root(">")
    kernel.store["__LEGACY_CMD_DI_API__"] = linkd.DependencyInjectionManager()

    # Default Legacy Dependency Injection
    di = t.cast(linkd.DependencyInjectionManager, kernel.store["__LEGACY_CMD_DI_API__"])
    di.registry_for(linkd.Contexts.ROOT).register_value(Kernel, kernel)


def unload_cmd_module(kernel: Kernel):
    del kernel.store["__CMD_API__"]
    del kernel.store["__CMD_DI_API__"]


async def load(kernel: Kernel):
    load_cmd_module(kernel)


async def unload(kernel: Kernel):
    unload_cmd_module(kernel)
