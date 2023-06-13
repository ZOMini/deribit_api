import asyncio
from http import HTTPStatus

import aiohttp
import orjson
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.logger import logger
from db.db_connection import get_db_contextmanager
from db.db_models import Currency
from services.aiohttp_client import get_aiohttp

logger.name = 'worker'


class WorkerService:
    def __init__(self,
                 db_session: AsyncSession,
                 aio_session: aiohttp.ClientSession) -> None:
        self.db_session = db_session
        self.aio_session = aio_session

    async def post_db(self,
                      ticker: str,
                      ticker_value: float) -> Currency:
        obj = Currency(ticker=ticker, value=ticker_value)
        self.db_session.add(obj)
        return obj

    async def parse_response(self, r: aiohttp.ClientResponse, ticker) -> float:
        response_bin = await r.read()
        return orjson.loads(response_bin)['result'][ticker]

    async def request_and_post_db(  # type: ignore[return]
            self,
            ticker: str,
            url: str) -> tuple[int, Currency]:
        try:
            async with self.aio_session.get(url + ticker) as r:
                if r.status == HTTPStatus.OK:
                    ticker_value = await self.parse_response(r, ticker)
                    db_obj = await self.post_db(ticker, ticker_value)
                    return HTTPStatus.OK.value, db_obj
        except Exception as e:
            logger.error('url - %s exception - %s', url, e.args)
            await self.db_session.rollback()

    async def run_tasks(self, tickers: tuple, url: str) -> dict:
        tasks = [asyncio.ensure_future(
                 self.request_and_post_db(cur, url)) for cur in tickers]
        done, _ = await asyncio.wait(tasks)
        await self.db_session.commit()
        return {str(d.result()[1].id): int(d.result()[0]) for d in done}


async def run_works() -> dict:
    currencies = settings.currencies
    url = settings.currencies_url
    async with get_aiohttp() as aio_session:
        async with get_db_contextmanager() as pg_session:
            worker_service = WorkerService(pg_session, aio_session)
            result = await worker_service.run_tasks(currencies, url)
            logger.debug(result)
            return result


def worker_run():
    asyncio.run(run_works())
