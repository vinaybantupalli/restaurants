import logging

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from mongoengine import connect

from blocklist import BLOCKLIST
from resources import order_blueprint, restaurant_blueprint, table_blueprint, user_blueprint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    app.config["API_TITLE"] = "Restaurants REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["PROPAGATE_EXCEPTIONS"] = True

    connect(host='mongodb://127.0.0.1:27017/restaurants')  # to run app via app.py
    # connect(host='mongodb://mongo_local/restaurants')    # to run app via docker method

    api = Api(app)
    logging.basicConfig(level=logging.DEBUG)

    app.config["JWT_SECRET_KEY"] = "vinay"
    # TODO: use repeatable key from config
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401,

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401,

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"description": "Request does not contain an access token.", "error": "authorization_required", }),
            401,)

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token is not fresh.", "error": "fresh_token_required", }), 401,

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401,

    api.register_blueprint(order_blueprint)
    api.register_blueprint(restaurant_blueprint)
    api.register_blueprint(table_blueprint)
    api.register_blueprint(user_blueprint)

    return app


if __name__ == "__main__":
    create_app().run()
