from backend.app.web.app import setup_app


async def app():
    app_ = setup_app()
    return app_
