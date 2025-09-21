from bot import Core
from bot.types import Plugin

from plugins.command.api import CommandClient
from plugins.config import Config


from fbchat_muqit import Client, ThreadType, Message


import time
from functools import wraps


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


class FacebookPlugin(Plugin[Core]):
    async def on_run(self, core):
        config: Config = core.d["config"]
        command_client: CommandClient = core.d["command_client"]
        command_parser = core.d["dew"]

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
                    # author_id is message sender ID
                    if message.startswith(config.bot.prefix):
                        node = command_parser.parse(message[1:])
                        result = await command_client.execute(node)

                        if not is_throttled():
                            await self.sendMessage(result, str(thread_id), thread_type, reply_to_id=mid)

            cookies_path = config.bot.fb_client.cookies_path

            client = await FBClient.startSession(cookies_path)

            core.d["fb_client"] = client

            await client.listen()

    async def on_stop(self, core):
        client = core.d["fb_client"]

        await client.stopListening()


__plugin__ = FacebookPlugin()
