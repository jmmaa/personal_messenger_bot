from __future__ import annotations

import sys
import asyncio
from dataclasses import dataclass
import logging
import time

import asyncpg

from fbchat_muqit import Client, Message, ThreadType


from bot.commands.di import DependencyInjector


from bot.config import Config
from bot.utils import load_toml, load_env
from bot.commands import CommandClient
from bot.commands.plugins import food_buff
from bot.database import Pool, get_postgres_dsn_from_env


import abc

import typing as t


class Plugin(abc.ABC):
    async def load(self, bot: Bot):
        pass

    async def unload(self, bot: Bot):
        pass

    def on_add(self, bot: Bot):
        pass

    def on_remove(self, bot: Bot):
        pass


class ConfigPlugin(Plugin):
    def on_add(self, bot: Bot):
        config = load_toml("config.toml")

        bot.d["config"] = Config(**config)

    def on_remove(self, bot: Bot):
        del bot.d["config"]


class DatabasePlugin(Plugin):
    async def load(self, bot: Bot):
        env = load_env()

        dsn = get_postgres_dsn_from_env(env)

        bot.d["database"] = await asyncpg.create_pool(dsn)

    async def unload(self, bot: Bot):
        pool: asyncpg.Pool = bot.d["database"]

        await pool.close()


class CommandPlugin(Plugin):
    async def load(self, bot: Bot):
        pool: Pool = bot.d["database"]

        dependency_manager = DependencyInjector({})

        dependency_manager.set(Pool, pool)

        client = CommandClient(di=dependency_manager, registry={})

        client.register(food_buff.addr)

        bot.d["command"] = client


class InjectDatabaseToCommandClientPlugin(Plugin):
    async def load(self, bot: Bot):
        client: CommandClient = bot.d["command"]
        pool: Pool = bot.d["database"]

        client.di.set(Pool, pool)

    async def unload(self, bot: Bot):
        client: CommandClient = bot.d["command"]

        await client.di.unset(Pool)


class ToramPlugin(Plugin):
    async def load(self, bot: Bot):
        pool: Pool = bot.d["database"]

        # TODO schema of the database here
        # TODO toram commands here


class Bot:
    def __init__(self, d: t.Dict[t.Any, t.Any] = dict(), plugins: list[Plugin] = list()) -> None:
        self.d = d
        self.plugins = plugins

        # DEFAULT PLUGIN
        self.add_plugin(ConfigPlugin())
        self.add_plugin(DatabasePlugin())
        self.add_plugin(CommandPlugin())
        self.add_plugin(InjectDatabaseToCommandClientPlugin())

    async def execute(self, inp: str):
        return inp

    def add_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)
        plugin.on_add(self)

    def add_plugins(self, plugins: list[Plugin]):
        for plugin in plugins:
            self.add_plugin(plugin)

    # def remove_plugin(self, name: str)
    # def remove_plugins

    async def load_plugins(self):
        for plugin in self.plugins:
            try:
                logging.info(f"loading '{plugin}'")
                await plugin.load(self)
                logging.info(f"loaded '{plugin}'")
            except asyncio.CancelledError:
                logging.info(f"loading '{plugin}'")
                await plugin.load(self)
                logging.info(f"loaded '{plugin}'")
            except Exception as e:
                logging.error(f"Error unloading '{plugin}': {e}")

    async def unload_plugins(self):
        for plugin in reversed(self.plugins):
            try:
                logging.info(f"unloading '{plugin}'")
                await plugin.unload(self)
                logging.info(f"unloaded '{plugin}'")
            except asyncio.CancelledError:
                logging.info(f"unloading '{plugin}'")
                await plugin.unload(self)
                logging.info(f"unloaded '{plugin}'")
            except Exception as e:
                logging.error(f"Error unloading '{plugin}': {e}")


async def main():
    bot = Bot()

    config: Config = bot.d["config"]

    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
        handlers=[
            logging.FileHandler(config.bot.logging.file),
            logging.StreamHandler(),
        ],
    )

    logging.getLogger().setLevel(logging._nameToLevel[config.bot.logging.level])

    # CUSTOM PLUGINS

    bot.add_plugin(ToramPlugin())

    #

    await bot.load_plugins()

    command_client: CommandClient = bot.d["command"]

    pool: asyncpg.Pool = bot.d["database"]

    if config.bot.shell_mode:
        if config.bot.shell_mode:
            try:
                while True:
                    inp = input()

                    if inp.startswith(config.bot.prefix):
                        result = await command_client.execute(inp[1:])

                        print(result)

            except Exception as e:
                await bot.unload_plugins()

    else:

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
                if message.startswith(config.bot.prefix):
                    result = await command_client.execute(message[1:])

                    await self.sendMessage(
                        await result,
                        str(thread_id),
                        thread_type,
                        reply_to_id=mid,
                    )

            async def run(self):
                while True:
                    try:
                        cookies_path = config.bot.fb_client.cookies_path

                    except Exception as e:
                        raise e

                    session = await self.startSession(cookies_path)
                    if await session.isLoggedIn():
                        logging.info("logged in!")

                    try:
                        await session.listen()
                    except Exception as e:
                        logging.error(e)

                        print("retrying connection...")
                        time.sleep(1)


# TODO
# ADD LOGGING
# ADD MORE PLUGINS
# DECIDE THE DATABASE STRUCTURE

# async def main():
#     bot = Bot()

#     bot.run()


# async def main():
#     # ensure that config is loaded
#     config_path = "./config.toml"

#     try:
#         config = Config(**load_toml(config_path))

#         # LOGGING SETUP
#         logging.basicConfig(
#             format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
#             handlers=[
#                 logging.FileHandler(config.bot.logging.file),
#                 logging.StreamHandler(),
#             ],
#         )

#         logging.getLogger().setLevel(logging._nameToLevel[config.bot.logging.level])

#         logging.debug(f"loaded config from '{config_path}'")

#     except Exception as e:
#         logging.error(f"cannot load config from '{config_path}': {e}")
#         raise e

#     # COMMAND SETUP
#     di = DependencyInjector({})

#     command_client = CommandClient(di, registry={})
#     command_client.register(food_buff.addr)
#     command_client.register(info.info)

#     logging.debug(f"command registry: {command_client.registry}")

#     # DATABASE SETUP
#     env = load_env()
#     dsn = get_postgres_dsn_from_env(env)
#     pool = await asyncpg.create_pool(dsn)

#     async def teardown(pool: Pool):
#         await pool.close()

#     di.set(Pool, pool, teardown=teardown)

#     # SHELL MODE IF SET TO TRUE
#     if config.bot.shell_mode:
#         while True:
#             try:
#                 inp = input()

#                 if inp.startswith(config.bot.prefix):
#                     print(
#                         "\n",
#                         await command_client.execute(inp[1:]),
#                     )

#             except KeyboardInterrupt:
#                 await di.unset(Pool)

#             except Exception as e:
#                 print(e)
#                 continue

#     class _Client(Client):
#         async def onMessage(
#             self,
#             mid: str,
#             author_id: str,
#             message: str,
#             message_object: Message,
#             thread_id=None,
#             thread_type=ThreadType.USER,
#             ts=None,
#             metadata=None,
#             msg=None,
#         ):
#             if message.startswith(config.bot.prefix):
#                 result = await command_client.execute(message[1:])

#                 await self.sendMessage(
#                     await result,
#                     str(thread_id),
#                     thread_type,
#                     reply_to_id=mid,
#                 )

#     while True:
#         try:
#             cookies_path = config.bot.fb_client.cookies_path

#         except Exception as e:
#             raise e

#         bot = await _Client.startSession(cookies_path)
#         # if await bot.isLoggedIn():
#         # fetch_client_info = await bot.fetchUserInfo(bot.uid)
#         # client_info = fetch_client_info[bot.uid]

#         try:
#             await bot.listen()
#         except Exception as e:
#             logging.error(e)

#             print("retrying connection...")
#             time.sleep(1)
