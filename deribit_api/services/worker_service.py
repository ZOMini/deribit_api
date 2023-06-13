import asyncio
from http import HTTPStatus

import aiohttp
import orjson
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.logger import logger
from db.pg import get_pg_contextmanager
from models.deribit_models import Currency
from services.aiohttp_client import get_aiohttp

logger.name = 'worker'


class WorkerService:
    pg_session: AsyncSession
    aio_session: aiohttp.ClientSession

    async def post_pg(self,
                      ticker: str,
                      ticker_value: float) -> Currency:
        obj = Currency(ticker=ticker, value=ticker_value)
        self.pg_session.add(obj)
        return obj

    async def parse_response(self, r: aiohttp.ClientResponse, ticker):
        response_bin = await r.read()
        return orjson.loads(response_bin)['result'][ticker]

    async def request_and_post_pg(  # type: ignore[return]
            self,
            ticker: str,
            url: str) -> tuple[int, Currency]:
        try:
            async with self.aio_session.get(url + ticker) as r:
                if r.status == HTTPStatus.OK:
                    ticker_value = await self.parse_response(r, ticker)
                    pg_obj = await self.post_pg(ticker, ticker_value)
                    return HTTPStatus.OK.value, pg_obj
        except Exception as e:
            logger.error('url - %s exception - %s', url, e.args)
            await self.pg_session.rollback()

    async def run_tasks(self, tickers: tuple, url: str) -> dict:
        async with get_aiohttp() as self.aio_session:
            async with get_pg_contextmanager() as self.pg_session:
                tasks = [asyncio.ensure_future(
                         self.request_and_post_pg(cur, url)) for cur in tickers]
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
