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

import datetime

import mock
import pytest

from google.auth import _helpers
from google.auth import exceptions
from google.auth import transport
from google.auth.compute_engine import credentials


class TestCredentials(object):
    credentials = None

    @pytest.fixture(autouse=True)
    def credentials_fixture(self):
        self.credentials = credentials.Credentials()

    def test_default_state(self):
        assert not self.credentials.valid
        # Expiration hasn't been set yet
        assert not self.credentials.expired
        # Scopes aren't needed
        assert not self.credentials.requires_scopes
        # Service account email hasn't been populated
        assert self.credentials.service_account_email == 'default'

    @mock.patch(
        'google.auth._helpers.utcnow',
        return_value=datetime.datetime.min + _helpers.CLOCK_SKEW)
    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    def test_refresh_success(self, get, utcnow):
        get.side_effect = [{
            # First request is for sevice account info.
            'email': 'service-account@example.com',
            'scopes': ['one', 'two']
        }, {
            # Second request is for the token.
            'access_token': 'token',
            'expires_in': 500
        }]

        # Refresh credentials
        self.credentials.refresh(None)

        # Check that the credentials have the token and proper expiration
        assert self.credentials.token == 'token'
        assert self.credentials.expiry == (
            utcnow() + datetime.timedelta(seconds=500))

        # Check the credential info
        assert (self.credentials.service_account_email ==
                'service-account@example.com')
        assert self.credentials._scopes == ['one', 'two']

        # Check that the credentials are valid (have a token and are not
        # expired)
        assert self.credentials.valid

    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    def test_refresh_error(self, get):
        get.side_effect = exceptions.TransportError('http error')

        with pytest.raises(exceptions.RefreshError) as excinfo:
            self.credentials.refresh(None)

        assert excinfo.match(r'http error')

    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    def test_before_request_refreshes(self, get):
        get.side_effect = [{
            # First request is for sevice account info.
            'email': 'service-account@example.com',
            'scopes': 'one two'
        }, {
            # Second request is for the token.
            'access_token': 'token',
            'expires_in': 500
        }]

        # Credentials should start as invalid
        assert not self.credentials.valid

        # before_request should cause a refresh
        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials.before_request(
            request, 'GET', 'http://example.com?a=1#3', {})

        # The refresh endpoint should've been called.
        assert get.called

        # Credentials should now be valid.
        assert self.credentials.valid
