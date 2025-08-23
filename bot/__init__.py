import logging
import time
import typing

from fbchat_muqit import Client, Message, ThreadType


from bot.utils import load_toml
from bot.commands import CommandClient, CommandInput
from bot.plugins import food_buff, info


def leveling_guide_command(kwargs: CommandInput):
    pass


def help_command(_):
    pass


async def main():
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    logging.getLogger().setLevel(logging.DEBUG)

    # ensure that config is loaded
    config_path = "./config.toml"

    try:
        config = load_toml(config_path)

        logging.debug(f"loaded config from '{config_path}'")
        logging.debug(config)

    except Exception as e:
        logging.error(f"cannot load config from '{config_path}': {e}")
        raise e

    def get_command_list_as_msg(_):
        food_buff_data = load_toml("./food_buff_data.toml")

        return food_buff_data["food_buffs"]["help"]["text"]

    command_client = CommandClient(registry={})

    command_client.register(food_buff.addr)
    command_client.register(info.info)

    logging.info("registered commands")
    logging.debug(f"command registry: {command_client.registry}")

    # while True:
    #     inp = input()

    #     if inp.startswith("/"):
    #         print("\n", command_client.execute(inp.replace("/", "")))

    # TODO LATER

    # COMMANDS
    # ORGANIZE THE CODE
    # MAYBE ADD CONTEXT INSTEAD OF COMMAND KWARGS ONLY

    class _Client(Client):
        # async def onPeopleAdded(
        #     self,
        #     mid=None,
        #     added_ids=None,
        #     author_id=None,
        #     thread_id=None,
        #     ts=None,
        #     msg=None,
        # ):
        #     await self.sendMessage(
        #         """Welcome to Eternally Guild!
        #         Please read the guidelines on the pictures below
        #         """,
        #         str(thread_id),
        #         thread_type=ThreadType.GROUP,
        #         mentions=added_ids,
        #     )
        #     await self.sendLocalFiles(
        #         [
        #             "./.eternally_guild_files/3.jpg",
        #             "./.eternally_guild_files/2.jpg",
        #             "./.eternally_guild_files/1.jpg",
        #         ],
        #         thread_id=str(thread_id),
        #         thread_type=ThreadType.GROUP,
        #     )

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
