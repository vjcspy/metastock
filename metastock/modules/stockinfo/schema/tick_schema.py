from marshmallow import Schema, fields


# Lược đồ cho phần tử trong mảng "meta"
class TickMetaItemSchema(Schema):
    time = fields.String(required=True)
    vol = fields.Integer(required=True)
    p = fields.Integer(required=True)
    a = fields.String(required=True)


# Lược đồ chính
class TickSchema(Schema):
    id = fields.Integer(required=True)
    symbol = fields.String(required=True)
    date = fields.DateTime(required=True)
    meta = fields.List(fields.Nested(TickMetaItemSchema), required=True)


tick_schema = TickSchema()
