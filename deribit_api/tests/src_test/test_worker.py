from http import HTTPStatus

import pytest

from db.db_models import Currency
from services.worker_service import run_works_async


@pytest.mark.asyncio
async def test_get_data_and_post_in_pg(db_get_obj_by_id, db_delete_obj_by_id):
    """Тестирует воркер. Статус гет запроса и произошла ли запись в БД."""
    worker_response = await run_works_async()
    for id, status in worker_response.items():
        obj = await db_get_obj_by_id(id)
        await db_delete_obj_by_id(obj)
        assert status == HTTPStatus.OK
        assert isinstance(obj, Currency)
