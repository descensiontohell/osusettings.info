import datetime

from typing import Optional

from attr import dataclass


@dataclass
class Playstyle:
    id: int
    name: str


@dataclass
class Mouse:
    id: int = None
    name: str = None
    width: int = None
    height: int = None
    length: int = None
    weight: int = None
    sensor: str = None
    switch: str = None


@dataclass
class Mousepad:
    id: int = None
    name: str = None


@dataclass
class Tablet:
    id: int = None
    name: str = None


@dataclass
class Keyboard:
    id: int = None
    name: str = None


@dataclass
class Switch:
    id: int = None
    name: str = None


@dataclass
class Player:
    last_updated: datetime.date
    is_admin: bool
    osu_id: int
    name: str
    global_rank: int
    performance: float
    is_restricted: bool
    is_mouse: bool
    country: str
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
    polling_rate: int
    play_area_width: int
    play_area_height: int
    refresh_rate: int
    raw_input: bool
    mouse: Optional[Mouse]
    mousepad: Optional[Mousepad]
    tablet: Optional[Tablet]
    keyboard: Optional[Keyboard]
    switch: Optional[Switch]
    is_active: bool


@dataclass
class Settings:
    last_updated: datetime.date
    osu_id: int
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
    polling_rate: int
    play_area_width: int
    play_area_height: int
    refresh_rate: int
    raw_input: bool
    mouse: Optional[Mouse]
    mousepad: Optional[Mousepad]
    tablet: Optional[Tablet]
    keyboard: Optional[Keyboard]
    switch: Optional[Switch]
