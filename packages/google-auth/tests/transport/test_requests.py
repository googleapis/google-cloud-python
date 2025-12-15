# Copyright 2016 Google LLC
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

import datetime
import functools
import http.client as http_client
import os
import sys

import freezegun
import mock
import OpenSSL
import pytest  # type: ignore
import requests
import requests.adapters

from google.auth import environment_vars
from google.auth import exceptions
import google.auth.credentials
import google.auth.transport._custom_tls_signer
import google.auth.transport._mtls_helper
import google.auth.transport.requests
from google.oauth2 import service_account
from tests.transport import compliance


@pytest.fixture
def frozen_time():
    with freezegun.freeze_time("1970-01-01 00:00:00", tick=False) as frozen:
        yield frozen


CERT_MOCK_VAL = b"-----BEGIN CERTIFICATE-----\nMIIDIzCCAgugAwIBAgIJAMfISuBQ5m+5MA0GCSqGSIb3DQEBBQUAMBUxEzARBgNV\nBAMTCnVuaXQtdGVzdHMwHhcNMTExMjA2MTYyNjAyWhcNMjExMjAzMTYyNjAyWjAV\nMRMwEQYDVQQDEwp1bml0LXRlc3RzMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB\nCgKCAQEA4ej0p7bQ7L/r4rVGUz9RN4VQWoej1Bg1mYWIDYslvKrk1gpj7wZgkdmM\n7oVK2OfgrSj/FCTkInKPqaCR0gD7K80q+mLBrN3PUkDrJQZpvRZIff3/xmVU1Wer\nuQLFJjnFb2dqu0s/FY/2kWiJtBCakXvXEOb7zfbINuayL+MSsCGSdVYsSliS5qQp\ngyDap+8b5fpXZVJkq92hrcNtbkg7hCYUJczt8n9hcCTJCfUpApvaFQ18pe+zpyl4\n+WzkP66I28hniMQyUlA1hBiskT7qiouq0m8IOodhv2fagSZKjOTTU2xkSBc//fy3\nZpsL7WqgsZS7Q+0VRK8gKfqkxg5OYQIDAQABo3YwdDAdBgNVHQ4EFgQU2RQ8yO+O\ngN8oVW2SW7RLrfYd9jEwRQYDVR0jBD4wPIAU2RQ8yO+OgN8oVW2SW7RLrfYd9jGh\nGaQXMBUxEzARBgNVBAMTCnVuaXQtdGVzdHOCCQDHyErgUOZvuTAMBgNVHRMEBTAD\nAQH/MA0GCSqGSIb3DQEBBQUAA4IBAQBRv+M/6+FiVu7KXNjFI5pSN17OcW5QUtPr\nodJMlWrJBtynn/TA1oJlYu3yV5clc/71Vr/AxuX5xGP+IXL32YDF9lTUJXG/uUGk\n+JETpKmQviPbRsvzYhz4pf6ZIOZMc3/GIcNq92ECbseGO+yAgyWUVKMmZM0HqXC9\novNslqe0M8C1sLm1zAR5z/h/litE7/8O2ietija3Q/qtl2TOXJdCA6sgjJX2WUql\nybrC55ct18NKf3qhpcEkGQvFU40rVYApJpi98DiZPYFdx1oBDp/f4uZ3ojpxRVFT\ncDwcJLfNRCPUhormsY7fDS9xSyThiHsW9mjJYdcaKQkwYZ0F11yB\n-----END CERTIFICATE-----\n"
KEY_MOCK_VAL = b"-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIHeMEkGCSqGSIb3DQEFDTA8MBsGCSqGSIb3DQEFDDAOBAj9XnJ2h78QVAICCAAw\nHQYJYIZIAWUDBAECBBBeiiOF2LnLzq/wjb/viwMwBIGQk28Zkfj2EIk42bgc7UzC\nSf98qssCVhsIYz0Xa3eSATg8Cpn83YieaBeyxdk/tXTnrOhxMV/vt7T98kWhaGbH\n5Z9CdGVLfes0UFvVJqrlk6vcf2sOnLCGbrn78HS+ayrGOCRSCd/7+dnEiB/7Um1B\nMk6BBJHsLEnZZSHyfrw8jvYgVmcSBy/WdY0pqldD/+4D\n-----END ENCRYPTED PRIVATE KEY-----\n"


class TestRequestResponse(compliance.RequestResponseTests):
    def make_request(self):
        return google.auth.transport.requests.Request()

    def test_timeout(self):
        http = mock.create_autospec(requests.Session, instance=True)
        request = google.auth.transport.requests.Request(http)
        request(url="http://example.com", method="GET", timeout=5)

        assert http.request.call_args[1]["timeout"] == 5

    def test_session_closed_on_del(self):
        http = mock.create_autospec(requests.Session, instance=True)
        request = google.auth.transport.requests.Request(http)
        request.__del__()
        http.close.assert_called_with()

        http = mock.create_autospec(requests.Session, instance=True)
        http.close.side_effect = TypeError("test injected TypeError")
        request = google.auth.transport.requests.Request(http)
        request.__del__()
        http.close.assert_called_with()


class TestTimeoutGuard(object):
    def make_guard(self, *args, **kwargs):
        return google.auth.transport.requests.TimeoutGuard(*args, **kwargs)

    def test_tracks_elapsed_time_w_numeric_timeout(self, frozen_time):
        with self.make_guard(timeout=10) as guard:
            frozen_time.tick(delta=datetime.timedelta(seconds=3.8))
        assert guard.remaining_timeout == 6.2

    def test_tracks_elapsed_time_w_tuple_timeout(self, frozen_time):
        with self.make_guard(timeout=(16, 19)) as guard:
            frozen_time.tick(delta=datetime.timedelta(seconds=3.8))
        assert guard.remaining_timeout == (12.2, 15.2)

    def test_noop_if_no_timeout(self, frozen_time):
        with self.make_guard(timeout=None) as guard:
            frozen_time.tick(delta=datetime.timedelta(days=3650))
        # NOTE: no timeout error raised, despite years have passed
        assert guard.remaining_timeout is None

    def test_timeout_error_w_numeric_timeout(self, frozen_time):
        with pytest.raises(requests.exceptions.Timeout):
            with self.make_guard(timeout=10) as guard:
                frozen_time.tick(delta=datetime.timedelta(seconds=10.001))
        assert guard.remaining_timeout == pytest.approx(-0.001)

    def test_timeout_error_w_tuple_timeout(self, frozen_time):
        with pytest.raises(requests.exceptions.Timeout):
            with self.make_guard(timeout=(11, 10)) as guard:
                frozen_time.tick(delta=datetime.timedelta(seconds=10.001))
        assert guard.remaining_timeout == pytest.approx((0.999, -0.001))

    def test_custom_timeout_error_type(self, frozen_time):
        class FooError(Exception):
            pass

        with pytest.raises(FooError):
            with self.make_guard(timeout=1, timeout_error_type=FooError):
                frozen_time.tick(delta=datetime.timedelta(seconds=2))

    def test_lets_suite_errors_bubble_up(self, frozen_time):
        with pytest.raises(IndexError):
            with self.make_guard(timeout=1):
                [1, 2, 3][3]


class CredentialsStub(google.auth.credentials.Credentials):
    def __init__(self, token="token"):
        super(CredentialsStub, self).__init__()
        self.token = token

    def apply(self, headers, token=None):
        headers["authorization"] = self.token

    def before_request(self, request, method, url, headers):
        self.apply(headers)

    def refresh(self, request):
        self.token += "1"

    def with_quota_project(self, quota_project_id):
        raise NotImplementedError()


class TimeTickCredentialsStub(CredentialsStub):
    """Credentials that spend some (mocked) time when refreshing a token."""

    def __init__(self, time_tick, token="token"):
        self._time_tick = time_tick
        super(TimeTickCredentialsStub, self).__init__(token=token)

    def refresh(self, request):
        self._time_tick()
        super(TimeTickCredentialsStub, self).refresh(requests)


class AdapterStub(requests.adapters.BaseAdapter):
    def __init__(self, responses, headers=None):
        super(AdapterStub, self).__init__()
        self.responses = responses
        self.requests = []
        self.headers = headers or {}

    def send(self, request, **kwargs):
        # pylint: disable=arguments-differ
        # request is the only required argument here and the only argument
        # we care about.
        self.requests.append(request)
        return self.responses.pop(0)

    def close(self):  # pragma: NO COVER
        # pylint wants this to be here because it's abstract in the base
        # class, but requests never actually calls it.
        return


class TimeTickAdapterStub(AdapterStub):
    """Adapter that spends some (mocked) time when making a request."""

    def __init__(self, time_tick, responses, headers=None):
        self._time_tick = time_tick
        super(TimeTickAdapterStub, self).__init__(responses, headers=headers)

    def send(self, request, **kwargs):
        self._time_tick()
        return super(TimeTickAdapterStub, self).send(request, **kwargs)


class TestMutualTlsAdapter(object):
    @mock.patch.object(requests.adapters.HTTPAdapter, "init_poolmanager")
    @mock.patch.object(requests.adapters.HTTPAdapter, "proxy_manager_for")
    def test_success(self, mock_proxy_manager_for, mock_init_poolmanager):
        adapter = google.auth.transport.requests._MutualTlsAdapter(
            pytest.public_cert_bytes, pytest.private_key_bytes
        )

        adapter.init_poolmanager()
        mock_init_poolmanager.assert_called_with(ssl_context=adapter._ctx_poolmanager)

        adapter.proxy_manager_for()
        mock_proxy_manager_for.assert_called_with(ssl_context=adapter._ctx_proxymanager)

    def test_invalid_cert_or_key(self):
        with pytest.raises(OpenSSL.crypto.Error):
            google.auth.transport.requests._MutualTlsAdapter(
                b"invalid cert", b"invalid key"
            )

    @mock.patch.dict("sys.modules", {"OpenSSL.crypto": None})
    def test_import_error(self):
        with pytest.raises(ImportError):
            google.auth.transport.requests._MutualTlsAdapter(
                pytest.public_cert_bytes, pytest.private_key_bytes
            )


def make_response(status=http_client.OK, data=None):
    response = requests.Response()
    response.status_code = status
    response._content = data
    return response


class TestAuthorizedSession(object):
    TEST_URL = "http://example.com/"

    def test_constructor(self):
        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock.sentinel.credentials
        )

        assert authed_session.credentials == mock.sentinel.credentials

    def test_constructor_with_auth_request(self):
        http = mock.create_autospec(requests.Session)
        auth_request = google.auth.transport.requests.Request(http)

        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock.sentinel.credentials, auth_request=auth_request
        )

        assert authed_session._auth_request is auth_request

    def test_request_default_timeout(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        response = make_response()
        adapter = AdapterStub([response])

        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
        authed_session.mount(self.TEST_URL, adapter)

        patcher = mock.patch("google.auth.transport.requests.requests.Session.request")
        with patcher as patched_request:
            authed_session.request("GET", self.TEST_URL)

        expected_timeout = google.auth.transport.requests._DEFAULT_TIMEOUT
        assert patched_request.call_args[1]["timeout"] == expected_timeout

    def test_request_no_refresh(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        response = make_response()
        adapter = AdapterStub([response])

        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
        authed_session.mount(self.TEST_URL, adapter)

        result = authed_session.request("GET", self.TEST_URL)

        assert response == result
        assert credentials.before_request.called
        assert not credentials.refresh.called
        assert len(adapter.requests) == 1
        assert adapter.requests[0].url == self.TEST_URL
        assert adapter.requests[0].headers["authorization"] == "token"

    def test_request_refresh(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = make_response(status=http_client.OK)
        # First request will 401, second request will succeed.
        adapter = AdapterStub(
            [make_response(status=http_client.UNAUTHORIZED), final_response]
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.TEST_URL, adapter)

        result = authed_session.request("GET", self.TEST_URL)

        assert result == final_response
        assert credentials.before_request.call_count == 2
        assert credentials.refresh.called
        assert len(adapter.requests) == 2

        assert adapter.requests[0].url == self.TEST_URL
        assert adapter.requests[0].headers["authorization"] == "token"

        assert adapter.requests[1].url == self.TEST_URL
        assert adapter.requests[1].headers["authorization"] == "token1"

    def test_request_max_allowed_time_timeout_error(self, frozen_time):
        tick_one_second = functools.partial(
            frozen_time.tick, delta=datetime.timedelta(seconds=1.0)
        )

        credentials = mock.Mock(
            wraps=TimeTickCredentialsStub(time_tick=tick_one_second)
        )
        adapter = TimeTickAdapterStub(
            time_tick=tick_one_second, responses=[make_response(status=http_client.OK)]
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
        authed_session.mount(self.TEST_URL, adapter)

        # Because a request takes a full mocked second, max_allowed_time shorter
        # than that will cause a timeout error.
        with pytest.raises(requests.exceptions.Timeout):
            authed_session.request("GET", self.TEST_URL, max_allowed_time=0.9)

    def test_request_max_allowed_time_w_transport_timeout_no_error(self, frozen_time):
        tick_one_second = functools.partial(
            frozen_time.tick, delta=datetime.timedelta(seconds=1.0)
        )

        credentials = mock.Mock(
            wraps=TimeTickCredentialsStub(time_tick=tick_one_second)
        )
        adapter = TimeTickAdapterStub(
            time_tick=tick_one_second,
            responses=[
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ],
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
        authed_session.mount(self.TEST_URL, adapter)

        # A short configured transport timeout does not affect max_allowed_time.
        # The latter is not adjusted to it and is only concerned with the actual
        # execution time. The call below should thus not raise a timeout error.
        authed_session.request("GET", self.TEST_URL, timeout=0.5, max_allowed_time=3.1)

    def test_request_max_allowed_time_w_refresh_timeout_no_error(self, frozen_time):
        tick_one_second = functools.partial(
            frozen_time.tick, delta=datetime.timedelta(seconds=1.0)
        )

        credentials = mock.Mock(
            wraps=TimeTickCredentialsStub(time_tick=tick_one_second)
        )
        adapter = TimeTickAdapterStub(
            time_tick=tick_one_second,
            responses=[
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ],
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=1.1
        )
        authed_session.mount(self.TEST_URL, adapter)

        # A short configured refresh timeout does not affect max_allowed_time.
        # The latter is not adjusted to it and is only concerned with the actual
        # execution time. The call below should thus not raise a timeout error
        # (and `timeout` does not come into play either, as it's very long).
        authed_session.request("GET", self.TEST_URL, timeout=60, max_allowed_time=3.1)

    def test_request_timeout_w_refresh_timeout_timeout_error(self, frozen_time):
        tick_one_second = functools.partial(
            frozen_time.tick, delta=datetime.timedelta(seconds=1.0)
        )

        credentials = mock.Mock(
            wraps=TimeTickCredentialsStub(time_tick=tick_one_second)
        )
        adapter = TimeTickAdapterStub(
            time_tick=tick_one_second,
            responses=[
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.OK),
            ],
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=100
        )
        authed_session.mount(self.TEST_URL, adapter)

        # An UNAUTHORIZED response triggers a refresh (an extra request), thus
        # the final request that otherwise succeeds results in a timeout error
        # (all three requests together last 3 mocked seconds).
        with pytest.raises(requests.exceptions.Timeout):
            authed_session.request(
                "GET", self.TEST_URL, timeout=60, max_allowed_time=2.9
            )

    def test_authorized_session_without_default_host(self):
        credentials = mock.create_autospec(service_account.Credentials)

        authed_session = google.auth.transport.requests.AuthorizedSession(credentials)

        authed_session.credentials._create_self_signed_jwt.assert_called_once_with(None)

    def test_authorized_session_with_default_host(self):
        default_host = "pubsub.googleapis.com"
        credentials = mock.create_autospec(service_account.Credentials)

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, default_host=default_host
        )

        authed_session.credentials._create_self_signed_jwt.assert_called_once_with(
            "https://{}/".format(default_host)
        )

    def test_configure_mtls_channel_with_callback(self):
        mock_callback = mock.Mock()
        mock_callback.return_value = (
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel(mock_callback)

        assert auth_session.is_mtls
        assert isinstance(
            auth_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_with_metadata(self, mock_get_client_cert_and_key):
        mock_get_client_cert_and_key.return_value = (
            True,
            pytest.public_cert_bytes,
            pytest.private_key_bytes,
        )

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel()

        assert auth_session.is_mtls
        assert isinstance(
            auth_session.adapters["https://"],
            google.auth.transport.requests._MutualTlsAdapter,
        )

    @mock.patch.object(google.auth.transport.requests._MutualTlsAdapter, "__init__")
    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_non_mtls(
        self, mock_get_client_cert_and_key, mock_adapter_ctor
    ):
        mock_get_client_cert_and_key.return_value = (False, None, None)

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            auth_session.configure_mtls_channel()

        assert not auth_session.is_mtls

        # Assert _MutualTlsAdapter constructor is not called.
        mock_adapter_ctor.assert_not_called()

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_exceptions(self, mock_get_client_cert_and_key):
        mock_get_client_cert_and_key.side_effect = exceptions.ClientCertError()

        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )
        with pytest.raises(exceptions.MutualTLSChannelError):
            with mock.patch.dict(
                os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
            ):
                auth_session.configure_mtls_channel()

        mock_get_client_cert_and_key.return_value = (False, None, None)
        with mock.patch.dict("sys.modules"):
            sys.modules["OpenSSL"] = None
            with pytest.raises(exceptions.MutualTLSChannelError):
                with mock.patch.dict(
                    os.environ,
                    {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"},
                ):
                    auth_session.configure_mtls_channel()

    @mock.patch(
        "google.auth.transport._mtls_helper.get_client_cert_and_key", autospec=True
    )
    def test_configure_mtls_channel_without_client_cert_env(
        self, get_client_cert_and_key
    ):
        # Test client cert won't be used if GOOGLE_API_USE_CLIENT_CERTIFICATE
        # environment variable is not set.
        auth_session = google.auth.transport.requests.AuthorizedSession(
            credentials=mock.Mock()
        )

        auth_session.configure_mtls_channel()
        assert not auth_session.is_mtls
        get_client_cert_and_key.assert_not_called()

        mock_callback = mock.Mock()
        auth_session.configure_mtls_channel(mock_callback)
        assert not auth_session.is_mtls
        mock_callback.assert_not_called()

    def test_close_wo_passed_in_auth_request(self):
        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock.sentinel.credentials
        )
        authed_session._auth_request_session = mock.Mock(spec=["close"])

        authed_session.close()

        authed_session._auth_request_session.close.assert_called_once_with()

    def test_close_w_passed_in_auth_request(self):
        http = mock.create_autospec(requests.Session)
        auth_request = google.auth.transport.requests.Request(http)
        authed_session = google.auth.transport.requests.AuthorizedSession(
            mock.sentinel.credentials, auth_request=auth_request
        )

        authed_session.close()  # no raise

    def test_cert_rotation_when_cert_mismatch_and_mtls_enabled(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = make_response(status=http_client.OK)
        # First request will 401, second request will succeed.
        adapter = AdapterStub(
            [make_response(status=http_client.UNAUTHORIZED), final_response]
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.TEST_URL, adapter)

        old_cert = b"-----BEGIN CERTIFICATE-----\nMIIBdTCCARqgAwIBAgIJAOYVvu/axMxvMAoGCCqGSM49BAMCMCcxJTAjBgNVBAMM\nHEdvb2dsZSBFbmRwb2ludCBWZXJpZmljYXRpb24wHhcNMjUwNzMwMjMwNjA4WhcN\nMjYwNzMxMjMwNjA4WjAnMSUwIwYDVQQDDBxHb29nbGUgRW5kcG9pbnQgVmVyaWZp\nY2F0aW9uMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEbtr18gkEtwPow2oqyZsU\n4KLwFaLFlRlYv55UATS3QTDykDnIufC42TJCnqFRYhwicwpE2jnUV+l9g3Voias8\nraMvMC0wCQYDVR0TBAIwADALBgNVHQ8EBAMCB4AwEwYDVR0lBAwwCgYIKwYBBQUH\nAwIwCgYIKoZIzj0EAwIDSQAwRgIhAKcjW6dmF1YCksXPgDPlPu/nSnOjb3qCcivz\n/Jxq2zoeAiEA7/aNxcEoCGS3hwMIXoaaD/vPcZOOopKSyqXCvxRooKQ=\n-----END CERTIFICATE-----\n"

        # New certificate and key to simulate rotation.
        new_cert = CERT_MOCK_VAL
        new_key = KEY_MOCK_VAL

        # Set _cached_cert to a callable that returns the old certificate.
        authed_session._cached_cert = old_cert
        authed_session._is_mtls = True

        # Mock call_client_cert_callback to return the new certificate.
        with mock.patch.object(
            google.auth.transport._mtls_helper._agent_identity_utils,
            "call_client_cert_callback",
            return_value=(new_cert, new_key),
        ) as mock_callback:
            result = authed_session.request("GET", self.TEST_URL)

        # Asserts to verify the behavior.
        assert mock_callback.called
        assert credentials.refresh.called
        assert credentials.refresh.call_count == 1
        assert result.status_code == final_response.status_code

    def test_no_cert_rotation_when_cert_match_and_mTLS_enabled(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = make_response(status=http_client.UNAUTHORIZED)
        adapter = AdapterStub(
            [
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.UNAUTHORIZED),
            ]
        )
        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.TEST_URL, adapter)
        authed_session._is_mtls = True

        old_cert = CERT_MOCK_VAL

        # New certificate and key to simulate rotation.
        new_cert = old_cert
        new_key = KEY_MOCK_VAL

        # Set _cached_cert to a callable that returns the old certificate.
        authed_session._cached_cert = old_cert

        # Mock call_client_cert_callback to return the new certificate.
        with mock.patch.object(
            google.auth.transport._mtls_helper._agent_identity_utils,
            "call_client_cert_callback",
            return_value=(new_cert, new_key),
        ):
            result = authed_session.request("GET", self.TEST_URL)

        # Asserts to verify the behavior.
        assert credentials.refresh.call_count == 2
        assert result.status_code == final_response.status_code

    def test_no_cert_match_check_when_mtls_disabled(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = make_response(status=http_client.UNAUTHORIZED)
        adapter = AdapterStub(
            [
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.UNAUTHORIZED),
                make_response(status=http_client.UNAUTHORIZED),
            ]
        )
        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.TEST_URL, adapter)
        authed_session._is_mtls = False

        new_cert = CERT_MOCK_VAL

        # New certificate and key to simulate rotation.
        new_key = KEY_MOCK_VAL

        # Mock call_client_cert_callback to return the new certificate.
        with mock.patch.object(
            google.auth.transport._mtls_helper._agent_identity_utils,
            "call_client_cert_callback",
            return_value=(new_cert, new_key),
        ) as mock_callback:
            result = authed_session.request("GET", self.TEST_URL)

        # Asserts to verify the behavior.
        assert not mock_callback.called
        assert result.status_code == final_response.status_code

    def test_no_cert_rotation_when_no_unauthorized_response(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        final_response = make_response(status=http_client.UPGRADE_REQUIRED)

        # Response is set to code other than 401(Unauthorized).
        adapter = AdapterStub([make_response(status=http_client.UPGRADE_REQUIRED)])
        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.TEST_URL, adapter)

        authed_session._is_mtls = True

        result = authed_session.request("GET", self.TEST_URL)
        assert result.status_code == final_response.status_code

        # Asserts to verify the behavior.
        assert not credentials.refresh.called
        assert credentials.refresh.call_count == 0

    def test_cert_rotation_failure_raises_error(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        # First request will 401, second request will fail to reconfigure mTLS.
        adapter = AdapterStub([make_response(status=http_client.UNAUTHORIZED)])

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.TEST_URL, adapter)

        old_cert = b"-----BEGIN CERTIFICATE-----\nMIIBdTCCARqgAwIBAgIJAOYVvu/axMxvMAoGCCqGSM49BAMCMCcxJTAjBgNVBAMM\nHEdvb2dsZSBFbmRwb2ludCBWZXJpZmljYXRpb24wHhcNMjUwNzMwMjMwNjA4WhcN\nMjYwNzMxMjMwNjA4WjAnMSUwIwYDVQQDDBxHb29nbGUgRW5kcG9pbnQgVmVyaWZp\nY2F0aW9uMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEbtr18gkEtwPow2oqyZsU\n4KLwFaLFlRlYv55UATS3QTDykDnIufC42TJCnqFRYhwicwpE2jnUV+l9g3Voias8\nraMvMC0wCQYDVR0TBAIwADALBgNVHQ8EBAMCB4AwEwYDVR0lBAwwCgYIKwYBBQUH\nAwIwCgYIKoZIzj0EAwIDSQAwRgIhAKcjW6dmF1YCksXPgDPlPu/nSnOjb3qCcivz\n/Jxq2zoeAiEA7/aNxcEoCGS3hwMIXoaaD/vPcZOOopKSyqXCvxRooKQ=\n-----END CERTIFICATE-----\n"

        # New certificate and key to simulate rotation.
        new_cert = CERT_MOCK_VAL
        new_key = KEY_MOCK_VAL

        authed_session._cached_cert = old_cert
        authed_session._is_mtls = True

        with mock.patch.object(
            google.auth.transport._mtls_helper._agent_identity_utils,
            "call_client_cert_callback",
            return_value=(new_cert, new_key),
        ):
            with mock.patch.object(
                authed_session,
                "configure_mtls_channel",
                side_effect=Exception("Failed to reconfigure"),
            ):
                with pytest.raises(exceptions.MutualTLSChannelError):
                    authed_session.request("GET", self.TEST_URL)

                # Assert to verify behavior
                credentials.refresh.assert_not_called()

    def test_cert_rotation_check_params_fails(self):
        credentials = mock.Mock(wraps=CredentialsStub())
        adapter = AdapterStub([make_response(status=http_client.UNAUTHORIZED)])

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_timeout=60
        )
        authed_session.mount(self.TEST_URL, adapter)
        authed_session._is_mtls = True
        authed_session._cached_cert = b"cached_cert"

        with mock.patch(
            "google.auth.transport.requests._mtls_helper.check_parameters_for_unauthorized_response",
            side_effect=Exception("check_params failed"),
        ) as mock_check_params:
            with pytest.raises(Exception, match="check_params failed"):
                authed_session.request("GET", self.TEST_URL)

            mock_check_params.assert_called_once()
            credentials.refresh.assert_not_called()

    def test_cert_rotation_logic_skipped_on_other_refresh_status_codes(self):
        """
        Tests that the code can handle a refresh triggered by a status code
        other than 401 (UNAUTHORIZED). This covers the 'else' branch of the
        'if response.status_code == http_client.UNAUTHORIZED' check
        """
        credentials = mock.Mock(wraps=CredentialsStub())
        # Configure the session to treat 503 (Service Unavailable) as a refreshable error
        custom_refresh_codes = [http_client.SERVICE_UNAVAILABLE]

        # Return 503 first, then 200
        adapter = AdapterStub(
            [
                make_response(status=http_client.SERVICE_UNAVAILABLE),
                make_response(status=http_client.OK),
            ]
        )

        authed_session = google.auth.transport.requests.AuthorizedSession(
            credentials, refresh_status_codes=custom_refresh_codes
        )
        authed_session.mount(self.TEST_URL, adapter)

        # Enable mTLS to prove it is skipped despite being enabled
        authed_session._is_mtls = True

        with mock.patch(
            "google.auth.transport.requests._mtls_helper", autospec=True
        ) as mock_helper:
            authed_session.request("GET", self.TEST_URL)

            # Assert refresh happened (Outer Check was True)
            assert credentials.refresh.called

            # Assert mTLS check logic was SKIPPED (Inner Check was False)
            assert not mock_helper.check_parameters_for_unauthorized_response.called


class TestMutualTlsOffloadAdapter(object):
    @mock.patch.object(requests.adapters.HTTPAdapter, "init_poolmanager")
    @mock.patch.object(requests.adapters.HTTPAdapter, "proxy_manager_for")
    @mock.patch.object(
        google.auth.transport._custom_tls_signer.CustomTlsSigner, "load_libraries"
    )
    @mock.patch.object(
        google.auth.transport._custom_tls_signer.CustomTlsSigner,
        "attach_to_ssl_context",
    )
    def test_success(
        self,
        mock_attach_to_ssl_context,
        mock_load_libraries,
        mock_proxy_manager_for,
        mock_init_poolmanager,
    ):
        enterprise_cert_file_path = "/path/to/enterprise/cert/json"
        adapter = google.auth.transport.requests._MutualTlsOffloadAdapter(
            enterprise_cert_file_path
        )

        mock_load_libraries.assert_called_once()
        assert mock_attach_to_ssl_context.call_count == 2

        adapter.init_poolmanager()
        mock_init_poolmanager.assert_called_with(ssl_context=adapter._ctx_poolmanager)

        adapter.proxy_manager_for()
        mock_proxy_manager_for.assert_called_with(ssl_context=adapter._ctx_proxymanager)

    @mock.patch.object(requests.adapters.HTTPAdapter, "init_poolmanager")
    @mock.patch.object(requests.adapters.HTTPAdapter, "proxy_manager_for")
    @mock.patch.object(
        google.auth.transport._custom_tls_signer.CustomTlsSigner, "should_use_provider"
    )
    @mock.patch.object(
        google.auth.transport._custom_tls_signer.CustomTlsSigner, "load_libraries"
    )
    @mock.patch.object(
        google.auth.transport._custom_tls_signer.CustomTlsSigner,
        "attach_to_ssl_context",
    )
    def test_success_should_use_provider(
        self,
        mock_attach_to_ssl_context,
        mock_load_libraries,
        mock_should_use_provider,
        mock_proxy_manager_for,
        mock_init_poolmanager,
    ):
        enterprise_cert_file_path = "/path/to/enterprise/cert/json"
        adapter = google.auth.transport.requests._MutualTlsOffloadAdapter(
            enterprise_cert_file_path
        )

        mock_should_use_provider.side_effect = True
        mock_load_libraries.assert_called_once()
        assert mock_attach_to_ssl_context.call_count == 2

        adapter.init_poolmanager()
        mock_init_poolmanager.assert_called_with(ssl_context=adapter._ctx_poolmanager)

        adapter.proxy_manager_for()
        mock_proxy_manager_for.assert_called_with(ssl_context=adapter._ctx_proxymanager)
