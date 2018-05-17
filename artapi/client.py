from . import settings
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


class ArtApiClient(object):
    """
    Client that allow to connect to Art Api service.
    Client is singleton object to keep token.
    Example usage:
        client = ArtApiClient()
        client.get('/health/', data={'test': 'test'})
    """

    version = settings.ART_API_VERSION
    token = None
    expired = None

    __instance = None

    def __new__(cls):
        if ArtApiClient.__instance is None:
            ArtApiClient.__instance = object.__new__(cls)
        return ArtApiClient.__instance

    def perform_request(self, method='get', url=None, *args, **kwargs):
        """
        Method that allows to generate request and returns response
        This is base method that will be used by get(), post(), put(), etc
        methods. args and kwargs can contain custom headers, data, params or files

        Example:
            ArtApiClient().perform_request('/token/', headers={'X-TRACKING-ID': '1'})
        Will generate request to http://settings.ART_API_URL/token/ with extra header
        X-TRACKING-ID = 1, headers will be updated by default headers from get_headers() method.


        """
        # Populate headers and perform request

        self.expire_token()
        headers = self.get_headers(kwargs.pop('headers', None))
        url = self.get_absolute_url(url)

        # Get data from kwargs, can be dict or already json.
        data = kwargs.pop('data', None)
        if isinstance(data, dict):
            # Requests supports json
            data = json.dumps(data)

        params = kwargs.pop('params', None)
        if isinstance(params, dict):
            params = json.dumps(params)

        files = kwargs.pop('files', None)

        response = getattr(requests, method)(
            url,
            headers=headers,
            data=data,
            params=params,
            files=files,
            *args,
            **kwargs
        )
        response.raise_for_status()
        return response

    def get_headers(self, headers=None):
        headers = headers if headers else {}
        headers['Accept'] = 'application/json;' \
                            ' indent=4, version={}'.format(self.version)
        headers['Content-Type'] = 'application/json; charset=utf8'
        if self.token is None:
            self.token = self.get_token()
        headers['Authorization'] = "Bearer {}".format(self.token)
        return headers

    def get(self, url=None, *args, **kwargs):
        return self.perform_request('get', url, *args, **kwargs)

    def post(self, url=None, *args, **kwargs):
        return self.perform_request('post', url, *args, **kwargs)

    def put(self, url=None, *args, **kwargs):
        return self.perform_request('put', url, *args, **kwargs)

    def patch(self, url=None, *args, **kwargs):
        return self.perform_request('patch', url, *args, **kwargs)

    def delete(self, url=None, *args, **kwargs):
        return self.perform_request('delete', url, *args, **kwargs)

    @staticmethod
    def get_absolute_url(url):
        return urlparse.urljoin(settings.ART_API_URL, url)

    def get_token(self):
        """
        Returns token for header  
        """

        # TODO: Change to right token path.
        url = self.get_absolute_url('/token/')
        response = self.get(url, data={'login': 'test'})
        # TODO: Check if possible to do it
        self.expired = response.data.get("expired")

        return response.data.get('token')

    def expire_token(self):
        """
        TODO: Implement token expiration.
        Can be:
         if self.expired == datetime.now():
            self.token = None

        """
        pass
