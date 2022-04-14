import os.path
from tests.functionality.test_sessions import test_sessions_id_generator_page

# test send json with the correct data:
def test_send_json(test_client, json_msg_for_testing=None):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'log?session_id=x' page is requested (GET) where x is the session id (=9 digits).
    .log should be created according to the provided json file
    THEN check the response is valid
    """

    gen_session_id = test_sessions_id_generator_page(test_client=test_client, return_session_id=True)

    sample_session_json = {
    "message": "pytest message check!",
    "additional": {
        "operatingSystem": "Ubuntu", 
        "browserName": "Opera", 
        "browserFullVersion": "89.0.4389.128",
        "navigatorUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    },
    "level": "INFO",
    "timestamp": "2022-02-07T19:18:30.733Z",
    "fileName": "main.py", 
    "lineNumber": "9897"
    }

    if json_msg_for_testing:
        sample_session_json["message"] = json_msg_for_testing + " session_id: " + str(gen_session_id)


    # get the response of sample_session_json json with a new generated gen_session_id session:
    response = test_client.post(f'/log?session_id={gen_session_id}', json=sample_session_json)

    assert response.status_code == 200
    assert f'logging session id: {str(gen_session_id)} done!' in str(response.data)
    
    # could be added in windows env (can be customized to a linux env):
    # assure the log file created according to the session id:
    # assert os.path.exists(os.getcwd() + "\\logging\\" + str(gen_session_id)+".log")
    
    # called from test_sessions_id_msg, should return the session id in order to proceed:
    if json_msg_for_testing:
        return gen_session_id


# test send json with wrong json keys
def test_send_json_wrong_keys(test_client, json_msg_for_testing=None):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'log?session_id=x' page is requested (GET) where x is the session id (=9 digits).
    due to wrong key/s in json file - apropirate message should be retrived.
    THEN check the response is valid
    """

    gen_session_id = test_sessions_id_generator_page(test_client=test_client, return_session_id=True)

    # 'additional' key is wrong, and 'level' is missing
    sample_session_json = {
    "message": "pytest message check with wrong json keys",
    "wrong-additional-in[put": {
        "operatingSystem": "Ubuntu", 
        "browserName": "Opera", 
        "browserFullVersion": "89.0.4389.128",
        "navigatorUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    },
    "timestamp": "2022-02-07T19:18:30.733Z",
    "fileName": "main.py", 
    "lineNumber": "9897"
    }

    # get the response of sample_session_json json with a new generated gen_session_id session:
    response = test_client.post(f'/log?session_id={gen_session_id}', json=sample_session_json)

    assert response.status_code == 501
    assert "The following key/s are missing:\\n\'additional\', \'level" in str(response.data)
    

# test send json with wrong session_id<9 digits:
def test_send_json_wrong_session_id(test_client, json_msg_for_testing=None):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'log?session_id=x' page is requested (GET) where x is the wrong session id (=3 digits).
    due to wrong session id - apropirate message should be retrived.
    THEN check the response is valid
    """

    sample_session_json = {
    "message": "pytest message check!",
    "additional": {
        "operatingSystem": "Ubuntu", 
        "browserName": "Opera", 
        "browserFullVersion": "89.0.4389.128",
        "navigatorUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    },
    "level": "INFO",
    "timestamp": "2022-02-07T19:18:30.733Z",
    "fileName": "main.py", 
    "lineNumber": "9897"
    }

    # get the response of sample_session_json json with wrong session_id session:
    response = test_client.post(f'/log?session_id=999', json=sample_session_json)

    assert response.status_code == 501
    assert "The provided session id isn\'t valid!" in str(response.data)
    

def test_sessions_id_msg(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'session_msg?session_id=x' page is posted where x is the session id (>=1000).
    x will be pulled from the db, after posting JSON session id
    THEN check the response is valid
    """

    # sample message to test:
    json_msg_for_testing = "This is a test message from test_sessions_id_msg using pytest!"

    # send sample json, and retrive it's session_id:
    gen_session_id = test_send_json(test_client=test_client, json_msg_for_testing=json_msg_for_testing)

    # get response message of gen_session_id:
    response = test_client.get(f'/session_msg?session_id={gen_session_id}')

    assert f"{json_msg_for_testing} session_id: " + str(gen_session_id) in str(response.data)


# test session id without message:
def test_sessions_id_without_msg(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'session_msg?session_id=x' page is posted where x is the session id (>=1000).
    x will be pulled from the db, after posting JSON session id
    THEN check the response is valid
    """
    gen_session_id = test_sessions_id_generator_page(test_client=test_client, return_session_id=True)

    # get response message of gen_session_id:
    response = test_client.get(f'/session_msg?session_id={gen_session_id}')

    assert response.status_code == 200
    assert f'There is no message for session id {str(gen_session_id)}' in str(response.data)

