import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from models.deribit_models import Currency


@pytest_asyncio.fixture()
def pg_get_obj_by_id(pg_client: AsyncSession):
    async def inner(id: str):
        pg_obj = await pg_client.get(Currency, id)
        await pg_client.commit()
        return pg_obj
    return inner


@pytest_asyncio.fixture()
def pg_delete_obj_by_id(pg_client: AsyncSession):
    async def inner(obj: Currency):
        await pg_client.delete(obj)
        await pg_client.commit()
    return inner
