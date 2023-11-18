import logging
from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from flask_smorest import abort

from models import Order, OrderItem
from models.user import User
from schemas import OrderItemSchema, PlainOrderSchema, OrderSchema

blp = Blueprint("Orders", "orders", description="Operations on orders")
logger = logging.getLogger(__name__)


@blp.route("/order")
class OrderUtils(MethodView):
    @jwt_required()
    @blp.response(200, OrderSchema(many=True))
    def get(self):
        restaurant_id = get_jwt_identity().split(":")[0]
        table_id = get_jwt_identity().split(":")[1]

        return Order.objects()

    @jwt_required()
    @blp.arguments(PlainOrderSchema)
    @blp.response(201, PlainOrderSchema)
    def post(self, order_data):
        curr_user = User.objects(username=get_jwt_identity()).first()

        restaurant_id = order_data.get('restaurant_id')
        table_id = order_data.get('table_id')

        if not curr_user.is_admin_or_curr_owner_by_id(restaurant_id): 
            abort(403, message="Current user doesn't have access to create orders on this table.")

        order = Order(restaurant_id=restaurant_id, table_id=table_id, active=True)
        order.save()
        return order, 201
    


@blp.route("/order/<int:order_id>")
class RestaurantOps(MethodView):
    @jwt_required()
    @blp.response(200, OrderSchema)
    def get(self, order_id):
        order = Order.objects(order_id=order_id).first()
        return order

    @blp.response(200)
    @jwt_required()
    def delete(self, order_id):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin_or_curr_owner_by_id():
            abort(403, message="Current user doesn't have access to delete orders.")

        order = Order.objects(id=order_id).first()
        order.delete()
        return {"message": "Order Deleted Successfully"}, 200

    @blp.arguments(OrderSchema)
    @blp.response(200, OrderSchema)
    @jwt_required()
    def put(self, updated_data, restaurant_id):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin():
            abort(403, message="Current user doesn't have access to update this restaurant.")
