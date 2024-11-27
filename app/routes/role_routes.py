from flask import Blueprint, jsonify, request
from app.models import Role, db
from app.utils.decorators import role_required
from flask_jwt_extended import jwt_required

role_bp = Blueprint('role', __name__)

@role_bp.route('/roles', methods=['GET'])
@jwt_required()
@role_required(['Admin'])
def get_roles():
    roles = Role.query.all()
    return jsonify([{"id": role.id, "name": role.name, "permissions": role.permissions} for role in roles])

@role_bp.route('/roles', methods=['POST'])
@jwt_required()
@role_required(['Admin'])
def create_role():
    data = request.json
    role = Role(name=data['name'], permissions=data['permissions'])
    db.session.add(role)
    db.session.commit()
    return jsonify({"message": "Role created successfully"}), 201