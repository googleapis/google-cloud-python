# Copyright 2026 Google LLC
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

import json
import os
import ssl
from unittest import mock

import pytest

from google.auth import exceptions
from google.auth.aio import credentials
from google.auth.aio.transport import sessions

# This is the valid "workload" format the library expects
VALID_WORKLOAD_CONFIG = {
    "version": 1,
    "cert_configs": {
        "workload": {"cert_path": "/tmp/mock_cert.pem", "key_path": "/tmp/mock_key.pem"}
    },
}


class TestSessionsMtls:
    @pytest.mark.asyncio
    async def test_configure_mtls_channel(self):
        """
        Tests that the mTLS channel configures correctly when a
        valid workload config is mocked.
        """
        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}
        ), mock.patch("os.path.exists") as mock_exists, mock.patch(
            "builtins.open", mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG))
        ), mock.patch(
            "google.auth.aio.transport.mtls.get_client_cert_and_key"
        ) as mock_helper, mock.patch(
            "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
        ) as mock_make_context:
            mock_exists.return_value = True
            mock_helper.return_value = (True, b"fake_cert_data", b"fake_key_data")

            mock_context = mock.Mock(spec=ssl.SSLContext)
            mock_make_context.return_value = mock_context

            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            await session.configure_mtls_channel()

            assert session._is_mtls is True
            mock_make_context.assert_called_once_with(
                b"fake_cert_data", b"fake_key_data"
            )

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_disabled(self):
        """
        Tests behavior when the config file does not exist.
        """
        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}
        ), mock.patch("os.path.exists") as mock_exists:
            mock_exists.return_value = False
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            await session.configure_mtls_channel()

            # If the file doesn't exist, it shouldn't error; it just won't use mTLS
            assert session._is_mtls is False

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_invalid_format(self):
        """
        Verifies that the MutualTLSChannelError is raised for bad formats.
        """
        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}
        ), mock.patch("os.path.exists") as mock_exists, mock.patch(
            "builtins.open", mock.mock_open(read_data='{"invalid": "format"}')
        ):
            mock_exists.return_value = True
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            with pytest.raises(exceptions.MutualTLSChannelError):
                await session.configure_mtls_channel()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_mock_callback(self):
        """
        Tests mTLS configuration using bytes-returning callback.
        """

        def mock_callback():
            return (b"fake_cert_bytes", b"fake_key_bytes")

        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}
        ), mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ), mock.patch(
            "ssl.SSLContext.load_cert_chain"
        ):
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            await session.configure_mtls_channel(client_cert_callback=mock_callback)

            assert session._is_mtls is True
