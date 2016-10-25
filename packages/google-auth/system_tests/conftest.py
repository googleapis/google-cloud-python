# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

from google.auth import _helpers
import google.auth.transport.urllib3
import pytest
import urllib3


HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
HTTP = urllib3.PoolManager()
TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'


@pytest.fixture
def service_account_file():
    """The full path to a valid service account key file."""
    yield os.path.join(DATA_DIR, 'service_account.json')


@pytest.fixture
def request():
    """A transport.request object."""
    yield google.auth.transport.urllib3.Request(HTTP)


@pytest.fixture
def token_info(request):
    """Returns a function that obtains OAuth2 token info."""
    def _token_info(access_token=None, id_token=None):
        query_params = {}

        if access_token is not None:
            query_params['access_token'] = access_token
        elif id_token is not None:
            query_params['id_token'] = id_token
        else:
            raise ValueError('No token specified.')

        url = _helpers.update_query(TOKEN_INFO_URL, query_params)

        response = request(url=url, method='GET')

        return json.loads(response.data.decode('utf-8'))

    yield _token_info


def verify_environment():
    """Checks to make sure that requisite data files are available."""
    if not os.path.isdir(DATA_DIR):
        raise EnvironmentError(
            'In order to run system tests, test data must exist in '
            'system_tests/data. See CONTRIBUTING.rst for details.')


def pytest_configure(config):
    """Pytest hook that runs before Pytest collects any tests."""
    verify_environment()
