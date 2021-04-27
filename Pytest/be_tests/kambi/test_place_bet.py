import pytest


@pytest.mark.smoke
@pytest.mark.run(order=9)
def test_place_bet_and_verify_couponid_smoke(login_user_smoke, place_bet, kambiapi):
    kambi_session_id = login_user_smoke['response_data']['data']['kambi_session_id']

    # verify the place bet response
    verify_place_bet(place_bet)
    coupon_ref = place_bet['couponRef']

    # call coupon history endpoint and verify bet
    coupon_history = kambiapi.get_coupon_history(kambi_session_id, coupon_ref)

    # Body contains coupon Ref
    assert coupon_history[0]['couponRef']
    # Body.bets contains bet Ref
    assert coupon_history[0]['bets'][0]['betRef']
    # Body.bets contains stake
    assert coupon_history[0]['bets'][0]['stake']
    # Body.outcomes contains outcomeId
    assert coupon_history[0]['outcomes'][0]['outcomeId']
    # Body.outcomes contains eventId
    assert coupon_history[0]['outcomes'][0]['eventId']
    # Body.outcomes contains betOfferId and matches
    assert coupon_history[0]['outcomes'][0]['betOfferId'] == place_bet['coupon']['outcomes'][0]['betOfferId']
    # Body.couponRows contains outcomeId and matches
    assert coupon_history[0]['couponRows'][0]['outcomeId'] == place_bet['coupon']['couponRows'][0]['outcomeId']
    # Body.events contains eventId and matches
    assert coupon_history[0]['events'][0]['eventId'] == place_bet['coupon']['events'][0]['eventId']


@pytest.fixture()
def place_bet(login_user_smoke, kambiapi):
    kambi_session_id = login_user_smoke['response_data']['data']['kambi_session_id']
    place_bet_response = kambiapi.place_bet(kambi_session_id)
    return place_bet_response


def verify_place_bet(bet_response):
    # Body contains status and matches SUCCESS
    assert bet_response['status'] in ["SUCCESS", "LIVE_DELAY_PENDING"]
    # Body.coupon contains coupon Ref
    assert bet_response['couponRef']
    # Body.bets contains bet Ref
    assert bet_response['coupon']['bets'][0]['betRef']
    # Body.bets contains playedOdds
    assert bet_response['coupon']['bets'][0]['playedOdds']
    # Body.bets contains stake
    assert bet_response['coupon']['bets'][0]['stake']
    # Body.outcomes contains outcomeId
    assert bet_response['coupon']['outcomes'][0]['outcomeId']
    # Body.outcomes contains eventId
    assert bet_response['coupon']['outcomes'][0]['eventId']
    # Body.outcomes contains betOfferId
    assert bet_response['coupon']['outcomes'][0]['betOfferId']
    # Body.couponRows contains outcomeId
    assert bet_response['coupon']['couponRows'][0]['outcomeId']
    # Body.couponRows contains playedOdds
    assert bet_response['coupon']['couponRows'][0]['playedOdds']
    # Body.events contains eventId
    assert bet_response['coupon']['events'][0]['eventId']
