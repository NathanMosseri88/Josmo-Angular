from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    # initializes DB columns 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # admin column to allow manually assigned admins to create users (and maybe other abilities down the line) -- defaults to false
    admin = db.Column(db.Boolean, default=False, nullable=False)
    # user has many presets -- sets up relationship to presets
    presets = db.relationship('Preset', backref='user', lazy=True)

    def set_password(self, password):  # hash and store password as to not be represented by readable plain text
        self.password = generate_password_hash(password)

    def check_password(self, password):  # checks hashed password for a match and returns boolean
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User %r>' % self.username