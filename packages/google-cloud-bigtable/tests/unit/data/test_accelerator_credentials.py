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
"""Unit tests for the accelerator credential-safety guardrail: which auth
configuration the client forwards to the daemon vs. falls back to native for.
These exercise pure helpers on the async client without spinning up a full
client or event loop."""

from types import SimpleNamespace

import pytest
from google.api_core.client_options import ClientOptions
from google.auth import compute_engine

from google.cloud.bigtable.data._async.client import (
    BigtableDataClientAsync,
    _AcceleratorUnverified,
    _DataApiTargetAsync,
)


def _bare_client():
    """A client instance that skips __init__ (no network / event loop)."""
    return object.__new__(BigtableDataClientAsync)


class _FakeCreds:
    """Stand-in credential exposing (or not) a service_account_email."""

    def __init__(self, email=None):
        if email is not None:
            self.service_account_email = email


class TestInitAcceleratorConfig:
    def test_no_config_forwards_default_scopes(self):
        c = _bare_client()
        c._init_accelerator_config(explicit_credentials=False, client_options=None)
        assert c._accelerator_blocked_reason is None
        assert "--scopes" in c._accelerator_flags
        assert c._accelerator_env == {}

    def test_explicit_credentials_blocks(self):
        c = _bare_client()
        c._init_accelerator_config(explicit_credentials=True, client_options=None)
        assert c._accelerator_blocked_reason is not None
        assert "credentials" in c._accelerator_blocked_reason

    def test_api_key_blocks(self):
        c = _bare_client()
        c._init_accelerator_config(
            explicit_credentials=False, client_options=ClientOptions(api_key="AIzaKEY")
        )
        assert "api_key" in c._accelerator_blocked_reason

    def test_client_cert_source_blocks(self):
        c = _bare_client()
        c._init_accelerator_config(
            explicit_credentials=False,
            client_options=ClientOptions(client_cert_source=lambda: (b"", b"")),
        )
        assert "client_cert_source" in c._accelerator_blocked_reason

    def test_forwards_non_secret_knobs(self):
        c = _bare_client()
        opts = ClientOptions(
            scopes=["https://www.googleapis.com/auth/custom"],
            quota_project_id="quota-proj",
            api_endpoint="https://custom.example.com:443",
            universe_domain="my-universe.example.com",
        )
        c._init_accelerator_config(explicit_credentials=False, client_options=opts)
        flags = c._accelerator_flags
        assert flags[flags.index("--scopes") + 1] == (
            "https://www.googleapis.com/auth/custom"
        )
        assert flags[flags.index("--quota-project") + 1] == "quota-proj"
        # api_endpoint is normalized to host:port (scheme stripped).
        assert flags[flags.index("--data-endpoint") + 1] == "custom.example.com:443"
        assert flags[flags.index("--universe-domain") + 1] == "my-universe.example.com"
        assert c._accelerator_blocked_reason is None

    def test_default_universe_not_forwarded(self):
        c = _bare_client()
        c._init_accelerator_config(
            explicit_credentials=False,
            client_options=ClientOptions(universe_domain="googleapis.com"),
        )
        assert "--universe-domain" not in c._accelerator_flags

    def test_credentials_file_forwarded_as_env_path(self):
        c = _bare_client()
        c._init_accelerator_config(
            explicit_credentials=False,
            client_options=ClientOptions(credentials_file="/path/to/key.json"),
        )
        assert c._accelerator_env["GOOGLE_APPLICATION_CREDENTIALS"] == (
            "/path/to/key.json"
        )
        # The path is not a "secret" that blocks acceleration.
        assert c._accelerator_blocked_reason is None


class TestResolvePrincipal:
    def test_service_account_email(self):
        c = _bare_client()
        c._credentials = _FakeCreds(email="svc@proj.iam.gserviceaccount.com")
        assert c._resolve_principal() == "svc@proj.iam.gserviceaccount.com"

    def test_no_email_returns_none(self):
        c = _bare_client()
        c._credentials = _FakeCreds()  # e.g. plain gcloud user ADC
        assert c._resolve_principal() is None

    def test_default_email_returns_none(self):
        c = _bare_client()
        c._credentials = _FakeCreds(email="default")
        assert c._resolve_principal() is None

    def test_cached_across_calls(self):
        c = _bare_client()
        c._credentials = _FakeCreds(email="svc@proj.iam.gserviceaccount.com")
        assert c._resolve_principal() == "svc@proj.iam.gserviceaccount.com"
        # A later credential swap does not change the memoized principal.
        c._credentials = _FakeCreds(email="other@proj.iam.gserviceaccount.com")
        assert c._resolve_principal() == "svc@proj.iam.gserviceaccount.com"

    def test_compute_engine_refresh(self):
        # Compute Engine credentials only expose the email after a refresh
        # against the metadata server (email defaults to "default" until then).
        creds = compute_engine.Credentials()
        assert creds.service_account_email == "default"

        def fake_refresh(request):
            creds._service_account_email = "compute-sa@proj.iam.gserviceaccount.com"

        creds.refresh = fake_refresh
        c = _bare_client()
        c._credentials = creds
        assert c._resolve_principal() == "compute-sa@proj.iam.gserviceaccount.com"


# Matching scopes on both sides by default, so principal-focused tests below
# exercise only the principal branch. The daemon writes ``scopes`` as a JSON
# array (see google-cloud-go .../accelerator/cmd/identity.go).
_SCOPES = ["https://www.googleapis.com/auth/bigtable.data"]


class _FakeServer:
    def __init__(self, principal, scopes=_SCOPES, missing=False):
        self._principal = principal
        self._scopes = scopes
        self._missing = missing

    def read_identity(self):
        if self._missing:
            return {}
        return {"principal": self._principal, "scopes": self._scopes}


def _verify(
    client_principal,
    daemon_principal,
    missing=False,
    client_scopes=_SCOPES,
    daemon_scopes=_SCOPES,
):
    """Invoke the Table's verify helper against fake client/server doubles."""
    table = SimpleNamespace(
        client=SimpleNamespace(
            _resolve_principal=lambda: client_principal,
            _accelerator_scopes=client_scopes,
        )
    )
    server = _FakeServer(daemon_principal, scopes=daemon_scopes, missing=missing)
    _DataApiTargetAsync._verify_daemon_identity(table, server)


class TestVerifyDaemonIdentity:
    def test_match_proceeds(self):
        # Matching principal and scopes: returns without raising.
        _verify("svc@proj.iam.gserviceaccount.com", "svc@proj.iam.gserviceaccount.com")

    def test_mismatch_raises(self):
        with pytest.raises(RuntimeError, match="identity mismatch"):
            _verify(
                "svc-a@proj.iam.gserviceaccount.com",
                "svc-b@proj.iam.gserviceaccount.com",
            )

    def test_client_unknown_falls_back(self):
        with pytest.raises(_AcceleratorUnverified):
            _verify(None, "svc@proj.iam.gserviceaccount.com")

    def test_daemon_unknown_falls_back(self):
        with pytest.raises(_AcceleratorUnverified):
            _verify("svc@proj.iam.gserviceaccount.com", None)

    def test_daemon_missing_principal_falls_back(self):
        with pytest.raises(_AcceleratorUnverified):
            _verify("svc@proj.iam.gserviceaccount.com", None, missing=True)

    def test_scope_match_ignores_order_and_dupes(self):
        # Principals match; scopes differ only in order/duplication -> proceed.
        _verify(
            "svc@proj.iam.gserviceaccount.com",
            "svc@proj.iam.gserviceaccount.com",
            client_scopes=["scope-a", "scope-b"],
            daemon_scopes=["scope-b", "scope-a", "scope-a"],
        )

    def test_scope_mismatch_raises(self):
        # Principals match but the daemon resolved a different effective scope.
        with pytest.raises(RuntimeError, match="scope mismatch"):
            _verify(
                "svc@proj.iam.gserviceaccount.com",
                "svc@proj.iam.gserviceaccount.com",
                client_scopes=["https://www.googleapis.com/auth/bigtable.data"],
                daemon_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

    def test_daemon_missing_scopes_falls_back(self):
        # Older daemon that resolves a principal but writes no scopes.
        with pytest.raises(_AcceleratorUnverified):
            _verify(
                "svc@proj.iam.gserviceaccount.com",
                "svc@proj.iam.gserviceaccount.com",
                daemon_scopes=[],
            )

    def test_client_missing_scopes_falls_back(self):
        with pytest.raises(_AcceleratorUnverified):
            _verify(
                "svc@proj.iam.gserviceaccount.com",
                "svc@proj.iam.gserviceaccount.com",
                client_scopes=[],
            )
