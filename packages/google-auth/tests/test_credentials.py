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
import os

import mock
import pytest  # type: ignore

from google.auth import _helpers
from google.auth import credentials
from google.auth import environment_vars
from google.auth import exceptions
from google.oauth2 import _client


class CredentialsImpl(credentials.CredentialsWithTrustBoundary):
    def _refresh_token(self, request):
        self.token = "refreshed-token"
        self.expiry = (
            datetime.datetime.utcnow()
            + _helpers.REFRESH_THRESHOLD
            + datetime.timedelta(seconds=5)
        )

    def with_quota_project(self, quota_project_id):
        raise NotImplementedError()

    def _build_trust_boundary_lookup_url(self):
        # Using self.token here to make the URL dynamic for testing purposes
        return "http://mock.url/lookup_for_{}".format(self.token)


class CredentialsImplWithMetrics(credentials.Credentials):
    def refresh(self, request):
        self.token = request

    def _metric_header_for_usage(self):
        return "foo"


def test_credentials_constructor():
    credentials = CredentialsImpl()
    assert not credentials.token
    assert not credentials.expiry
    assert not credentials.expired
    assert not credentials.valid
    assert credentials.universe_domain == "googleapis.com"
    assert not credentials._use_non_blocking_refresh


def test_credentials_get_cred_info():
    credentials = CredentialsImpl()
    assert not credentials.get_cred_info()


def test_with_non_blocking_refresh():
    c = CredentialsImpl()
    c.with_non_blocking_refresh()
    assert c._use_non_blocking_refresh


def test_expired_and_valid():
    credentials = CredentialsImpl()
    credentials.token = "token"

    assert credentials.valid
    assert not credentials.expired

    # Set the expiration to one second more than now plus the clock skew
    # accomodation. These credentials should be valid.
    credentials.expiry = (
        _helpers.utcnow() + _helpers.REFRESH_THRESHOLD + datetime.timedelta(seconds=1)
    )

    assert credentials.valid
    assert not credentials.expired

    # Set the credentials expiration to now. Because of the clock skew
    # accomodation, these credentials should report as expired.
    credentials.expiry = _helpers.utcnow()

    assert not credentials.valid
    assert credentials.expired


def test_before_request():
    credentials = CredentialsImpl()
    request = mock.Mock()
    headers = {}

    # First call should call refresh, setting the token.
    credentials.before_request(request, "http://example.com", "GET", headers)
    assert credentials.valid
    assert credentials.token == "refreshed-token"
    assert headers["authorization"] == "Bearer refreshed-token"
    assert "x-allowed-locations" not in headers

    request = mock.Mock()
    headers = {}

    # Second call shouldn't call refresh.
    credentials.before_request(request, "http://example.com", "GET", headers)
    assert credentials.valid
    assert credentials.token == "refreshed-token"
    assert headers["authorization"] == "Bearer refreshed-token"
    assert "x-allowed-locations" not in headers


def test_before_request_with_trust_boundary():
    DUMMY_BOUNDARY = "0xA30"
    credentials = CredentialsImpl()
    credentials._trust_boundary = {"locations": [], "encodedLocations": DUMMY_BOUNDARY}
    request = mock.Mock()
    headers = {}

    # First call should call refresh, setting the token.
    credentials.before_request(request, "http://example.com", "GET", headers)
    assert credentials.valid
    assert credentials.token == "refreshed-token"
    assert headers["authorization"] == "Bearer refreshed-token"
    assert headers["x-allowed-locations"] == DUMMY_BOUNDARY

    request = mock.Mock()
    headers = {}

    # Second call shouldn't call refresh.
    credentials.before_request(request, "http://example.com", "GET", headers)
    assert credentials.valid
    assert credentials.token == "refreshed-token"
    assert headers["authorization"] == "Bearer refreshed-token"
    assert headers["x-allowed-locations"] == DUMMY_BOUNDARY


def test_before_request_metrics():
    credentials = CredentialsImplWithMetrics()
    request = "token"
    headers = {}

    credentials.before_request(request, "http://example.com", "GET", headers)
    assert headers["x-goog-api-client"] == "foo"


def test_anonymous_credentials_ctor():
    anon = credentials.AnonymousCredentials()
    assert anon.token is None
    assert anon.expiry is None
    assert not anon.expired
    assert anon.valid


def test_anonymous_credentials_refresh():
    anon = credentials.AnonymousCredentials()
    request = object()
    with pytest.raises(ValueError):
        anon.refresh(request)


def test_anonymous_credentials_apply_default():
    anon = credentials.AnonymousCredentials()
    headers = {}
    anon.apply(headers)
    assert headers == {}
    with pytest.raises(ValueError):
        anon.apply(headers, token="TOKEN")


def test_anonymous_credentials_before_request():
    anon = credentials.AnonymousCredentials()
    request = object()
    method = "GET"
    url = "https://example.com/api/endpoint"
    headers = {}
    anon.before_request(request, method, url, headers)
    assert headers == {}


class ReadOnlyScopedCredentialsImpl(credentials.ReadOnlyScoped, CredentialsImpl):
    @property
    def requires_scopes(self):
        return super(ReadOnlyScopedCredentialsImpl, self).requires_scopes


def test_readonly_scoped_credentials_constructor():
    credentials = ReadOnlyScopedCredentialsImpl()
    assert credentials._scopes is None


def test_readonly_scoped_credentials_scopes():
    credentials = ReadOnlyScopedCredentialsImpl()
    credentials._scopes = ["one", "two"]
    assert credentials.scopes == ["one", "two"]
    assert credentials.has_scopes(["one"])
    assert credentials.has_scopes(["two"])
    assert credentials.has_scopes(["one", "two"])
    assert not credentials.has_scopes(["three"])

    # Test with default scopes
    credentials_with_default = ReadOnlyScopedCredentialsImpl()
    credentials_with_default._default_scopes = ["one", "two"]
    assert credentials_with_default.has_scopes(["one", "two"])
    assert not credentials_with_default.has_scopes(["three"])

    # Test with no scopes
    credentials_no_scopes = ReadOnlyScopedCredentialsImpl()
    assert not credentials_no_scopes.has_scopes(["one"])

    assert credentials_no_scopes.has_scopes([])


def test_readonly_scoped_credentials_requires_scopes():
    credentials = ReadOnlyScopedCredentialsImpl()
    assert not credentials.requires_scopes


class RequiresScopedCredentialsImpl(credentials.Scoped, CredentialsImpl):
    def __init__(self, scopes=None, default_scopes=None):
        super(RequiresScopedCredentialsImpl, self).__init__()
        self._scopes = scopes
        self._default_scopes = default_scopes

    @property
    def requires_scopes(self):
        return not self.scopes

    def with_scopes(self, scopes, default_scopes=None):
        return RequiresScopedCredentialsImpl(
            scopes=scopes, default_scopes=default_scopes
        )


def test_create_scoped_if_required_scoped():
    unscoped_credentials = RequiresScopedCredentialsImpl()
    scoped_credentials = credentials.with_scopes_if_required(
        unscoped_credentials, ["one", "two"]
    )

    assert scoped_credentials is not unscoped_credentials
    assert not scoped_credentials.requires_scopes
    assert scoped_credentials.has_scopes(["one", "two"])


def test_create_scoped_if_required_not_scopes():
    unscoped_credentials = CredentialsImpl()
    scoped_credentials = credentials.with_scopes_if_required(
        unscoped_credentials, ["one", "two"]
    )

    assert scoped_credentials is unscoped_credentials


def test_nonblocking_refresh_fresh_credentials():
    c = CredentialsImpl()

    c._refresh_worker = mock.MagicMock()

    request = mock.Mock()

    c.refresh(request)
    assert c.token_state == credentials.TokenState.FRESH

    c.with_non_blocking_refresh()
    c.before_request(request, "http://example.com", "GET", {})


def test_nonblocking_refresh_invalid_credentials():
    c = CredentialsImpl()
    c.with_non_blocking_refresh()

    request = mock.Mock()
    headers = {}

    assert c.token_state == credentials.TokenState.INVALID

    c.before_request(request, "http://example.com", "GET", headers)
    assert c.token_state == credentials.TokenState.FRESH
    assert c.valid
    assert c.token == "refreshed-token"
    assert headers["authorization"] == "Bearer refreshed-token"
    assert "x-identity-trust-boundary" not in headers


def test_nonblocking_refresh_stale_credentials():
    c = CredentialsImpl()
    c.with_non_blocking_refresh()

    request = mock.Mock()
    headers = {}

    # Invalid credentials MUST require a blocking refresh.
    c.before_request(request, "http://example.com", "GET", headers)
    assert c.token_state == credentials.TokenState.FRESH
    assert not c._refresh_worker._worker

    c.expiry = (
        datetime.datetime.utcnow()
        + _helpers.REFRESH_THRESHOLD
        - datetime.timedelta(seconds=1)
    )

    # STALE credentials SHOULD spawn a non-blocking worker
    assert c.token_state == credentials.TokenState.STALE
    c.before_request(request, "http://example.com", "GET", headers)
    assert c._refresh_worker._worker is not None

    assert c.token_state == credentials.TokenState.FRESH
    assert c.valid
    assert c.token == "refreshed-token"
    assert headers["authorization"] == "Bearer refreshed-token"
    assert "x-identity-trust-boundary" not in headers


def test_nonblocking_refresh_failed_credentials():
    c = CredentialsImpl()
    c.with_non_blocking_refresh()

    request = mock.Mock()
    headers = {}

    # Invalid credentials MUST require a blocking refresh.
    c.before_request(request, "http://example.com", "GET", headers)
    assert c.token_state == credentials.TokenState.FRESH
    assert not c._refresh_worker._worker

    c.expiry = (
        datetime.datetime.utcnow()
        + _helpers.REFRESH_THRESHOLD
        - datetime.timedelta(seconds=1)
    )

    # STALE credentials SHOULD spawn a non-blocking worker
    assert c.token_state == credentials.TokenState.STALE
    c._refresh_worker._worker = mock.MagicMock()
    c._refresh_worker._worker._error_info = "Some Error"
    c.before_request(request, "http://example.com", "GET", headers)
    assert c._refresh_worker._worker is not None

    assert c.token_state == credentials.TokenState.FRESH
    assert c.valid
    assert c.token == "refreshed-token"
    assert headers["authorization"] == "Bearer refreshed-token"
    assert "x-identity-trust-boundary" not in headers


def test_token_state_no_expiry():
    c = CredentialsImpl()

    request = mock.Mock()
    c.refresh(request)

    c.expiry = None
    assert c.token_state == credentials.TokenState.FRESH

    c.before_request(request, "http://example.com", "GET", {})


class TestCredentialsWithTrustBoundary(object):
    @mock.patch.object(_client, "_lookup_trust_boundary")
    def test_lookup_trust_boundary_env_var_not_true(self, mock_lookup_tb):
        creds = CredentialsImpl()
        request = mock.Mock()

        # Ensure env var is not "true"
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "false"}
        ):
            result = creds._refresh_trust_boundary(request)

        assert result is None
        mock_lookup_tb.assert_not_called()

    @mock.patch.object(_client, "_lookup_trust_boundary")
    def test_lookup_trust_boundary_env_var_missing(self, mock_lookup_tb):
        creds = CredentialsImpl()
        request = mock.Mock()

        # Ensure env var is missing
        with mock.patch.dict(os.environ, clear=True):
            result = creds._refresh_trust_boundary(request)

        assert result is None
        mock_lookup_tb.assert_not_called()

    @mock.patch.object(_client, "_lookup_trust_boundary")
    def test_lookup_trust_boundary_non_default_universe(self, mock_lookup_tb):
        creds = CredentialsImpl()
        creds._universe_domain = "my.universe.com"  # Non-GDU
        request = mock.Mock()

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"}
        ):
            result = creds._refresh_trust_boundary(request)

        assert result is None
        mock_lookup_tb.assert_not_called()

    @mock.patch.object(_client, "_lookup_trust_boundary")
    def test_lookup_trust_boundary_calls_client_and_build_url(self, mock_lookup_tb):
        creds = CredentialsImpl()
        creds.token = "test_token"  # For _build_trust_boundary_lookup_url
        request = mock.Mock()
        expected_url = "http://mock.url/lookup_for_test_token"
        expected_boundary_info = {"encodedLocations": "0xABC"}
        mock_lookup_tb.return_value = expected_boundary_info

        # Mock _build_trust_boundary_lookup_url to ensure it's called.
        mock_build_url = mock.Mock(return_value=expected_url)
        creds._build_trust_boundary_lookup_url = mock_build_url

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"}
        ):
            result = creds._lookup_trust_boundary(request)

        assert result == expected_boundary_info
        mock_build_url.assert_called_once()
        expected_headers = {"authorization": "Bearer test_token"}
        mock_lookup_tb.assert_called_once_with(
            request, expected_url, headers=expected_headers
        )

    @mock.patch.object(_client, "_lookup_trust_boundary")
    def test_lookup_trust_boundary_build_url_returns_none(self, mock_lookup_tb):
        creds = CredentialsImpl()
        request = mock.Mock()

        # Mock _build_trust_boundary_lookup_url to return None
        mock_build_url = mock.Mock(return_value=None)
        creds._build_trust_boundary_lookup_url = mock_build_url

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"}
        ):
            with pytest.raises(
                exceptions.InvalidValue,
                match="Failed to build trust boundary lookup URL.",
            ):
                creds._lookup_trust_boundary(request)

        mock_build_url.assert_called_once()  # Ensure _build_trust_boundary_lookup_url was called
        mock_lookup_tb.assert_not_called()  # Ensure _client.lookup_trust_boundary was not called

    @mock.patch("google.auth.credentials._LOGGER")
    @mock.patch("google.auth._helpers.is_logging_enabled", return_value=True)
    @mock.patch.object(_client, "_lookup_trust_boundary")
    def test_refresh_trust_boundary_fails_with_cached_data_and_logging(
        self, mock_lookup_tb, mock_is_logging_enabled, mock_logger
    ):
        creds = CredentialsImpl()
        creds._trust_boundary = {"encodedLocations": "0xABC"}
        request = mock.Mock()

        refresh_error = exceptions.RefreshError("Lookup failed")
        mock_lookup_tb.side_effect = refresh_error

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"}
        ):
            creds.refresh(request)

        mock_lookup_tb.assert_called_once()
        mock_is_logging_enabled.assert_called_once_with(mock_logger)
        mock_logger.debug.assert_called_once_with(
            "Using cached trust boundary due to refresh error: %s", refresh_error
        )
