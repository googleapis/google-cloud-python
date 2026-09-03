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

import asyncio
import http.client as http_client
import json
import os
import ssl
from unittest import mock

import pytest

from google.auth import exceptions
from google.auth.aio import credentials
from google.auth.aio import transport
from google.auth.aio.transport import sessions
from google.auth.exceptions import TimeoutError

# This is the valid "workload" format the library expects
VALID_WORKLOAD_CONFIG = {
    "version": 1,
    "cert_configs": {
        "workload": {
            "cert_path": "/tmp/mock_cert.pem",
            "key_path": "/tmp/mock_key.pem",
        }
    },
}


class TestSessionsMtls:
    @pytest.mark.asyncio
    async def test_configure_mtls_channel(self):
        """Tests that the mTLS channel configures correctly when a valid workload config is mocked."""
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists") as mock_exists,
            mock.patch(
                "builtins.open",
                mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG)),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key"
            ) as mock_helper,
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
            ) as mock_make_context,
            mock.patch("aiohttp.TCPConnector") as mock_connector,
            mock.patch("aiohttp.ClientSession") as mock_session,
        ):
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
        """Tests behavior when the config file does not exist."""
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists") as mock_exists,
        ):
            mock_exists.return_value = False
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)
            await session.configure_mtls_channel()
            assert session._is_mtls is False
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_invalid_format(self):
        """Verifies that the MutualTLSChannelError is raised for bad formats."""
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists") as mock_exists,
            mock.patch(
                "builtins.open", mock.mock_open(read_data='{"invalid": "format"}')
            ),
        ):
            mock_exists.return_value = True
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            with pytest.raises(exceptions.MutualTLSChannelError):
                await session.configure_mtls_channel()
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_invalid_fields(self):
        """If cert is missing expected keys, it should fail gracefully."""
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists") as mock_exists,
            mock.patch(
                "builtins.open", mock.mock_open(read_data='{"cert_configs": {}}')
            ),
        ):
            mock_exists.return_value = True
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)
            await session.configure_mtls_channel()
            assert session._is_mtls is False
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_mock_callback(self):
        """Tests mTLS configuration using bytes-returning callback."""

        def mock_callback():
            return (b"fake_cert_bytes", b"fake_key_bytes")

        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
            ) as mock_make_context,
            mock.patch("aiohttp.TCPConnector") as mock_connector,
            mock.patch("aiohttp.ClientSession") as mock_session,
        ):
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
        """Tests that if _auth_request is not an AiohttpRequest, _is_mtls is set to False."""
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists") as mock_exists,
            mock.patch(
                "builtins.open",
                mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG)),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key"
            ) as mock_helper,
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
            ) as mock_make_context,
        ):
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

            assert session._is_mtls is False
            mock_make_context.assert_not_called()
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_exception_resets_flag(self):
        """Tests that self._is_mtls is reset to False if an exception is raised during configuration."""
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists") as mock_exists,
            mock.patch(
                "builtins.open",
                mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG)),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key"
            ) as mock_helper,
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
            ) as mock_make_context,
        ):
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
        """Tests that self._is_mtls is reset to False if a TransportError is raised."""
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists") as mock_exists,
            mock.patch(
                "builtins.open",
                mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG)),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key"
            ) as mock_helper,
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
            ) as mock_make_context,
        ):
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
        """Tests that if configure_mtls_channel already succeeded, a subsequent failure preserves state."""
        # Step 1: Successful configuration
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists") as mock_exists,
            mock.patch(
                "builtins.open",
                mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG)),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key"
            ) as mock_helper,
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
            ) as mock_make_context,
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession") as mock_session,
        ):
            mock_session.return_value.close = mock.AsyncMock()
            mock_exists.return_value = True
            mock_helper.return_value = (
                True,
                b"fake_cert_data_1",
                b"fake_key_data_1",
            )

            mock_context = mock.Mock(spec=ssl.SSLContext)
            mock_make_context.return_value = mock_context

            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            await session.configure_mtls_channel()
            assert session._is_mtls is True
            assert session._cached_cert == b"fake_cert_data_1"
            first_auth_request = session._auth_request

            # Step 2: Failed subsequent configuration attempt
            session._mtls_init_task = None
            mock_make_context.side_effect = exceptions.ClientCertError("Mock error")

            with pytest.raises(exceptions.MutualTLSChannelError):
                await session.configure_mtls_channel()

            assert session._is_mtls is True
            assert session._cached_cert == b"fake_cert_data_1"
            assert session._auth_request is first_auth_request
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_close_exception_does_not_abort(self):
        """Tests that an exception in old_auth_request.close() does not abort configuration."""
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists") as mock_exists,
            mock.patch(
                "builtins.open",
                mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG)),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key"
            ) as mock_helper,
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context"
            ) as mock_make_context,
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession") as mock_session,
        ):
            mock_session.return_value.close = mock.AsyncMock()
            mock_exists.return_value = True
            mock_helper.return_value = (True, b"fake_cert_data", b"fake_key_data")

            mock_context = mock.Mock(spec=ssl.SSLContext)
            mock_make_context.return_value = mock_context

            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            session._auth_request.close = mock.AsyncMock(
                side_effect=Exception("Mock close error")
            )

            await session.configure_mtls_channel()

            assert session._is_mtls is True
            assert session._cached_cert == b"fake_cert_data"
            await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_failure_raises_error(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)

        mock_resp = mock.Mock()
        mock_resp.status_code = http_client.UNAUTHORIZED
        mock_auth_req = mock.AsyncMock(return_value=mock_resp)

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        new_cert = b"new_cert"
        new_key = b"new_key"

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            mock_check.return_value = (new_cert, new_key, b"old_fp", b"new_fp")
            mock_conf.side_effect = Exception("Failed to reconfigure")

            with pytest.raises(exceptions.MutualTLSChannelError):
                await session.request("GET", "https://pubsub.mtls.googleapis.com/test")

            mock_check.assert_called_once()
            mock_conf.assert_called_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_check_params_fails(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock()

        mock_resp = mock.Mock()
        mock_resp.status_code = http_client.UNAUTHORIZED
        mock_auth_req = mock.AsyncMock(return_value=mock_resp)

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            mock_check.side_effect = exceptions.MutualTLSChannelError(
                "Failed to check params"
            )

            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )

            assert resp == mock_resp
            mock_check.assert_called_once()
            mock_creds.refresh.assert_not_called()
            mock_conf.assert_not_called()

        await session.close()

    @pytest.mark.asyncio
    async def test_no_cert_rotation_when_cert_matches_and_mtls_enabled(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_401.close = mock.AsyncMock()

        mock_resp_200 = mock.Mock()
        mock_resp_200.status_code = http_client.OK

        # 401 on initial request, 200 on retry after refresh
        mock_auth_req = mock.AsyncMock(side_effect=[mock_resp_401, mock_resp_200])

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        new_cert = b"new_cert"
        new_key = b"new_key"

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            # Matching fingerprints mean no mTLS rotation is needed
            mock_check.return_value = (new_cert, new_key, b"old_fp", b"old_fp")

            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )

            assert resp == mock_resp_200
            mock_check.assert_called_once()
            mock_conf.assert_not_called()
            mock_creds.refresh.assert_called_once()
            assert mock_auth_req.call_count == 2
            mock_resp_401.close.assert_awaited_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_success_and_retry(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_200 = mock.Mock()
        mock_resp_200.status_code = http_client.OK

        mock_auth_req = mock.AsyncMock(side_effect=[mock_resp_401, mock_resp_200])

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        new_cert = b"new_cert"
        new_key = b"new_key"

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            mock_check.return_value = (new_cert, new_key, b"old_fp", b"new_fp")

            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )

            assert resp == mock_resp_200
            mock_check.assert_called_once()
            mock_conf.assert_called_once_with(mock.ANY)
            mock_creds.refresh.assert_called_once()
            assert mock_creds.before_request.call_count == 2

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_lock_contention(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED

        mock_resp_200 = mock.Mock()
        mock_resp_200.status_code = http_client.OK

        mock_auth_req = mock.AsyncMock(
            side_effect=[mock_resp_401] * 3 + [mock_resp_200] * 3
        )

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        new_cert = b"new_cert"
        new_key = b"new_key"

        async def mock_configure_mtls_channel(*args, **kwargs):
            await asyncio.sleep(0.01)
            session._cached_cert = new_cert

        async def mock_check_side_effect(cached_cert, callback=None):
            if cached_cert == b"old_cert":
                return (new_cert, new_key, b"old_fp", b"new_fp")
            return (new_cert, new_key, b"new_fp", b"new_fp")

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            mock_check.side_effect = mock_check_side_effect
            mock_conf.side_effect = mock_configure_mtls_channel

            tasks = [
                session.request("GET", "https://pubsub.mtls.googleapis.com/test")
                for _ in range(3)
            ]
            responses = await asyncio.gather(*tasks)

        for resp in responses:
            assert resp == mock_resp_200

        mock_check.assert_called_once()
        mock_conf.assert_called_once()
        assert mock_creds.refresh.call_count == 1

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_lock_contention_no_cert_change(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_200 = mock.Mock()
        mock_resp_200.status_code = http_client.OK

        mock_auth_req = mock.AsyncMock(
            side_effect=[mock_resp_401] * 3 + [mock_resp_200] * 3
        )

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        async def mock_check_side_effect(cached_cert, callback=None):
            await asyncio.sleep(0.01)
            return (b"old_cert", b"old_key", b"old_fp", b"old_fp")

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            mock_check.side_effect = mock_check_side_effect

            tasks = [
                session.request("GET", "https://pubsub.mtls.googleapis.com/test")
                for _ in range(3)
            ]
            responses = await asyncio.gather(*tasks)

            for resp in responses:
                assert resp == mock_resp_200

            mock_check.assert_called_once()
            mock_conf.assert_not_called()
            # Concurrent 401s properly deduplicate to 1 refresh
            assert mock_creds.refresh.call_count == 1

        await session.close()

    @pytest.mark.asyncio
    async def test_psc_endpoint_triggers_cert_rotation(self):
        """Verifies that PSC endpoints (*.p.googleapis.com) are recognized as mTLS endpoints."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_200 = mock.Mock()
        mock_resp_200.status_code = http_client.OK

        mock_auth_req = mock.AsyncMock(side_effect=[mock_resp_401, mock_resp_200])

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        new_cert = b"new_cert"
        new_key = b"new_key"

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            mock_check.return_value = (new_cert, new_key, b"old_fp", b"new_fp")

            resp = await session.request("GET", "https://pubsub.p.googleapis.com/test")

            assert resp == mock_resp_200
            mock_check.assert_called_once()
            mock_conf.assert_called_once_with(mock.ANY)

        await session.close()

    @pytest.mark.asyncio
    async def test_non_mtls_url_bypasses_rotation(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_auth_req = mock.AsyncMock(return_value=mock_resp_401)

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )

        session._is_mtls = True
        session._cached_cert = b"old_cert"

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            resp = await session.request("GET", "https://example.com/test")

            assert resp == mock_resp_401
            mock_check.assert_not_called()
            mock_conf.assert_not_called()
            assert mock_creds.refresh.call_count == 2
            assert mock_auth_req.call_count == 3

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_skips_retry_for_streaming(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock()

        mock_resp = mock.Mock()
        mock_resp.status_code = http_client.UNAUTHORIZED
        mock_auth_req = mock.AsyncMock(return_value=mock_resp)

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        class MockStream:
            def read(self):
                pass

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            mock_check.return_value = (b"new", b"new", b"old_fp", b"new_fp")

            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test", data=MockStream()
            )

            assert resp == mock_resp
            mock_conf.assert_called_once()

        mock_creds.refresh.assert_called_once()
        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_credential_refresh_fails(self):
        """Covers the except block for RefreshError when credentials fail to refresh."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(
            side_effect=exceptions.RefreshError("Refresh failed")
        )

        mock_resp = mock.Mock()
        mock_resp.status_code = http_client.UNAUTHORIZED
        mock_auth_req = mock.AsyncMock(return_value=mock_resp)

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ),
        ):
            mock_check.return_value = (b"new", b"new", b"old_fp", b"new_fp")

            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )

            assert resp == mock_resp
            mock_creds.refresh.assert_called_once()
            mock_auth_req.assert_called_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_max_retries_exceeded(self):
        """Covers the `if _auth_retry_count < 2:` max retry limit."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp = mock.Mock()
        mock_resp.status_code = http_client.UNAUTHORIZED
        mock_resp.close = mock.AsyncMock()
        mock_auth_req = mock.AsyncMock(return_value=mock_resp)

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ),
        ):
            mock_check.return_value = (b"new", b"new", b"old_fp", b"new_fp")

            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )

            assert resp == mock_resp
            assert mock_auth_req.call_count == 3
            assert mock_check.call_count == 2
            assert mock_resp.close.call_count == 2

        await session.close()

    @pytest.mark.asyncio
    async def test_session_close_cleans_old_auth_requests(self):
        """Covers the loop in the `close()` method that drains `_old_auth_requests`."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock.AsyncMock()
        )

        mock_old_req_1 = mock.AsyncMock()
        mock_old_req_2 = mock.AsyncMock()
        mock_old_req_3_fails = mock.AsyncMock()
        mock_old_req_3_fails.close.side_effect = Exception("Close error")

        session._old_auth_requests.extend(
            [mock_old_req_1, mock_old_req_2, mock_old_req_3_fails]
        )

        await session.close()

        mock_old_req_1.close.assert_called_once()
        mock_old_req_2.close.assert_called_once()
        mock_old_req_3_fails.close.assert_called_once()
        assert len(session._old_auth_requests) == 0

    @pytest.mark.asyncio
    async def test_request_401_streaming_refreshes_creds_and_returns_open_response(
        self,
    ):
        """Verifies that streaming requests refresh credentials but return the unclosed response."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_401.close = mock.AsyncMock()

        mock_auth_req = mock.AsyncMock(return_value=mock_resp_401)
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )

        streaming_data = (chunk for chunk in [b"chunk1", b"chunk2"])
        response = await session.request(
            "POST", "https://example.com", data=streaming_data
        )

        assert response == mock_resp_401
        mock_creds.refresh.assert_awaited_once()
        mock_resp_401.close.assert_not_called()
        await session.close()

    @pytest.mark.asyncio
    async def test_request_401_closes_response_on_timeout_during_recovery(self):
        """Verifies that response is closed when auth_with_timeout times out during _recover_auth_state."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)

        async def slow_refresh(*args, **kwargs):
            await asyncio.sleep(10)

        mock_creds.refresh = mock.AsyncMock(side_effect=slow_refresh)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_401.close = mock.AsyncMock()

        mock_auth_req = mock.AsyncMock(return_value=mock_resp_401)
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )

        with pytest.raises(TimeoutError):
            await session.request("GET", "https://example.com", max_allowed_time=0.01)

        mock_resp_401.close.assert_awaited_once()
        await session.close()

    @pytest.mark.asyncio
    async def test_request_401_closes_response_on_cancellation(self):
        """Verifies that response is closed and CancelledError propagated if task is cancelled."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)

        refresh_started = asyncio.Event()

        async def cancel_on_refresh(*args, **kwargs):
            refresh_started.set()
            await asyncio.sleep(10)

        mock_creds.refresh = mock.AsyncMock(side_effect=cancel_on_refresh)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_401.close = mock.AsyncMock()

        mock_auth_req = mock.AsyncMock(return_value=mock_resp_401)
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )

        task = asyncio.create_task(session.request("GET", "https://example.com"))
        await refresh_started.wait()
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task

        mock_resp_401.close.assert_awaited_once()
        await session.close()

    @pytest.mark.asyncio
    async def test_request_401_concurrent_refreshes_are_deduplicated(self):
        """Verifies that concurrent 401s execute only one credentials.refresh call."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_401.close = mock.AsyncMock()

        mock_resp_200 = mock.Mock()
        mock_resp_200.status_code = http_client.OK
        mock_resp_200.close = mock.AsyncMock()

        mock_auth_req = mock.AsyncMock(
            side_effect=[
                mock_resp_401,
                mock_resp_401,
                mock_resp_200,
                mock_resp_200,
            ]
        )
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )

        refresh_count = 0

        async def slow_refresh(*args, **kwargs):
            nonlocal refresh_count
            refresh_count += 1
            await asyncio.sleep(0.05)

        mock_creds.refresh = mock.AsyncMock(side_effect=slow_refresh)

        results = await asyncio.gather(
            session.request("GET", "https://example.com/1"),
            session.request("GET", "https://example.com/2"),
        )

        assert all(r.status_code == 200 for r in results)
        assert refresh_count == 1
        await session.close()
