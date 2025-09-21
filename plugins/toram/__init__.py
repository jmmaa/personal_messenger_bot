import os
import logging
import typing as t

from bot import Plugin, Core

from plugins.db import Pool


logging = logging.getLogger(__name__)


class ToramPlugin(Plugin[Core]):
    async def on_load(self, core):
        pool = t.cast(Pool | None, core.d.get("pool"))

        if pool:
            async with pool.acquire() as conn:
                schema_path = os.path.dirname(__file__) + "\\schema.sql"

                logging.debug(f"initiating toram database schema from {schema_path}")

                with open(schema_path, "r") as f:
                    schema = f.read()

                    await conn.execute(schema)

                logging.debug(f"initiated toram database schema from {schema_path}")
        else:
            raise Exception("db pool connection not found!, have you installed db plugin?")

    # async def unload(self, core):


__plugin__ = ToramPlugin()
