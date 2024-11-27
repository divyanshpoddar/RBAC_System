from flask import Blueprint, request, jsonify
from app.models import User, Role, db
from app.utils.auth import generate_token
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], role_id=data.get('role_id', 2))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = generate_token(user)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/roles', methods=['GET'])
@jwt_required()
def get_roles():
    current_user = get_jwt_identity()
    
    print(current_user) 

    if isinstance(current_user, dict) and current_user.get('role') == 1:
        roles = Role.query.all() 
        role_list = [{"id": role.id, "name": role.name, "permissions": role.permissions} for role in roles]
        return jsonify({"roles": role_list}), 200
    else:
        return jsonify({"message": "Permission denied"}), 403