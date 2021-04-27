import pytest
import time
import logging

logging.basicConfig(level=logging.INFO)
timeout = 10


@pytest.mark.smoke
@pytest.mark.run(order=4)
def test_get_profile(login_user_smoke, pivapi):
    """test piv get profile and update profile endpoints"""

    token = login_user_smoke['response_data']['data']['token']
    username = login_user_smoke['response_data']['data']['username']
    guid = login_user_smoke['response_data']['data']['guid']
    email = login_user_smoke['response_data']['data']['email']

    get_profile_response = pivapi.get_profile(token)

    print(get_profile_response)

    # Body contains odds_format and matches american
    assert get_profile_response['preferences']['odds_format'] == 'american'

    # Body contains require_login_security_questions and matches false (deprecated)
    #assert not get_profile_response['preferences']['require_login_security_questions']

    # Body contains require_login_secondary_auth and matches false
    assert not get_profile_response['preferences']['require_login_secondary_auth']

    # Body contains login_notification and matches false
    assert not get_profile_response['preferences']['login_notification']

    # Body contains bet_acceptance_criteria and matches accept_higher_odds
    assert get_profile_response['preferences']['bet_acceptance_criteria'] == 'accept_higher_odds'

    # Body contains review_odds_change and matches false
    assert not get_profile_response['preferences']['review_odds_change'], \
        "review_odds_change not found or doesn't match"

    # Body contains username and matches
    assert get_profile_response['username'] == username, "username not found or doesn't match"

    # Body contains guid and matches
    assert get_profile_response['guid'] == guid, "no guid found or doesn't match"

    # Body contains email and matches
    assert get_profile_response['email'] == email, "email not found or doesn't match"

    # Body contains locale and matches en_US
    assert get_profile_response['locale'] == 'en_US', "locale doesn't match"

    timeout_start = time.time()
    loyalty_id = get_profile_response['loyalty_id']
    # keep calling get profile until Loyaltyid shows or timeout is met
    # Body contains loyalty_id
    if not loyalty_id:
        while time.time() < timeout_start + timeout and not loyalty_id:
            logging.info(' loyalty id not found polling again')
            loyalty_id = pivapi.get_profile(token)['loyalty_id']

    assert loyalty_id, 'No loyalty id found'

    # Body contains country_code
    assert get_profile_response['country_code']

    # Body contains market
    assert get_profile_response['market']


@pytest.mark.smoke
@pytest.mark.run(order=5)
@pytest.mark.parametrize('odds_format, require_login_secondary_auth, login_notification, '
                         'review_odds_change, allow_stake_all_straights',
                         [('decimal', False, True, False, True),
                          ('american', True, False, False, True),
                          ('decimal', False, False, True, False),
                          ('american', False, False, False, True)]
                         )
def test_update_profile(login_user_smoke, odds_format, pivapi , require_login_secondary_auth,
                        login_notification, review_odds_change, allow_stake_all_straights):
    token = login_user_smoke['response_data']['data']['token']

    update_profile_response = pivapi.update_profile(token, odds_format, require_login_secondary_auth,
                                                        login_notification, review_odds_change,
                                                        allow_stake_all_straights)

    assert update_profile_response['message'] == 'User updated'

    assert update_profile_response['data']['preferences']['odds_format'] == odds_format

    assert update_profile_response['data']['preferences']['require_login_secondary_auth'] \
           == require_login_secondary_auth

    assert update_profile_response['data']['preferences']['login_notification'] == login_notification

    assert update_profile_response['data']['preferences']['review_odds_change'] == review_odds_change

    assert update_profile_response['data']['preferences']['allow_stake_all_straights'] == allow_stake_all_straights

