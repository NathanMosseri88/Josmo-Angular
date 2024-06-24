from . import db
import json

class Proposal(db.Model):
    # initializes DB columns 
    id = db.Column(db.Integer, primary_key=True)
    run_type = db.Column(db.String(100), nullable=True)
    view_by = db.Column(db.String(100), nullable=True)
    pairs_cases = db.Column(db.String(100), nullable=True)
    include_columns = db.Column(db.JSON, nullable=True)
    stock_filters = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=True)
    file_name = db.Column(db.String(100), nullable=True)
    styles = db.Column(db.JSON, nullable=False)
    
    @property
    def serizalize(self):  # fromat to send requested proposal data to client
        return {
            'id': self.id,
            'run_type': self.run_type,
            'view_by': self.view_by,
            'pairs_cases': self.pairs_cases,
            'include_columns': self.include_columns,            
            'stock_filters': self.stock_filters,
            'status': self.status,
            'file_name': self.file_name,
            'styles': self.styles
        }