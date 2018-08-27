from datetime import datetime, timedelta

import requests

try:
    # python 3
    import urllib.parse as urlparse
except ImportError:
    # python 2
    import urlparse  # noqa
try:
    # Django support https://docs.djangoproject.com/en/1.7/releases/1.5/#simplejson-incompatibilities
    import simplejson as json
except ImportError:
    import json


class CoreApiClient(object):
    """
    Client that allow to connect to Core Api service.
    Client is singleton object to keep token.
    Example usage:
        client = CoreApiClient()
        client.get('/health/', data={'test': 'test'})
    """

    token = None
    expired = None

    __instance = None

    def __new__(cls, *args, **kwargs):
        if CoreApiClient.__instance is None:
            CoreApiClient.__instance = object.__new__(cls)
        return CoreApiClient.__instance

    def __init__(self, api_url, client_id, client_secret, api_version):
        self.api_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_version = api_version

    def perform_request(self, method='get', url=None, *args, **kwargs):
        """
        Method that allows to generate request and returns response
        This is base method that will be used by get(), post(), put(), etc
        methods. args and kwargs can contain custom headers, data, params or files
        """

        # Populate headers and perform request
        headers = self.get_headers(kwargs.pop('headers', None))
        url = self.get_absolute_url(url)

        response = getattr(requests, method)(
            url,
            headers=headers,
            timeout=30,
            *args,
            **kwargs
        )
        return response

    def get_headers(self, headers=None):
        """
        Prepare headers to use
        :param additional headers:
        :return headers dict:
        """
        headers = headers if headers else {}
        headers['Accept'] = 'application/json;'

        if self.is_token_expired:
            self.token = self._get_token()
        headers['Authorization'] = "Bearer {}".format(self.token)
        return headers

    def get(self, url=None, *args, **kwargs):
        return self.retry_if_401('get', url, *args, **kwargs)

    def post(self, url=None, *args, **kwargs):
        return self.retry_if_401('post', url, *args, **kwargs)

    def put(self, url=None, *args, **kwargs):
        return self.perform_request('put', url, *args, **kwargs)

    def patch(self, url=None, *args, **kwargs):
        return self.perform_request('patch', url, *args, **kwargs)

    def delete(self, url=None, *args, **kwargs):
        return self.perform_request('delete', url, *args, **kwargs)

    def retry_if_401(self, method, url, *args, **kwargs):
        response = self.perform_request(method, url, *args, **kwargs)
        if response.status_code == 401:
            self._get_token()
            return self.perform_request(method, url, *args, **kwargs)
        return response

    def get_absolute_url(self, url):
        """
        Prepare url to Core application
        :param url:
        :return string url:
        """
        return urlparse.urljoin(self.api_url, url)

    def get_api_absolute_url(self, url):
        """
        Prepare full API url to Core application
        :param url:
        :return string url:
        """
        url_temp = 'v{}{}'.format(self.api_version, url)
        return self.get_absolute_url(url_temp)

    @property
    def is_token_expired(self):
        """
        Check if current token is ok
        :return True - token is ok. False - expired:
        """
        if self.expired:
            if self.expired >= datetime.now() - timedelta(minutes=5):
                return True
        return False

    def _get_token(self):
        """
        Returns token for header
        :return string object:
        """
        url = self.get_absolute_url('/o/token/')
        response = requests.post(url, data={"grant_type": "client_credentials",
                                            'client_id': self.client_id,
                                            'client_secret': self.client_secret})
        response.raise_for_status()

        response = response.json()
        self.token = response['access_token']
        expires = response['expires_in']
        self.expired = datetime.now() + timedelta(seconds=expires)

        return self.token

    def send_poa(self, data):
        """
        Send POA data to Core application
        :param data:
        :return requests Response object:
        """
        url = self.get_api_absolute_url('/poa/')
        response = self.post(url, json=data)

        return response

    def send_poe(self, data, file_obj):
        """
        Send POE data to Core application
        :param data:
        :param file_obj:
        :return requests Response object:
        """
        url = self.get_api_absolute_url('/poe/')
        poe = {
            'data': json.dumps(data)
        }
        files = {'file': file_obj}
        response = self.post(url, data=poe, files=files)

        return response

    def get_statuses(self, request_ids):
        """
        Get transaction statuses by a list of request id's
        :param request_ids:
        :return requests Response object:
        """
        req_ids_str = ','.join(request_ids)
        url = self.get_api_absolute_url('/transaction/statuses/?request_ids=' + req_ids_str)
        response = self.get(url)

        return response
