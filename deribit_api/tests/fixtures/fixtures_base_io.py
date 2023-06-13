import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_async_engine(settings.data_base, echo=True, query_cache_size=0)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def db_client():
    async_session: AsyncSession = sessionmaker(engine,
                                               class_=AsyncSession,
                                               expire_on_commit=False,
                                               autoflush=True)
    async with async_session() as session:
        yield session
