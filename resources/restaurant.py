import logging

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from flask_smorest import abort

from models import Restaurant, User
from schemas import RestaurantSchema, PlainRestaurantSchema

blp = Blueprint("Restaurants", "restaurants", description="Operations on restaurants")
logger = logging.getLogger(__name__)


@blp.route("/restaurant")
class RestaurantUtils(MethodView):
    @jwt_required()
    @blp.response(200, PlainRestaurantSchema(many=True))
    def get(self):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin():
            abort(403, message="Current user doesn't have access to get restaurants.")

        return Restaurant.objects()

    @jwt_required(fresh=True)
    @blp.arguments(RestaurantSchema)
    @blp.response(201, PlainRestaurantSchema)
    def post(self, restaurant_data):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin():
            abort(403, message="Current user doesn't have access to create restaurants.")

        restaurant = Restaurant(**restaurant_data)
        restaurant.save()
        return restaurant


@blp.route("/restaurant/<int:restaurant_id>")
class RestaurantOps(MethodView):
    @jwt_required()
    @blp.response(200, PlainRestaurantSchema)
    def get(self, restaurant_id):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin_or_curr_owner(restaurant_id):
            abort(403, message="Current user doesn't have access to do get on this restaurant.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        logger.debug(f"log {restaurant.__repr__()}")
        return restaurant

    @blp.response(200)
    @jwt_required()
    def delete(self, restaurant_id):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin():
            abort(403, message="Current user doesn't have access to delete restaurants.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        restaurant.delete()
        return {"message": "Restaurant Deleted Successfully"}, 200
