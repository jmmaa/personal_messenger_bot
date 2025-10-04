from dataclasses import dataclass
from functools import wraps

import time
import asyncio
import logging
import typing as t

from fbchat_muqit import Client, ThreadType, Message
import dew
import linkd

from modules.cmd.api import CommandTree
from yui.kernel import Kernel
from modules.lifecycle import StartedEvent, StoppingEvent
from yui.types import MaybeAwaitable


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


@dataclass
class FBMessage:
    text: str
    mid: str
    author_id: str
    message_object: Message
    thread_id: str
    thread_type: ThreadType


@dataclass
class FBMessageReceivedEvent:
    message: FBMessage
    kernel: Kernel


async def execute_legacy_fb_command(event: FBMessageReceivedEvent):
    di = t.cast(linkd.DependencyInjectionManager, event.kernel.cache["__LEGACY_CMD_DI_API__"])
    tree = t.cast(CommandTree, event.kernel.cache["__LEGACY_CMD_API__"])
    fb_client = t.cast(Client, event.kernel.cache["__FACEBOOK_CLIENT__"])

    prefix = ">"
    if event.message.text.startswith(prefix):
        message = event.message.text[1:]
        command_sequence = dew.get_keyword_seq(dew.parse(message))

        func = t.cast(
            t.Callable[..., MaybeAwaitable[t.Any | None]], tree.get_tree([prefix, *command_sequence]).data.func
        )

        di_injected_func = di.contextual(linkd.Contexts.ROOT)(linkd.inject(func))

        result = await di_injected_func()

        await fb_client.sendMessage(
            str(result), str(event.message.thread_id), event.message.thread_type, reply_to_id=event.message.mid
        )

    else:
        logger.debug(f"cmd is not recognized as it is not starting with prefix '{prefix}'")


async def start_client(event: StartedEvent):
    config = event.kernel.cache.get("__CONFIG__")

    is_throttled = throttle(2)(lambda: None)

    if config:

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
                if not is_throttled():
                    fb_message = FBMessage(
                        text=message,
                        mid=mid,
                        author_id=author_id,
                        message_object=message_object,
                        thread_id=str(thread_id),
                        thread_type=thread_type,
                    )
                    await event.kernel.event_manager.emit(FBMessageReceivedEvent(fb_message, event.kernel))
                    # await self.sendMessage(result, str(thread_id), thread_type, reply_to_id=mid)

        cookies_path = config.bot.fb_client.cookies_path

        client = await FBClient.startSession(cookies_path)

        event.kernel.cache["__FACEBOOK_CLIENT__"] = client

        while True:
            try:
                await client.listen()

            except asyncio.CancelledError as e:
                logger.debug(e)
                logger.debug("listening cancelled on facebook client")
                break

            except Exception as e:
                logger.debug(e)
                logger.debug("reconnecting...")

                time.sleep(3)


async def stop_client(event: StoppingEvent):
    client = event.kernel.cache["__FACEBOOK_CLIENT__"]

    await client.stopListening()


async def load(kernel: Kernel):
    kernel.event_manager.subscribe(StartedEvent, start_client)
    kernel.event_manager.subscribe(StoppingEvent, stop_client)

    # for capturing events that needs commands
    kernel.event_manager.add_event(FBMessageReceivedEvent)
    kernel.event_manager.subscribe(FBMessageReceivedEvent, execute_legacy_fb_command)


async def unload(kernel: Kernel):
    kernel.event_manager.unsubscribe(StartedEvent, start_client)

    # for removing events that needs commands
    kernel.event_manager.unsubscribe(FBMessageReceivedEvent, execute_legacy_fb_command)
    kernel.event_manager.remove_event(FBMessageReceivedEvent)
