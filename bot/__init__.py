from __future__ import annotations


import abc
import asyncio
import logging
import typing as t
import importlib


from bot.types import Plugin
from bot.utils import maybe_await


T = t.TypeVar("T")


def load_plugin_spec(package: str) -> Plugin[Core]:
    module = importlib.import_module(package)

    for symbols in module.__dict__.items():
        if isinstance(symbols[1], Plugin):
            return symbols[1]

    else:
        raise Exception(f"could not find 'Plugin' instance in '{package}'")


def load_plugin_specs(plugins: list[str]) -> list[Plugin[Core]]:
    plugin_specs = []

    for plugin in plugins:
        plugin_specs.append(load_plugin_spec(plugin))

    return plugin_specs


_KT = t.TypeVar("_KT")
_VT = t.TypeVar("_VT")


class DataStore(dict):
    def __getitem__(self, key: _KT, /) -> _VT:
        logging.debug(f"get item in key'{key}' from datastore")
        return super().__getitem__(key)

    def __setitem__(self, key: _KT, value: _VT, /) -> None:
        logging.debug(f"set item '{value}' to '{key}' into datastore")
        return super().__setitem__(key, value)

    def __delitem__(self, key: _KT, /) -> None:
        logging.debug(f"deleted '{key}' in datastore")
        return super().__delitem__(key)

    def type_safe_get(self, _type: _VT, key: _KT):
        return t.cast(_VT | None, self.get(key))


# class Bot:
#     def __init__(
#         self,
#         d: DataStore = DataStore(),
#         plugins: list[Plugin[Bot]] = list(),
#         pipeline: list[t.Callable[..., t.Any]] = list(),
#     ) -> None:
#         self.d = d
#         self.plugins = plugins
#         self.pipeline = pipeline

#     def add_plugin(self, plugin: Plugin[Bot]):
#         logging.info(f"adding plugin '{plugin}'")
#         self.plugins.append(plugin)
#         plugin.on_add(self)
#         logging.info(f"added plugin '{plugin}'")

#     def add_plugins(self, plugins: list[Plugin[Bot]]):
#         for plugin in plugins:
#             self.add_plugin(plugin)

#     async def execute(self, input: str) -> t.Any:
#         result = input
#         for pipe in self.pipeline:
#             result = await maybe_await(pipe(result))

#         return result

#     async def load_plugins(self):
#         for plugin in self.plugins:
#             try:
#                 logging.info(f"loading '{plugin}'")
#                 await plugin.load(self)
#                 logging.info(f"loaded '{plugin}'")
#             except asyncio.CancelledError:
#                 logging.info(f"loading '{plugin}'")
#                 await plugin.load(self)
#                 logging.info(f"loaded '{plugin}'")
#             except Exception as e:
#                 logging.error(f"Error loading '{plugin}': {e}")

#     async def unload_plugins(self):
#         for plugin in reversed(self.plugins):
#             try:
#                 logging.info(f"unloading '{plugin}'")
#                 await plugin.unload(self)
#                 logging.info(f"unloaded '{plugin}'")
#             except asyncio.CancelledError:
#                 logging.info(f"unloading '{plugin}'")
#                 await plugin.unload(self)
#                 logging.info(f"unloaded '{plugin}'")
#             except Exception as e:
#                 logging.error(f"Error unloading '{plugin}': {e}")

#     async def run(self):
#         for plugin in self.plugins:
#             try:
#                 logging.info(f"running '{plugin}'")
#                 await plugin.run(self)
#                 logging.info(f"ran '{plugin}'")
#             except asyncio.CancelledError:
#                 logging.info(f"ran '{plugin}'")
#                 await plugin.run(self)
#                 logging.info(f"ran '{plugin}'")
#             except Exception as e:
#                 logging.error(f"Error running '{plugin}': {e}")

#     async def stop(self):
#         for plugin in reversed(self.plugins):
#             try:
#                 logging.info(f"stopping '{plugin}'")
#                 await plugin.stop(self)
#                 logging.info(f"stopped '{plugin}'")
#             except asyncio.CancelledError:
#                 logging.info(f"stopping '{plugin}'")
#                 await plugin.stop(self)
#                 logging.info(f"stopped '{plugin}'")
#             except Exception as e:
#                 logging.error(f"Error stopping '{plugin}': {e}")


class Core:
    def __init__(self, d: DataStore = DataStore(), plugins: list[Plugin[Core]] = []) -> None:
        self.d = d
        self.plugins = plugins

    def add_plugin(self, plugin: Plugin[Core]):
        self.plugins.append(plugin)
        plugin.on_add(self)

    def add_plugins(self, plugins: list[Plugin[Core]]):
        for plugin in plugins:
            self.add_plugin(plugin)

    async def load_plugin(self, plugin: Plugin[Core]):
        try:
            logging.info(f"loading '{plugin}'")
            await plugin.on_load(self)
            logging.info(f"loaded '{plugin}'")
        except asyncio.CancelledError:
            logging.info(f"loading '{plugin}'")
            await plugin.on_load(self)
            logging.info(f"loaded '{plugin}'")
        except Exception as e:
            logging.error(f"Error loading '{plugin}': {e}")

    async def load_plugins(self, plugins: list[Plugin[Core]]):
        for plugin in plugins:
            await self.load_plugin(plugin)

    async def load(self):
        await self.load_plugins(self.plugins)

    async def unload_plugin(self, plugin: Plugin[Core]):
        try:
            logging.info(f"loading '{plugin}'")
            await plugin.on_unload(self)
            logging.info(f"loaded '{plugin}'")
        except asyncio.CancelledError:
            logging.info(f"loading '{plugin}'")
            await plugin.on_unload(self)
            logging.info(f"loaded '{plugin}'")
        except Exception as e:
            logging.error(f"Error loading '{plugin}': {e}")

    async def unload_plugins(self, plugins: list[Plugin[Core]]):
        for plugin in reversed(plugins):
            await self.unload_plugin(plugin)

    async def unload(self):
        await self.unload_plugins(self.plugins)

    async def run_plugin(self, plugin: Plugin[Core]):
        try:
            logging.info(f"running '{plugin}'")
            await plugin.on_run(self)
            logging.info(f"ran '{plugin}'")
        except asyncio.CancelledError:
            logging.info(f"running '{plugin}'")
            await plugin.on_run(self)
            logging.info(f"ran '{plugin}'")
        except Exception as e:
            logging.error(f"Error running '{plugin}': {e}")

    async def run_plugins(self, plugins: list[Plugin[Core]]):
        for plugin in reversed(plugins):
            await self.run_plugin(plugin)

    async def run(self):
        await self.run_plugins(self.plugins)

    async def stop_plugin(self, plugin: Plugin[Core]):
        try:
            logging.info(f"stopping '{plugin}'")
            await plugin.on_stop(self)
            logging.info(f"stopped '{plugin}'")
        except asyncio.CancelledError:
            logging.info(f"stopping '{plugin}'")
            await plugin.on_stop(self)
            logging.info(f"stopped '{plugin}'")
        except Exception as e:
            logging.error(f"Error stopping '{plugin}': {e}")

    async def stop_plugins(self, plugins: list[Plugin[Core]]):
        for plugin in reversed(plugins):
            await self.stop_plugin(plugin)

    async def stop(self):
        await self.stop_plugins(self.plugins)

    async def start(self):
        try:
            await self.load()
            await self.run()

        except Exception as e:
            raise e

        finally:
            await self.stop()
            await self.unload()
