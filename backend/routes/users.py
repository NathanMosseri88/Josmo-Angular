from flask import Blueprint, request, jsonify
from ..models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

@users_bp.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    username = login_data.get('username')
    password = login_data.get('password')

    user = User.query.filter_by(username=username).first()  # query DB for user with username from request data from client
    if user and user.check_password(password):  # if a user was found and the password sent by client matches that user's hashed password
        access_token = create_access_token(identity=user.id)  # create an encypted jwt token representing the User's ID
        return jsonify(access_token=access_token), 200  # returns the access token to the client for further authorization
    
    # if user credentials do not match return 401-Unauthorized 
    return jsonify({'error': "Invalid Credentials"}), 401

# creating new users is currently done manually through 'flask shell' CLI tool
# an 'admin' column can be added to the Users table to allow only users with admin as 'true' to access a 'signup' route to create new users
# admin boolean will default to false and can only be assigned to true by us manually creating users through the CLI