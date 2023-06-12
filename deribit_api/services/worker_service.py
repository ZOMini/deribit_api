import asyncio
from http import HTTPStatus

import aiohttp
import orjson
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.config import settings
from core.logger import logger
from models.deribit_models import Currency

logger.name = 'worker'


class WorkerService:

    async def post_pg(self,
                      cur_name: str,
                      cur_value: float,
                      pg_session: AsyncSession) -> Currency:
        obj = Currency(ticker=cur_name, value=cur_value)
        pg_session.add(obj)
        return obj

    async def parse_response(self, r: aiohttp.ClientResponse, currency_name):
        response_bin = await r.read()
        return orjson.loads(response_bin)['result'][currency_name]

    async def request_and_post_pg(  #  type: ignore[return]
            self,
            client: aiohttp.ClientSession,
            pg_session: AsyncSession,
            currency_name: str,
            url: str) -> tuple[int, Currency]:  
        try:
            async with client.get(url + currency_name) as r:
                if r.status == HTTPStatus.OK:
                    currency_value = await self.parse_response(r, currency_name)
                    pg_obj = await self.post_pg(currency_name,
                                                currency_value,
                                                pg_session)
                    return HTTPStatus.OK.value, pg_obj
        except Exception as e:
            logger.error('url - %s exception - %s', url, e.args)
            await pg_session.rollback()

    async def run_tasks(self, currencies: tuple, url: str) -> dict:
        engine = create_async_engine(settings.data_base)
        async_session = AsyncSession(engine, expire_on_commit=False)
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(settings.main_timeout),
            connector=aiohttp.TCPConnector(
                limit=settings.max_connections,
                keepalive_timeout=settings.max_connections / 2,
                ssl=True)) as client:
            async with async_session as pg_session:
                tasks = [asyncio.ensure_future(
                         self.request_and_post_pg(client, pg_session, cur, url)) for cur in currencies]
                done, _ = await asyncio.wait(tasks)
                await pg_session.commit()
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
