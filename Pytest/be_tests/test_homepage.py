import pytest


@pytest.mark.smoke
@pytest.mark.run(order=6)
def test_homepage(pivapi):
    homepage_response = pivapi.get_homepage()
    assert homepage_response
