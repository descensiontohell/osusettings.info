import typing
from typing import Optional

from osu import AsynchronousClient, AuthHandler, Scope

from backend.app.store.base.base_accessor import BaseAccessor
from backend.app.web.player_stats import PlayerStats

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class AuthAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "Auth", *args, **kwargs)
        self.app = app
        self.auth: Optional[AuthHandler] = None

    async def connect(self, app: "Application"):
        self.auth = AuthHandler(
            client_id=self.app.config.credentials.client_id,
            client_secret=self.app.config.credentials.client_secret,
            redirect_url=self.app.config.credentials.server_name,
            scope=Scope.identify(),
        )

    async def identify_player(self, oauth_code: str) -> dict:
        self.auth.get_auth_token(oauth_code)
        osu_api_client = AsynchronousClient(self.auth)
        user = await osu_api_client.get_own_data("osu")
        return {
            "osu_id": user.id,
            "name": user.username,
            "global_rank": user.statistics.global_rank,
            "performance": user.statistics.pp,
            "country": user.country_code,
            "is_restricted": user.is_restricted,
        }
