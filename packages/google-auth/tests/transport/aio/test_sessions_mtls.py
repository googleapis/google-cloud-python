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
            assert session._cached_cert == b"fake_cert_data"
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
        bad_config = {"version": 1, "cert_configs": {"workload": {}}}
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists") as mock_exists,
            mock.patch(
                "builtins.open", mock.mock_open(read_data=json.dumps(bad_config))
            ),
        ):
            mock_exists.return_value = True
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            with pytest.raises(exceptions.MutualTLSChannelError):
                await session.configure_mtls_channel()
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_mock_callback(self):
        """Tests that passing a direct callback bypasses the metadata config file."""

        def custom_callback():
            return b"custom_cert", b"custom_key"

        with (
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

            await session.configure_mtls_channel(client_cert_callback=custom_callback)

            assert session._is_mtls is True
            assert session._cached_cert == b"custom_cert"
            mock_make_context.assert_called_once_with(b"custom_cert", b"custom_key")
            mock_connector.assert_called_once_with(ssl=mock_context)
            mock_session.assert_called_once_with(connector=mock_connector.return_value)
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_custom_request(self):
        """Tests that a custom auth_request is properly initialized with mTLS."""
        mock_custom_request = mock.AsyncMock(spec=transport.AsyncRequest)
        mock_custom_request.configure_mtls_channel = mock.AsyncMock()
        mock_custom_request.close = mock.AsyncMock()

        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_custom_request
        )

        def custom_callback():
            return b"custom_cert", b"custom_key"

        await session.configure_mtls_channel(client_cert_callback=custom_callback)

        assert session._is_mtls is True
        mock_custom_request.configure_mtls_channel.assert_called_once_with(
            custom_callback
        )
        await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_exception_resets_flag(self):
        """Tests that if an unexpected error occurs, _is_mtls stays False."""
        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists", return_value=True),
            mock.patch(
                "builtins.open",
                mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG)),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                side_effect=Exception("Unexpected boom!"),
            ),
        ):
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            with pytest.raises(exceptions.MutualTLSChannelError):
                await session.configure_mtls_channel()

            assert session._is_mtls is False
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_transport_error_resets_flag(self):
        """Tests that if custom auth_request raises an error, _is_mtls stays False."""
        mock_custom_request = mock.AsyncMock(spec=transport.AsyncRequest)
        mock_custom_request.configure_mtls_channel = mock.AsyncMock(
            side_effect=exceptions.TransportError("Boom!")
        )
        mock_custom_request.close = mock.AsyncMock()

        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_custom_request
        )

        def custom_callback():
            return b"custom_cert", b"custom_key"

        with pytest.raises(exceptions.TransportError):
            await session.configure_mtls_channel(client_cert_callback=custom_callback)

        assert session._is_mtls is False
        await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_atomic_on_exception(self):
        """Tests that an exception during channel creation leaves the previous auth_request intact."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_original_auth_request = mock.AsyncMock(spec=transport.AsyncRequest)
        mock_original_auth_request.close = mock.AsyncMock()

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_original_auth_request
        )

        with (
            mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}),
            mock.patch("os.path.exists", return_value=True),
            mock.patch(
                "builtins.open",
                mock.mock_open(read_data=json.dumps(VALID_WORKLOAD_CONFIG)),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(True, b"fake_cert_data", b"fake_key_data"),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                side_effect=Exception("Failed to make SSL context"),
            ),
        ):
            with pytest.raises(exceptions.MutualTLSChannelError):
                await session.configure_mtls_channel()

            assert session._is_mtls is False
            assert session._auth_request is mock_original_auth_request
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_close_exception_does_not_abort(self):
        """Tests that an exception in old_auth_request.close() during eviction does not abort configuration."""
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

            # Drive configure_mtls_channel 3 times with failing transports to exercise eviction loop (maxlen=2)
            for i in range(3):
                failing_req = mock.AsyncMock()
                failing_req.close.side_effect = Exception(f"Failed to close session {i}")
                session._auth_request = failing_req
                session._mtls_init_task = None
                await session.configure_mtls_channel()

            assert session._is_mtls is True
            assert session._cached_cert == b"fake_cert_data"
            await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_failure_raises_error(self):
        """Verifies that an error in configure_mtls_channel raises MutualTLSChannelError."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_auth_req = mock.AsyncMock()
        mock_resp = mock.Mock()
        mock_resp.status_code = http_client.UNAUTHORIZED
        mock_resp.close = mock.AsyncMock()
        mock_auth_req.return_value = mock_resp

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
            mock_resp.close.assert_called_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_check_params_fails(self):
        """Verifies that a failure during parameter checking falls back to the original response."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_auth_req = mock.AsyncMock()
        mock_resp = mock.Mock()
        mock_resp.status_code = http_client.UNAUTHORIZED
        mock_resp.close = mock.AsyncMock()
        mock_auth_req.return_value = mock_resp

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"cached_cert"

        with mock.patch(
            "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
            new_callable=mock.AsyncMock,
            side_effect=exceptions.ClientCertError("check_params failed"),
        ) as mock_check_params:
            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )
            assert resp == mock_resp
            mock_check_params.assert_called_once()
            mock_creds.refresh.assert_called_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_no_cert_rotation_when_cert_matches_and_mtls_enabled(self):
        """Verifies that if the fingerprint has not changed, reconfiguration is skipped."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_auth_req = mock.AsyncMock()
        mock_resp = mock.Mock()
        mock_resp.status_code = http_client.UNAUTHORIZED
        mock_resp.close = mock.AsyncMock()
        mock_auth_req.return_value = mock_resp

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
            mock_check.return_value = (
                b"new_cert",
                b"new_key",
                b"same_fp",
                b"same_fp",
            )

            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )

            assert resp == mock_resp
            mock_check.assert_called_once()
            mock_conf.assert_not_called()
            mock_creds.refresh.assert_called_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_success_and_retry(self):
        """Verifies successful cert rotation, channel reconfiguration, and request retry."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_401.close = mock.AsyncMock()

        mock_resp_200 = mock.Mock()
        mock_resp_200.status_code = http_client.OK
        mock_resp_200.close = mock.AsyncMock()

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
            mock_conf.assert_called_once()
            cb = (
                mock_conf.call_args.args[0]
                if mock_conf.call_args.args
                else mock_conf.call_args.kwargs["client_cert_callback"]
            )
            assert cb() == (new_cert, new_key)
            mock_creds.refresh.assert_called_once()
            assert mock_auth_req.call_count == 2
            mock_resp_401.close.assert_called_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_lock_contention(self):
        """Verifies that concurrent requests serialize mTLS check and skip redundant checks."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401_1 = mock.Mock()
        mock_resp_401_1.status_code = http_client.UNAUTHORIZED
        mock_resp_401_1.close = mock.AsyncMock()

        mock_resp_401_2 = mock.Mock()
        mock_resp_401_2.status_code = http_client.UNAUTHORIZED
        mock_resp_401_2.close = mock.AsyncMock()

        mock_resp_200_1 = mock.Mock()
        mock_resp_200_1.status_code = http_client.OK
        mock_resp_200_1.close = mock.AsyncMock()

        mock_resp_200_2 = mock.Mock()
        mock_resp_200_2.status_code = http_client.OK
        mock_resp_200_2.close = mock.AsyncMock()

        mock_auth_req = mock.AsyncMock(
            side_effect=[
                mock_resp_401_1,
                mock_resp_401_2,
                mock_resp_200_1,
                mock_resp_200_2,
            ]
        )

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        async def slow_check(*args, **kwargs):
            await asyncio.sleep(0.05)
            return (b"new", b"new", b"old_fp", b"new_fp")

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                side_effect=slow_check,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            results = await asyncio.gather(
                session.request("GET", "https://pubsub.mtls.googleapis.com/test1"),
                session.request("GET", "https://pubsub.mtls.googleapis.com/test2"),
            )

            assert results == [mock_resp_200_1, mock_resp_200_2]
            assert mock_check.call_count == 1
            assert mock_conf.call_count == 1
            assert mock_creds.refresh.call_count == 1

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_lock_contention_no_cert_change(self):
        """Verifies lock contention when certificates have not changed."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401_1 = mock.Mock()
        mock_resp_401_1.status_code = http_client.UNAUTHORIZED
        mock_resp_401_1.close = mock.AsyncMock()

        mock_resp_401_2 = mock.Mock()
        mock_resp_401_2.status_code = http_client.UNAUTHORIZED
        mock_resp_401_2.close = mock.AsyncMock()

        mock_resp_200_1 = mock.Mock()
        mock_resp_200_1.status_code = http_client.OK
        mock_resp_200_1.close = mock.AsyncMock()

        mock_resp_200_2 = mock.Mock()
        mock_resp_200_2.status_code = http_client.OK
        mock_resp_200_2.close = mock.AsyncMock()

        mock_auth_req = mock.AsyncMock(
            side_effect=[
                mock_resp_401_1,
                mock_resp_401_2,
                mock_resp_200_1,
                mock_resp_200_2,
            ]
        )

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )
        session._is_mtls = True
        session._cached_cert = b"old_cert"

        async def slow_check(*args, **kwargs):
            await asyncio.sleep(0.05)
            return (b"new", b"new", b"same_fp", b"same_fp")

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                side_effect=slow_check,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            results = await asyncio.gather(
                session.request("GET", "https://pubsub.mtls.googleapis.com/test1"),
                session.request("GET", "https://pubsub.mtls.googleapis.com/test2"),
            )

            assert results == [mock_resp_200_1, mock_resp_200_2]
            assert mock_check.call_count == 1
            assert mock_conf.call_count == 0
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
        mock_resp_401.close = mock.AsyncMock()

        mock_resp_200 = mock.Mock()
        mock_resp_200.status_code = http_client.OK
        mock_resp_200.close = mock.AsyncMock()

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
            mock_conf.assert_called_once()
            cb = (
                mock_conf.call_args.args[0]
                if mock_conf.call_args.args
                else mock_conf.call_args.kwargs["client_cert_callback"]
            )
            assert cb() == (new_cert, new_key)

        await session.close()

    @pytest.mark.asyncio
    async def test_non_mtls_url_bypasses_rotation(self):
        """Verifies that standard non-mTLS URLs bypass certificate rotation."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_401.close = mock.AsyncMock()

        mock_resp_200 = mock.Mock()
        mock_resp_200.status_code = http_client.OK
        mock_resp_200.close = mock.AsyncMock()

        mock_auth_req = mock.AsyncMock(side_effect=[mock_resp_401, mock_resp_200])

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
            resp = await session.request("GET", "https://pubsub.googleapis.com/test")

            assert resp == mock_resp_200
            mock_check.assert_not_called()
            mock_conf.assert_not_called()
            mock_creds.refresh.assert_called_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_skips_retry_for_streaming(self):
        """Verifies that streaming requests skip retry on 401 and return the response."""
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

        def data_gen():
            yield b"part1"
            yield b"part2"

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
                "POST", "https://pubsub.mtls.googleapis.com/test", data=data_gen()
            )

            assert resp == mock_resp
            mock_check.assert_called_once()
            mock_conf.assert_called_once()
            mock_creds.refresh.assert_called_once()
            assert mock_auth_req.call_count == 1
            mock_resp.close.assert_not_called()

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
            await session.request("GET", "https://example.com", max_allowed_time=0.1)

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
