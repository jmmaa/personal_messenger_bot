from __future__ import annotations

import typing as t

import pydantic

from bot import Bot, Plugin
from bot.utils import load_toml


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


class ConfigPlugin(Plugin[Bot]):
    def on_add(self, client):
        config = load_toml("config.toml")
        client.d["config"] = Config(**config)

    def on_remove(self, client):
        del client.d["config"]


__plugin__ = ConfigPlugin()
