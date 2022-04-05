from marshmallow import Schema, fields


class SuperuserSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
