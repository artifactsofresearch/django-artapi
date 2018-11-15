from datetime import datetime, timedelta
import os
import unittest
from unittest import mock
from artapi.client import CoreApiClient
import shelve


class TestResponse:
    def __init__(self):
        self.status_code = 401

    def raise_for_status(self):
        pass

    def json(self, expires_in=60 * 60 * 12):
        return {'access_token': 'test-token',
                'expires_in': expires_in}


class TestApiClient(unittest.TestCase):
    def setUp(self):
        self.client = CoreApiClient('https://site.com/', 'test-client-id', 'test-client-secret', 1)

    def test_set_token(self):
        self.skipTest('change after testing')
        self.client.token = TestResponse().json()
        with shelve.open('.cache') as shelve_file:
            self.assertEqual(shelve_file['API_TOKEN'], 'test-token')
        os.remove('.cache')

    def test_get_token(self):
        self.skipTest('change after testing')
        with shelve.open('.cache') as shelve_file:
            shelve_file['API_TOKEN'] = 'test-token'
        self.assertEqual(self.client.token['API_TOKEN'], 'test-token')
        os.remove('.cache')

    @mock.patch.object(CoreApiClient, '_set_token')
    def test_header(self, mock__set_token):
        """
        Test if header is valid
        """
        self.skipTest('change after testing')
        self.client.token = TestResponse().json()
        self.assertEqual(self.client.get_headers(), {'Accept': 'application/json;',
                                                     'Authorization': 'Bearer test-token'})
        self.assertEqual(self.client.get_headers({'key': 0}), {'Accept': 'application/json;',
                                                               'Authorization': 'Bearer test-token',
                                                               'key': 0})
        os.remove('.cache')

    def test_url(self):
        """
        Test that URL is validly formed
        """
        self.assertEqual(self.client.get_api_absolute_url('/poa/'), 'https://site.com/v1/poa/')

    @mock.patch.object(CoreApiClient, '_set_token', return_value=TestResponse())
    @mock.patch.object(CoreApiClient, 'perform_request', return_value=TestResponse())
    def test_401_error(self, mock_perform_request, mock__set_token):
        """
        Check if you received a 401 error, went to get a token
        """
        self.client.post()
        self.assertEqual(mock_perform_request.call_count, 2)

    def test_is_token_expired(self):
        # token is active for 12h
        self.skipTest('change after testing')
        self.client.token = TestResponse().json(expires_in=-5 * 60)
        self.assertTrue(self.client.is_token_expired)
        os.remove('.cache')

    @mock.patch('requests.post', return_value=TestResponse())
    def test__set_token(self, mock_requests_post):
        """
        Check if return valid token
        """
        self.skipTest('change after testing')
        self.client._set_token()
        self.assertEqual(self.client.token['API_TOKEN'], 'test-token')
        os.remove('.cache')

    def test_working_without_cachse_file(self):
        """
        Check if we choose to not use cache file, file is not created
        """
        client = CoreApiClient('https://site.com/', 'test-client-id', 'test-client-secret', 1, None)
        client.token = TestResponse().json()
        self.assertFalse(os.path.isfile('.cache'))


if __name__ == '__main__':
    unittest.main()
