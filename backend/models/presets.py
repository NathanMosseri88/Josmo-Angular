from . import db
import json

class Preset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    styles = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_preset_user'), nullable=False)

    def set_styles(self, styles):
        self.styles = json.dumps(styles)

    def get_styles(self):
        return json.loads(self.styles)
    
    def __repr__(self):
        return '<Preset %r>' % self.name