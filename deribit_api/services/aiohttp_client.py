import asyncio
from contextlib import asynccontextmanager

import aiohttp


@asynccontextmanager
async def get_aiohttp():
    client = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=35,
                                       loop=asyncio.get_event_loop()))
    try:
        yield client
    finally:
        await client.close()
