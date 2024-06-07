from . import db

class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)