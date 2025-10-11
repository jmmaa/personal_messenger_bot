from __future__ import annotations
import asyncio
from asyncio.tasks import Task
import sys
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


KT = t.TypeVar("KT")
VT = t.TypeVar("VT")


class Store(t.Generic[KT, VT], dict[KT, VT]):
    def __getitem__(self, key: KT, /):
        logger.debug(f"get item in key'{key}' from store")
        return super().__getitem__(key)

    def __setitem__(self, key, value: VT, /) -> None:
        logger.debug(f"set item '{value}' to '{key}' into store")
        return super().__setitem__(key, value)

    def __delitem__(self, key: KT, /) -> None:
        logger.debug(f"deleted '{key}' in store")
        return super().__delitem__(key)


class Hooks:
    mapping: Store[str, list[t.Callable[..., t.Any | None]]]

    def __init__(self, mapping=Store()) -> None:
        self.mapping = mapping

    def add_hook(self, hook: str):
        # TODO: add a check to ensure that the hook is not added again
        self.mapping[hook] = []

        logger.debug(f"added hook '{hook}'")

    def remove_hook(self, hook: str):
        del self.mapping[hook]

        logger.debug(f"removed hook '{hook}'")

    def subscribe(self, hook: str, callback: t.Callable[[T], MaybeAwaitable[t.Any | None]]):
        callbacks = self.mapping.get(hook)

        if callbacks is not None:
            self.mapping[hook].append(callback)

            logger.debug(f"subscribed to '{hook}' with callback '{callback.__name__}'")

        else:
            raise Exception(f"attempting to subscribe to an unknown hook '{hook}'")

    def unsubscribe(self, hook: str, callback: t.Callable[[T], MaybeAwaitable[t.Any | None]]):
        callbacks = self.mapping.get(hook)

        if callbacks is not None:
            self.mapping[hook].remove(callback)

            logger.debug(f"unsubscribed to '{hook}' with callback '{callback.__name__}'")

        else:
            raise Exception(f"attempting to unsubscribe to an unknown hook '{hook}'")

    async def emit(self, hook: str, payload: t.Any):
        callbacks = self.mapping.get(hook)

        if callbacks is not None:
            logger.debug(f"emitting hook '{hook}'")
            for callback in self.mapping[hook]:
                logger.debug(f"calling '{callback.__name__}'")
                await maybe_await(callback(payload))

        else:
            raise Exception(f"attempting to emit an unknown hook '{hook}'")


class Kernel:
    def __init__(
        self,
        modules: list[ModuleType] = [],
        hooks: Hooks = Hooks(),
        store: dict[str, t.Any] = Store(),
    ) -> None:
        self.modules = modules
        self.hooks: Hooks = hooks
        self.store = store

    def get(self, key: str):
        return self.store[key]

    def set(self, key: str, value: t.Any):
        self.store[key] = value

    def add_hook(self, hook: str):
        self.hooks.add_hook(hook)

    def remove_hook(self, hook: str):
        self.hooks.remove_hook(hook)

    def sub(self, hook: str, callback: t.Callable[[T], MaybeAwaitable[t.Any | None]]):
        self.hooks.subscribe(hook, callback)

    def unsub(self, hook: str, callback: t.Callable[[T], MaybeAwaitable[t.Any | None]]):
        self.hooks.unsubscribe(hook, callback)

    async def emit(self, hook: str, payload: t.Any):
        await self.hooks.emit(hook, payload)

    def add_module_from_package(self, package: str):
        """adds a module from a package name to the module list but not loaded yet to kernel"""
        self.modules.append(importlib.import_module(package))

    def add_module(self, module: ModuleType):
        """adds a module to the module list but not loaded yet to kernel"""
        self.modules.append(module)

    def add_modules_from_packages(self, packages: list[str]):
        for package in packages:
            self.add_module_from_package(package)

    def add_modules(self, modules: list[ModuleType]):
        for module in modules:
            self.add_module(module)

    def remove_module(self, module: ModuleType):
        self.modules.remove(module)

    def remove_module_from_package(self, package: str):
        for module in self.modules:
            if module.__name__ == package:
                self.modules.remove(module)

    async def load_module(self, package: str):
        for module in self.modules:
            if module.__name__ == package:
                await maybe_await(module.load(self))

    async def unload_module(self, package: str):
        for module in self.modules:
            if module.__name__ == package:
                await maybe_await(module.unload(self))

    async def load_modules(self):
        for module in self.modules:
            await maybe_await(module.load(self))

    async def unload_modules(self):
        for module in reversed(self.modules):
            await maybe_await(module.unload(self))

    async def boot(self):
        await self.load_modules()

    async def reboot(self):
        await self.unload_modules()
        await self.load_modules()

    async def shutdown(self):
        await self.unload_modules()
