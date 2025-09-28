from __future__ import annotations

from dataclasses import dataclass
import typing as t
import inspect
import logging

T = t.TypeVar("T")

MaybeAwaitable: t.TypeAlias = t.Union[T, t.Awaitable[T]]

logging = logging.getLogger("yui")


async def maybe_await(obj: MaybeAwaitable[T]) -> T:
    if inspect.iscoroutine(obj):
        return await obj

    return t.cast(T, obj)


@dataclass
class DependencyInjector:
    _registry: dict[t.Any, t.Callable[[t.Any], MaybeAwaitable[t.Any] | None]]

    def __str__(self) -> str:
        return "DependencyInjector"

    def set(
        self,
        _type: t.Any,
        value: t.Any,
    ):
        logging.debug(f"dependency: {_type}:{value}")

        self._registry[_type] = value

        logging.debug(f"added '{_type}' as a dependency")

    async def unset(self, _type: object):
        existing = self._registry.get(_type)

        if existing:
            self._registry.pop(_type)
            logging.debug(f"removed '{_type}' as a dependency")

        else:
            raise Exception(f"cannot remove '{_type}' dependency, it doesnt exist")

    def inject(self, func: t.Callable[..., MaybeAwaitable[T]]) -> t.Callable[..., MaybeAwaitable[T]]:
        async def _(*args, **kwargs):
            __params = {}

            parameters = inspect.signature(
                func,
                eval_str=True,
            ).parameters

            for annot_item in parameters.items():
                data = self._registry.get(annot_item[1].annotation)

                if data is not None:
                    item = self._registry[annot_item[1].annotation]
                    __params[annot_item[0]] = item

            result = func(*args, **kwargs, **__params)

            return await maybe_await(result)

        _.__name__ = func.__name__

        return _
