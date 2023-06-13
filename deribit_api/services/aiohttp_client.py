import asyncio
from contextlib import asynccontextmanager

import aiohttp

from core.config import settings


@asynccontextmanager
async def get_aiohttp():
    client = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(
            None,
            connect=settings.main_timeout,
            sock_read=settings.main_timeout + 2.0,
            sock_connect=settings.main_timeout),
        connector=aiohttp.TCPConnector(
            limit=settings.max_connections,
            loop=asyncio.get_event_loop(),
            keepalive_timeout=settings.main_timeout / 2,
            ssl=True))
    try:
        yield client
    finally:
        await client.close()
