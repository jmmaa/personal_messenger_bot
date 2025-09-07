from __future__ import annotations


import abc
import asyncio
import logging
import typing as t
import importlib

from bot.utils import maybe_await


T = t.TypeVar("T")


class Plugin(abc.ABC, t.Generic[T]):
    async def load(self, client: T):
        pass

    async def unload(self, client: T):
        pass

    def on_add(self, client: T):
        pass

    def on_remove(self, client: T):
        pass


def load_plugin_spec(package: str) -> Plugin[Bot]:
    module = importlib.import_module(package)

    for symbols in module.__dict__.items():
        if isinstance(symbols[1], Plugin):
            return symbols[1]

    else:
        raise Exception(f"could not find 'Plugin' instance in '{package}'")


def load_plugin_specs(plugins: list[str]) -> list[Plugin[Bot]]:
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


class Bot:
    def __init__(
        self,
        d: DataStore = DataStore(),
        plugins: list[Plugin[Bot]] = list(),
        pipeline: list[t.Callable[..., t.Any]] = list(),
    ) -> None:
        self.d = d
        self.plugins = plugins
        self.pipeline = pipeline

    def add_plugin(self, plugin: Plugin):
        logging.info(f"adding plugin '{plugin}'")
        self.plugins.append(plugin)
        plugin.on_add(self)
        logging.info(f"added plugin '{plugin}'")

    def add_plugins(self, plugins: list[Plugin]):
        for plugin in plugins:
            self.add_plugin(plugin)

    # def remove_plugin(self, name: str)
    # def remove_plugins

    async def execute(self, input: str) -> t.Any:
        result = input
        for pipe in self.pipeline:
            result = await maybe_await(pipe(result))

        return result

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
                logging.error(f"Error loading '{plugin}': {e}")

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
