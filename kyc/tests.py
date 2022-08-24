# Create your tests here.
import os
import json
from rest_framework.test import APITestCase
from utilities.credmanager.credentials.get_credentials import get_cred
import logging

logger = logging.getLogger(__name__)


class PanAuthenticationTests(APITestCase):
    """Function to test for authentication of pan number"""
    def test_pan_authentication(self):
        """
        Tests for authenticating pan number
        """
        test_name = 'karza_pan_authentication'
        url_endpoint = 'kyckra_pan_authentication'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json', **{'HTTP_AUTHORIZATION': cred['authorization']},
                                      follow=True)
            logger.debug('Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])


class EntityPANProfileTests(APITestCase):
    """Function to test for verifying pan profile"""
    def test_entity_pan_profile(self):
        """
        Tests for verifying entity pan profile
        """
        test_name = 'karza_entity_pan_profile'
        url_endpoint = 'kyckra_entity_pan_profile'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json',
                                             **{'HTTP_AUTHORIZATION': cred['authorization']},
                                             follow=True)
            logger.debug(
                'Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])


class EntityGSTAuthenticationTests(APITestCase):
    """Function to test for authenticating gst for an entity"""
    def test_entity_gst_authentication(self):
        """
        Tests for authenticating gst for an entity
        """
        test_name = 'karza_entity_gst_authentication'
        url_endpoint = 'kyckra_entity_gst_authentication'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json',
                                             **{'HTTP_AUTHORIZATION': cred['authorization']},
                                             follow=True)
            logger.debug(
                'Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])


class EntityGSTSearchBasisPANTests(APITestCase):
    """Function to test for authenticating pan number"""
    def test_entity_gst_search_basis_pan(self):
        """
        Tests for verifying pan details in order to fetch gst
        """
        test_name = 'karza_entity_gst_search_basis_pan'
        url_endpoint = 'kyckra_entity_gst_search_basis_pan'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json',
                                             **{'HTTP_AUTHORIZATION': cred['authorization']},
                                             follow=True)
            logger.debug(
                'Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])


class BankVerificationTests(APITestCase):
    """Function to test for verifying bank details"""
    def test_bank_verification(self):
        """
        Tests for verifying bank details
        """
        test_name = 'karza_bank_verification'
        url_endpoint = 'kyckra_bank_account_verification'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json',
                                             **{'HTTP_AUTHORIZATION': cred['authorization']},
                                             follow=True)
            logger.debug(
                'Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])


class BankVerificationAdvancedTests(APITestCase):
    """Function to test for verifying bank account details"""
    def test_bank_verification_advanced(self):
        """
        Tests for verifying bank account details of an individual or entity
        """
        test_name = 'karza_bank_verification_advanced'
        url_endpoint = 'kyckra_bank_account_verification_advanced'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json',
                                             **{'HTTP_AUTHORIZATION': cred['authorization']},
                                             follow=True)
            logger.debug(
                'Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])


class PANStatusCheckTests(APITestCase):
    """Function to test for verifying pan status"""
    def test_pan_status_check(self):
        """
        Tests for verifying pan status of an individual or entity
        """
        test_name = 'karza_pan_status_check'
        url_endpoint = 'kyckra_pan_status_check'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json',
                                             **{'HTTP_AUTHORIZATION': cred['authorization']},
                                             follow=True)
            logger.debug(
                'Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])


class KycOcrTests(APITestCase):
    """Function to test for authenticating pan number"""
    def test_kyc_ocr(self):
        """
        Tests for verifying pan details in order to fetch gst
        """
        test_name = 'karza_kyc_ocr'
        url_endpoint = 'kyckra_kyc_ocr'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json',
                                             **{'HTTP_AUTHORIZATION': cred['authorization']},
                                             follow=True)
            logger.debug(
                'Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])


class CkycDownloadTests(APITestCase):
    """Function to test for authenticating pan number"""
    def test_ckyc_download(self):
        """
        Tests for verifying pan details in order to fetch gst
        """
        test_name = 'karza_ckyc_download'
        url_endpoint = 'kyckra_ckyc_download'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json',
                                             **{'HTTP_AUTHORIZATION': cred['authorization']},
                                             follow=True)
            logger.debug(
                'Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])


class CkycSearchTests(APITestCase):
    """Function to test for authenticating pan number"""
    def test_ckyc_search(self):
        """
        Tests for verifying pan details in order to fetch gst
        """
        test_name = 'karza_ckyc_search'
        url_endpoint = 'kyckra_ckyc_search'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json',
                                             **{'HTTP_AUTHORIZATION': cred['authorization']},
                                             follow=True)
            logger.debug(
                'Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])


class PANAuthenticationAdvanced(APITestCase):
    """Function to test for authentication of pan number"""
    def test_pan_authentication_advanced(self):
        """
        Tests for authenticating pan number
        """
        test_name = 'karza_pan_authentication_advanced'
        url_endpoint = 'kyckra_pan_authentication_advanced'
        logger.debug(f"Test started for {test_name}")

        cred = get_cred()
        url = cred['url'] + f"{url_endpoint}" + '/'
        dir_name = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir_name, f"apis/{test_name}/unittestcases_json")

        with open(filename, "r") as file:
            data = json.load(file)

        logger.debug('Sending TEST data to  the url: %s, data: %s' % (url, data))

        for i in range(len(data)):
            test_response = self.client.post(url, data[i]['test_params'], format='json', **{'HTTP_AUTHORIZATION': cred['authorization']},
                                      follow=True)
            logger.debug('Testing status code response: %s, code: %d' % (test_response.json(), test_response.status_code))
            self.assertEqual(test_response.json()['Status'], data[i]['expected_output']['Status'])
