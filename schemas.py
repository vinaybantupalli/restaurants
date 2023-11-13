from marshmallow import Schema, fields

from models.user_type import UserType


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


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    user_type = fields.Enum(UserType, required=True, dump_only=True)


class OwnerSchema(UserSchema):
    restaurant_id = fields.Int(required=True)


class PlainTableSchema(Schema):
    table_id = fields.Int(required=True)


class TableSchema(PlainTableSchema):
    restaurant_id = fields.Int(required=True)


class TableOtpSchema(Schema):
    otp = fields.Int(required=True)
