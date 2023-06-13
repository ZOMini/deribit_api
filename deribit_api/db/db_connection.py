from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_async_engine(settings.data_base, echo=settings.debug)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)  # type: ignore[call-overload]


# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@asynccontextmanager
async def get_db_contextmanager():
    engine = create_async_engine(settings.data_base, echo=settings.debug)
    session = AsyncSession(engine, expire_on_commit=False)
    try:
        yield session
    finally:
        await session.close()
