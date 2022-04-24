from marshmallow import Schema, fields


class MousepadSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)


class PlaystyleSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)


class SwitchSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)


class TabletSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)


class KeyboardSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)


class MouseSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)
    sensor = fields.Str(required=True)
    weight = fields.Int(required=True)
    length = fields.Int(required=True)
    width = fields.Int(required=True)
    height = fields.Int(required=True)
    switch = fields.Str(required=True)


class PlayerSchema(Schema):
    osu_id = fields.Int(required=True)
    name = fields.Str(required=True)
    global_rank = fields.Int(required=True)
    performance = fields.Float(required=True)
    is_banned = fields.Bool(required=True)
    is_restricted = fields.Bool(required=True)
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
    last_updated = fields.Date(required=True)
    mouse = fields.Nested("MouseSchema", many=False)
    mousepad = fields.Nested("MousepadSchema", many=False)
    tablet = fields.Nested("TabletSchema", many=False)
    keyboard = fields.Nested("KeyboardSchema", many=False)
    switch = fields.Nested("SwitchSchema", many=False)


class LeaderboardSchema(Schema):
    is_mouse_list = fields.Boolean(required=True)
    players = fields.Nested("PlayerSchema", many=True)


class GetPlayersQuerySchema(Schema):
    order_by = fields.Str()
    min_rank = fields.Int()
    max_rank = fields.Int()
    is_mouse = fields.Bool()
    playstyle = fields.List(fields.Int())
    #playstyle = fields.Str()
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

