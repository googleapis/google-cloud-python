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
import pickle
import sys

import mock
import pytest

from google.auth import _helpers
from google.auth import exceptions
from google.auth import transport
from google.oauth2 import credentials


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

AUTH_USER_JSON_FILE = os.path.join(DATA_DIR, "authorized_user.json")

with open(AUTH_USER_JSON_FILE, "r") as fh:
    AUTH_USER_INFO = json.load(fh)


class TestCredentials(object):
    TOKEN_URI = "https://example.com/oauth2/token"
    REFRESH_TOKEN = "refresh_token"
    CLIENT_ID = "client_id"
    CLIENT_SECRET = "client_secret"

    @classmethod
    def make_credentials(cls):
        return credentials.Credentials(
            token=None,
            refresh_token=cls.REFRESH_TOKEN,
            token_uri=cls.TOKEN_URI,
            client_id=cls.CLIENT_ID,
            client_secret=cls.CLIENT_SECRET,
        )

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

    @mock.patch("google.oauth2._client.refresh_grant", autospec=True)
    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.min + _helpers.CLOCK_SKEW,
    )
    def test_refresh_success(self, unused_utcnow, refresh_grant):
        token = "token"
        expiry = _helpers.utcnow() + datetime.timedelta(seconds=500)
        grant_response = {"id_token": mock.sentinel.id_token}
        refresh_grant.return_value = (
            # Access token
            token,
            # New refresh token
            None,
            # Expiry,
            expiry,
            # Extra data
            grant_response,
        )

        request = mock.create_autospec(transport.Request)
        credentials = self.make_credentials()

        # Refresh credentials
        credentials.refresh(request)

        # Check jwt grant call.
        refresh_grant.assert_called_with(
            request,
            self.TOKEN_URI,
            self.REFRESH_TOKEN,
            self.CLIENT_ID,
            self.CLIENT_SECRET,
            None,
        )

        # Check that the credentials have the token and expiry
        assert credentials.token == token
        assert credentials.expiry == expiry
        assert credentials.id_token == mock.sentinel.id_token

        # Check that the credentials are valid (have a token and are not
        # expired)
        assert credentials.valid

    def test_refresh_no_refresh_token(self):
        request = mock.create_autospec(transport.Request)
        credentials_ = credentials.Credentials(token=None, refresh_token=None)

        with pytest.raises(exceptions.RefreshError, match="necessary fields"):
            credentials_.refresh(request)

        request.assert_not_called()

    @mock.patch("google.oauth2._client.refresh_grant", autospec=True)
    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.min + _helpers.CLOCK_SKEW,
    )
    def test_credentials_with_scopes_requested_refresh_success(
        self, unused_utcnow, refresh_grant
    ):
        scopes = ["email", "profile"]
        token = "token"
        expiry = _helpers.utcnow() + datetime.timedelta(seconds=500)
        grant_response = {"id_token": mock.sentinel.id_token}
        refresh_grant.return_value = (
            # Access token
            token,
            # New refresh token
            None,
            # Expiry,
            expiry,
            # Extra data
            grant_response,
        )

        request = mock.create_autospec(transport.Request)
        creds = credentials.Credentials(
            token=None,
            refresh_token=self.REFRESH_TOKEN,
            token_uri=self.TOKEN_URI,
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            scopes=scopes,
        )

        # Refresh credentials
        creds.refresh(request)

        # Check jwt grant call.
        refresh_grant.assert_called_with(
            request,
            self.TOKEN_URI,
            self.REFRESH_TOKEN,
            self.CLIENT_ID,
            self.CLIENT_SECRET,
            scopes,
        )

        # Check that the credentials have the token and expiry
        assert creds.token == token
        assert creds.expiry == expiry
        assert creds.id_token == mock.sentinel.id_token
        assert creds.has_scopes(scopes)

        # Check that the credentials are valid (have a token and are not
        # expired.)
        assert creds.valid

    @mock.patch("google.oauth2._client.refresh_grant", autospec=True)
    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.min + _helpers.CLOCK_SKEW,
    )
    def test_credentials_with_scopes_returned_refresh_success(
        self, unused_utcnow, refresh_grant
    ):
        scopes = ["email", "profile"]
        token = "token"
        expiry = _helpers.utcnow() + datetime.timedelta(seconds=500)
        grant_response = {
            "id_token": mock.sentinel.id_token,
            "scopes": " ".join(scopes),
        }
        refresh_grant.return_value = (
            # Access token
            token,
            # New refresh token
            None,
            # Expiry,
            expiry,
            # Extra data
            grant_response,
        )

        request = mock.create_autospec(transport.Request)
        creds = credentials.Credentials(
            token=None,
            refresh_token=self.REFRESH_TOKEN,
            token_uri=self.TOKEN_URI,
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            scopes=scopes,
        )

        # Refresh credentials
        creds.refresh(request)

        # Check jwt grant call.
        refresh_grant.assert_called_with(
            request,
            self.TOKEN_URI,
            self.REFRESH_TOKEN,
            self.CLIENT_ID,
            self.CLIENT_SECRET,
            scopes,
        )

        # Check that the credentials have the token and expiry
        assert creds.token == token
        assert creds.expiry == expiry
        assert creds.id_token == mock.sentinel.id_token
        assert creds.has_scopes(scopes)

        # Check that the credentials are valid (have a token and are not
        # expired.)
        assert creds.valid

    @mock.patch("google.oauth2._client.refresh_grant", autospec=True)
    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.min + _helpers.CLOCK_SKEW,
    )
    def test_credentials_with_scopes_refresh_failure_raises_refresh_error(
        self, unused_utcnow, refresh_grant
    ):
        scopes = ["email", "profile"]
        scopes_returned = ["email"]
        token = "token"
        expiry = _helpers.utcnow() + datetime.timedelta(seconds=500)
        grant_response = {
            "id_token": mock.sentinel.id_token,
            "scopes": " ".join(scopes_returned),
        }
        refresh_grant.return_value = (
            # Access token
            token,
            # New refresh token
            None,
            # Expiry,
            expiry,
            # Extra data
            grant_response,
        )

        request = mock.create_autospec(transport.Request)
        creds = credentials.Credentials(
            token=None,
            refresh_token=self.REFRESH_TOKEN,
            token_uri=self.TOKEN_URI,
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            scopes=scopes,
        )

        # Refresh credentials
        with pytest.raises(
            exceptions.RefreshError, match="Not all requested scopes were granted"
        ):
            creds.refresh(request)

        # Check jwt grant call.
        refresh_grant.assert_called_with(
            request,
            self.TOKEN_URI,
            self.REFRESH_TOKEN,
            self.CLIENT_ID,
            self.CLIENT_SECRET,
            scopes,
        )

        # Check that the credentials have the token and expiry
        assert creds.token == token
        assert creds.expiry == expiry
        assert creds.id_token == mock.sentinel.id_token
        assert creds.has_scopes(scopes)

        # Check that the credentials are valid (have a token and are not
        # expired.)
        assert creds.valid

    def test_apply_with_quota_project_id(self):
        creds = credentials.Credentials(
            token="token",
            refresh_token=self.REFRESH_TOKEN,
            token_uri=self.TOKEN_URI,
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            quota_project_id="quota-project-123",
        )

        headers = {}
        creds.apply(headers)
        assert headers["x-goog-user-project"] == "quota-project-123"

    def test_apply_with_no_quota_project_id(self):
        creds = credentials.Credentials(
            token="token",
            refresh_token=self.REFRESH_TOKEN,
            token_uri=self.TOKEN_URI,
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
        )

        headers = {}
        creds.apply(headers)
        assert "x-goog-user-project" not in headers

    def test_with_quota_project(self):
        creds = credentials.Credentials(
            token="token",
            refresh_token=self.REFRESH_TOKEN,
            token_uri=self.TOKEN_URI,
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            quota_project_id="quota-project-123",
        )

        new_creds = creds.with_quota_project("new-project-456")
        assert new_creds.quota_project_id == "new-project-456"
        headers = {}
        creds.apply(headers)
        assert "x-goog-user-project" in headers

    def test_from_authorized_user_info(self):
        info = AUTH_USER_INFO.copy()

        creds = credentials.Credentials.from_authorized_user_info(info)
        assert creds.client_secret == info["client_secret"]
        assert creds.client_id == info["client_id"]
        assert creds.refresh_token == info["refresh_token"]
        assert creds.token_uri == credentials._GOOGLE_OAUTH2_TOKEN_ENDPOINT
        assert creds.scopes is None

        scopes = ["email", "profile"]
        creds = credentials.Credentials.from_authorized_user_info(info, scopes)
        assert creds.client_secret == info["client_secret"]
        assert creds.client_id == info["client_id"]
        assert creds.refresh_token == info["refresh_token"]
        assert creds.token_uri == credentials._GOOGLE_OAUTH2_TOKEN_ENDPOINT
        assert creds.scopes == scopes

    def test_from_authorized_user_file(self):
        info = AUTH_USER_INFO.copy()

        creds = credentials.Credentials.from_authorized_user_file(AUTH_USER_JSON_FILE)
        assert creds.client_secret == info["client_secret"]
        assert creds.client_id == info["client_id"]
        assert creds.refresh_token == info["refresh_token"]
        assert creds.token_uri == credentials._GOOGLE_OAUTH2_TOKEN_ENDPOINT
        assert creds.scopes is None

        scopes = ["email", "profile"]
        creds = credentials.Credentials.from_authorized_user_file(
            AUTH_USER_JSON_FILE, scopes
        )
        assert creds.client_secret == info["client_secret"]
        assert creds.client_id == info["client_id"]
        assert creds.refresh_token == info["refresh_token"]
        assert creds.token_uri == credentials._GOOGLE_OAUTH2_TOKEN_ENDPOINT
        assert creds.scopes == scopes

    def test_to_json(self):
        info = AUTH_USER_INFO.copy()
        creds = credentials.Credentials.from_authorized_user_info(info)

        # Test with no `strip` arg
        json_output = creds.to_json()
        json_asdict = json.loads(json_output)
        assert json_asdict.get("token") == creds.token
        assert json_asdict.get("refresh_token") == creds.refresh_token
        assert json_asdict.get("token_uri") == creds.token_uri
        assert json_asdict.get("client_id") == creds.client_id
        assert json_asdict.get("scopes") == creds.scopes
        assert json_asdict.get("client_secret") == creds.client_secret

        # Test with a `strip` arg
        json_output = creds.to_json(strip=["client_secret"])
        json_asdict = json.loads(json_output)
        assert json_asdict.get("token") == creds.token
        assert json_asdict.get("refresh_token") == creds.refresh_token
        assert json_asdict.get("token_uri") == creds.token_uri
        assert json_asdict.get("client_id") == creds.client_id
        assert json_asdict.get("scopes") == creds.scopes
        assert json_asdict.get("client_secret") is None

    def test_pickle_and_unpickle(self):
        creds = self.make_credentials()
        unpickled = pickle.loads(pickle.dumps(creds))

        # make sure attributes aren't lost during pickling
        assert list(creds.__dict__).sort() == list(unpickled.__dict__).sort()

        for attr in list(creds.__dict__):
            assert getattr(creds, attr) == getattr(unpickled, attr)

    def test_pickle_with_missing_attribute(self):
        creds = self.make_credentials()

        # remove an optional attribute before pickling
        # this mimics a pickle created with a previous class definition with
        # fewer attributes
        del creds.__dict__["_quota_project_id"]

        unpickled = pickle.loads(pickle.dumps(creds))

        # Attribute should be initialized by `__setstate__`
        assert unpickled.quota_project_id is None

    # pickles are not compatible across versions
    @pytest.mark.skipif(
        sys.version_info < (3, 5),
        reason="pickle file can only be loaded with Python >= 3.5",
    )
    def test_unpickle_old_credentials_pickle(self):
        # make sure a credentials file pickled with an older
        # library version (google-auth==1.5.1) can be unpickled
        with open(
            os.path.join(DATA_DIR, "old_oauth_credentials_py3.pickle"), "rb"
        ) as f:
            credentials = pickle.load(f)
            assert credentials.quota_project_id is None


class TestUserAccessTokenCredentials(object):
    def test_instance(self):
        cred = credentials.UserAccessTokenCredentials()
        assert cred._account is None

        cred = cred.with_account("account")
        assert cred._account == "account"

    @mock.patch("google.auth._cloud_sdk.get_auth_access_token", autospec=True)
    def test_refresh(self, get_auth_access_token):
        get_auth_access_token.return_value = "access_token"
        cred = credentials.UserAccessTokenCredentials()
        cred.refresh(None)
        assert cred.token == "access_token"

    @mock.patch(
        "google.oauth2.credentials.UserAccessTokenCredentials.apply", autospec=True
    )
    @mock.patch(
        "google.oauth2.credentials.UserAccessTokenCredentials.refresh", autospec=True
    )
    def test_before_request(self, refresh, apply):
        cred = credentials.UserAccessTokenCredentials()
        cred.before_request(mock.Mock(), "GET", "https://example.com", {})
        refresh.assert_called()
        apply.assert_called()
