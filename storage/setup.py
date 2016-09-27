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

from shutil import copytree

try:
    copytree('../setup_base', './setup_base')
except:
    pass
from setup_base.base import SETUP_BASE

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PACKAGE_ROOT, 'README.rst')) as file_obj:
    README = file_obj.read()

# NOTE: This is duplicated throughout and we should try to
#       consolidate.
from setup_base.base import SETUP_BASE

REQUIREMENTS = [
    'google-cloud-core >= 0.20.0',
]

setup(
    name='google-cloud-storage',
    version='0.20.0',
    description='Python Client for Google Cloud Storage',
    long_description=README,
    namespace_packages=[
        'google',
        'google.cloud',
    ],
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    **SETUP_BASE
)
