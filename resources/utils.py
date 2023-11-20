from models.user_type import UserType


def get_table_key(restaurant_id, table_id):
    return str(restaurant_id) + "," + str(table_id)


def get_owner_key(restaurant_id, username):
    return str(restaurant_id) + "," + username


def get_token_restaurant_id(token_user_key):
    return int(token_user_key.split(",")[0])


def get_token_user_id(token_user_key):
    return token_user_key.split(",")[1]


def get_token_user_type(jwt_token):
    return int(jwt_token.split(":")[0])


def get_token_user_key(jwt_token):
    return jwt_token.split(":")[1]


def is_admin(jwt_token):
    return get_token_user_type(jwt_token) is UserType.ADMIN.value


def is_admin_or_curr_owner_by_id(jwt_token, restaurant_id):
    if is_admin(jwt_token):
        return True
    token_user_type = get_token_user_type(jwt_token)
    token_user_key = get_token_user_key(jwt_token)
    token_restaurant_id = get_token_restaurant_id(token_user_key)
    return token_user_type == UserType.OWNER.value and restaurant_id == token_restaurant_id


def is_admin_or_curr_owner_by_name(jwt_token, username):
    if is_admin(jwt_token):
        return True
    token_user_type = get_token_user_type(jwt_token)
    token_user_key = get_token_user_key(jwt_token)
    token_user_id = get_token_user_id(token_user_key)
    return token_user_type == UserType.OWNER.value and token_user_id == username


def is_admin_or_curr_owner_or_table(jwt_token, restaurant_id, table_id):
    if is_admin(jwt_token):
        return True
    token_user_type = get_token_user_type(jwt_token)
    token_user_key = get_token_user_key(jwt_token)
    token_restaurant_id = get_token_restaurant_id(token_user_key)
    token_user_id = get_token_user_id(token_user_key)
    return ((token_user_type == UserType.TABLE.value and token_restaurant_id == restaurant_id
             and int(token_user_id) == table_id)
            or (token_user_type == UserType.OWNER.value and restaurant_id == token_restaurant_id))
