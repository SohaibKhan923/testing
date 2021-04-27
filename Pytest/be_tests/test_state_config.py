import pytest


@pytest.mark.smoke
@pytest.mark.run(order=8)
@pytest.mark.parametrize('state', ['PA'])
def test_state_config(pivapi, state):
    stateconfig_response = pivapi.get_stateconfig(state)
    assert stateconfig_response['region_code'] == state, "Region code didn't match"
