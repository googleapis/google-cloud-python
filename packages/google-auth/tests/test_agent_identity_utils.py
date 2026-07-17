# Copyright 2025 Google LLC
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
import hashlib
import json
from unittest import mock
import urllib.parse

from cryptography import x509
import pytest

from google.auth import _agent_identity_utils, environment_vars, exceptions

# A mock PEM-encoded certificate without an Agent Identity SPIFFE ID.
NON_AGENT_IDENTITY_CERT_BYTES = (
    b"-----BEGIN CERTIFICATE-----\n"
    b"MIIDIzCCAgugAwIBAgIJAMfISuBQ5m+5MA0GCSqGSIb3DQEBBQUAMBUxEzARBgNV\n"
    b"BAMTCnVuaXQtdGVzdHMwHhcNMTExMjA2MTYyNjAyWhcNMjExMjAzMTYyNjAyWjAV\n"
    b"MRMwEQYDVQQDEwp1bml0LXRlc3RzMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB\n"
    b"CgKCAQEA4ej0p7bQ7L/r4rVGUz9RN4VQWoej1Bg1mYWIDYslvKrk1gpj7wZgkdmM\n"
    b"7oVK2OfgrSj/FCTkInKPqaCR0gD7K80q+mLBrN3PUkDrJQZpvRZIff3/xmVU1Wer\n"
    b"uQLFJjnFb2dqu0s/FY/2kWiJtBCakXvXEOb7zfbINuayL+MSsCGSdVYsSliS5qQp\n"
    b"gyDap+8b5fpXZVJkq92hrcNtbkg7hCYUJczt8n9hcCTJCfUpApvaFQ18pe+zpyl4\n"
    b"+WzkP66I28hniMQyUlA1hBiskT7qiouq0m8IOodhv2fagSZKjOTTU2xkSBc//fy3\n"
    b"ZpsL7WqgsZS7Q+0VRK8gKfqkxg5OYQIDAQABo3YwdDAdBgNVHQ4EFgQU2RQ8yO+O\n"
    b"gN8oVW2SW7RLrfYd9jEwRQYDVR0jBD4wPIAU2RQ8yO+OgN8oVW2SW7RLrfYd9jGh\n"
    b"GaQXMBUxEzARBgNVBAMTCnVuaXQtdGVzdHOCCQDHyErgUOZvuTAMBgNVHRMEBTAD\n"
    b"AQH/MA0GCSqGSIb3DQEBBQUAA4IBAQBRv+M/6+FiVu7KXNjFI5pSN17OcW5QUtPr\n"
    b"odJMlWrJBtynn/TA1oJlYu3yV5clc/71Vr/AxuX5xGP+IXL32YDF9lTUJXG/uUGk\n"
    b"+JETpKmQviPbRsvzYhz4pf6ZIOZMc3/GIcNq92ECbseGO+yAgyWUVKMmZM0HqXC9\n"
    b"ovNslqe0M8C1sLm1zAR5z/h/litE7/8O2ietija3Q/qtl2TOXJdCA6sgjJX2WUql\n"
    b"ybrC55ct18NKf3qhpcEkGQvFU40rVYApJpi98DiZPYFdx1oBDp/f4uZ3ojpxRVFT\n"
    b"cDwcJLfNRCPUhormsY7fDS9xSyThiHsW9mjJYdcaKQkwYZ0F11yB\n"
    b"-----END CERTIFICATE-----\n"
)


class TestAgentIdentityUtils:
    @pytest.fixture(autouse=True)
    def clean_env(self, monkeypatch):
        monkeypatch.delenv(
            environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE,
            raising=False,
        )
        monkeypatch.delenv(
            environment_vars.CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE,
            raising=False,
        )

    @mock.patch("cryptography.x509.load_pem_x509_certificate")
    def test_parse_certificate(self, mock_load_cert):
        result = _agent_identity_utils.parse_certificate(b"cert_bytes")
        mock_load_cert.assert_called_once_with(b"cert_bytes")
        assert result == mock_load_cert.return_value

    def test_is_certificate_file_ready_empty_path(self):
        result = _agent_identity_utils._is_certificate_file_ready("")
        assert result is False

    def test_get_agent_identity_certificate_path_empty_env(self, monkeypatch):
        monkeypatch.delenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, raising=False
        )
        result = _agent_identity_utils.get_agent_identity_certificate_path()
        assert result is None

    @mock.patch("google.auth._agent_identity_utils.os.path.commonpath")
    @mock.patch(
        "google.auth._agent_identity_utils._get_cert_path_with_optional_polling"
    )
    def test_get_agent_identity_certificate_path_value_error(
        self, mock_get_cert, mock_commonpath, monkeypatch
    ):
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, "/path/to/config.json"
        )
        mock_commonpath.side_effect = ValueError("Different drives")
        mock_get_cert.return_value = "cert_path"

        result = _agent_identity_utils.get_agent_identity_certificate_path()
        assert result == "cert_path"
        mock_get_cert.assert_called_once_with("/path/to/config.json", False)

    @mock.patch("google.auth._agent_identity_utils.os.stat")
    def test_is_certificate_file_ready_permission_error(self, mock_stat):
        mock_stat.side_effect = PermissionError("Permission denied")
        with pytest.raises(PermissionError):
            _agent_identity_utils._is_certificate_file_ready("/path/to/cert")

    @mock.patch("google.auth._agent_identity_utils.os.stat")
    def test_is_certificate_file_ready_os_error(self, mock_stat):
        mock_stat.side_effect = OSError("Not found")
        # Should swallow the OSError and return False
        result = _agent_identity_utils._is_certificate_file_ready("/path/to/cert")
        assert result is False

    @mock.patch("google.auth._agent_identity_utils.os.stat")
    def test_is_certificate_file_ready_not_a_file(self, mock_stat):
        import stat

        mock_stat.return_value = mock.MagicMock(st_mode=stat.S_IFDIR, st_size=4096)
        result = _agent_identity_utils._is_certificate_file_ready("/path/to/cert")
        assert result is False

    def test__is_agent_identity_certificate_invalid(self):
        cert = _agent_identity_utils.parse_certificate(NON_AGENT_IDENTITY_CERT_BYTES)
        assert not _agent_identity_utils._is_agent_identity_certificate(cert)

    @pytest.mark.parametrize(
        "spiffe_id",
        [
            "spiffe://agents.global.proj-12345.system.id.goog/workload",
            "spiffe://agents.global.org-12345.system.id.goog/workload",
            "spiffe://agents-nonprod.global.proj-12345.system.id.goog/workload",
            "spiffe://agents-nonprod.global.org-12345.system.id.goog/workload",
        ],
    )
    def test__is_agent_identity_certificate_valid_spiffe(self, spiffe_id):
        mock_cert = mock.MagicMock()
        mock_ext = mock.MagicMock()
        mock_san_value = mock.MagicMock()
        mock_cert.extensions.get_extension_for_oid.return_value = mock_ext
        mock_ext.value = mock_san_value
        mock_san_value.get_values_for_type.return_value = [spiffe_id]
        assert _agent_identity_utils._is_agent_identity_certificate(mock_cert)

    def test__is_agent_identity_certificate_non_matching_spiffe(self):
        mock_cert = mock.MagicMock()
        mock_ext = mock.MagicMock()
        mock_san_value = mock.MagicMock()
        mock_cert.extensions.get_extension_for_oid.return_value = mock_ext
        mock_ext.value = mock_san_value
        mock_san_value.get_values_for_type.return_value = [
            "spiffe://other.domain.com/workload"
        ]
        assert not _agent_identity_utils._is_agent_identity_certificate(mock_cert)

    def test__is_agent_identity_certificate_no_san(self):
        mock_cert = mock.MagicMock()
        mock_cert.extensions.get_extension_for_oid.side_effect = x509.ExtensionNotFound(
            "Test extension not found", None
        )
        assert not _agent_identity_utils._is_agent_identity_certificate(mock_cert)

    def test__is_agent_identity_certificate_not_spiffe_uri(self):
        mock_cert = mock.MagicMock()
        mock_ext = mock.MagicMock()
        mock_san_value = mock.MagicMock()
        mock_cert.extensions.get_extension_for_oid.return_value = mock_ext
        mock_ext.value = mock_san_value
        mock_san_value.get_values_for_type.return_value = ["https://example.com"]
        assert not _agent_identity_utils._is_agent_identity_certificate(mock_cert)

    def test_calculate_certificate_fingerprint(self):
        mock_cert = mock.MagicMock()
        mock_cert.public_bytes.return_value = b"der-bytes"

        # Expected: base64 (standard), unpadded, then URL-encoded
        base64_fingerprint = base64.b64encode(
            hashlib.sha256(b"der-bytes").digest()
        ).decode("utf-8")
        unpadded_base64_fingerprint = base64_fingerprint.rstrip("=")
        expected_fingerprint = urllib.parse.quote(unpadded_base64_fingerprint)

        fingerprint = _agent_identity_utils.calculate_certificate_fingerprint(mock_cert)

        assert fingerprint == expected_fingerprint

    @mock.patch("google.auth._agent_identity_utils._is_agent_identity_certificate")
    def test_should_request_bound_token(self, mock_is_agent, monkeypatch):
        # Agent cert, default env var (opt-in)
        mock_is_agent.return_value = True
        monkeypatch.delenv(
            environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES,
            raising=False,
        )
        assert _agent_identity_utils.should_request_bound_token(mock.sentinel.cert)

        # Agent cert, explicit opt-in
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES,
            "true",
        )
        assert _agent_identity_utils.should_request_bound_token(mock.sentinel.cert)

        # Agent cert, explicit opt-out
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES,
            "false",
        )
        assert not _agent_identity_utils.should_request_bound_token(mock.sentinel.cert)

        # Non-agent cert, opt-in
        mock_is_agent.return_value = False
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES,
            "true",
        )
        assert not _agent_identity_utils.should_request_bound_token(mock.sentinel.cert)

    @mock.patch("google.auth._agent_identity_utils._is_agent_identity_certificate")
    def test_should_request_bound_token_explicit_use_client_cert_false(
        self, mock_is_agent, monkeypatch
    ):
        mock_is_agent.return_value = True
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE,
            "false",
        )
        assert not _agent_identity_utils.should_request_bound_token(mock.sentinel.cert)

    @mock.patch("google.auth._agent_identity_utils._is_agent_identity_certificate")
    def test_should_request_bound_token_explicit_use_client_cert_invalid(
        self, mock_is_agent, monkeypatch
    ):
        mock_is_agent.return_value = True
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE,
            "foo",
        )
        assert not _agent_identity_utils.should_request_bound_token(mock.sentinel.cert)

    @mock.patch("google.auth._agent_identity_utils._is_agent_identity_certificate")
    def test_should_request_bound_token_auto_enablement(self, mock_is_agent):
        mock_is_agent.return_value = True
        assert _agent_identity_utils.should_request_bound_token(mock.sentinel.cert)

    def test_get_agent_identity_certificate_path_success(self, tmpdir, monkeypatch):
        cert_path = tmpdir.join("cert.pem")
        cert_path.write("cert_content")
        config_path = tmpdir.join("config.json")
        config_path.write(
            json.dumps({"cert_configs": {"workload": {"cert_path": str(cert_path)}}})
        )
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        result = _agent_identity_utils.get_agent_identity_certificate_path()
        assert result == str(cert_path)

    @mock.patch("time.sleep")
    @mock.patch("google.auth._agent_identity_utils.os.path.exists")
    def test_get_agent_identity_certificate_path_retry(
        self, mock_exists, mock_sleep, tmpdir, monkeypatch
    ):
        monkeypatch.setattr(
            "google.auth._agent_identity_utils._WELL_KNOWN_CERT_PATH",
            str(tmpdir.join("certificates.pem")),
        )
        config_path = tmpdir.join("config.json")
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        # File doesn't exist initially
        mock_exists.return_value = False

        with pytest.raises(exceptions.RefreshError):
            _agent_identity_utils.get_agent_identity_certificate_path()

        assert mock_sleep.call_count == len(_agent_identity_utils._POLLING_INTERVALS)

    @mock.patch("time.sleep")
    @mock.patch("google.auth._agent_identity_utils.os.path.exists")
    def test_get_agent_identity_certificate_path_failure(
        self, mock_exists, mock_sleep, tmpdir, monkeypatch
    ):
        monkeypatch.setattr(
            "google.auth._agent_identity_utils._WELL_KNOWN_CERT_PATH",
            str(tmpdir.join("certificates.pem")),
        )
        config_path = tmpdir.join("non_existent_config.json")
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        # Simulate workload env (well_known_dir exists) to avoid fail-fast
        mock_exists.return_value = False

        with pytest.raises(exceptions.RefreshError) as excinfo:
            _agent_identity_utils.get_agent_identity_certificate_path()

        assert "not found after multiple retries" in str(excinfo.value)
        assert (
            environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES
            in str(excinfo.value)
        )
        assert mock_sleep.call_count == len(_agent_identity_utils._POLLING_INTERVALS)

    @mock.patch("time.sleep")
    @mock.patch("google.auth._agent_identity_utils.os.path.exists")
    def test_get_agent_identity_certificate_path_fail_fast_config_missing(
        self, mock_exists, mock_sleep, tmpdir, monkeypatch
    ):
        # Simulate config path outside well-known dir where config file does not exist.
        well_known_path = tmpdir.mkdir("well_known").join("certificates.pem")
        monkeypatch.setattr(
            "google.auth._agent_identity_utils._WELL_KNOWN_CERT_PATH",
            str(well_known_path),
        )

        config_path = tmpdir.mkdir("custom").join("custom_config.json")
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        mock_exists.return_value = False

        result = _agent_identity_utils.get_agent_identity_certificate_path()

        assert result is None
        mock_sleep.assert_not_called()

    @mock.patch("time.sleep")
    @mock.patch("google.auth._agent_identity_utils.os.path.exists")
    def test_get_agent_identity_certificate_path_fail_fast_cert_missing(
        self, mock_exists, mock_sleep, tmpdir, monkeypatch
    ):
        # Simulate config path outside well-known dir where config is valid but cert is missing.
        well_known_path = tmpdir.mkdir("well_known_cert").join("certificates.pem")
        monkeypatch.setattr(
            "google.auth._agent_identity_utils._WELL_KNOWN_CERT_PATH",
            str(well_known_path),
        )

        custom_dir = tmpdir.mkdir("custom_cert")
        config_path = custom_dir.join("custom_config.json")
        cert_path_str = str(custom_dir.join("cert.pem"))

        config_path.write(
            json.dumps({"cert_configs": {"workload": {"cert_path": cert_path_str}}})
        )
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        def exists_side_effect(path):
            return path == str(config_path)

        mock_exists.side_effect = exists_side_effect

        result = _agent_identity_utils.get_agent_identity_certificate_path()

        assert result is None
        mock_sleep.assert_not_called()

    @mock.patch("time.sleep")
    @mock.patch("google.auth._agent_identity_utils.os.path.exists")
    def test_get_agent_identity_certificate_path_cert_not_found(
        self, mock_exists, mock_sleep, tmpdir, monkeypatch
    ):
        monkeypatch.setattr(
            "google.auth._agent_identity_utils._WELL_KNOWN_CERT_PATH",
            str(tmpdir.join("certificates.pem")),
        )
        cert_path_str = str(tmpdir.join("cert.pem"))
        config_path = tmpdir.join("config.json")
        config_path.write(
            json.dumps({"cert_configs": {"workload": {"cert_path": cert_path_str}}})
        )
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        def exists_side_effect(path):
            return path == str(config_path)

        mock_exists.side_effect = exists_side_effect

        with pytest.raises(exceptions.RefreshError):
            _agent_identity_utils.get_agent_identity_certificate_path()

        assert mock_sleep.call_count == len(_agent_identity_utils._POLLING_INTERVALS)

    @mock.patch("time.sleep")
    def test_get_agent_identity_certificate_path_non_workload_config(
        self, mock_sleep, tmpdir, monkeypatch
    ):
        config_path = tmpdir.join("config.json")
        config_path.write(
            json.dumps({"cert_configs": {"pkcs11": {"module": "some_module"}}})
        )
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        result = _agent_identity_utils.get_agent_identity_certificate_path()

        # Should return None immediately without polling
        assert result is None
        mock_sleep.assert_not_called()

    @mock.patch("time.sleep")
    def test_get_agent_identity_certificate_path_invalid_json(
        self, mock_sleep, tmpdir, monkeypatch
    ):
        config_path = tmpdir.join("config.json")
        config_path.write("{invalid_json: true}")  # Invalid JSON missing quotes
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        result = _agent_identity_utils.get_agent_identity_certificate_path()

        # Should return None immediately without polling/sleeping
        assert result is None
        mock_sleep.assert_not_called()

    @mock.patch("time.sleep")
    def test_get_agent_identity_certificate_path_non_dict_json(
        self, mock_sleep, tmpdir, monkeypatch
    ):
        config_path = tmpdir.join("config.json")
        config_path.write(json.dumps(["not", "a", "dict"]))  # Valid JSON list
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        result = _agent_identity_utils.get_agent_identity_certificate_path()

        # Should fail fast immediately and return None without polling
        assert result is None
        mock_sleep.assert_not_called()

    @mock.patch("time.sleep")
    def test_get_agent_identity_certificate_path_workload_config_missing_cert_path(
        self, mock_sleep, tmpdir, monkeypatch
    ):
        config_path = tmpdir.join("config.json")
        config_path.write(json.dumps({"cert_configs": {"workload": {}}}))
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        result = _agent_identity_utils.get_agent_identity_certificate_path()

        # Should return None immediately without polling
        assert result is None
        mock_sleep.assert_not_called()

    @mock.patch("time.sleep")
    @mock.patch("google.auth._agent_identity_utils.os.path.exists")
    def test_get_agent_identity_certificate_path_permission_error_config(
        self, mock_exists, mock_sleep, tmpdir, monkeypatch
    ):
        config_path = tmpdir.join("config.json")
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )
        # Mock os.path.exists so ECP workstation fail-fast is not triggered
        mock_exists.return_value = True

        # Mocking open to raise PermissionError
        mock_open = mock.mock_open()
        mock_open.side_effect = PermissionError("Permission denied")

        with mock.patch("builtins.open", mock_open):
            result = _agent_identity_utils.get_agent_identity_certificate_path()

        assert result is None
        mock_sleep.assert_not_called()

    @mock.patch("time.sleep")
    @mock.patch("google.auth._agent_identity_utils._is_certificate_file_ready")
    def test_get_agent_identity_certificate_path_permission_error_cert_file(
        self, mock_is_ready, mock_sleep, tmpdir, monkeypatch
    ):
        well_known_path = tmpdir.mkdir("well_known").join("certificates.pem")
        monkeypatch.setattr(
            "google.auth._agent_identity_utils._WELL_KNOWN_CERT_PATH",
            str(well_known_path),
        )

        config_path = tmpdir.mkdir("custom").join("custom_config.json")
        cert_path_str = str(tmpdir.join("cert.pem"))
        config_path.write(
            json.dumps({"cert_configs": {"workload": {"cert_path": cert_path_str}}})
        )
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_CERTIFICATE_CONFIG, str(config_path)
        )

        # Mock _is_certificate_file_ready to raise PermissionError
        mock_is_ready.side_effect = PermissionError("Permission denied")

        result = _agent_identity_utils.get_agent_identity_certificate_path()

        assert result is None
        mock_sleep.assert_not_called()

    @mock.patch("google.auth._agent_identity_utils.get_agent_identity_certificate_path")
    def test_get_and_parse_agent_identity_certificate_opted_out(
        self, mock_get_path, monkeypatch
    ):
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES,
            "false",
        )
        result = _agent_identity_utils.get_and_parse_agent_identity_certificate()
        assert result is None
        mock_get_path.assert_not_called()

    @mock.patch("google.auth._agent_identity_utils.get_agent_identity_certificate_path")
    def test_get_and_parse_agent_identity_certificate_no_path(
        self, mock_get_path, monkeypatch
    ):
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES,
            "true",
        )
        mock_get_path.return_value = None
        result = _agent_identity_utils.get_and_parse_agent_identity_certificate()
        assert result is None
        mock_get_path.assert_called_once()

    @mock.patch("google.auth._agent_identity_utils.parse_certificate")
    @mock.patch("google.auth._agent_identity_utils.get_agent_identity_certificate_path")
    def test_get_and_parse_agent_identity_certificate_success(
        self, mock_get_path, mock_parse_certificate, monkeypatch
    ):
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES,
            "true",
        )
        mock_get_path.return_value = "/fake/cert.pem"
        mock_open = mock.mock_open(read_data=b"cert_bytes")

        with mock.patch("builtins.open", mock_open):
            result = _agent_identity_utils.get_and_parse_agent_identity_certificate()

        mock_open.assert_called_once_with("/fake/cert.pem", "rb")
        mock_parse_certificate.assert_called_once_with(b"cert_bytes")
        assert result == mock_parse_certificate.return_value

    @mock.patch("google.auth._agent_identity_utils.get_agent_identity_certificate_path")
    def test_get_and_parse_agent_identity_certificate_use_client_cert_false(
        self, mock_get_path, monkeypatch
    ):
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE,
            "false",
        )
        result = _agent_identity_utils.get_and_parse_agent_identity_certificate()
        assert result is None
        mock_get_path.assert_not_called()

    @mock.patch("google.auth._agent_identity_utils.get_agent_identity_certificate_path")
    def test_get_and_parse_agent_identity_certificate_use_client_cert_invalid(
        self, mock_get_path, monkeypatch
    ):
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE,
            "foo",
        )
        result = _agent_identity_utils.get_and_parse_agent_identity_certificate()
        assert result is None
        mock_get_path.assert_not_called()

    @mock.patch("google.auth._agent_identity_utils.get_agent_identity_certificate_path")
    def test_get_and_parse_agent_identity_certificate_file_read_error(
        self, mock_get_path, monkeypatch
    ):
        monkeypatch.setenv(
            environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES,
            "true",
        )
        mock_get_path.return_value = "/fake/cert.pem"
        mock_open = mock.mock_open()
        mock_open.side_effect = PermissionError("Permission denied")

        with mock.patch("builtins.open", mock_open):
            result = _agent_identity_utils.get_and_parse_agent_identity_certificate()

        assert result is None

    def test_get_cached_cert_fingerprint_no_cert(self):
        with pytest.raises(ValueError, match="mTLS connection is not configured."):
            _agent_identity_utils.get_cached_cert_fingerprint(None)

    def test_get_cached_cert_fingerprint_with_cert(self):
        fingerprint = _agent_identity_utils.get_cached_cert_fingerprint(
            NON_AGENT_IDENTITY_CERT_BYTES
        )
        assert isinstance(fingerprint, str)


class TestAgentIdentityUtilsNoCryptography:
    @pytest.fixture(autouse=True)
    def mock_cryptography_import(self):
        with mock.patch.dict(
            "sys.modules",
            {
                "cryptography": None,
                "cryptography.hazmat": None,
                "cryptography.hazmat.primitives": None,
                "cryptography.hazmat.primitives.serialization": None,
            },
        ):
            yield

    def test_parse_certificate_raises_import_error(self):
        with pytest.raises(ImportError, match="The cryptography library is required"):
            _agent_identity_utils.parse_certificate(b"cert_bytes")

    def test_is_agent_identity_certificate_raises_import_error(self):
        with pytest.raises(ImportError, match="The cryptography library is required"):
            _agent_identity_utils._is_agent_identity_certificate(mock.sentinel.cert)

    def test_calculate_certificate_fingerprint_raises_import_error(self):
        with pytest.raises(ImportError, match="The cryptography library is required"):
            _agent_identity_utils.calculate_certificate_fingerprint(mock.sentinel.cert)
