from marshmallow import Schema, fields

from models.user_type import UserType


class PlainItemSchema(Schema):
    item_id = fields.Int(dump_only=True)
    name = fields.Str()
    price = fields.Int()
    description = fields.Str()
    active = fields.Boolean()
    image = fields.Str()
    tags = fields.List(fields.Str())


class ItemQueryArgs(Schema):
    active = fields.Boolean()


class PlainRestaurantSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    metadata = fields.Dict(required=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class MenuLayoutSchema(Schema):
    sort_order = fields.List(fields.String())
    # layout = fields.Dict(keys=fields.String(), values=fields.String())
    layout = fields.Dict(keys=fields.String(), values=fields.Nested('self'))


class RestaurantSchema(PlainRestaurantSchema):
    items = fields.List(fields.Nested(PlainItemSchema()))
    menu_layout = fields.Nested(MenuLayoutSchema())


class RestaurantUpdateSchema(Schema):
    metadata = fields.Dict()


class PlainOrderItemSchema(Schema):
    order_item_id = fields.Int(required=True)
    quantity = fields.Int(required=False)


class OrderItemSchema(Schema):
    order_item_id = fields.Int(dump_only=True)
    item_id = fields.Int(required=True)
    batch_id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    price = fields.Int(dump_only=True)
    quantity = fields.Int(required=True)
    instructions = fields.Str(required=False)
    timestamp = fields.DateTime(dump_only=True)


class PlainOrderSchema(Schema):
    table_id = fields.Int()
    order_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class OrderSchema(PlainOrderSchema):
    restaurant_id = fields.Int()
    active = fields.Boolean()
    items = fields.List(fields.Nested(OrderItemSchema()))


class BillItem(Schema):
    name = fields.Str()
    price = fields.Int()
    quantity = fields.Int()


class BillSchema(Schema):
    table_id = fields.Int()
    order_id = fields.Int()
    items = fields.List(fields.Nested(BillItem()))


class OrderQueryArgs(Schema):
    active = fields.Boolean()


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


class PlainTokenSchema(Schema):
    access_token = fields.Str()


class TokenSchema(PlainTokenSchema):
    refresh_token = fields.Str()
