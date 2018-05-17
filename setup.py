# !/usr/bin/env python
__version__ = "1.0.0"

from distutils.core import setup

setup(
    name='artapi',
    version=__version__,
    description='Library that helps working with Art-Api service',
    author='Artifacts Team',
    author_email='service@artifacts.io',
    url='https://github.com/artifactsofresearch/django-artapi',
    packages=['artapi', ],
    install_requires=[
        'requests',
        'urllib'
    ],
)
