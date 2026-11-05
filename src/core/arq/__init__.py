from fastapi import FastAPI, Request

from arq import create_pool
from src.shared.workers.settings import REDIS_SETTINGS


async def arq_pool(app: FastAPI):
    app.state.arq = await create_pool(REDIS_SETTINGS)
    yield
    await app.state.arq.close()


def get_arq(request: Request):
    return request.app.state.arq
