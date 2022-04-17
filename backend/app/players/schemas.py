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
    brand = fields.Str(required=True)
    model = fields.Str(required=True)


class MouseSchema(Schema):
    id = fields.Int(required=False)
    brand = fields.Str(required=True)
    model = fields.Str(required=True)
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
    players = fields.Nested("PlayerSchema", many=True)

