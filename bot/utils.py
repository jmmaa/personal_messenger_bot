import tomllib
import typing as t
import os
import inspect

import dotenv


def load_toml(path: str) -> dict[str, t.Any]:
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)

            return data

    except Exception as e:
        raise e


Env: t.TypeAlias = t.Mapping[str, str | None]


def load_env() -> Env:
    dotenv.load_dotenv()  # to load vars from .env file

    return t.cast(Env, os.environ)


T = t.TypeVar("T")

MaybeAwaitable: t.TypeAlias = t.Union[T, t.Awaitable[T]]


async def maybe_await(obj: MaybeAwaitable[T]) -> T:
    if inspect.iscoroutine(obj):
        return await obj

    return t.cast(T, obj)
