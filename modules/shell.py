import logging
import asyncio

from yui import Kernel
from modules.lifecycle import StartedEvent

logger = logging.getLogger("yui")


async def start_shell(event: StartedEvent):
    config = event.kernel.cache.get("__CONFIG__")
    command_client = event.kernel.cache.get("__COMMAND_CLIENT__")
    parse_command = event.kernel.cache.get("__COMMAND_PARSER__")

    if config and command_client and parse_command:
        if config.bot.shell_mode:
            try:
                while True:
                    inp = input()

                    if inp.startswith(config.bot.prefix):
                        cmd = inp[1:]

                        result = await command_client.execute(parse_command(cmd))

                        print(result)

            except asyncio.CancelledError as e:
                logger.debug(e)

            except Exception as e:
                logger.debug(e)


async def load(kernel: Kernel):
    kernel.event_manager.subscribe(StartedEvent, start_shell)


async def unload(kernel: Kernel):
    kernel.event_manager.unsubscribe(StartedEvent, start_shell)
