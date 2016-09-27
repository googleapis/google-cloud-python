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

from setuptools import find_packages
from setuptools import setup


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PACKAGE_ROOT, 'README.rst')) as file_obj:
    README = file_obj.read()

# NOTE: This is duplicated throughout and we should try to
#       consolidate.
from setup_base import SETUP_BASE

REQUIREMENTS = [
    'google-cloud-bigquery >= 0.20.0',
    'google-cloud-bigtable >= 0.20.0',
    'google-cloud-core >= 0.20.0',
    'google-cloud-datastore >= 0.20.0',
    'google-cloud-dns >= 0.20.0',
    'google-cloud-error-reporting >= 0.20.0',
    'google-cloud-language >= 0.20.0',
    'google-cloud-logging >= 0.20.0',
    'google-cloud-monitoring >= 0.20.0',
    'google-cloud-pubsub >= 0.20.0',
    'google-cloud-resource-manager >= 0.20.0',
    'google-cloud-storage >= 0.20.0',
    'google-cloud-translate >= 0.20.0',
    'google-cloud-vision >= 0.20.0',
]

setup(
    name='google-cloud',
    version='0.20.0',
    description='API Client library for Google Cloud',
    long_description=README,
    install_requires=REQUIREMENTS,
    **SETUP_BASE
)
