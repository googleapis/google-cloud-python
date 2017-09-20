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

from google.auth import _helpers
from google.auth import transport
from google.oauth2 import credentials


class TestCredentials(object):
    TOKEN_URI = 'https://example.com/oauth2/token'
    REFRESH_TOKEN = 'refresh_token'
    CLIENT_ID = 'client_id'
    CLIENT_SECRET = 'client_secret'

    @classmethod
    def make_credentials(cls):
        return credentials.Credentials(
            token=None, refresh_token=cls.REFRESH_TOKEN,
            token_uri=cls.TOKEN_URI, client_id=cls.CLIENT_ID,
            client_secret=cls.CLIENT_SECRET)

    def test_default_state(self):
        credentials = self.make_credentials()
        assert not credentials.valid
        # Expiration hasn't been set yet
        assert not credentials.expired
        # Scopes aren't required for these credentials
        assert not credentials.requires_scopes
        # Test properties
        assert credentials.refresh_token == self.REFRESH_TOKEN
        assert credentials.token_uri == self.TOKEN_URI
        assert credentials.client_id == self.CLIENT_ID
        assert credentials.client_secret == self.CLIENT_SECRET

    @mock.patch('google.oauth2._client.refresh_grant', autospec=True)
    @mock.patch(
        'google.auth._helpers.utcnow',
        return_value=datetime.datetime.min + _helpers.CLOCK_SKEW)
    def test_refresh_success(self, unused_utcnow, refresh_grant):
        token = 'token'
        expiry = _helpers.utcnow() + datetime.timedelta(seconds=500)
        grant_response = {'id_token': mock.sentinel.id_token}
        refresh_grant.return_value = (
            # Access token
            token,
            # New refresh token
            None,
            # Expiry,
            expiry,
            # Extra data
            grant_response)

        request = mock.create_autospec(transport.Request)
        credentials = self.make_credentials()

        # Refresh credentials
        credentials.refresh(request)

        # Check jwt grant call.
        refresh_grant.assert_called_with(
            request, self.TOKEN_URI, self.REFRESH_TOKEN, self.CLIENT_ID,
            self.CLIENT_SECRET)

        # Check that the credentials have the token and expiry
        assert credentials.token == token
        assert credentials.expiry == expiry
        assert credentials.id_token == mock.sentinel.id_token

        # Check that the credentials are valid (have a token and are not
        # expired)
        assert credentials.valid
