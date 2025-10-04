import logging
import typing as t

from dataclasses import dataclass
import linkd
import dew


from modules.cmd.api import CommandTree, create_root
from yui import Kernel
from yui.types import MaybeAwaitable


logger = logging.getLogger("yui.cmd")


def load_cmd_module(kernel: Kernel):
    kernel.cache["__CMD_API__"] = create_root("/")
    kernel.cache["__CMD_DI_API__"] = linkd.DependencyInjectionManager()

    # Default Dependency Injection
    di = t.cast(linkd.DependencyInjectionManager, kernel.cache["__CMD_DI_API__"])
    di.registry_for(linkd.Contexts.ROOT).register_value(Kernel, kernel)

    # legacy '>' commands
    kernel.cache["__LEGACY_CMD_API__"] = create_root(">")
    kernel.cache["__LEGACY_CMD_DI_API__"] = linkd.DependencyInjectionManager()

    # Default Legacy Dependency Injection
    di = t.cast(linkd.DependencyInjectionManager, kernel.cache["__LEGACY_CMD_DI_API__"])
    di.registry_for(linkd.Contexts.ROOT).register_value(Kernel, kernel)


def unload_cmd_module(kernel: Kernel):
    del kernel.cache["__CMD_API__"]
    del kernel.cache["__CMD_DI_API__"]


@dataclass
class CommandReceivedEvent:
    cmd: str
    kernel: Kernel


async def execute_legacy_command(event: CommandReceivedEvent):
    di = t.cast(linkd.DependencyInjectionManager, event.kernel.cache["__LEGACY_CMD_DI_API__"])

    tree = t.cast(CommandTree, event.kernel.cache["__LEGACY_CMD_API__"])

    prefix = ">"
    if event.cmd.startswith(prefix):
        cmd = event.cmd[1:]

        command_sequence = dew.get_keyword_seq(dew.parse(cmd))

        func = t.cast(
            t.Callable[..., MaybeAwaitable[t.Any | None]], tree.get_tree([prefix, *command_sequence]).data.func
        )

        di_injected_func = di.contextual(linkd.Contexts.ROOT)(linkd.inject(func))

        result = await di_injected_func()

        print(result)

    else:
        logger.debug(f"cmd is not recognized as it is not starting with prefix '{prefix}'")


async def load(kernel: Kernel):
    load_cmd_module(kernel)

    # for capturing events that needs commands
    kernel.event_manager.add_event(CommandReceivedEvent)
    kernel.event_manager.subscribe(CommandReceivedEvent, execute_legacy_command)


async def unload(kernel: Kernel):
    unload_cmd_module(kernel)

    kernel.event_manager.unsubscribe(CommandReceivedEvent, execute_legacy_command)
    kernel.event_manager.remove_event(CommandReceivedEvent)
