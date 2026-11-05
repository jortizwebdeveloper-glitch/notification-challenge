from pydantic_core import ValidationError

import src.core.db.models  # noqa: F401
from src.core.db import scope_async_session
from src.modules.send import SendData, SendRepository
from src.shared.channels import ChannelData, get_channel
from src.shared.errors import validation_error_handle

from .settings import REDIS_SETTINGS

SEND_REPO = "send_repo"


async def startup(ctx):
    pass


async def shutdown(ctx):
    pass


async def send_notification(ctx, payload):

    data: ChannelData = payload["data"]
    user_id: int = payload["user_id"]
    body = SendData(data.model_dump())
    try:
        channel = get_channel(data)
        result = await channel.send()
        body["content"] = result.content
        body["status"] = "success"

    except ValidationError as exc:
        errors = validation_error_handle(exc)
        body["status"] = "validation_error"
        body["log"] = str(errors)
        raise

    except Exception as e:
        body["status"] = "error"
        body["log"] = str(e)
        raise

    finally:
        print(body)
        async with scope_async_session() as session:
            sends = SendRepository(async_session=session)
            await sends.async_create(body, user_id)

    return "Finish"


class WorkerSettings:
    functions = [send_notification]  # noqa: RUF012
    redis_settings = REDIS_SETTINGS
    on_startup = startup
    on_shutdown = shutdown
    max_jobs = 10  # jobs concurrentes por worker
    job_timeout = 300  # segundos
    keep_result = 3600  # cuánto guardar el resultado
    max_tries = 3
    health_check_interval = 30
