import logging
import random

from flask.views import MethodView
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required, )
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from blocklist import BLOCKLIST
from models import User, UserType
from resources.utils import get_table_key
from schemas import UserSchema, OwnerSchema, TableOtpSchema

blp = Blueprint("Users", "users", description="Operations on users")
logger = logging.getLogger(__name__)


@blp.route("/admin")
class AdminOps(MethodView):
    # This endpoint is for internal use only
    @blp.arguments(UserSchema, description="Create Admin User")
    @jwt_required(fresh=True)
    def post(self, user_data):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin():
            abort(403, message="Current user doesn't have access to create admin users.")

        if User.objects(username=user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = User(username=user_data["username"], password=pbkdf2_sha256.hash(user_data["password"]),
                    user_type=UserType.ADMIN)
        user.save()

        return {"message": "User created successfully."}, 201


@blp.route("/owner")
class OwnerOps(MethodView):
    @blp.arguments(OwnerSchema)
    @jwt_required(fresh=True)
    def post(self, user_data):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin():
            abort(403, message="Current user doesn't have access to create owners.")

        if User.objects(username=user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = User(username=user_data["username"], password=pbkdf2_sha256.hash(user_data["password"]),
                    user_type=UserType.OWNER, restaurant_id=user_data["restaurant_id"])
        user.save()

        return {"message": "User created successfully."}, 201


@blp.route("/owner/<string:username>")
class OwnerUtils(MethodView):
    # used for testing for now
    @jwt_required()
    @blp.response(200, OwnerSchema)
    def get(self, username):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin_or_curr_user(username=username):
            abort(403, message="Current user doesn't have access to view owner.")

        user = User.objects(username=username).first()

        if user.user_type != UserType.OWNER:
            abort(400, message="Requested user is not owner.")

        return user

    @jwt_required(fresh=True)
    @blp.response(200, None)
    def delete(self, username):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin():
            abort(403, message="Current user doesn't have access to delete owners.")

        user = User.objects(username=username).first()
        user.delete()
        return {"message": "User Deleted Successfully"}, 200


@blp.route("/otp/restaurant/<int:restaurant_id>/table/<int:table_id>")
class TableOtpUtils(MethodView):
    @blp.response(200)
    def post(self, restaurant_id, table_id):
        table = User.objects(username=get_table_key(restaurant_id, table_id)).first()

        if 99999 < int(table.password) < 1000000:
            abort(400, message="Session for table already exists.")

        table.update(set__password=str(random.randint(100000, 999999)))
        return {"message": "Otp Generated. Please contact Restaurant Staff"}, 200

    @jwt_required()
    @blp.response(200, TableOtpSchema)
    def get(self, restaurant_id, table_id):
        curr_user = User.objects(username=get_jwt_identity()).first()

        if not curr_user.is_admin_or_curr_owner(restaurant_id):
            abort(403, message="Current user doesn't have access to view otp.")

        table = User.objects(restaurant_id=restaurant_id, table_id=table_id).first()

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
        return {"message": "Successfully logged out."}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        curr_user = get_jwt_identity()
        new_token = create_access_token(identity=curr_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200
