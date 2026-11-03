from arq.connections import RedisSettings
from pydantic_core import ValidationError

from src.shared.channels import ChannelData, get_channel
from src.shared.errors import validation_error_handle

REDIS_SETTINGS = RedisSettings(
    host="localhost",
    port=6379,
    database=0,
    password=None,
)


async def startup(ctx):
    # abrir conexiones a DB, clientes HTTP, etc.
    ctx["session"] = "mi-recurso"


async def shutdown(ctx):
    # cerrar recursos
    pass


async def send_notification(ctx, data: ChannelData):
    try:
        channel = get_channel(data)
        result = await channel.send()
        print(result.to)
    except ValidationError as exc:
        errors = validation_error_handle(exc)
        print(errors)
        raise

    except Exception as e:
        print(e)
        raise

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
