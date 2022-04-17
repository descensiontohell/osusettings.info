import typing
import aioredis

if typing.TYPE_CHECKING:
    from app import Application


def setup_redis(app: "Application"):
    redis = aioredis.from_url(f"redis://{app.config.redis.host}")
    app.redis = redis


