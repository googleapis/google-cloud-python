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
        callback = mock.AsyncMock(return_value=(b"cert", b"key"))
        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(True, b"cert", b"key"),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ) as mock_make_context,
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession"),
        ):
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)
            await session.configure_mtls_channel(callback)
            assert session.is_mtls is True
            assert session._cached_cert == b"cert"
            mock_make_context.assert_called_once_with(b"cert", b"key")
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_custom_request(self):
        custom_req = mock.AsyncMock(spec=transport.Request)
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        session = sessions.AsyncAuthorizedSession(mock_creds, auth_request=custom_req)
        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(True, b"cert", b"key"),
            ),
            pytest.warns(
                UserWarning,
                match="Attempted to establish mTLS, but a custom async transport was provided",
            ),
        ):
            await session.configure_mtls_channel()
            assert session.is_mtls is False
            assert session._cached_cert is None
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_exception_preserves_flag(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        session = sessions.AsyncAuthorizedSession(mock_creds)
        session._is_mtls = True
        session._cached_cert = b"old_cert"
        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                side_effect=Exception("Disk failure"),
            ),
            pytest.raises(exceptions.MutualTLSChannelError),
        ):
            await session.configure_mtls_channel(lambda: (b"new_cert", b"new_key"))
        assert session.is_mtls is True
        assert session._cached_cert == b"old_cert"
        await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_transport_error_resets_flag(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        session = sessions.AsyncAuthorizedSession(mock_creds)
        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(True, b"cert", b"key"),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.ClientSession", side_effect=Exception("Session error")),
            pytest.raises(exceptions.MutualTLSChannelError),
        ):
            await session.configure_mtls_channel()
        assert session.is_mtls is False
        assert session._cached_cert is None
        await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_atomic_on_exception(self):
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        session = sessions.AsyncAuthorizedSession(mock_creds)
        orig_req = session._auth_request
        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                side_effect=RuntimeError("Fatal error"),
            ),
            pytest.raises(exceptions.MutualTLSChannelError),
        ):
            await session.configure_mtls_channel()
        assert session._auth_request is orig_req
        assert session.is_mtls is False
        await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_close_exception_does_not_abort(self):
        """Tests that an exception in old_auth_request.close() during eviction does not abort configuration."""
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
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession") as mock_session,
        ):
            mock_session.return_value.close = mock.AsyncMock()

            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            # Pre-populate _old_auth_requests with failing transports to test eviction (maxlen >= 2)
            failing_req_1 = mock.AsyncMock()
            failing_req_1.close.side_effect = Exception("Close failure 1")
            failing_req_2 = mock.AsyncMock()
            failing_req_2.close.side_effect = Exception("Close failure 2")
            session._old_auth_requests.extend([failing_req_1, failing_req_2])

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
        """Verifies that a failure during parameter checking falls back to credential refresh and retries."""
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
        session._cached_cert = b"cached_cert"

        with mock.patch(
            "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
            new_callable=mock.AsyncMock,
            side_effect=exceptions.ClientCertError("check_params failed"),
        ) as mock_check_params:
            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )
            assert resp == mock_resp_200
            mock_check_params.assert_called_once()
            mock_creds.refresh.assert_called_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_no_cert_rotation_when_cert_matches_and_mtls_enabled(self):
        """Verifies that if the fingerprint has not changed, reconfiguration is skipped and retry succeeds."""
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
            mock_check.return_value = (
                b"new_cert",
                b"new_key",
                b"same_fp",
                b"same_fp",
            )

            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )

            assert resp == mock_resp_200
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
            # The rotation path passes the rotated cert/key explicitly rather
            # than temporarily swapping the shared `_client_cert_callback`,
            # which must therefore be left untouched.
            assert mock_conf.call_args.kwargs["_cert_key_override"] == (
                new_cert,
                new_key,
            )
            assert session._client_cert_callback is None
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
            # The rotation path passes the rotated cert/key explicitly rather
            # than temporarily swapping the shared `_client_cert_callback`,
            # which must therefore be left untouched.
            assert mock_conf.call_args.kwargs["_cert_key_override"] == (
                new_cert,
                new_key,
            )
            assert session._client_cert_callback is None

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

    @pytest.mark.asyncio
    async def test_cert_rotation_with_completed_mtls_init_task(self):
        """
        Verifies that when _mtls_init_task is already completed, receiving a 401
        with rotated certificates properly resets _mtls_init_task and reconfigures mTLS.
        """
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        # 1. Pre-populate _mtls_init_task with an already completed task
        async def dummy_completed():
            return None

        initial_task = asyncio.create_task(dummy_completed())
        await initial_task
        assert initial_task.done()
        # 2. Mock 401 then 200 responses
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
        session._mtls_init_task = initial_task  # Pre-populate completed task
        new_cert = b"new_cert"
        new_key = b"new_key"

        async def fake_configure(cb=None, **kwargs):
            session._mtls_init_task = asyncio.create_task(dummy_completed())

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", side_effect=fake_configure
            ) as mock_conf,
        ):
            mock_check.return_value = (new_cert, new_key, b"old_fp", b"new_fp")
            # Must use a hostname matching _MTLS_URL_PREFIXES (e.g. *.mtls.googleapis.com)
            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )
            assert resp == mock_resp_200
            mock_conf.assert_called_once()
            # Verify the previous completed task was cleared during rotation
            assert session._mtls_init_task is not initial_task
            mock_creds.refresh.assert_called_once()
            assert mock_auth_req.call_count == 2
        await session.close()

    @pytest.mark.asyncio
    async def test_401_retry_raises_timeout_before_refresh(self):
        """
        Tests that TimeoutError is raised if max_allowed_time expires before
        credentials.refresh can be executed following a 401 response.
        """
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_auth_request = mock.AsyncMock(spec=transport.Request)

        status_access_count = 0

        class _CustomResponse:
            def __init__(self):
                self.close = mock.AsyncMock()

            @property
            def status_code(self):
                nonlocal status_access_count
                status_access_count += 1
                return 401

        mock_resp_401 = _CustomResponse()

        async def fake_auth_request(*args, **kwargs):
            return mock_resp_401

        mock_auth_request.side_effect = fake_auth_request
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_request
        )

        def mock_time():
            if status_access_count >= 2:
                return 100.0
            return 0.1

        with mock.patch(
            "google.auth.aio.transport.sessions.time.monotonic", side_effect=mock_time
        ):
            with pytest.raises(
                exceptions.TimeoutError,
                match="Timeout exceeded before credential refresh could begin",
            ):
                await session.request(
                    "GET", "https://example.com", max_allowed_time=1.0
                )
        # Confirm credentials.refresh was never called
        mock_creds.refresh.assert_not_called()
        await session.close()

    @pytest.mark.asyncio
    async def test_401_retry_raises_timeout_before_subsequent_retry(self):
        """
        Tests that TimeoutError is raised if credentials.refresh succeeds on 401,
        but elapsed time exceeds max_allowed_time before the retried request can execute.
        """
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_auth_request = mock.AsyncMock(spec=transport.Request)
        mock_resp_401 = mock.Mock(spec=transport.Response, status_code=401)
        mock_resp_401.close = mock.AsyncMock()
        mock_auth_request.return_value = mock_resp_401

        async def fake_refresh(auth_request):
            return None

        mock_creds.refresh = mock.AsyncMock(side_effect=fake_refresh)
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_request
        )

        after_refresh_count = 0

        def mock_time():
            nonlocal after_refresh_count
            if mock_creds.refresh.called:
                after_refresh_count += 1
                if after_refresh_count >= 2:
                    return 100.0
            return 0.1

        with mock.patch(
            "google.auth.aio.transport.sessions.time.monotonic", side_effect=mock_time
        ):
            with pytest.raises(
                exceptions.TimeoutError,
                match=r"(Timeout exceeded before retrying the request|Context manager exceeded the configured timeout)",
            ):
                await session.request(
                    "GET", "https://example.com", max_allowed_time=1.0
                )
        # Refresh succeeded once, but subsequent retry was stopped by timeout
        assert mock_creds.refresh.call_count == 1
        assert mock_auth_request.call_count == 1
        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_lock_contention_check_params_fails(self):
        """Verifies lock contention when certificate parameter check raises a handled exception."""
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
        session._cached_cert = b"cached_cert"

        async def slow_failing_check(*args, **kwargs):
            await asyncio.sleep(0.05)
            raise exceptions.ClientCertError("check_params failed")

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                side_effect=slow_failing_check,
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
            assert session._mtls_check_counter == 1
            assert mock_conf.call_count == 0
            assert mock_creds.refresh.call_count == 1

        await session.close()

    @pytest.mark.asyncio
    async def test_no_cert_rotation_when_client_cert_does_not_exist(self):
        """Verifies that if client certificate does not exist, reconfiguration is skipped with proper logging."""
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
            mock.patch.object(sessions._LOGGER, "info") as mock_logger_info,
        ):
            mock_check.return_value = (None, None, None, None)

            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )

            assert resp == mock_resp_200
            mock_check.assert_called_once()
            mock_conf.assert_not_called()
            mock_creds.refresh.assert_called_once()
            mock_logger_info.assert_any_call(
                "Skipping reconfiguration of mTLS channel because the client"
                " certificate does not exist."
            )

        await session.close()

    @pytest.mark.asyncio
    async def test_request_cancellation_propagates_and_leaves_mtls_init_running(self):
        """Verifies that cancelling an in-flight request propagates CancelledError
        to the caller while asyncio.shield preserves self._mtls_init_task running
        in the background.
        """
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_auth_request = mock.AsyncMock(spec=transport.Request)
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_request
        )
        init_started = asyncio.Event()
        init_can_finish = asyncio.Event()

        async def slow_mtls_init():
            init_started.set()
            await init_can_finish.wait()
            session._is_mtls = True

        # Simulate an in-progress mTLS initialization task
        mtls_task = asyncio.create_task(slow_mtls_init())
        session._mtls_init_task = mtls_task
        # Launch an in-flight request that awaits the shielded mTLS task
        req_task = asyncio.create_task(session.request("GET", "https://example.com"))
        # Ensure the mTLS task has started and the request is waiting on it
        await init_started.wait()
        # Yield to event loop to guarantee session.request has reached await asyncio.shield(...)
        await asyncio.sleep(0)
        # Cancel the in-flight request
        req_task.cancel()
        # 1. Verify asyncio.CancelledError is propagated to the request caller
        with pytest.raises(asyncio.CancelledError):
            await req_task
        # 2. Verify self._mtls_init_task was NOT cancelled and is still running
        assert not session._mtls_init_task.cancelled()
        assert not session._mtls_init_task.done()
        # 3. Allow self._mtls_init_task to complete and verify it finishes cleanly
        init_can_finish.set()
        await session._mtls_init_task
        assert session._mtls_init_task.done()
        assert not session._mtls_init_task.cancelled()
        assert session._is_mtls is True
        await session.close()

    @pytest.mark.asyncio
    async def test_401_mtls_rotation_e2e_unmocked_configure(self):
        """End-to-end 401 recovery test with unmocked configure_mtls_channel."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        cert_v1 = b"cert_v1"
        key_v1 = b"key_v1"
        cert_v2 = b"cert_v2"
        key_v2 = b"key_v2"

        certs_queue = [(True, cert_v1, key_v1), (True, cert_v2, key_v2)]

        async def mock_get_cert(cb=None):
            if certs_queue:
                return certs_queue.pop(0)
            return (True, cert_v2, key_v2)

        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                side_effect=mock_get_cert,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession"),
        ):
            session = sessions.AsyncAuthorizedSession(mock_creds)
            await session.configure_mtls_channel()
            assert session.is_mtls is True
            assert session._cached_cert == cert_v1
            first_auth_req = session._auth_request

            mock_resp_401 = mock.Mock()
            mock_resp_401.status_code = http_client.UNAUTHORIZED
            mock_resp_401.close = mock.AsyncMock()

            mock_resp_200 = mock.Mock()
            mock_resp_200.status_code = http_client.OK
            mock_resp_200.close = mock.AsyncMock()

            with (
                mock.patch(
                    "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                    new_callable=mock.AsyncMock,
                    return_value=(cert_v2, key_v2, b"fp1", b"fp2"),
                ),
                mock.patch.object(
                    sessions.AiohttpRequest,
                    "__call__",
                    side_effect=[mock_resp_401, mock_resp_200],
                ),
            ):
                resp = await session.request(
                    "GET", "https://pubsub.mtls.googleapis.com/test"
                )
                assert resp.status_code == 200
                assert session.is_mtls is True
                assert session._cached_cert == cert_v2
                assert session._auth_request is not first_auth_req
                assert mock_creds.refresh.call_count == 1
            await session.close()

    @pytest.mark.asyncio
    async def test_401_cert_check_type_error_falls_back_to_refresh(self):
        """Verifies that TypeError in cert check logs warning and falls back to refresh and retry."""
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
        session._cached_cert = b"some_cert"

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
                new_callable=mock.AsyncMock,
                side_effect=TypeError("Callback returned invalid type"),
            ),
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
            mock.patch.object(sessions._LOGGER, "warning") as mock_warn,
        ):
            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )
            assert resp == mock_resp_200
            mock_conf.assert_not_called()
            mock_creds.refresh.assert_called_once()
            assert any(
                "Falling back to credential refresh and retry." in str(call)
                for call in mock_warn.call_args_list
            )
        await session.close()

    @pytest.mark.asyncio
    async def test_401_cert_check_without_cached_cert_skips_reconfiguration(self):
        """Verifies that when cached_cert is None, cert check produces equal fingerprints and skips reconfiguration."""
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
        session._cached_cert = None

        with (
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                new_callable=mock.AsyncMock,
                return_value=(True, b"cert_bytes", b"key_bytes"),
            ),
            mock.patch("google.auth._agent_identity_utils.parse_certificate"),
            mock.patch(
                "google.auth._agent_identity_utils.calculate_certificate_fingerprint",
                return_value="FINGERPRINT_1",
            ),
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
            mock.patch.object(sessions._LOGGER, "info") as mock_info,
        ):
            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )
            assert resp == mock_resp_200
            mock_conf.assert_not_called()
            mock_creds.refresh.assert_called_once()
            assert any(
                "certificate has not changed" in str(call)
                for call in mock_info.call_args_list
            )
        await session.close()

    @pytest.mark.asyncio
    async def test_401_refresh_raises_invalid_operation_returns_401(self):
        """Verifies that exceptions.InvalidOperation during refresh is caught and returns the 401 response."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(
            side_effect=exceptions.InvalidOperation("Invalid operation")
        )

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_401.close = mock.AsyncMock()

        mock_auth_req = mock.AsyncMock(return_value=mock_resp_401)

        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )

        resp = await session.request("GET", "https://example.com")
        assert resp == mock_resp_401
        mock_creds.refresh.assert_called_once()
        await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_idempotent_when_called_repeatedly(self):
        """Tests that calling configure_mtls_channel repeatedly without a new callback reuses the existing task."""
        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(True, b"cert_bytes", b"key_bytes"),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession"),
        ):
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)
            await session.configure_mtls_channel()
            assert session.is_mtls is True
            first_auth_req = session._auth_request
            first_task = session._mtls_init_task

            # Call configure_mtls_channel again without new callback
            await session.configure_mtls_channel()
            assert session._auth_request is first_auth_req
            assert session._mtls_init_task is first_task

            # Call configure_mtls_channel with a new callback - should reconfigure
            def new_callback():
                return b"new_cert", b"new_key"

            await session.configure_mtls_channel(new_callback)
            assert session._auth_request is not first_auth_req
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_exception_preserves_existing_mtls_state(self):
        """Tests that an exception during re-configuration does not clear existing is_mtls and cached_cert."""
        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(True, b"cert_v1", b"key_v1"),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession"),
        ):
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)
            await session.configure_mtls_channel()
            assert session.is_mtls is True
            assert session._cached_cert == b"cert_v1"
            first_auth_req = session._auth_request

            # Now attempt reconfiguring with a failing callback/context
            with (
                mock.patch(
                    "google.auth.aio.transport.mtls.get_client_cert_and_key",
                    side_effect=RuntimeError("Reconfig failure"),
                ),
                pytest.raises(exceptions.MutualTLSChannelError),
            ):
                await session.configure_mtls_channel(lambda: (b"cert_v2", b"key_v2"))

            # Session should still retain its previous mTLS state and active auth_request
            assert session.is_mtls is True
            assert session._cached_cert == b"cert_v1"
            assert session._auth_request is first_auth_req
            await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_credential_refresh_not_implemented_retries(self):
        """Validate credentials that raise NotImplementedError on refresh()
        still trigger a retry after mTLS reconfiguration, not return the 401."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(side_effect=NotImplementedError)

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

        with mock.patch(
            "google.auth.aio.transport.mtls.check_parameters_for_unauthorized_response",
            new_callable=mock.AsyncMock,
        ) as mock_check:
            with mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf:
                mock_check.return_value = (
                    b"new_cert",
                    b"new_key",
                    b"old_fp",
                    b"new_fp",
                )

                resp = await session.request(
                    "GET", "https://pubsub.mtls.googleapis.com/test"
                )

                # Validate that the handler falls through to `return None`
                # on NotImplementedError in order to signal retry.
                assert resp == mock_resp_200
                mock_conf.assert_called_once()
                mock_creds.refresh.assert_called_once()
                assert mock_auth_req.call_count == 2
                mock_resp_401.close.assert_called_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_401_mtls_consecutive_multi_rotation(self):
        """Verifies that consecutive rotations (v1 -> v2 -> v3) succeed.

        `configure_mtls_channel` is deliberately NOT mocked here. The
        low-level helpers are patched instead so the real reconfiguration path
        executes; otherwise this test would still pass even if rotation
        stopped swapping the transport or started clobbering the shared
        `_client_cert_callback`.
        """
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(return_value=None)

        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(True, b"cert_v1", b"key_v1"),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession"),
        ):

            def user_cb():
                return (b"cert_v1", b"key_v1")

            session = sessions.AsyncAuthorizedSession(mock_creds)
            # Configure with an explicit, non-None user callback. A rotation
            # that clobbers this shared attribute is then observable; with a
            # default of None the overwrite would be a silent no-op.
            await session.configure_mtls_channel(user_cb)
            assert session._cached_cert == b"cert_v1"
            assert session._client_cert_callback is user_cb

            rotations = ((b"cert_v1", b"cert_v2"), (b"cert_v2", b"cert_v3"))
            for old_cert, new_cert in rotations:
                prev_auth_request = session._auth_request
                with (
                    mock.patch(
                        "google.auth.aio.transport.mtls."
                        "check_parameters_for_unauthorized_response",
                        new_callable=mock.AsyncMock,
                        return_value=(new_cert, b"key", b"fp_old", b"fp_new"),
                    ) as mock_check,
                    mock.patch.object(
                        sessions.AiohttpRequest,
                        "__call__",
                        side_effect=[
                            mock.Mock(status_code=401, close=mock.AsyncMock()),
                            mock.Mock(status_code=200, close=mock.AsyncMock()),
                        ],
                    ),
                ):
                    resp = await session.request(
                        "GET", "https://pubsub.mtls.googleapis.com/test"
                    )

                assert resp.status_code == 200
                # The check is driven by the previously cached cert and the
                # user's callback (None), so the on-disk cert can be read.
                mock_check.assert_called_once_with(old_cert, user_cb)
                # Real reconfiguration ran: cert cached and transport swapped.
                assert session._cached_cert == new_cert
                assert session._auth_request is not prev_auth_request
                assert session.is_mtls is True
                # Shared callback state must survive rotation untouched.
                assert session._client_cert_callback is user_cb

            await session.close()

    @pytest.mark.asyncio
    async def test_non_mtls_not_implemented_refresh_returns_401_without_retry(self):
        """Verifies that non-mTLS 401s on credentials that raise NotImplementedError
        return the 401 immediately without retrying."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(side_effect=NotImplementedError)

        mock_resp_401 = mock.Mock()
        mock_resp_401.status_code = http_client.UNAUTHORIZED
        mock_resp_401.close = mock.AsyncMock()

        mock_auth_req = mock.AsyncMock(return_value=mock_resp_401)
        session = sessions.AsyncAuthorizedSession(
            mock_creds, auth_request=mock_auth_req
        )

        resp = await session.request("GET", "https://example.com")
        assert resp == mock_resp_401
        assert mock_auth_req.call_count == 1
        mock_creds.refresh.assert_called_once()
        mock_resp_401.close.assert_not_called()
        await session.close()

    @pytest.mark.asyncio
    async def test_cert_rotation_credential_refresh_invalid_operation_retries(self):
        """Verifies that when mTLS is reconfigured, credentials raising InvalidOperation
        (e.g., StaticCredentials) still retry on the reconfigured mTLS channel."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(
            side_effect=exceptions.InvalidOperation("Static credentials")
        )

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
                return_value=(b"new_cert", b"new_key", b"old_fp", b"new_fp"),
            ),
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            resp = await session.request(
                "GET", "https://pubsub.mtls.googleapis.com/test"
            )
            assert resp == mock_resp_200
            mock_conf.assert_called_once()
            mock_creds.refresh.assert_called_once()
            assert mock_auth_req.call_count == 2
            mock_resp_401.close.assert_called_once()

        await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_reverts_to_default_when_callback_none(self):
        """Tests that passing callback=None when a callback was previously set reconfigures back to ADC."""
        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(True, b"cert", b"key"),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession"),
        ):
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            def custom_cb():
                return b"c", b"k"

            await session.configure_mtls_channel(custom_cb)
            assert session._client_cert_callback is custom_cb
            task1 = session._mtls_init_task

            # Revert to default
            await session.configure_mtls_channel(None)
            assert session._client_cert_callback is None
            assert session._mtls_init_task is not task1
            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_force_reconfigures_same_callback(self):
        """Tests that force=True reconfigures even if callback is identical."""
        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(True, b"cert", b"key"),
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession"),
        ):
            mock_creds = mock.AsyncMock(spec=credentials.Credentials)
            session = sessions.AsyncAuthorizedSession(mock_creds)

            await session.configure_mtls_channel()
            task1 = session._mtls_init_task

            # Same callback with force=True
            await session.configure_mtls_channel(force=True)
            assert session._mtls_init_task is not task1
            await session.close()

    @pytest.mark.asyncio
    async def test_concurrent_rotation_retries_for_non_refreshable_credentials(self):
        """Concurrent 401s with non-refreshable credentials must both retry.

        Only one coroutine performs the rotation; the other skips the check
        block via the dedupe counter. The skipping coroutine must still observe
        that the channel was reconfigured since its own 401 and retry, rather
        than returning the stale 401 to the caller.
        """
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        mock_creds.before_request = mock.AsyncMock(return_value=None)
        mock_creds.refresh = mock.AsyncMock(side_effect=NotImplementedError)

        def _resp(status):
            return mock.Mock(status_code=status, close=mock.AsyncMock())

        mock_resp_401_1 = _resp(http_client.UNAUTHORIZED)
        mock_resp_401_2 = _resp(http_client.UNAUTHORIZED)
        mock_resp_200_1 = _resp(http_client.OK)
        mock_resp_200_2 = _resp(http_client.OK)

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
            # Hold the rotation lock long enough that the second coroutine
            # queues behind it and then takes the dedupe path.
            await asyncio.sleep(0.05)
            return (b"new_cert", b"new_key", b"old_fp", b"new_fp")

        with (
            mock.patch(
                "google.auth.aio.transport.mtls."
                "check_parameters_for_unauthorized_response",
                side_effect=slow_check,
            ) as mock_check,
            mock.patch.object(
                session, "configure_mtls_channel", new_callable=mock.AsyncMock
            ) as mock_conf,
        ):
            results = await asyncio.gather(
                session.request("GET", "https://pubsub.mtls.googleapis.com/t1"),
                session.request("GET", "https://pubsub.mtls.googleapis.com/t2"),
            )

        # Exactly one coroutine ran the check and the rotation.
        assert mock_check.call_count == 1
        assert mock_conf.call_count == 1
        # Both requests must have been retried on the rotated channel.
        assert results == [mock_resp_200_1, mock_resp_200_2]
        assert mock_auth_req.call_count == 4

        await session.close()

    @pytest.mark.asyncio
    async def test_reconfigure_to_non_mtls_replaces_stale_mtls_transport(self):
        """A session leaving mTLS must not keep serving the old client cert."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)
        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession"),
        ):
            with mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(True, b"cert", b"key"),
            ):
                session = sessions.AsyncAuthorizedSession(mock_creds)
                await session.configure_mtls_channel()

            assert session.is_mtls is True
            mtls_transport = session._auth_request

            # The workload stops providing a client certificate.
            with mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                return_value=(False, None, None),
            ):
                await session.configure_mtls_channel(force=True)

            assert session.is_mtls is False
            assert session._cached_cert is None
            # The stale mTLS transport must be retired, not silently reused.
            assert session._auth_request is not mtls_transport
            assert mtls_transport in session._old_auth_requests

            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_propagates_caller_cancellation(self):
        """Cancelling the caller must raise, not be swallowed by cleanup."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)

        async def slow_get_cert(cb=None):
            await asyncio.sleep(10)
            return (True, b"cert", b"key")

        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                side_effect=slow_get_cert,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession"),
        ):
            session = sessions.AsyncAuthorizedSession(mock_creds)
            caller = asyncio.create_task(session.configure_mtls_channel())
            await asyncio.sleep(0.02)

            caller.cancel()
            with pytest.raises(asyncio.CancelledError):
                await caller

            await session.close()

    @pytest.mark.asyncio
    async def test_configure_mtls_channel_follows_replacement_task(self):
        """A caller awaiting a task that gets replaced follows the new one."""
        mock_creds = mock.AsyncMock(spec=credentials.Credentials)

        release = asyncio.Event()

        async def gated_get_cert(cb=None):
            await release.wait()
            return (True, b"cert", b"key")

        with (
            mock.patch(
                "google.auth.transport._mtls_helper.check_use_client_cert",
                return_value=True,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.get_client_cert_and_key",
                side_effect=gated_get_cert,
            ),
            mock.patch(
                "google.auth.aio.transport.mtls.make_client_cert_ssl_context",
                return_value=mock.Mock(spec=ssl.SSLContext),
            ),
            mock.patch("aiohttp.TCPConnector"),
            mock.patch("aiohttp.ClientSession"),
        ):
            session = sessions.AsyncAuthorizedSession(mock_creds)

            # First caller starts and blocks on the gated configuration.
            waiter = asyncio.create_task(session.configure_mtls_channel())
            await asyncio.sleep(0.02)
            first_task = session._mtls_init_task
            assert first_task is not None

            # A forced reconfiguration cancels and replaces that task.
            release.set()
            await session.configure_mtls_channel(force=True)
            assert session._mtls_init_task is not first_task

            # The original caller must not surface a cancellation it never
            # requested; it follows the replacement task instead.
            await waiter
            assert session.is_mtls is True

            await session.close()

    @pytest.mark.asyncio
    async def test_retrieve_task_exception_helper(self):
        """The done-callback marks failures retrieved and tolerates cancels."""

        async def boom():
            raise RuntimeError("boom")

        task = asyncio.create_task(boom())
        task.add_done_callback(sessions._retrieve_task_exception)
        with pytest.raises(RuntimeError):
            await task

        async def sleeper():
            await asyncio.sleep(10)

        cancelled = asyncio.create_task(sleeper())
        cancelled.cancel()
        with pytest.raises(asyncio.CancelledError):
            await cancelled
        # Must not raise CancelledError/InvalidStateError when inspected.
        sessions._retrieve_task_exception(cancelled)
