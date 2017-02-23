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
import json
import os

import mock
import pytest

from google.auth import _helpers
from google.auth import crypt
from google.auth import jwt
from google.oauth2 import service_account


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

with open(os.path.join(DATA_DIR, 'privatekey.pem'), 'rb') as fh:
    PRIVATE_KEY_BYTES = fh.read()

with open(os.path.join(DATA_DIR, 'public_cert.pem'), 'rb') as fh:
    PUBLIC_CERT_BYTES = fh.read()

with open(os.path.join(DATA_DIR, 'other_cert.pem'), 'rb') as fh:
    OTHER_CERT_BYTES = fh.read()

SERVICE_ACCOUNT_JSON_FILE = os.path.join(DATA_DIR, 'service_account.json')

with open(SERVICE_ACCOUNT_JSON_FILE, 'r') as fh:
    SERVICE_ACCOUNT_INFO = json.load(fh)


@pytest.fixture(scope='module')
def signer():
    return crypt.RSASigner.from_string(PRIVATE_KEY_BYTES, '1')


class TestCredentials(object):
    SERVICE_ACCOUNT_EMAIL = 'service-account@example.com'
    TOKEN_URI = 'https://example.com/oauth2/token'
    credentials = None

    @pytest.fixture(autouse=True)
    def credentials_fixture(self, signer):
        self.credentials = service_account.Credentials(
            signer, self.SERVICE_ACCOUNT_EMAIL, self.TOKEN_URI)

    def test_from_service_account_info(self):
        credentials = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO)

        assert (credentials._signer.key_id ==
                SERVICE_ACCOUNT_INFO['private_key_id'])
        assert (credentials.service_account_email ==
                SERVICE_ACCOUNT_INFO['client_email'])
        assert credentials._token_uri == SERVICE_ACCOUNT_INFO['token_uri']

    def test_from_service_account_info_args(self):
        info = SERVICE_ACCOUNT_INFO.copy()
        scopes = ['email', 'profile']
        subject = 'subject'
        additional_claims = {'meta': 'data'}

        credentials = service_account.Credentials.from_service_account_info(
            info, scopes=scopes, subject=subject,
            additional_claims=additional_claims)

        assert credentials.service_account_email == info['client_email']
        assert credentials._signer.key_id == info['private_key_id']
        assert credentials._token_uri == info['token_uri']
        assert credentials._scopes == scopes
        assert credentials._subject == subject
        assert credentials._additional_claims == additional_claims

    def test_from_service_account_file(self):
        info = SERVICE_ACCOUNT_INFO.copy()

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_JSON_FILE)

        assert credentials.service_account_email == info['client_email']
        assert credentials._signer.key_id == info['private_key_id']
        assert credentials._token_uri == info['token_uri']

    def test_from_service_account_file_args(self):
        info = SERVICE_ACCOUNT_INFO.copy()
        scopes = ['email', 'profile']
        subject = 'subject'
        additional_claims = {'meta': 'data'}

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_JSON_FILE, subject=subject,
            scopes=scopes, additional_claims=additional_claims)

        assert credentials.service_account_email == info['client_email']
        assert credentials._signer.key_id == info['private_key_id']
        assert credentials._token_uri == info['token_uri']
        assert credentials._scopes == scopes
        assert credentials._subject == subject
        assert credentials._additional_claims == additional_claims

    def test_to_jwt_credentials(self):
        jwt_from_svc = self.credentials.to_jwt_credentials(
            audience=mock.sentinel.audience)
        jwt_from_info = jwt.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO,
            audience=mock.sentinel.audience)

        assert isinstance(jwt_from_svc, jwt.Credentials)
        assert jwt_from_svc._signer.key_id == jwt_from_info._signer.key_id
        assert jwt_from_svc._issuer == jwt_from_info._issuer
        assert jwt_from_svc._subject == jwt_from_info._subject
        assert jwt_from_svc._audience == jwt_from_info._audience

    def test_default_state(self):
        assert not self.credentials.valid
        # Expiration hasn't been set yet
        assert not self.credentials.expired
        # Scopes haven't been specified yet
        assert self.credentials.requires_scopes

    def test_sign_bytes(self):
        to_sign = b'123'
        signature = self.credentials.sign_bytes(to_sign)
        assert crypt.verify_signature(to_sign, signature, PUBLIC_CERT_BYTES)

    def test_signer(self):
        assert isinstance(self.credentials.signer, crypt.Signer)

    def test_signer_email(self):
        assert self.credentials.signer_email == self.SERVICE_ACCOUNT_EMAIL

    def test_create_scoped(self):
        scopes = ['email', 'profile']
        credentials = self.credentials.with_scopes(scopes)
        assert credentials._scopes == scopes

    def test__make_authorization_grant_assertion(self):
        token = self.credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, PUBLIC_CERT_BYTES)
        assert payload['iss'] == self.SERVICE_ACCOUNT_EMAIL
        assert payload['aud'] == self.TOKEN_URI

    def test__make_authorization_grant_assertion_scoped(self):
        scopes = ['email', 'profile']
        credentials = self.credentials.with_scopes(scopes)
        token = credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, PUBLIC_CERT_BYTES)
        assert payload['scope'] == 'email profile'

    def test__make_authorization_grant_assertion_subject(self):
        subject = 'user@example.com'
        credentials = self.credentials.with_subject(subject)
        token = credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, PUBLIC_CERT_BYTES)
        assert payload['sub'] == subject

    @mock.patch('google.oauth2._client.jwt_grant', autospec=True)
    def test_refresh_success(self, jwt_grant_mock):
        token = 'token'
        jwt_grant_mock.return_value = (
            token, _helpers.utcnow() + datetime.timedelta(seconds=500), None)
        request_mock = mock.Mock()

        # Refresh credentials
        self.credentials.refresh(request_mock)

        # Check jwt grant call.
        assert jwt_grant_mock.called
        request, token_uri, assertion = jwt_grant_mock.call_args[0]
        assert request == request_mock
        assert token_uri == self.credentials._token_uri
        assert jwt.decode(assertion, PUBLIC_CERT_BYTES)
        # No further assertion done on the token, as there are separate tests
        # for checking the authorization grant assertion.

        # Check that the credentials have the token.
        assert self.credentials.token == token

        # Check that the credentials are valid (have a token and are not
        # expired)
        assert self.credentials.valid

    @mock.patch('google.oauth2._client.jwt_grant', autospec=True)
    def test_before_request_refreshes(self, jwt_grant_mock):
        token = 'token'
        jwt_grant_mock.return_value = (
            token, _helpers.utcnow() + datetime.timedelta(seconds=500), None)
        request_mock = mock.Mock()

        # Credentials should start as invalid
        assert not self.credentials.valid

        # before_request should cause a refresh
        self.credentials.before_request(
            request_mock, 'GET', 'http://example.com?a=1#3', {})

        # The refresh endpoint should've been called.
        assert jwt_grant_mock.called

        # Credentials should now be valid.
        assert self.credentials.valid
