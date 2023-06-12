import asyncio
from http import HTTPStatus

import aiohttp
import orjson
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.config import settings
from core.logger import logger
from models.deribit_models import Currency
from services.aiohttp_client import get_aiohttp

logger.name = 'worker'


class WorkerService:
    pg_session: AsyncSession
    aio_session: aiohttp.ClientSession

    async def post_pg(self,
                      cur_name: str,
                      cur_value: float) -> Currency:
        obj = Currency(ticker=cur_name, value=cur_value)
        self.pg_session.add(obj)
        return obj

    async def parse_response(self, r: aiohttp.ClientResponse, currency_name):
        response_bin = await r.read()
        return orjson.loads(response_bin)['result'][currency_name]

    async def request_and_post_pg(  # type: ignore[return]
            self,
            currency_name: str,
            url: str) -> tuple[int, Currency]:
        try:
            async with self.aio_session.get(url + currency_name) as r:
                if r.status == HTTPStatus.OK:
                    currency_value = await self.parse_response(r, currency_name)
                    pg_obj = await self.post_pg(currency_name, currency_value)
                    return HTTPStatus.OK.value, pg_obj
        except Exception as e:
            logger.error('url - %s exception - %s', url, e.args)
            await self.pg_session.rollback()

    async def run_tasks(self, currencies: tuple, url: str) -> dict:
        engine = create_async_engine(settings.data_base)
        async with get_aiohttp() as self.aio_session:
            async with AsyncSession(engine, expire_on_commit=False) as self.pg_session:
                tasks = [asyncio.ensure_future(
                         self.request_and_post_pg(cur, url)) for cur in currencies]
                done, _ = await asyncio.wait(tasks)
                await self.pg_session.commit()
                return {str(d.result()[1].id): int(d.result()[0]) for d in done}

    def run_works(self):
        currencies = settings.currencies
        url = settings.currencies_url
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(self.run_tasks(currencies, url))
        loop.run_until_complete(asyncio.sleep(0.0))
        loop.close()
        logger.debug(result)
        return result
