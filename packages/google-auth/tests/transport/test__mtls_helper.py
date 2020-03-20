# Copyright 2020 Google LLC
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

import os
import re

import mock
import pytest

from google.auth.transport import _mtls_helper

CONTEXT_AWARE_METADATA = {"cert_provider_command": ["some command"]}

CONTEXT_AWARE_METADATA_NO_CERT_PROVIDER_COMMAND = {}


def check_cert_and_key(content, expected_cert, expected_key):
    success = True

    cert_match = re.findall(_mtls_helper._CERT_REGEX, content)
    success = success and len(cert_match) == 1 and cert_match[0] == expected_cert

    key_match = re.findall(_mtls_helper._KEY_REGEX, content)
    success = success and len(key_match) == 1 and key_match[0] == expected_key

    return success


class TestCertAndKeyRegex(object):
    def test_cert_and_key(self):
        # Test single cert and single key
        check_cert_and_key(
            pytest.public_cert_bytes + pytest.private_key_bytes,
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )
        check_cert_and_key(
            pytest.private_key_bytes + pytest.public_cert_bytes,
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        # Test cert chain and single key
        check_cert_and_key(
            pytest.public_cert_bytes
            + pytest.public_cert_bytes
            + pytest.private_key_bytes,
            pytest.public_cert_bytes + pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )
        check_cert_and_key(
            pytest.private_key_bytes
            + pytest.public_cert_bytes
            + pytest.public_cert_bytes,
            pytest.public_cert_bytes + pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

    def test_key(self):
        # Create some fake keys for regex check.
        KEY = b"""-----BEGIN PRIVATE KEY-----
        MIIBCgKCAQEA4ej0p7bQ7L/r4rVGUz9RN4VQWoej1Bg1mYWIDYslvKrk1gpj7wZg
        /fy3ZpsL7WqgsZS7Q+0VRK8gKfqkxg5OYQIDAQAB
        -----END PRIVATE KEY-----"""
        RSA_KEY = b"""-----BEGIN RSA PRIVATE KEY-----
        MIIBCgKCAQEA4ej0p7bQ7L/r4rVGUz9RN4VQWoej1Bg1mYWIDYslvKrk1gpj7wZg
        /fy3ZpsL7WqgsZS7Q+0VRK8gKfqkxg5OYQIDAQAB
        -----END RSA PRIVATE KEY-----"""
        EC_KEY = b"""-----BEGIN EC PRIVATE KEY-----
        MIIBCgKCAQEA4ej0p7bQ7L/r4rVGUz9RN4VQWoej1Bg1mYWIDYslvKrk1gpj7wZg
        /fy3ZpsL7WqgsZS7Q+0VRK8gKfqkxg5OYQIDAQAB
        -----END EC PRIVATE KEY-----"""

        check_cert_and_key(
            pytest.public_cert_bytes + KEY, pytest.public_cert_bytes, KEY
        )
        check_cert_and_key(
            pytest.public_cert_bytes + RSA_KEY, pytest.public_cert_bytes, RSA_KEY
        )
        check_cert_and_key(
            pytest.public_cert_bytes + EC_KEY, pytest.public_cert_bytes, EC_KEY
        )


class TestCheckaMetadataPath(object):
    def test_success(self):
        metadata_path = os.path.join(pytest.data_dir, "context_aware_metadata.json")
        returned_path = _mtls_helper._check_dca_metadata_path(metadata_path)
        assert returned_path is not None

    def test_failure(self):
        metadata_path = os.path.join(pytest.data_dir, "not_exists.json")
        returned_path = _mtls_helper._check_dca_metadata_path(metadata_path)
        assert returned_path is None


class TestReadMetadataFile(object):
    def test_success(self):
        metadata_path = os.path.join(pytest.data_dir, "context_aware_metadata.json")
        metadata = _mtls_helper._read_dca_metadata_file(metadata_path)

        assert "cert_provider_command" in metadata

    def test_file_not_json(self):
        # read a file which is not json format.
        metadata_path = os.path.join(pytest.data_dir, "privatekey.pem")
        with pytest.raises(ValueError):
            _mtls_helper._read_dca_metadata_file(metadata_path)


class TestGetClientSslCredentials(object):
    def create_mock_process(self, output, error):
        # There are two steps to execute a script with subprocess.Popen.
        # (1) process = subprocess.Popen([comannds])
        # (2) stdout, stderr = process.communicate()
        # This function creates a mock process which can be returned by a mock
        # subprocess.Popen. The mock process returns the given output and error
        # when mock_process.communicate() is called.
        mock_process = mock.Mock()
        attrs = {"communicate.return_value": (output, error), "returncode": 0}
        mock_process.configure_mock(**attrs)
        return mock_process

    @mock.patch("subprocess.Popen", autospec=True)
    def test_success(self, mock_popen):
        mock_popen.return_value = self.create_mock_process(
            pytest.public_cert_bytes + pytest.private_key_bytes, b""
        )
        cert, key = _mtls_helper.get_client_ssl_credentials(CONTEXT_AWARE_METADATA)
        assert cert == pytest.public_cert_bytes
        assert key == pytest.private_key_bytes

    @mock.patch("subprocess.Popen", autospec=True)
    def test_success_with_cert_chain(self, mock_popen):
        PUBLIC_CERT_CHAIN_BYTES = pytest.public_cert_bytes + pytest.public_cert_bytes
        mock_popen.return_value = self.create_mock_process(
            PUBLIC_CERT_CHAIN_BYTES + pytest.private_key_bytes, b""
        )
        cert, key = _mtls_helper.get_client_ssl_credentials(CONTEXT_AWARE_METADATA)
        assert cert == PUBLIC_CERT_CHAIN_BYTES
        assert key == pytest.private_key_bytes

    def test_missing_cert_provider_command(self):
        with pytest.raises(ValueError):
            assert _mtls_helper.get_client_ssl_credentials(
                CONTEXT_AWARE_METADATA_NO_CERT_PROVIDER_COMMAND
            )

    @mock.patch("subprocess.Popen", autospec=True)
    def test_missing_cert(self, mock_popen):
        mock_popen.return_value = self.create_mock_process(
            pytest.private_key_bytes, b""
        )
        with pytest.raises(ValueError):
            assert _mtls_helper.get_client_ssl_credentials(CONTEXT_AWARE_METADATA)

    @mock.patch("subprocess.Popen", autospec=True)
    def test_missing_key(self, mock_popen):
        mock_popen.return_value = self.create_mock_process(
            pytest.public_cert_bytes, b""
        )
        with pytest.raises(ValueError):
            assert _mtls_helper.get_client_ssl_credentials(CONTEXT_AWARE_METADATA)

    @mock.patch("subprocess.Popen", autospec=True)
    def test_cert_provider_returns_error(self, mock_popen):
        mock_popen.return_value = self.create_mock_process(b"", b"some error")
        mock_popen.return_value.returncode = 1
        with pytest.raises(RuntimeError):
            assert _mtls_helper.get_client_ssl_credentials(CONTEXT_AWARE_METADATA)

    @mock.patch("subprocess.Popen", autospec=True)
    def test_popen_raise_exception(self, mock_popen):
        mock_popen.side_effect = OSError()
        with pytest.raises(OSError):
            assert _mtls_helper.get_client_ssl_credentials(CONTEXT_AWARE_METADATA)


class TestGetClientCertAndKey(object):
    def test_callback_success(self):
        callback = mock.Mock()
        callback.return_value = (pytest.public_cert_bytes, pytest.private_key_bytes)

        found_cert_key, cert, key = _mtls_helper.get_client_cert_and_key(callback)
        assert found_cert_key
        assert cert == pytest.public_cert_bytes
        assert key == pytest.private_key_bytes

    @mock.patch(
        "google.auth.transport._mtls_helper._check_dca_metadata_path", autospec=True
    )
    def test_no_metadata(self, mock_check_dca_metadata_path):
        mock_check_dca_metadata_path.return_value = None

        found_cert_key, cert, key = _mtls_helper.get_client_cert_and_key()
        assert not found_cert_key

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_ssl_credentials", autospec=True
    )
    @mock.patch(
        "google.auth.transport._mtls_helper._check_dca_metadata_path", autospec=True
    )
    def test_use_metadata(
        self, mock_check_dca_metadata_path, mock_get_client_ssl_credentials
    ):
        mock_check_dca_metadata_path.return_value = os.path.join(
            pytest.data_dir, "context_aware_metadata.json"
        )
        mock_get_client_ssl_credentials.return_value = (
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        found_cert_key, cert, key = _mtls_helper.get_client_cert_and_key()
        assert found_cert_key
        assert cert == pytest.public_cert_bytes
        assert key == pytest.private_key_bytes
