from marshmallow import Schema, fields


class SuperuserLoginSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
