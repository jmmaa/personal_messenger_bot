from dataclasses import dataclass
import logging
import asyncio
import typing as t

import linkd
import dew


from yui import Kernel
from yui.types import MaybeAwaitable


from modules.cmd import CommandReceivedEvent
from modules.cmd.api import CommandTree
from modules.lifecycle import StartedEvent

logger = logging.getLogger("yui")


@dataclass
class InputReceivedEvent:
    inp: str
    kernel: Kernel


async def execute_legacy_command(event: InputReceivedEvent):
    di = t.cast(linkd.DependencyInjectionManager, event.kernel.cache["__LEGACY_CMD_DI_API__"])
    tree = t.cast(CommandTree, event.kernel.cache["__LEGACY_CMD_API__"])

    prefix = ">"
    if event.inp.startswith(prefix):
        inp = event.inp[1:]

        command_sequence = dew.get_keyword_seq(dew.parse(inp))

        func = t.cast(
            t.Callable[..., MaybeAwaitable[t.Any | None]], tree.get_tree([prefix, *command_sequence]).data.func
        )

        di_injected_func = di.contextual(linkd.Contexts.ROOT)(linkd.inject(func))

        result = await di_injected_func()

        print(result)

    else:
        logger.debug(f"cmd is not recognized as it is not starting with prefix '{prefix}'")


async def start_shell(event: StartedEvent):
    config = event.kernel.cache.get("__CONFIG__")

    if config:
        if config.bot.shell_mode:
            try:
                while True:
                    inp = input()
                    await event.kernel.event_manager.emit(InputReceivedEvent(inp, event.kernel))

            except asyncio.CancelledError as e:
                logger.debug(e)

            except Exception as e:
                logger.debug(e)


async def load(kernel: Kernel):
    kernel.event_manager.subscribe(StartedEvent, start_shell)

    # for capturing events that needs commands
    kernel.event_manager.add_event(InputReceivedEvent)
    kernel.event_manager.subscribe(InputReceivedEvent, execute_legacy_command)


async def unload(kernel: Kernel):
    kernel.event_manager.unsubscribe(StartedEvent, start_shell)

    kernel.event_manager.unsubscribe(InputReceivedEvent, execute_legacy_command)
    kernel.event_manager.remove_event(InputReceivedEvent)
