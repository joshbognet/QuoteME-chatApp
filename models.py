from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy



db=SQLAlchemy()



    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    
    
    def __repr__(self):
        return f'<student {self.username}>'