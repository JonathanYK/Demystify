# sessions table:
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sessions(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String)
    
    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return "Session ID generated: " + str(self.id)