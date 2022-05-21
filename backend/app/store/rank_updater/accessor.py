import json
from typing import Optional

from aiohttp import ClientSession, TCPConnector

from backend.app.store.base.base_accessor import BaseAccessor


class RankUpdater(BaseAccessor):
    def __init__(self, app, **kwargs):
        super().__init__(app=app, name=kwargs.get("name"))
        self.app = app
        self.session: Optional[ClientSession] = None
        self.update_token_in: int = 0
        self.access_token: Optional[str] = None
        self.client_id = app.config.credentials.client_id
        self.client_secret = app.config.credentials.client_secret
        self.grant_type = app.config.credentials.grant_type
        self.scope = app.config.credentials.scope

    async def connect(self, app):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=True))
        await self.obtain_access_token()

    async def obtain_access_token(self):
        async with self.session.post(
                url=self.app.const.TOKEN_API_PATH,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": self.grant_type,
                    "scope": self.scope,
                },
        ) as resp:
            data = await resp.json()
            self.update_token_in = data["expires_in"] - self.app.const.TOKEN_EXPIRE_HANDICAP
            self.access_token = data["access_token"]


