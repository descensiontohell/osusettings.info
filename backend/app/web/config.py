import typing
from dataclasses import dataclass
from typing import Optional

import yaml

if typing.TYPE_CHECKING:
    from app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class SuperuserConfig:
    login: str
    password: str


@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class Config:
    superuser: SuperuserConfig
    session: SessionConfig = None
    database: DatabaseConfig = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        superuser=SuperuserConfig(
            login=raw_config["superuser"]["login"],
            password=raw_config["superuser"]["password"],
        ),
        database=DatabaseConfig(**raw_config["database"]),
    )









