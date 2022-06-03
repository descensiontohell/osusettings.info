import typing

from osu import AsynchronousClient

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


def setup_osu_api(app: "Application"):
    client_id = app.config.credentials.client_id
    client_secret = app.config.credentials.client_secret
    redirect_url = app.config.credentials.server_name

    return AsynchronousClient.from_client_credentials(
        client_id=client_id,
        client_secret=client_secret,
        redirect_url=redirect_url,
    )
