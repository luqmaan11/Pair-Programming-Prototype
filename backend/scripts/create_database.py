from __future__ import annotations

import asyncio
import os
from sqlalchemy.engine.url import make_url

import asyncpg
from dotenv import load_dotenv

DEFAULT_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/pair_programming"


def build_connection_args(raw_url: str) -> tuple[dict[str, object], str]:
    url = make_url(raw_url)
    database = url.database or "pair_programming"
    connection_kwargs: dict[str, object] = {
        "user": url.username or "postgres",
        "password": url.password or "postgres",
        "host": url.host or "localhost",
        "port": url.port or 5432,
        "database": os.getenv("PG_TEMPLATE_DB", "postgres"),
    }
    return connection_kwargs, database


async def main() -> None:
    load_dotenv()
    raw_url = os.getenv("DATABASE_URL", DEFAULT_URL)
    conn_kwargs, target_db = build_connection_args(raw_url)
    conn = await asyncpg.connect(**conn_kwargs)
    exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname=$1", target_db)
    if exists:
        print(f"database '{target_db}' already exists")
    else:
        await conn.execute(f"CREATE DATABASE \"{target_db}\"")
        print(f"created database '{target_db}'")
    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
