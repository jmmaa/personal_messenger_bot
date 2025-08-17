import logging
import time
import typing

from fbchat_muqit import Client, Message, ThreadType


from bot.utils import load_config
from bot.commands import CommandClient, CommandInput, CommandRegistry
from bot.commands.food_buff import food_buff_command


def help_command(kwargs: CommandInput):
    help = """/help
    /addr stat:<stat here>

    /guide gq
    /guide graid
    /guide lvl
    /guide fbuff

    LEGACY COMMANDS (to be removed soon): 

    >addr <stat here>
    """

    return help


async def main():
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    logging.getLogger().setLevel(logging.DEBUG)

    # ensure that config is loaded
    config_path = "./config.toml"

    try:
        config = load_config(config_path)

        logging.debug(f"loaded config from '{config_path}'")
        logging.debug(config)

    except Exception as e:
        logging.error(f"cannot load config from '{config_path}': {e}")
        raise e

    # build commands

    # add functionality to print the commands registered
    registry: CommandRegistry = {
        "help": {
            "func": help_command,
            "sub_commands": {},
        },
        "addr": {
            "func": food_buff_command,
            "sub_commands": {},
        },
        "guide": {
            "func": lambda x: str(x) + " TORAAAAM",
            "sub_commands": {
                "gq": {
                    "func": lambda x: str(x),
                    "sub_commands": {},
                },
                "graid": {
                    "func": lambda x: str(x),
                    "sub_commands": {},
                },
                "lvl": {
                    "func": lambda x: str(x),
                    "sub_commands": {},
                },
                "fbuff": {
                    "func": lambda x: str(x),
                    "sub_commands": {},
                },
            },
        },
    }

    command_client = CommandClient(registry=registry)

    logging.debug("registered commands")
    logging.debug(f"command registry: {command_client.registry}")

    # while True:
    #     inp = input("type cmd: ")

    #     if inp.startswith("/"):
    #         print(command_client.execute(inp.replace("/", "")))

    class _Client(Client):
        async def onPeopleAdded(
            self,
            mid=None,
            added_ids=None,
            author_id=None,
            thread_id=None,
            ts=None,
            msg=None,
        ):
            await self.sendMessage(
                """Welcome to Eternally Guild!
                Please read the guidelines on the pictures below
                """,
                str(thread_id),
                thread_type=ThreadType.GROUP,
                mentions=added_ids,
            )
            await self.sendLocalFiles(
                [
                    "./.eternally_guild_files/3.jpg",
                    "./.eternally_guild_files/2.jpg",
                    "./.eternally_guild_files/1.jpg",
                ],
                thread_id=str(thread_id),
                thread_type=ThreadType.GROUP,
            )

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
            print(message)
            if message.startswith("/"):
                result = command_client.execute(message.replace("/", ""))

                await self.sendMessage(
                    result,
                    str(thread_id),
                    thread_type,
                    reply_to_id=mid,
                )

    while True:
        try:
            cookies_path = config["bot"]["cookies_path"]

        except Exception as e:
            raise e

        bot = await _Client.startSession(cookies_path)
        # if await bot.isLoggedIn():
        # fetch_client_info = await bot.fetchUserInfo(bot.uid)
        # client_info = fetch_client_info[bot.uid]

        try:
            await bot.listen()
        except Exception as _:
            print("retrying connection...")
            time.sleep(1)
