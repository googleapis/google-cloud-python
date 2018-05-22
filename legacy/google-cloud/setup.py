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
import logging

from setuptools import setup

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PACKAGE_ROOT, 'setup-README.rst')) as file_obj:
    README = file_obj.read()

# NOTE: This is duplicated throughout and we should try to
#       consolidate.
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
        'Development Status :: 7 - Inactive',
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
    'google-api-core >= 0.1.2, < 0.2.0dev',
    'google-cloud-bigquery >= 0.28.0, < 0.29dev',
    'google-cloud-bigquery-datatransfer >= 0.1.0, < 0.2dev',
    'google-cloud-bigtable >= 0.28.1, < 0.29dev',
    'google-cloud-container >= 0.1.0, < 0.2dev',
    'google-cloud-core >= 0.28.0, < 0.29dev',
    'google-cloud-datastore >= 1.4.0, < 1.5dev',
    'google-cloud-dns >= 0.28.0, < 0.29dev',
    'google-cloud-error-reporting >= 0.28.0, < 0.29dev',
    'google-cloud-firestore >= 0.28.0, < 0.29dev',
    'google-cloud-language >= 1.0.0, < 1.1dev',
    'google-cloud-logging >= 1.4.0, < 1.5dev',
    'google-cloud-monitoring >= 0.28.0, < 0.29dev',
    'google-cloud-pubsub >= 0.30.0, < 0.31dev',
    'google-cloud-resource-manager >= 0.28.0, < 0.29dev',
    'google-cloud-runtimeconfig >= 0.28.0, < 0.29dev',
    'google-cloud-spanner >= 0.29.0, < 0.30dev',
    'google-cloud-speech >= 0.30.0, < 0.31dev',
    'google-cloud-storage >= 1.6.0, < 1.7dev',
    'google-cloud-trace >= 0.17.0, < 0.18dev',
    'google-cloud-translate >= 1.3.0, < 1.4dev',
    'google-cloud-videointelligence >= 1.0.0, < 1.1dev',
    'google-cloud-vision >= 0.29.0, < 0.30dev',
]

setup(
    name='google-cloud',
    version='0.33.1',
    description='API Client library for Google Cloud',
    long_description=README,
    install_requires=REQUIREMENTS,
    **SETUP_BASE
)

warning = "WARNING: The google-cloud Python package is deprecated. On " \
          "June 18, 2018, this package will no longer install any other " \
          "packages. Please install the product-specific google-cloud-* " \
          "packages needed for your application. See " \
          "https://github.com/GoogleCloudPlatform/google-cloud-python."

logging.warn(warning)
