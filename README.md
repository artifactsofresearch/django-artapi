# django-artapi
# Versions:
 Versions supported by library bumpversion lib. More about it https://pypi.python.org/pypi/bumpversion
## Get current version

```bash
python setup.py --version
```

## Create new version
1. Install `bumpversion`
2. Run
    ```bash
     bumpversion <part (required)>
    ```
    The part of the version to increase, e.g. major, minor, patch.
    - Patch increase from 1.0.0 to 1.0.1
    - Minor increase from 1.0.0 to 1.1.0
    - Patch increase from 1.0.0 to 2.0.0

#### Do not forget to change CHANGELOG.md.

# Quick start

Add `artapi` to your `INSTALLED_APPS` setting

```python

INSTALLED_APPS = (
    ...
    'artapi',
    ...
)
```

# Modules and features

### artapi.client

`ArtApiClient` is wrapper over requests library that ensures passing needed headers to request.
`ArtApiClient().get('/health/')` will call GET on `{ART_API_URL}/health/` url and returns data


# Tests
To run tests:

`python -m unittest discover -s {path-to-project}`