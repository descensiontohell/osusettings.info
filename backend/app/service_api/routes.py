from aiohttp.web_app import Application


def setup_routes(app: "Application"):
    from backend.app.service_api.views import SuperuserManageAdminsView
    from backend.app.service_api.views import SuperuserLoginView
    from backend.app.service_api.views import SuperuserCalculateEdpiView

    app.router.add_view("/api/su/login", SuperuserLoginView)
    app.router.add_view("/api/su/admins", SuperuserManageAdminsView)
    app.router.add_view("/api/su/edpi", SuperuserCalculateEdpiView)
