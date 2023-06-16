import asyncio

import aiohttp

from core.config import settings


def get_http_client() -> aiohttp.ClientSession:
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
    return client
