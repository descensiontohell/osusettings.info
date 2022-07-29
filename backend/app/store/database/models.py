from sqlalchemy.sql import func

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, MetaData, Float, Date
from sqlalchemy.orm import declarative_base, relationship

from backend.app.store.players.dataclasses import Playstyle, Mouse, Tablet, Keyboard, Switch, Player, Settings, Mousepad

from backend.app.store.service_api.dataclasses import Superuser, Admin

meta = MetaData()
Base = declarative_base(meta)


class PlaystyleModel(Base):
    __tablename__ = "playstyle"
    id = Column(Integer(), primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    is_mouse = Column(Boolean())
    player = relationship("PlayerModel", back_populates="playstyle")
    settings = relationship("SettingsModel", back_populates="playstyle")

    def to_dc(self):
        return Playstyle(
            id=self.id,
            name=self.name,
            is_mouse=self.is_mouse,
        )


class MouseModel(Base):
    __tablename__ = "mouse"
    id = Column(Integer(), primary_key=True)
    relevance = Column(Integer(), default=0)
    name = Column(String(), nullable=False)
    width = Column(Integer(), nullable=True)
    height = Column(Integer(), nullable=True)
    length = Column(Integer(), nullable=True)
    weight = Column(Integer(), nullable=True)
    sensor = Column(String(), nullable=True)
    switch = Column(String(), nullable=True)
    player = relationship("PlayerModel", back_populates="mouse")
    settings = relationship("SettingsModel", back_populates="mouse")

    def to_dc(self):
        return Mouse(
            id=self.id,
            name=self.name,
            width=self.width,
            height=self.height,
            length=self.length,
            weight=self.weight,
            sensor=self.sensor,
            switch=self.switch,
        )


class TabletModel(Base):
    __tablename__ = "tablet"
    id = Column(Integer(), primary_key=True)
    relevance = Column(Integer(), default=0)
    name = Column(String(), nullable=False)
    player = relationship("PlayerModel", back_populates="tablet")
    settings = relationship("SettingsModel", back_populates="tablet")

    def to_dc(self):
        return Tablet(
            id=self.id,
            name=self.name,
        )


class KeyboardModel(Base):
    __tablename__ = "keyboard"
    id = Column(Integer(), primary_key=True)
    relevance = Column(Integer(), default=0)
    name = Column(String(), nullable=False)
    player = relationship("PlayerModel", back_populates="keyboard")
    settings = relationship("SettingsModel", back_populates="keyboard")

    def to_dc(self):
        return Keyboard(
            id=self.id,
            name=self.name,
        )


class SwitchModel(Base):
    __tablename__ = 'switch'
    id = Column(Integer(), primary_key=True)
    relevance = Column(Integer(), default=0)
    name = Column(String(), nullable=False)
    player = relationship("PlayerModel", back_populates="switch")
    settings = relationship("SettingsModel", back_populates="switch")

    def to_dc(self):
        return Switch(
            id=self.id,
            name=self.name,
        )


class MousepadModel(Base):
    __tablename__ = 'mousepad'
    id = Column(Integer(), primary_key=True)
    relevance = Column(Integer(), default=0)
    name = Column(String(), nullable=False)
    player = relationship("PlayerModel", back_populates="mousepad")
    settings = relationship("SettingsModel", back_populates="mousepad")

    def to_dc(self):
        return Mousepad(
            id=self.id,
            name=self.name,
        )


class PlayerModel(Base):
    __tablename__ = "players"
    last_updated = Column(Date(), nullable=True, server_default=func.now())
    is_admin = Column(Boolean(), nullable=True, server_default="false")
    osu_id = Column(Integer(), primary_key=True)
    name = Column(String(20), nullable=False)
    country_code = Column(String())
    global_rank = Column(Integer(), nullable=True)
    performance = Column(Float(10), nullable=True)
    is_banned = Column(Boolean(), nullable=False)
    is_restricted = Column(Boolean(), nullable=False)
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
    polling_rate = Column(Integer(), nullable=True)
    play_area_width = Column(Integer(), nullable=True)
    play_area_height = Column(Integer(), nullable=True)
    refresh_rate = Column(Integer(), nullable=True)
    raw_input = Column(Boolean(), nullable=True)
    mouse_id = Column(Integer(), ForeignKey("mouse.id"))
    mouse = relationship("MouseModel", back_populates="player")
    mousepad_id = Column(Integer(), ForeignKey("mousepad.id"))
    mousepad = relationship("MousepadModel", back_populates="player")
    tablet_id = Column(Integer(), ForeignKey("tablet.id"))
    tablet = relationship("TabletModel", back_populates="player")
    keyboard_id = Column(Integer(), ForeignKey("keyboard.id"))
    keyboard = relationship("KeyboardModel", back_populates="player")
    switch_id = Column(Integer(), ForeignKey("switch.id"))
    switch = relationship("SwitchModel", back_populates="player")
    updated_by = Column(String(), nullable=False)
    is_active = Column(Boolean(), nullable=False, server_default="true")

    def to_dc(self):
        if self.playstyle is not None:
            playstyle = self.playstyle.to_dc().name
        else:
            playstyle = None

        if self.mouse is not None:
            mouse = self.mouse.to_dc()
        else:
            mouse = Mouse()

        if self.mousepad is not None:
            mousepad = self.mousepad.to_dc()
        else:
            mousepad = Mousepad()

        if self.tablet is not None:
            tablet = self.tablet.to_dc()
        else:
            tablet = Tablet()

        if self.keyboard is not None:
            keyboard = self.keyboard.to_dc()
        else:
            keyboard = Keyboard()

        if self.switch is not None:
            switch = self.switch.to_dc()
        else:
            switch = Switch()

        return Player(
            last_updated=self.last_updated,
            is_admin=self.is_admin,
            osu_id=self.osu_id,
            name=self.name,
            global_rank=self.global_rank,
            performance=self.performance,
            is_restricted=self.is_restricted,
            is_mouse=self.is_mouse,
            country=self.country_code,
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
            polling_rate=self.polling_rate,
            play_area_width=self.play_area_width,
            play_area_height=self.play_area_height,
            refresh_rate=self.refresh_rate,
            raw_input=self.raw_input,
            mouse=mouse,
            mousepad=mousepad,
            tablet=tablet,
            keyboard=keyboard,
            switch=switch,
            is_active=self.is_active,
            updated_by=self.updated_by,
        )


class SettingsModel(Base):
    __tablename__ = "previous_settings"
    id = Column(Integer(), primary_key=True)
    last_updated = Column(Date(), nullable=True, server_default=func.now())
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
    polling_rate = Column(Integer(), nullable=True)
    play_area_width = Column(Integer(), nullable=True)
    play_area_height = Column(Integer(), nullable=True)
    refresh_rate = Column(Integer(), nullable=True)
    raw_input = Column(Boolean(), nullable=True)
    mouse_id = Column(Integer(), ForeignKey("mouse.id"))
    mouse = relationship("MouseModel", back_populates="settings")
    mousepad_id = Column(Integer(), ForeignKey("mousepad.id"))
    mousepad = relationship("MousepadModel", back_populates="settings")
    tablet_id = Column(Integer(), ForeignKey("tablet.id"))
    tablet = relationship("TabletModel", back_populates="settings")
    keyboard_id = Column(Integer(), ForeignKey("keyboard.id"))
    keyboard = relationship("KeyboardModel", back_populates="settings")
    switch_id = Column(Integer(), ForeignKey("switch.id"))
    switch = relationship("SwitchModel", back_populates="settings")
    updated_by = Column(String(), nullable=False)

    def to_dc(self):
        if self.playstyle is not None:
            playstyle = self.playstyle.to_dc().name
        else:
            playstyle = None

        if self.mouse is not None:
            mouse = self.mouse.to_dc()
        else:
            mouse = Mouse()

        if self.mousepad is not None:
            mousepad = self.mousepad.to_dc()
        else:
            mousepad = Mousepad()

        if self.tablet is not None:
            tablet = self.tablet.to_dc()
        else:
            tablet = Tablet()

        if self.keyboard is not None:
            keyboard = self.keyboard.to_dc()
        else:
            keyboard = Keyboard()

        if self.switch is not None:
            switch = self.switch.to_dc()
        else:
            switch = Switch()

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
            polling_rate=self.polling_rate,
            play_area_width=self.play_area_width,
            play_area_height=self.play_area_height,
            refresh_rate=self.refresh_rate,
            raw_input=self.raw_input,
            mouse=mouse,
            mousepad=mousepad,
            tablet=tablet,
            keyboard=keyboard,
            switch=switch,
            updated_by=self.updated_by,
        )


class SuperuserModel(Base):
    __tablename__ = "superuser"
    name = Column(String(), primary_key=True)
    password = Column(String())

    def to_dc(self):
        return Superuser(name=self.name, password=self.password)


class AdminModel(Base):
    __tablename__ = "admins"
    osu_id = Column(Integer(), primary_key=True)
    name = Column(String())

    def to_dc(self):
        return Admin(osu_id=self.osu_id, name=self.name)
