import typing
from dataclasses import dataclass

from envyaml import EnvYAML

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
    server_name: str


@dataclass
class Config:
    superuser: SuperuserConfig
    session: SessionConfig = None
    database: DatabaseConfig = None
    redis: RedisConfig = None
    credentials: Credentials = None


def setup_config(app: "Application", config_path: str):
    env = EnvYAML(config_path)
    app.config = Config(
        credentials=Credentials(
            client_id=env["credentials.client_id"],
            client_secret=env["credentials.client_secret"],
            grant_type=env["credentials.grant_type"],
            scope=env["credentials.scope"],
            server_name=env["credentials.server_name"],
        ),
        session=SessionConfig(
            key=env["session.key"],
        ),
        superuser=SuperuserConfig(
            login=env["superuser.login"],
            password=str(env["superuser.password"]),
        ),
        database=DatabaseConfig(
            host=env["database.host"],
            user=env["database.user"],
            password=env["database.password"],
            database=env["database.database"],
        ),
        redis=RedisConfig(
            host=env["redis.host"],
        ),
    )
