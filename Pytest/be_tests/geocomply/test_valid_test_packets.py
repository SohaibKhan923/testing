import pytest


@pytest.mark.smoke
@pytest.mark.run(order=7)
def test_generate_and_validate_valid_test_packets(login_user_smoke, geo_generate_smoke, geo_validate_smoke):
    # check response to verify correct state came back from generate
    assert geo_generate_smoke['state'] == login_user_smoke['state'], \
        "Geocomply test packet State didn't match initial State"

    # check to make sure test packet exists
    assert geo_generate_smoke['packet']

    # check geo validate response
    assert geo_validate_smoke['can_bet']
    assert geo_validate_smoke['state'] == login_user_smoke['state'] and not geo_validate_smoke['state_change']


@pytest.fixture()
def geo_generate_smoke(login_user_smoke, geoapi):
    geocomply_jwt = login_user_smoke['response_data']['data']['geocomply_jwt']
    return geoapi.generate_test_packet(geocomply_jwt)


@pytest.fixture()
def geo_validate_smoke(login_user_smoke, geo_generate_smoke, geoapi):
    geocomply_jwt = login_user_smoke['response_data']['data']['geocomply_jwt']
    packet = geo_generate_smoke['packet']
    state = geo_generate_smoke['state']
    return geoapi.validate_test_packet(geocomply_jwt, packet, state )