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

from google.api_core.client_options import ClientOptions

from google.cloud.bigtable.data._async.client import BigtableDataClientAsync


def _bare_client():
    """A client instance that skips __init__ (no network / event loop)."""
    return object.__new__(BigtableDataClientAsync)


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
