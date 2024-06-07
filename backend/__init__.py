from flask import Flask
from flask_cors import CORS
from .models import db
from .routes import presets_bp, users_bp, proposals_bp

def create_app():
    app = Flask(__name__)

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)

    # create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(presets_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(proposals_bp, url_prefix='/api')

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

    return app
