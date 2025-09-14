from abc import ABC
import typing as t

T = t.TypeVar("T")


class Plugin(ABC, t.Generic[T]):
    async def on_load(self, core: T):
        pass

    async def on_unload(self, core: T):
        pass

    async def on_run(self, core: T):
        pass

    async def on_stop(self, core: T):
        pass

    def on_add(self, core: T):
        pass

    def on_remove(self, core: T):
        pass
