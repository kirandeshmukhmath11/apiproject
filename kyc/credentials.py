import json
import re
import http.client
import logging
import requests
import http.client
# from tests_cred.credentials.get_credentials import get_cred
from utilities.credmanager.credentials.get_credentials import get_cred
from utilities.status_codes import KarzaInternalStatusCodes
logger_info = logging.getLogger('info_logs')
logger_error = logging.getLogger('error_logs')


class KarzaKeys():
    # Get api key,api url and test api url
    cred = get_cred()
    api_key = cred['api_key']
    test_api_url = cred['test_api_url']
    api_url = cred['api_url']

    def make_api_call(self, request):
        """ Get api key,api url and test api url """
        try:
            conn = http.client.HTTPSConnection(self.test_api_url)
            headers = {'content-type': "application/json", 'x-karza-key': self.api_key}

            api_endpoint_url = request['api_endpoint_url']

            payload = json.dumps(request['payload'])

            # payload = "{\"consent\":\"<<Y/N>>\",\"pan\":\"BXXXXXXXXR\"}"

            conn.request("POST", api_endpoint_url, payload, headers)

            # conn.request("POST", "/v2/pan", payload, headers)
            res = conn.getresponse()
            data = res.read()

            match = re.findall(r'.*("status.*:(\d{3})|"status":(\d{3})).*', str(data))
            output_json = dict(zip(['request_details', 'response_details'],
                                   [payload, data.decode("utf-8")]))

            if match:
                match = int(match[0][1])
                status_codes_lst = KarzaInternalStatusCodes.list()
                for item in status_codes_lst:
                    if not (isinstance(data, dict)) and match == item['status']:
                        output_json['response_details'] = dict(zip(['Status', 'Message', 'Payload'],
                                                                   [match,
                                                                    item['message'],
                                                                    data.decode("utf-8")]))
                        return output_json

            if not (isinstance(data, dict)):
                output_json['response_details'] = dict(zip(['Status', 'Message', 'Payload'],
                                                           [500, "Issue with 3rd part api call",
                                                            data.decode("utf-8")]))
            return output_json
        except Exception as ex:
            logger_error.error(f"Exception Encountered while making service call with "
                               f" Exception is : {ex}", exc_info=1)
            output_json = dict(zip(['Status', 'Message', 'request_details', 'response_details'],
                                   [500, f"Exception Encountered  service call with "
                                         f"service_request_id. Exception is : {ex}", None,
                                    None]))
            return output_json

    def make_api_call_nontest(self, request):
        """ Get api key,api url and test api url """
        conn = http.client.HTTPSConnection(self.api_url)
        headers = {'content-type': "application/json", 'x-karza-key': self.api_key}

        api_endpoint_url = request['api_endpoint_url']
        payload = json.dumps(request['payload'])
        # payload = "{\"consent\":\"<<Y/N>>\",\"pan\":\"BXXXXXXXXR\"}"

        conn.request("POST", api_endpoint_url, payload, headers)
        # conn.request("POST", "/v2/pan", payload, headers)

        res = conn.getresponse()
        data = res.read()

        output_json = dict(zip(['request_details', 'response_details'],
                               [payload, data.decode("utf-8")]))

        return output_json

    def make_api_call_2(self, request):
        """ Get api key,api url and test api url """
        url = f"https://self.test_api_url{request['api_endpoint_url']}"

        # payload = "{\"consent\":\"Y\",\"pan\":\"AKVPA3378G\"}"
        payload = json.dumps(request['payload'])
        headers = {'content-type': 'application/json', 'x-karza-key': self.api_key}
        response = requests.request("POST", url, data=payload, headers=headers)

        output_json = dict(zip(['request_details', 'response_details'],
                               [payload, response.text]))

        return output_json

    def make_api_call_3(self, request):
        """ Get api key,api url and test api url """
        conn = http.client.HTTPSConnection(self.api_url)
        headers = {'content-type': "application/json", 'x-karza-key': self.api_key}

        api_endpoint_url = request['api_endpoint_url']
        payload = json.dumps(request['payload'])
        # payload = "{\"consent\":\"<<Y/N>>\",\"pan\":\"BXXXXXXXXR\"}"

        conn.request("POST", api_endpoint_url, payload, headers)
        # conn.request("POST", "/v2/pan", payload, headers)

        res = conn.getresponse()
        data = res.read()

        output_json = dict(zip(['request_details', 'response_details'],
                               [payload, data.decode("utf-8")]))

        return output_json

