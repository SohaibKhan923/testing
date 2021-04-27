import requests
import logging
import json
from env_data import env_data

logging.basicConfig(level=logging.INFO)


class GeoApi:
    def __init__(self, env='dev'):
        try:
            self.url = env_data[env]['geo_url']
            logging.info('Initialized GeocomplyApi for ENV: %s', env)
        except KeyError:
            raise KeyError('Unsupported Environment')

    def generate_test_packet(self, geo_jwt, state='PA'):
        generate_test_url = self.url + f'/geocomply/dev_generate/{state}/'

        payload = json.dumps(
            {
                "error_code": 0,
                "state": state,
                "geolocate_in": 900,
                "troubleshooter": []
            })

        generate_test_request = requests.post(generate_test_url,
                                              headers={'X-geo-JWT': geo_jwt,
                                                       'consumer': 'script'
                                                       },
                                              data=payload)
        generate_test_request.raise_for_status()
        generate_test_response = generate_test_request.json()

        logging.info(' Generated Test packet for state: %s', generate_test_response['state'])

        return generate_test_response

    def validate_test_packet(self, geo_jwt, packet, state='PA'):
        validate_packet_url = self.url + '/geocomply/validate/'

        payload = json.dumps({
            "state": state,
            "packet": packet
        })

        validate_packet_request = requests.post(validate_packet_url,
                                                headers={'X-geo-JWT': geo_jwt,
                                                         'consumer': 'script'
                                                         },
                                                data=payload)
        validate_packet_request.raise_for_status()
        validate_packet_response = validate_packet_request.json()
        logging.info(' Validated Test packet for state: %s', validate_packet_response['state'])
        return validate_packet_response
