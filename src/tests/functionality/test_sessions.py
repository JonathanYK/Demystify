def test_main_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid.
    """

    response = test_client.get('/')
    print(response.data)
    assert "Main demystify project page" in str(response.data)
    assert response.status_code == 200


def test_sessions_id_generator_page(test_client, return_session_id=False):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/session_id' page is requested (GET)
    THEN check that a valid session id generated.
    """

    response = test_client.get('/session_id')
    ret_lst = str(response.data)[2:-1].split(":")
    gen_session_id = int(ret_lst[1][1:])

    assert ret_lst[0] == "Session ID generated"
    
    # gen_session_id has to be exactly 9 digits:
    assert len(str(gen_session_id)) == 9
    assert response.status_code == 201

    if return_session_id:
        return gen_session_id

