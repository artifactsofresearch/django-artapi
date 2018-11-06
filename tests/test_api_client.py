import os
import unittest
from unittest import mock

import requests

from artapi.client import CoreApiClient


class TestResponse:
    def __init__(self):
        self.status_code = 401


class TestApiClient(unittest.TestCase):
    def setUp(self):
        self.client = CoreApiClient('test-api-url', 'test-client-id', 'test-client-secret', 'test-api-version')

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
        Test if url is valid
        """
        self.assertEqual(self.client.get_api_absolute_url('test-url'), 'vtest-api-versiontest-url')

    @mock.patch.object(CoreApiClient, 'perform_request', return_value=TestResponse())
    def test_401_error(self, mock_perform_request):
        """
        Check if you received a 401 error, went to get a token
        """
        with self.assertRaises(requests.exceptions.MissingSchema):
            self.client.post()
