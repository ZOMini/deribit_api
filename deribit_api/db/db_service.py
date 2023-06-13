import datetime
from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from core.logger import logging
from db.db_connection import get_db
from db.db_models import Currency

logger = logging.getLogger(__name__)


class DBService:
    def __init__(self, db_conn: AsyncSession):
        self.db_conn = db_conn

    async def all_by_currency(self, ticker) -> Sequence[Currency]:
        scalars = await self.db_conn.scalars(
            select(Currency).filter(Currency.ticker == ticker)
            .order_by(Currency.timestamp.desc()))
        return scalars.all()

    async def last_currency(self, ticker) -> Currency:
        scalar = await self.db_conn.scalar(
            select(Currency).filter(Currency.ticker == ticker)
            .order_by(Currency.timestamp.desc()).limit(1))
        return scalar

    async def currency_by_date(self, ticker, date) -> Sequence[Currency]:
        scalars = await self.db_conn.scalars(
            select(Currency).filter(Currency.ticker == ticker)
            .filter(Currency.timestamp.between(
                date, date + datetime.timedelta(days=1)))
            .order_by(Currency.timestamp.desc()))
        return scalars.all()


def get_db_service(
    db_conn: AsyncSession = Depends(get_db),
) -> DBService:
    return DBService(db_conn)
