from arq.connections import RedisSettings

from src.shared.settings import settings

host = settings.REDIS_HOST or "localhost"
REDIS_SETTINGS = RedisSettings(
    host=host,
    port=6379,
    database=0,
    password=None,
)
