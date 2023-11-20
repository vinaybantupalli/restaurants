import logging
from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from flask_smorest import abort

from models import Order, OrderItem, Restaurant
from resources.utils import is_admin_or_curr_owner_or_table, is_admin_or_curr_owner_by_id
from schemas import PlainOrderSchema, OrderSchema, OrderItemSchema

blp = Blueprint("Orders", "orders", description="Operations on orders")
logger = logging.getLogger(__name__)


@blp.route("/restaurant/<int:restaurant_id>/order")
class OrderUtils(MethodView):
    @jwt_required()
    @blp.response(200, OrderSchema(many=True))
    def get(self, restaurant_id):

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), restaurant_id):
            abort(403, message="Current user doesn't have access to get orders on this restaurant.")

        return Order.objects().order_by('-updated_at')

    @jwt_required()
    @blp.arguments(PlainOrderSchema)
    @blp.response(201, OrderSchema)
    def post(self, order_data, restaurant_id):
        table_id = order_data.get('table_id')

        if not is_admin_or_curr_owner_or_table(get_jwt_identity(), restaurant_id, table_id):
            abort(403, message="Current user doesn't have access to create orders on this table.")

        order = Order(restaurant_id=restaurant_id, table_id=table_id, active=True, updated_at=datetime.utcnow())
        order.save()
        return order, 201


@blp.route("/restaurant/<int:restaurant_id>/order/active")
class ActiveOrderUtils(MethodView):
    @jwt_required()
    @blp.response(200, OrderSchema(many=True))
    def get(self, restaurant_id):
        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), restaurant_id):
            abort(403, message="Current user doesn't have access to get orders on this restaurant.")

        return Order.objects(active=True).order_by('-updated_at')


@blp.route("/order/<int:order_id>")
class RestaurantOps(MethodView):
    @jwt_required()
    @blp.response(200, OrderSchema)
    def get(self, order_id):
        order = Order.objects(order_id=order_id).first()

        if not is_admin_or_curr_owner_or_table(get_jwt_identity(), order.restaurant_id, order.table_id):
            abort(403, message="Current user doesn't have access to view this order.")

        return order

    @blp.response(200)
    @jwt_required()
    def delete(self, order_id):
        order = Order.objects(id=order_id).first()

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), order.restaurant_id):
            abort(403, message="Current user doesn't have access to delete orders.")

        order.delete()
        return {"message": "Order Deleted Successfully"}, 200


@blp.route("/order/<int:order_id>/order_item")
class OrderItemsUtils(MethodView):
    @jwt_required()
    @blp.arguments(OrderItemSchema(many=True))
    @blp.response(200, OrderSchema)
    def post(self, order_item_data, order_id):
        order = Order.objects(order_id=order_id).first()

        if not is_admin_or_curr_owner_or_table(get_jwt_identity(), order.restaurant_id, order.table_id):
            abort(403, message="Current user doesn't have access to update this order.")

        curr_timestamp = datetime.utcnow()

        # get the highest batch_id in the current order's items
        highest_batch_id = 0
        if order.items:
            highest_batch_id = max(item.batch_id for item in order.items)

        for item_data in order_item_data:
            # retrieve the corresponding item from the restaurant document
            item_id = item_data['item_id']
            restaurant = Restaurant.objects(id=order.restaurant_id).first()
            item = next((item for item in restaurant.items if item.item_id == item_id), None)

            if item is None:
                abort(404, message="Item not found in the restaurant.")

            order_item = OrderItem(item_id=item_id, batch_id=highest_batch_id + 1, name=item.name, price=item.price,
                                   quantity=item_data['quantity'], instructions=item_data.get('instructions', ''),
                                   timestamp=curr_timestamp)

            order.items.append(order_item)
        order.save()
        return order, 200

    @jwt_required()
    @blp.response(200, OrderItemSchema(many=True))
    def get(self, order_id):
        order = Order.objects(order_id=order_id).first()

        if not is_admin_or_curr_owner_or_table(get_jwt_identity(), order.restaurant_id, order.table_id):
            abort(403, message="Current user doesn't have access to view this order item.")

        return order.items


@blp.route("/order/<int:order_id>/order_item/<int:order_item_id>")
class OrderItemsOps(MethodView):
    @jwt_required()
    @blp.response(200, OrderItemSchema)
    def get(self, order_id, order_item_id):
        order = Order.objects(order_id=order_id).first()

        if not is_admin_or_curr_owner_or_table(get_jwt_identity(), order.restaurant_id, order.table_id):
            abort(403, message="Current user doesn't have access to view this order item.")

        order_item = next((item for item in order.items if item.order_item_id == order_item_id), None)

        if order_item is None:
            abort(404, message="Order item not found.")

        return order_item
