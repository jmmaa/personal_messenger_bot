import os
import logging

from bot import Bot
from bot import Plugin
from plugins.db import Pool


logging = logging.getLogger(__name__)


class ToramPlugin(Plugin[Bot]):
    async def load(self, client):
        pool: Pool = client.d["pool"]

        async with pool.acquire() as conn:
            schema_path = os.path.dirname(__file__) + "\\schema.sql"
            logging.debug(f"initiating toram database schema from {schema_path}")

            with open(schema_path, "r") as f:
                schema = f.read()

                await conn.execute(schema)

            logging.debug(f"initiated toram database schema from {schema_path}")

    # async def unload(self, client):


__plugin__ = ToramPlugin()
