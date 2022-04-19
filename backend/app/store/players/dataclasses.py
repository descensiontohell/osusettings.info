import datetime

from typing import Optional

from attr import dataclass


@dataclass
class Playstyle:
    id: int
    name: str


@dataclass
class Mouse:
    id: int
    name: str
    width: int
    height: int
    length: int
    weight: int
    sensor: str
    switch: str


@dataclass
class Mousepad:
    id: int
    name: str


@dataclass
class Tablet:
    id: int
    name: str


@dataclass
class Keyboard:
    id: int
    name: str


@dataclass
class Switch:
    id: int
    name: str


@dataclass
class Player:
    last_updated: datetime.datetime
    is_admin: bool
    osu_id: int
    name: str
    global_rank: int
    performance: int
    is_restricted: bool
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