import pytest
import time

timeout = 10


@pytest.mark.smoke
@pytest.mark.run(order=2)
def test_login_smoke(login_user_smoke, pivapi):
    """tests PIV login endpoint"""
    verify_login_results(login_user_smoke, pivapi)


@pytest.mark.parametrize("login_user", ["PA", "MI", "IL"], indirect=True)
def test_login_all_states(login_user, pivapi):
    """tests PIV login endpoint"""
    verify_login_results(login_user, pivapi)


@pytest.fixture()
def login_user(request, pivapi):
    """Registers a new user for each test method that uses this fixture"""
    state = request.param
    register_response = pivapi.register_user(state)
    username = register_response['initial_data']['username']
    password = register_response['initial_data']['password']
    return pivapi.login_user(username, password, state)


def verify_login_results(response_data, pivapi):
    assert response_data['response_data']['data']['pam_session_id']
    assert response_data['response_data']['data']['kambi_session_id']
    assert response_data['response_data']['data']['token']
    assert response_data['response_data']['data']['user_guid']
    
    assert response_data['response_data']['data']['username'] \
           and (response_data['response_data']['data']['username']
                == response_data['initial_data']['username'].lower())

    # verify KYC Status
    kyc_approved = response_data['response_data']['data']['kyc_approved']
    kyc_status = response_data['response_data']['data']['kyc_status']
    token = response_data['response_data']['data']['token']

    timeout_start = time.time()
    # keep checking user profile until KYC is complete or timeout is met
    while time.time() < timeout_start + timeout and (not kyc_approved or kyc_status != 'COMPLETE'):
        get_profile_response = pivapi.get_profile(token)
        kyc_approved = get_profile_response['kyc_approved']
        kyc_status = get_profile_response['kyc_status']

    assert kyc_approved and kyc_status == 'COMPLETE'

