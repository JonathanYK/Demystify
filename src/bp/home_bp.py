from flask import Blueprint
from .err_bp import handle_server_500
from project.sessions import db, Sessions

# validates that the provided json file includes mandatory fields: 
def validate_json_keys(json_data):
    keys_dict = json_data.keys()
    must_have_keys = ["message", "additional", "level", "timestamp", "fileName", "lineNumber"]

    return all(map(lambda provided_json_keys: True if provided_json_keys in keys_dict else False, must_have_keys))

# sets the provided msg in the db, handles overriding data:
def set_msg(session_id, msg):
    
    try:
        ret_val = ""
        session_update = db.session.query(Sessions).get(session_id)
        if session_update.msg :
            ret_val = "Overriding message for session id: " + session_id + ", previous message was: " + session_update.msg + "\n"
        session_update.msg = msg
        db.session.commit()
        return ret_val

    except:
        return handle_server_500("There was an issue adding message to a session id!")


# blueprint for home page of demystify project:
home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/")
def home():
    return "Main demystify project page"