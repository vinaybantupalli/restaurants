import logging

from flask.views import MethodView
from flask_smorest import Blueprint

from models import Restaurant
from schemas import RestaurantSchema, PlainRestaurantSchema

blp = Blueprint("Restaurants", "restaurants", description="Operations on restaurants")
logger = logging.getLogger(__name__)


@blp.route("/restaurant/<string:restaurant_id>")
class RestaurantAPI(MethodView):
    # @jwt_required()
    @blp.response(200, PlainRestaurantSchema)
    def get(self, restaurant_id):
        restaurant = Restaurant.objects(id=restaurant_id).first()
        logger.debug(f"log {restaurant.__repr__()}")
        return restaurant


@blp.route("/restaurant")
class RestaurantList(MethodView):
    @blp.response(200, PlainRestaurantSchema(many=True))
    def get(self):
        return Restaurant.objects()

    @blp.arguments(RestaurantSchema)
    @blp.response(201, PlainRestaurantSchema)
    def post(self, restaurant_data):
        restaurant = Restaurant(**restaurant_data)
        restaurant.save()
        return restaurant
