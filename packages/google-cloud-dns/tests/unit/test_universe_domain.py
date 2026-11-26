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
from types import MappingProxyType
from typing import Any
from unittest import mock
from urllib.parse import urlparse

import google.auth
import pytest
import requests
from google.api_core import client_options as client_options_lib
from google.api_core.universe import EmptyUniverseError, UniverseMismatchError
from google.auth import credentials as auth_credentials
from google.auth.exceptions import MutualTLSChannelError

from google.cloud import dns

DEFAULT_PROJECT_ID = "test-proj"
DEFAULT_UNIVERSE = "googleapis.com"
CUSTOM_UNIVERSE = "apis-tpclp.goog"


class FakeScopedQuotaCredentials(
    auth_credentials.Scoped, auth_credentials.CredentialsWithQuotaProject
):
    """Fake Credentials supporting scopes, quota project, and universe_domain."""

    def __init__(
        self,
        universe_domain: str = DEFAULT_UNIVERSE,
        quota_project_id: str | None = None,
        scopes: tuple[str, ...] | None = None,
    ) -> None:
        super().__init__()
        self._universe_domain = universe_domain
        self._quota_project_id = quota_project_id
        self._scopes = scopes
        self.token = "fake-token"

    @property
    def universe_domain(self) -> str:
        return self._universe_domain

    @property
    def requires_scopes(self) -> bool:
        return False

    def refresh(self, request: Any) -> None:  # pragma: NO COVER
        self.token = "fake-token"

    def with_scopes(
        self, scopes: Any, default_scopes: Any = None
    ) -> FakeScopedQuotaCredentials:  # pragma: NO COVER
        return FakeScopedQuotaCredentials(
            universe_domain=self._universe_domain,
            quota_project_id=self._quota_project_id,
            scopes=tuple(scopes or default_scopes or ()),
        )

    def with_quota_project(
        self, quota_project_id: str | None
    ) -> FakeScopedQuotaCredentials:  # pragma: NO COVER
        return FakeScopedQuotaCredentials(
            universe_domain=self._universe_domain,
            quota_project_id=quota_project_id,
            scopes=self._scopes,
        )


def _is_googleapis_host(url: str) -> bool:
    host = urlparse(url).hostname
    return bool(host and (host == "googleapis.com" or host.endswith(".googleapis.com")))


@pytest.fixture
def captured_requests(monkeypatch: pytest.MonkeyPatch) -> Iterator[list[str]]:
    seen_urls: list[str] = []

    def _guarded_send(self, request, *args, **kwargs):
        if _is_googleapis_host(request.url):  # pragma: NO COVER
            raise ConnectionRefusedError(
                f"Unexpected googleapis.com call: {request.url}"
            )
        seen_urls.append(request.url)
        resp = requests.Response()
        resp.status_code = 200
        resp._content = b'{"quota": {"managedZones": 10}}'
        resp.headers = {"content-type": "application/json"}
        resp.encoding = "utf-8"
        return resp

    monkeypatch.setattr(requests.Session, "send", _guarded_send)
    yield seen_urls


class TestDnsUniverseDomain:
    @pytest.mark.parametrize(
        "client_options",
        [
            {"universe_domain": CUSTOM_UNIVERSE},
            MappingProxyType({"universe_domain": CUSTOM_UNIVERSE}),
            client_options_lib.ClientOptions(universe_domain=CUSTOM_UNIVERSE),
        ],
    )
    def test_custom_universe_routing_and_default_host(
        self, captured_requests: list[str], client_options: Any
    ) -> None:
        creds = FakeScopedQuotaCredentials(CUSTOM_UNIVERSE)
        client = dns.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=creds,
            client_options=client_options,
        )

        assert client.universe_domain == CUSTOM_UNIVERSE
        assert client._connection.API_BASE_URL == f"https://dns.{CUSTOM_UNIVERSE}"
        assert client.quotas() == {"managedZones": 10}
        assert captured_requests == [
            f"https://dns.{CUSTOM_UNIVERSE}/dns/v1/projects/{DEFAULT_PROJECT_ID}?prettyPrint=false"
        ]
        assert client._http._default_host == f"dns.{CUSTOM_UNIVERSE}"

    def test_env_var_universe_with_adc(
        self, monkeypatch: pytest.MonkeyPatch, captured_requests: list[str]
    ) -> None:
        monkeypatch.setenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", CUSTOM_UNIVERSE)
        adc_creds = FakeScopedQuotaCredentials(CUSTOM_UNIVERSE)

        with mock.patch.object(
            google.auth,
            "default",
            autospec=True,
            return_value=(adc_creds, DEFAULT_PROJECT_ID),
        ):
            client = dns.Client(project=DEFAULT_PROJECT_ID)

        assert client.universe_domain == CUSTOM_UNIVERSE
        assert client._connection.API_BASE_URL == f"https://dns.{CUSTOM_UNIVERSE}"
        assert client.quotas() == {"managedZones": 10}
        assert len(captured_requests) == 1

    def test_universe_validation_and_empty_errors(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        with pytest.raises(UniverseMismatchError):
            dns.Client(
                project=DEFAULT_PROJECT_ID,
                credentials=FakeScopedQuotaCredentials(DEFAULT_UNIVERSE),
                client_options={"universe_domain": CUSTOM_UNIVERSE},
            )

        with pytest.raises(UniverseMismatchError):
            dns.Client(
                project=DEFAULT_PROJECT_ID,
                credentials=FakeScopedQuotaCredentials(CUSTOM_UNIVERSE),
            )

        with pytest.raises(EmptyUniverseError):
            dns.Client(
                project=DEFAULT_PROJECT_ID,
                credentials=auth_credentials.AnonymousCredentials(),
                client_options={"universe_domain": ""},
            )

        monkeypatch.setenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", "")
        with pytest.raises(EmptyUniverseError):
            dns.Client(
                project=DEFAULT_PROJECT_ID,
                credentials=auth_credentials.AnonymousCredentials(),
            )

    def test_anonymous_credentials_and_api_endpoint_precedence(
        self, monkeypatch: pytest.MonkeyPatch, captured_requests: list[str]
    ) -> None:
        monkeypatch.setenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", "env.goog")
        anon_client = dns.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=auth_credentials.AnonymousCredentials(),
            client_options={
                "universe_domain": CUSTOM_UNIVERSE,
                "api_endpoint": "https://custom-dns.internal:8443",
            },
        )
        assert anon_client.universe_domain == CUSTOM_UNIVERSE
        assert (
            anon_client._connection.API_BASE_URL == "https://custom-dns.internal:8443"
        )
        assert anon_client.quotas() == {"managedZones": 10}
        assert captured_requests == [
            f"https://custom-dns.internal:8443/dns/v1/projects/{DEFAULT_PROJECT_ID}?prettyPrint=false"
        ]

    def test_mtls_always_gating(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GOOGLE_API_USE_MTLS_ENDPOINT", "always")

        tpc_client = dns.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=FakeScopedQuotaCredentials(CUSTOM_UNIVERSE),
            client_options={"universe_domain": CUSTOM_UNIVERSE},
        )
        with pytest.raises(MutualTLSChannelError):
            tpc_client._connection.get_api_base_url_for_mtls()

        gdu_client = dns.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=FakeScopedQuotaCredentials(DEFAULT_UNIVERSE),
        )
        with pytest.raises(ValueError, match="mTLS endpoint is not available"):
            gdu_client._connection.get_api_base_url_for_mtls()
