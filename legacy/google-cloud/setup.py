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
]

setup(
    name='google-cloud',
    version='0.34.0',
    description='API Client library for Google Cloud',
    long_description=README,
    install_requires=REQUIREMENTS,
    **SETUP_BASE
)

warning = "WARNING: The google-cloud Python package is deprecated. This " \
          "package no longer installs any other " \
          "packages. Please install the product-specific google-cloud-* " \
          "packages needed for your application. See " \
          "https://github.com/GoogleCloudPlatform/google-cloud-python."

logging.warn(warning)
