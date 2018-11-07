import os
import unittest
from unittest import mock

from artapi.client import CoreApiClient


class TestResponse:
    def __init__(self):
        self.status_code = 401


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
