from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import User
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
