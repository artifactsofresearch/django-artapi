from datetime import datetime, timedelta
import os
import unittest
from unittest import mock
from artapi.client import CoreApiClient


class TestResponse:
    def __init__(self):
        self.status_code = 401

    def raise_for_status(self):
        pass

    def json(self):
        return {'access_token': 'test-token',
                'expires_in': 60 * 60}


class TestApiClient(unittest.TestCase):
    def setUp(self):
        self.client = CoreApiClient('https://site.com/', 'test-client-id', 'test-client-secret', 1)

    def test_set_token(self):
        self.client.token = 'test-token'
        self.assertEqual(os.environ.get('CORE_API_TOKEN'), 'test-token')

    def test_get_token(self):
        os.environ['CORE_API_TOKEN'] = 'test-token'
        self.assertEqual(self.client.token, 'test-token')

    @mock.patch.object(CoreApiClient, '_get_token', return_value='test-token')
    def test_header(self, mock__get_token):
        """
        Test if header is valid
        """
        self.assertEqual(self.client.get_headers(), {'Accept': 'application/json;',
                                                     'Authorization': 'Bearer test-token'})
        self.assertEqual(self.client.get_headers({'key': 0}), {'Accept': 'application/json;',
                                                               'Authorization': 'Bearer test-token',
                                                               'key': 0})

    def test_url(self):
        """
        Test that URL is validly formed
        """
        self.assertEqual(self.client.get_api_absolute_url('/poa/'), 'https://site.com/v1/poa/')

    @mock.patch.object(CoreApiClient, '_get_token', return_value=TestResponse())
    @mock.patch.object(CoreApiClient, 'perform_request', return_value=TestResponse())
    def test_401_error(self, mock_perform_request, mock__get_token):
        """
        Check if you received a 401 error, went to get a token
        """
        self.client.post()
        self.assertEqual(mock_perform_request.call_count, 2)

    def test_is_token_expired(self):
        self.client.expires_at = datetime.now() - timedelta(minutes=10)
        self.assertTrue(self.client.is_token_expired)

        self.client.expires_at = datetime.now()
        self.assertFalse(self.client.is_token_expired)

    def test_expires_at(self):
        """
        Check if return date is valid
        """
        self.client.expires_at = datetime.now()
        self.assertEqual(self.client.expires_at,
                         datetime.strptime(os.environ['CORE_API_EXPIRES_AT'], '%Y-%m-%d %H:%M:%S.%f'))

    @mock.patch('requests.post', return_value=TestResponse())
    def test__get_toke(self, mock_requests_post):
        """
        Check if return valid token
        """
        token = self.client._get_token()
        self.assertEqual(token, 'test-token')


if __name__ == '__main__':
    unittest.main()
