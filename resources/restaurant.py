import logging
from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from flask_smorest import abort

from models import Restaurant
from resources.utils import is_admin, is_admin_or_curr_owner_by_id
from schemas import RestaurantSchema, PlainRestaurantSchema, RestaurantUpdateSchema, MenuLayoutSchema

blp = Blueprint("Restaurants", "restaurants", description="Operations on restaurants")
logger = logging.getLogger(__name__)


@blp.route("/restaurant")
class RestaurantUtils(MethodView):
    @jwt_required()
    @blp.response(200, RestaurantSchema(many=True))
    def get(self):

        if not is_admin(get_jwt_identity()):
            abort(403, message="Current user doesn't have access to get restaurants.")

        return Restaurant.objects()

    @jwt_required(fresh=True)
    @blp.arguments(PlainRestaurantSchema)
    @blp.response(201, RestaurantSchema)
    def post(self, restaurant_data):

        if not is_admin(get_jwt_identity()):
            abort(403, message="Current user doesn't have access to create restaurants.")

        restaurant = Restaurant(**restaurant_data)
        restaurant.updated_at = datetime.utcnow()
        restaurant.save()
        return restaurant


@blp.route("/restaurant/<int:restaurant_id>")
class RestaurantOps(MethodView):
    @jwt_required()
    @blp.response(200, RestaurantSchema)
    def get(self, restaurant_id):

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), restaurant_id):
            abort(403, message="Current user doesn't have access to do get on this restaurant.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        logger.debug(f"log {restaurant.__repr__()}")
        return restaurant

    @blp.response(200)
    @jwt_required(fresh=True)
    def delete(self, restaurant_id):

        if not is_admin(get_jwt_identity()):
            abort(403, message="Current user doesn't have access to delete restaurants.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        restaurant.delete()
        return {"message": "Restaurant Deleted Successfully"}, 200

    @blp.arguments(RestaurantUpdateSchema)
    @blp.response(200, RestaurantSchema)
    @jwt_required(fresh=True)
    def put(self, updated_data, restaurant_id):

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), restaurant_id):
            abort(403, message="Current user doesn't have access to update this restaurant.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        restaurant.updated_at = datetime.utcnow()
        restaurant.update(**updated_data)
        restaurant.reload()
        return restaurant, 200


@blp.route("/restaurant/<int:restaurant_id>/menu_layout")
class MenuLayoutUtils(MethodView):
    @jwt_required(fresh=True)
    @blp.arguments(MenuLayoutSchema)
    @blp.response(201, RestaurantSchema)
    def post(self, menu_layout, restaurant_id):

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), restaurant_id):
            abort(403, message="Current user doesn't have access to update this restaurant.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        restaurant.updated_at = datetime.utcnow()
        restaurant.update(menu_layout=menu_layout)
        restaurant.reload()
        return restaurant, 200
