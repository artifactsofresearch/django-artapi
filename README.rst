django-artapi
=============

Versions:
---------
Versions supported by library bumpversion lib. More about it https://pypi.python.org/pypi/bumpversion

Get current version
-------------------
::

    python setup.py --version


Create new version
------------------
1. Install ``bumpversion``
2. Run

   ``bumpversion <part (required)>``

   The part of the version to increase, e.g. major, minor, patch.
    - Patch increase from 1.0.0 to 1.0.1
    - Minor increase from 1.0.0 to 1.1.0
    - Patch increase from 1.0.0 to 2.0.0

Do not forget to change CHANGELOG.md.


Quick start
-----------
::

    client = CoreApiClient(api_url, client_id, client_id, api_version)

    client.send_poa(data)

By default, the library stores the token inside the CoreApiClient.
To memorize the token not only for the current session, you need to pass a parameter ``cache_location``:

client = CoreApiClient(api_url, client_id, client_id, api_version, cache_location)
The ``cache_location`` indicates the path to the storage of the token cache file.

Modules and features
--------------------

artapi.client
*************

``ArtApiClient`` is wrapper over requests library that ensures passing needed headers to request.
``ArtApiClient().get('/health/')`` will call GET on ``{ART_API_URL}/health/`` url and returns data


Tests
-----
To run tests::

    python -m unittest discover -s {path-to-project}

