from marshmallow import Schema, fields


class MousepadSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=False)


class PlaystyleSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)


class SwitchSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=False)


class TabletSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=False)


class KeyboardSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=False)


class MouseSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=False)
    sensor = fields.Str(required=False)
    weight = fields.Int(required=False)
    length = fields.Int(required=False)
    width = fields.Int(required=False)
    height = fields.Int(required=False)
    switch = fields.Str(required=False)


class PlayerSchema(Schema):
    osu_id = fields.Int(required=True)
    name = fields.Str(required=True)
    global_rank = fields.Int(required=True)
    performance = fields.Float(required=True)
    is_banned = fields.Bool(required=True)
    is_restricted = fields.Bool(required=True)
    country = fields.Str(required=True)
    is_mouse = fields.Bool(required=True)
    playstyle = fields.Str(required=True)
    mouse_edpi = fields.Int(required=True)
    dpi = fields.Int(required=True)
    os_sens = fields.Int(required=True)
    os_accel = fields.Bool(required=True)
    multiplier = fields.Float(required=True)
    res_width = fields.Int(required=True)
    res_height = fields.Int(required=True)
    raw_input = fields.Bool(required=True)
    tablet_area_width = fields.Int()
    tablet_area_height = fields.Int()
    play_area_width = fields.Int()
    play_area_height = fields.Int()
    last_updated = fields.Date(required=True)
    mouse = fields.Nested("MouseSchema", many=False)
    mousepad = fields.Nested("MousepadSchema", many=False)
    tablet = fields.Nested("TabletSchema", many=False)
    keyboard = fields.Nested("KeyboardSchema", many=False)
    switch = fields.Nested("SwitchSchema", many=False)
    is_active = fields.Bool(required=True)
    updated_by = fields.Str(required=True)


class LeaderboardSchema(Schema):
    is_mouse_list = fields.Boolean(required=True)
    players = fields.Nested("PlayerSchema", many=True)


class GetPlayersQuerySchema(Schema):
    order_by = fields.Str()
    min_rank = fields.Int()
    max_rank = fields.Int()
    is_mouse = fields.Bool()
    playstyle = fields.List(fields.Int())
    page = fields.Int()
    name = fields.Str()
    country = fields.Str()
    min_edpi = fields.Int()
    max_edpi = fields.Int()
    min_area_width = fields.Int()
    min_area_height = fields.Int()
    max_area_width = fields.Int()
    max_area_height = fields.Int()
    mouse = fields.Str()
    mousepad = fields.Str()
    keyboard = fields.Str()
    switch = fields.Str()
    tablet = fields.Str()


class PreviousSettingsSchema(Schema):
    last_updated = fields.Date(required=True)
    is_mouse = fields.Bool()
    playstyle = fields.Str()
    mouse_edpi = fields.Int()
    tablet_area_width = fields.Int()
    tablet_area_height = fields.Int()
    dpi = fields.Int()
    os_sens = fields.Int()
    os_accel = fields.Bool()
    multiplier = fields.Float()
    res_width = fields.Int()
    res_height = fields.Int()
    polling_rate = fields.Int()
    play_area_width = fields.Int()
    play_area_height = fields.Int()
    refresh_rate = fields.Int()
    raw_input = fields.Bool()
    mouse = fields.Nested("MouseSchema", many=False)
    mousepad = fields.Nested("MousepadSchema", many=False)
    tablet = fields.Nested("TabletSchema", many=False)
    keyboard = fields.Nested("KeyboardSchema", many=False)
    switch = fields.Nested("SwitchSchema", many=False)
    updated_by = fields.Str(required=True)


class SettingsHistorySchema(Schema):
    settings = fields.Nested("PreviousSettingsSchema", many=True)


class UpdatePlayerSettingsSchema(Schema):
    add_new_mouse = fields.Bool()
    add_new_mousepad = fields.Bool()
    add_new_keyboard = fields.Bool()
    add_new_switch = fields.Bool()
    add_new_tablet = fields.Bool()
    last_updated = fields.Date(required=True)
    is_mouse = fields.Bool()
    playstyle = fields.Str()
    mouse_edpi = fields.Int()
    tablet_area_width = fields.Int()
    tablet_area_height = fields.Int()
    dpi = fields.Int()
    os_sens = fields.Int()
    os_accel = fields.Bool()
    multiplier = fields.Float()
    res_width = fields.Int()
    res_height = fields.Int()
    polling_rate = fields.Int()
    play_area_width = fields.Int()
    play_area_height = fields.Int()
    refresh_rate = fields.Int()
    raw_input = fields.Bool()
    mouse = fields.Nested("MouseSchema", many=False)
    mousepad = fields.Nested("MousepadSchema", many=False)
    tablet = fields.Nested("TabletSchema", many=False)
    keyboard = fields.Nested("KeyboardSchema", many=False)
    switch = fields.Nested("SwitchSchema", many=False)
    updated_by = fields.Str(required=True)
