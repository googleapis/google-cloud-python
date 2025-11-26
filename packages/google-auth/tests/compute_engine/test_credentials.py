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
import base64
import datetime
import os

import mock
import pytest  # type: ignore
import responses  # type: ignore

from google.auth import _helpers
from google.auth import environment_vars
from google.auth import exceptions
from google.auth import jwt
from google.auth import transport
from google.auth.compute_engine import credentials
from google.auth.transport import requests
from google.oauth2 import _client

SAMPLE_ID_TOKEN_EXP = 1584393400

# header: {"alg": "RS256", "typ": "JWT", "kid": "1"}
# payload: {"iss": "issuer", "iat": 1584393348, "sub": "subject",
#   "exp": 1584393400,"aud": "audience"}
SAMPLE_ID_TOKEN = (
    b"eyJhbGciOiAiUlMyNTYiLCAidHlwIjogIkpXVCIsICJraWQiOiAiMSJ9."
    b"eyJpc3MiOiAiaXNzdWVyIiwgImlhdCI6IDE1ODQzOTMzNDgsICJzdWIiO"
    b"iAic3ViamVjdCIsICJleHAiOiAxNTg0MzkzNDAwLCAiYXVkIjogImF1ZG"
    b"llbmNlIn0."
    b"OquNjHKhTmlgCk361omRo18F_uY-7y0f_AmLbzW062Q1Zr61HAwHYP5FM"
    b"316CK4_0cH8MUNGASsvZc3VqXAqub6PUTfhemH8pFEwBdAdG0LhrNkU0H"
    b"WN1YpT55IiQ31esLdL5q-qDsOPpNZJUti1y1lAreM5nIn2srdWzGXGs4i"
    b"TRQsn0XkNUCL4RErpciXmjfhMrPkcAjKA-mXQm2fa4jmTlEZFqFmUlym1"
    b"ozJ0yf5grjN6AslN4OGvAv1pS-_Ko_pGBS6IQtSBC6vVKCUuBfaqNjykg"
    b"bsxbLa6Fp0SYeYwO8ifEnkRvasVpc1WTQqfRB2JCj5pTBDzJpIpFCMmnQ"
)

ACCESS_TOKEN_REQUEST_METRICS_HEADER_VALUE = (
    "gl-python/3.7 auth/1.1 auth-request-type/at cred-type/mds"
)
ID_TOKEN_REQUEST_METRICS_HEADER_VALUE = (
    "gl-python/3.7 auth/1.1 auth-request-type/it cred-type/mds"
)
FAKE_SERVICE_ACCOUNT_EMAIL = "foo@bar.com"
FAKE_QUOTA_PROJECT_ID = "fake-quota-project"
FAKE_SCOPES = ["scope1", "scope2"]
FAKE_DEFAULT_SCOPES = ["scope3", "scope4"]
FAKE_UNIVERSE_DOMAIN = "fake-universe-domain"


class TestCredentials(object):
    credentials = None
    credentials_with_all_fields = None
    VALID_TRUST_BOUNDARY = {"encodedLocations": "valid-encoded-locations"}
    NO_OP_TRUST_BOUNDARY = {"encodedLocations": ""}
    EXPECTED_TRUST_BOUNDARY_LOOKUP_URL_DEFAULT_UNIVERSE = "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/default/allowedLocations"

    @pytest.fixture(autouse=True)
    def credentials_fixture(self):
        self.credentials = credentials.Credentials()
        self.credentials_with_all_fields = credentials.Credentials(
            service_account_email=FAKE_SERVICE_ACCOUNT_EMAIL,
            quota_project_id=FAKE_QUOTA_PROJECT_ID,
            scopes=FAKE_SCOPES,
            default_scopes=FAKE_DEFAULT_SCOPES,
            universe_domain=FAKE_UNIVERSE_DOMAIN,
        )

    def test_get_cred_info(self):
        assert self.credentials.get_cred_info() == {
            "credential_source": "metadata server",
            "credential_type": "VM credentials",
            "principal": "default",
        }

    def test_default_state(self):
        assert not self.credentials.valid
        # Expiration hasn't been set yet
        assert not self.credentials.expired
        # Scopes are needed
        assert self.credentials.requires_scopes
        # Service account email hasn't been populated
        assert self.credentials.service_account_email == "default"
        # No quota project
        assert not self.credentials._quota_project_id
        # Universe domain is the default and not cached
        assert self.credentials._universe_domain == "googleapis.com"
        assert not self.credentials._universe_domain_cached

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.min + _helpers.REFRESH_THRESHOLD,
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_refresh_success(self, get, utcnow):
        get.side_effect = [
            {
                # First request is for sevice account info.
                "email": "service-account@example.com",
                "scopes": ["one", "two"],
            },
            {
                # Second request is for the token.
                "access_token": "token",
                "expires_in": 500,
            },
        ]

        # Refresh credentials
        self.credentials.refresh(None)

        # Check that the credentials have the token and proper expiration
        assert self.credentials.token == "token"
        assert self.credentials.expiry == (utcnow() + datetime.timedelta(seconds=500))

        # Check the credential info
        assert self.credentials.service_account_email == "service-account@example.com"
        assert self.credentials._scopes == ["one", "two"]

        # Check that the credentials are valid (have a token and are not
        # expired)
        assert self.credentials.valid

    @mock.patch(
        "google.auth.metrics.token_request_access_token_mds",
        return_value=ACCESS_TOKEN_REQUEST_METRICS_HEADER_VALUE,
    )
    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.min + _helpers.REFRESH_THRESHOLD,
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_refresh_success_with_scopes(self, get, utcnow, mock_metrics_header_value):
        get.side_effect = [
            {
                # First request is for sevice account info.
                "email": "service-account@example.com",
                "scopes": ["one", "two"],
            },
            {
                # Second request is for the token.
                "access_token": "token",
                "expires_in": 500,
            },
        ]

        # Refresh credentials
        scopes = ["three", "four"]
        self.credentials = self.credentials.with_scopes(scopes)
        self.credentials.refresh(None)

        # Check that the credentials have the token and proper expiration
        assert self.credentials.token == "token"
        assert self.credentials.expiry == (utcnow() + datetime.timedelta(seconds=500))

        # Check the credential info
        assert self.credentials.service_account_email == "service-account@example.com"
        assert self.credentials._scopes == scopes

        # Check that the credentials are valid (have a token and are not
        # expired)
        assert self.credentials.valid

        kwargs = get.call_args[1]
        assert kwargs["params"] == {"scopes": "three,four"}
        assert kwargs["headers"] == {
            "x-goog-api-client": ACCESS_TOKEN_REQUEST_METRICS_HEADER_VALUE
        }

    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_refresh_no_email(self, get):
        get.return_value = {
            # No "email" field.
            "scopes": ["one", "two"]
        }

        with pytest.raises(exceptions.RefreshError) as excinfo:
            self.credentials.refresh(None)

        assert excinfo.match(r"missing 'email' field")

    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_refresh_error(self, get):
        get.side_effect = exceptions.TransportError("http error")

        with pytest.raises(exceptions.RefreshError) as excinfo:
            self.credentials.refresh(None)

        assert excinfo.match(r"http error")

    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_before_request_refreshes(self, get):
        get.side_effect = [
            {
                # First request is for sevice account info.
                "email": "service-account@example.com",
                "scopes": "one two",
            },
            {
                # Second request is for the token.
                "access_token": "token",
                "expires_in": 500,
            },
        ]

        # Credentials should start as invalid
        assert not self.credentials.valid

        # before_request should cause a refresh
        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials.before_request(request, "GET", "http://example.com?a=1#3", {})

        # The refresh endpoint should've been called.
        assert get.called

        # Credentials should now be valid.
        assert self.credentials.valid

    def test_with_quota_project(self):
        creds = self.credentials_with_all_fields.with_quota_project("project-foo")

        assert creds._quota_project_id == "project-foo"
        assert creds._service_account_email == FAKE_SERVICE_ACCOUNT_EMAIL
        assert creds._scopes == FAKE_SCOPES
        assert creds._default_scopes == FAKE_DEFAULT_SCOPES
        assert creds.universe_domain == FAKE_UNIVERSE_DOMAIN
        assert creds._universe_domain_cached

    def test_with_scopes(self):
        scopes = ["one", "two"]
        creds = self.credentials_with_all_fields.with_scopes(scopes)

        assert creds._scopes == scopes
        assert creds._quota_project_id == FAKE_QUOTA_PROJECT_ID
        assert creds._service_account_email == FAKE_SERVICE_ACCOUNT_EMAIL
        assert creds._default_scopes is None
        assert creds.universe_domain == FAKE_UNIVERSE_DOMAIN
        assert creds._universe_domain_cached

    def test_with_universe_domain(self):
        creds = self.credentials_with_all_fields.with_universe_domain("universe_domain")

        assert creds._scopes == FAKE_SCOPES
        assert creds._quota_project_id == FAKE_QUOTA_PROJECT_ID
        assert creds._service_account_email == FAKE_SERVICE_ACCOUNT_EMAIL
        assert creds._default_scopes == FAKE_DEFAULT_SCOPES
        assert creds.universe_domain == "universe_domain"
        assert creds._universe_domain_cached

    def test_with_trust_boundary(self):
        creds = self.credentials_with_all_fields
        new_boundary = {"encodedLocations": "new_boundary"}
        new_creds = creds.with_trust_boundary(new_boundary)

        assert new_creds is not creds
        assert new_creds._trust_boundary == new_boundary
        assert new_creds._service_account_email == creds._service_account_email
        assert new_creds._quota_project_id == creds._quota_project_id
        assert new_creds._scopes == creds._scopes
        assert new_creds._default_scopes == creds._default_scopes

    def test_token_usage_metrics(self):
        self.credentials.token = "token"
        self.credentials.expiry = None

        headers = {}
        self.credentials.before_request(mock.Mock(), None, None, headers)
        assert headers["authorization"] == "Bearer token"
        assert headers["x-goog-api-client"] == "cred-type/mds"

    @mock.patch(
        "google.auth.compute_engine._metadata.get_universe_domain",
        return_value="fake_universe_domain",
    )
    def test_universe_domain(self, get_universe_domain):
        # Check the default state
        assert not self.credentials._universe_domain_cached
        assert self.credentials._universe_domain == "googleapis.com"

        # calling the universe_domain property should trigger a call to
        # get_universe_domain to fetch the value. The value should be cached.
        assert self.credentials.universe_domain == "fake_universe_domain"
        assert self.credentials._universe_domain == "fake_universe_domain"
        assert self.credentials._universe_domain_cached
        get_universe_domain.assert_called_once()

        # calling the universe_domain property the second time should use the
        # cached value instead of calling get_universe_domain
        assert self.credentials.universe_domain == "fake_universe_domain"
        get_universe_domain.assert_called_once()

    @mock.patch("google.auth.compute_engine._metadata.get_universe_domain")
    def test_user_provided_universe_domain(self, get_universe_domain):
        assert self.credentials_with_all_fields.universe_domain == FAKE_UNIVERSE_DOMAIN
        assert self.credentials_with_all_fields._universe_domain_cached

        # Since user provided universe_domain, we will not call the universe
        # domain endpoint.
        get_universe_domain.assert_not_called()

    @mock.patch("google.oauth2._client._lookup_trust_boundary", autospec=True)
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_refresh_trust_boundary_lookup_skipped_if_env_var_not_true(
        self, mock_metadata_get, mock_lookup_tb
    ):
        creds = self.credentials
        request = mock.Mock()

        mock_metadata_get.side_effect = [
            # from _retrieve_info
            {"email": "default", "scopes": ["scope1"]},
            # from get_service_account_token
            {"access_token": "mock_token", "expires_in": 3600},
        ]

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "false"}
        ):
            creds.refresh(request)

        mock_lookup_tb.assert_not_called()
        assert creds._trust_boundary is None

    @mock.patch("google.oauth2._client._lookup_trust_boundary", autospec=True)
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_refresh_trust_boundary_lookup_skipped_if_env_var_missing(
        self, mock_metadata_get, mock_lookup_tb
    ):
        creds = self.credentials
        request = mock.Mock()

        mock_metadata_get.side_effect = [
            # from _retrieve_info
            {"email": "default", "scopes": ["scope1"]},
            # from get_service_account_token
            {"access_token": "mock_token", "expires_in": 3600},
        ]

        with mock.patch.dict(os.environ, clear=True):
            creds.refresh(request)

        mock_lookup_tb.assert_not_called()
        assert creds._trust_boundary is None

    @mock.patch.object(_client, "_lookup_trust_boundary", autospec=True)
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_refresh_trust_boundary_lookup_success(
        self, mock_metadata_get, mock_lookup_tb
    ):
        mock_lookup_tb.return_value = {
            "locations": ["us-central1"],
            "encodedLocations": "0xABC",
        }
        creds = self.credentials
        request = mock.Mock()

        # The first call to _metadata.get is for service account info, the second
        # for the access token, and the third for the universe domain.
        mock_metadata_get.side_effect = [
            # from _retrieve_info
            {"email": "resolved-email@example.com", "scopes": ["scope1"]},
            # from get_service_account_token
            {"access_token": "mock_token", "expires_in": 3600},
            # from get_universe_domain
            "",
        ]

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"}
        ):
            creds.refresh(request)

        # Verify _metadata.get was called three times.
        assert mock_metadata_get.call_count == 3
        # Verify lookup_trust_boundary was called with correct URL and token
        expected_url = "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/resolved-email@example.com/allowedLocations"
        mock_lookup_tb.assert_called_once_with(
            request, expected_url, headers={"authorization": "Bearer mock_token"}
        )
        # Verify trust boundary was set
        assert creds._trust_boundary == {
            "locations": ["us-central1"],
            "encodedLocations": "0xABC",
        }

        # Verify x-allowed-locations header is set by apply()
        headers_applied = {}
        creds.apply(headers_applied)
        assert headers_applied["x-allowed-locations"] == "0xABC"

    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch.object(_client, "_lookup_trust_boundary", autospec=True)
    def test_refresh_trust_boundary_lookup_fails_no_cache(
        self, mock_lookup_tb, mock_metadata_get
    ):
        mock_lookup_tb.side_effect = exceptions.RefreshError("Lookup failed")
        creds = self.credentials
        request = mock.Mock()

        # Mock metadata calls for token, universe domain, and service account info
        mock_metadata_get.side_effect = [
            # from _retrieve_info
            {"email": "resolved-email@example.com", "scopes": ["scope1"]},
            # from get_service_account_token
            {"access_token": "mock_token", "expires_in": 3600},
            # from get_universe_domain
            "",
        ]

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"}
        ):
            with pytest.raises(exceptions.RefreshError, match="Lookup failed"):
                creds.refresh(request)

        assert creds._trust_boundary is None
        assert mock_metadata_get.call_count == 3
        mock_lookup_tb.assert_called_once()

    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch.object(_client, "_lookup_trust_boundary", autospec=True)
    def test_refresh_trust_boundary_lookup_fails_with_cached_data(
        self, mock_lookup_tb, mock_metadata_get
    ):
        # First refresh: Successfully fetch a valid trust boundary.
        mock_lookup_tb.return_value = {
            "locations": ["us-central1"],
            "encodedLocations": "0xABC",
        }
        mock_metadata_get.side_effect = [
            # from _retrieve_info
            {"email": "resolved-email@example.com", "scopes": ["scope1"]},
            # from get_service_account_token
            {"access_token": "mock_token_1", "expires_in": 3600},
            # from get_universe_domain
            "",
        ]
        creds = self.credentials
        request = mock.Mock()

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"}
        ):
            creds.refresh(request)

        assert creds._trust_boundary == {
            "locations": ["us-central1"],
            "encodedLocations": "0xABC",
        }
        mock_lookup_tb.assert_called_once()

        # Second refresh: Mock lookup to fail, but expect cached data to be preserved.
        mock_lookup_tb.reset_mock()
        mock_lookup_tb.side_effect = exceptions.RefreshError("Lookup failed")

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"}
        ):
            # This refresh should not raise an error because a cached value exists.
            mock_metadata_get.reset_mock()
            mock_metadata_get.side_effect = [
                # from _retrieve_info
                {"email": "resolved-email@example.com", "scopes": ["scope1"]},
                # from get_service_account_token
                {"access_token": "mock_token_2", "expires_in": 3600},
                # from get_universe_domain
                "",
            ]
            creds.refresh(request)

        assert creds._trust_boundary == {
            "locations": ["us-central1"],
            "encodedLocations": "0xABC",
        }
        mock_lookup_tb.assert_called_once()

    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch.object(_client, "_lookup_trust_boundary", autospec=True)
    def test_refresh_fetches_no_op_trust_boundary(
        self, mock_lookup_tb, mock_metadata_get
    ):
        mock_lookup_tb.return_value = {"locations": [], "encodedLocations": "0x0"}
        creds = self.credentials
        request = mock.Mock()

        mock_metadata_get.side_effect = [
            # from _retrieve_info
            {"email": "resolved-email@example.com", "scopes": ["scope1"]},
            # from get_service_account_token
            {"access_token": "mock_token", "expires_in": 3600},
            # from get_universe_domain
            "",
        ]

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"}
        ):
            creds.refresh(request)

        assert creds._trust_boundary == {"locations": [], "encodedLocations": "0x0"}
        assert mock_metadata_get.call_count == 3
        expected_url = "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/resolved-email@example.com/allowedLocations"
        mock_lookup_tb.assert_called_once_with(
            request, expected_url, headers={"authorization": "Bearer mock_token"}
        )
        # Verify that an empty header was added.
        headers_applied = {}
        creds.apply(headers_applied)
        assert headers_applied["x-allowed-locations"] == ""

    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch.object(_client, "_lookup_trust_boundary", autospec=True)
    def test_refresh_starts_with_no_op_trust_boundary_skips_lookup(
        self, mock_lookup_tb, mock_metadata_get
    ):
        creds = self.credentials
        # Use pre-cache universe domain to avoid an extra metadata call.
        creds._universe_domain_cached = True
        creds._trust_boundary = {"locations": [], "encodedLocations": "0x0"}
        request = mock.Mock()

        mock_metadata_get.side_effect = [
            # from _retrieve_info
            {"email": "resolved-email@example.com", "scopes": ["scope1"]},
            # from get_service_account_token
            {"access_token": "mock_token", "expires_in": 3600},
        ]

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"}
        ):
            creds.refresh(request)

        # Verify trust boundary remained NO_OP
        assert creds._trust_boundary == {"locations": [], "encodedLocations": "0x0"}
        # Lookup should be skipped
        mock_lookup_tb.assert_not_called()
        # Two metadata calls for token refresh should have happened.
        assert mock_metadata_get.call_count == 2

        # Verify that an empty header was added.
        headers_applied = {}
        creds.apply(headers_applied)
        assert headers_applied["x-allowed-locations"] == ""

    @mock.patch(
        "google.auth.compute_engine._metadata.get_service_account_info", autospec=True
    )
    @mock.patch(
        "google.auth.compute_engine._metadata.get_universe_domain", autospec=True
    )
    def test_build_trust_boundary_lookup_url_default_email(
        self, mock_get_universe_domain, mock_get_service_account_info
    ):
        # Test with default service account email, which needs resolution
        creds = self.credentials
        creds._service_account_email = "default"
        mock_get_service_account_info.return_value = {
            "email": "resolved-email@example.com"
        }
        mock_get_universe_domain.return_value = "googleapis.com"

        url = creds._build_trust_boundary_lookup_url()

        mock_get_service_account_info.assert_called_once_with(mock.ANY, "default")
        mock_get_universe_domain.assert_called_once_with(mock.ANY)
        assert url == (
            "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/resolved-email@example.com/allowedLocations"
        )

    @mock.patch(
        "google.auth.compute_engine._metadata.get_service_account_info", autospec=True
    )
    @mock.patch(
        "google.auth.compute_engine._metadata.get_universe_domain", autospec=True
    )
    def test_build_trust_boundary_lookup_url_explicit_email(
        self, mock_get_universe_domain, mock_get_service_account_info
    ):
        # Test with an explicit service account email, no resolution needed
        creds = self.credentials
        creds._service_account_email = FAKE_SERVICE_ACCOUNT_EMAIL
        mock_get_universe_domain.return_value = "googleapis.com"

        url = creds._build_trust_boundary_lookup_url()

        mock_get_service_account_info.assert_not_called()
        mock_get_universe_domain.assert_called_once_with(mock.ANY)
        assert url == (
            "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/foo@bar.com/allowedLocations"
        )

    @mock.patch(
        "google.auth.compute_engine._metadata.get_service_account_info", autospec=True
    )
    @mock.patch(
        "google.auth.compute_engine._metadata.get_universe_domain", autospec=True
    )
    def test_build_trust_boundary_lookup_url_non_default_universe(
        self, mock_get_universe_domain, mock_get_service_account_info
    ):
        # Test with a non-default universe domain
        creds = self.credentials_with_all_fields

        url = creds._build_trust_boundary_lookup_url()

        # Universe domain is cached and email is explicit, so no metadata calls needed.
        mock_get_service_account_info.assert_not_called()
        mock_get_universe_domain.assert_not_called()
        assert url == (
            "https://iamcredentials.fake-universe-domain/v1/projects/-/serviceAccounts/foo@bar.com/allowedLocations"
        )

    @mock.patch(
        "google.auth.compute_engine._metadata.get_service_account_info", autospec=True
    )
    def test_build_trust_boundary_lookup_url_get_service_account_info_fails(
        self, mock_get_service_account_info
    ):
        # Test scenario where get_service_account_info fails
        mock_get_service_account_info.side_effect = exceptions.TransportError(
            "Failed to get info"
        )
        creds = self.credentials
        creds._service_account_email = "default"

        with pytest.raises(
            exceptions.RefreshError,
            match=r"Failed to get service account email for trust boundary lookup: .*",
        ):
            creds._build_trust_boundary_lookup_url()

    @mock.patch(
        "google.auth.compute_engine._metadata.get_service_account_info", autospec=True
    )
    def test_build_trust_boundary_lookup_url_no_email(
        self, mock_get_service_account_info
    ):
        # Test with default service account email, which needs resolution, but metadata
        # returns no email.
        creds = self.credentials
        creds._service_account_email = "default"
        mock_get_service_account_info.return_value = {"scopes": ["one", "two"]}

        with pytest.raises(exceptions.RefreshError) as excinfo:
            creds._build_trust_boundary_lookup_url()

        assert excinfo.match(r"missing 'email' field")


class TestIDTokenCredentials(object):
    credentials = None

    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_default_state(self, get):
        get.side_effect = [
            {"email": "service-account@example.com", "scope": ["one", "two"]}
        ]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://example.com"
        )

        assert not self.credentials.valid
        # Expiration hasn't been set yet
        assert not self.credentials.expired
        # Service account email hasn't been populated
        assert self.credentials.service_account_email == "service-account@example.com"
        # Signer is initialized
        assert self.credentials.signer
        assert self.credentials.signer_email == "service-account@example.com"
        # No quota project
        assert not self.credentials._quota_project_id

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.utcfromtimestamp(0),
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    def test_make_authorization_grant_assertion(self, sign, get, utcnow):
        get.side_effect = [
            {"email": "service-account@example.com", "scopes": ["one", "two"]}
        ]
        sign.side_effect = [b"signature"]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com"
        )

        # Generate authorization grant:
        token = self.credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, verify=False)

        # The JWT token signature is 'signature' encoded in base 64:
        assert token.endswith(b".c2lnbmF0dXJl")

        # Check that the credentials have the token and proper expiration
        assert payload == {
            "aud": "https://www.googleapis.com/oauth2/v4/token",
            "exp": 3600,
            "iat": 0,
            "iss": "service-account@example.com",
            "target_audience": "https://audience.com",
        }

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.utcfromtimestamp(0),
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    def test_with_service_account(self, sign, get, utcnow):
        sign.side_effect = [b"signature"]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request,
            target_audience="https://audience.com",
            service_account_email="service-account@other.com",
        )

        # Generate authorization grant:
        token = self.credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, verify=False)

        # The JWT token signature is 'signature' encoded in base 64:
        assert token.endswith(b".c2lnbmF0dXJl")

        # Check that the credentials have the token and proper expiration
        assert payload == {
            "aud": "https://www.googleapis.com/oauth2/v4/token",
            "exp": 3600,
            "iat": 0,
            "iss": "service-account@other.com",
            "target_audience": "https://audience.com",
        }

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.utcfromtimestamp(0),
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    def test_additional_claims(self, sign, get, utcnow):
        get.side_effect = [
            {"email": "service-account@example.com", "scopes": ["one", "two"]}
        ]
        sign.side_effect = [b"signature"]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request,
            target_audience="https://audience.com",
            additional_claims={"foo": "bar"},
        )

        # Generate authorization grant:
        token = self.credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, verify=False)

        # The JWT token signature is 'signature' encoded in base 64:
        assert token.endswith(b".c2lnbmF0dXJl")

        # Check that the credentials have the token and proper expiration
        assert payload == {
            "aud": "https://www.googleapis.com/oauth2/v4/token",
            "exp": 3600,
            "iat": 0,
            "iss": "service-account@example.com",
            "target_audience": "https://audience.com",
            "foo": "bar",
        }

    def test_token_uri(self):
        request = mock.create_autospec(transport.Request, instance=True)

        self.credentials = credentials.IDTokenCredentials(
            request=request,
            signer=mock.Mock(),
            service_account_email="foo@example.com",
            target_audience="https://audience.com",
        )
        assert self.credentials._token_uri == credentials._DEFAULT_TOKEN_URI

        self.credentials = credentials.IDTokenCredentials(
            request=request,
            signer=mock.Mock(),
            service_account_email="foo@example.com",
            target_audience="https://audience.com",
            token_uri="https://example.com/token",
        )
        assert self.credentials._token_uri == "https://example.com/token"

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.utcfromtimestamp(0),
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    def test_with_target_audience(self, sign, get, utcnow):
        get.side_effect = [
            {"email": "service-account@example.com", "scopes": ["one", "two"]}
        ]
        sign.side_effect = [b"signature"]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com"
        )
        self.credentials = self.credentials.with_target_audience("https://actually.not")

        # Generate authorization grant:
        token = self.credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, verify=False)

        # The JWT token signature is 'signature' encoded in base 64:
        assert token.endswith(b".c2lnbmF0dXJl")

        # Check that the credentials have the token and proper expiration
        assert payload == {
            "aud": "https://www.googleapis.com/oauth2/v4/token",
            "exp": 3600,
            "iat": 0,
            "iss": "service-account@example.com",
            "target_audience": "https://actually.not",
        }

        # Check that the signer have been initialized with a Request object
        assert isinstance(self.credentials._signer._request, transport.Request)

    @responses.activate
    def test_with_target_audience_integration(self):
        """Test that it is possible to refresh credentials
        generated from `with_target_audience`.

        Instead of mocking the methods, the HTTP responses
        have been mocked.
        """

        # mock information about credentials
        responses.add(
            responses.GET,
            "http://metadata.google.internal/computeMetadata/v1/instance/"
            "service-accounts/default/?recursive=true",
            status=200,
            content_type="application/json",
            json={
                "scopes": "email",
                "email": "service-account@example.com",
                "aliases": ["default"],
            },
        )

        # mock information about universe_domain
        responses.add(
            responses.GET,
            "http://metadata.google.internal/computeMetadata/v1/universe/"
            "universe-domain",
            status=200,
            content_type="application/json",
            json={},
        )

        # mock token for credentials
        responses.add(
            responses.GET,
            "http://metadata.google.internal/computeMetadata/v1/instance/"
            "service-accounts/default/token",
            status=200,
            content_type="application/json",
            json={
                "access_token": "some-token",
                "expires_in": 3210,
                "token_type": "Bearer",
            },
        )

        # mock sign blob endpoint
        signature = base64.b64encode(b"some-signature").decode("utf-8")
        responses.add(
            responses.POST,
            "https://iamcredentials.googleapis.com/v1/projects/-/"
            "serviceAccounts/service-account@example.com:signBlob",
            status=200,
            content_type="application/json",
            json={"keyId": "some-key-id", "signedBlob": signature},
        )

        id_token = "{}.{}.{}".format(
            base64.b64encode(b'{"some":"some"}').decode("utf-8"),
            base64.b64encode(b'{"exp": 3210}').decode("utf-8"),
            base64.b64encode(b"token").decode("utf-8"),
        )

        # mock id token endpoint
        responses.add(
            responses.POST,
            "https://www.googleapis.com/oauth2/v4/token",
            status=200,
            content_type="application/json",
            json={"id_token": id_token, "expiry": 3210},
        )

        self.credentials = credentials.IDTokenCredentials(
            request=requests.Request(),
            service_account_email="service-account@example.com",
            target_audience="https://audience.com",
        )

        self.credentials = self.credentials.with_target_audience("https://actually.not")

        self.credentials.refresh(requests.Request())

        assert self.credentials.token is not None

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.utcfromtimestamp(0),
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    def test_with_quota_project(self, sign, get, utcnow):
        get.side_effect = [
            {"email": "service-account@example.com", "scopes": ["one", "two"]}
        ]
        sign.side_effect = [b"signature"]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com"
        )
        self.credentials = self.credentials.with_quota_project("project-foo")

        assert self.credentials._quota_project_id == "project-foo"

        # Generate authorization grant:
        token = self.credentials._make_authorization_grant_assertion()
        payload = jwt.decode(token, verify=False)

        # The JWT token signature is 'signature' encoded in base 64:
        assert token.endswith(b".c2lnbmF0dXJl")

        # Check that the credentials have the token and proper expiration
        assert payload == {
            "aud": "https://www.googleapis.com/oauth2/v4/token",
            "exp": 3600,
            "iat": 0,
            "iss": "service-account@example.com",
            "target_audience": "https://audience.com",
        }

        # Check that the signer have been initialized with a Request object
        assert isinstance(self.credentials._signer._request, transport.Request)

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.utcfromtimestamp(0),
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    def test_with_token_uri(self, sign, get, utcnow):
        get.side_effect = [
            {"email": "service-account@example.com", "scopes": ["one", "two"]}
        ]
        sign.side_effect = [b"signature"]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request,
            target_audience="https://audience.com",
            token_uri="http://xyz.com",
        )
        assert self.credentials._token_uri == "http://xyz.com"
        creds_with_token_uri = self.credentials.with_token_uri("http://example.com")
        assert creds_with_token_uri._token_uri == "http://example.com"

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.utcfromtimestamp(0),
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    def test_with_token_uri_exception(self, sign, get, utcnow):
        get.side_effect = [
            {"email": "service-account@example.com", "scopes": ["one", "two"]}
        ]
        sign.side_effect = [b"signature"]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request,
            target_audience="https://audience.com",
            use_metadata_identity_endpoint=True,
        )
        assert self.credentials._token_uri is None
        with pytest.raises(ValueError):
            self.credentials.with_token_uri("http://example.com")

    @responses.activate
    def test_with_quota_project_integration(self):
        """Test that it is possible to refresh credentials
        generated from `with_quota_project`.

        Instead of mocking the methods, the HTTP responses
        have been mocked.
        """

        # mock information about credentials
        responses.add(
            responses.GET,
            "http://metadata.google.internal/computeMetadata/v1/instance/"
            "service-accounts/default/?recursive=true",
            status=200,
            content_type="application/json",
            json={
                "scopes": "email",
                "email": "service-account@example.com",
                "aliases": ["default"],
            },
        )

        # mock token for credentials
        responses.add(
            responses.GET,
            "http://metadata.google.internal/computeMetadata/v1/instance/"
            "service-accounts/default/token",
            status=200,
            content_type="application/json",
            json={
                "access_token": "some-token",
                "expires_in": 3210,
                "token_type": "Bearer",
            },
        )

        # stubby response about universe_domain
        responses.add(
            responses.GET,
            "http://metadata.google.internal/computeMetadata/v1/universe/"
            "universe-domain",
            status=200,
            content_type="application/json",
            json={},
        )

        # mock sign blob endpoint
        signature = base64.b64encode(b"some-signature").decode("utf-8")
        responses.add(
            responses.POST,
            "https://iamcredentials.googleapis.com/v1/projects/-/"
            "serviceAccounts/service-account@example.com:signBlob",
            status=200,
            content_type="application/json",
            json={"keyId": "some-key-id", "signedBlob": signature},
        )

        id_token = "{}.{}.{}".format(
            base64.b64encode(b'{"some":"some"}').decode("utf-8"),
            base64.b64encode(b'{"exp": 3210}').decode("utf-8"),
            base64.b64encode(b"token").decode("utf-8"),
        )

        # mock id token endpoint
        responses.add(
            responses.POST,
            "https://www.googleapis.com/oauth2/v4/token",
            status=200,
            content_type="application/json",
            json={"id_token": id_token, "expiry": 3210},
        )

        self.credentials = credentials.IDTokenCredentials(
            request=requests.Request(),
            service_account_email="service-account@example.com",
            target_audience="https://audience.com",
        )

        self.credentials = self.credentials.with_quota_project("project-foo")

        self.credentials.refresh(requests.Request())

        assert self.credentials.token is not None
        assert self.credentials._quota_project_id == "project-foo"

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.utcfromtimestamp(0),
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    @mock.patch("google.oauth2._client.id_token_jwt_grant", autospec=True)
    def test_refresh_success(self, id_token_jwt_grant, sign, get, utcnow):
        get.side_effect = [
            {"email": "service-account@example.com", "scopes": ["one", "two"]}
        ]
        sign.side_effect = [b"signature"]
        id_token_jwt_grant.side_effect = [
            ("idtoken", datetime.datetime.utcfromtimestamp(3600), {})
        ]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com"
        )

        # Refresh credentials
        self.credentials.refresh(None)

        # Check that the credentials have the token and proper expiration
        assert self.credentials.token == "idtoken"
        assert self.credentials.expiry == (datetime.datetime.utcfromtimestamp(3600))

        # Check the credential info
        assert self.credentials.service_account_email == "service-account@example.com"

        # Check that the credentials are valid (have a token and are not
        # expired)
        assert self.credentials.valid

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.utcfromtimestamp(0),
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    def test_refresh_error(self, sign, get, utcnow):
        get.side_effect = [
            {"email": "service-account@example.com", "scopes": ["one", "two"]}
        ]
        sign.side_effect = [b"signature"]

        request = mock.create_autospec(transport.Request, instance=True)
        response = mock.Mock()
        response.data = b'{"error": "http error"}'
        response.status = 404  # Throw a 404 so the request is not retried.
        request.side_effect = [response]

        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com"
        )

        with pytest.raises(exceptions.RefreshError) as excinfo:
            self.credentials.refresh(request)

        assert excinfo.match(r"http error")

    @mock.patch(
        "google.auth._helpers.utcnow",
        return_value=datetime.datetime.utcfromtimestamp(0),
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    @mock.patch("google.oauth2._client.id_token_jwt_grant", autospec=True)
    def test_before_request_refreshes(self, id_token_jwt_grant, sign, get, utcnow):
        get.side_effect = [
            {"email": "service-account@example.com", "scopes": "one two"}
        ]
        sign.side_effect = [b"signature"]
        id_token_jwt_grant.side_effect = [
            ("idtoken", datetime.datetime.utcfromtimestamp(3600), {})
        ]

        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com"
        )

        # Credentials should start as invalid
        assert not self.credentials.valid

        # before_request should cause a refresh
        request = mock.create_autospec(transport.Request, instance=True)
        self.credentials.before_request(request, "GET", "http://example.com?a=1#3", {})

        # The refresh endpoint should've been called.
        assert get.called

        # Credentials should now be valid.
        assert self.credentials.valid

    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    @mock.patch("google.auth.iam.Signer.sign", autospec=True)
    def test_sign_bytes(self, sign, get):
        get.side_effect = [
            {"email": "service-account@example.com", "scopes": ["one", "two"]}
        ]
        sign.side_effect = [b"signature"]

        request = mock.create_autospec(transport.Request, instance=True)
        response = mock.Mock()
        response.data = b'{"signature": "c2lnbmF0dXJl"}'
        response.status = 200
        request.side_effect = [response]

        self.credentials = credentials.IDTokenCredentials(
            request=request, target_audience="https://audience.com"
        )

        # Generate authorization grant:
        signature = self.credentials.sign_bytes(b"some bytes")

        # The JWT token signature is 'signature' encoded in base 64:
        assert signature == b"signature"

    @mock.patch(
        "google.auth.metrics.token_request_id_token_mds",
        return_value=ID_TOKEN_REQUEST_METRICS_HEADER_VALUE,
    )
    @mock.patch(
        "google.auth.compute_engine._metadata.get_service_account_info", autospec=True
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_get_id_token_from_metadata(
        self, get, get_service_account_info, mock_metrics_header_value
    ):
        get.return_value = SAMPLE_ID_TOKEN
        get_service_account_info.return_value = {"email": "foo@example.com"}

        cred = credentials.IDTokenCredentials(
            mock.Mock(), "audience", use_metadata_identity_endpoint=True
        )
        cred.refresh(request=mock.Mock())

        assert get.call_args.kwargs["headers"] == {
            "x-goog-api-client": ID_TOKEN_REQUEST_METRICS_HEADER_VALUE
        }

        assert cred.token == SAMPLE_ID_TOKEN
        assert cred.expiry == datetime.datetime.utcfromtimestamp(SAMPLE_ID_TOKEN_EXP)
        assert cred._use_metadata_identity_endpoint
        assert cred._signer is None
        assert cred._token_uri is None
        assert cred._service_account_email == "foo@example.com"
        assert cred._target_audience == "audience"
        with pytest.raises(ValueError):
            cred.sign_bytes(b"bytes")

    @mock.patch(
        "google.auth.compute_engine._metadata.get_service_account_info", autospec=True
    )
    def test_with_target_audience_for_metadata(self, get_service_account_info):
        get_service_account_info.return_value = {"email": "foo@example.com"}

        cred = credentials.IDTokenCredentials(
            mock.Mock(), "audience", use_metadata_identity_endpoint=True
        )
        cred = cred.with_target_audience("new_audience")

        assert cred._target_audience == "new_audience"
        assert cred._use_metadata_identity_endpoint
        assert cred._signer is None
        assert cred._token_uri is None
        assert cred._service_account_email == "foo@example.com"

    @mock.patch(
        "google.auth.compute_engine._metadata.get_service_account_info", autospec=True
    )
    def test_id_token_with_quota_project(self, get_service_account_info):
        get_service_account_info.return_value = {"email": "foo@example.com"}

        cred = credentials.IDTokenCredentials(
            mock.Mock(), "audience", use_metadata_identity_endpoint=True
        )
        cred = cred.with_quota_project("project-foo")

        assert cred._quota_project_id == "project-foo"
        assert cred._use_metadata_identity_endpoint
        assert cred._signer is None
        assert cred._token_uri is None
        assert cred._service_account_email == "foo@example.com"

    @mock.patch(
        "google.auth.compute_engine._metadata.get_service_account_info", autospec=True
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_invalid_id_token_from_metadata(self, get, get_service_account_info):
        get.return_value = "invalid_id_token"
        get_service_account_info.return_value = {"email": "foo@example.com"}

        cred = credentials.IDTokenCredentials(
            mock.Mock(), "audience", use_metadata_identity_endpoint=True
        )

        with pytest.raises(ValueError):
            cred.refresh(request=mock.Mock())

    @mock.patch(
        "google.auth.compute_engine._metadata.get_service_account_info", autospec=True
    )
    @mock.patch("google.auth.compute_engine._metadata.get", autospec=True)
    def test_transport_error_from_metadata(self, get, get_service_account_info):
        get.side_effect = exceptions.TransportError("transport error")
        get_service_account_info.return_value = {"email": "foo@example.com"}

        cred = credentials.IDTokenCredentials(
            mock.Mock(), "audience", use_metadata_identity_endpoint=True
        )

        with pytest.raises(exceptions.RefreshError) as excinfo:
            cred.refresh(request=mock.Mock())
        assert excinfo.match(r"transport error")

    def test_get_id_token_from_metadata_constructor(self):
        with pytest.raises(ValueError):
            credentials.IDTokenCredentials(
                mock.Mock(),
                "audience",
                use_metadata_identity_endpoint=True,
                token_uri="token_uri",
            )
        with pytest.raises(ValueError):
            credentials.IDTokenCredentials(
                mock.Mock(),
                "audience",
                use_metadata_identity_endpoint=True,
                signer=mock.Mock(),
            )
        with pytest.raises(ValueError):
            credentials.IDTokenCredentials(
                mock.Mock(),
                "audience",
                use_metadata_identity_endpoint=True,
                additional_claims={"key", "value"},
            )
        with pytest.raises(ValueError):
            credentials.IDTokenCredentials(
                mock.Mock(),
                "audience",
                use_metadata_identity_endpoint=True,
                service_account_email="foo@example.com",
            )
