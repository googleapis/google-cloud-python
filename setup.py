# Copyright 2016 Google Inc.
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

from setuptools import setup


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
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
    ],
}


REQUIREMENTS = [
    'google-cloud-bigquery >= 0.25.0, < 0.26dev',
    'google-cloud-bigtable >= 0.25.0, < 0.26dev',
    'google-cloud-core >= 0.25.0, < 0.26dev',
    'google-cloud-datastore >= 1.1.0, < 2.0dev',
    'google-cloud-dns >= 0.25.0, < 0.26dev',
    'google-cloud-error-reporting >= 0.25.0, < 0.26dev',
    'google-cloud-language >= 0.25.0, < 0.26dev',
    'google-cloud-logging >= 1.1.0, < 2.0dev',
    'google-cloud-monitoring >= 0.25.0, < 0.26dev',
    'google-cloud-pubsub >= 0.26.0, < 0.27dev',
    'google-cloud-resource-manager >= 0.25.0, < 0.26dev',
    'google-cloud-runtimeconfig >= 0.25.0, < 0.26dev',
    'google-cloud-spanner >= 0.25.0, < 0.26dev',
    'google-cloud-speech >= 0.26.0, < 0.27dev',
    'google-cloud-storage >= 1.2.0, < 2.0dev',
    'google-cloud-translate >= 0.25.0, < 0.26dev',
    'google-cloud-videointelligence >= 0.25.0, < 0.26dev',
    'google-cloud-vision >= 0.25.0, < 0.26dev',
]

setup(
    name='google-cloud',
    version='0.26.0',
    description='API Client library for Google Cloud',
    long_description=README,
    install_requires=REQUIREMENTS,
    **SETUP_BASE
)
