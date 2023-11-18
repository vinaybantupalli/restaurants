import logging
from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from flask_smorest import abort

from models import Restaurant, Item
from resources.utils import is_admin, is_admin_or_curr_owner_by_id
from schemas import PlainItemSchema, RestaurantSchema, PlainRestaurantSchema, RestaurantUpdateSchema

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

        if not is_admin(get_jwt_identity()):
            abort(403, message="Current user doesn't have access to update this restaurant.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        restaurant.updated_at = datetime.utcnow()
        restaurant.update(**updated_data)
        restaurant.reload()
        return restaurant, 200


@blp.route("/restaurant/<int:restaurant_id>/item")
class ItemUtils(MethodView):
    @jwt_required()
    @blp.response(200, PlainItemSchema(many=True))
    def get(self, restaurant_id):

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), restaurant_id):
            abort(403, message="Current user doesn't have access to do get on this restaurant.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        return restaurant.items

    @jwt_required(fresh=True)
    @blp.arguments(PlainItemSchema)
    @blp.response(201, PlainItemSchema)
    def post(self, item_data, restaurant_id):

        if not is_admin(get_jwt_identity()):
            abort(403, message="Current user doesn't have access to create items on this restaurant.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        item = Item(**item_data)
        restaurant.items.append(item)
        restaurant.updated_at = datetime.utcnow()
        restaurant.save()
        return PlainItemSchema().dump(item), 201


@blp.route("/restaurant/<int:restaurant_id>/item/<int:item_id>")
class ItemOps(MethodView):
    @jwt_required()
    @blp.response(200, PlainItemSchema)
    def get(self, restaurant_id, item_id):

        if not is_admin_or_curr_owner_by_id(get_jwt_identity(), restaurant_id):
            abort(403, message="Current user doesn't have access to do get on this restaurant.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        item = next((item for item in restaurant.items if item.item_id == item_id), None)

        if item is None:
            abort(404, message="Item not found in the restaurant.")

        return PlainItemSchema().dump(item), 200

    @blp.response(200)
    @jwt_required(fresh=True)
    def delete(self, restaurant_id, item_id):

        if not is_admin(get_jwt_identity()):
            abort(403, message="Current user doesn't have access to delete items on restaurant.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        item = next((item for item in restaurant.items if item.item_id == item_id), None)

        if item is None:
            abort(404, message="Item not found in the restaurant.")

        restaurant.items.remove(item)
        restaurant.save()
        return {"message": f"Item {item_id} deleted successfully"}, 200

    @blp.arguments(PlainItemSchema)
    @blp.response(200, PlainItemSchema)
    @jwt_required(fresh=True)
    def put(self, updated_data, restaurant_id, item_id):

        if not is_admin(get_jwt_identity()):
            abort(403, message="Current user doesn't have access to update items on this restaurant.")

        restaurant = Restaurant.objects(id=restaurant_id).first()
        item = next((item for item in restaurant.items if item.item_id == item_id), None)

        if item is None:
            abort(404, message="Item not found in the restaurant.")

        for key, value in updated_data.items():
            setattr(item, key, value)

        restaurant.save()
        return PlainItemSchema().dump(item), 200
