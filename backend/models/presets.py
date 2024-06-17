from . import db
import json

class Preset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    styles = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_preset_user'), nullable=False)
    
    def __repr__(self):
        return '<Preset %r>' % self.name