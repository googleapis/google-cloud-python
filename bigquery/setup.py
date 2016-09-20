import os

from setuptools import setup
from setuptools import find_packages


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PACKAGE_ROOT, 'README.rst')) as file_obj:
    README = file_obj.read()

# NOTE: This is duplicated throughout and we should try to
#       consolidate.
SETUP_BASE = {
    'author': 'Google Cloud Platform',
    'author_email': 'jjg+google-cloud-python@google.com',
    'scripts': [],
    'url': 'https://github.com/GoogleCloudPlatform/google-cloud-python',
    'license': 'Apache 2.0',
    'platforms': 'Posix; MacOS X; Windows',
    'include_package_data': True,
    'zip_safe': False,
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
    ],
}


REQUIREMENTS = [
    'google-cloud-core >= 0.19.0',
]

setup(
    name='google-cloud-bigquery',
    version='0.19.0',
    description='Python Client for Google BigQuery',
    long_description=README,
    namespace_packages=[
        'google',
        'google.cloud',
    ],
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    **SETUP_BASE
)
