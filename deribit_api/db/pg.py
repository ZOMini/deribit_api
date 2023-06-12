import runpy
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings

engine = create_async_engine(settings.data_base, echo=settings.debug)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) #  type: ignore[call-overload]


async def get_pg() -> AsyncSession: #  type: ignore[misc]
    async with async_session() as session:
        yield session


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
