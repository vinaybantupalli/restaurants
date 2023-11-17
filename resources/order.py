import logging
from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from flask_smorest import abort

from models import Order, OrderItem
from schemas import OrderItemSchema, PlainOrderSchema, OrderSchema

blp = Blueprint("Orders", "orders", description="Operations on orders")
logger = logging.getLogger(__name__)
