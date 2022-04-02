import datetime

from sqlalchemy.sql import func

import typing
from dataclasses import dataclass
from typing import Optional, List

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, MetaData, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship

meta = MetaData()
Base = declarative_base(meta)


@dataclass
class Playstyle:
    name: str


class PlaystyleModel(Base):
    __tablename__ = "playstyle"
    id = Column(Integer(), primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    player = relationship("PlayerModel", back_populates="playstyle")
    settings = relationship("SettingsModel", back_populates="playstyle")

    def to_dc(self):
        return Playstyle(name=self.name)


@dataclass
class Mouse:
    brand: str
    model: str
    width: int
    height: int
    length: int
    weight: int
    sensor: str


class MouseModel(Base):
    __tablename__ = "mouse"
    id = Column(Integer(), primary_key=True)
    brand = Column(String(), nullable=False)
    model = Column(String(), nullable=False)
    width = Column(Integer(), nullable=True)
    height = Column(Integer(), nullable=True)
    length = Column(Integer(), nullable=True)
    weight = Column(Integer(), nullable=True)
    sensor = Column(String(), nullable=True)
    player = relationship("PlayerModel", back_populates="mouse")
    settings = relationship("SettingsModel", back_populates="mouse")

    def to_dc(self):
        return Mouse(
            brand=self.brand,
            model=self.model,
            width=self.width,
            height=self.height,
            length=self.length,
            weight=self.weight,
            sensor=self.sensor,
        )


@dataclass
class Tablet:
    name: str


class TabletModel(Base):
    __tablename__ = "tablet"
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    player = relationship("PlayerModel", back_populates="tablet")
    settings = relationship("SettingsModel", back_populates="tablet")

    def to_dc(self):
        return Tablet(name=self.name)


@dataclass
class Keyboard:
    brand: str
    model: str


class KeyboardModel(Base):
    __tablename__ = "keyboard"
    id = Column(Integer(), primary_key=True)
    brand = Column(String(), nullable=False)
    model = Column(String(), nullable=False)
    player = relationship("PlayerModel", back_populates="keyboard")
    settings = relationship("SettingsModel", back_populates="keyboard")

    def to_dc(self):
        return Keyboard(brand=self.brand, model=self.model)


@dataclass
class Switch:
    name: str


class SwitchModel(Base):
    __tablename__ = 'switch'
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    player = relationship("PlayerModel", back_populates="switch")
    settings = relationship("SettingsModel", back_populates="switch")

    def to_dc(self):
        return Switch(name=self.name)


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


class PlayerModel(Base):
    __tablename__ = "players"
    last_updated = Column(DateTime(), nullable=False, server_default=func.now())
    is_admin = Column(Boolean(), nullable=False, default=False)
    osu_id = Column(Integer(), primary_key=True)
    name = Column(String(20), nullable=False)
    global_rank = Column(Integer(), nullable=True)
    performance = Column(Float(10), nullable=True)
    is_mouse = Column(Boolean(), nullable=True)
    playstyle_id = Column(Integer(), ForeignKey("playstyle.id"))
    playstyle = relationship("PlaystyleModel", back_populates="player")
    mouse_edpi = Column(Integer(), nullable=True)
    tablet_area_width = Column(Integer(), nullable=True)
    tablet_area_height = Column(Integer(), nullable=True)
    dpi = Column(Integer(), nullable=True)
    os_sens = Column(Integer(), nullable=True)
    os_accel = Column(Boolean(), nullable=True)
    multiplier = Column(Float(), nullable=True)
    res_width = Column(Integer(), nullable=True)
    res_height = Column(Integer(), nullable=True)
    refresh_rate = Column(Integer(), nullable=True)
    raw_input = Column(Boolean(), nullable=True)
    mouse_id = Column(Integer(), ForeignKey("mouse.id"))
    mouse = relationship("MouseModel", back_populates="player")
    tablet_id = Column(Integer(), ForeignKey("tablet.id"))
    tablet = relationship("TabletModel", back_populates="player")
    keyboard_id = Column(Integer(), ForeignKey("keyboard.id"))
    keyboard = relationship("KeyboardModel", back_populates="player")
    switch_id = Column(Integer(), ForeignKey("switch.id"))
    switch = relationship("SwitchModel", back_populates="player")

    def to_dc(self):
        if self.playstyle is not None:
            playstyle = self.playstyle.to_dc().name
        else:
            playstyle = None

        if self.mouse is not None:
            mouse = self.mouse.to_dc()
        else:
            mouse = None

        if self.tablet is not None:
            tablet = self.tablet.to_dc()
        else:
            tablet = None

        if self.keyboard is not None:
            keyboard = self.keyboard.to_dc()
        else:
            keyboard = None

        if self.switch is not None:
            switch = self.switch.to_dc()
        else:
            switch = None

        return Player(
            last_updated=self.last_updated,
            is_admin=self.is_admin,
            osu_id=self.osu_id,
            name=self.name,
            global_rank=self.global_rank,
            performance=self.performance,
            is_mouse=self.is_mouse,
            playstyle=playstyle,
            mouse_edpi=self.mouse_edpi,
            tablet_area_width=self.tablet_area_width,
            tablet_area_height=self.tablet_area_height,
            dpi=self.dpi,
            os_sens=self.os_sens,
            os_accel=self.os_accel,
            multiplier=self.multiplier,
            res_width=self.res_width,
            res_height=self.res_height,
            refresh_rate=self.refresh_rate,
            raw_input=self.raw_input,
            mouse=mouse,
            tablet=tablet,
            keyboard=keyboard,
            switch=switch,
        )


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


class SettingsModel(Base):
    __tablename__ = "previous_settings"
    id = Column(Integer(), primary_key=True)
    last_updated = Column(DateTime(), nullable=False, server_default=func.now())
    osu_id = Column(Integer(), ForeignKey("players.osu_id"), nullable=False)
    is_mouse = Column(Boolean(), nullable=True)
    playstyle = relationship("PlaystyleModel", back_populates="settings")
    playstyle_id = Column(Integer(), ForeignKey("playstyle.id"))
    mouse_edpi = Column(Integer(), nullable=True)
    tablet_area_width = Column(Integer(), nullable=True)
    tablet_area_height = Column(Integer(), nullable=True)
    dpi = Column(Integer(), nullable=True)
    os_sens = Column(Integer(), nullable=True)
    os_accel = Column(Boolean(), nullable=True)
    multiplier = Column(Float(), nullable=True)
    res_width = Column(Integer(), nullable=True)
    res_height = Column(Integer(), nullable=True)
    refresh_rate = Column(Integer(), nullable=True)
    raw_input = Column(Boolean(), nullable=True)
    mouse_id = Column(Integer(), ForeignKey("mouse.id"))
    mouse = relationship("MouseModel", back_populates="settings")
    tablet_id = Column(Integer(), ForeignKey("tablet.id"))
    tablet = relationship("TabletModel", back_populates="settings")
    keyboard_id = Column(Integer(), ForeignKey("keyboard.id"))
    keyboard = relationship("KeyboardModel", back_populates="settings")
    switch_id = Column(Integer(), ForeignKey("switch.id"))
    switch = relationship("SwitchModel", back_populates="settings")

    def to_dc(self):
        if self.playstyle is not None:
            playstyle = self.playstyle.to_dc().name
        else:
            playstyle = None

        if self.mouse is not None:
            mouse = self.mouse.to_dc()
        else:
            mouse = None

        if self.tablet is not None:
            tablet = self.tablet.to_dc()
        else:
            tablet = None

        if self.keyboard is not None:
            keyboard = self.keyboard.to_dc()
        else:
            keyboard = None

        if self.switch is not None:
            switch = self.switch.to_dc()
        else:
            switch = None

        return Settings(
            last_updated=self.last_updated,
            osu_id=self.osu_id,
            is_mouse=self.is_mouse,
            playstyle=playstyle,
            mouse_edpi=self.mouse_edpi,
            tablet_area_width=self.tablet_area_width,
            tablet_area_height=self.tablet_area_height,
            dpi=self.dpi,
            os_sens=self.os_sens,
            os_accel=self.os_accel,
            multiplier=self.multiplier,
            res_width=self.res_width,
            res_height=self.res_height,
            refresh_rate=self.refresh_rate,
            raw_input=self.raw_input,
            mouse=mouse,
            tablet=tablet,
            keyboard=keyboard,
            switch=switch,
        )

