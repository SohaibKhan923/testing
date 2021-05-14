import pytest
import time
import logging
from piv_api import PivApi
from geocomply_api import GeoApi
from kambi_api import KambiApi

logging.basicConfig(level=logging.INFO)


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev",
                     help="environment to execute tests in ex: dev or qa")


@pytest.fixture(autouse=True, scope='session', name='pivapi')
def initialize_piv_api(pytestconfig, env):
    """Initialize the piv API for the test session with given environment"""
    return PivApi(env=env)


@pytest.fixture(autouse=True, scope='session')
def env(pytestconfig):
    """Initialize the piv API for the test session with given environment"""
    return pytestconfig.getoption('env')


@pytest.fixture(autouse=True, scope='session', name='geoapi')
def initialize_geo_api(pytestconfig, env):
    """Initialize the piv API for the test session with given environment"""
    return GeoApi(env=env)


@pytest.fixture(autouse=True, scope='session', name='kambiapi')
def initialize_kambi_api(pytestconfig, env):
    """Initialize the piv API for the test session with given environment"""
    return KambiApi(env=env)


@pytest.fixture(autouse=True, scope='session')
def register_user_smoke(pivapi):
    """Registers a user for use throughout the entire session"""
    return pivapi.register_user()


@pytest.fixture(autouse=True, scope='session')
def login_user_smoke(register_user_smoke, pivapi):
    username = register_user_smoke['initial_data']['username']
    password = register_user_smoke['initial_data']['password']
    state = register_user_smoke['state']
    return pivapi.login_user(username, password, state)


def pytest_html_report_title(report):
    report.title = "BE Automated tests"


@pytest.fixture(autouse=True, scope='session')
def full_testrun_duration():
    start = time.time()
    yield
    stop = time.time()
    delta = stop - start
    message = ('RUN duration : {:0.3} seconds'.format(delta))
    logging.info(message)
