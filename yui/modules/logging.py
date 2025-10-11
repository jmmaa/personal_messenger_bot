from __future__ import annotations
from yui.kernel import Kernel

import logging
import pydantic
import typing as t

logger = logging.getLogger("yui")


LogLevel: t.TypeAlias = t.Literal["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"]


class LoggingConfig(pydantic.BaseModel):
    file: str = pydantic.Field(default="bot.log")
    level: LogLevel = pydantic.Field(default="NOTSET")


class BotConfig(pydantic.BaseModel):
    logging: LoggingConfig = LoggingConfig()


class _ParseLoggingConfig(pydantic.BaseModel):
    bot: BotConfig = BotConfig()


async def load(kernel: Kernel):
    config = kernel.store.get("__CONFIG__")

    # Apparently this makes logging even more efficient! (src hikari.py repo)
    logging.logThreads = False
    logging.logProcesses = False
    logging.logMultiprocessing = False

    if config is not None:
        config = _ParseLoggingConfig(**config)

        # improve the configuration options for this
        formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(name)s: %(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(config.bot.logging.file)
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        logger.setLevel(logging._nameToLevel[config.bot.logging.level])
        logger.debug(f"successfully configured logger '{logger.name}'")


async def unload(kernel: Kernel):
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])
