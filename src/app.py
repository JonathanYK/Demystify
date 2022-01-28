import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
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
            return False

    return True
    


def print_CRITICAL(logger, logging_data):
    for data in logging_data:
        logger.critical(data)

def print_ERROR(logger, logging_data):
    for data in logging_data:
        logger.error(data)

def print_WARNING(logger, logging_data):
    for data in logging_data:
        logger.warning(data)

def print_INFO(logger, logging_data):
    for data in logging_data:
        logger.info(data)

def print_DEBUG(logger, logging_data):
    for data in logging_data:
        logger.debug(data)

def print_NOTSET(logger, logging_data):
    for data in logging_data:
        logger.notset(data)


# logging the data to a .log file:
def log_data(logger, session_id, json_data):

    logging_data = []

    # parsering the json params:

    str_log_level = json_data["level"]
    logging_data.append(str_log_level)
    logging_data.append(json_data["timestamp"])
    logging_data.append(json_data["fileName"])
    logging_data.append(json_data["lineNumber"])

    dynamic_log_printer = globals()["print_%s" % str_log_level]
    logger.setLevel(logging.getLevelName(str_log_level))
    session_formatter = logging.Formatter("%(asctime)s::%(levelname)s::%(name)s::%(message)s")
    
    file_handler = logging.FileHandler(filename=session_id+".log", mode="a")
    file_handler.set_name(session_id)
    file_handler.setFormatter(session_formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(session_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    dynamic_log_printer(logger, logging_data)

    logger.removeHandler(file_handler)
    logger.removeHandler(stream_handler)


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


@app.route("/log", methods=["POST"])
def log():
    logger = logging.getLogger("__name__")
    # retriving the session id from the url:
    curr_session_id = request.args.get("session_id")

    # validate the session id:
    if session_id_validation(curr_session_id) is False:
        return "#400: The provided session id isn't valid!"
    
    # validate there arn't missing required keys in json file:
    if validate_json_keys(request.json) is False:
        return "#400: There is a missing key/s in the provided json!"

    # log the date to a dedicated file (session_id.log):
    log_data(logger, curr_session_id, request.json)

    return "#200: logging done!"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)