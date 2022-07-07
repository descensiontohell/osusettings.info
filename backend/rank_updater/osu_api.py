from osu import AsynchronousClient


def setup_osu_api(config):
    client_id = config.credentials.client_id
    client_secret = config.credentials.client_secret
    redirect_url = f"{config.credentials.server_name}/callback"

    return AsynchronousClient.from_client_credentials(
        client_id=client_id,
        client_secret=client_secret,
        redirect_url=redirect_url,
    )
