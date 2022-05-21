from marshmallow import Schema, fields


class SuperuserLoginRequestSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class SuperuserLoginResponseSchema(Schema):
    name = fields.Str(required=True)


class SuperuserManageAdminsSchema(Schema):
    osu_id = fields.Int(required=True)


class AdminSchema(Schema):
    name = fields.Str(required=True)
    osu_id = fields.Int(required=True)


class ListAdminsSchema(Schema):
    admins = fields.Nested("AdminSchema", many=True)
