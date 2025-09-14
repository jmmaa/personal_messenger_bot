from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import typing as t
import asyncio

from bot import Core, Plugin
from bot.utils import MaybeAwaitable, maybe_await


T = t.TypeVar("T")


class AsyncObserver(ABC, t.Generic[T]):
    @abstractmethod
    async def update(self, subject: AsyncSubject[T]):
        pass


class AsyncSubject(ABC, t.Generic[T]):
    def __init__(self, value: T | None = None) -> None:
        self._value = value
        self._observers = []

    @property
    def value(self) -> T:
        raise NotImplementedError

    @value.setter
    def value(self, value: T):
        self._value = value

    @value.getter
    def value(self) -> T | None:
        return self._value

    @property
    def observers(self) -> list[AsyncObserver[T]]:
        raise NotImplementedError

    @observers.setter
    def observers(self, observers: list[AsyncObserver[T]]):
        self._observers = observers

    @observers.getter
    def observers(self) -> list[AsyncObserver[T]]:
        return self._observers

    @abstractmethod
    async def notify(self):
        pass

    @abstractmethod
    def subscribe(self, observer: AsyncObserver[T]):
        pass

    @abstractmethod
    def unsubscribe(self, observer: AsyncObserver[T]):
        pass


class AsyncSignal(AsyncSubject[T]):
    async def notify(self):
        for observer in self.observers:
            await observer.update(self)

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers.pop(self.observers.index(observer))


class EventPlugin(Plugin[Core]):
    def on_add(self, core):
        core.d["event_manager"] = AsyncSignal()

    def on_remove(self, core):
        del core.d["create_async_signal"]


__plugin__ = EventPlugin()
