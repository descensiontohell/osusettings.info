import os
from typing import Optional
from aiohttp.web import (
    Application as AiohttpApplication,
    View as AiohttpView,
    Request as AiohttpRequest,
)

from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_cors import CorsViewMixin

from backend.app.web.const import Const
from backend.app.web.cors import setup_cors
from backend.app.web.jinja import setup_jinja
from backend.app.web.middlewares import setup_middlewares
from backend.app.store.redis.redis import setup_redis
from backend.app.web.logger import setup_logging
from backend.app.store import setup_store, Store
from backend.app.store.database.database import Database
from backend.app.web.config import Config, setup_config
from backend.app.web.routes import setup_routes


class Application(AiohttpApplication):
    config: Optional[Config] = None
    store: Optional[Store] = None
    database: Optional[Database] = None
    const: Const = Const()
    admins: list[int] = []


class Request(AiohttpRequest):
    player_name: Optional[str] = None
    player_id: Optional[int] = None
    is_superuser: Optional[bool] = False
    is_admin: Optional[bool] = False

    @property
    def app(self) -> "Application":
        return super().app()


class View(AiohttpView, CorsViewMixin):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})


def setup_app(config_path: str = None) -> Application:
    if not config_path:
        config_path = os.path.join(os.path.abspath("."), 'config.yml')
    app = Application()
    setup_logging(app)
    setup_jinja(app)
    setup_config(app, config_path)
    setup_routes(app)
    setup_redis(app)
    setup_store(app)
    setup_session(app, RedisStorage(app.store.redis))
    setup_middlewares(app)
    setup_aiohttp_apispec(app, title="osusettings", url="/api/docs/json", swagger_path="/api/docs")
    setup_cors(app)
    return app
