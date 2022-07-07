import typing
import aioredis

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


def setup_redis(app: "Application"):
    redis = aioredis.from_url(f"redis://{app.config.redis.host}")
    return redis
