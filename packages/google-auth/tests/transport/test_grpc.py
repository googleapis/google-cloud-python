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
import importlib
import os
import time
from unittest import mock
import warnings

import grpc
import pytest  # type: ignore

from google.auth import _helpers
from google.auth import credentials
from google.auth import environment_vars
from google.auth import exceptions
from google.auth import transport
from google.oauth2 import service_account


def unwrap(ch):
    if isinstance(ch, mock.Mock) or isinstance(ch, mock.MagicMock):
        return ch
    if hasattr(ch, "_channel"):
        return unwrap(ch._channel)
    return ch


try:
    # pylint: disable=ungrouped-imports

    import google.auth.transport.grpc

    HAS_GRPC = True
except ImportError:  # pragma: NO COVER
    HAS_GRPC = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
METADATA_PATH = os.path.join(DATA_DIR, "context_aware_metadata.json")
with open(os.path.join(DATA_DIR, "privatekey.pem"), "rb") as fh:
    PRIVATE_KEY_BYTES = fh.read()
with open(os.path.join(DATA_DIR, "public_cert.pem"), "rb") as fh:
    PUBLIC_CERT_BYTES = fh.read()

pytestmark = pytest.mark.skipif(not HAS_GRPC, reason="gRPC is unavailable.")


class CredentialsStub(credentials.Credentials):
    def __init__(self, token="token"):
        super(CredentialsStub, self).__init__()
        self.token = token
        self.expiry = None

    def refresh(self, request):
        self.token += "1"

    def with_quota_project(self, quota_project_id):
        raise NotImplementedError()


class TestAuthMetadataPlugin(object):
    def test_call_no_refresh(self):
        credentials = CredentialsStub()
        request = mock.create_autospec(transport.Request)

        plugin = google.auth.transport.grpc.AuthMetadataPlugin(credentials, request)

        context = mock.create_autospec(grpc.AuthMetadataContext, instance=True)
        context.method_name = mock.sentinel.method_name
        context.service_url = mock.sentinel.service_url
        callback = mock.create_autospec(grpc.AuthMetadataPluginCallback)

        plugin(context, callback)

        time.sleep(2)

        callback.assert_called_once_with(
            [("authorization", "Bearer {}".format(credentials.token))], None
        )

    def test_call_refresh(self):
        credentials = CredentialsStub()
        credentials.expiry = datetime.datetime.min + _helpers.REFRESH_THRESHOLD
        request = mock.create_autospec(transport.Request)

        plugin = google.auth.transport.grpc.AuthMetadataPlugin(credentials, request)

        context = mock.create_autospec(grpc.AuthMetadataContext, instance=True)
        context.method_name = mock.sentinel.method_name
        context.service_url = mock.sentinel.service_url
        callback = mock.create_autospec(grpc.AuthMetadataPluginCallback)

        plugin(context, callback)

        time.sleep(2)

        assert credentials.token == "token1"
        callback.assert_called_once_with(
            [("authorization", "Bearer {}".format(credentials.token))], None
        )

    def test__get_authorization_headers_with_service_account(self):
        credentials = mock.create_autospec(service_account.Credentials)
        request = mock.create_autospec(transport.Request)

        plugin = google.auth.transport.grpc.AuthMetadataPlugin(credentials, request)

        context = mock.create_autospec(grpc.AuthMetadataContext, instance=True)
        context.method_name = "methodName"
        context.service_url = "https://pubsub.googleapis.com/methodName"

        plugin._get_authorization_headers(context)

        credentials._create_self_signed_jwt.assert_called_once_with(None)

    def test__get_authorization_headers_with_service_account_and_default_host(self):
        credentials = mock.create_autospec(service_account.Credentials)
        request = mock.create_autospec(transport.Request)

        default_host = "pubsub.googleapis.com"
        plugin = google.auth.transport.grpc.AuthMetadataPlugin(
            credentials, request, default_host=default_host
        )

        context = mock.create_autospec(grpc.AuthMetadataContext, instance=True)
        context.method_name = "methodName"
        context.service_url = "https://pubsub.googleapis.com/methodName"

        plugin._get_authorization_headers(context)

        credentials._create_self_signed_jwt.assert_called_once_with(
            "https://{}/".format(default_host)
        )

    def test_suppress_metrics_header(self):
        credentials = mock.create_autospec(service_account.Credentials)

        # Mock credentials before_request that adds metric and authorization
        def mock_before_request(request, method, url, headers):
            headers["x-goog-api-client"] = "foo"
            headers["authorization"] = "Bearer token"

        credentials.before_request.side_effect = mock_before_request
        request = mock.create_autospec(transport.Request)

        # By default, suppress_metrics_header=False
        plugin = google.auth.transport.grpc.AuthMetadataPlugin(credentials, request)
        context = mock.create_autospec(grpc.AuthMetadataContext, instance=True)
        context.method_name = "methodName"
        context.service_url = "https://pubsub.googleapis.com/methodName"

        headers = dict(plugin._get_authorization_headers(context))
        assert "x-goog-api-client" in headers
        assert headers["x-goog-api-client"] == "foo"

        # With suppress_metrics_header=True
        plugin_suppressed = google.auth.transport.grpc.AuthMetadataPlugin(
            credentials, request, suppress_metrics_header=True
        )
        headers_suppressed = dict(plugin_suppressed._get_authorization_headers(context))
        assert "x-goog-api-client" not in headers_suppressed
        assert headers_suppressed["authorization"] == "Bearer token"


@mock.patch(
    "google.auth.transport._mtls_helper.get_client_ssl_credentials", autospec=True
)
@mock.patch("grpc.composite_channel_credentials", autospec=True)
@mock.patch("grpc.metadata_call_credentials", autospec=True)
@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("grpc.secure_channel", autospec=True)
class TestSecureAuthorizedChannel(object):
    @mock.patch("google.auth.transport._mtls_helper._load_json_file", autospec=True)
    @mock.patch("google.auth.transport._mtls_helper._check_config_path", autospec=True)
    def test_secure_authorized_channel_adc(
        self,
        check_config_path,
        load_json_file,
        secure_channel,
        ssl_channel_credentials,
        metadata_call_credentials,
        composite_channel_credentials,
        get_client_ssl_credentials,
    ):
        credentials = CredentialsStub()
        request = mock.create_autospec(transport.Request)
        target = "example.com:80"

        # Mock the context aware metadata and client cert/key so mTLS SSL channel
        # will be used.
        check_config_path.return_value = METADATA_PATH
        load_json_file.return_value = {"cert_provider_command": ["some command"]}
        get_client_ssl_credentials.return_value = (
            True,
            PUBLIC_CERT_BYTES,
            PRIVATE_KEY_BYTES,
            None,
        )

        channel = None
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            channel = google.auth.transport.grpc.secure_authorized_channel(
                credentials, request, target, options=mock.sentinel.options
            )

        # Check the auth plugin construction.
        auth_plugin = metadata_call_credentials.call_args[0][0]
        assert isinstance(auth_plugin, google.auth.transport.grpc.AuthMetadataPlugin)
        assert auth_plugin._credentials == credentials
        assert auth_plugin._request == request

        # Check the ssl channel call.
        ssl_channel_credentials.assert_called_once_with(
            certificate_chain=PUBLIC_CERT_BYTES, private_key=PRIVATE_KEY_BYTES
        )

        # Check the composite credentials call.
        composite_channel_credentials.assert_called_once_with(
            ssl_channel_credentials.return_value, metadata_call_credentials.return_value
        )

        # Check the channel call.
        secure_channel.assert_called_once_with(
            target,
            composite_channel_credentials.return_value,
            options=mock.sentinel.options,
        )
        assert unwrap(channel) == secure_channel.return_value

    @mock.patch("google.auth.transport.grpc.SslCredentials", autospec=True)
    def test_secure_authorized_channel_adc_without_client_cert_env(
        self,
        ssl_credentials_adc_method,
        secure_channel,
        ssl_channel_credentials,
        metadata_call_credentials,
        composite_channel_credentials,
        get_client_ssl_credentials,
    ):
        # Test client cert won't be used if GOOGLE_API_USE_CLIENT_CERTIFICATE
        # environment variable is not set.
        credentials = CredentialsStub()
        request = mock.create_autospec(transport.Request)
        target = "example.com:80"

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "false"}
        ):
            channel = google.auth.transport.grpc.secure_authorized_channel(
                credentials, request, target, options=mock.sentinel.options
            )

        # Check the auth plugin construction.
        auth_plugin = metadata_call_credentials.call_args[0][0]
        assert isinstance(auth_plugin, google.auth.transport.grpc.AuthMetadataPlugin)
        assert auth_plugin._credentials == credentials
        assert auth_plugin._request == request

        # Check the ssl channel call.
        ssl_channel_credentials.assert_called_once()
        ssl_credentials_adc_method.assert_not_called()

        # Check the composite credentials call.
        composite_channel_credentials.assert_called_once_with(
            ssl_channel_credentials.return_value, metadata_call_credentials.return_value
        )

        # Check the channel call.
        secure_channel.assert_called_once_with(
            target,
            composite_channel_credentials.return_value,
            options=mock.sentinel.options,
        )
        assert unwrap(channel) == secure_channel.return_value

    def test_secure_authorized_channel_explicit_ssl(
        self,
        secure_channel,
        ssl_channel_credentials,
        metadata_call_credentials,
        composite_channel_credentials,
        get_client_ssl_credentials,
    ):
        credentials = mock.Mock()
        request = mock.Mock()
        target = "example.com:80"
        ssl_credentials = mock.Mock()

        google.auth.transport.grpc.secure_authorized_channel(
            credentials, request, target, ssl_credentials=ssl_credentials
        )

        # Since explicit SSL credentials are provided, get_client_ssl_credentials
        # shouldn't be called.
        assert not get_client_ssl_credentials.called

        # Check the ssl channel call.
        assert not ssl_channel_credentials.called

        # Check the composite credentials call.
        composite_channel_credentials.assert_called_once_with(
            ssl_credentials, metadata_call_credentials.return_value
        )

    def test_secure_authorized_channel_mutual_exclusive(
        self,
        secure_channel,
        ssl_channel_credentials,
        metadata_call_credentials,
        composite_channel_credentials,
        get_client_ssl_credentials,
    ):
        credentials = mock.Mock()
        request = mock.Mock()
        target = "example.com:80"
        ssl_credentials = mock.Mock()
        client_cert_callback = mock.Mock()

        with pytest.raises(ValueError):
            google.auth.transport.grpc.secure_authorized_channel(
                credentials,
                request,
                target,
                ssl_credentials=ssl_credentials,
                client_cert_callback=client_cert_callback,
            )

    def test_secure_authorized_channel_with_client_cert_callback_success(
        self,
        secure_channel,
        ssl_channel_credentials,
        metadata_call_credentials,
        composite_channel_credentials,
        get_client_ssl_credentials,
    ):
        credentials = mock.Mock()
        request = mock.Mock()
        target = "example.com:80"
        client_cert_callback = mock.Mock()
        client_cert_callback.return_value = (PUBLIC_CERT_BYTES, PRIVATE_KEY_BYTES)

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            google.auth.transport.grpc.secure_authorized_channel(
                credentials, request, target, client_cert_callback=client_cert_callback
            )

        client_cert_callback.assert_called_once()

        # Check we are using the cert and key provided by client_cert_callback.
        ssl_channel_credentials.assert_called_once_with(
            certificate_chain=PUBLIC_CERT_BYTES, private_key=PRIVATE_KEY_BYTES
        )

        # Check the composite credentials call.
        composite_channel_credentials.assert_called_once_with(
            ssl_channel_credentials.return_value, metadata_call_credentials.return_value
        )

    @mock.patch("google.auth.transport._mtls_helper._load_json_file", autospec=True)
    @mock.patch("google.auth.transport._mtls_helper._check_config_path", autospec=True)
    def test_secure_authorized_channel_with_client_cert_callback_failure(
        self,
        check_config_path,
        load_json_file,
        secure_channel,
        ssl_channel_credentials,
        metadata_call_credentials,
        composite_channel_credentials,
        get_client_ssl_credentials,
    ):
        credentials = mock.Mock()
        request = mock.Mock()
        target = "example.com:80"

        client_cert_callback = mock.Mock()
        client_cert_callback.side_effect = Exception("callback exception")

        with pytest.raises(Exception) as excinfo:
            with mock.patch.dict(
                os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
            ):
                google.auth.transport.grpc.secure_authorized_channel(
                    credentials,
                    request,
                    target,
                    client_cert_callback=client_cert_callback,
                )

        assert str(excinfo.value) == "callback exception"

    def test_secure_authorized_channel_cert_callback_without_client_cert_env(
        self,
        secure_channel,
        ssl_channel_credentials,
        metadata_call_credentials,
        composite_channel_credentials,
        get_client_ssl_credentials,
    ):
        # Test client cert won't be used if GOOGLE_API_USE_CLIENT_CERTIFICATE
        # environment variable is not set.
        credentials = mock.Mock()
        request = mock.Mock()
        target = "example.com:80"
        client_cert_callback = mock.Mock()

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "false"}
        ):
            google.auth.transport.grpc.secure_authorized_channel(
                credentials, request, target, client_cert_callback=client_cert_callback
            )

        # Check client_cert_callback is not called because GOOGLE_API_USE_CLIENT_CERTIFICATE
        # is not set.
        client_cert_callback.assert_not_called()

        ssl_channel_credentials.assert_called_once()

        # Check the composite credentials call.
        composite_channel_credentials.assert_called_once_with(
            ssl_channel_credentials.return_value, metadata_call_credentials.return_value
        )


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch(
    "google.auth.transport._mtls_helper.get_client_ssl_credentials", autospec=True
)
@mock.patch("google.auth.transport._mtls_helper._load_json_file", autospec=True)
@mock.patch("google.auth.transport._mtls_helper._check_config_path", autospec=True)
class TestSslCredentials(object):
    @mock.patch("os.path.exists", autospec=True)
    def test_no_context_aware_metadata(
        self,
        mock_path_exists,
        mock_check_config_path,
        mock_load_json_file,
        mock_get_client_ssl_credentials,
        mock_ssl_channel_credentials,
    ):
        mock_path_exists.return_value = False
        # Mock that the metadata file doesn't exist.
        mock_check_config_path.return_value = None

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            ssl_credentials = google.auth.transport.grpc.SslCredentials()

        # Since no context aware metadata is found, we wouldn't call
        # get_client_ssl_credentials, and the SSL channel credentials created is
        # non mTLS.
        assert ssl_credentials.ssl_credentials is not None
        assert not ssl_credentials.is_mtls
        mock_get_client_ssl_credentials.assert_not_called()
        mock_ssl_channel_credentials.assert_called_once_with()

    def test_get_client_ssl_credentials_failure(
        self,
        mock_check_config_path,
        mock_load_json_file,
        mock_get_client_ssl_credentials,
        mock_ssl_channel_credentials,
    ):
        mock_check_config_path.return_value = METADATA_PATH
        mock_load_json_file.return_value = {"cert_provider_command": ["some command"]}

        # Mock that client cert and key are not loaded and exception is raised.
        mock_get_client_ssl_credentials.side_effect = exceptions.ClientCertError()

        with pytest.raises(exceptions.MutualTLSChannelError):
            with mock.patch.dict(
                os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
            ):
                assert google.auth.transport.grpc.SslCredentials().ssl_credentials

    def test_get_client_ssl_credentials_success(
        self,
        mock_check_config_path,
        mock_load_json_file,
        mock_get_client_ssl_credentials,
        mock_ssl_channel_credentials,
    ):
        mock_check_config_path.return_value = METADATA_PATH
        mock_load_json_file.return_value = {"cert_provider_command": ["some command"]}
        mock_get_client_ssl_credentials.return_value = (
            True,
            PUBLIC_CERT_BYTES,
            PRIVATE_KEY_BYTES,
            None,
        )

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            ssl_credentials = google.auth.transport.grpc.SslCredentials()

        assert ssl_credentials.ssl_credentials is not None
        assert ssl_credentials.is_mtls
        mock_get_client_ssl_credentials.assert_called_once()
        mock_ssl_channel_credentials.assert_called_once_with(
            certificate_chain=PUBLIC_CERT_BYTES, private_key=PRIVATE_KEY_BYTES
        )

    @mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", autospec=True
    )
    def test_get_client_ssl_credentials_workload_cert(
        self,
        mock_has_default_client_cert_source,
        mock_check_config_path,
        mock_load_json_file,
        mock_get_client_ssl_credentials,
        mock_ssl_channel_credentials,
    ):
        # Mock that context-aware metadata does not exist, but workload cert config does.
        mock_check_config_path.return_value = None
        mock_has_default_client_cert_source.return_value = True
        mock_get_client_ssl_credentials.return_value = (
            True,
            PUBLIC_CERT_BYTES,
            PRIVATE_KEY_BYTES,
            None,
        )

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            ssl_credentials = google.auth.transport.grpc.SslCredentials()

        # If a workload certificate config exists on the device (and use_client_cert is true),
        # is_mtls must be True and get_client_ssl_credentials should be invoked.
        assert ssl_credentials.ssl_credentials is not None
        assert ssl_credentials.is_mtls
        mock_get_client_ssl_credentials.assert_called_once()
        mock_ssl_channel_credentials.assert_called_once_with(
            certificate_chain=PUBLIC_CERT_BYTES, private_key=PRIVATE_KEY_BYTES
        )

    def test_get_client_ssl_credentials_without_client_cert_env(
        self,
        mock_check_config_path,
        mock_load_json_file,
        mock_get_client_ssl_credentials,
        mock_ssl_channel_credentials,
    ):
        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "false"}
        ):
            ssl_credentials = google.auth.transport.grpc.SslCredentials()

        assert ssl_credentials.ssl_credentials is not None
        assert not ssl_credentials.is_mtls
        mock_check_config_path.assert_not_called()
        mock_load_json_file.assert_not_called()
        mock_get_client_ssl_credentials.assert_not_called()
        mock_ssl_channel_credentials.assert_called_once()

    def test_get_client_ssl_credentials_no_workload_cert(
        self,
        mock_check_config_path,
        mock_load_json_file,
        mock_get_client_ssl_credentials,
        mock_ssl_channel_credentials,
    ):
        mock_check_config_path.return_value = METADATA_PATH
        mock_load_json_file.return_value = {"cert_provider_command": ["some command"]}
        mock_get_client_ssl_credentials.return_value = (
            False,
            None,
            None,
            None,
        )

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            ssl_credentials = google.auth.transport.grpc.SslCredentials()

        assert ssl_credentials.ssl_credentials is not None
        assert not ssl_credentials.is_mtls
        mock_get_client_ssl_credentials.assert_called_once()
        mock_ssl_channel_credentials.assert_called_once_with()

    def test_get_client_ssl_credentials_os_error(
        self,
        mock_check_config_path,
        mock_load_json_file,
        mock_get_client_ssl_credentials,
        mock_ssl_channel_credentials,
    ):
        mock_check_config_path.return_value = METADATA_PATH
        mock_load_json_file.return_value = {"cert_provider_command": ["some command"]}
        mock_get_client_ssl_credentials.side_effect = OSError("Mock file read error")

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            ssl_credentials = google.auth.transport.grpc.SslCredentials()

        with pytest.raises(exceptions.MutualTLSChannelError):
            _ = ssl_credentials.ssl_credentials

        assert ssl_credentials.is_mtls

    def test_get_client_ssl_credentials_transient_error_retry(
        self,
        mock_check_config_path,
        mock_load_json_file,
        mock_get_client_ssl_credentials,
        mock_ssl_channel_credentials,
    ):
        mock_check_config_path.return_value = METADATA_PATH
        mock_load_json_file.return_value = {"cert_provider_command": ["some command"]}
        # First call fails with OSError, second succeeds
        mock_get_client_ssl_credentials.side_effect = [
            OSError("Mock transient error"),
            (True, b"cert", b"key", None),
        ]

        with mock.patch.dict(
            os.environ, {environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE: "true"}
        ):
            ssl_credentials = google.auth.transport.grpc.SslCredentials()

        # First call raises error
        with pytest.raises(exceptions.MutualTLSChannelError):
            _ = ssl_credentials.ssl_credentials

        assert ssl_credentials.is_mtls  # Should remain True

        # Second call succeeds
        assert ssl_credentials.ssl_credentials is not None
        assert ssl_credentials.is_mtls
        mock_ssl_channel_credentials.assert_called_with(
            certificate_chain=b"cert", private_key=b"key"
        )

    def test_get_client_ssl_credentials_auto_enablement(
        self,
        mock_check_config_path,
        mock_load_json_file,
        mock_get_client_ssl_credentials,
        mock_ssl_channel_credentials,
    ):
        fake_config_content = '{"version": 1, "cert_configs": {"workload": {"cert_path": "/tmp/mock_cert.pem", "key_path": "/tmp/mock_key.pem"}}}'
        mock_get_client_ssl_credentials.return_value = (
            True,
            PUBLIC_CERT_BYTES,
            PRIVATE_KEY_BYTES,
            None,
        )

        with mock.patch.dict(
            os.environ,
            {
                environment_vars.GOOGLE_API_CERTIFICATE_CONFIG: "fake_config_path.json",
            },
        ), mock.patch(
            "builtins.open", mock.mock_open(read_data=fake_config_content)
        ), mock.patch(
            "os.path.exists", return_value=True
        ):
            # Ensure mTLS explicit flags are not present in the environment
            os.environ.pop(environment_vars.GOOGLE_API_USE_CLIENT_CERTIFICATE, None)
            os.environ.pop(
                environment_vars.CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE, None
            )
            ssl_credentials = google.auth.transport.grpc.SslCredentials()

        assert ssl_credentials.ssl_credentials is not None
        assert ssl_credentials.is_mtls
        mock_get_client_ssl_credentials.assert_called_once()
        mock_ssl_channel_credentials.assert_called_once_with(
            certificate_chain=PUBLIC_CERT_BYTES, private_key=PRIVATE_KEY_BYTES
        )


@mock.patch("google.auth.transport.grpc._ReplayableIterator")
def test_interceptor_uses_factory_if_callable(mock_replayable):
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()

    call_no_factory = transport_grpc._RetryableStreamResponseIterator(
        continuation=mock.Mock(),
        client_call_details=mock.Mock(),
        request_or_iterator=[b"1", b"2"],
        interceptor=interceptor,
        is_client_stream=True,
    )
    assert call_no_factory._uses_factory is False
    assert call_no_factory._payload is not None

    def generator_factory():
        return (x for x in [b"1", b"2"])

    call_factory = transport_grpc._RetryableStreamResponseIterator(
        continuation=mock.Mock(),
        client_call_details=mock.Mock(),
        request_or_iterator=generator_factory,
        interceptor=interceptor,
        is_client_stream=True,
    )
    assert call_factory._uses_factory is True
    assert call_factory._payload is None


@mock.patch("google.auth.transport.grpc.CertRotationInterceptor._should_retry")
def test_factory_infinite_replay_on_error(mock_should_retry):
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()
    interceptor._wrapper = mock.Mock()
    interceptor._wrapper._cached_cert = "cert"
    mock_should_retry.side_effect = [
        (True, b"cert", b"key", None),
        (False, None, None, None),
    ]

    mock_inner_call1 = mock.Mock()
    mock_err = transport_grpc.grpc.RpcError()
    mock_err.code = lambda: transport_grpc.grpc.StatusCode.UNAUTHENTICATED
    mock_inner_call1.__next__ = mock.Mock(side_effect=mock_err)

    mock_inner_call2 = mock.Mock()
    mock_inner_call2.__next__ = mock.Mock(side_effect=[b"SUCCESS", StopIteration])

    continuation = mock.Mock(side_effect=[mock_inner_call1, mock_inner_call2])

    factory_calls = 0

    def factory():
        nonlocal factory_calls
        factory_calls += 1
        return (x for x in [b"A"])

    stream = transport_grpc._RetryableStreamResponseIterator(
        continuation=continuation,
        client_call_details=mock.Mock(),
        request_or_iterator=factory,
        interceptor=interceptor,
        is_client_stream=True,
    )

    responses = list(stream)
    assert responses == [b"SUCCESS"]
    assert factory_calls == 2


@mock.patch("google.auth.transport._mtls_helper.decrypt_private_key")
@mock.patch(
    "google.auth.transport._mtls_helper.check_parameters_for_unauthorized_response"
)
@mock.patch("google.auth.transport.grpc.secure_authorized_channel")
def test_refresh_logic_closes_old_channel(
    mock_secure_channel, mock_check_params, mock_decrypt
):
    import google.auth.transport.grpc as transport_grpc

    mock_check_params.return_value = ("cert", "cert", "passphrase", "old_fp", "new_fp")
    mock_decrypt.return_value = b"decrypted_key"
    old_channel = mock.Mock()
    new_channel = mock.Mock()
    mock_secure_channel.return_value = new_channel

    subscriber = mock.Mock()

    refreshing_channel = transport_grpc.MTLSRefreshingChannel(
        target="example.com:443",
        factory_args={},
        initial_channel=old_channel,
        initial_cert="cert",
    )
    refreshing_channel.subscribe(subscriber)

    refreshing_channel.refresh_logic(
        1, call_cert_bytes=b"newcert", call_key_bytes=b"newkey", passphrase=None
    )

    old_channel.unsubscribe.assert_called_once_with(subscriber)
    new_channel.subscribe.assert_called_once_with(subscriber)
    # old_channel.close.assert_called_once()  # Removed in PR 18019


@mock.patch("google.auth.transport.grpc.CertRotationInterceptor._should_retry")
def test_unary_response_future_deadline_exceeded_on_retry(mock_should_retry):
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()
    interceptor._wrapper = mock.Mock()
    interceptor._wrapper._cached_cert = "cert"
    mock_should_retry.return_value = (True, b"cert", b"key", None)

    mock_err = transport_grpc.grpc.RpcError()
    mock_err.code = lambda: transport_grpc.grpc.StatusCode.UNAUTHENTICATED

    inner_future = mock.Mock()
    inner_future.exception = lambda: mock_err
    inner_future.result = mock.Mock(side_effect=mock_err)

    callbacks_fired = []

    def callback(f):
        callbacks_fired.append(f)

    call_details = mock.Mock()
    call_details.timeout = 0.001  # very short timeout

    # Simulating initial call
    future = transport_grpc._RetryableUnaryResponseFuture(
        continuation=lambda cd, pl: inner_future,
        client_call_details=call_details,
        request_or_iterator=b"request",
        interceptor=interceptor,
        is_client_stream=False,
    )
    future._completion_event.set()
    future.add_done_callback(callback)

    # Allow time to elapse so remaining timeout <= 0
    time.sleep(0.01)

    # Trigger inner future completion
    future._on_inner_future_done(inner_future)

    # Verify future is marked done and does not hang
    assert future.done() is True
    assert len(callbacks_fired) == 1
    with pytest.raises(transport_grpc.grpc.RpcError):
        future.result(timeout=1)


@mock.patch("google.auth.transport.grpc.CertRotationInterceptor._should_retry")
def test_unary_response_future_cancelled(mock_should_retry):
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()
    interceptor._wrapper = mock.Mock()
    interceptor._wrapper._cached_cert = "cert"

    # Mock an incoming cancelled inner_future
    inner_future = mock.Mock()
    inner_future.cancelled.return_value = True

    callbacks_fired = []

    def callback(f):
        callbacks_fired.append(f)

    # Throw an exception inside the callback execution to cover the newly added except branch
    def failing_callback(f):
        raise Exception("Deliberate failure to test exception catching")

    call_details = mock.Mock()
    future = transport_grpc._RetryableUnaryResponseFuture(
        continuation=lambda cd, pl: inner_future,
        client_call_details=call_details,
        request_or_iterator=b"request",
        interceptor=interceptor,
        is_client_stream=False,
    )
    future._completion_event.set()
    future.add_done_callback(callback)
    future.add_done_callback(failing_callback)

    future._on_inner_future_done(inner_future)

    assert future.done() is True
    assert len(callbacks_fired) == 1


@mock.patch("google.auth.transport.grpc.CertRotationInterceptor._should_retry")
def test_unary_response_future_rpc_error_retry_start_call_exception(mock_should_retry):
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()
    interceptor._wrapper = mock.Mock()
    interceptor._wrapper._cached_cert = "cert"

    mock_err = transport_grpc.grpc.RpcError()
    mock_err.code = lambda: transport_grpc.grpc.StatusCode.UNAUTHENTICATED
    mock_should_retry.return_value = (True, b"cert", b"key", None)

    inner_future = mock.Mock()
    inner_future.cancelled.return_value = False
    inner_future.exception.return_value = mock_err

    call_details = mock.Mock()

    future = transport_grpc._RetryableUnaryResponseFuture(
        continuation=lambda cd, pl: inner_future,
        client_call_details=call_details,
        request_or_iterator=b"request",
        interceptor=interceptor,
        is_client_stream=False,
    )
    future._completion_event.set()

    with mock.patch.object(future, "_start_call", side_effect=mock_err):
        future._on_inner_future_done(inner_future)

    assert interceptor._wrapper.refresh_logic.call_count == 2


def test_stream_response_iterator_done():
    import google.auth.transport.grpc as transport_grpc

    interceptor = mock.Mock()
    interceptor._wrapper = mock.Mock()
    interceptor._wrapper._cached_cert = "cert"

    iterator = transport_grpc._RetryableStreamResponseIterator(
        continuation=lambda cd, pl: mock.Mock(),
        client_call_details=mock.Mock(),
        request_or_iterator=b"request",
        interceptor=interceptor,
        is_client_stream=False,
    )

    assert iterator.done() is False
    iterator._is_completed = True
    assert iterator.done() is True


def test_start_call_wrapper_none():
    import pytest
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()
    if hasattr(interceptor, "_wrapper"):
        del interceptor._wrapper

    inner_future = mock.Mock()
    call_details = mock.Mock()

    with pytest.raises(AttributeError):
        transport_grpc._RetryableUnaryResponseFuture(
            continuation=lambda cd, pl: inner_future,
            client_call_details=call_details,
            request_or_iterator=b"request",
            interceptor=interceptor,
            is_client_stream=False,
        )


def test_start_call_wrapper_none_branch():
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()
    interceptor._wrapper = None

    inner_future = mock.Mock()
    call_details = mock.Mock()

    future = transport_grpc._RetryableUnaryResponseFuture(
        continuation=lambda cd, pl: inner_future,
        client_call_details=call_details,
        request_or_iterator=b"request",
        interceptor=interceptor,
        is_client_stream=False,
    )
    future._completion_event.set()
    assert getattr(future, "_attempt_cert", "NOT_SET") is None


@mock.patch("google.auth.transport.grpc.CertRotationInterceptor._should_retry")
def test_unary_response_future_rpc_error_no_wrapper(mock_should_retry):
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()
    interceptor._wrapper = None

    mock_err = transport_grpc.grpc.RpcError()
    mock_err.code = lambda: transport_grpc.grpc.StatusCode.UNAUTHENTICATED
    mock_should_retry.return_value = (True, b"cert", b"key", None)

    inner_future = mock.Mock()
    inner_future.cancelled.return_value = False
    inner_future.exception.return_value = mock_err

    call_details = mock.Mock()

    future = transport_grpc._RetryableUnaryResponseFuture(
        continuation=lambda cd, pl: inner_future,
        client_call_details=call_details,
        request_or_iterator=b"request",
        interceptor=interceptor,
        is_client_stream=False,
    )
    future._completion_event.set()

    with mock.patch.object(future, "_start_call", side_effect=mock_err):
        future._on_inner_future_done(inner_future)


@mock.patch("google.auth.transport.grpc.CertRotationInterceptor._should_retry")
def test_unary_response_future_rpc_error_should_not_retry(mock_should_retry):
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()
    interceptor._wrapper = mock.Mock()
    interceptor._wrapper._cached_cert = "cert"

    mock_err = transport_grpc.grpc.RpcError()
    mock_err.code = lambda: transport_grpc.grpc.StatusCode.UNAUTHENTICATED
    mock_should_retry.return_value = (False, None, None, None)

    inner_future = mock.Mock()
    inner_future.cancelled.return_value = False
    inner_future.exception.return_value = mock_err

    call_details = mock.Mock()

    future = transport_grpc._RetryableUnaryResponseFuture(
        continuation=lambda cd, pl: inner_future,
        client_call_details=call_details,
        request_or_iterator=b"request",
        interceptor=interceptor,
        is_client_stream=False,
    )
    future._completion_event.set()

    with mock.patch.object(future, "_start_call", side_effect=mock_err):
        future._on_inner_future_done(inner_future)

    interceptor._wrapper.refresh_logic.assert_not_called()


def test_mtls_call_interceptor_should_retry_cases():
    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()

    assert interceptor._should_retry(grpc.StatusCode.UNAUTHENTICATED, 0, "cert1") == (
        False,
        None,
        None,
        None,
    )

    wrapper_mock = mock.Mock()
    wrapper_mock._cached_cert = "cert1"
    interceptor._wrapper = wrapper_mock
    assert interceptor._should_retry(grpc.StatusCode.INTERNAL, 0, "cert1") == (
        False,
        None,
        None,
        None,
    )
    assert interceptor._should_retry(grpc.StatusCode.UNAUTHENTICATED, 2, "cert1") == (
        False,
        None,
        None,
        None,
    )

    wrapper_mock._cached_cert = "cert2"
    assert interceptor._should_retry(grpc.StatusCode.UNAUTHENTICATED, 0, "cert1") == (
        True,
        None,
        None,
        None,
    )

    wrapper_mock._cached_cert = "cert1"
    with mock.patch(
        "google.auth.transport._mtls_helper.check_parameters_for_unauthorized_response"
    ) as mock_check:
        mock_check.return_value = (None, None, None, "fp1", "fp2")
        assert interceptor._should_retry(
            grpc.StatusCode.UNAUTHENTICATED, 0, "cert1"
        ) == (True, None, None, None)

    with mock.patch(
        "google.auth.transport._mtls_helper.check_parameters_for_unauthorized_response"
    ) as mock_check:
        mock_check.return_value = (None, None, None, "fp1", "fp1")
        assert interceptor._should_retry(
            grpc.StatusCode.UNAUTHENTICATED, 0, "cert1"
        ) == (False, None, None, None)


def test_mtls_call_interceptor_interceptors_methods():
    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    interceptor = transport_grpc.CertRotationInterceptor()

    def dummy_continuation(*args, **kwargs):
        return mock.Mock()

    mock_details = mock.Mock()
    mock_request = mock.Mock()

    res = interceptor.intercept_unary_unary(
        dummy_continuation, mock_details, mock_request
    )
    assert isinstance(res, transport_grpc._RetryableUnaryResponseFuture)

    res = interceptor.intercept_stream_unary(
        dummy_continuation, mock_details, mock_request
    )
    assert isinstance(res, transport_grpc._RetryableUnaryResponseFuture)

    res = interceptor.intercept_unary_stream(
        dummy_continuation, mock_details, mock_request
    )
    assert isinstance(res, transport_grpc._RetryableStreamResponseIterator)

    res = interceptor.intercept_stream_stream(
        dummy_continuation, mock_details, mock_request
    )
    assert isinstance(res, transport_grpc._RetryableStreamResponseIterator)


def test_mtls_refreshing_channel_refresh_logic_cases():
    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    channel = transport_grpc.MTLSRefreshingChannel("target", {}, mock.Mock(), b"cert1")
    with mock.patch(
        "google.auth.transport._mtls_helper.check_parameters_for_unauthorized_response"
    ) as mock_check, mock.patch("google.auth.transport.grpc.secure_authorized_channel"):
        mock_check.return_value = (None, None, None, "fp1", "fp1")
        assert (
            channel.refresh_logic(
                1,
                call_cert_bytes=mock_check.return_value[0],
                call_key_bytes=mock_check.return_value[1],
            )
            is None
        )
        mock_check.return_value = (None, None, None, "fp1", "fp2")
        assert (
            channel.refresh_logic(
                0,
                call_cert_bytes=mock_check.return_value[0],
                call_key_bytes=mock_check.return_value[1],
            )
            is None
        )

    def dummy_callback():
        return b"cert2", b"key2", None

    with mock.patch(
        "google.auth.transport._mtls_helper.check_parameters_for_unauthorized_response"
    ) as mock_check, mock.patch(
        "google.auth.transport.grpc.secure_authorized_channel"
    ) as mock_secure:
        mock_check.return_value = (b"cert2", b"key2", None, "fp1", "fp2")
        new_channel_mock = mock.Mock()
        mock_secure.return_value = new_channel_mock
        assert (
            channel.refresh_logic(
                0,
                call_cert_bytes=mock_check.return_value[0],
                call_key_bytes=mock_check.return_value[1],
            )
            is None
        )
        assert channel._cached_cert == b"cert2"
        assert channel._channel == new_channel_mock


def test_mtls_refreshing_channel_subscribe_unsubscribe_close():
    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    channel = transport_grpc.MTLSRefreshingChannel("target", {}, mock.Mock(), b"cert1")
    cb = mock.Mock()
    channel.subscribe(cb)
    assert cb in channel._subscribers
    channel.unsubscribe(cb)
    assert cb not in channel._subscribers

    channel.close()
    assert channel._channel.close.called


def test_mtls_refreshing_channel_unary_unary():
    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    channel = transport_grpc.MTLSRefreshingChannel("target", {}, mock.Mock(), b"cert1")
    res = channel.unary_unary("method")
    assert res is not None

    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    channel = transport_grpc.MTLSRefreshingChannel("target", {}, mock.Mock(), b"cert1")
    res = channel.unary_unary("method")
    assert res is not None


def test_mtls_refreshing_channel_unary_stream():
    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    channel = transport_grpc.MTLSRefreshingChannel("target", {}, mock.Mock(), b"cert1")
    res = channel.unary_stream("method")
    assert res is not None


def test_mtls_refreshing_channel_stream_unary():
    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    channel = transport_grpc.MTLSRefreshingChannel("target", {}, mock.Mock(), b"cert1")
    res = channel.stream_unary("method")
    assert res is not None


def test_mtls_refreshing_channel_stream_stream():
    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    channel = transport_grpc.MTLSRefreshingChannel("target", {}, mock.Mock(), b"cert1")
    res = channel.stream_stream("method")
    assert res is not None


def test_retryable_unary_response_future_methods():
    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    mock_future = mock.Mock()

    def dummy_continuation(*args, **kwargs):
        return mock_future

    interceptor = transport_grpc.CertRotationInterceptor()
    interceptor._wrapper = mock.Mock()
    interceptor._wrapper._cached_cert = "cert"

    future = transport_grpc._RetryableUnaryResponseFuture(
        dummy_continuation, mock.Mock(), mock.Mock(), interceptor
    )

    future._completion_event.set()
    future.initial_metadata()
    future.trailing_metadata()
    future.code()
    future.details()
    future.cancel()
    future.cancelled()
    future.is_active()
    future.time_remaining()

    mock_future.result.return_value = "r"
    assert future.result() == "r"
    mock_future.exception.return_value = Exception("e")
    assert isinstance(future.exception(), Exception)
    mock_future.traceback.return_value = "tb"
    assert future.traceback() == "tb"

    future.add_done_callback(lambda x: None)


def test_retryable_stream_response_iterator_methods():
    from unittest import mock
    import google.auth.transport.grpc as transport_grpc

    mock_iterator = mock.Mock()

    def dummy_continuation(*args, **kwargs):
        return mock_iterator

    interceptor = transport_grpc.CertRotationInterceptor()
    interceptor._wrapper = mock.Mock()
    interceptor._wrapper._cached_cert = "cert"

    iterator = transport_grpc._RetryableStreamResponseIterator(
        dummy_continuation, mock.Mock(), mock.Mock(), interceptor
    )

    iterator.initial_metadata()
    iterator.trailing_metadata()
    iterator.code()
    iterator.details()
    iterator.cancel()
    iterator.cancelled()
    iterator.is_active()
    iterator.time_remaining()
    iterator.add_done_callback(lambda x: None)


def test_grpc_version_warning_for_older_version(monkeypatch):
    monkeypatch.setattr(grpc, "__version__", "1.80.0")
    with pytest.warns(
        FutureWarning, match="does not support Post-Quantum Cryptography"
    ):
        importlib.reload(google.auth.transport.grpc)


def test_grpc_version_warning_not_emitted_for_supported_version(monkeypatch):
    monkeypatch.setattr(grpc, "__version__", "1.83.0")
    with warnings.catch_warnings():
        warnings.simplefilter("error", FutureWarning)
        importlib.reload(google.auth.transport.grpc)


def test_grpc_version_warning_not_emitted_when_no_version(monkeypatch):
    monkeypatch.delattr(grpc, "__version__", raising=False)
    with warnings.catch_warnings():
        warnings.simplefilter("error", FutureWarning)
        importlib.reload(google.auth.transport.grpc)
