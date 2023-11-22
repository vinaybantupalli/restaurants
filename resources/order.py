import logging
import random
from collections import defaultdict
from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from flask_smorest import abort

from models import Order, OrderItem, Restaurant, User
from resources.utils import is_admin_or_curr_owner_or_table, is_admin_or_curr_owner_by_id, get_table_key
from schemas import PlainOrderSchema, OrderSchema, OrderItemSchema, OrderQueryArgs, PlainOrderItemSchema, BillSchema

blp = Blueprint("Orders", "orders", description="Operations on orders")
logger = logging.getLogger(__name__)


@blp.route("/restaurant/<int:restaurant_id>/order")
class OrderUtils(MethodView):
    @jwt_required()
    @blp.arguments(OrderQueryArgs, location="query")
    @blp.response(200, OrderSchema(many=True))
    def get(self, search_values, restaurant_id):

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), restaurant_id):
            abort(403, message="Current user doesn't have access to get orders on this restaurant.")

        if 'active' in search_values:
            return Order.objects(active=search_values.get('active')).order_by('-updated_at')

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
        order = Order.objects(order_id=order_id).first()

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), order.restaurant_id):
            abort(403, message="Current user doesn't have access to delete orders.")

        order.delete()
        return {"message": "Order Deleted Successfully"}, 200


def get_bill_from_order(order):
    # Create a dictionary to hold the combined quantities of items
    combined_items = defaultdict(lambda: {"quantity": 0, "price": 0, "name": ""})
    # Iterate over all items in the order
    for item in order.items:
        # Combine quantities if item_id for different order_item_id are matching
        combined_items[item.item_id]["quantity"] += item.quantity
        combined_items[item.item_id]["price"] = item.price
        combined_items[item.item_id]["name"] = item.name
    # Generate a list of BillItem
    bill_items = [{"name": v["name"], "price": v["price"], "quantity": v["quantity"]} for v in combined_items.values()]
    # Construct a BillSchema as response of the API
    bill = {"table_id": order.table_id, "order_id": order.order_id, "items": bill_items}
    return bill


@blp.route("/order/<int:order_id>/lock")
class LockBillOps(MethodView):
    @jwt_required()
    @blp.response(200, BillSchema)
    def post(self, order_id):
        order = Order.objects(order_id=order_id).first()

        if not is_admin_or_curr_owner_or_table(get_jwt_identity(), order.restaurant_id, order.table_id):
            abort(403, message="Current user doesn't have access to lock this order.")

        order.update(active=False)

        table = User.objects(username=get_table_key(order.restaurant_id, order.table_id)).first()
        table.update(password="1")

        bill = get_bill_from_order(order)

        return bill, 200


@blp.route("/order/<int:order_id>/unlock")
class UnlockBillOps(MethodView):
    @jwt_required()
    @blp.response(200)
    def post(self, order_id):
        order = Order.objects(order_id=order_id).first()

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), order.restaurant_id):
            abort(403, message="Current user doesn't have access to unlock orders.")

        order.update(active=True)

        table = User.objects(username=get_table_key(order.restaurant_id, order.table_id)).first()
        table.update(set__password=str(random.randint(100000, 999999)))

        return {"message": "Order Unlocked Successfully"}, 200


@blp.route("/order/<int:order_id>/bill")
class BillOps(MethodView):
    @jwt_required()
    @blp.response(200, BillSchema)
    def get(self, order_id):
        order = Order.objects(order_id=order_id).first()

        if not is_admin_or_curr_owner_or_table(get_jwt_identity(), order.restaurant_id, order.table_id):
            abort(403, message="Current user doesn't have access to view bill on this table")

        bill = get_bill_from_order(order)

        return bill, 200


@blp.route("/order/<int:order_id>/order_item")
class OrderItemsUtils(MethodView):
    @jwt_required()
    @blp.arguments(OrderItemSchema(many=True))
    @blp.response(200, OrderSchema)
    def post(self, order_item_data, order_id):
        order = Order.objects(order_id=order_id).first()

        if not is_admin_or_curr_owner_or_table(get_jwt_identity(), order.restaurant_id, order.table_id):
            abort(403, message="Current user doesn't have access to update this order.")

        if not order.active:
            abort(400, message="Order not active. Cannot edit order now.")

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

    @jwt_required()
    @blp.arguments(PlainOrderItemSchema(many=True))
    @blp.response(200, OrderSchema)
    def delete(self, order_item_data, order_id):
        order = Order.objects(order_id=order_id).first()

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), order.restaurant_id):
            abort(403, message="Current user doesn't have access to update this order.")

        for item_data in order_item_data:
            # retrieve the corresponding item from the restaurant document
            order_item_id = item_data['order_item_id']

            order_item = next((item for item in order.items if item.order_item_id == order_item_id), None)
            if order_item is None:
                continue

            if 'quantity' in item_data:
                quantity = item_data.get('quantity')
                if quantity > order_item.quantity:
                    abort(400, message="Quantity invalid for current order item id")
                order_item.quantity = order_item.quantity - quantity
            else:
                order_item.quantity = 0

        order.save()
        return order, 200


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
