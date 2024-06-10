from . import db
import json

class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    run_type = db.Column(db.String, nullable=True)
    view_by = db.Column(db.String, nullable=True)
    pairs_cases = db.Column(db.String, nullable=True)
    include_columns = db.Column(db.Text, nullable=True)
    stock_filters = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=True)
    file_name = db.Column(db.String, nullable=True)
    styles = db.Column(db.String, nullable=False)

    def set_styles(self, styles):
        self.styles = json.dumps(styles)

    def get_styles(self): 
        return json.loads(self.styles)
    
    def set_include_columns(self, columns):
        self.include_columns = json.dumps(columns)

    def get_include_columns(self):
        return json.loads(self.include_columns)
    
    @property
    def serizalize(self):
        return {
            'id': self.id,
            'run_type': self.run_type,
            'view_by': self.view_by,
            'pairs_cases': self.pairs_cases,
            'include_columns': self.get_include_columns(),            
            'stock_filters': self.stock_filters,
            'status': self.status,
            'file_name': self.file_name,
            'styles': self.get_styles()
        }