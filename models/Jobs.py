import datetime
from app import db

def _get_date():

    return 

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location  = db.Column(db.String(120), nullable=True)
    total = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'), nullable=False)
    def __repr__(self):
        return f'id: {self.id}, term: {self.term}, location: {self.location}, total: {self.total}'
db.create_all()