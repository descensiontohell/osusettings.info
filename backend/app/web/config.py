import typing
from dataclasses import dataclass

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
    user: str
    password: str
    database: str


@dataclass
class RedisConfig:
    host: str


@dataclass
class Credentials:
    client_id: int
    client_secret: str
    grant_type: str
    scope: str


@dataclass
class Config:
    superuser: SuperuserConfig
    session: SessionConfig = None
    database: DatabaseConfig = None
    redis: RedisConfig = None
    credentials: Credentials = None


def setup_config(app: "Application", config_path: str):

    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)
    app.config = Config(
        credentials=Credentials(
            client_id=raw_config["credentials"]["client_id"],
            client_secret=raw_config["credentials"]["client_secret"],
            grant_type=raw_config["credentials"]["grant_type"],
            scope=raw_config["credentials"]["scope"],
        ),
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        superuser=SuperuserConfig(
            login=raw_config["superuser"]["login"],
            password=raw_config["superuser"]["password"],
        ),
        database=DatabaseConfig(
            host=raw_config["database"]["host"],
            user=raw_config["database"]["user"],
            password=raw_config["database"]["password"],
            database=raw_config["database"]["database"],
        ),
        redis=RedisConfig(
            host=raw_config["redis"]["host"],
        ),
    )









