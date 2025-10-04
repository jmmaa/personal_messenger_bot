from __future__ import annotations
from types import ModuleType


import typing as t
import importlib
import logging


from yui.types import MaybeAwaitable
from yui.utils import maybe_await


T = t.TypeVar("T")


logger = logging.getLogger("yui")


class EventManager:
    mapping: dict[str, list[t.Callable[..., t.Any | None]]]

    def __init__(self, mapping=dict()) -> None:
        self.mapping = mapping

    def convert_object_to_key(self, event: object):
        return event.__module__ + "." + event.__qualname__

    def add_event(self, event: type[T]):
        key = self.convert_object_to_key(event)

        # TODO: add a check to ensure that the event is not added again
        self.mapping[key] = []

        logger.debug(f"added event '{event}' with key '{key}'")

    def remove_event(self, event: type[T]):
        key = self.convert_object_to_key(event)

        del self.mapping[key]

        logger.debug(f"removed event '{event}' with key '{key}'")

    def subscribe(self, event: type[T], callback: t.Callable[[T], MaybeAwaitable[t.Any | None]]):
        key = self.convert_object_to_key(event)

        callbacks = self.mapping.get(key)

        if callbacks is not None:
            self.mapping[key].append(callback)

            logger.debug(f"subscribed to event '{event}' with callback '{callback.__name__}'")

        else:
            raise Exception(f"attempting to subscribe to an unknown event '{event}'")

    def unsubscribe(self, event: type[T], callback: t.Callable[[T], MaybeAwaitable[t.Any | None]]):
        key = self.convert_object_to_key(event)

        callbacks = self.mapping.get(key)

        if callbacks is not None:
            self.mapping[key].remove(callback)

            logger.debug(f"unsubscribed to event '{event}' with callback '{callback.__name__}'")

        else:
            raise Exception(f"attempting to unsubscribe to an unknown event '{event}'")

    async def emit(self, event: object):
        key = self.convert_object_to_key(event.__class__)

        callbacks = self.mapping.get(key)

        if callbacks is not None:
            logger.debug(f"emitting event '{event}'")
            for callback in self.mapping[key]:
                logger.debug(f"calling '{callback.__name__}'")
                await maybe_await(callback(event))

        else:
            raise Exception(f"attempting to emit an unknown event '{event}'")


class Cache(dict):
    def __getitem__(self, key, /):
        logger.debug(f"get item in key'{key}' from cache")
        return super().__getitem__(key)

    def __setitem__(self, key, value, /) -> None:
        logger.debug(f"set item '{value}' to '{key}' into cache")
        return super().__setitem__(key, value)

    def __delitem__(self, key, /) -> None:
        logger.debug(f"deleted '{key}' in cache")
        return super().__delitem__(key)


class ModuleManager:
    def __init__(self, modules: list[ModuleType] = []) -> None:
        self.modules = modules

    def import_module(self, module: str):
        loaded_module = importlib.import_module(module)
        return loaded_module


class Kernel:
    def __init__(self) -> None:
        self.event_manager: EventManager = EventManager()
        self.module_manager: ModuleManager = ModuleManager()
        self.cache: Cache = Cache()

    async def load_module(self, module: str):
        loaded_module = self.module_manager.import_module(module)

        self.module_manager.modules.append(loaded_module)

        # the module must have a defined 'load' and 'unload' function
        await maybe_await(loaded_module.load(self))

    async def load_modules(self, modules: list[str]):
        for module in modules:
            await self.load_module(module)

    async def unload_module(self, module: str):
        for loaded_module in self.module_manager.modules:
            if loaded_module.__name__ == module:
                await maybe_await(loaded_module.unload(self))

    async def unload_modules(self):
        for loaded_module in reversed(self.module_manager.modules):
            await maybe_await(loaded_module.unload(self))
