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
@users_bp.route('/signup', methods=['POST'])
@jwt_required()
def signup(): 
    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(id=current_user_id).first()
    print(current_user, current_user.admin)
    if current_user and current_user.admin:
        signup_data = request.get_json()
        username = signup_data.get('username')
        password = signup_data.get('password')
        email = signup_data.get('email')

        if not username or not password or not email:
            return jsonify({'error': 'All credentials must be filled in'}), 400
        
        new_user = User(
            username=username,
            email=email
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'username': new_user.username, 'email': new_user.email}), 201

    return jsonify({'error': 'Only authorized users can create users'}), 401


