import requests
import logging
import json
from env_data import env_data

logging.basicConfig(level=logging.INFO)


class KambiApi:
    def __init__(self, env='dev'):
        try:
            self.url = env_data[env]['kambi_url']
            self.playerapiurl = self.url + "/player/api"
            logging.info('Initialized kambi Api for ENV: %s', env)
        except KeyError:
            raise KeyError('Unsupported Environment')

    def get_events(self):
        offering_url = self.url + "/offering/v2018/pivuspa/betoffer/landing.json?lang=en_US&market=US"
        logging.info(' Getting bet_Offers from Kambi')
        get_events_request = requests.get(offering_url)
        get_events_request.raise_for_status()
        get_events_response = get_events_request.json()

        for result in get_events_response['result']:
            event_type = result['name']
            events = result['events']
            if event_type != 'startingsoonaggregate':
                if events:
                    for event_dict in events:
                        bet_Offers = event_dict['betOffers']
                        if bet_Offers:
                            for bet_Offer in bet_Offers:
                                bet_Offer_str = json.dumps(bet_Offer)
                                if not ('suspended' in bet_Offer_str):
                                    outcomes = bet_Offer['outcomes']
                                    for outcome in outcomes:
                                        if outcome['status'] == 'OPEN':
                                            return {
                                                'outcomeId': outcome['id'],
                                                'betOfferId': outcome['betOfferId'],
                                                'eventId': bet_Offer['eventId'],
                                                'approvedOdds': outcome['odds']
                                            }

    def place_bet(self, kambi_session_id, stake=1000):
        event_info = self.get_events()

        place_bet_url = self.playerapiurl + "/v2019/pivuspa/coupon.json?lang=en_US&market=US&channel_id=1"

        headers = {'Authorization': 'Bearer ' + kambi_session_id,
                   'Content-Type': 'application/json',
                   'consumer': 'script'
                   }

        payload = json.dumps({
            "couponRows": [{
                "index": 0,
                "odds": event_info['approvedOdds'],
                "outcomeId": event_info['outcomeId'],
                "type": "SIMPLE"
            }],
            "bets": [{
                "couponRowIndexes": [0],
                "eachWay": 'false',
                "stake": stake
            }],
            "allowOddsChange": "NO",
            "channel": "WEB",
            "trackingData": {
                "hasTeaser": False,
                "isBetBuilderCombination": False,
                "selectedOutcomes": [{
                    "id": event_info['outcomeId'],
                    "outcomeId": event_info['outcomeId'],
                    "betofferId": event_info['betOfferId'],
                    "eventId": event_info['eventId'],
                    "approvedOdds": event_info['approvedOdds'],
                    "isLiveBetoffer": False,
                    "isPrematchBetoffer": True,
                    "fromBetBuilder": False,
                    "oddsApproved": True,
                    "eachWayApproved": True,
                    "source": "Event List View"
                }]
            },
            "requestId": "f24ab52b-3707-4e93-a4b4-f280e75474b8"
        })
        logging.info(' placing bet on EventId: %s and betOfferId: %s', event_info['eventId'], event_info['betOfferId'])

        place_bet_request = requests.request("POST", place_bet_url, headers=headers, data=payload)

        place_bet_request.raise_for_status()

        logging.info(' Successfully placed bet')

        place_bet_response = place_bet_request.json()
        return place_bet_response

    def get_coupon_history(self, kambi_session_id, couponref):
        get_coupon_history_url = self.playerapiurl + f"/v2019/pivuspa/coupon/history/{couponref}.json"

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + kambi_session_id
        }
        get_coupon_history_request = requests.get(get_coupon_history_url, headers=headers, data=payload)
        get_coupon_history_request.raise_for_status()
        get_coupon_history_response = get_coupon_history_request.json()
        logging.info(' Successfully retrieved coupon history couponRef: %s', get_coupon_history_response[0]['couponRef'])
        return get_coupon_history_response
