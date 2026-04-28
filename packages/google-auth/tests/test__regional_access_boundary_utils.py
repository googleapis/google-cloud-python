# Copyright 2026 Google Inc.
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
from unittest import mock

import pytest  # type: ignore

from google.auth import _helpers
from google.auth import _regional_access_boundary_utils
from google.auth import credentials
from google.auth import environment_vars


class CredentialsImpl(credentials.CredentialsWithRegionalAccessBoundary):
    def __init__(self, universe_domain=None):
        super(CredentialsImpl, self).__init__()
        if universe_domain:
            self._universe_domain = universe_domain

    def _perform_refresh_token(self, request):
        self.token = "refreshed-token"
        self.expiry = (
            datetime.datetime.utcnow()
            + _helpers.REFRESH_THRESHOLD
            + datetime.timedelta(seconds=5)
        )

    def with_quota_project(self, quota_project_id):
        raise NotImplementedError()

    def _build_regional_access_boundary_lookup_url(self):
        # Using self.token here to make the URL dynamic for testing purposes
        return "http://mock.url/lookup_for_{}".format(self.token)

    def _make_copy(self):
        new_credentials = self.__class__()
        self._copy_regional_access_boundary_manager(new_credentials)
        return new_credentials


@pytest.fixture(autouse=True)
def clear_rab_cache():
    """Clears the Regional Access Boundary enablement cache before every test."""
    _regional_access_boundary_utils.is_regional_access_boundary_enabled.cache_clear()


class TestCredentialsWithRegionalAccessBoundary(object):
    def test_is_regional_access_boundary_enabled_cached(self, monkeypatch):
        # Set to true
        monkeypatch.setenv(environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED, "true")
        assert (
            _regional_access_boundary_utils.is_regional_access_boundary_enabled()
            is True
        )

        # Change env var to false, but it should still return True due to caching
        monkeypatch.setenv(environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED, "false")
        assert (
            _regional_access_boundary_utils.is_regional_access_boundary_enabled()
            is True
        )

        # Clear cache and it should now reflect the new value
        _regional_access_boundary_utils.is_regional_access_boundary_enabled.cache_clear()
        assert (
            _regional_access_boundary_utils.is_regional_access_boundary_enabled()
            is False
        )

    @mock.patch(
        "google.auth._regional_access_boundary_utils._RegionalAccessBoundaryRefreshManager.start_refresh"
    )
    def test_maybe_start_refresh_is_skipped_if_env_var_not_set(
        self, mock_start_refresh
    ):
        creds = CredentialsImpl()
        with mock.patch.dict(os.environ, clear=True):
            creds._maybe_start_regional_access_boundary_refresh(
                mock.Mock(), "http://example.com"
            )
        mock_start_refresh.assert_not_called()

    @mock.patch(
        "google.auth._regional_access_boundary_utils._RegionalAccessBoundaryRefreshManager.start_refresh"
    )
    def test_maybe_start_refresh_is_skipped_if_not_expired(self, mock_start_refresh):
        creds = CredentialsImpl()
        creds._rab_manager._data = _regional_access_boundary_utils._RegionalAccessBoundaryData(
            encoded_locations="0xABC",
            expiry=_helpers.utcnow() + datetime.timedelta(hours=2),
            cooldown_expiry=None,
            cooldown_duration=_regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
        )
        with mock.patch.dict(
            os.environ,
            {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"},
        ):
            creds._maybe_start_regional_access_boundary_refresh(
                mock.Mock(), "http://example.com"
            )
        mock_start_refresh.assert_not_called()

    @mock.patch(
        "google.auth._regional_access_boundary_utils._RegionalAccessBoundaryRefreshManager.start_refresh"
    )
    def test_maybe_start_refresh_triggered_if_soft_expired(self, mock_start_refresh):
        creds = CredentialsImpl()
        creds._rab_manager._data = _regional_access_boundary_utils._RegionalAccessBoundaryData(
            encoded_locations="0xABC",
            expiry=_helpers.utcnow() + datetime.timedelta(minutes=30),
            cooldown_expiry=None,
            cooldown_duration=_regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
        )
        request = mock.Mock()
        with mock.patch.dict(
            os.environ,
            {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"},
        ):
            creds._maybe_start_regional_access_boundary_refresh(
                request, "http://example.com"
            )
        mock_start_refresh.assert_called_once_with(creds, request, creds._rab_manager)

    @mock.patch(
        "google.auth._regional_access_boundary_utils._RegionalAccessBoundaryRefreshManager.start_refresh"
    )
    def test_maybe_start_refresh_is_skipped_if_cooldown_active(
        self, mock_start_refresh
    ):
        creds = CredentialsImpl()
        creds._rab_manager._data = _regional_access_boundary_utils._RegionalAccessBoundaryData(
            encoded_locations=None,
            expiry=None,
            cooldown_expiry=_helpers.utcnow() + datetime.timedelta(minutes=5),
            cooldown_duration=_regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
        )
        with mock.patch.dict(
            os.environ,
            {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"},
        ):
            creds._maybe_start_regional_access_boundary_refresh(
                mock.Mock(), "http://example.com"
            )
        mock_start_refresh.assert_not_called()

    @mock.patch(
        "google.auth._regional_access_boundary_utils._RegionalAccessBoundaryRefreshManager.start_refresh"
    )
    def test_maybe_start_refresh_is_skipped_for_regional_endpoint(
        self, mock_start_refresh
    ):
        creds = CredentialsImpl()
        with mock.patch.dict(
            os.environ,
            {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"},
        ):
            creds._maybe_start_regional_access_boundary_refresh(
                mock.Mock(), "https://my-service.us-east1.rep.googleapis.com"
            )
        mock_start_refresh.assert_not_called()

    @mock.patch(
        "google.auth._regional_access_boundary_utils._RegionalAccessBoundaryRefreshManager.start_refresh"
    )
    def test_maybe_start_refresh_is_triggered(self, mock_start_refresh):
        creds = CredentialsImpl()
        request = mock.Mock()
        with mock.patch.dict(
            os.environ,
            {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"},
        ):
            creds._maybe_start_regional_access_boundary_refresh(
                request, "http://example.com"
            )
        mock_start_refresh.assert_called_once_with(creds, request, creds._rab_manager)

    def test_apply_headers_success(self):
        creds = CredentialsImpl()
        creds._rab_manager._data = _regional_access_boundary_utils._RegionalAccessBoundaryData(
            encoded_locations="0xABC",
            expiry=_helpers.utcnow() + datetime.timedelta(hours=1),
            cooldown_expiry=None,
            cooldown_duration=_regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
        )
        headers = {}
        creds._rab_manager.apply_headers(headers)
        assert headers == {"x-allowed-locations": "0xABC"}

    def test_apply_headers_removes_header_if_none(self):
        creds = CredentialsImpl()
        creds._rab_manager._data = _regional_access_boundary_utils._RegionalAccessBoundaryData(
            encoded_locations=None,
            expiry=_helpers.utcnow() + datetime.timedelta(hours=1),
            cooldown_expiry=None,
            cooldown_duration=_regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
        )
        headers = {"x-allowed-locations": "0xABC"}
        creds._rab_manager.apply_headers(headers)
        assert headers == {}

    def test_apply_headers_removes_header_if_empty(self):
        creds = CredentialsImpl()
        creds._rab_manager._data = _regional_access_boundary_utils._RegionalAccessBoundaryData(
            encoded_locations="",
            expiry=_helpers.utcnow() + datetime.timedelta(hours=1),
            cooldown_expiry=None,
            cooldown_duration=_regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
        )
        headers = {"x-allowed-locations": "0xABC"}
        creds._rab_manager.apply_headers(headers)
        assert headers == {}

    def test_copy_regional_access_boundary_state(self):
        source_creds = CredentialsImpl()
        snapshot = _regional_access_boundary_utils._RegionalAccessBoundaryData(
            encoded_locations="0xABC",
            expiry=_helpers.utcnow(),
            cooldown_expiry=_helpers.utcnow(),
            cooldown_duration=_regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
        )
        source_creds._rab_manager._data = snapshot

        target_creds = CredentialsImpl()
        source_creds._copy_regional_access_boundary_manager(target_creds)

        assert target_creds._rab_manager is not source_creds._rab_manager
        assert target_creds._rab_manager._data is source_creds._rab_manager._data

    def test_serialization(self):
        import pickle

        manager = _regional_access_boundary_utils._RegionalAccessBoundaryManager()
        manager._data = _regional_access_boundary_utils._RegionalAccessBoundaryData(
            encoded_locations="0xABC",
            expiry=_helpers.utcnow(),
            cooldown_expiry=_helpers.utcnow(),
            cooldown_duration=_regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
        )

        pickled = pickle.dumps(manager)
        unpickled = pickle.loads(pickled)

        assert unpickled._data == manager._data
        assert unpickled._update_lock is not None
        assert unpickled.refresh_manager._lock is not None
        assert unpickled.refresh_manager._worker is None

    @mock.patch(
        "google.auth._regional_access_boundary_utils._RegionalAccessBoundaryRefreshManager.start_refresh"
    )
    def test_maybe_start_refresh_is_skipped_if_non_default_universe_domain(
        self, mock_start_refresh
    ):
        creds = CredentialsImpl(universe_domain="not.googleapis.com")
        with mock.patch.dict(
            os.environ,
            {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"},
        ):
            creds._maybe_start_regional_access_boundary_refresh(
                mock.Mock(), "http://example.com"
            )
        mock_start_refresh.assert_not_called()

    @mock.patch(
        "google.auth._regional_access_boundary_utils._RegionalAccessBoundaryRefreshManager.start_refresh"
    )
    @mock.patch("urllib.parse.urlparse")
    def test_maybe_start_refresh_handles_url_parse_errors(
        self, mock_urlparse, mock_start_refresh
    ):
        mock_urlparse.side_effect = ValueError("Malformed URL")
        creds = CredentialsImpl()
        request = mock.Mock()
        with mock.patch.dict(
            os.environ,
            {environment_vars.GOOGLE_AUTH_TRUST_BOUNDARY_ENABLED: "true"},
        ):
            creds._maybe_start_regional_access_boundary_refresh(
                request, "http://malformed-url"
            )
        mock_start_refresh.assert_called_once_with(creds, request, creds._rab_manager)

    @mock.patch("google.oauth2._client._lookup_regional_access_boundary")
    @mock.patch.object(CredentialsImpl, "_build_regional_access_boundary_lookup_url")
    def test_lookup_regional_access_boundary_success(
        self, mock_build_url, mock_lookup_rab
    ):
        creds = CredentialsImpl()
        creds.token = "token"
        request = mock.Mock()
        mock_build_url.return_value = "http://rab.example.com"
        mock_lookup_rab.return_value = {"encodedLocations": "success"}

        result = creds._lookup_regional_access_boundary(request)

        mock_build_url.assert_called_once()
        mock_lookup_rab.assert_called_once_with(
            request, "http://rab.example.com", headers={"authorization": "Bearer token"}
        )
        assert result == {"encodedLocations": "success"}

    @mock.patch("google.oauth2._client._lookup_regional_access_boundary")
    @mock.patch.object(CredentialsImpl, "_build_regional_access_boundary_lookup_url")
    def test_lookup_regional_access_boundary_failure(
        self, mock_build_url, mock_lookup_rab
    ):
        creds = CredentialsImpl()
        creds.token = "token"
        request = mock.Mock()
        mock_build_url.return_value = "http://rab.example.com"
        mock_lookup_rab.return_value = None

        result = creds._lookup_regional_access_boundary(request)

        mock_build_url.assert_called_once()
        mock_lookup_rab.assert_called_once_with(
            request, "http://rab.example.com", headers={"authorization": "Bearer token"}
        )
        assert result is None

    @mock.patch("google.oauth2._client._lookup_regional_access_boundary")
    @mock.patch.object(CredentialsImpl, "_build_regional_access_boundary_lookup_url")
    def test_lookup_regional_access_boundary_null_url(
        self, mock_build_url, mock_lookup_rab
    ):
        creds = CredentialsImpl()
        creds.token = "token"
        request = mock.Mock()
        mock_build_url.return_value = None

        result = creds._lookup_regional_access_boundary(request)

        mock_build_url.assert_called_once()
        mock_lookup_rab.assert_not_called()
        assert result is None

    def test_credentials_with_regional_access_boundary_initialization(self):
        creds = CredentialsImpl()
        assert creds._rab_manager._data.encoded_locations is None
        assert creds._rab_manager._data.expiry is None
        assert creds._rab_manager._data.cooldown_expiry is None
        assert creds._rab_manager._data.cooldown_duration == (
            credentials._regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN
        )
        assert creds._rab_manager._update_lock is not None

    @mock.patch("google.auth._helpers.utcnow")
    def test_regional_access_boundary_refresh_thread_run_success(self, mock_utcnow):
        mock_now = datetime.datetime(2025, 1, 1, 12, 0, 0)
        mock_utcnow.return_value = mock_now

        creds = mock.Mock()
        request = mock.Mock()
        rab_manager = _regional_access_boundary_utils._RegionalAccessBoundaryManager()

        creds._lookup_regional_access_boundary.return_value = {
            "locations": ["us-east1"],
            "encodedLocations": "0xABC123",
        }

        worker = _regional_access_boundary_utils._RegionalAccessBoundaryRefreshThread(
            creds, request, rab_manager
        )
        worker.run()

        assert rab_manager._data.encoded_locations == "0xABC123"
        expected_expiry = (
            mock_now
            + _regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_TTL
        )
        assert rab_manager._data.expiry == expected_expiry
        assert rab_manager._data.cooldown_expiry is None

    @mock.patch("google.auth._helpers.utcnow")
    def test_regional_access_boundary_refresh_thread_run_failure(self, mock_utcnow):
        mock_now = datetime.datetime(2025, 1, 1, 12, 0, 0)
        mock_utcnow.return_value = mock_now

        creds = mock.Mock()
        request = mock.Mock()
        rab_manager = _regional_access_boundary_utils._RegionalAccessBoundaryManager()

        initial_cooldown = rab_manager._data.cooldown_duration

        creds._lookup_regional_access_boundary.side_effect = Exception(
            "Network failure"
        )

        worker = _regional_access_boundary_utils._RegionalAccessBoundaryRefreshThread(
            creds, request, rab_manager
        )
        worker.run()

        assert rab_manager._data.encoded_locations is None
        assert rab_manager._data.expiry is None
        expected_cooldown_expiry = mock_now + initial_cooldown
        assert rab_manager._data.cooldown_expiry == expected_cooldown_expiry
        assert rab_manager._data.cooldown_duration == initial_cooldown * 2

    @mock.patch("google.auth._helpers.utcnow")
    def test_regional_access_boundary_refresh_thread_run_failure_hard_expiry(
        self, mock_utcnow
    ):
        mock_now = datetime.datetime(2025, 1, 1, 12, 0, 0)
        mock_utcnow.return_value = mock_now

        creds = mock.Mock()
        request = mock.Mock()
        rab_manager = _regional_access_boundary_utils._RegionalAccessBoundaryManager()

        # Simulate existing data that has hard expired
        rab_manager._data = _regional_access_boundary_utils._RegionalAccessBoundaryData(
            encoded_locations="0xExpiredToken",
            expiry=mock_now - datetime.timedelta(hours=1),
            cooldown_expiry=None,
            cooldown_duration=_regional_access_boundary_utils.DEFAULT_REGIONAL_ACCESS_BOUNDARY_COOLDOWN,
        )

        creds._lookup_regional_access_boundary.side_effect = Exception(
            "Network failure"
        )

        worker = _regional_access_boundary_utils._RegionalAccessBoundaryRefreshThread(
            creds, request, rab_manager
        )
        worker.run()

        # Assert data was aggressively cleared rather than reused due to total expiration
        assert rab_manager._data.encoded_locations is None
        assert rab_manager._data.expiry is None
        assert rab_manager._data.cooldown_expiry is not None

    def test_regional_access_boundary_refresh_manager_start_refresh_safety_lock(self):
        manager = (
            _regional_access_boundary_utils._RegionalAccessBoundaryRefreshManager()
        )
        creds = mock.Mock()
        request = mock.Mock()
        rab_manager = mock.Mock()

        mock_worker = mock.Mock()
        mock_worker.is_alive.return_value = True
        manager._worker = mock_worker

        with mock.patch(
            "google.auth._regional_access_boundary_utils._RegionalAccessBoundaryRefreshThread"
        ) as mock_thread_class:
            manager.start_refresh(creds, request, rab_manager)

            mock_thread_class.assert_not_called()
            assert manager._worker == mock_worker
