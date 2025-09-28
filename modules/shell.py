import logging


from yui import Kernel
from modules.lifecycle import StartedEvent

logger = logging.getLogger("yui")


async def start_shell(event: StartedEvent):
    config = event.kernel.cache.get("__CONFIG__")

    if config:
        if config.bot.shell_mode:
            try:
                while True:
                    inp = input()

                    print(inp)

            except Exception as e:
                logger.debug(e)


async def load(kernel: Kernel):
    kernel.event_manager.subscribe(StartedEvent, start_shell)


async def unload(kernel: Kernel):
    kernel.event_manager.unsubscribe(StartedEvent, start_shell)
