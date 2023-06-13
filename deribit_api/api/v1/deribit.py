import datetime
from enum import Enum
from typing import Sequence

from fastapi import APIRouter, Depends, Query

from db.db_models import Currency
from db.db_service import DBService, get_db_service

router = APIRouter()


class Ticker(str, Enum):
    BTC = 'BTC'
    ETH = 'ETH'


@router.get('/all_by_currency')
async def all_by_currency(
    ticker: Ticker,
    db_service: DBService = Depends(get_db_service),
) -> Sequence[Currency]:
    # Тут явно напрашивается пагинация, но в задании её нет.
    return await db_service.all_by_currency(ticker)


@router.get('/last_currency')
async def last_currency(
    ticker: Ticker,
    db_service: DBService = Depends(get_db_service),
) -> Currency:
    return await db_service.last_currency(ticker)


@router.get('/currency_by_date')
async def currency_by_date(
    ticker: Ticker,
    date: datetime.date = Query('2023-06-13', required=True),
    db_service: DBService = Depends(get_db_service),
) -> Sequence[Currency]:
    return await db_service.currency_by_date(ticker, date)
