from flask import Blueprint, request
from .home_bp import Sessions, db
from .err_bp import handle_bad_input_501, handle_server_500
from sqlalchemy.orm import sessionmaker, scoped_session

# validates that curr_session_id in db:
def session_id_validation(curr_session_id):
    return db.session.query(db.exists().where(Sessions.id == curr_session_id)).scalar()


def get_new_session_id():
    
    # generate session id using gen_session_id (according gen_session_id defenitions):
    gen_rand_session = Sessions.gen_session_id()

    # validate that gen_rand_session not exists in the db:
    while db.session.query(db.exists().where(Sessions.id == gen_rand_session)).scalar():
         gen_rand_session = Sessions.gen_session_id()

    return gen_rand_session

    
def get_msg(session_id):
    
    try:
        ret_msg = db.session.query(Sessions).get(session_id).msg
        if not ret_msg:
            return "There is no message for session id " + session_id
        else:
            return "The message for session id " + str(session_id) + " is: " + ret_msg
    
    except:
         return handle_server_500(f"There was an issue retriving the message for session id: {session_id}")


sessions_blueprint = Blueprint('sessions', __name__)

# handles invalid requests:
@sessions_blueprint.route("/session_id", methods=["POST", "PUT", "DELETE"])
def handle_session_id_forbidden_requests():
    return handle_bad_input_501("This method is forbidden for session_id url!")


@sessions_blueprint.route("/session_id", methods=["GET"])
def session_id_generator():
    
    # configure db and get a session id:
    new_session_id = get_new_session_id()

    # create new session with the generated session id:
    new_session = Sessions(new_session_id)
    
    # save the session in the db:
    try:
        
        # creating an infra route to the db engine: 
        sm = sessionmaker(bind=db.engine)

        # creating thread-specific session of sm - handles multiple access to the same sm, using sm to create a session:
        session = scoped_session(sm)

        # adding and commiting new_session to db using the local scoped_session:
        session.add(new_session)
        session.commit()
        return repr(new_session), 201

    except:
            return handle_server_500("There was an issue adding new session id to the db!")

    finally:
        session.close()


# handles invalid requests:
@sessions_blueprint.route("/session_msg", methods=["POST", "PUT", "DELETE"])
def handle_session_msg_forbidden_requests():
    return handle_bad_input_501("This method is forbidden for session msg url!")


# retriving the message of a provided session_id:
@sessions_blueprint.route("/session_msg", methods=["GET"])
def get_session_msg():
    
    # retriving the session_id from the request:
    curr_session_id = request.args.get("session_id")

    if session_id_validation(curr_session_id) is False:
        return handle_bad_input_501(f"The provided session id {curr_session_id} isn't valid!")
    return get_msg(curr_session_id)

    