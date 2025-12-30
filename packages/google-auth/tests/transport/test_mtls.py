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

from unittest import mock

import pytest  # type: ignore

from google.auth import exceptions
from google.auth.transport import _mtls_helper
from google.auth.transport import mtls


@mock.patch("google.auth.transport._mtls_helper._check_config_path")
def test_has_default_client_cert_source_with_context_aware_metadata(mock_check):
    """
    Directly tests the logic: if CONTEXT_AWARE_METADATA_PATH is found, return True.
    """

    # Setup: Return a path only for the Context Aware Metadata Path
    def side_effect(path):
        if path == _mtls_helper.CONTEXT_AWARE_METADATA_PATH:
            return "/path/to/context_aware_metadata.json"
        return None

    mock_check.side_effect = side_effect

    # Execute
    result = mtls.has_default_client_cert_source()

    # Assert
    assert result is True
    mock_check.assert_any_call(_mtls_helper.CONTEXT_AWARE_METADATA_PATH)
    assert side_effect("non-matching-path") is None


@mock.patch("google.auth.transport._mtls_helper._check_config_path")
def test_has_default_client_cert_source_falls_back(mock_check):
    """
    Tests that it skips CONTEXT_AWARE_METADATA_PATH if None, and checks the next path.
    """

    # Setup: First path is None, second path is valid
    def side_effect(path):
        if path == _mtls_helper.CERTIFICATE_CONFIGURATION_DEFAULT_PATH:
            return "/path/to/default_cert.json"
        return None

    mock_check.side_effect = side_effect

    # Execute
    result = mtls.has_default_client_cert_source()

    # Assert
    assert result is True
    # Verify the sequence of calls
    expected_calls = [
        mock.call(_mtls_helper.CONTEXT_AWARE_METADATA_PATH),
        mock.call(_mtls_helper.CERTIFICATE_CONFIGURATION_DEFAULT_PATH),
    ]
    mock_check.assert_has_calls(expected_calls)


@mock.patch("google.auth.transport.mtls.getenv", autospec=True)
@mock.patch("google.auth.transport._mtls_helper._check_config_path", autospec=True)
def test_has_default_client_cert_source_env_var_success(check_config_path, mock_getenv):
    # 1. Mock getenv to return our test path
    mock_getenv.side_effect = (
        lambda var: "path/to/cert.json"
        if var == "GOOGLE_API_CERTIFICATE_CONFIG"
        else None
    )

    # 2. Mock _check_config_path side effect
    def side_effect(path):
        # Return None for legacy paths to ensure we reach the env var logic
        if path == "path/to/cert.json":
            return "/absolute/path/to/cert.json"
        return None

    check_config_path.side_effect = side_effect

    # 3. This should now return True
    assert mtls.has_default_client_cert_source()

    # 4. Verify the env var path was checked
    check_config_path.assert_called_with("path/to/cert.json")


@mock.patch("google.auth.transport.mtls.getenv", autospec=True)
@mock.patch("google.auth.transport._mtls_helper._check_config_path", autospec=True)
def test_has_default_client_cert_source_env_var_invalid_config_path(
    check_config_path, mock_getenv
):
    # Set the env var but make the check fail
    mock_getenv.side_effect = (
        lambda var: "invalid/path" if var == "GOOGLE_API_CERTIFICATE_CONFIG" else None
    )
    check_config_path.return_value = None

    assert not mtls.has_default_client_cert_source()


@mock.patch("google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True)
@mock.patch("google.auth.transport.mtls.has_default_client_cert_source", autospec=True)
def test_default_client_cert_source(
    has_default_client_cert_source, get_client_cert_and_key
):
    # Test default client cert source doesn't exist.
    has_default_client_cert_source.return_value = False
    with pytest.raises(exceptions.MutualTLSChannelError):
        mtls.default_client_cert_source()

    # The following tests will assume default client cert source exists.
    has_default_client_cert_source.return_value = True

    # Test good callback.
    get_client_cert_and_key.return_value = (True, b"cert", b"key")
    callback = mtls.default_client_cert_source()
    assert callback() == (b"cert", b"key")

    # Test bad callback which throws exception.
    get_client_cert_and_key.side_effect = ValueError()
    callback = mtls.default_client_cert_source()
    with pytest.raises(exceptions.MutualTLSChannelError):
        callback()


@mock.patch(
    "google.auth.transport._mtls_helper.get_client_ssl_credentials", autospec=True
)
@mock.patch("google.auth.transport.mtls.has_default_client_cert_source", autospec=True)
def test_default_client_encrypted_cert_source(
    has_default_client_cert_source, get_client_ssl_credentials
):
    # Test default client cert source doesn't exist.
    has_default_client_cert_source.return_value = False
    with pytest.raises(exceptions.MutualTLSChannelError):
        mtls.default_client_encrypted_cert_source("cert_path", "key_path")

    # The following tests will assume default client cert source exists.
    has_default_client_cert_source.return_value = True

    # Test good callback.
    get_client_ssl_credentials.return_value = (True, b"cert", b"key", b"passphrase")
    callback = mtls.default_client_encrypted_cert_source("cert_path", "key_path")
    with mock.patch("{}.open".format(__name__), return_value=mock.MagicMock()):
        assert callback() == ("cert_path", "key_path", b"passphrase")

    # Test bad callback which throws exception.
    get_client_ssl_credentials.side_effect = exceptions.ClientCertError()
    callback = mtls.default_client_encrypted_cert_source("cert_path", "key_path")
    with pytest.raises(exceptions.MutualTLSChannelError):
        callback()


@mock.patch("google.auth.transport._mtls_helper.check_use_client_cert", autospec=True)
def test_should_use_client_cert(check_use_client_cert):
    check_use_client_cert.return_value = mock.Mock()
    assert mtls.should_use_client_cert()

    check_use_client_cert.return_value = False
    assert not mtls.should_use_client_cert()
