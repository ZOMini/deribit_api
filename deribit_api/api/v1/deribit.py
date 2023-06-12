import datetime
from enum import Enum

from fastapi import APIRouter, Depends, Query

from models.deribit_models import Currency
from services.deribit_service import DeribitService, get_deribit_service

router = APIRouter()

class Ticker(str, Enum):
    BTC = 'BTC'
    ETH = 'ETH'

@router.get('/all_by_currency')
async def all_by_currency(
    tiker: Ticker,
    deribit_service: DeribitService = Depends(get_deribit_service),
) -> list[Currency]:
    # Тут явно напрашивается пагинация, но в задании её нет.
    return await deribit_service.all_by_currency(tiker)


@router.get('/last_currency')
async def last_currency(
    tiker: Ticker,
    deribit_service: DeribitService = Depends(get_deribit_service),
) -> Currency:
    return await deribit_service.last_currency(tiker)


@router.get('/currency_by_date')
async def currency_by_date(
    tiker: Ticker,
    date: datetime.date = Query('2023-06-13', required=True),
    deribit_service: DeribitService = Depends(get_deribit_service),
) -> list[Currency]:
    return await deribit_service.currency_by_date(tiker, date)
