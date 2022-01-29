# TODO: at the end of this project, handle the following warning:
# e:\Coding\Demystify\src\env\lib\site-packages\flask_sqlalchemy\__init__.py:872: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.


from flask import Flask, request
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

def set_msg(session_id, msg):
    
    try:
        ret_val = ""
        session_update = db.session.query(Sessions).get(session_id)
        if session_update.msg is not None:
            ret_val = "overriding message for session id: " + session_id + ", previous message was: " + session_update.msg + "\n"
        session_update.msg = msg
        db.session.commit()
        return ret_val
    except:
        return handle_server_500("There was an issue adding message to a session id!")


def get_msg(session_id):
    try:

        ret_msg = db.session.query(Sessions).get(session_id).msg
        if ret_msg is None:
            return "There is no message for session id " + session_id
        else :
            return "The message for session id " + str(session_id) + " is: " + ret_msg
    
    except:
         return handle_server_500("There was an issue retriving the message for this session id!")

# sessions table:
class Sessions(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String)
    
    def __init__(self, id):
        self.id = id
        

    def __repr__(self):
        return "Session ID generated: " + str(self.id)


def validate_json_keys(json_data):

    keys_dict = json_data.keys()
    must_have_keys = ["message", "additional", "level", "timestamp", "fileName", "lineNumber"]

    # THIS IS REPLACED WITH THE BELOW LAMBDA!!
    # for key in must_have_keys:
    #     if key not in keys_dict:
    #         return False

    # return True

    return all(map(lambda provided_json_keys: True if provided_json_keys in keys_dict else False, must_have_keys))

def log_level_validation(cur_log_level):
    curr_log_lvls = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
    return True if cur_log_level in curr_log_lvls else False
 
# dynamic methods, each for the appropriate level:
def print_CRITICAL(logger, logging_data):
    for data in logging_data: logger.critical(data)

def print_ERROR(logger, logging_data):
    for data in logging_data: logger.error(data)

def print_WARNING(logger, logging_data):
    for data in logging_data: logger.warning(data)

def print_INFO(logger, logging_data):
    for data in logging_data: logger.info(data)

def print_DEBUG(logger, logging_data):
    for data in logging_data: logger.debug(data)

def print_NOTSET(logger, logging_data):
    for data in logging_data: logger.notset(data)


# logging the data to a .log file:
def log_data(logger, session_id, json_data):

    # list for relevant logging params:
    logging_data = []

    # parsering the json params:
    str_log_level = json_data["level"]
    # validate str_log_level:
    if log_level_validation(str_log_level) is False:
        return handle_bad_input_501("The provided log level isn't valid!")

    logging_data.append(str_log_level)
    logging_data.append(json_data["timestamp"])
    logging_data.append(json_data["fileName"])
    logging_data.append(json_data["lineNumber"])

    # create log level printings according to provided log level, then set the same log level:
    dynamic_log_printer = globals()["print_%s" % str_log_level]
    logger.setLevel(logging.getLevelName(str_log_level))

    # config session formatter both for file_handler and stream_handler:
    session_formatter = logging.Formatter("%(asctime)s::%(levelname)s::%(name)s::%(message)s")
    
    # file_handler configurations:
    file_handler = logging.FileHandler(filename=session_id+".log", mode="a")
    file_handler.set_name(session_id)
    file_handler.setFormatter(session_formatter)

    # stream_handler configurations:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(session_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # dynamic printing to the relevant log:
    dynamic_log_printer(logger, logging_data)

    # removing both file and stream handlers, in order to avoid duplications:
    logger.removeHandler(file_handler)
    logger.removeHandler(stream_handler)

## error handlers ##

@app.errorhandler(404)
def handle_bad_request_404():
    return "Bad request! Resource not found.", 404

@app.errorhandler(500)
def handle_server_500(err_msg):
    return err_msg, 500

@app.errorhandler(501)
def handle_bad_input_501(err_msg):
    return err_msg, 501

## error handlers ##

@app.route("/")
def home():
    return "Main demystify page"


@app.route("/session_id", methods=["POST", "PUT", "DELETE"])
def handle_session_id_forbidden_requests():
    return handle_bad_input_501("This method is forbidden for session_id url!")

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
        return repr(new_session), 201
    except:
            return handle_server_500("There was an issue adding new session id to the db!")

@app.route("/session_msg", methods=["POST", "PUT", "DELETE"])
def handle_session_msg_forbidden_requests():
    return handle_bad_input_501("This method is forbidden for session msg url!")

@app.route("/session_msg", methods=["GET"])
def get_session_msg():
    
    curr_session_id = request.args.get("session_id")
    if session_id_validation(curr_session_id) is False:
        return handle_bad_input_501("The provided session id isn't valid!")

    return get_msg(curr_session_id)


@app.route("/log", methods=["GET", "PUT", "DELETE"])
def handle_session_log_forbidden_requests():
    return handle_bad_input_501("This method is forbidden for log url!")


@app.route("/log", methods=["POST"])
def log():

    ret_val = ""

    # retriving the session id from the url:
    curr_session_id = request.args.get("session_id")

    # validate the session id:
    if session_id_validation(curr_session_id) is False:
        return handle_bad_input_501("The provided session id isn't valid!")

    # validate there arn't missing required keys in json file:
    if validate_json_keys(request.json) is False:
        return handle_bad_input_501("There is a missing key/s in the provided json!")

    logger = logging.getLogger("__name__")

    curr_msg = request.json["message"]
    ret_val+=set_msg(curr_session_id, curr_msg)

    # log the date to a dedicated file (session_id.log):
    log_data(logger, curr_session_id, request.json)

    ret_val+="logging done!"
    return ret_val


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)