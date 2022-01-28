from distutils.debug import DEBUG
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false, func, true
import logging

app = Flask(__name__)
db_name = 'sessions.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
db = SQLAlchemy(app)

def get_new_session_id():
    # get the max session id (or None if there is no db): 
    max_session_id = db.session.query(func.max(Sessions.id)).scalar()

    # increase session id if it isnt none:
    if max_session_id is not None:
        max_session_id+=1
    else:
        # if max is none - set id to 1000 (default), then return it:
        max_session_id = 1000

    # return new session id number:
    return max_session_id

def session_id_validation(curr_session_id):
    return db.session.query(db.exists().where(Sessions.id == curr_session_id)).scalar()

# sessions table:
class Sessions(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "#201: Session ID generated: " + str(self.id)


def validate_json_keys(json_data):

    keys_dict = json_data.keys()
    must_have_keys = ["message", "additional", "level", "timestamp", "fileName", "lineNumber"]
    for key in must_have_keys:
        if key not in keys_dict:
            return false

    return true
    
    


# logging the data to a .log file:
def log_data(session_id, json_data):

    # parsering the json params:
    str_log_level = json_data["level"]
    time_stamp = json_data["timestamp"]
    file_name = json_data["fileName"]
    line_number = json_data["lineNumber"]

    # logging configuration and printings:
    logging.basicConfig(filename=session_id+".log", filemode="a", level=logging.DEBUG)

    logging.debug(str_log_level)
    logging.debug(time_stamp)
    logging.debug(file_name)
    logging.debug(line_number)


@app.route("/")
def home():
    return "Main demystify page"


@app.route("/session_id", methods=["GET"])

def session_id_generator():
    
    # configure db and get a session id:
    new_session_id = get_new_session_id()

    # create new session with the generated session id:
    new_session = Sessions(new_session_id)
    
    # save the session in the db:
    try:
        db.session.add(new_session)
        db.session.commit()
        return repr(new_session)
    except:
            return "#400: There was an issue adding new session id to the db!"


# TODO: add validations to provided JSON params! 
# TODO: return the relevant http code! 
@app.route("/log", methods=["POST"])
def log():
    # retriving the session id from the url:
    curr_session_id = request.args.get("session_id")

    if session_id_validation(curr_session_id) is None:
        return "#400: The provided session id isn't valid!"
    
    if validate_json_keys(request.json) is false:
        return "#400: There is a missing key/s in the provided json!"

    log_data(curr_session_id, request.json)

    return "#200: logging done!"



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    