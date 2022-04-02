import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Playstyle:
    name: str


@dataclass
class Mouse:
    brand: str
    model: str
    width: int
    height: int
    length: int
    weight: int
    sensor: str


@dataclass
class Tablet:
    name: str


@dataclass
class Keyboard:
    brand: str
    model: str


@dataclass
class Switch:
    name: str


@dataclass
class Player:
    last_updated: datetime.datetime
    is_admin: bool
    osu_id: int
    name: str
    global_rank: int
    performance: int
    is_mouse: bool
    playstyle: Optional[Playstyle]
    mouse_edpi: int
    tablet_area_width: int
    tablet_area_height: int
    dpi: int
    os_sens: int
    os_accel: bool
    multiplier: float
    res_width: int
    res_height: int
    refresh_rate: int
    raw_input: bool
    mouse: Optional[Mouse]
    tablet: Optional[Tablet]
    keyboard: Optional[Keyboard]
    switch: Optional[Switch]


@dataclass
class Settings:
    last_updated: datetime.datetime
    osu_id: int
    is_mouse: bool
    playstyle: Optional[Playstyle]
    mouse_edpi: int
    tablet_area_width: int
    tablet_area_height: int
    dpi: int
    os_sens: str
    os_accel: bool
    multiplier: float
    res_width: int
    res_height: int
    refresh_rate: int
    raw_input: bool
    mouse: Optional[Mouse]
    tablet: Optional[Tablet]
    keyboard: Optional[Keyboard]
    switch: Optional[Switch]

