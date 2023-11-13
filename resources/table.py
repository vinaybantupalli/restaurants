import logging

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from flask_smorest import abort

from models import User
from models.user_type import UserType
from resources.utils import get_table_key
from schemas import TableSchema, PlainTableSchema

blp = Blueprint("Tables", "tables", description="Operations on tables")
logger = logging.getLogger(__name__)


@blp.route("/restaurant/<int:restaurant_id>/table")
class TableUtils(MethodView):
    @blp.response(200, TableSchema(many=True))
    @jwt_required()
    def get(self, restaurant_id):
        curr_user = User.objects(username=get_jwt_identity()).first()

        # user either needs to be admin or owner of the restaurant
        if not curr_user.is_admin_or_curr_owner(restaurant_id):
            abort(403, message="Current user doesn't have access to view tables on this restaurant.")

        return User.objects(restaurant_id=restaurant_id)

    @jwt_required(fresh=True)
    @blp.arguments(PlainTableSchema)
    def post(self, table_data, restaurant_id):
        curr_user = User.objects(username=get_jwt_identity()).first()

        # user either needs to be admin or owner of the restaurant
        if not curr_user.is_admin_or_curr_owner(restaurant_id):
            abort(403, message="Current user doesn't have access to either create tables at all or on this restaurant.")

        table_id = table_data["table_id"]
        username = get_table_key(restaurant_id, table_id)

        if User.objects(username=username).first():
            abort(409, message="A table with that id already exists.")

        user = User(username=username, password="1", user_type=UserType.TABLE, restaurant_id=restaurant_id,
                    table_id=table_id)
        user.save()

        return {"message": "Table created successfully."}, 201


@blp.route("/restaurant/<int:restaurant_id>/table/<int:table_id>")
class TableOps(MethodView):
    @blp.response(200, TableSchema)
    @jwt_required()
    def get(self, restaurant_id, table_id):
        curr_user = User.objects(username=get_jwt_identity()).first()

        # user either needs to be admin or owner of the restaurant
        if not curr_user.is_admin_or_curr_owner(restaurant_id):
            abort(403, message="Current user doesn't have access to view this table.")

        username = get_table_key(restaurant_id, table_id)
        return User.objects(username=username).first()

    @blp.response(200)
    @jwt_required()
    def delete(self, restaurant_id, table_id):
        curr_user = User.objects(username=get_jwt_identity()).first()

        # user either needs to be admin or owner of the restaurant
        if not curr_user.is_admin_or_curr_owner(restaurant_id):
            abort(403, message="Current user doesn't have access to delete this table.")

        username = get_table_key(restaurant_id, table_id)
        table = User.objects(username=username).first()
        table.delete()
        return {"message": "Table Deleted Successfully"}, 200
