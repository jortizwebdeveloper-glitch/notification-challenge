from typing import Annotated

from fastapi import Depends, FastAPI, Request

from arq import ArqRedis, create_pool
from src.shared.worker import REDIS_SETTINGS


async def arq_pool(app: FastAPI):
    app.state.arq = await create_pool(REDIS_SETTINGS)
    yield
    await app.state.arq.close()


def get_arq(request: Request):
    return request.app.state.arq


ArqDep = Annotated[ArqRedis, Depends(get_arq)]
