# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.logging_v2.services.config_service_v2 import ConfigServiceV2AsyncClient
from google.cloud.logging_v2.services.config_service_v2 import ConfigServiceV2Client
from google.cloud.logging_v2.services.config_service_v2 import pagers
from google.cloud.logging_v2.services.config_service_v2 import transports
from google.cloud.logging_v2.types import logging_config
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
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

    assert ConfigServiceV2Client._get_default_mtls_endpoint(None) is None
    assert ConfigServiceV2Client._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert ConfigServiceV2Client._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert ConfigServiceV2Client._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert ConfigServiceV2Client._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert ConfigServiceV2Client._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class,transport_name", [
    (ConfigServiceV2Client, "grpc"),
    (ConfigServiceV2AsyncClient, "grpc_asyncio"),
])
def test_config_service_v2_client_from_service_account_info(client_class, transport_name):
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
    (transports.ConfigServiceV2GrpcTransport, "grpc"),
    (transports.ConfigServiceV2GrpcAsyncIOTransport, "grpc_asyncio"),
])
def test_config_service_v2_client_service_account_always_use_jwt(transport_class, transport_name):
    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class,transport_name", [
    (ConfigServiceV2Client, "grpc"),
    (ConfigServiceV2AsyncClient, "grpc_asyncio"),
])
def test_config_service_v2_client_from_service_account_file(client_class, transport_name):
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


def test_config_service_v2_client_get_transport_class():
    transport = ConfigServiceV2Client.get_transport_class()
    available_transports = [
        transports.ConfigServiceV2GrpcTransport,
    ]
    assert transport in available_transports

    transport = ConfigServiceV2Client.get_transport_class("grpc")
    assert transport == transports.ConfigServiceV2GrpcTransport


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (ConfigServiceV2Client, transports.ConfigServiceV2GrpcTransport, "grpc"),
    (ConfigServiceV2AsyncClient, transports.ConfigServiceV2GrpcAsyncIOTransport, "grpc_asyncio"),
])
@mock.patch.object(ConfigServiceV2Client, "DEFAULT_ENDPOINT", modify_default_endpoint(ConfigServiceV2Client))
@mock.patch.object(ConfigServiceV2AsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ConfigServiceV2AsyncClient))
def test_config_service_v2_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ConfigServiceV2Client, 'get_transport_class') as gtc:
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ConfigServiceV2Client, 'get_transport_class') as gtc:
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
    (ConfigServiceV2Client, transports.ConfigServiceV2GrpcTransport, "grpc", "true"),
    (ConfigServiceV2AsyncClient, transports.ConfigServiceV2GrpcAsyncIOTransport, "grpc_asyncio", "true"),
    (ConfigServiceV2Client, transports.ConfigServiceV2GrpcTransport, "grpc", "false"),
    (ConfigServiceV2AsyncClient, transports.ConfigServiceV2GrpcAsyncIOTransport, "grpc_asyncio", "false"),
])
@mock.patch.object(ConfigServiceV2Client, "DEFAULT_ENDPOINT", modify_default_endpoint(ConfigServiceV2Client))
@mock.patch.object(ConfigServiceV2AsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ConfigServiceV2AsyncClient))
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_config_service_v2_client_mtls_env_auto(client_class, transport_class, transport_name, use_client_cert_env):
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
    ConfigServiceV2Client, ConfigServiceV2AsyncClient
])
@mock.patch.object(ConfigServiceV2Client, "DEFAULT_ENDPOINT", modify_default_endpoint(ConfigServiceV2Client))
@mock.patch.object(ConfigServiceV2AsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ConfigServiceV2AsyncClient))
def test_config_service_v2_client_get_mtls_endpoint_and_cert_source(client_class):
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
    (ConfigServiceV2Client, transports.ConfigServiceV2GrpcTransport, "grpc"),
    (ConfigServiceV2AsyncClient, transports.ConfigServiceV2GrpcAsyncIOTransport, "grpc_asyncio"),
])
def test_config_service_v2_client_client_options_scopes(client_class, transport_class, transport_name):
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
    (ConfigServiceV2Client, transports.ConfigServiceV2GrpcTransport, "grpc", grpc_helpers),
    (ConfigServiceV2AsyncClient, transports.ConfigServiceV2GrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_config_service_v2_client_client_options_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
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

def test_config_service_v2_client_client_options_from_dict():
    with mock.patch('google.cloud.logging_v2.services.config_service_v2.transports.ConfigServiceV2GrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = ConfigServiceV2Client(
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
    (ConfigServiceV2Client, transports.ConfigServiceV2GrpcTransport, "grpc", grpc_helpers),
    (ConfigServiceV2AsyncClient, transports.ConfigServiceV2GrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_config_service_v2_client_create_channel_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
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
  logging_config.ListBucketsRequest,
  dict,
])
def test_list_buckets(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListBucketsResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_buckets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListBucketsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBucketsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_buckets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__') as call:
        client.list_buckets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListBucketsRequest()

@pytest.mark.asyncio
async def test_list_buckets_async(transport: str = 'grpc_asyncio', request_type=logging_config.ListBucketsRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListBucketsResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_buckets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListBucketsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBucketsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_buckets_async_from_dict():
    await test_list_buckets_async(request_type=dict)


def test_list_buckets_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.ListBucketsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__') as call:
        call.return_value = logging_config.ListBucketsResponse()
        client.list_buckets(request)

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
async def test_list_buckets_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.ListBucketsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListBucketsResponse())
        await client.list_buckets(request)

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


def test_list_buckets_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListBucketsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_buckets(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_buckets_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_buckets(
            logging_config.ListBucketsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_buckets_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListBucketsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListBucketsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_buckets(
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
async def test_list_buckets_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_buckets(
            logging_config.ListBucketsRequest(),
            parent='parent_value',
        )


def test_list_buckets_pager(transport_name: str = "grpc"):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListBucketsResponse(
                buckets=[],
                next_page_token='def',
            ),
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
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
        pager = client.list_buckets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, logging_config.LogBucket)
                   for i in results)
def test_list_buckets_pages(transport_name: str = "grpc"):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListBucketsResponse(
                buckets=[],
                next_page_token='def',
            ),
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_buckets(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_buckets_async_pager():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListBucketsResponse(
                buckets=[],
                next_page_token='def',
            ),
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_buckets(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, logging_config.LogBucket)
                for i in responses)


@pytest.mark.asyncio
async def test_list_buckets_async_pages():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_buckets),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListBucketsResponse(
                buckets=[],
                next_page_token='def',
            ),
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListBucketsResponse(
                buckets=[
                    logging_config.LogBucket(),
                    logging_config.LogBucket(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_buckets(request={})).pages: # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  logging_config.GetBucketRequest,
  dict,
])
def test_get_bucket(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_bucket),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogBucket(
            name='name_value',
            description='description_value',
            retention_days=1512,
            locked=True,
            lifecycle_state=logging_config.LifecycleState.ACTIVE,
        )
        response = client.get_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogBucket)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.retention_days == 1512
    assert response.locked is True
    assert response.lifecycle_state == logging_config.LifecycleState.ACTIVE


def test_get_bucket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_bucket),
            '__call__') as call:
        client.get_bucket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetBucketRequest()

@pytest.mark.asyncio
async def test_get_bucket_async(transport: str = 'grpc_asyncio', request_type=logging_config.GetBucketRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_bucket),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogBucket(
            name='name_value',
            description='description_value',
            retention_days=1512,
            locked=True,
            lifecycle_state=logging_config.LifecycleState.ACTIVE,
        ))
        response = await client.get_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogBucket)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.retention_days == 1512
    assert response.locked is True
    assert response.lifecycle_state == logging_config.LifecycleState.ACTIVE


@pytest.mark.asyncio
async def test_get_bucket_async_from_dict():
    await test_get_bucket_async(request_type=dict)


def test_get_bucket_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.GetBucketRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_bucket),
            '__call__') as call:
        call.return_value = logging_config.LogBucket()
        client.get_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_bucket_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.GetBucketRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_bucket),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogBucket())
        await client.get_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  logging_config.CreateBucketRequest,
  dict,
])
def test_create_bucket(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_bucket),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogBucket(
            name='name_value',
            description='description_value',
            retention_days=1512,
            locked=True,
            lifecycle_state=logging_config.LifecycleState.ACTIVE,
        )
        response = client.create_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogBucket)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.retention_days == 1512
    assert response.locked is True
    assert response.lifecycle_state == logging_config.LifecycleState.ACTIVE


def test_create_bucket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_bucket),
            '__call__') as call:
        client.create_bucket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateBucketRequest()

@pytest.mark.asyncio
async def test_create_bucket_async(transport: str = 'grpc_asyncio', request_type=logging_config.CreateBucketRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_bucket),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogBucket(
            name='name_value',
            description='description_value',
            retention_days=1512,
            locked=True,
            lifecycle_state=logging_config.LifecycleState.ACTIVE,
        ))
        response = await client.create_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogBucket)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.retention_days == 1512
    assert response.locked is True
    assert response.lifecycle_state == logging_config.LifecycleState.ACTIVE


@pytest.mark.asyncio
async def test_create_bucket_async_from_dict():
    await test_create_bucket_async(request_type=dict)


def test_create_bucket_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.CreateBucketRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_bucket),
            '__call__') as call:
        call.return_value = logging_config.LogBucket()
        client.create_bucket(request)

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
async def test_create_bucket_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.CreateBucketRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_bucket),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogBucket())
        await client.create_bucket(request)

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


@pytest.mark.parametrize("request_type", [
  logging_config.UpdateBucketRequest,
  dict,
])
def test_update_bucket(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_bucket),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogBucket(
            name='name_value',
            description='description_value',
            retention_days=1512,
            locked=True,
            lifecycle_state=logging_config.LifecycleState.ACTIVE,
        )
        response = client.update_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogBucket)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.retention_days == 1512
    assert response.locked is True
    assert response.lifecycle_state == logging_config.LifecycleState.ACTIVE


def test_update_bucket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_bucket),
            '__call__') as call:
        client.update_bucket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateBucketRequest()

@pytest.mark.asyncio
async def test_update_bucket_async(transport: str = 'grpc_asyncio', request_type=logging_config.UpdateBucketRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_bucket),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogBucket(
            name='name_value',
            description='description_value',
            retention_days=1512,
            locked=True,
            lifecycle_state=logging_config.LifecycleState.ACTIVE,
        ))
        response = await client.update_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogBucket)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.retention_days == 1512
    assert response.locked is True
    assert response.lifecycle_state == logging_config.LifecycleState.ACTIVE


@pytest.mark.asyncio
async def test_update_bucket_async_from_dict():
    await test_update_bucket_async(request_type=dict)


def test_update_bucket_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UpdateBucketRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_bucket),
            '__call__') as call:
        call.return_value = logging_config.LogBucket()
        client.update_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_bucket_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UpdateBucketRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_bucket),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogBucket())
        await client.update_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  logging_config.DeleteBucketRequest,
  dict,
])
def test_delete_bucket(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_bucket),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteBucketRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_bucket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_bucket),
            '__call__') as call:
        client.delete_bucket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteBucketRequest()

@pytest.mark.asyncio
async def test_delete_bucket_async(transport: str = 'grpc_asyncio', request_type=logging_config.DeleteBucketRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_bucket),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteBucketRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_bucket_async_from_dict():
    await test_delete_bucket_async(request_type=dict)


def test_delete_bucket_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.DeleteBucketRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_bucket),
            '__call__') as call:
        call.return_value = None
        client.delete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_bucket_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.DeleteBucketRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_bucket),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  logging_config.UndeleteBucketRequest,
  dict,
])
def test_undelete_bucket(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undelete_bucket),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.undelete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UndeleteBucketRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_undelete_bucket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undelete_bucket),
            '__call__') as call:
        client.undelete_bucket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UndeleteBucketRequest()

@pytest.mark.asyncio
async def test_undelete_bucket_async(transport: str = 'grpc_asyncio', request_type=logging_config.UndeleteBucketRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undelete_bucket),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.undelete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UndeleteBucketRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_undelete_bucket_async_from_dict():
    await test_undelete_bucket_async(request_type=dict)


def test_undelete_bucket_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UndeleteBucketRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undelete_bucket),
            '__call__') as call:
        call.return_value = None
        client.undelete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_undelete_bucket_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UndeleteBucketRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undelete_bucket),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.undelete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  logging_config.ListViewsRequest,
  dict,
])
def test_list_views(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListViewsResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_views(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListViewsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListViewsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_views_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__') as call:
        client.list_views()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListViewsRequest()

@pytest.mark.asyncio
async def test_list_views_async(transport: str = 'grpc_asyncio', request_type=logging_config.ListViewsRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListViewsResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_views(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListViewsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListViewsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_views_async_from_dict():
    await test_list_views_async(request_type=dict)


def test_list_views_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.ListViewsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__') as call:
        call.return_value = logging_config.ListViewsResponse()
        client.list_views(request)

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
async def test_list_views_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.ListViewsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListViewsResponse())
        await client.list_views(request)

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


def test_list_views_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListViewsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_views(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_views_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_views(
            logging_config.ListViewsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_views_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListViewsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListViewsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_views(
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
async def test_list_views_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_views(
            logging_config.ListViewsRequest(),
            parent='parent_value',
        )


def test_list_views_pager(transport_name: str = "grpc"):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                    logging_config.LogView(),
                    logging_config.LogView(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListViewsResponse(
                views=[],
                next_page_token='def',
            ),
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                    logging_config.LogView(),
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
        pager = client.list_views(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, logging_config.LogView)
                   for i in results)
def test_list_views_pages(transport_name: str = "grpc"):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                    logging_config.LogView(),
                    logging_config.LogView(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListViewsResponse(
                views=[],
                next_page_token='def',
            ),
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                    logging_config.LogView(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_views(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_views_async_pager():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                    logging_config.LogView(),
                    logging_config.LogView(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListViewsResponse(
                views=[],
                next_page_token='def',
            ),
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                    logging_config.LogView(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_views(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, logging_config.LogView)
                for i in responses)


@pytest.mark.asyncio
async def test_list_views_async_pages():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_views),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                    logging_config.LogView(),
                    logging_config.LogView(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListViewsResponse(
                views=[],
                next_page_token='def',
            ),
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListViewsResponse(
                views=[
                    logging_config.LogView(),
                    logging_config.LogView(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_views(request={})).pages: # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  logging_config.GetViewRequest,
  dict,
])
def test_get_view(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_view),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogView(
            name='name_value',
            description='description_value',
            filter='filter_value',
        )
        response = client.get_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogView)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'


def test_get_view_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_view),
            '__call__') as call:
        client.get_view()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetViewRequest()

@pytest.mark.asyncio
async def test_get_view_async(transport: str = 'grpc_asyncio', request_type=logging_config.GetViewRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_view),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogView(
            name='name_value',
            description='description_value',
            filter='filter_value',
        ))
        response = await client.get_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogView)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'


@pytest.mark.asyncio
async def test_get_view_async_from_dict():
    await test_get_view_async(request_type=dict)


def test_get_view_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.GetViewRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_view),
            '__call__') as call:
        call.return_value = logging_config.LogView()
        client.get_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_view_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.GetViewRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_view),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogView())
        await client.get_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  logging_config.CreateViewRequest,
  dict,
])
def test_create_view(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_view),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogView(
            name='name_value',
            description='description_value',
            filter='filter_value',
        )
        response = client.create_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogView)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'


def test_create_view_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_view),
            '__call__') as call:
        client.create_view()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateViewRequest()

@pytest.mark.asyncio
async def test_create_view_async(transport: str = 'grpc_asyncio', request_type=logging_config.CreateViewRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_view),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogView(
            name='name_value',
            description='description_value',
            filter='filter_value',
        ))
        response = await client.create_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogView)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'


@pytest.mark.asyncio
async def test_create_view_async_from_dict():
    await test_create_view_async(request_type=dict)


def test_create_view_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.CreateViewRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_view),
            '__call__') as call:
        call.return_value = logging_config.LogView()
        client.create_view(request)

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
async def test_create_view_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.CreateViewRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_view),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogView())
        await client.create_view(request)

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


@pytest.mark.parametrize("request_type", [
  logging_config.UpdateViewRequest,
  dict,
])
def test_update_view(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_view),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogView(
            name='name_value',
            description='description_value',
            filter='filter_value',
        )
        response = client.update_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogView)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'


def test_update_view_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_view),
            '__call__') as call:
        client.update_view()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateViewRequest()

@pytest.mark.asyncio
async def test_update_view_async(transport: str = 'grpc_asyncio', request_type=logging_config.UpdateViewRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_view),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogView(
            name='name_value',
            description='description_value',
            filter='filter_value',
        ))
        response = await client.update_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogView)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'


@pytest.mark.asyncio
async def test_update_view_async_from_dict():
    await test_update_view_async(request_type=dict)


def test_update_view_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UpdateViewRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_view),
            '__call__') as call:
        call.return_value = logging_config.LogView()
        client.update_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_view_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UpdateViewRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_view),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogView())
        await client.update_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  logging_config.DeleteViewRequest,
  dict,
])
def test_delete_view(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_view),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteViewRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_view_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_view),
            '__call__') as call:
        client.delete_view()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteViewRequest()

@pytest.mark.asyncio
async def test_delete_view_async(transport: str = 'grpc_asyncio', request_type=logging_config.DeleteViewRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_view),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteViewRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_view_async_from_dict():
    await test_delete_view_async(request_type=dict)


def test_delete_view_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.DeleteViewRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_view),
            '__call__') as call:
        call.return_value = None
        client.delete_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_view_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.DeleteViewRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_view),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  logging_config.ListSinksRequest,
  dict,
])
def test_list_sinks(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListSinksResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_sinks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListSinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSinksPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_sinks_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__') as call:
        client.list_sinks()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListSinksRequest()

@pytest.mark.asyncio
async def test_list_sinks_async(transport: str = 'grpc_asyncio', request_type=logging_config.ListSinksRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListSinksResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_sinks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListSinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSinksAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_sinks_async_from_dict():
    await test_list_sinks_async(request_type=dict)


def test_list_sinks_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.ListSinksRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__') as call:
        call.return_value = logging_config.ListSinksResponse()
        client.list_sinks(request)

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
async def test_list_sinks_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.ListSinksRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListSinksResponse())
        await client.list_sinks(request)

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


def test_list_sinks_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListSinksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_sinks(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_sinks_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_sinks(
            logging_config.ListSinksRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_sinks_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListSinksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListSinksResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_sinks(
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
async def test_list_sinks_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_sinks(
            logging_config.ListSinksRequest(),
            parent='parent_value',
        )


def test_list_sinks_pager(transport_name: str = "grpc"):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListSinksResponse(
                sinks=[],
                next_page_token='def',
            ),
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                    logging_config.LogSink(),
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
        pager = client.list_sinks(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, logging_config.LogSink)
                   for i in results)
def test_list_sinks_pages(transport_name: str = "grpc"):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListSinksResponse(
                sinks=[],
                next_page_token='def',
            ),
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_sinks(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_sinks_async_pager():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListSinksResponse(
                sinks=[],
                next_page_token='def',
            ),
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_sinks(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, logging_config.LogSink)
                for i in responses)


@pytest.mark.asyncio
async def test_list_sinks_async_pages():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_sinks),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListSinksResponse(
                sinks=[],
                next_page_token='def',
            ),
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListSinksResponse(
                sinks=[
                    logging_config.LogSink(),
                    logging_config.LogSink(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_sinks(request={})).pages: # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  logging_config.GetSinkRequest,
  dict,
])
def test_get_sink(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogSink(
            name='name_value',
            destination='destination_value',
            filter='filter_value',
            description='description_value',
            disabled=True,
            output_version_format=logging_config.LogSink.VersionFormat.V2,
            writer_identity='writer_identity_value',
            include_children=True,
            bigquery_options=logging_config.BigQueryOptions(use_partitioned_tables=True),
        )
        response = client.get_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetSinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogSink)
    assert response.name == 'name_value'
    assert response.destination == 'destination_value'
    assert response.filter == 'filter_value'
    assert response.description == 'description_value'
    assert response.disabled is True
    assert response.output_version_format == logging_config.LogSink.VersionFormat.V2
    assert response.writer_identity == 'writer_identity_value'
    assert response.include_children is True


def test_get_sink_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_sink),
            '__call__') as call:
        client.get_sink()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetSinkRequest()

@pytest.mark.asyncio
async def test_get_sink_async(transport: str = 'grpc_asyncio', request_type=logging_config.GetSinkRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogSink(
            name='name_value',
            destination='destination_value',
            filter='filter_value',
            description='description_value',
            disabled=True,
            output_version_format=logging_config.LogSink.VersionFormat.V2,
            writer_identity='writer_identity_value',
            include_children=True,
        ))
        response = await client.get_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetSinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogSink)
    assert response.name == 'name_value'
    assert response.destination == 'destination_value'
    assert response.filter == 'filter_value'
    assert response.description == 'description_value'
    assert response.disabled is True
    assert response.output_version_format == logging_config.LogSink.VersionFormat.V2
    assert response.writer_identity == 'writer_identity_value'
    assert response.include_children is True


@pytest.mark.asyncio
async def test_get_sink_async_from_dict():
    await test_get_sink_async(request_type=dict)


def test_get_sink_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.GetSinkRequest()

    request.sink_name = 'sink_name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_sink),
            '__call__') as call:
        call.return_value = logging_config.LogSink()
        client.get_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'sink_name=sink_name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_sink_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.GetSinkRequest()

    request.sink_name = 'sink_name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_sink),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogSink())
        await client.get_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'sink_name=sink_name_value',
    ) in kw['metadata']


def test_get_sink_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogSink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_sink(
            sink_name='sink_name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].sink_name
        mock_val = 'sink_name_value'
        assert arg == mock_val


def test_get_sink_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_sink(
            logging_config.GetSinkRequest(),
            sink_name='sink_name_value',
        )

@pytest.mark.asyncio
async def test_get_sink_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogSink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogSink())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_sink(
            sink_name='sink_name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].sink_name
        mock_val = 'sink_name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_sink_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_sink(
            logging_config.GetSinkRequest(),
            sink_name='sink_name_value',
        )


@pytest.mark.parametrize("request_type", [
  logging_config.CreateSinkRequest,
  dict,
])
def test_create_sink(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogSink(
            name='name_value',
            destination='destination_value',
            filter='filter_value',
            description='description_value',
            disabled=True,
            output_version_format=logging_config.LogSink.VersionFormat.V2,
            writer_identity='writer_identity_value',
            include_children=True,
            bigquery_options=logging_config.BigQueryOptions(use_partitioned_tables=True),
        )
        response = client.create_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateSinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogSink)
    assert response.name == 'name_value'
    assert response.destination == 'destination_value'
    assert response.filter == 'filter_value'
    assert response.description == 'description_value'
    assert response.disabled is True
    assert response.output_version_format == logging_config.LogSink.VersionFormat.V2
    assert response.writer_identity == 'writer_identity_value'
    assert response.include_children is True


def test_create_sink_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_sink),
            '__call__') as call:
        client.create_sink()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateSinkRequest()

@pytest.mark.asyncio
async def test_create_sink_async(transport: str = 'grpc_asyncio', request_type=logging_config.CreateSinkRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogSink(
            name='name_value',
            destination='destination_value',
            filter='filter_value',
            description='description_value',
            disabled=True,
            output_version_format=logging_config.LogSink.VersionFormat.V2,
            writer_identity='writer_identity_value',
            include_children=True,
        ))
        response = await client.create_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateSinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogSink)
    assert response.name == 'name_value'
    assert response.destination == 'destination_value'
    assert response.filter == 'filter_value'
    assert response.description == 'description_value'
    assert response.disabled is True
    assert response.output_version_format == logging_config.LogSink.VersionFormat.V2
    assert response.writer_identity == 'writer_identity_value'
    assert response.include_children is True


@pytest.mark.asyncio
async def test_create_sink_async_from_dict():
    await test_create_sink_async(request_type=dict)


def test_create_sink_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.CreateSinkRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_sink),
            '__call__') as call:
        call.return_value = logging_config.LogSink()
        client.create_sink(request)

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
async def test_create_sink_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.CreateSinkRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_sink),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogSink())
        await client.create_sink(request)

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


def test_create_sink_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogSink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_sink(
            parent='parent_value',
            sink=logging_config.LogSink(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].sink
        mock_val = logging_config.LogSink(name='name_value')
        assert arg == mock_val


def test_create_sink_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_sink(
            logging_config.CreateSinkRequest(),
            parent='parent_value',
            sink=logging_config.LogSink(name='name_value'),
        )

@pytest.mark.asyncio
async def test_create_sink_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogSink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogSink())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_sink(
            parent='parent_value',
            sink=logging_config.LogSink(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].sink
        mock_val = logging_config.LogSink(name='name_value')
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_sink_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_sink(
            logging_config.CreateSinkRequest(),
            parent='parent_value',
            sink=logging_config.LogSink(name='name_value'),
        )


@pytest.mark.parametrize("request_type", [
  logging_config.UpdateSinkRequest,
  dict,
])
def test_update_sink(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogSink(
            name='name_value',
            destination='destination_value',
            filter='filter_value',
            description='description_value',
            disabled=True,
            output_version_format=logging_config.LogSink.VersionFormat.V2,
            writer_identity='writer_identity_value',
            include_children=True,
            bigquery_options=logging_config.BigQueryOptions(use_partitioned_tables=True),
        )
        response = client.update_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateSinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogSink)
    assert response.name == 'name_value'
    assert response.destination == 'destination_value'
    assert response.filter == 'filter_value'
    assert response.description == 'description_value'
    assert response.disabled is True
    assert response.output_version_format == logging_config.LogSink.VersionFormat.V2
    assert response.writer_identity == 'writer_identity_value'
    assert response.include_children is True


def test_update_sink_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_sink),
            '__call__') as call:
        client.update_sink()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateSinkRequest()

@pytest.mark.asyncio
async def test_update_sink_async(transport: str = 'grpc_asyncio', request_type=logging_config.UpdateSinkRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogSink(
            name='name_value',
            destination='destination_value',
            filter='filter_value',
            description='description_value',
            disabled=True,
            output_version_format=logging_config.LogSink.VersionFormat.V2,
            writer_identity='writer_identity_value',
            include_children=True,
        ))
        response = await client.update_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateSinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogSink)
    assert response.name == 'name_value'
    assert response.destination == 'destination_value'
    assert response.filter == 'filter_value'
    assert response.description == 'description_value'
    assert response.disabled is True
    assert response.output_version_format == logging_config.LogSink.VersionFormat.V2
    assert response.writer_identity == 'writer_identity_value'
    assert response.include_children is True


@pytest.mark.asyncio
async def test_update_sink_async_from_dict():
    await test_update_sink_async(request_type=dict)


def test_update_sink_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UpdateSinkRequest()

    request.sink_name = 'sink_name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_sink),
            '__call__') as call:
        call.return_value = logging_config.LogSink()
        client.update_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'sink_name=sink_name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_sink_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UpdateSinkRequest()

    request.sink_name = 'sink_name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_sink),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogSink())
        await client.update_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'sink_name=sink_name_value',
    ) in kw['metadata']


def test_update_sink_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogSink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_sink(
            sink_name='sink_name_value',
            sink=logging_config.LogSink(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].sink_name
        mock_val = 'sink_name_value'
        assert arg == mock_val
        arg = args[0].sink
        mock_val = logging_config.LogSink(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_sink_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_sink(
            logging_config.UpdateSinkRequest(),
            sink_name='sink_name_value',
            sink=logging_config.LogSink(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_sink_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogSink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogSink())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_sink(
            sink_name='sink_name_value',
            sink=logging_config.LogSink(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].sink_name
        mock_val = 'sink_name_value'
        assert arg == mock_val
        arg = args[0].sink
        mock_val = logging_config.LogSink(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_sink_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_sink(
            logging_config.UpdateSinkRequest(),
            sink_name='sink_name_value',
            sink=logging_config.LogSink(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  logging_config.DeleteSinkRequest,
  dict,
])
def test_delete_sink(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteSinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_sink_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_sink),
            '__call__') as call:
        client.delete_sink()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteSinkRequest()

@pytest.mark.asyncio
async def test_delete_sink_async(transport: str = 'grpc_asyncio', request_type=logging_config.DeleteSinkRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteSinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_sink_async_from_dict():
    await test_delete_sink_async(request_type=dict)


def test_delete_sink_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.DeleteSinkRequest()

    request.sink_name = 'sink_name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_sink),
            '__call__') as call:
        call.return_value = None
        client.delete_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'sink_name=sink_name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_sink_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.DeleteSinkRequest()

    request.sink_name = 'sink_name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_sink),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_sink(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'sink_name=sink_name_value',
    ) in kw['metadata']


def test_delete_sink_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_sink(
            sink_name='sink_name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].sink_name
        mock_val = 'sink_name_value'
        assert arg == mock_val


def test_delete_sink_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_sink(
            logging_config.DeleteSinkRequest(),
            sink_name='sink_name_value',
        )

@pytest.mark.asyncio
async def test_delete_sink_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_sink),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_sink(
            sink_name='sink_name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].sink_name
        mock_val = 'sink_name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_sink_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_sink(
            logging_config.DeleteSinkRequest(),
            sink_name='sink_name_value',
        )


@pytest.mark.parametrize("request_type", [
  logging_config.ListExclusionsRequest,
  dict,
])
def test_list_exclusions(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListExclusionsResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_exclusions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListExclusionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListExclusionsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_exclusions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__') as call:
        client.list_exclusions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListExclusionsRequest()

@pytest.mark.asyncio
async def test_list_exclusions_async(transport: str = 'grpc_asyncio', request_type=logging_config.ListExclusionsRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListExclusionsResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_exclusions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.ListExclusionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListExclusionsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_exclusions_async_from_dict():
    await test_list_exclusions_async(request_type=dict)


def test_list_exclusions_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.ListExclusionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__') as call:
        call.return_value = logging_config.ListExclusionsResponse()
        client.list_exclusions(request)

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
async def test_list_exclusions_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.ListExclusionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListExclusionsResponse())
        await client.list_exclusions(request)

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


def test_list_exclusions_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListExclusionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_exclusions(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_exclusions_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_exclusions(
            logging_config.ListExclusionsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_exclusions_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.ListExclusionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.ListExclusionsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_exclusions(
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
async def test_list_exclusions_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_exclusions(
            logging_config.ListExclusionsRequest(),
            parent='parent_value',
        )


def test_list_exclusions_pager(transport_name: str = "grpc"):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[],
                next_page_token='def',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
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
        pager = client.list_exclusions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, logging_config.LogExclusion)
                   for i in results)
def test_list_exclusions_pages(transport_name: str = "grpc"):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[],
                next_page_token='def',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_exclusions(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_exclusions_async_pager():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[],
                next_page_token='def',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_exclusions(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, logging_config.LogExclusion)
                for i in responses)


@pytest.mark.asyncio
async def test_list_exclusions_async_pages():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_exclusions),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                ],
                next_page_token='abc',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[],
                next_page_token='def',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                ],
                next_page_token='ghi',
            ),
            logging_config.ListExclusionsResponse(
                exclusions=[
                    logging_config.LogExclusion(),
                    logging_config.LogExclusion(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_exclusions(request={})).pages: # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  logging_config.GetExclusionRequest,
  dict,
])
def test_get_exclusion(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogExclusion(
            name='name_value',
            description='description_value',
            filter='filter_value',
            disabled=True,
        )
        response = client.get_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetExclusionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogExclusion)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'
    assert response.disabled is True


def test_get_exclusion_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_exclusion),
            '__call__') as call:
        client.get_exclusion()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetExclusionRequest()

@pytest.mark.asyncio
async def test_get_exclusion_async(transport: str = 'grpc_asyncio', request_type=logging_config.GetExclusionRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogExclusion(
            name='name_value',
            description='description_value',
            filter='filter_value',
            disabled=True,
        ))
        response = await client.get_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetExclusionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogExclusion)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'
    assert response.disabled is True


@pytest.mark.asyncio
async def test_get_exclusion_async_from_dict():
    await test_get_exclusion_async(request_type=dict)


def test_get_exclusion_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.GetExclusionRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_exclusion),
            '__call__') as call:
        call.return_value = logging_config.LogExclusion()
        client.get_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_exclusion_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.GetExclusionRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_exclusion),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogExclusion())
        await client.get_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_exclusion_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogExclusion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_exclusion(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_exclusion_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_exclusion(
            logging_config.GetExclusionRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_exclusion_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogExclusion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogExclusion())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_exclusion(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_exclusion_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_exclusion(
            logging_config.GetExclusionRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  logging_config.CreateExclusionRequest,
  dict,
])
def test_create_exclusion(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogExclusion(
            name='name_value',
            description='description_value',
            filter='filter_value',
            disabled=True,
        )
        response = client.create_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateExclusionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogExclusion)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'
    assert response.disabled is True


def test_create_exclusion_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_exclusion),
            '__call__') as call:
        client.create_exclusion()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateExclusionRequest()

@pytest.mark.asyncio
async def test_create_exclusion_async(transport: str = 'grpc_asyncio', request_type=logging_config.CreateExclusionRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogExclusion(
            name='name_value',
            description='description_value',
            filter='filter_value',
            disabled=True,
        ))
        response = await client.create_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.CreateExclusionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogExclusion)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'
    assert response.disabled is True


@pytest.mark.asyncio
async def test_create_exclusion_async_from_dict():
    await test_create_exclusion_async(request_type=dict)


def test_create_exclusion_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.CreateExclusionRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_exclusion),
            '__call__') as call:
        call.return_value = logging_config.LogExclusion()
        client.create_exclusion(request)

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
async def test_create_exclusion_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.CreateExclusionRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_exclusion),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogExclusion())
        await client.create_exclusion(request)

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


def test_create_exclusion_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogExclusion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_exclusion(
            parent='parent_value',
            exclusion=logging_config.LogExclusion(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].exclusion
        mock_val = logging_config.LogExclusion(name='name_value')
        assert arg == mock_val


def test_create_exclusion_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_exclusion(
            logging_config.CreateExclusionRequest(),
            parent='parent_value',
            exclusion=logging_config.LogExclusion(name='name_value'),
        )

@pytest.mark.asyncio
async def test_create_exclusion_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogExclusion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogExclusion())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_exclusion(
            parent='parent_value',
            exclusion=logging_config.LogExclusion(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].exclusion
        mock_val = logging_config.LogExclusion(name='name_value')
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_exclusion_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_exclusion(
            logging_config.CreateExclusionRequest(),
            parent='parent_value',
            exclusion=logging_config.LogExclusion(name='name_value'),
        )


@pytest.mark.parametrize("request_type", [
  logging_config.UpdateExclusionRequest,
  dict,
])
def test_update_exclusion(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogExclusion(
            name='name_value',
            description='description_value',
            filter='filter_value',
            disabled=True,
        )
        response = client.update_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateExclusionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogExclusion)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'
    assert response.disabled is True


def test_update_exclusion_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_exclusion),
            '__call__') as call:
        client.update_exclusion()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateExclusionRequest()

@pytest.mark.asyncio
async def test_update_exclusion_async(transport: str = 'grpc_asyncio', request_type=logging_config.UpdateExclusionRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogExclusion(
            name='name_value',
            description='description_value',
            filter='filter_value',
            disabled=True,
        ))
        response = await client.update_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateExclusionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.LogExclusion)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.filter == 'filter_value'
    assert response.disabled is True


@pytest.mark.asyncio
async def test_update_exclusion_async_from_dict():
    await test_update_exclusion_async(request_type=dict)


def test_update_exclusion_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UpdateExclusionRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_exclusion),
            '__call__') as call:
        call.return_value = logging_config.LogExclusion()
        client.update_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_exclusion_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UpdateExclusionRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_exclusion),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogExclusion())
        await client.update_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_update_exclusion_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogExclusion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_exclusion(
            name='name_value',
            exclusion=logging_config.LogExclusion(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].exclusion
        mock_val = logging_config.LogExclusion(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_exclusion_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_exclusion(
            logging_config.UpdateExclusionRequest(),
            name='name_value',
            exclusion=logging_config.LogExclusion(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_exclusion_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.LogExclusion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.LogExclusion())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_exclusion(
            name='name_value',
            exclusion=logging_config.LogExclusion(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].exclusion
        mock_val = logging_config.LogExclusion(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_exclusion_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_exclusion(
            logging_config.UpdateExclusionRequest(),
            name='name_value',
            exclusion=logging_config.LogExclusion(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  logging_config.DeleteExclusionRequest,
  dict,
])
def test_delete_exclusion(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteExclusionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_exclusion_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_exclusion),
            '__call__') as call:
        client.delete_exclusion()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteExclusionRequest()

@pytest.mark.asyncio
async def test_delete_exclusion_async(transport: str = 'grpc_asyncio', request_type=logging_config.DeleteExclusionRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.DeleteExclusionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_exclusion_async_from_dict():
    await test_delete_exclusion_async(request_type=dict)


def test_delete_exclusion_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.DeleteExclusionRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_exclusion),
            '__call__') as call:
        call.return_value = None
        client.delete_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_exclusion_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.DeleteExclusionRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_exclusion),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_exclusion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_exclusion_flattened():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_exclusion(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_exclusion_flattened_error():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_exclusion(
            logging_config.DeleteExclusionRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_exclusion_flattened_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_exclusion),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_exclusion(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_exclusion_flattened_error_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_exclusion(
            logging_config.DeleteExclusionRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  logging_config.GetCmekSettingsRequest,
  dict,
])
def test_get_cmek_settings(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_cmek_settings),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.CmekSettings(
            name='name_value',
            kms_key_name='kms_key_name_value',
            service_account_id='service_account_id_value',
        )
        response = client.get_cmek_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetCmekSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.CmekSettings)
    assert response.name == 'name_value'
    assert response.kms_key_name == 'kms_key_name_value'
    assert response.service_account_id == 'service_account_id_value'


def test_get_cmek_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_cmek_settings),
            '__call__') as call:
        client.get_cmek_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetCmekSettingsRequest()

@pytest.mark.asyncio
async def test_get_cmek_settings_async(transport: str = 'grpc_asyncio', request_type=logging_config.GetCmekSettingsRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_cmek_settings),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.CmekSettings(
            name='name_value',
            kms_key_name='kms_key_name_value',
            service_account_id='service_account_id_value',
        ))
        response = await client.get_cmek_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.GetCmekSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.CmekSettings)
    assert response.name == 'name_value'
    assert response.kms_key_name == 'kms_key_name_value'
    assert response.service_account_id == 'service_account_id_value'


@pytest.mark.asyncio
async def test_get_cmek_settings_async_from_dict():
    await test_get_cmek_settings_async(request_type=dict)


def test_get_cmek_settings_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.GetCmekSettingsRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_cmek_settings),
            '__call__') as call:
        call.return_value = logging_config.CmekSettings()
        client.get_cmek_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_cmek_settings_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.GetCmekSettingsRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_cmek_settings),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.CmekSettings())
        await client.get_cmek_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  logging_config.UpdateCmekSettingsRequest,
  dict,
])
def test_update_cmek_settings(request_type, transport: str = 'grpc'):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_cmek_settings),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_config.CmekSettings(
            name='name_value',
            kms_key_name='kms_key_name_value',
            service_account_id='service_account_id_value',
        )
        response = client.update_cmek_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateCmekSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.CmekSettings)
    assert response.name == 'name_value'
    assert response.kms_key_name == 'kms_key_name_value'
    assert response.service_account_id == 'service_account_id_value'


def test_update_cmek_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_cmek_settings),
            '__call__') as call:
        client.update_cmek_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateCmekSettingsRequest()

@pytest.mark.asyncio
async def test_update_cmek_settings_async(transport: str = 'grpc_asyncio', request_type=logging_config.UpdateCmekSettingsRequest):
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_cmek_settings),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(logging_config.CmekSettings(
            name='name_value',
            kms_key_name='kms_key_name_value',
            service_account_id='service_account_id_value',
        ))
        response = await client.update_cmek_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == logging_config.UpdateCmekSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_config.CmekSettings)
    assert response.name == 'name_value'
    assert response.kms_key_name == 'kms_key_name_value'
    assert response.service_account_id == 'service_account_id_value'


@pytest.mark.asyncio
async def test_update_cmek_settings_async_from_dict():
    await test_update_cmek_settings_async(request_type=dict)


def test_update_cmek_settings_field_headers():
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UpdateCmekSettingsRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_cmek_settings),
            '__call__') as call:
        call.return_value = logging_config.CmekSettings()
        client.update_cmek_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_cmek_settings_field_headers_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_config.UpdateCmekSettingsRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_cmek_settings),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(logging_config.CmekSettings())
        await client.update_cmek_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ConfigServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ConfigServiceV2Client(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ConfigServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ConfigServiceV2Client(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.ConfigServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ConfigServiceV2Client(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ConfigServiceV2Client(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ConfigServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ConfigServiceV2Client(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ConfigServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ConfigServiceV2Client(transport=transport)
    assert client.transport is transport

def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ConfigServiceV2GrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ConfigServiceV2GrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

@pytest.mark.parametrize("transport_class", [
    transports.ConfigServiceV2GrpcTransport,
    transports.ConfigServiceV2GrpcAsyncIOTransport,
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
    transport = ConfigServiceV2Client.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name

def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.ConfigServiceV2GrpcTransport,
    )

def test_config_service_v2_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ConfigServiceV2Transport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json"
        )


def test_config_service_v2_base_transport():
    # Instantiate the base transport.
    with mock.patch('google.cloud.logging_v2.services.config_service_v2.transports.ConfigServiceV2Transport.__init__') as Transport:
        Transport.return_value = None
        transport = transports.ConfigServiceV2Transport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'list_buckets',
        'get_bucket',
        'create_bucket',
        'update_bucket',
        'delete_bucket',
        'undelete_bucket',
        'list_views',
        'get_view',
        'create_view',
        'update_view',
        'delete_view',
        'list_sinks',
        'get_sink',
        'create_sink',
        'update_sink',
        'delete_sink',
        'list_exclusions',
        'get_exclusion',
        'create_exclusion',
        'update_exclusion',
        'delete_exclusion',
        'get_cmek_settings',
        'update_cmek_settings',
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


def test_config_service_v2_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(google.auth, 'load_credentials_from_file', autospec=True) as load_creds, mock.patch('google.cloud.logging_v2.services.config_service_v2.transports.ConfigServiceV2Transport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ConfigServiceV2Transport(
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
),
            quota_project_id="octopus",
        )


def test_config_service_v2_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc, mock.patch('google.cloud.logging_v2.services.config_service_v2.transports.ConfigServiceV2Transport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ConfigServiceV2Transport()
        adc.assert_called_once()


def test_config_service_v2_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ConfigServiceV2Client()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/cloud-platform.read-only',
            'https://www.googleapis.com/auth/logging.admin',
            'https://www.googleapis.com/auth/logging.read',
),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConfigServiceV2GrpcTransport,
        transports.ConfigServiceV2GrpcAsyncIOTransport,
    ],
)
def test_config_service_v2_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(                'https://www.googleapis.com/auth/cloud-platform',                'https://www.googleapis.com/auth/cloud-platform.read-only',                'https://www.googleapis.com/auth/logging.admin',                'https://www.googleapis.com/auth/logging.read',),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConfigServiceV2GrpcTransport,
        transports.ConfigServiceV2GrpcAsyncIOTransport,
    ],
)
def test_config_service_v2_transport_auth_gdch_credentials(transport_class):
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
        (transports.ConfigServiceV2GrpcTransport, grpc_helpers),
        (transports.ConfigServiceV2GrpcAsyncIOTransport, grpc_helpers_async)
    ],
)
def test_config_service_v2_transport_create_channel(transport_class, grpc_helpers):
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
),
            scopes=["1", "2"],
            default_host="logging.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("transport_class", [transports.ConfigServiceV2GrpcTransport, transports.ConfigServiceV2GrpcAsyncIOTransport])
def test_config_service_v2_grpc_transport_client_cert_source_for_mtls(
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
def test_config_service_v2_host_no_port(transport_name):
    client = ConfigServiceV2Client(
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
def test_config_service_v2_host_with_port(transport_name):
    client = ConfigServiceV2Client(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='logging.googleapis.com:8000'),
        transport=transport_name,
    )
    assert client.transport._host == (
        'logging.googleapis.com:8000'
    )

def test_config_service_v2_grpc_transport_channel():
    channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ConfigServiceV2GrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_config_service_v2_grpc_asyncio_transport_channel():
    channel = aio.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ConfigServiceV2GrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.ConfigServiceV2GrpcTransport, transports.ConfigServiceV2GrpcAsyncIOTransport])
def test_config_service_v2_transport_channel_mtls_with_client_cert_source(
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
@pytest.mark.parametrize("transport_class", [transports.ConfigServiceV2GrpcTransport, transports.ConfigServiceV2GrpcAsyncIOTransport])
def test_config_service_v2_transport_channel_mtls_with_adc(
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


def test_cmek_settings_path():
    project = "squid"
    expected = "projects/{project}/cmekSettings".format(project=project, )
    actual = ConfigServiceV2Client.cmek_settings_path(project)
    assert expected == actual


def test_parse_cmek_settings_path():
    expected = {
        "project": "clam",
    }
    path = ConfigServiceV2Client.cmek_settings_path(**expected)

    # Check that the path construction is reversible.
    actual = ConfigServiceV2Client.parse_cmek_settings_path(path)
    assert expected == actual

def test_log_bucket_path():
    project = "whelk"
    location = "octopus"
    bucket = "oyster"
    expected = "projects/{project}/locations/{location}/buckets/{bucket}".format(project=project, location=location, bucket=bucket, )
    actual = ConfigServiceV2Client.log_bucket_path(project, location, bucket)
    assert expected == actual


def test_parse_log_bucket_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "bucket": "mussel",
    }
    path = ConfigServiceV2Client.log_bucket_path(**expected)

    # Check that the path construction is reversible.
    actual = ConfigServiceV2Client.parse_log_bucket_path(path)
    assert expected == actual

def test_log_exclusion_path():
    project = "winkle"
    exclusion = "nautilus"
    expected = "projects/{project}/exclusions/{exclusion}".format(project=project, exclusion=exclusion, )
    actual = ConfigServiceV2Client.log_exclusion_path(project, exclusion)
    assert expected == actual


def test_parse_log_exclusion_path():
    expected = {
        "project": "scallop",
        "exclusion": "abalone",
    }
    path = ConfigServiceV2Client.log_exclusion_path(**expected)

    # Check that the path construction is reversible.
    actual = ConfigServiceV2Client.parse_log_exclusion_path(path)
    assert expected == actual

def test_log_sink_path():
    project = "squid"
    sink = "clam"
    expected = "projects/{project}/sinks/{sink}".format(project=project, sink=sink, )
    actual = ConfigServiceV2Client.log_sink_path(project, sink)
    assert expected == actual


def test_parse_log_sink_path():
    expected = {
        "project": "whelk",
        "sink": "octopus",
    }
    path = ConfigServiceV2Client.log_sink_path(**expected)

    # Check that the path construction is reversible.
    actual = ConfigServiceV2Client.parse_log_sink_path(path)
    assert expected == actual

def test_log_view_path():
    project = "oyster"
    location = "nudibranch"
    bucket = "cuttlefish"
    view = "mussel"
    expected = "projects/{project}/locations/{location}/buckets/{bucket}/views/{view}".format(project=project, location=location, bucket=bucket, view=view, )
    actual = ConfigServiceV2Client.log_view_path(project, location, bucket, view)
    assert expected == actual


def test_parse_log_view_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "bucket": "scallop",
        "view": "abalone",
    }
    path = ConfigServiceV2Client.log_view_path(**expected)

    # Check that the path construction is reversible.
    actual = ConfigServiceV2Client.parse_log_view_path(path)
    assert expected == actual

def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(billing_account=billing_account, )
    actual = ConfigServiceV2Client.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = ConfigServiceV2Client.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ConfigServiceV2Client.parse_common_billing_account_path(path)
    assert expected == actual

def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder, )
    actual = ConfigServiceV2Client.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = ConfigServiceV2Client.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ConfigServiceV2Client.parse_common_folder_path(path)
    assert expected == actual

def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization, )
    actual = ConfigServiceV2Client.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = ConfigServiceV2Client.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ConfigServiceV2Client.parse_common_organization_path(path)
    assert expected == actual

def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project, )
    actual = ConfigServiceV2Client.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = ConfigServiceV2Client.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ConfigServiceV2Client.parse_common_project_path(path)
    assert expected == actual

def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(project=project, location=location, )
    actual = ConfigServiceV2Client.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = ConfigServiceV2Client.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ConfigServiceV2Client.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.ConfigServiceV2Transport, '_prep_wrapped_messages') as prep:
        client = ConfigServiceV2Client(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.ConfigServiceV2Transport, '_prep_wrapped_messages') as prep:
        transport_class = ConfigServiceV2Client.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

@pytest.mark.asyncio
async def test_transport_close_async():
    client = ConfigServiceV2AsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(type(getattr(client.transport, "grpc_channel")), "close") as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = ConfigServiceV2Client(
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
        client = ConfigServiceV2Client(
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
    (ConfigServiceV2Client, transports.ConfigServiceV2GrpcTransport),
    (ConfigServiceV2AsyncClient, transports.ConfigServiceV2GrpcAsyncIOTransport),
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
