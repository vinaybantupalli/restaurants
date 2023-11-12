import logging
import random

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required, )
from passlib.hash import pbkdf2_sha256

from models import User
from models.user_type import UserType
from schemas import UserSchema, OwnerSchema, TableSchema, TableOtpSchema
from blocklist import BLOCKLIST

blp = Blueprint("Users", "users", description="Operations on users")
logger = logging.getLogger(__name__)


def is_admin_or_restaurant_owner(user, user_data):
    return (user.user_type == UserType.ADMIN or (
            user.user_type == UserType.OWNER and user.restaurant_id == user_data["restaurant_id"]))


def get_table_key(restaurant_id, table_id):
    return str(restaurant_id) + ":" + str(table_id)


@blp.route("/admin")
class CreateAdmin(MethodView):
    # This endpoint is for internal use only
    @blp.arguments(UserSchema)
    @jwt_required(fresh=True)
    def post(self, user_data):
        current_user = User.objects(username=get_jwt_identity()).first()

        if current_user.user_type != UserType.ADMIN:
            abort(403, message="Current user doesn't have access to create admin users")

        if User.objects(username=user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = User(username=user_data["username"], password=pbkdf2_sha256.hash(user_data["password"]),
                    user_type=UserType.ADMIN)
        user.save()

        return {"message": "User created successfully."}, 201


@blp.route("/owner")
class CreateOwner(MethodView):
    @blp.arguments(OwnerSchema)
    @jwt_required(fresh=True)
    def post(self, user_data):
        current_user = User.objects(username=get_jwt_identity()).first()

        if current_user.user_type != UserType.ADMIN:
            abort(403, message="Current user doesn't have access to create owners")

        if User.objects(username=user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = User(username=user_data["username"], password=pbkdf2_sha256.hash(user_data["password"]),
                    user_type=UserType.OWNER, restaurant_id=user_data["restaurant_id"])
        user.save()

        return {"message": "User created successfully."}, 201


@blp.route("/table")
class CreateTable(MethodView):
    @blp.arguments(TableSchema)
    @jwt_required(fresh=True)
    def post(self, user_data):
        curr_user = User.objects(username=get_jwt_identity()).first()

        # user either needs to be admin or owner of the restaurant
        if not is_admin_or_restaurant_owner(curr_user, user_data):
            abort(403, message="Current user doesn't have access to either create tables at all or on this restaurant.")

        restaurant_id = user_data["restaurant_id"]
        table_id = user_data["table_id"]
        username = get_table_key(restaurant_id, table_id)

        if User.objects(username=username).first():
            abort(409, message="A table with that id already exists.")

        user = User(username=username, password="1", user_type=UserType.TABLE, restaurant_id=restaurant_id,
                    table_id=table_id)
        user.save()

        return {"message": "Table created successfully."}, 201


@blp.route("/otp/restaurant/<int:restaurant_id>/table/<int:table_id>")
class TableOtp(MethodView):
    def post(self, restaurant_id, table_id):
        table = User.objects(username=get_table_key(restaurant_id, table_id)).first()

        if 99999 < int(table.password) < 1000000:
            abort(400, message="Session for table already exists.")

        table.update(set__password=str(random.randint(100000, 999999)))
        return {"message": "Otp Generated. Contact Restaurant Staff"}, 200

    @jwt_required()
    @blp.response(200, TableOtpSchema)
    def get(self, restaurant_id, table_id):
        curr_user = User.objects(username=get_jwt_identity()).first()
        table = User.objects(restaurant_id=restaurant_id, table_id=table_id).first()

        if not is_admin_or_restaurant_owner(curr_user, {"restaurant_id": restaurant_id}):
            abort(403, message="Current user doesn't have access to view otp.")

        return {"otp": int(table.password)}


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = User.objects(username=user_data["username"]).first()

        if user and ((user.user_type == UserType.TABLE and user_data["password"] == user.password) or (
                pbkdf2_sha256.verify(user_data["password"], user.password))):
            access_token = create_access_token(identity=user.username, fresh=True)
            refresh_token = create_refresh_token(user.username)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@blp.route("/user/<string:username>")
class UserAPI(MethodView):
    # used for testing for now
    @blp.response(200, UserSchema)
    def get(self, username):
        user = User.objects(username=username).first()
        return user

    @blp.response(200, None)
    def delete(self, username):
        user = User.objects(username=username).first()
        user.delete()
        return {"message": "User Deleted Successfully"}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200
