# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from collections.abc import Iterator
import inspect
import types
from typing import Any
from unittest import mock
from urllib.parse import urlparse

import pytest
import requests

import google.api_core.client_options as client_options_lib
from google.api_core.universe import EmptyUniverseError, UniverseMismatchError
import google.auth
from google.auth import credentials as auth_credentials
import google.auth.compute_engine
from google.auth.exceptions import MutualTLSChannelError
from google.cloud import _helpers
from google.cloud import _http
from google.cloud.client import (
    _CREDENTIALS_REFRESH_TIMEOUT,
    _validate_credentials_universe,
    Client,
    ClientWithProject,
)

DEFAULT_PROJECT_ID = "test-proj"
DEFAULT_UNIVERSE = "googleapis.com"
CUSTOM_UNIVERSE = "apis-tpclp.goog"


class _FakeCredentials(auth_credentials.Credentials):
    def __init__(self, universe_domain: str = DEFAULT_UNIVERSE) -> None:
        super().__init__()
        self._universe_domain = universe_domain
        self.token = "fake-token"

    @property
    def universe_domain(self) -> str:
        return self._universe_domain

    def refresh(self, request: Any) -> None:  # pragma: NO COVER
        pass


def _is_googleapis_url(url: str) -> bool:
    host = urlparse(url).hostname
    return bool(host and (host == "googleapis.com" or host.endswith(".googleapis.com")))


@pytest.fixture
def assert_no_googleapis_calls(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    def _guarded_send(self, request, *args, **kwargs):  # pragma: NO COVER
        if _is_googleapis_url(request.url):
            raise ConnectionRefusedError(
                f"Unexpected googleapis.com call: {request.url}"
            )
        resp = requests.Response()
        resp.status_code = 200
        resp._content = b"{}"
        resp.headers = {"content-type": "application/json"}
        resp.encoding = "utf-8"
        return resp

    monkeypatch.setattr(requests.Session, "send", _guarded_send)
    yield


class _MockServiceConnection(_http.JSONConnection):
    DEFAULT_API_ENDPOINT_TEMPLATE = "https://mock.{universe_domain}"
    API_BASE_MTLS_URL = "https://mock.mtls.googleapis.com"
    ALLOW_AUTO_SWITCH_TO_MTLS_URL = True
    API_VERSION = "v1"
    API_URL_TEMPLATE = "{api_base_url}/{api_version}{path}"


class _NoMtlsServiceConnection(_http.JSONConnection):
    DEFAULT_API_ENDPOINT_TEMPLATE = "https://nomtls.{universe_domain}"
    API_BASE_MTLS_URL = None
    ALLOW_AUTO_SWITCH_TO_MTLS_URL = True
    API_VERSION = "v1"
    API_URL_TEMPLATE = "{api_base_url}/{api_version}{path}"


class _MockServiceClient(ClientWithProject):
    SCOPE = None

    def __init__(
        self,
        project=DEFAULT_PROJECT_ID,
        credentials=None,
        client_options=None,
        _http=None,
    ):
        super().__init__(
            project=project,
            credentials=credentials,
            client_options=client_options,
            _http=_http,
        )
        self._connection = _MockServiceConnection(self)


class TestClientAndConnectionUniverse:
    @pytest.mark.parametrize(
        ("client_options", "env_val", "expected_universe"),
        [
            (None, None, DEFAULT_UNIVERSE),
            ({}, None, DEFAULT_UNIVERSE),
            (client_options_lib.ClientOptions(), None, DEFAULT_UNIVERSE),
            (None, f"  {CUSTOM_UNIVERSE}  ", CUSTOM_UNIVERSE),
            ({"universe_domain": CUSTOM_UNIVERSE}, None, CUSTOM_UNIVERSE),
            (
                types.MappingProxyType({"universe_domain": CUSTOM_UNIVERSE}),
                "other.goog",
                CUSTOM_UNIVERSE,
            ),
            (
                client_options_lib.ClientOptions(universe_domain=CUSTOM_UNIVERSE),
                "other.goog",
                CUSTOM_UNIVERSE,
            ),
            ({"universe_domain": DEFAULT_UNIVERSE}, CUSTOM_UNIVERSE, DEFAULT_UNIVERSE),
        ],
    )
    def test_universe_resolution_and_routing(
        self,
        monkeypatch: pytest.MonkeyPatch,
        assert_no_googleapis_calls: None,
        client_options: Any,
        env_val: str | None,
        expected_universe: str,
    ) -> None:
        if env_val is not None:
            monkeypatch.setenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", env_val)

        client = _MockServiceClient(
            credentials=_FakeCredentials(expected_universe),
            client_options=client_options,
        )
        assert client.universe_domain == expected_universe
        assert client._connection.API_BASE_URL == f"https://mock.{expected_universe}"
        if expected_universe != DEFAULT_UNIVERSE:
            assert client._connection.api_request("GET", "/items") == {}

    @pytest.mark.parametrize(
        ("client_options", "env_val"),
        [
            ({"universe_domain": ""}, None),
            ({"universe_domain": ""}, CUSTOM_UNIVERSE),
            (client_options_lib.ClientOptions(universe_domain="   "), None),
            (None, ""),
            (None, "   "),
        ],
    )
    def test_empty_universe_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
        client_options: Any,
        env_val: str | None,
    ) -> None:
        if env_val is not None:
            monkeypatch.setenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", env_val)
        with pytest.raises(EmptyUniverseError):
            _MockServiceClient(
                credentials=auth_credentials.AnonymousCredentials(),
                client_options=client_options,
            )

    def test_invalid_client_options_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="ClientOptions instance, Mapping, or None"):
            Client(
                credentials=auth_credentials.AnonymousCredentials(),
                client_options="invalid",
            )

    def test_credentials_universe_validation(
        self, monkeypatch: pytest.MonkeyPatch, assert_no_googleapis_calls: None
    ) -> None:
        # Unconfigured credential mocks do not fail in __init__ when _http is unused
        unconfigured_mock = mock.Mock(spec=auth_credentials.Credentials)
        assert _MockServiceClient(credentials=unconfigured_mock).universe_domain == (
            DEFAULT_UNIVERSE
        )

        # Case 2a: TPC client + GDU credentials raises UniverseMismatchError on HTTP use
        tpc_with_gdu_creds = _MockServiceClient(
            credentials=_FakeCredentials(DEFAULT_UNIVERSE),
            client_options={"universe_domain": CUSTOM_UNIVERSE},
        )
        with pytest.raises(UniverseMismatchError):
            tpc_with_gdu_creds._connection.api_request("GET", "/items")

        # Case 2b: GDU client + TPC credentials raises UniverseMismatchError on HTTP use
        gdu_with_tpc_creds = _MockServiceClient(
            credentials=_FakeCredentials(CUSTOM_UNIVERSE)
        )
        with pytest.raises(UniverseMismatchError):
            _ = gdu_with_tpc_creds._http

        # ADC credentials validated on HTTP use after resolution
        monkeypatch.setenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", CUSTOM_UNIVERSE)
        with mock.patch.object(
            google.auth,
            "default",
            autospec=True,
            return_value=(_FakeCredentials(DEFAULT_UNIVERSE), DEFAULT_PROJECT_ID),
        ):
            adc_client = _MockServiceClient()
            with pytest.raises(UniverseMismatchError):
                _ = adc_client._http

        # Exemptions: None (when _http provided), AnonymousCredentials, uncached GCE
        custom_http_client = Client(
            _http=object(), client_options={"universe_domain": CUSTOM_UNIVERSE}
        )
        assert custom_http_client.universe_domain == CUSTOM_UNIVERSE
        _validate_credentials_universe(
            custom_http_client.universe_domain, custom_http_client._credentials
        )

        anon_client = _MockServiceClient(
            credentials=auth_credentials.AnonymousCredentials(),
            client_options={"universe_domain": CUSTOM_UNIVERSE},
        )
        assert anon_client.universe_domain == CUSTOM_UNIVERSE
        assert anon_client._connection.api_request("GET", "/items") == {}

        uncached_gce = google.auth.compute_engine.Credentials()
        uncached_client = _MockServiceClient(
            credentials=uncached_gce,
            client_options={"universe_domain": CUSTOM_UNIVERSE},
        )
        assert uncached_client.universe_domain == CUSTOM_UNIVERSE
        assert uncached_client._http is not None

        # Cached GCE credentials ARE validated
        cached_gce = google.auth.compute_engine.Credentials(scopes=("s",))
        cached_gce._universe_domain_cached = True  # type: ignore[attr-defined]
        cached_gce_client = _MockServiceClient(
            credentials=cached_gce,
            client_options={"universe_domain": CUSTOM_UNIVERSE},
        )
        with pytest.raises(UniverseMismatchError):
            _ = cached_gce_client._http

    def test_custom_api_endpoint_and_bare_client_fallbacks(self) -> None:
        client = _MockServiceClient(
            credentials=_FakeCredentials(CUSTOM_UNIVERSE),
            client_options={
                "universe_domain": CUSTOM_UNIVERSE,
                "api_endpoint": "https://custom.mock.internal:8443",
            },
        )
        assert client._connection.API_BASE_URL == "https://custom.mock.internal:8443"
        assert (
            _MockServiceConnection(
                client, api_endpoint="https://direct.mock.internal"
            ).API_BASE_URL
            == "https://direct.mock.internal"
        )
        assert (
            _MockServiceConnection(object()).API_BASE_URL
            == "https://mock.googleapis.com"
        )
        assert (
            _MockServiceConnection(mock.Mock()).API_BASE_URL
            == "https://mock.googleapis.com"
        )

    def test_default_host_propagation_and_self_signed_jwt(self) -> None:
        from google.auth import crypt
        from google.oauth2 import service_account

        sa_kwargs: dict[str, Any] = {"always_use_jwt_access": True}
        target_universe = DEFAULT_UNIVERSE
        if (
            "universe_domain"
            in inspect.signature(service_account.Credentials).parameters
        ):  # pragma: NO COVER
            sa_kwargs["universe_domain"] = CUSTOM_UNIVERSE
            target_universe = CUSTOM_UNIVERSE

        sa_creds = service_account.Credentials(
            mock.Mock(spec=crypt.Signer),
            "sa@test-proj.iam.gserviceaccount.com",
            "https://oauth2.googleapis.com/token",
            **sa_kwargs,
        )
        client = _MockServiceClient(
            credentials=sa_creds,
            client_options={"universe_domain": target_universe},
        )
        assert client._http._default_host == f"mock.{target_universe}"
        assert (
            client._credentials._jwt_credentials._audience
            == f"https://mock.{target_universe}/"
        )

        for api_base_url, expected_host in [
            ("mock.apis-tpclp.goog:443", "mock.apis-tpclp.goog"),
            ("https:///", None),
        ]:
            edge_client = _MockServiceClient(
                credentials=auth_credentials.AnonymousCredentials()
            )
            edge_client._connection.API_BASE_URL = api_base_url
            with mock.patch(
                "google.auth.transport.requests.AuthorizedSession"
            ) as mock_session_cls:
                mock_session_cls.return_value = mock.Mock()
                _ = edge_client._http
                expected_kwargs: dict[str, Any] = {
                    "refresh_timeout": _CREDENTIALS_REFRESH_TIMEOUT
                }
                if expected_host:
                    expected_kwargs["default_host"] = expected_host
                mock_session_cls.assert_called_once_with(
                    edge_client._credentials, **expected_kwargs
                )

    def test_mtls_gating_and_fallbacks(self, monkeypatch: pytest.MonkeyPatch) -> None:
        tpc_client = _MockServiceClient(
            credentials=_FakeCredentials(CUSTOM_UNIVERSE),
            client_options={"universe_domain": CUSTOM_UNIVERSE},
            _http=mock.Mock(is_mtls=True, spec=["is_mtls"]),
        )
        monkeypatch.setenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        assert (
            tpc_client._connection.get_api_base_url_for_mtls()
            == f"https://mock.{CUSTOM_UNIVERSE}"
        )

        monkeypatch.setenv("GOOGLE_API_USE_MTLS_ENDPOINT", "always")
        with pytest.raises(MutualTLSChannelError):
            tpc_client._connection.get_api_base_url_for_mtls()

        custom_ep_client = _MockServiceClient(
            credentials=_FakeCredentials(CUSTOM_UNIVERSE),
            client_options={
                "universe_domain": CUSTOM_UNIVERSE,
                "api_endpoint": "https://custom.mock.internal",
            },
        )
        assert (
            custom_ep_client._connection.get_api_base_url_for_mtls()
            == "https://custom.mock.internal"
        )

        gdu_client = Client(
            credentials=auth_credentials.AnonymousCredentials(),
            _http=mock.Mock(is_mtls=True, spec=["is_mtls"]),
        )
        emulator_conn = _MockServiceConnection(gdu_client)
        emulator_conn.API_BASE_URL = "localhost:9023"
        assert emulator_conn.get_api_base_url_for_mtls() == "localhost:9023"

        no_mtls_conn = _NoMtlsServiceConnection(gdu_client)
        with pytest.raises(ValueError, match="mTLS endpoint is not available"):
            no_mtls_conn.get_api_base_url_for_mtls()
        monkeypatch.setenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        assert (
            no_mtls_conn.get_api_base_url_for_mtls() == "https://nomtls.googleapis.com"
        )


class TestMakeSecureChannelDefaultHost:
    def test_forwards_or_omits_default_host_by_signature(self) -> None:
        sentinel = object()

        def with_default_host(
            credentials, request, target, default_host=None, **kwargs
        ):
            return sentinel  # pragma: NO COVER

        def without_default_host(credentials, request, target, **kwargs):
            return sentinel  # pragma: NO COVER

        for fn, expected_extra in [
            (with_default_host, {"default_host": "datastore.apis-tpclp.goog"}),
            (without_default_host, {}),
        ]:
            mock_fn = mock.create_autospec(fn, return_value=sentinel)
            creds = object()
            with mock.patch(
                "google.auth.transport.grpc.secure_authorized_channel", new=mock_fn
            ):
                assert (
                    _helpers.make_secure_channel(
                        creds, "agent", "datastore.apis-tpclp.goog"
                    )
                    is sentinel
                )
            mock_fn.assert_called_once_with(
                creds,
                mock.ANY,
                "datastore.apis-tpclp.goog:443",
                options=(("grpc.primary_user_agent", "agent"),),
                **expected_extra,
            )
