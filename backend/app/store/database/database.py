import typing
from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class Database:

    def __init__(self, app: "Application"):
        self.app = app
        self.db: Optional[AsyncSession] = None

    async def connect(self, *_, **kw):
        try:
            self._engine = create_async_engine(
                f"postgresql+asyncpg://{self.app.config.database.user}:{self.app.config.database.password}@{self.app.config.database.host}/{self.app.config.database.database}",
                pool_size=20,
                max_overflow=0,
            )
        except Exception as e:
            self.app.logger.error("Exception", exc_info=e)
        self.db = sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def disconnect(self, *_, **kw):
        if self.db:
            #await self.db.close()
            self._engine = None
            self.db: Optional[AsyncSession] = None

