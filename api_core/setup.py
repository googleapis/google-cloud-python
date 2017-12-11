# Copyright 2016 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from setuptools import find_packages
from setuptools import setup


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PACKAGE_ROOT, 'README.rst')) as file_obj:
    README = file_obj.read()


SETUP_BASE = {
    'author': 'Google Cloud Platform',
    'author_email': 'googleapis-publisher@google.com',
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
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
    ],
}


REQUIREMENTS = [
    'googleapis-common-protos >= 1.5.3, < 2.0dev',
    'protobuf >= 3.0.0',
    'google-auth >= 0.4.0, < 2.0.0dev',
    'requests >= 2.18.0, < 3.0.0dev',
    'setuptools >= 34.0.0',
    'six >= 1.10.0',
    # pytz does not adhere to semver and uses a year.month based scheme.
    # Any valid version of pytz should work for us.
    'pytz',
]

EXTRAS_REQUIREMENTS = {
    ':python_version<"3.2"': ['futures >= 3.2.0'],
    'grpc': ['grpcio >= 1.7.0'],
}

setup(
    name='google-api-core',
    version='0.1.3.dev1',
    description='Core Google API Client Library',
    long_description=README,
    namespace_packages=['google'],
    packages=find_packages(exclude=('tests*',)),
    install_requires=REQUIREMENTS,
    extras_require=EXTRAS_REQUIREMENTS,
    **SETUP_BASE
)
