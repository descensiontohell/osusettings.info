from dataclasses import dataclass
from hashlib import sha256


@dataclass
class Superuser:
    name: str
    password: str

    def is_valid_password(self, pw: str) -> bool:
        return self.password == sha256(pw.encode()).hexdigest()


@dataclass
class Admin:
    osu_id: int
    name: str
