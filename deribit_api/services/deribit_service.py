import datetime
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from core.logger import logging
from db.pg import get_pg
from models.deribit_models import Currency

logger = logging.getLogger(__name__)


class DeribitService:
    def __init__(self, pg_conn: AsyncSession):
        self.pg_conn = pg_conn

    async def all_by_currency(self, ticker) -> list[Currency]:
        scalars = await self.pg_conn.scalars(
            select(Currency).filter(Currency.ticker == ticker)
            .order_by(Currency.timestamp.desc()))
        return scalars.all()


    async def last_currency(self, ticker) -> Currency:
        scalar = await self.pg_conn.scalar(
            select(Currency).filter(Currency.ticker == ticker)
            .order_by(Currency.timestamp.desc()).limit(1))
        return scalar


    async def currency_by_date(self, ticker, date) -> list[Currency]:
        scalars = await self.pg_conn.scalars(
            select(Currency).filter(Currency.ticker == ticker)
            .filter(Currency.timestamp.between(
                date, date+datetime.timedelta(days=1)))
            .order_by(Currency.timestamp.desc()))
        return scalars.all()

@lru_cache()
def get_deribit_service(
    pg_conn: AsyncSession = Depends(get_pg),
) -> DeribitService:
    return DeribitService(pg_conn)
