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
from google.auth import jwt
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


class TestIDTokenCredentials(object):
    credentials = None

    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    def test_default_state(self, get):
        get.side_effect = [{
            'email': 'service-account@example.com',
            'scope': ['one', 'two'],
        }]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://example.com")

        assert not self.credentials.valid
        # Expiration hasn't been set yet
        assert not self.credentials.expired
        # Service account email hasn't been populated
        assert (self.credentials.service_account_email
                == 'service-account@example.com')
        # Signer is initialized
        assert self.credentials.signer
        assert self.credentials.signer_email == 'service-account@example.com'

    @mock.patch(
        'google.auth._helpers.utcnow',
        return_value=datetime.datetime.utcfromtimestamp(0))
    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    @mock.patch('google.auth.iam.Signer.sign', autospec=True)
    def test_make_authorization_grant_assertion(self, sign, get, utcnow):
        get.side_effect = [{
            'email': 'service-account@example.com',
            'scopes': ['one', 'two']
        }]
        sign.side_effect = [b'signature']

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com")

        # Generate authorization grant:
        token = self.credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, verify=False)

        # The JWT token signature is 'signature' encoded in base 64:
        assert token.endswith(b'.c2lnbmF0dXJl')

        # Check that the credentials have the token and proper expiration
        assert payload == {
            'aud': 'https://www.googleapis.com/oauth2/v4/token',
            'exp': 3600,
            'iat': 0,
            'iss': 'service-account@example.com',
            'target_audience': 'https://audience.com'}

    @mock.patch(
        'google.auth._helpers.utcnow',
        return_value=datetime.datetime.utcfromtimestamp(0))
    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    @mock.patch('google.auth.iam.Signer.sign', autospec=True)
    def test_with_service_account(self, sign, get, utcnow):
        sign.side_effect = [b'signature']

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com",
            service_account_email="service-account@other.com")

        # Generate authorization grant:
        token = self.credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, verify=False)

        # The JWT token signature is 'signature' encoded in base 64:
        assert token.endswith(b'.c2lnbmF0dXJl')

        # Check that the credentials have the token and proper expiration
        assert payload == {
            'aud': 'https://www.googleapis.com/oauth2/v4/token',
            'exp': 3600,
            'iat': 0,
            'iss': 'service-account@other.com',
            'target_audience': 'https://audience.com'}

    @mock.patch(
        'google.auth._helpers.utcnow',
        return_value=datetime.datetime.utcfromtimestamp(0))
    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    @mock.patch('google.auth.iam.Signer.sign', autospec=True)
    def test_additional_claims(self, sign, get, utcnow):
        get.side_effect = [{
            'email': 'service-account@example.com',
            'scopes': ['one', 'two']
        }]
        sign.side_effect = [b'signature']

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com",
            additional_claims={'foo': 'bar'})

        # Generate authorization grant:
        token = self.credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, verify=False)

        # The JWT token signature is 'signature' encoded in base 64:
        assert token.endswith(b'.c2lnbmF0dXJl')

        # Check that the credentials have the token and proper expiration
        assert payload == {
            'aud': 'https://www.googleapis.com/oauth2/v4/token',
            'exp': 3600,
            'iat': 0,
            'iss': 'service-account@example.com',
            'target_audience': 'https://audience.com',
            'foo': 'bar'}

    @mock.patch(
        'google.auth._helpers.utcnow',
        return_value=datetime.datetime.utcfromtimestamp(0))
    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    @mock.patch('google.auth.iam.Signer.sign', autospec=True)
    def test_with_target_audience(self, sign, get, utcnow):
        get.side_effect = [{
            'email': 'service-account@example.com',
            'scopes': ['one', 'two']
        }]
        sign.side_effect = [b'signature']

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com")
        self.credentials = (
            self.credentials.with_target_audience("https://actually.not"))

        # Generate authorization grant:
        token = self.credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, verify=False)

        # The JWT token signature is 'signature' encoded in base 64:
        assert token.endswith(b'.c2lnbmF0dXJl')

        # Check that the credentials have the token and proper expiration
        assert payload == {
            'aud': 'https://www.googleapis.com/oauth2/v4/token',
            'exp': 3600,
            'iat': 0,
            'iss': 'service-account@example.com',
            'target_audience': 'https://actually.not'}

    @mock.patch(
        'google.auth._helpers.utcnow',
        return_value=datetime.datetime.utcfromtimestamp(0))
    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    @mock.patch('google.auth.iam.Signer.sign', autospec=True)
    @mock.patch('google.oauth2._client.id_token_jwt_grant', autospec=True)
    def test_refresh_success(self, id_token_jwt_grant, sign, get, utcnow):
        get.side_effect = [{
            'email': 'service-account@example.com',
            'scopes': ['one', 'two']
        }]
        sign.side_effect = [b'signature']
        id_token_jwt_grant.side_effect = [(
            'idtoken',
            datetime.datetime.utcfromtimestamp(3600),
            {},
        )]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com")

        # Refresh credentials
        self.credentials.refresh(None)

        # Check that the credentials have the token and proper expiration
        assert self.credentials.token == 'idtoken'
        assert self.credentials.expiry == (
            datetime.datetime.utcfromtimestamp(3600))

        # Check the credential info
        assert (self.credentials.service_account_email ==
                'service-account@example.com')

        # Check that the credentials are valid (have a token and are not
        # expired)
        assert self.credentials.valid

    @mock.patch(
        'google.auth._helpers.utcnow',
        return_value=datetime.datetime.utcfromtimestamp(0))
    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    @mock.patch('google.auth.iam.Signer.sign', autospec=True)
    def test_refresh_error(self, sign, get, utcnow):
        get.side_effect = [{
            'email': 'service-account@example.com',
            'scopes': ['one', 'two'],
        }]
        sign.side_effect = [b'signature']

        request = mock.create_autospec(transport.Request, instance=True)
        response = mock.Mock()
        response.data = b'{"error": "http error"}'
        response.status = 500
        request.side_effect = [response]

        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com")

        with pytest.raises(exceptions.RefreshError) as excinfo:
            self.credentials.refresh(request)

        assert excinfo.match(r'http error')

    @mock.patch(
        'google.auth._helpers.utcnow',
        return_value=datetime.datetime.utcfromtimestamp(0))
    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    @mock.patch('google.auth.iam.Signer.sign', autospec=True)
    @mock.patch('google.oauth2._client.id_token_jwt_grant', autospec=True)
    def test_before_request_refreshes(
            self, id_token_jwt_grant, sign, get, utcnow):
        get.side_effect = [{
            'email': 'service-account@example.com',
            'scopes': 'one two'
        }]
        sign.side_effect = [b'signature']
        id_token_jwt_grant.side_effect = [(
            'idtoken',
            datetime.datetime.utcfromtimestamp(3600),
            {},
        )]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com")

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

    @mock.patch('google.auth.compute_engine._metadata.get', autospec=True)
    @mock.patch('google.auth.iam.Signer.sign', autospec=True)
    def test_sign_bytes(self, sign, get):
        get.side_effect = [{
            'email': 'service-account@example.com',
            'scopes': ['one', 'two']
        }]
        sign.side_effect = [b'signature']

        request = mock.create_autospec(transport.Request, instance=True)
        response = mock.Mock()
        response.data = b'{"signature": "c2lnbmF0dXJl"}'
        response.status = 200
        request.side_effect = [response]

        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com")

        # Generate authorization grant:
        signature = self.credentials.sign_bytes(b"some bytes")

        # The JWT token signature is 'signature' encoded in base 64:
        assert signature == b'signature'
