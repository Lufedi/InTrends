
from app import db

class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term =  db.Column(db.String(120), unique=True, nullable=False)
    jobs =  db.relationship('Job', backref='term', lazy=True)

    def __repr__(self):
        return f'id: {self.id}, term: {self.term}'
db.create_all()