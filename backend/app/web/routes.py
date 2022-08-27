from aiohttp.web_app import Application


def setup_routes(app: "Application"):
    from backend.app.auth.routes import setup_routes as auth_setup_routes
    from backend.app.items.routes import setup_routes as items_setup_routes
    from backend.app.players.routes import setup_routes as player_setup_routes
    from backend.app.service_api.routes import setup_routes as service_setup_routes

    service_setup_routes(app)
    auth_setup_routes(app)
    player_setup_routes(app)
    items_setup_routes(app)
