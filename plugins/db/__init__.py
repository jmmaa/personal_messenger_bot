import asyncpg
import typing as t
import logging

import pydantic

from bot import Bot
from bot import Plugin
from plugins.env import Env


Pool: t.TypeAlias = asyncpg.Pool
Connection: t.TypeAlias = asyncpg.Connection


class PostgresDatabaseSecrets(pydantic.BaseModel):
    POSTGRES_NAME: str | None
    POSTGRES_USER: str | None
    POSTGRES_HOST: str | None
    POSTGRES_PORT: str | None
    POSTGRES_PASSWORD: str | None


def create_postgres_dsn(
    name: str,
    user: str,
    host: str,
    port: int,
    password: str,
):
    return f"postgres://{user}:{password}@{host}:{port}/{name}"


def get_postgres_dsn_from_env(env: t.Mapping[str, str | None]):
    secrets = PostgresDatabaseSecrets(**env)

    dsn = create_postgres_dsn(
        name=secrets.POSTGRES_NAME or "postgres",
        user=secrets.POSTGRES_USER or "postgres",
        password=secrets.POSTGRES_PASSWORD or "postgres",
        port=int(secrets.POSTGRES_PORT or 5432),
        host=secrets.POSTGRES_HOST or "localhost",
    )

    return dsn


class DatabasePlugin(Plugin[Bot]):
    async def load(self, client: Bot):
        env = client.d.get("env")

        if env:
            dsn = get_postgres_dsn_from_env(env)

            pool = await asyncpg.create_pool(dsn)

            client.d["pool"] = pool

        else:
            raise Exception("env not found, is 'env' plugin installed?")

    async def unload(self, client: Bot):
        pool: Pool = client.d["pool"]

        if pool:
            await pool.close()

        else:
            logging.error("pool already closed")


__plugin__ = DatabasePlugin()
