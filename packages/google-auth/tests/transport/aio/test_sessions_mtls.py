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
from google.auth.aio import transport
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
        ) as mock_make_context, mock.patch(
            "aiohttp.TCPConnector"
        ) as mock_connector, mock.patch(
            "aiohttp.ClientSession"
        ) as mock_session:
            mock_session.return_value.close = mock.AsyncMock()
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
            mock_connector.assert_called_once_with(ssl=mock_context)
            mock_session.assert_called_once_with(connector=mock_connector.return_value)
            await session.close()

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
            assert session._is_mtls is False
            await session.close()

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
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_invalud_fields(self):
        """
        If cert is missing expected keys, it should fail gracefully
        """
        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}
        ), mock.patch("os.path.exists") as mock_exists, mock.patch(
            "builtins.open", mock.mock_open(read_data='{"cert_configs": {}}')
        ):
            mock_exists.return_value = True
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)
            await session.configure_mtls_channel()
            assert session._is_mtls is False
            await session.close()

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
            "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
        ) as mock_make_context, mock.patch(
            "aiohttp.TCPConnector"
        ) as mock_connector, mock.patch(
            "aiohttp.ClientSession"
        ) as mock_session:
            mock_session.return_value.close = mock.AsyncMock()
            mock_context = mock.Mock(spec=ssl.SSLContext)
            mock_make_context.return_value = mock_context

            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            await session.configure_mtls_channel(client_cert_callback=mock_callback)

            assert session._is_mtls is True
            mock_make_context.assert_called_once_with(
                b"fake_cert_bytes", b"fake_key_bytes"
            )
            mock_connector.assert_called_once_with(ssl=mock_context)
            mock_session.assert_called_once_with(connector=mock_connector.return_value)
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_custom_request(self):
        """Tests that if _auth_request is not an AiohttpRequest, _is_mtls is set to False
        because we can't configure the custom request with mTLS.
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
            mock_auth_request = mock.AsyncMock(spec=transport.Request)
            session = sessions.AsyncAuthorizedSession(
                mock_creds, auth_request=mock_auth_request
            )

            with pytest.warns(UserWarning, match="Attempted to establish mTLS"):
                await session.configure_mtls_channel()

            # If the request handler is not an AiohttpRequest, the library cannot configure
            # the connection to use mTLS, so _is_mtls must be False to reflect this unconfigured state.
            assert session._is_mtls is False
            mock_make_context.assert_not_called()
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_exception_resets_flag(self):
        """
        Tests that self._is_mtls is reset to False if an exception is raised
        during configuration.
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
            mock_make_context.side_effect = exceptions.ClientCertError("Mock error")

            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            with pytest.raises(exceptions.MutualTLSChannelError):
                await session.configure_mtls_channel()

            assert session._is_mtls is False
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_transport_error_resets_flag(self):
        """
        Tests that self._is_mtls is reset to False if a TransportError is raised
        during configuration.
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
            mock_make_context.side_effect = exceptions.TransportError("Mock error")

            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            with pytest.raises(exceptions.MutualTLSChannelError):
                await session.configure_mtls_channel()

            assert session._is_mtls is False
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_atomic_on_exception(self):
        """
        Tests that if configure_mtls_channel has already successfully configured mTLS,
        a subsequent attempt that raises an exception will preserve the original mTLS state.
        """
        # Step 1: Successful configuration
        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}
        ), mock.patch("os.path.exists") as mock_exists, mock.patch(
            "builtins.open", mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG))
        ), mock.patch(
            "google.auth.aio.transport.mtls.get_client_cert_and_key"
        ) as mock_helper, mock.patch(
            "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
        ) as mock_make_context, mock.patch(
            "aiohttp.TCPConnector"
        ), mock.patch(
            "aiohttp.ClientSession"
        ) as mock_session:
            mock_session.return_value.close = mock.AsyncMock()
            mock_exists.return_value = True
            mock_helper.return_value = (True, b"fake_cert_data_1", b"fake_key_data_1")

            mock_context = mock.Mock(spec=ssl.SSLContext)
            mock_make_context.return_value = mock_context

            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            await session.configure_mtls_channel()
            assert session._is_mtls is True
            assert session._cached_cert == b"fake_cert_data_1"
            first_auth_request = session._auth_request

            # Step 2: Failed subsequent configuration attempt
            # Reset task so we trigger a new configuration run
            session._mtls_init_task = None

            # Patch context generator to fail this time
            mock_make_context.side_effect = exceptions.ClientCertError("Mock error")

            with pytest.raises(exceptions.MutualTLSChannelError):
                await session.configure_mtls_channel()

            # Verify that the state remains unchanged from the first successful configuration
            assert session._is_mtls is True
            assert session._cached_cert == b"fake_cert_data_1"
            assert session._auth_request is first_auth_request
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_close_exception_does_not_abort(self):
        """
        Tests that if old_auth_request.close() raises an exception, the mTLS
        configuration is still considered successful, and is_mtls remains True
        without raising MutualTLSChannelError.
        """
        with mock.patch.dict(
            os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}
        ), mock.patch("os.path.exists") as mock_exists, mock.patch(
            "builtins.open", mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG))
        ), mock.patch(
            "google.auth.aio.transport.mtls.get_client_cert_and_key"
        ) as mock_helper, mock.patch(
            "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
        ) as mock_make_context, mock.patch(
            "aiohttp.TCPConnector"
        ), mock.patch(
            "aiohttp.ClientSession"
        ) as mock_session:
            mock_session.return_value.close = mock.AsyncMock()
            mock_exists.return_value = True
            mock_helper.return_value = (True, b"fake_cert_data", b"fake_key_data")

            mock_context = mock.Mock(spec=ssl.SSLContext)
            mock_make_context.return_value = mock_context

            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            # Mock close() of the initial self._auth_request to raise an exception
            session._auth_request.close = mock.AsyncMock(
                side_effect=Exception("Mock close error")
            )

            # Should complete successfully without raising MutualTLSChannelError
            await session.configure_mtls_channel()

            assert session._is_mtls is True
            assert session._cached_cert == b"fake_cert_data"
            await session.close()
