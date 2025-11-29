from __future__ import annotations

import logging
import os
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from models.base import Base

logger = logging.getLogger(__name__)

engine: Optional[AsyncEngine] = None
SessionLocal: Optional[async_sessionmaker[AsyncSession]] = None


async def init_db() -> Optional[async_sessionmaker[AsyncSession]]:
    global engine, SessionLocal
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/pair_programming",
    ).strip()
    if not database_url:
        logger.warning("DATABASE_URL not set; using in-memory room store")
        return None
    try:
        engine = create_async_engine(database_url, future=True, echo=False)
        SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Connected to Postgres and initialized schema")
        return SessionLocal
    except Exception as exc:
        logger.warning("Postgres unavailable (%s); falling back to in-memory store", exc)
        if engine:
            await engine.dispose()
        engine = None
        SessionLocal = None
        return None


async def shutdown_db() -> None:
    global engine
    if engine is not None:
        await engine.dispose()
        engine = None
