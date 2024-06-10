from flask import Blueprint, request, jsonify
from ..models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

@users_bp.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    username = login_data.get('username')
    password = login_data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    
    return jsonify({'error': "Invalid Credentials"}), 401

