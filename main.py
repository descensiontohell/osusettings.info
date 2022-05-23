import os

from backend.app.web.app import setup_app
from aiohttp.web import run_app

if os.environ.get("IS_IN_DOCKER", False):
    config_name = "config.yml"
else:
    config_name = "config_local.yml"

run_app(setup_app(config_path=os.path.join(os.path.abspath("."), config_name)))
