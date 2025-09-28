import asyncio
import logging


from fbchat_muqit import Client, ThreadType, Message


import time
from functools import wraps

from yui.kernel import Kernel
from modules.lifecycle import StartedEvent, StoppingEvent


logger = logging.getLogger("yui")


def throttle(delay_seconds):
    """
    A decorator that throttles a function, allowing it to be called at most
    once within the specified delay_seconds.
    """

    def decorator(func):
        last_called = 0  # Stores the timestamp of the last successful call

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called
            current_time = time.time()

            if current_time - last_called >= delay_seconds:
                result = func(*args, **kwargs)
                last_called = current_time
                return result
            else:
                # Optionally, you could log a message or return a specific value
                # indicating the call was throttled.
                return True  # Or raise an exception, or return a placeholder

        return wrapper

    return decorator


async def start_client(event: StartedEvent):
    config = event.kernel.cache.get("__CONFIG__")
    command_client = event.kernel.cache.get("__COMMAND_CLIENT__")
    parse_command = event.kernel.cache.get("__COMMAND_PARSER__")

    is_throttled = throttle(2)(lambda: None)

    if config and parse_command and command_client:

        class FBClient(Client):
            async def onMessage(
                self,
                mid: str,
                author_id: str,
                message: str,
                message_object: Message,
                thread_id=None,
                thread_type=ThreadType.USER,
                ts=None,
                metadata=None,
                msg=None,
            ):
                # author_id is message sender ID
                if message.startswith(config.bot.prefix):
                    await asyncio.sleep(1)
                    node = parse_command(message[1:])
                    result = await command_client.execute(node)

                    if not is_throttled():
                        await self.sendMessage(result, str(thread_id), thread_type, reply_to_id=mid)

        cookies_path = config.bot.fb_client.cookies_path

        client = await FBClient.startSession(cookies_path)

        event.kernel.cache["__FACEBOOK_CLIENT__"] = client

        try:
            await client.listen()
        except asyncio.CancelledError as e:
            logger.debug(e)


async def stop_client(event: StoppingEvent):
    client = event.kernel.cache["__FACEBOOK_CLIENT__"]

    await client.stopListening()


async def load(kernel: Kernel):
    kernel.event_manager.subscribe(StartedEvent, start_client)
    kernel.event_manager.subscribe(StoppingEvent, stop_client)


async def unload(kernel: Kernel):
    kernel.event_manager.unsubscribe(StartedEvent, start_client)
