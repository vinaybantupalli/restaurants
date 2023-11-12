import logging

from flask.views import MethodView
from flask_smorest import Blueprint

from schemas import RestaurantSchema, PlainRestaurantSchema

blp = Blueprint("Restaurants", "restaurants", description="Operations on restaurants")
logger = logging.getLogger(__name__)

restaurants = {}


@blp.route("/restaurant/<string:restaurant_id>")
class Restaurant(MethodView):
    # @jwt_required()
    @blp.response(200, PlainRestaurantSchema)
    def get(self, restaurant_id):
        logger.debug("log %s" % (restaurants.get(restaurant_id)))
        return restaurants.get(restaurant_id)


@blp.route("/restaurant")
class RestaurantList(MethodView):
    @blp.response(200, PlainRestaurantSchema(many=True))
    def get(self):
        return restaurants.values()

    @blp.arguments(RestaurantSchema)
    @blp.response(201, PlainRestaurantSchema)
    def post(self, restaurants_data):
        restaurants["1"] = {"id": 1, **restaurants_data}
        return restaurants["1"]
