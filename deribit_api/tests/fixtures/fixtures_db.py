import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_models import Currency


@pytest_asyncio.fixture()
def db_get_obj_by_id(db_client: AsyncSession):
    async def inner(id: str):
        db_obj = await db_client.get(Currency, id)
        await db_client.commit()
        return db_obj
    return inner


@pytest_asyncio.fixture()
def db_delete_obj_by_id(db_client: AsyncSession):
    async def inner(obj: Currency):
        await db_client.delete(obj)
        await db_client.commit()
    return inner
