from __future__ import annotations

import typing as t

import pydantic


from yui.utils import load_toml
from yui.kernel import Kernel


class Config(pydantic.BaseModel):
    bot: BotConfig


class BotConfig(pydantic.BaseModel):
    prefix: str = "/"
    shell_mode: bool = False
    logging: BotLoggingConfig
    fb_client: BotFBClientConfig


class BotFBClientConfig(pydantic.BaseModel):
    cookies_path: str = "cookies.json"


class BotLoggingConfig(pydantic.BaseModel):
    file: str = "bot.log"
    level: t.Literal["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"] = "NOTSET"


async def load(kernel: Kernel):
    kernel.cache["__CONFIG__"] = Config(**load_toml("./config.toml"))


async def unload(kernel: Kernel):
    del kernel.cache["__CONFIG__"]
