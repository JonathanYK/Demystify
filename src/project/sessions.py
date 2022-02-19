import random
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# sessions table:
class Sessions(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String)
    
    def __init__(self, id):
        self.id = id
        

    def __repr__(self):
        return "Session ID generated: " + str(self.id)


    def gen_session_id():
        # should return random session id between 100000000 and 999999999 with exact 9 digits:
        return random.randrange(100000000, 999999999, 9)

        