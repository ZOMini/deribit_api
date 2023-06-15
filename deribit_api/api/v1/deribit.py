import datetime
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status

from db.db_models import Currency
from db.db_service import DBService, get_db_service

router = APIRouter()

Ticker = Annotated[str, Query(required=True, enum=['BTC', 'ETH'])]


@router.get('/all_by_currency')
async def all_by_currency(
    ticker: Ticker,
    db_service: DBService = Depends(get_db_service),
) -> Sequence[Currency | None]:
    # Тут явно напрашивается пагинация, но в задании её нет.
    return await db_service.all_by_currency(ticker)


@router.get('/last_currency')
async def last_currency(
    ticker: Ticker,
    db_service: DBService = Depends(get_db_service),
) -> Currency | HTTPException:
    currency = await db_service.last_currency(ticker)
    if not currency:
        return HTTPException(status.HTTP_404_NOT_FOUND)
    return currency


@router.get('/currency_by_date')
async def currency_by_date(
    ticker: Ticker,
    date: datetime.date = Query('2023-06-13', required=True),
    db_service: DBService = Depends(get_db_service),
) -> Sequence[Currency | None]:
    return await db_service.currency_by_date(ticker, date)
