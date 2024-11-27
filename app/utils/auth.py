from flask_jwt_extended import create_access_token

def generate_token(user):
    return create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role_id})
