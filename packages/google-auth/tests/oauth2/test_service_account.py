# Copyright 2016 Google LLC
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

from google.auth import _helpers
from google.auth import crypt
from google.auth import jwt
from google.auth import transport
from google.oauth2 import service_account


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

with open(os.path.join(DATA_DIR, "privatekey.pem"), "rb") as fh:
    PRIVATE_KEY_BYTES = fh.read()

with open(os.path.join(DATA_DIR, "public_cert.pem"), "rb") as fh:
    PUBLIC_CERT_BYTES = fh.read()

with open(os.path.join(DATA_DIR, "other_cert.pem"), "rb") as fh:
    OTHER_CERT_BYTES = fh.read()

SERVICE_ACCOUNT_JSON_FILE = os.path.join(DATA_DIR, "service_account.json")

with open(SERVICE_ACCOUNT_JSON_FILE, "r") as fh:
    SERVICE_ACCOUNT_INFO = json.load(fh)

SIGNER = crypt.RSASigner.from_string(PRIVATE_KEY_BYTES, "1")


class TestCredentials(object):
    SERVICE_ACCOUNT_EMAIL = "service-account@example.com"
    TOKEN_URI = "https://example.com/oauth2/token"

    @classmethod
    def make_credentials(cls):
        return service_account.Credentials(
            SIGNER, cls.SERVICE_ACCOUNT_EMAIL, cls.TOKEN_URI
        )

    def test_from_service_account_info(self):
        credentials = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO
        )

        assert credentials._signer.key_id == SERVICE_ACCOUNT_INFO["private_key_id"]
        assert credentials.service_account_email == SERVICE_ACCOUNT_INFO["client_email"]
        assert credentials._token_uri == SERVICE_ACCOUNT_INFO["token_uri"]

    def test_from_service_account_info_args(self):
        info = SERVICE_ACCOUNT_INFO.copy()
        scopes = ["email", "profile"]
        subject = "subject"
        additional_claims = {"meta": "data"}

        credentials = service_account.Credentials.from_service_account_info(
            info, scopes=scopes, subject=subject, additional_claims=additional_claims
        )

        assert credentials.service_account_email == info["client_email"]
        assert credentials.project_id == info["project_id"]
        assert credentials._signer.key_id == info["private_key_id"]
        assert credentials._token_uri == info["token_uri"]
        assert credentials._scopes == scopes
        assert credentials._subject == subject
        assert credentials._additional_claims == additional_claims

    def test_from_service_account_file(self):
        info = SERVICE_ACCOUNT_INFO.copy()

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_JSON_FILE
        )

        assert credentials.service_account_email == info["client_email"]
        assert credentials.project_id == info["project_id"]
        assert credentials._signer.key_id == info["private_key_id"]
        assert credentials._token_uri == info["token_uri"]

    def test_from_service_account_file_args(self):
        info = SERVICE_ACCOUNT_INFO.copy()
        scopes = ["email", "profile"]
        subject = "subject"
        additional_claims = {"meta": "data"}

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_JSON_FILE,
            subject=subject,
            scopes=scopes,
            additional_claims=additional_claims,
        )

        assert credentials.service_account_email == info["client_email"]
        assert credentials.project_id == info["project_id"]
        assert credentials._signer.key_id == info["private_key_id"]
        assert credentials._token_uri == info["token_uri"]
        assert credentials._scopes == scopes
        assert credentials._subject == subject
        assert credentials._additional_claims == additional_claims

    def test_default_state(self):
        credentials = self.make_credentials()
        assert not credentials.valid
        # Expiration hasn't been set yet
        assert not credentials.expired
        # Scopes haven't been specified yet
        assert credentials.requires_scopes

    def test_sign_bytes(self):
        credentials = self.make_credentials()
        to_sign = b"123"
        signature = credentials.sign_bytes(to_sign)
        assert crypt.verify_signature(to_sign, signature, PUBLIC_CERT_BYTES)

    def test_signer(self):
        credentials = self.make_credentials()
        assert isinstance(credentials.signer, crypt.Signer)

    def test_signer_email(self):
        credentials = self.make_credentials()
        assert credentials.signer_email == self.SERVICE_ACCOUNT_EMAIL

    def test_create_scoped(self):
        credentials = self.make_credentials()
        scopes = ["email", "profile"]
        credentials = credentials.with_scopes(scopes)
        assert credentials._scopes == scopes

    def test_with_claims(self):
        credentials = self.make_credentials()
        new_credentials = credentials.with_claims({"meep": "moop"})
        assert new_credentials._additional_claims == {"meep": "moop"}

    def test_with_quota_project(self):
        credentials = self.make_credentials()
        new_credentials = credentials.with_quota_project("new-project-456")
        assert new_credentials.quota_project_id == "new-project-456"
        hdrs = {}
        new_credentials.apply(hdrs, token="tok")
        assert "x-goog-user-project" in hdrs

    def test__make_authorization_grant_assertion(self):
        credentials = self.make_credentials()
        token = credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, PUBLIC_CERT_BYTES)
        assert payload["iss"] == self.SERVICE_ACCOUNT_EMAIL
        assert payload["aud"] == self.TOKEN_URI

    def test__make_authorization_grant_assertion_scoped(self):
        credentials = self.make_credentials()
        scopes = ["email", "profile"]
        credentials = credentials.with_scopes(scopes)
        token = credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, PUBLIC_CERT_BYTES)
        assert payload["scope"] == "email profile"

    def test__make_authorization_grant_assertion_subject(self):
        credentials = self.make_credentials()
        subject = "user@example.com"
        credentials = credentials.with_subject(subject)
        token = credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, PUBLIC_CERT_BYTES)
        assert payload["sub"] == subject

    @mock.patch("google.oauth2._client.jwt_grant", autospec=True)
    def test_refresh_success(self, jwt_grant):
        credentials = self.make_credentials()
        token = "token"
        jwt_grant.return_value = (
            token,
            _helpers.utcnow() + datetime.timedelta(seconds=500),
            {},
        )
        request = mock.create_autospec(transport.Request, instance=True)

        # Refresh credentials
        credentials.refresh(request)

        # Check jwt grant call.
        assert jwt_grant.called

        called_request, token_uri, assertion = jwt_grant.call_args[0]
        assert called_request == request
        assert token_uri == credentials._token_uri
        assert jwt.decode(assertion, PUBLIC_CERT_BYTES)
        # No further assertion done on the token, as there are separate tests
        # for checking the authorization grant assertion.

        # Check that the credentials have the token.
        assert credentials.token == token

        # Check that the credentials are valid (have a token and are not
        # expired)
        assert credentials.valid

    @mock.patch("google.oauth2._client.jwt_grant", autospec=True)
    def test_before_request_refreshes(self, jwt_grant):
        credentials = self.make_credentials()
        token = "token"
        jwt_grant.return_value = (
            token,
            _helpers.utcnow() + datetime.timedelta(seconds=500),
            None,
        )
        request = mock.create_autospec(transport.Request, instance=True)

        # Credentials should start as invalid
        assert not credentials.valid

        # before_request should cause a refresh
        credentials.before_request(request, "GET", "http://example.com?a=1#3", {})

        # The refresh endpoint should've been called.
        assert jwt_grant.called

        # Credentials should now be valid.
        assert credentials.valid


class TestIDTokenCredentials(object):
    SERVICE_ACCOUNT_EMAIL = "service-account@example.com"
    TOKEN_URI = "https://example.com/oauth2/token"
    TARGET_AUDIENCE = "https://example.com"

    @classmethod
    def make_credentials(cls):
        return service_account.IDTokenCredentials(
            SIGNER, cls.SERVICE_ACCOUNT_EMAIL, cls.TOKEN_URI, cls.TARGET_AUDIENCE
        )

    def test_from_service_account_info(self):
        credentials = service_account.IDTokenCredentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO, target_audience=self.TARGET_AUDIENCE
        )

        assert credentials._signer.key_id == SERVICE_ACCOUNT_INFO["private_key_id"]
        assert credentials.service_account_email == SERVICE_ACCOUNT_INFO["client_email"]
        assert credentials._token_uri == SERVICE_ACCOUNT_INFO["token_uri"]
        assert credentials._target_audience == self.TARGET_AUDIENCE

    def test_from_service_account_file(self):
        info = SERVICE_ACCOUNT_INFO.copy()

        credentials = service_account.IDTokenCredentials.from_service_account_file(
            SERVICE_ACCOUNT_JSON_FILE, target_audience=self.TARGET_AUDIENCE
        )

        assert credentials.service_account_email == info["client_email"]
        assert credentials._signer.key_id == info["private_key_id"]
        assert credentials._token_uri == info["token_uri"]
        assert credentials._target_audience == self.TARGET_AUDIENCE

    def test_default_state(self):
        credentials = self.make_credentials()
        assert not credentials.valid
        # Expiration hasn't been set yet
        assert not credentials.expired

    def test_sign_bytes(self):
        credentials = self.make_credentials()
        to_sign = b"123"
        signature = credentials.sign_bytes(to_sign)
        assert crypt.verify_signature(to_sign, signature, PUBLIC_CERT_BYTES)

    def test_signer(self):
        credentials = self.make_credentials()
        assert isinstance(credentials.signer, crypt.Signer)

    def test_signer_email(self):
        credentials = self.make_credentials()
        assert credentials.signer_email == self.SERVICE_ACCOUNT_EMAIL

    def test_with_target_audience(self):
        credentials = self.make_credentials()
        new_credentials = credentials.with_target_audience("https://new.example.com")
        assert new_credentials._target_audience == "https://new.example.com"

    def test__make_authorization_grant_assertion(self):
        credentials = self.make_credentials()
        token = credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, PUBLIC_CERT_BYTES)
        assert payload["iss"] == self.SERVICE_ACCOUNT_EMAIL
        assert payload["aud"] == self.TOKEN_URI
        assert payload["target_audience"] == self.TARGET_AUDIENCE

    @mock.patch("google.oauth2._client.id_token_jwt_grant", autospec=True)
    def test_refresh_success(self, id_token_jwt_grant):
        credentials = self.make_credentials()
        token = "token"
        id_token_jwt_grant.return_value = (
            token,
            _helpers.utcnow() + datetime.timedelta(seconds=500),
            {},
        )
        request = mock.create_autospec(transport.Request, instance=True)

        # Refresh credentials
        credentials.refresh(request)

        # Check jwt grant call.
        assert id_token_jwt_grant.called

        called_request, token_uri, assertion = id_token_jwt_grant.call_args[0]
        assert called_request == request
        assert token_uri == credentials._token_uri
        assert jwt.decode(assertion, PUBLIC_CERT_BYTES)
        # No further assertion done on the token, as there are separate tests
        # for checking the authorization grant assertion.

        # Check that the credentials have the token.
        assert credentials.token == token

        # Check that the credentials are valid (have a token and are not
        # expired)
        assert credentials.valid

    @mock.patch("google.oauth2._client.id_token_jwt_grant", autospec=True)
    def test_before_request_refreshes(self, id_token_jwt_grant):
        credentials = self.make_credentials()
        token = "token"
        id_token_jwt_grant.return_value = (
            token,
            _helpers.utcnow() + datetime.timedelta(seconds=500),
            None,
        )
        request = mock.create_autospec(transport.Request, instance=True)

        # Credentials should start as invalid
        assert not credentials.valid

        # before_request should cause a refresh
        credentials.before_request(request, "GET", "http://example.com?a=1#3", {})

        # The refresh endpoint should've been called.
        assert id_token_jwt_grant.called

        # Credentials should now be valid.
        assert credentials.valid
