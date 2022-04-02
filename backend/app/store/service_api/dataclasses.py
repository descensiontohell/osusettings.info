from dataclasses import dataclass


@dataclass
class Superuser:
    name: str
    password: str


@dataclass
class Admin:
    osu_id: int
    name: str
