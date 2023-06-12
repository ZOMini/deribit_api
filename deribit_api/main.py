import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import deribit
from db.pg import async_session, migrate

app = FastAPI(
    title='deribit',
    docs_url='/deribit/api/openapi',
    openapi_url='/deribit/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(deribit.router, prefix='/deribit/api/v1', tags=['deribit'])


@app.on_event('startup')
async def startup():
    migrate()


@app.on_event('shutdown')
async def shutdown():
    try:
        await async_session.close_all()
    except TypeError:
        pass


if __name__ == '__main__':
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=8001,
                limit_max_requests=128,
                workers=1,
                reload=False)
