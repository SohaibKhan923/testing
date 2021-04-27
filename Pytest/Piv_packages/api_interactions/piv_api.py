import requests
import random
import datetime
import logging
import json
from env_data import env_data
from faker import Faker
from faker.providers import internet

logging.basicConfig(level=logging.INFO)
fake = Faker()
fake.add_provider(internet)


class PivApi:
    def __init__(self, env='dev'):
        try:
            self.url = env_data[env]['sb-url']
            logging.info('Initialized PivApi for ENV: %s', env)
        except KeyError:
            raise KeyError('Unsupported Environment')

    def register_user(self, state='PA'):
        """
        registers a user with terms and conditions accepted
        """
        register_url = self.url + '/users/register/'
        now = datetime.datetime.now()
        postfix = str(now.day) + str(now.minute) + str(now.microsecond)
        username = "BEauto" + postfix
        password = "A@aaaaaa"
        user_email = username + "@test.com"
        firstname = fake.first_name()
        lastname = fake.last_name()

        payload = {'username': username,
                   'email': user_email,
                   'password': password,
                   'confirm_password': password,
                   'first_security_question_guid': 'df101541-030c-4df5-b55d-bc3d0055d53c',
                   'first_security_question_answer': 'Test1',
                   'second_security_question_guid': 'cb6d90d0-576d-4948-9013-a409ab13111e',
                   'second_security_question_answer': 'Test2',
                   'first_name': firstname,
                   'last_name': lastname,
                   "dob": str(fake.date_of_birth(minimum_age=21)),
                   "address1": "kyc_pass_4 main st.",
                   "address2": fake.building_number(),
                   "city": fake.city(),
                   "state": "PA",
                   "zipcode": "19145",
                   "country_code": "US",
                   "ssn_match": "1233",
                   "phone": f"{random.randint(100, 999)}-{random.randint(100, 999)}-"
                            f"{random.randint(100, 999)}",
                   "preferences": {
                       "odds_format": "american",
                       "require_login_security_questions": False,
                       "require_login_secondary_auth": False,
                       "login_notification": False,
                       "bet_acceptance_criteria": "accept_higher_odds",
                       "review_odds_change": False,
                       "allow_stake_all_straights": True
                   },
                   "channel": "WEB",
                   'currency_code': "USD"
                   }

        for checkbox in self.get_policy_checkboxes(state):
            payload[checkbox["name"]] = True

        register_user_request = requests.post(register_url,
                                              headers={'consumer': 'script',
                                                       'Content-Type': 'application/json',
                                                       'state': state},
                                              json=payload
                                              )
        register_user_response = register_user_request.json()

        # possible schema validation here

        logging.info(' Registered new user: %s in state: %s', username, state)

        return {'initial_data': payload,
                'response_data': register_user_response,
                'state': state,
                'status_code': register_user_request.status_code
                }

    def login_user(self, username, password, state):
        """
        Logs in the user
        """
        login_user_url = self.url + '/users/login/'
        payload = {'username': username, 'password': password}
        login_user_request = requests.post(login_user_url,
                                           headers={'consumer': 'script',
                                                    'Content-Type': 'application/json',
                                                    'state': state},
                                           json=payload
                                           )
        login_user_request.raise_for_status()
        login_user_response = login_user_request.json()
        logging.info(' Logged in with user: %s in State: %s', username, state)
        return {
            'initial_data': payload,
            'response_data': login_user_response,
            'state': state
        }

    def deposit_cash(self, username, token, deposit_amt=100):
        """
        deposits cash for a user
        """
        deposit_cash_url = self.url + '/users/deposit/'
        payload = {
            "amount": deposit_amt
        }
        logging.info('depositing cash $%s for user %s', deposit_amt, username)
        deposit_cash_request = requests.post(deposit_cash_url,
                                             headers={'Content-Type': 'application/json',
                                                      'consumer': 'script',
                                                      'Authorization': f'Token {token}'},
                                             json=payload)
        deposit_cash_request.raise_for_status()
        deposit_cash_reponse = deposit_cash_request.json()
        return deposit_cash_reponse

    def get_balance(self, token):
        """get user balance from piv api"""
        get_balance_url = self.url + '/users/balance/'

        payload = {}
        get_balance_request = requests.get(get_balance_url,
                                           headers={'Authorization': f'Token {token}',
                                                    'consumer': 'script'
                                                    },
                                           data=payload)
        get_balance_request.raise_for_status()
        get_balance_response = get_balance_request.json()
        return get_balance_response

    def get_profile(self, token):
        """get user profile"""
        get_profile_url = self.url + '/users/profile/'
        payload = {}
        get_profile_request = requests.get(get_profile_url,
                                           headers={'Authorization': f'Token {token}',
                                                    'consumer': 'script'
                                                    },
                                           data=payload)
        get_profile_request.raise_for_status()
        get_profile_response = get_profile_request.json()
        return get_profile_response

    def update_profile(self, token, odds_format, require_login_secondary_auth,
                       login_notification, review_odds_change, allow_stake_all_straights):
        """update user profile"""
        update_profile_url = self.url + '/users/profile/'
        payload = json.dumps({
            "locale": "en_US",
            "preferences": {
                "odds_format": odds_format,
                "require_login_security_questions": False,
                "require_login_secondary_auth": require_login_secondary_auth,
                "login_notification": login_notification,
                "review_odds_change": review_odds_change,
                "allow_stake_all_straights": allow_stake_all_straights
            }
        })
        logging.info(' Updating user profile')
        update_profile_request = requests.put(update_profile_url,
                                              headers={'Authorization': f'Token {token}',
                                                       'Content-Type': 'application/json',
                                                       'consumer': 'script'},
                                              data=payload)
        update_profile_request.raise_for_status()
        update_profile_response = update_profile_request.json()
        return update_profile_response

    def get_homepage(self, offering='pivuspa'):
        """get user balance from piv api"""
        get_homepage_url = self.url + '/offerings/homepage/'

        payload = {}
        headers = {'X-Offering-Id': offering,
                   'consumer': 'script'
                   }
        logging.info(' Getting homepage')
        get_homepage_request = requests.get(get_homepage_url,
                                            headers=headers,
                                            data=payload)
        get_homepage_request.raise_for_status()
        get_homepage_response = get_homepage_request.json()

        return get_homepage_response

    def get_stateconfig(self, state='PA'):
        """get user balance from piv api"""

        get_stateconfig_url = self.url + '/stateconfig/{0}/'.format(state)

        payload = {}
        headers = {}

        logging.info(' Getting stateconfig for State: %s', state)
        get_stateconfig_request = requests.get(get_stateconfig_url,
                                               headers=headers,
                                               data=payload)
        get_stateconfig_request.raise_for_status()
        get_stateconfig_response = get_stateconfig_request.json()

        return get_stateconfig_response

    def get_policy_checkboxes(self, state='PA'):
        get_policy_checkboxes_url = self.url + '/policy/accept/'

        headers = {'Content-Type': 'application/json',
                   'state': state,
                   'consumer': 'script'}

        logging.info(' Getting policy check boxes for State: %s', state)
        get_policy_checkboxes_request = requests.get(get_policy_checkboxes_url,
                                                     headers=headers,
                                                     data={})

        get_policy_checkboxes_request.raise_for_status()
        get_policy_checkboxes_response = get_policy_checkboxes_request.json()

        return get_policy_checkboxes_response["data"]["checkboxes"]

    def accept_policy(self, token, state='PA'):
        accept_policy_url = self.url + '/policy/accept/'

        payload = json.dumps({
            "confirm_tos": True,
            "confirm_age": True,
            "confirm_info": True,
            "confirm_keycasino": True,
            "confirm_crimescode": True
        })

        headers = {'Authorization': f'Token {token}',
                   'Content-Type': 'application/json',
                   'state': state,
                   'consumer': 'script'}

        logging.info(' Accepting policy doc for State: %s', state)
        accept_policy_request = requests.post(accept_policy_url,
                                              headers=headers,
                                              data=payload)

        accept_policy_request.raise_for_status()
        accept_policy_response = accept_policy_request.json()

        return accept_policy_response
