from mongoengine import Document, StringField, IntField, EnumField

from models.user_type import UserType


class User(Document):
    # This class will be used for admins, owners, tables
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    user_type = EnumField(UserType, required=True)
    restaurant_id = IntField(required=False)  # will be set only for owners and tables
    table_id = IntField(required=False)  # will be set only for tables

    def __repr__(self):
        return f'<User(username={self.username}, user_type={self.user_type})>'

    def is_admin_or_curr_owner(self, user_data):
        return (self.user_type == UserType.ADMIN or (
                self.user_type == UserType.OWNER and self.restaurant_id == user_data["restaurant_id"]))
