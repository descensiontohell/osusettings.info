from aiohttp.web_app import Application


def setup_routes(app: "Application"):

    from backend.app.service_api.views import SuperuserLoginView
    app.router.add_view("/su.login", SuperuserLoginView)
