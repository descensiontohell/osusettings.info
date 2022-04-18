import os

from backend.app.web.app import setup_app
from aiohttp.web import run_app

run_app(setup_app(config_path=os.path.join(os.getcwd(), 'config.yml')))
