from __future__ import annotations
import typing as t

import pydantic


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
