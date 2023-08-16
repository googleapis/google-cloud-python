# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers

from google.api import monitored_resource_pb2  # type: ignore
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2AsyncClient
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client
from google.cloud.logging_v2.services.logging_service_v2 import pagers
from google.cloud.logging_v2.services.logging_service_v2 import transports
from google.cloud.logging_v2.types import log_entry
from google.cloud.logging_v2.types import logging
from google.logging.type import http_request_pb2  # type: ignore
from google.logging.type import log_severity_pb2  # type: ignore
from google.longrunning import operations_pb2 # type: ignore
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return "foo.googleapis.com" if ("localhost" in client.DEFAULT_ENDPOINT) else client.DEFAULT_ENDPOINT


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert LoggingServiceV2Client._get_default_mtls_endpoint(None) is None
    assert LoggingServiceV2Client._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert LoggingServiceV2Client._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert LoggingServiceV2Client._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert LoggingServiceV2Client._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert LoggingServiceV2Client._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class,transport_name", [
    (LoggingServiceV2Client, "grpc"),
    (LoggingServiceV2AsyncClient, "grpc_asyncio"),
])
def test_logging_service_v2_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_info') as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'logging.googleapis.com:443'
        )


@pytest.mark.parametrize("transport_class,transport_name", [
    (transports.LoggingServiceV2GrpcTransport, "grpc"),
    (transports.LoggingServiceV2GrpcAsyncIOTransport, "grpc_asyncio"),
])
def test_logging_service_v2_client_service_account_always_use_jwt(transport_class, transport_name):
    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class,transport_name", [
    (LoggingServiceV2Client, "grpc"),
    (LoggingServiceV2AsyncClient, "grpc_asyncio"),
])
def test_logging_service_v2_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'logging.googleapis.com:443'
        )


def test_logging_service_v2_client_get_transport_class():
    transport = LoggingServiceV2Client.get_transport_class()
    available_transports = [
        transports.LoggingServiceV2GrpcTransport,
    ]
    assert transport in available_transports

    transport = LoggingServiceV2Client.get_transport_class("grpc")
    assert transport == transports.LoggingServiceV2GrpcTransport


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (LoggingServiceV2Client, transports.LoggingServiceV2GrpcTransport, "grpc"),
    (LoggingServiceV2AsyncClient, transports.LoggingServiceV2GrpcAsyncIOTransport, "grpc_asyncio"),
])
@mock.patch.object(LoggingServiceV2Client, "DEFAULT_ENDPOINT", modify_default_endpoint(LoggingServiceV2Client))
@mock.patch.object(LoggingServiceV2AsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(LoggingServiceV2AsyncClient))
def test_logging_service_v2_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(LoggingServiceV2Client, 'get_transport_class') as gtc:
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(LoggingServiceV2Client, 'get_transport_class') as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(api_audience="https://language.googleapis.com")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com"
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,use_client_cert_env", [
    (LoggingServiceV2Client, transports.LoggingServiceV2GrpcTransport, "grpc", "true"),
    (LoggingServiceV2AsyncClient, transports.LoggingServiceV2GrpcAsyncIOTransport, "grpc_asyncio", "true"),
    (LoggingServiceV2Client, transports.LoggingServiceV2GrpcTransport, "grpc", "false"),
    (LoggingServiceV2AsyncClient, transports.LoggingServiceV2GrpcAsyncIOTransport, "grpc_asyncio", "false"),
])
@mock.patch.object(LoggingServiceV2Client, "DEFAULT_ENDPOINT", modify_default_endpoint(LoggingServiceV2Client))
@mock.patch.object(LoggingServiceV2AsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(LoggingServiceV2AsyncClient))
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_logging_service_v2_client_mtls_env_auto(client_class, transport_class, transport_name, use_client_cert_env):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        options = client_options.ClientOptions(client_cert_source=client_cert_source_callback)
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
                with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=client_cert_source_callback):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch("google.auth.transport.mtls.has_default_client_cert_source", return_value=False):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [
    LoggingServiceV2Client, LoggingServiceV2AsyncClient
])
@mock.patch.object(LoggingServiceV2Client, "DEFAULT_ENDPOINT", modify_default_endpoint(LoggingServiceV2Client))
@mock.patch.object(LoggingServiceV2AsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(LoggingServiceV2AsyncClient))
def test_logging_service_v2_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=False):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
            with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=mock_client_cert_source):
                api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (LoggingServiceV2Client, transports.LoggingServiceV2GrpcTransport, "grpc"),
    (LoggingServiceV2AsyncClient, transports.LoggingServiceV2GrpcAsyncIOTransport, "grpc_asyncio"),
])
def test_logging_service_v2_client_client_options_scopes(client_class, transport_class, transport_name):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (LoggingServiceV2Client, transports.LoggingServiceV2GrpcTransport, "grpc", grpc_helpers),
    (LoggingServiceV2AsyncClient, transports.LoggingServiceV2GrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_logging_service_v2_client_client_options_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

def test_logging_service_v2_client_client_options_from_dict():
    with mock.patch('google.cloud.logging_v2.services.logging_service_v2.transports.LoggingServiceV2GrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = LoggingServiceV2Client(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (LoggingServiceV2Client, transports.LoggingServiceV2GrpcTransport, "grpc", grpc_helpers),
    (LoggingServiceV2AsyncClient, transports.LoggingServiceV2GrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_logging_service_v2_client_create_channel_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "logging.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/cloud-platform.read-only',
                'https://www.googleapis.com/auth/logging.admin',
                'https://www.googleapis.com/auth/logging.read',
                'https://www.googleapis.com/auth/logging.write',
),
            scopes=None,
            default_host="logging.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("request_type", [
  logging.DeleteLogRequest,
  dict,
])
def test_delete_log(request_type, transport: str = 'grpc'):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_log),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_log(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.DeleteLogRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_log_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_log),
            '__call__') as call:
        client.delete_log()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.DeleteLogRequest()

@pytest.mark.asyncio
async def test_delete_log_async(transport: str = 'grpc_asyncio', request_type=logging.DeleteLogRequest):
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_log),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_log(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.DeleteLogRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_log_async_from_dict():
    await test_delete_log_async(request_type=dict)


def test_delete_log_field_headers():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging.DeleteLogRequest()

    request.log_name = 'log_name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_log),
            '__call__') as call:
        call.return_value = None
        client.delete_log(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'log_name=log_name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_log_field_headers_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging.DeleteLogRequest()

    request.log_name = 'log_name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_log),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_log(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'log_name=log_name_value',
    ) in kw['metadata']


def test_delete_log_flattened():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_log),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_log(
            log_name='log_name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].log_name
        mock_val = 'log_name_value'
        assert arg == mock_val


def test_delete_log_flattened_error():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_log(
            logging.DeleteLogRequest(),
            log_name='log_name_value',
        )

@pytest.mark.asyncio
async def test_delete_log_flattened_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_log),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_log(
            log_name='log_name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].log_name
        mock_val = 'log_name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_log_flattened_error_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_log(
            logging.DeleteLogRequest(),
            log_name='log_name_value',
        )


@pytest.mark.parametrize("request_type", [
  logging.WriteLogEntriesRequest,
  dict,
])
def test_write_log_entries(request_type, transport: str = 'grpc'):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.write_log_entries),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.WriteLogEntriesResponse(
        )
        response = client.write_log_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.WriteLogEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging.WriteLogEntriesResponse)


def test_write_log_entries_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.write_log_entries),
            '__call__') as call:
        client.write_log_entries()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.WriteLogEntriesRequest()

@pytest.mark.asyncio
async def test_write_log_entries_async(transport: str = 'grpc_asyncio', request_type=logging.WriteLogEntriesRequest):
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.write_log_entries),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging.WriteLogEntriesResponse(
        ))
        response = await client.write_log_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.WriteLogEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging.WriteLogEntriesResponse)


@pytest.mark.asyncio
async def test_write_log_entries_async_from_dict():
    await test_write_log_entries_async(request_type=dict)


def test_write_log_entries_flattened():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.write_log_entries),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.WriteLogEntriesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.write_log_entries(
            log_name='log_name_value',
            resource=monitored_resource_pb2.MonitoredResource(type='type_value'),
            labels={'key_value': 'value_value'},
            entries=[log_entry.LogEntry(log_name='log_name_value')],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].log_name
        mock_val = 'log_name_value'
        assert arg == mock_val
        arg = args[0].resource
        mock_val = monitored_resource_pb2.MonitoredResource(type='type_value')
        assert arg == mock_val
        arg = args[0].labels
        mock_val = {'key_value': 'value_value'}
        assert arg == mock_val
        arg = args[0].entries
        mock_val = [log_entry.LogEntry(log_name='log_name_value')]
        assert arg == mock_val


def test_write_log_entries_flattened_error():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.write_log_entries(
            logging.WriteLogEntriesRequest(),
            log_name='log_name_value',
            resource=monitored_resource_pb2.MonitoredResource(type='type_value'),
            labels={'key_value': 'value_value'},
            entries=[log_entry.LogEntry(log_name='log_name_value')],
        )

@pytest.mark.asyncio
async def test_write_log_entries_flattened_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.write_log_entries),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.WriteLogEntriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging.WriteLogEntriesResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.write_log_entries(
            log_name='log_name_value',
            resource=monitored_resource_pb2.MonitoredResource(type='type_value'),
            labels={'key_value': 'value_value'},
            entries=[log_entry.LogEntry(log_name='log_name_value')],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].log_name
        mock_val = 'log_name_value'
        assert arg == mock_val
        arg = args[0].resource
        mock_val = monitored_resource_pb2.MonitoredResource(type='type_value')
        assert arg == mock_val
        arg = args[0].labels
        mock_val = {'key_value': 'value_value'}
        assert arg == mock_val
        arg = args[0].entries
        mock_val = [log_entry.LogEntry(log_name='log_name_value')]
        assert arg == mock_val

@pytest.mark.asyncio
async def test_write_log_entries_flattened_error_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.write_log_entries(
            logging.WriteLogEntriesRequest(),
            log_name='log_name_value',
            resource=monitored_resource_pb2.MonitoredResource(type='type_value'),
            labels={'key_value': 'value_value'},
            entries=[log_entry.LogEntry(log_name='log_name_value')],
        )


@pytest.mark.parametrize("request_type", [
  logging.ListLogEntriesRequest,
  dict,
])
def test_list_log_entries(request_type, transport: str = 'grpc'):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_log_entries),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogEntriesResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_log_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.ListLogEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLogEntriesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_log_entries_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_log_entries),
            '__call__') as call:
        client.list_log_entries()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.ListLogEntriesRequest()

@pytest.mark.asyncio
async def test_list_log_entries_async(transport: str = 'grpc_asyncio', request_type=logging.ListLogEntriesRequest):
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_log_entries),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging.ListLogEntriesResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_log_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.ListLogEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLogEntriesAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_log_entries_async_from_dict():
    await test_list_log_entries_async(request_type=dict)


def test_list_log_entries_flattened():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_log_entries),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogEntriesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_log_entries(
            resource_names=['resource_names_value'],
            filter='filter_value',
            order_by='order_by_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource_names
        mock_val = ['resource_names_value']
        assert arg == mock_val
        arg = args[0].filter
        mock_val = 'filter_value'
        assert arg == mock_val
        arg = args[0].order_by
        mock_val = 'order_by_value'
        assert arg == mock_val


def test_list_log_entries_flattened_error():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_log_entries(
            logging.ListLogEntriesRequest(),
            resource_names=['resource_names_value'],
            filter='filter_value',
            order_by='order_by_value',
        )

@pytest.mark.asyncio
async def test_list_log_entries_flattened_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_log_entries),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogEntriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging.ListLogEntriesResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_log_entries(
            resource_names=['resource_names_value'],
            filter='filter_value',
            order_by='order_by_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource_names
        mock_val = ['resource_names_value']
        assert arg == mock_val
        arg = args[0].filter
        mock_val = 'filter_value'
        assert arg == mock_val
        arg = args[0].order_by
        mock_val = 'order_by_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_log_entries_flattened_error_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_log_entries(
            logging.ListLogEntriesRequest(),
            resource_names=['resource_names_value'],
            filter='filter_value',
            order_by='order_by_value',
        )


def test_list_log_entries_pager(transport_name: str = "grpc"):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_log_entries),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
                next_page_token='abc',
            ),
            logging.ListLogEntriesResponse(
                entries=[],
                next_page_token='def',
            ),
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                ],
                next_page_token='ghi',
            ),
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_log_entries(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, log_entry.LogEntry)
                   for i in results)
def test_list_log_entries_pages(transport_name: str = "grpc"):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_log_entries),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
                next_page_token='abc',
            ),
            logging.ListLogEntriesResponse(
                entries=[],
                next_page_token='def',
            ),
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                ],
                next_page_token='ghi',
            ),
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_log_entries(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_log_entries_async_pager():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_log_entries),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
                next_page_token='abc',
            ),
            logging.ListLogEntriesResponse(
                entries=[],
                next_page_token='def',
            ),
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                ],
                next_page_token='ghi',
            ),
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_log_entries(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, log_entry.LogEntry)
                for i in responses)


@pytest.mark.asyncio
async def test_list_log_entries_async_pages():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_log_entries),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
                next_page_token='abc',
            ),
            logging.ListLogEntriesResponse(
                entries=[],
                next_page_token='def',
            ),
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                ],
                next_page_token='ghi',
            ),
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_log_entries(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  logging.ListMonitoredResourceDescriptorsRequest,
  dict,
])
def test_list_monitored_resource_descriptors(request_type, transport: str = 'grpc'):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_monitored_resource_descriptors),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListMonitoredResourceDescriptorsResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_monitored_resource_descriptors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.ListMonitoredResourceDescriptorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMonitoredResourceDescriptorsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_monitored_resource_descriptors_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_monitored_resource_descriptors),
            '__call__') as call:
        client.list_monitored_resource_descriptors()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.ListMonitoredResourceDescriptorsRequest()

@pytest.mark.asyncio
async def test_list_monitored_resource_descriptors_async(transport: str = 'grpc_asyncio', request_type=logging.ListMonitoredResourceDescriptorsRequest):
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_monitored_resource_descriptors),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging.ListMonitoredResourceDescriptorsResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_monitored_resource_descriptors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.ListMonitoredResourceDescriptorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMonitoredResourceDescriptorsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_monitored_resource_descriptors_async_from_dict():
    await test_list_monitored_resource_descriptors_async(request_type=dict)


def test_list_monitored_resource_descriptors_pager(transport_name: str = "grpc"):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_monitored_resource_descriptors),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
                next_page_token='abc',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[],
                next_page_token='def',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
                next_page_token='ghi',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_monitored_resource_descriptors(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, monitored_resource_pb2.MonitoredResourceDescriptor)
                   for i in results)
def test_list_monitored_resource_descriptors_pages(transport_name: str = "grpc"):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_monitored_resource_descriptors),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
                next_page_token='abc',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[],
                next_page_token='def',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
                next_page_token='ghi',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_monitored_resource_descriptors(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_monitored_resource_descriptors_async_pager():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_monitored_resource_descriptors),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
                next_page_token='abc',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[],
                next_page_token='def',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
                next_page_token='ghi',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_monitored_resource_descriptors(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, monitored_resource_pb2.MonitoredResourceDescriptor)
                for i in responses)


@pytest.mark.asyncio
async def test_list_monitored_resource_descriptors_async_pages():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_monitored_resource_descriptors),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
                next_page_token='abc',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[],
                next_page_token='def',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
                next_page_token='ghi',
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                    monitored_resource_pb2.MonitoredResourceDescriptor(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_monitored_resource_descriptors(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  logging.ListLogsRequest,
  dict,
])
def test_list_logs(request_type, transport: str = 'grpc'):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogsResponse(
            log_names=['log_names_value'],
            next_page_token='next_page_token_value',
        )
        response = client.list_logs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.ListLogsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLogsPager)
    assert response.log_names == ['log_names_value']
    assert response.next_page_token == 'next_page_token_value'


def test_list_logs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__') as call:
        client.list_logs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.ListLogsRequest()

@pytest.mark.asyncio
async def test_list_logs_async(transport: str = 'grpc_asyncio', request_type=logging.ListLogsRequest):
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging.ListLogsResponse(
            log_names=['log_names_value'],
            next_page_token='next_page_token_value',
        ))
        response = await client.list_logs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging.ListLogsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLogsAsyncPager)
    assert response.log_names == ['log_names_value']
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_logs_async_from_dict():
    await test_list_logs_async(request_type=dict)


def test_list_logs_field_headers():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging.ListLogsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__') as call:
        call.return_value = logging.ListLogsResponse()
        client.list_logs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_logs_field_headers_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging.ListLogsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging.ListLogsResponse())
        await client.list_logs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_logs_flattened():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_logs(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_logs_flattened_error():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_logs(
            logging.ListLogsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_logs_flattened_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging.ListLogsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_logs(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_logs_flattened_error_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_logs(
            logging.ListLogsRequest(),
            parent='parent_value',
        )


def test_list_logs_pager(transport_name: str = "grpc"):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogsResponse(
                log_names=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token='abc',
            ),
            logging.ListLogsResponse(
                log_names=[],
                next_page_token='def',
            ),
            logging.ListLogsResponse(
                log_names=[
                    str(),
                ],
                next_page_token='ghi',
            ),
            logging.ListLogsResponse(
                log_names=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_logs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, str)
                   for i in results)
def test_list_logs_pages(transport_name: str = "grpc"):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogsResponse(
                log_names=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token='abc',
            ),
            logging.ListLogsResponse(
                log_names=[],
                next_page_token='def',
            ),
            logging.ListLogsResponse(
                log_names=[
                    str(),
                ],
                next_page_token='ghi',
            ),
            logging.ListLogsResponse(
                log_names=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_logs(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_logs_async_pager():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogsResponse(
                log_names=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token='abc',
            ),
            logging.ListLogsResponse(
                log_names=[],
                next_page_token='def',
            ),
            logging.ListLogsResponse(
                log_names=[
                    str(),
                ],
                next_page_token='ghi',
            ),
            logging.ListLogsResponse(
                log_names=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_logs(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, str)
                for i in responses)


@pytest.mark.asyncio
async def test_list_logs_async_pages():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_logs),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogsResponse(
                log_names=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token='abc',
            ),
            logging.ListLogsResponse(
                log_names=[],
                next_page_token='def',
            ),
            logging.ListLogsResponse(
                log_names=[
                    str(),
                ],
                next_page_token='ghi',
            ),
            logging.ListLogsResponse(
                log_names=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_logs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  logging.TailLogEntriesRequest,
  dict,
])
def test_tail_log_entries(request_type, transport: str = 'grpc'):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.tail_log_entries),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([logging.TailLogEntriesResponse()])
        response = client.tail_log_entries(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, logging.TailLogEntriesResponse)


@pytest.mark.asyncio
async def test_tail_log_entries_async(transport: str = 'grpc_asyncio', request_type=logging.TailLogEntriesRequest):
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.tail_log_entries),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(side_effect=[logging.TailLogEntriesResponse()])
        response = await client.tail_log_entries(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, logging.TailLogEntriesResponse)


@pytest.mark.asyncio
async def test_tail_log_entries_async_from_dict():
    await test_tail_log_entries_async(request_type=dict)


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = LoggingServiceV2Client(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = LoggingServiceV2Client(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = LoggingServiceV2Client(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = LoggingServiceV2Client(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = LoggingServiceV2Client(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = LoggingServiceV2Client(transport=transport)
    assert client.transport is transport

def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.LoggingServiceV2GrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

@pytest.mark.parametrize("transport_class", [
    transports.LoggingServiceV2GrpcTransport,
    transports.LoggingServiceV2GrpcAsyncIOTransport,
])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, 'default') as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()

@pytest.mark.parametrize("transport_name", [
    "grpc",
])
def test_transport_kind(transport_name):
    transport = LoggingServiceV2Client.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name

def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.LoggingServiceV2GrpcTransport,
    )

def test_logging_service_v2_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.LoggingServiceV2Transport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json"
        )


def test_logging_service_v2_base_transport():
    # Instantiate the base transport.
    with mock.patch('google.cloud.logging_v2.services.logging_service_v2.transports.LoggingServiceV2Transport.__init__') as Transport:
        Transport.return_value = None
        transport = transports.LoggingServiceV2Transport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'delete_log',
        'write_log_entries',
        'list_log_entries',
        'list_monitored_resource_descriptors',
        'list_logs',
        'tail_log_entries',
        'get_operation',
        'cancel_operation',
        'list_operations',
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        'kind',
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_logging_service_v2_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(google.auth, 'load_credentials_from_file', autospec=True) as load_creds, mock.patch('google.cloud.logging_v2.services.logging_service_v2.transports.LoggingServiceV2Transport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.LoggingServiceV2Transport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with("credentials.json",
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/cloud-platform.read-only',
            'https://www.googleapis.com/auth/logging.admin',
            'https://www.googleapis.com/auth/logging.read',
            'https://www.googleapis.com/auth/logging.write',
),
            quota_project_id="octopus",
        )


def test_logging_service_v2_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc, mock.patch('google.cloud.logging_v2.services.logging_service_v2.transports.LoggingServiceV2Transport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.LoggingServiceV2Transport()
        adc.assert_called_once()


def test_logging_service_v2_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        LoggingServiceV2Client()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/cloud-platform.read-only',
            'https://www.googleapis.com/auth/logging.admin',
            'https://www.googleapis.com/auth/logging.read',
            'https://www.googleapis.com/auth/logging.write',
),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LoggingServiceV2GrpcTransport,
        transports.LoggingServiceV2GrpcAsyncIOTransport,
    ],
)
def test_logging_service_v2_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(                'https://www.googleapis.com/auth/cloud-platform',                'https://www.googleapis.com/auth/cloud-platform.read-only',                'https://www.googleapis.com/auth/logging.admin',                'https://www.googleapis.com/auth/logging.read',                'https://www.googleapis.com/auth/logging.write',),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LoggingServiceV2GrpcTransport,
        transports.LoggingServiceV2GrpcAsyncIOTransport,
    ],
)
def test_logging_service_v2_transport_auth_gdch_credentials(transport_class):
    host = 'https://language.com'
    api_audience_tests = [None, 'https://language2.com']
    api_audience_expect = [host, 'https://language2.com']
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, 'default', autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(return_value=gdch_mock)
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(
                e
            )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.LoggingServiceV2GrpcTransport, grpc_helpers),
        (transports.LoggingServiceV2GrpcAsyncIOTransport, grpc_helpers_async)
    ],
)
def test_logging_service_v2_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(
            quota_project_id="octopus",
            scopes=["1", "2"]
        )

        create_channel.assert_called_with(
            "logging.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/cloud-platform.read-only',
                'https://www.googleapis.com/auth/logging.admin',
                'https://www.googleapis.com/auth/logging.read',
                'https://www.googleapis.com/auth/logging.write',
),
            scopes=["1", "2"],
            default_host="logging.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("transport_class", [transports.LoggingServiceV2GrpcTransport, transports.LoggingServiceV2GrpcAsyncIOTransport])
def test_logging_service_v2_grpc_transport_client_cert_source_for_mtls(
    transport_class
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert,
                private_key=expected_key
            )


@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
])
def test_logging_service_v2_host_no_port(transport_name):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='logging.googleapis.com'),
         transport=transport_name,
    )
    assert client.transport._host == (
        'logging.googleapis.com:443'
    )

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
])
def test_logging_service_v2_host_with_port(transport_name):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='logging.googleapis.com:8000'),
        transport=transport_name,
    )
    assert client.transport._host == (
        'logging.googleapis.com:8000'
    )

def test_logging_service_v2_grpc_transport_channel():
    channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.LoggingServiceV2GrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_logging_service_v2_grpc_asyncio_transport_channel():
    channel = aio.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.LoggingServiceV2GrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.LoggingServiceV2GrpcTransport, transports.LoggingServiceV2GrpcAsyncIOTransport])
def test_logging_service_v2_transport_channel_mtls_with_client_cert_source(
    transport_class
):
    with mock.patch("grpc.ssl_channel_credentials", autospec=True) as grpc_ssl_channel_cred:
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, 'default') as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.LoggingServiceV2GrpcTransport, transports.LoggingServiceV2GrpcAsyncIOTransport])
def test_logging_service_v2_transport_channel_mtls_with_adc(
    transport_class
):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_log_path():
    project = "squid"
    log = "clam"
    expected = "projects/{project}/logs/{log}".format(project=project, log=log, )
    actual = LoggingServiceV2Client.log_path(project, log)
    assert expected == actual


def test_parse_log_path():
    expected = {
        "project": "whelk",
        "log": "octopus",
    }
    path = LoggingServiceV2Client.log_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_log_path(path)
    assert expected == actual

def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(billing_account=billing_account, )
    actual = LoggingServiceV2Client.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = LoggingServiceV2Client.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_common_billing_account_path(path)
    assert expected == actual

def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(folder=folder, )
    actual = LoggingServiceV2Client.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = LoggingServiceV2Client.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_common_folder_path(path)
    assert expected == actual

def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(organization=organization, )
    actual = LoggingServiceV2Client.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = LoggingServiceV2Client.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_common_organization_path(path)
    assert expected == actual

def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(project=project, )
    actual = LoggingServiceV2Client.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = LoggingServiceV2Client.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_common_project_path(path)
    assert expected == actual

def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(project=project, location=location, )
    actual = LoggingServiceV2Client.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = LoggingServiceV2Client.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.LoggingServiceV2Transport, '_prep_wrapped_messages') as prep:
        client = LoggingServiceV2Client(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.LoggingServiceV2Transport, '_prep_wrapped_messages') as prep:
        transport_class = LoggingServiceV2Client.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

@pytest.mark.asyncio
async def test_transport_close_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(type(getattr(client.transport, "grpc_channel")), "close") as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_cancel_operation(transport: str = "grpc"):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None
@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc"):
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None

def test_cancel_operation_field_headers():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value =  None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_cancel_operation_from_dict():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()
@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)
@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc"):
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)

def test_get_operation_field_headers():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_get_operation_from_dict():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()
@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)
@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc"):
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)

def test_list_operations_field_headers():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_list_operations_from_dict():
    client = LoggingServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()
@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = LoggingServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = LoggingServiceV2Client(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        with mock.patch.object(type(getattr(client.transport, close_name)), "close") as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()

def test_client_ctx():
    transports = [
        'grpc',
    ]
    for transport in transports:
        client = LoggingServiceV2Client(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()

@pytest.mark.parametrize("client_class,transport_class", [
    (LoggingServiceV2Client, transports.LoggingServiceV2GrpcTransport),
    (LoggingServiceV2AsyncClient, transports.LoggingServiceV2GrpcAsyncIOTransport),
])
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
