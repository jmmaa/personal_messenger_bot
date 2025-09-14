import os
import logging


from bot import Plugin, Core

from plugins.db import Pool, Record


logging = logging.getLogger(__name__)


class ToramPlugin(Plugin[Core]):
    async def on_load(self, core):
        pool = core.d.type_safe_get(Pool, "pool")

        if isinstance(pool, Pool):  # for some reason this gets a type error if not using `isinstance`
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
