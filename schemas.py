from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainRestaurantSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    restaurant_id = fields.Int(required=True, load_only=True)
    restaurant = fields.Nested(PlainRestaurantSchema(), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class RestaurantSchema(PlainRestaurantSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
