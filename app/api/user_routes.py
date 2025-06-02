from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User
from app import db
user_routes = Blueprint('users', __name__)


@user_routes.route('/')
@login_required
def users():
    """
    Query for all users and returns them in a list of user dictionaries
    """
    user = current_user.to_dict()

    if user['role'] == 'admin':
        # If the user is an admin, return all users
        users = User.query.all()
        return {'users': [user.to_dict() for user in users]}
    # If the user is not an admin, return only their own user
    # information
    return {'user': user}




@user_routes.route('/<int:id>')
@login_required
def user(id):
    """
    Query for a user by id and returns that user in a dictionary
    """
    user = User.query.get(id)
    return user.to_dict()


@user_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_role(id):
    """
    Update the role of a user by id.
    Only 'owner' or 'admin' can update roles.
    """
    if current_user.role not in {"owner", "admin"}:
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    new_role = data.get('role')
    print("hellloooo", new_role)
    if new_role not in {'admin', 'user', 'employee', }:
        return jsonify({"error": "Invalid role"}), 400

    user.role = new_role
    db.session.commit()
    return jsonify({"message": "User role updated successfully", "user": user.to_dict()}), 200
