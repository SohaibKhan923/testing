import pytest


@pytest.mark.smoke
@pytest.mark.run(order=1)
def test_registration_smoke(register_user_smoke):
    """tests PIV registration endpoint for smoke test"""
    assert register_user_smoke['status_code'] == 201, f"status code {register_user_smoke['status_code']} returned"
    verify_registration_response(register_user_smoke)


@pytest.mark.parametrize("register_user", ["PA", "MI", "IL"], indirect=True)
def test_registration_all_states(register_user):
    """tests PIV registration endpoint for all states"""
    verify_registration_response(register_user)


@pytest.fixture()
def register_user(request, pivapi):
    """Registers a new user for each test method that uses this fixture"""
    state = request.param
    return pivapi.register_user(state)


def verify_registration_response(response_data):
    """takes the object returned from registration and makes assertions"""

    assert response_data['response_data']['data']['kambi_session_id'], \
        'No Kambi session id found from registration'

    assert response_data['response_data']['data']['user_guid'], 'No User Guid Found'

    assert response_data['response_data']['data']['username'] and \
           (response_data['response_data']['data']['username'] ==
            response_data['initial_data']['username'].lower())

    assert response_data['response_data']['data']['email'] and \
           (response_data['response_data']['data']['email'] == response_data['initial_data']['email'])



