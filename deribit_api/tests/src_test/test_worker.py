from http import HTTPStatus

import pytest

from core.config import settings
from models.deribit_models import Currency
from services.worker_service import WorkerService


@pytest.mark.asyncio
async def test_get_data_and_post_in_pg(pg_get_obj_by_id, pg_delete_obj_by_id):
    """Тестирует воркер. Статус гет запроса и произошла ли запись в БД."""
    currencies = settings.currencies
    url = settings.currencies_url
    worker_service = WorkerService()
    worker_response = await worker_service.run_tasks(currencies, url)
    for id, status in worker_response.items():
        obj = await pg_get_obj_by_id(id)
        await pg_delete_obj_by_id(obj)
        assert status == HTTPStatus.OK
        assert isinstance(obj, Currency)
