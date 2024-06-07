from flask import Blueprint, request

users_bp = Blueprint('users', __name__)


@users_bp.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    print(login_data)
    return login_data
