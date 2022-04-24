from marshmallow import Schema, fields


class MouseSuggestionsListSchema(Schema):
    mice = fields.Nested("MouseSchema", many=True)


class MousepadSuggestionsListSchema(Schema):
    mousepads = fields.Nested("MousepadSchema", many=True)


class KeyboardSuggestionsListSchema(Schema):
    keyboards = fields.Nested("KeyboardSchema", many=True)


class SwitchSuggestionsListSchema(Schema):
    switches = fields.Nested("SwitchSchema", many=True)


class TabletSuggestionsListSchema(Schema):
    tablets = fields.Nested("TabletSchema", many=True)


