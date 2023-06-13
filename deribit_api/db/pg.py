import runpy
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_async_engine(settings.data_base, echo=settings.debug)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)  # type: ignore[call-overload]


# Dependency
async def get_pg() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@asynccontextmanager
async def get_pg_contextmanager():
    engine = create_async_engine(settings.data_base, echo=settings.debug)
    session = AsyncSession(engine, expire_on_commit=False)
    try:
        yield session
    finally:
        await session.close()


def migrate():
    engine = create_engine(settings.data_base_sync)
    if not engine.dialect.has_table(engine.connect(), 'currencies'):
        try:
            # На всякий пытается создать миграции, но они уже есть, должны быть.
            sys.argv = ['', 'revision', '-m', '"init"', '--autogenerate']
            runpy.run_module('alembic', run_name='__main__')
        except Exception:
            pass
        finally:
            # Мигрируем.
            sys.argv = ['', 'upgrade', 'head']
            runpy.run_module('alembic', run_name='__main__')
