from flask import Flask
from flask_cors import CORS
from .models import db, User, Preset, Proposal
from .routes import presets_bp, users_bp, proposals_bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Simple123@localhost/Josmo_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'f5bdd9ca0349ad5fc9601f228d97777d8104c38f0025ba6de590e21b0c6e0166'

    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(presets_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(proposals_bp, url_prefix='/api')

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Preset': Preset, 'Proposal': Proposal}

    return app
