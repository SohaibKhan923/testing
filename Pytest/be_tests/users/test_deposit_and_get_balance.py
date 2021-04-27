import pytest


@pytest.mark.smoke
@pytest.mark.run(order=3)
@pytest.mark.parametrize('deposit_amt', [50, 100, 167])
def test_deposit_and_get_balance(login_user_smoke, pivapi, deposit_amt):
    """tests PIV deposit endpoint"""

    token = login_user_smoke['response_data']['data']['token']
    username = login_user_smoke['response_data']['data']['username']

    # check user balance
    user_balance1 = float(pivapi.get_balance(token)['balance'])

    # deposit cash
    deposit_response = pivapi.deposit_cash(username, token, deposit_amt)

    assert deposit_response['success']
    assert str(deposit_amt) in deposit_response['message'] and 'Successful deposit of' in deposit_response['message']

    # check user balance post deposit to see if it updated correctly
    user_balance2 = float(pivapi.get_balance(token)['balance'])
    # keep checking balance until it updates
    while user_balance1 >= user_balance2:
        user_balance2 = float(pivapi.get_balance(token)['balance'])

    # once balance updates verify that it's equal to old balance plus deposit amount
    assert user_balance2 == user_balance1 + deposit_amt
