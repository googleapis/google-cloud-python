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
from collections.abc import Iterable
from google.protobuf import json_format
import json
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.asset_v1.services.asset_service import AssetServiceAsyncClient
from google.cloud.asset_v1.services.asset_service import AssetServiceClient
from google.cloud.asset_v1.services.asset_service import pagers
from google.cloud.asset_v1.services.asset_service import transports
from google.cloud.asset_v1.types import asset_service
from google.cloud.asset_v1.types import assets
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
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

    assert AssetServiceClient._get_default_mtls_endpoint(None) is None
    assert AssetServiceClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert AssetServiceClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert AssetServiceClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert AssetServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert AssetServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class,transport_name", [
    (AssetServiceClient, "grpc"),
    (AssetServiceAsyncClient, "grpc_asyncio"),
    (AssetServiceClient, "rest"),
])
def test_asset_service_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_info') as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'cloudasset.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://cloudasset.googleapis.com'
        )


@pytest.mark.parametrize("transport_class,transport_name", [
    (transports.AssetServiceGrpcTransport, "grpc"),
    (transports.AssetServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    (transports.AssetServiceRestTransport, "rest"),
])
def test_asset_service_client_service_account_always_use_jwt(transport_class, transport_name):
    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class,transport_name", [
    (AssetServiceClient, "grpc"),
    (AssetServiceAsyncClient, "grpc_asyncio"),
    (AssetServiceClient, "rest"),
])
def test_asset_service_client_from_service_account_file(client_class, transport_name):
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
            'cloudasset.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://cloudasset.googleapis.com'
        )


def test_asset_service_client_get_transport_class():
    transport = AssetServiceClient.get_transport_class()
    available_transports = [
        transports.AssetServiceGrpcTransport,
        transports.AssetServiceRestTransport,
    ]
    assert transport in available_transports

    transport = AssetServiceClient.get_transport_class("grpc")
    assert transport == transports.AssetServiceGrpcTransport


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (AssetServiceClient, transports.AssetServiceGrpcTransport, "grpc"),
    (AssetServiceAsyncClient, transports.AssetServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    (AssetServiceClient, transports.AssetServiceRestTransport, "rest"),
])
@mock.patch.object(AssetServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AssetServiceClient))
@mock.patch.object(AssetServiceAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AssetServiceAsyncClient))
def test_asset_service_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AssetServiceClient, 'get_transport_class') as gtc:
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AssetServiceClient, 'get_transport_class') as gtc:
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
    (AssetServiceClient, transports.AssetServiceGrpcTransport, "grpc", "true"),
    (AssetServiceAsyncClient, transports.AssetServiceGrpcAsyncIOTransport, "grpc_asyncio", "true"),
    (AssetServiceClient, transports.AssetServiceGrpcTransport, "grpc", "false"),
    (AssetServiceAsyncClient, transports.AssetServiceGrpcAsyncIOTransport, "grpc_asyncio", "false"),
    (AssetServiceClient, transports.AssetServiceRestTransport, "rest", "true"),
    (AssetServiceClient, transports.AssetServiceRestTransport, "rest", "false"),
])
@mock.patch.object(AssetServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AssetServiceClient))
@mock.patch.object(AssetServiceAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AssetServiceAsyncClient))
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_asset_service_client_mtls_env_auto(client_class, transport_class, transport_name, use_client_cert_env):
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
    AssetServiceClient, AssetServiceAsyncClient
])
@mock.patch.object(AssetServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AssetServiceClient))
@mock.patch.object(AssetServiceAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AssetServiceAsyncClient))
def test_asset_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
    (AssetServiceClient, transports.AssetServiceGrpcTransport, "grpc"),
    (AssetServiceAsyncClient, transports.AssetServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    (AssetServiceClient, transports.AssetServiceRestTransport, "rest"),
])
def test_asset_service_client_client_options_scopes(client_class, transport_class, transport_name):
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
    (AssetServiceClient, transports.AssetServiceGrpcTransport, "grpc", grpc_helpers),
    (AssetServiceAsyncClient, transports.AssetServiceGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
    (AssetServiceClient, transports.AssetServiceRestTransport, "rest", None),
])
def test_asset_service_client_client_options_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
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

def test_asset_service_client_client_options_from_dict():
    with mock.patch('google.cloud.asset_v1.services.asset_service.transports.AssetServiceGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = AssetServiceClient(
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
    (AssetServiceClient, transports.AssetServiceGrpcTransport, "grpc", grpc_helpers),
    (AssetServiceAsyncClient, transports.AssetServiceGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_asset_service_client_create_channel_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
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
            "cloudasset.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=None,
            default_host="cloudasset.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("request_type", [
  asset_service.ExportAssetsRequest,
  dict,
])
def test_export_assets(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.export_assets),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.export_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.ExportAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_assets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.export_assets),
            '__call__') as call:
        client.export_assets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.ExportAssetsRequest()

@pytest.mark.asyncio
async def test_export_assets_async(transport: str = 'grpc_asyncio', request_type=asset_service.ExportAssetsRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.export_assets),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.export_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.ExportAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_export_assets_async_from_dict():
    await test_export_assets_async(request_type=dict)


def test_export_assets_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.ExportAssetsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.export_assets),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.export_assets(request)

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
async def test_export_assets_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.ExportAssetsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.export_assets),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.export_assets(request)

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
  asset_service.ListAssetsRequest,
  dict,
])
def test_list_assets(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.ListAssetsResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.ListAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAssetsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_assets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__') as call:
        client.list_assets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.ListAssetsRequest()

@pytest.mark.asyncio
async def test_list_assets_async(transport: str = 'grpc_asyncio', request_type=asset_service.ListAssetsRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(asset_service.ListAssetsResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.ListAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAssetsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_assets_async_from_dict():
    await test_list_assets_async(request_type=dict)


def test_list_assets_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.ListAssetsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__') as call:
        call.return_value = asset_service.ListAssetsResponse()
        client.list_assets(request)

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
async def test_list_assets_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.ListAssetsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.ListAssetsResponse())
        await client.list_assets(request)

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


def test_list_assets_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.ListAssetsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_assets(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_assets_flattened_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_assets(
            asset_service.ListAssetsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_assets_flattened_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.ListAssetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.ListAssetsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_assets(
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
async def test_list_assets_flattened_error_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_assets(
            asset_service.ListAssetsRequest(),
            parent='parent_value',
        )


def test_list_assets_pager(transport_name: str = "grpc"):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                    assets.Asset(),
                    assets.Asset(),
                ],
                next_page_token='abc',
            ),
            asset_service.ListAssetsResponse(
                assets=[],
                next_page_token='def',
            ),
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                ],
                next_page_token='ghi',
            ),
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                    assets.Asset(),
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
        pager = client.list_assets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, assets.Asset)
                   for i in results)
def test_list_assets_pages(transport_name: str = "grpc"):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                    assets.Asset(),
                    assets.Asset(),
                ],
                next_page_token='abc',
            ),
            asset_service.ListAssetsResponse(
                assets=[],
                next_page_token='def',
            ),
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                ],
                next_page_token='ghi',
            ),
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                    assets.Asset(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_assets(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_assets_async_pager():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                    assets.Asset(),
                    assets.Asset(),
                ],
                next_page_token='abc',
            ),
            asset_service.ListAssetsResponse(
                assets=[],
                next_page_token='def',
            ),
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                ],
                next_page_token='ghi',
            ),
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                    assets.Asset(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_assets(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, assets.Asset)
                for i in responses)


@pytest.mark.asyncio
async def test_list_assets_async_pages():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_assets),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                    assets.Asset(),
                    assets.Asset(),
                ],
                next_page_token='abc',
            ),
            asset_service.ListAssetsResponse(
                assets=[],
                next_page_token='def',
            ),
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                ],
                next_page_token='ghi',
            ),
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                    assets.Asset(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_assets(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  asset_service.BatchGetAssetsHistoryRequest,
  dict,
])
def test_batch_get_assets_history(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_get_assets_history),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.BatchGetAssetsHistoryResponse(
        )
        response = client.batch_get_assets_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.BatchGetAssetsHistoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.BatchGetAssetsHistoryResponse)


def test_batch_get_assets_history_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_get_assets_history),
            '__call__') as call:
        client.batch_get_assets_history()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.BatchGetAssetsHistoryRequest()

@pytest.mark.asyncio
async def test_batch_get_assets_history_async(transport: str = 'grpc_asyncio', request_type=asset_service.BatchGetAssetsHistoryRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_get_assets_history),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(asset_service.BatchGetAssetsHistoryResponse(
        ))
        response = await client.batch_get_assets_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.BatchGetAssetsHistoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.BatchGetAssetsHistoryResponse)


@pytest.mark.asyncio
async def test_batch_get_assets_history_async_from_dict():
    await test_batch_get_assets_history_async(request_type=dict)


def test_batch_get_assets_history_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.BatchGetAssetsHistoryRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_get_assets_history),
            '__call__') as call:
        call.return_value = asset_service.BatchGetAssetsHistoryResponse()
        client.batch_get_assets_history(request)

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
async def test_batch_get_assets_history_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.BatchGetAssetsHistoryRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_get_assets_history),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.BatchGetAssetsHistoryResponse())
        await client.batch_get_assets_history(request)

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
  asset_service.CreateFeedRequest,
  dict,
])
def test_create_feed(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed(
            name='name_value',
            asset_names=['asset_names_value'],
            asset_types=['asset_types_value'],
            content_type=asset_service.ContentType.RESOURCE,
        )
        response = client.create_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.CreateFeedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)
    assert response.name == 'name_value'
    assert response.asset_names == ['asset_names_value']
    assert response.asset_types == ['asset_types_value']
    assert response.content_type == asset_service.ContentType.RESOURCE


def test_create_feed_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_feed),
            '__call__') as call:
        client.create_feed()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.CreateFeedRequest()

@pytest.mark.asyncio
async def test_create_feed_async(transport: str = 'grpc_asyncio', request_type=asset_service.CreateFeedRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed(
            name='name_value',
            asset_names=['asset_names_value'],
            asset_types=['asset_types_value'],
            content_type=asset_service.ContentType.RESOURCE,
        ))
        response = await client.create_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.CreateFeedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)
    assert response.name == 'name_value'
    assert response.asset_names == ['asset_names_value']
    assert response.asset_types == ['asset_types_value']
    assert response.content_type == asset_service.ContentType.RESOURCE


@pytest.mark.asyncio
async def test_create_feed_async_from_dict():
    await test_create_feed_async(request_type=dict)


def test_create_feed_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.CreateFeedRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_feed),
            '__call__') as call:
        call.return_value = asset_service.Feed()
        client.create_feed(request)

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
async def test_create_feed_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.CreateFeedRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_feed),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())
        await client.create_feed(request)

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


def test_create_feed_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_feed(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_create_feed_flattened_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_feed(
            asset_service.CreateFeedRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_create_feed_flattened_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_feed(
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
async def test_create_feed_flattened_error_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_feed(
            asset_service.CreateFeedRequest(),
            parent='parent_value',
        )


@pytest.mark.parametrize("request_type", [
  asset_service.GetFeedRequest,
  dict,
])
def test_get_feed(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed(
            name='name_value',
            asset_names=['asset_names_value'],
            asset_types=['asset_types_value'],
            content_type=asset_service.ContentType.RESOURCE,
        )
        response = client.get_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.GetFeedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)
    assert response.name == 'name_value'
    assert response.asset_names == ['asset_names_value']
    assert response.asset_types == ['asset_types_value']
    assert response.content_type == asset_service.ContentType.RESOURCE


def test_get_feed_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_feed),
            '__call__') as call:
        client.get_feed()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.GetFeedRequest()

@pytest.mark.asyncio
async def test_get_feed_async(transport: str = 'grpc_asyncio', request_type=asset_service.GetFeedRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed(
            name='name_value',
            asset_names=['asset_names_value'],
            asset_types=['asset_types_value'],
            content_type=asset_service.ContentType.RESOURCE,
        ))
        response = await client.get_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.GetFeedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)
    assert response.name == 'name_value'
    assert response.asset_names == ['asset_names_value']
    assert response.asset_types == ['asset_types_value']
    assert response.content_type == asset_service.ContentType.RESOURCE


@pytest.mark.asyncio
async def test_get_feed_async_from_dict():
    await test_get_feed_async(request_type=dict)


def test_get_feed_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.GetFeedRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_feed),
            '__call__') as call:
        call.return_value = asset_service.Feed()
        client.get_feed(request)

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
async def test_get_feed_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.GetFeedRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_feed),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())
        await client.get_feed(request)

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


def test_get_feed_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_feed(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_feed_flattened_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_feed(
            asset_service.GetFeedRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_feed_flattened_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_feed(
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
async def test_get_feed_flattened_error_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_feed(
            asset_service.GetFeedRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  asset_service.ListFeedsRequest,
  dict,
])
def test_list_feeds(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_feeds),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.ListFeedsResponse(
        )
        response = client.list_feeds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.ListFeedsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.ListFeedsResponse)


def test_list_feeds_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_feeds),
            '__call__') as call:
        client.list_feeds()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.ListFeedsRequest()

@pytest.mark.asyncio
async def test_list_feeds_async(transport: str = 'grpc_asyncio', request_type=asset_service.ListFeedsRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_feeds),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(asset_service.ListFeedsResponse(
        ))
        response = await client.list_feeds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.ListFeedsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.ListFeedsResponse)


@pytest.mark.asyncio
async def test_list_feeds_async_from_dict():
    await test_list_feeds_async(request_type=dict)


def test_list_feeds_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.ListFeedsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_feeds),
            '__call__') as call:
        call.return_value = asset_service.ListFeedsResponse()
        client.list_feeds(request)

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
async def test_list_feeds_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.ListFeedsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_feeds),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.ListFeedsResponse())
        await client.list_feeds(request)

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


def test_list_feeds_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_feeds),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.ListFeedsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_feeds(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_feeds_flattened_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_feeds(
            asset_service.ListFeedsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_feeds_flattened_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_feeds),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.ListFeedsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.ListFeedsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_feeds(
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
async def test_list_feeds_flattened_error_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_feeds(
            asset_service.ListFeedsRequest(),
            parent='parent_value',
        )


@pytest.mark.parametrize("request_type", [
  asset_service.UpdateFeedRequest,
  dict,
])
def test_update_feed(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed(
            name='name_value',
            asset_names=['asset_names_value'],
            asset_types=['asset_types_value'],
            content_type=asset_service.ContentType.RESOURCE,
        )
        response = client.update_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.UpdateFeedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)
    assert response.name == 'name_value'
    assert response.asset_names == ['asset_names_value']
    assert response.asset_types == ['asset_types_value']
    assert response.content_type == asset_service.ContentType.RESOURCE


def test_update_feed_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_feed),
            '__call__') as call:
        client.update_feed()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.UpdateFeedRequest()

@pytest.mark.asyncio
async def test_update_feed_async(transport: str = 'grpc_asyncio', request_type=asset_service.UpdateFeedRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed(
            name='name_value',
            asset_names=['asset_names_value'],
            asset_types=['asset_types_value'],
            content_type=asset_service.ContentType.RESOURCE,
        ))
        response = await client.update_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.UpdateFeedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)
    assert response.name == 'name_value'
    assert response.asset_names == ['asset_names_value']
    assert response.asset_types == ['asset_types_value']
    assert response.content_type == asset_service.ContentType.RESOURCE


@pytest.mark.asyncio
async def test_update_feed_async_from_dict():
    await test_update_feed_async(request_type=dict)


def test_update_feed_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.UpdateFeedRequest()

    request.feed.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_feed),
            '__call__') as call:
        call.return_value = asset_service.Feed()
        client.update_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'feed.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_feed_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.UpdateFeedRequest()

    request.feed.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_feed),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())
        await client.update_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'feed.name=name_value',
    ) in kw['metadata']


def test_update_feed_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_feed(
            feed=asset_service.Feed(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].feed
        mock_val = asset_service.Feed(name='name_value')
        assert arg == mock_val


def test_update_feed_flattened_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_feed(
            asset_service.UpdateFeedRequest(),
            feed=asset_service.Feed(name='name_value'),
        )

@pytest.mark.asyncio
async def test_update_feed_flattened_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.Feed()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.Feed())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_feed(
            feed=asset_service.Feed(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].feed
        mock_val = asset_service.Feed(name='name_value')
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_feed_flattened_error_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_feed(
            asset_service.UpdateFeedRequest(),
            feed=asset_service.Feed(name='name_value'),
        )


@pytest.mark.parametrize("request_type", [
  asset_service.DeleteFeedRequest,
  dict,
])
def test_delete_feed(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.DeleteFeedRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_feed_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_feed),
            '__call__') as call:
        client.delete_feed()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.DeleteFeedRequest()

@pytest.mark.asyncio
async def test_delete_feed_async(transport: str = 'grpc_asyncio', request_type=asset_service.DeleteFeedRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_feed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.DeleteFeedRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_feed_async_from_dict():
    await test_delete_feed_async(request_type=dict)


def test_delete_feed_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.DeleteFeedRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_feed),
            '__call__') as call:
        call.return_value = None
        client.delete_feed(request)

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
async def test_delete_feed_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.DeleteFeedRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_feed),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_feed(request)

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


def test_delete_feed_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_feed(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_feed_flattened_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_feed(
            asset_service.DeleteFeedRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_feed_flattened_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_feed),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_feed(
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
async def test_delete_feed_flattened_error_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_feed(
            asset_service.DeleteFeedRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  asset_service.SearchAllResourcesRequest,
  dict,
])
def test_search_all_resources(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllResourcesResponse(
            next_page_token='next_page_token_value',
        )
        response = client.search_all_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.SearchAllResourcesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAllResourcesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_search_all_resources_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__') as call:
        client.search_all_resources()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.SearchAllResourcesRequest()

@pytest.mark.asyncio
async def test_search_all_resources_async(transport: str = 'grpc_asyncio', request_type=asset_service.SearchAllResourcesRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(asset_service.SearchAllResourcesResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.search_all_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.SearchAllResourcesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAllResourcesAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_search_all_resources_async_from_dict():
    await test_search_all_resources_async(request_type=dict)


def test_search_all_resources_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.SearchAllResourcesRequest()

    request.scope = 'scope_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__') as call:
        call.return_value = asset_service.SearchAllResourcesResponse()
        client.search_all_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'scope=scope_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_search_all_resources_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.SearchAllResourcesRequest()

    request.scope = 'scope_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.SearchAllResourcesResponse())
        await client.search_all_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'scope=scope_value',
    ) in kw['metadata']


def test_search_all_resources_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllResourcesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_all_resources(
            scope='scope_value',
            query='query_value',
            asset_types=['asset_types_value'],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].scope
        mock_val = 'scope_value'
        assert arg == mock_val
        arg = args[0].query
        mock_val = 'query_value'
        assert arg == mock_val
        arg = args[0].asset_types
        mock_val = ['asset_types_value']
        assert arg == mock_val


def test_search_all_resources_flattened_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_all_resources(
            asset_service.SearchAllResourcesRequest(),
            scope='scope_value',
            query='query_value',
            asset_types=['asset_types_value'],
        )

@pytest.mark.asyncio
async def test_search_all_resources_flattened_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllResourcesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.SearchAllResourcesResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_all_resources(
            scope='scope_value',
            query='query_value',
            asset_types=['asset_types_value'],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].scope
        mock_val = 'scope_value'
        assert arg == mock_val
        arg = args[0].query
        mock_val = 'query_value'
        assert arg == mock_val
        arg = args[0].asset_types
        mock_val = ['asset_types_value']
        assert arg == mock_val

@pytest.mark.asyncio
async def test_search_all_resources_flattened_error_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_all_resources(
            asset_service.SearchAllResourcesRequest(),
            scope='scope_value',
            query='query_value',
            asset_types=['asset_types_value'],
        )


def test_search_all_resources_pager(transport_name: str = "grpc"):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
                next_page_token='abc',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[],
                next_page_token='def',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                ],
                next_page_token='ghi',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('scope', ''),
            )),
        )
        pager = client.search_all_resources(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, assets.ResourceSearchResult)
                   for i in results)
def test_search_all_resources_pages(transport_name: str = "grpc"):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
                next_page_token='abc',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[],
                next_page_token='def',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                ],
                next_page_token='ghi',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_all_resources(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_search_all_resources_async_pager():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
                next_page_token='abc',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[],
                next_page_token='def',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                ],
                next_page_token='ghi',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_all_resources(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, assets.ResourceSearchResult)
                for i in responses)


@pytest.mark.asyncio
async def test_search_all_resources_async_pages():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_resources),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
                next_page_token='abc',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[],
                next_page_token='def',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                ],
                next_page_token='ghi',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.search_all_resources(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  asset_service.SearchAllIamPoliciesRequest,
  dict,
])
def test_search_all_iam_policies(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllIamPoliciesResponse(
            next_page_token='next_page_token_value',
        )
        response = client.search_all_iam_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.SearchAllIamPoliciesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAllIamPoliciesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_search_all_iam_policies_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__') as call:
        client.search_all_iam_policies()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.SearchAllIamPoliciesRequest()

@pytest.mark.asyncio
async def test_search_all_iam_policies_async(transport: str = 'grpc_asyncio', request_type=asset_service.SearchAllIamPoliciesRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(asset_service.SearchAllIamPoliciesResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.search_all_iam_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.SearchAllIamPoliciesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAllIamPoliciesAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_search_all_iam_policies_async_from_dict():
    await test_search_all_iam_policies_async(request_type=dict)


def test_search_all_iam_policies_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.SearchAllIamPoliciesRequest()

    request.scope = 'scope_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__') as call:
        call.return_value = asset_service.SearchAllIamPoliciesResponse()
        client.search_all_iam_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'scope=scope_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_search_all_iam_policies_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.SearchAllIamPoliciesRequest()

    request.scope = 'scope_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.SearchAllIamPoliciesResponse())
        await client.search_all_iam_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'scope=scope_value',
    ) in kw['metadata']


def test_search_all_iam_policies_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllIamPoliciesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_all_iam_policies(
            scope='scope_value',
            query='query_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].scope
        mock_val = 'scope_value'
        assert arg == mock_val
        arg = args[0].query
        mock_val = 'query_value'
        assert arg == mock_val


def test_search_all_iam_policies_flattened_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_all_iam_policies(
            asset_service.SearchAllIamPoliciesRequest(),
            scope='scope_value',
            query='query_value',
        )

@pytest.mark.asyncio
async def test_search_all_iam_policies_flattened_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.SearchAllIamPoliciesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.SearchAllIamPoliciesResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_all_iam_policies(
            scope='scope_value',
            query='query_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].scope
        mock_val = 'scope_value'
        assert arg == mock_val
        arg = args[0].query
        mock_val = 'query_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_search_all_iam_policies_flattened_error_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_all_iam_policies(
            asset_service.SearchAllIamPoliciesRequest(),
            scope='scope_value',
            query='query_value',
        )


def test_search_all_iam_policies_pager(transport_name: str = "grpc"):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
                next_page_token='abc',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[],
                next_page_token='def',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                ],
                next_page_token='ghi',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('scope', ''),
            )),
        )
        pager = client.search_all_iam_policies(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, assets.IamPolicySearchResult)
                   for i in results)
def test_search_all_iam_policies_pages(transport_name: str = "grpc"):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
                next_page_token='abc',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[],
                next_page_token='def',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                ],
                next_page_token='ghi',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_all_iam_policies(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_search_all_iam_policies_async_pager():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
                next_page_token='abc',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[],
                next_page_token='def',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                ],
                next_page_token='ghi',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_all_iam_policies(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, assets.IamPolicySearchResult)
                for i in responses)


@pytest.mark.asyncio
async def test_search_all_iam_policies_async_pages():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.search_all_iam_policies),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
                next_page_token='abc',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[],
                next_page_token='def',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                ],
                next_page_token='ghi',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.search_all_iam_policies(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  asset_service.AnalyzeIamPolicyRequest,
  dict,
])
def test_analyze_iam_policy(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.analyze_iam_policy),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = asset_service.AnalyzeIamPolicyResponse(
            fully_explored=True,
        )
        response = client.analyze_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.AnalyzeIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.AnalyzeIamPolicyResponse)
    assert response.fully_explored is True


def test_analyze_iam_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.analyze_iam_policy),
            '__call__') as call:
        client.analyze_iam_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.AnalyzeIamPolicyRequest()

@pytest.mark.asyncio
async def test_analyze_iam_policy_async(transport: str = 'grpc_asyncio', request_type=asset_service.AnalyzeIamPolicyRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.analyze_iam_policy),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(asset_service.AnalyzeIamPolicyResponse(
            fully_explored=True,
        ))
        response = await client.analyze_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.AnalyzeIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.AnalyzeIamPolicyResponse)
    assert response.fully_explored is True


@pytest.mark.asyncio
async def test_analyze_iam_policy_async_from_dict():
    await test_analyze_iam_policy_async(request_type=dict)


def test_analyze_iam_policy_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.AnalyzeIamPolicyRequest()

    request.analysis_query.scope = 'scope_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.analyze_iam_policy),
            '__call__') as call:
        call.return_value = asset_service.AnalyzeIamPolicyResponse()
        client.analyze_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'analysis_query.scope=scope_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_analyze_iam_policy_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.AnalyzeIamPolicyRequest()

    request.analysis_query.scope = 'scope_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.analyze_iam_policy),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(asset_service.AnalyzeIamPolicyResponse())
        await client.analyze_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'analysis_query.scope=scope_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  asset_service.AnalyzeIamPolicyLongrunningRequest,
  dict,
])
def test_analyze_iam_policy_longrunning(request_type, transport: str = 'grpc'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.analyze_iam_policy_longrunning),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.analyze_iam_policy_longrunning(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.AnalyzeIamPolicyLongrunningRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_analyze_iam_policy_longrunning_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.analyze_iam_policy_longrunning),
            '__call__') as call:
        client.analyze_iam_policy_longrunning()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.AnalyzeIamPolicyLongrunningRequest()

@pytest.mark.asyncio
async def test_analyze_iam_policy_longrunning_async(transport: str = 'grpc_asyncio', request_type=asset_service.AnalyzeIamPolicyLongrunningRequest):
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.analyze_iam_policy_longrunning),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.analyze_iam_policy_longrunning(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == asset_service.AnalyzeIamPolicyLongrunningRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_analyze_iam_policy_longrunning_async_from_dict():
    await test_analyze_iam_policy_longrunning_async(request_type=dict)


def test_analyze_iam_policy_longrunning_field_headers():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.AnalyzeIamPolicyLongrunningRequest()

    request.analysis_query.scope = 'scope_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.analyze_iam_policy_longrunning),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.analyze_iam_policy_longrunning(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'analysis_query.scope=scope_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_analyze_iam_policy_longrunning_field_headers_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = asset_service.AnalyzeIamPolicyLongrunningRequest()

    request.analysis_query.scope = 'scope_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.analyze_iam_policy_longrunning),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.analyze_iam_policy_longrunning(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'analysis_query.scope=scope_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
    asset_service.ExportAssetsRequest,
    dict,
])
def test_export_assets_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.export_assets(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_export_assets_rest_required_fields(request_type=asset_service.ExportAssetsRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).export_assets._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).export_assets._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.export_assets(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_export_assets_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.export_assets._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent", "outputConfig", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_export_assets_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_export_assets") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_export_assets") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.ExportAssetsRequest.pb(asset_service.ExportAssetsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = asset_service.ExportAssetsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.export_assets(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_export_assets_rest_bad_request(transport: str = 'rest', request_type=asset_service.ExportAssetsRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.export_assets(request)


def test_export_assets_rest_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    asset_service.ListAssetsRequest,
    dict,
])
def test_list_assets_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.ListAssetsResponse(
              next_page_token='next_page_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.ListAssetsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_assets(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAssetsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_assets_rest_required_fields(request_type=asset_service.ListAssetsRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_assets._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_assets._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("asset_types", "content_type", "page_size", "page_token", "read_time", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = asset_service.ListAssetsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = asset_service.ListAssetsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_assets(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_assets_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_assets._get_unset_required_fields({})
    assert set(unset_fields) == (set(("assetTypes", "contentType", "pageSize", "pageToken", "readTime", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_assets_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_list_assets") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_list_assets") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.ListAssetsRequest.pb(asset_service.ListAssetsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = asset_service.ListAssetsResponse.to_json(asset_service.ListAssetsResponse())

        request = asset_service.ListAssetsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = asset_service.ListAssetsResponse()

        client.list_assets(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_assets_rest_bad_request(transport: str = 'rest', request_type=asset_service.ListAssetsRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_assets(request)


def test_list_assets_rest_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.ListAssetsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'sample1/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.ListAssetsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_assets(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=*/*}/assets" % client.transport._host, args[1])


def test_list_assets_rest_flattened_error(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_assets(
            asset_service.ListAssetsRequest(),
            parent='parent_value',
        )


def test_list_assets_rest_pager(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                    assets.Asset(),
                    assets.Asset(),
                ],
                next_page_token='abc',
            ),
            asset_service.ListAssetsResponse(
                assets=[],
                next_page_token='def',
            ),
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                ],
                next_page_token='ghi',
            ),
            asset_service.ListAssetsResponse(
                assets=[
                    assets.Asset(),
                    assets.Asset(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(asset_service.ListAssetsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'sample1/sample2'}

        pager = client.list_assets(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, assets.Asset)
                for i in results)

        pages = list(client.list_assets(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    asset_service.BatchGetAssetsHistoryRequest,
    dict,
])
def test_batch_get_assets_history_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.BatchGetAssetsHistoryResponse(
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.BatchGetAssetsHistoryResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.batch_get_assets_history(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.BatchGetAssetsHistoryResponse)


def test_batch_get_assets_history_rest_required_fields(request_type=asset_service.BatchGetAssetsHistoryRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_get_assets_history._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_get_assets_history._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("asset_names", "content_type", "read_time_window", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = asset_service.BatchGetAssetsHistoryResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = asset_service.BatchGetAssetsHistoryResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.batch_get_assets_history(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_batch_get_assets_history_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.batch_get_assets_history._get_unset_required_fields({})
    assert set(unset_fields) == (set(("assetNames", "contentType", "readTimeWindow", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_get_assets_history_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_batch_get_assets_history") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_batch_get_assets_history") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.BatchGetAssetsHistoryRequest.pb(asset_service.BatchGetAssetsHistoryRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = asset_service.BatchGetAssetsHistoryResponse.to_json(asset_service.BatchGetAssetsHistoryResponse())

        request = asset_service.BatchGetAssetsHistoryRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = asset_service.BatchGetAssetsHistoryResponse()

        client.batch_get_assets_history(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_get_assets_history_rest_bad_request(transport: str = 'rest', request_type=asset_service.BatchGetAssetsHistoryRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_get_assets_history(request)


def test_batch_get_assets_history_rest_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    asset_service.CreateFeedRequest,
    dict,
])
def test_create_feed_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.Feed(
              name='name_value',
              asset_names=['asset_names_value'],
              asset_types=['asset_types_value'],
              content_type=asset_service.ContentType.RESOURCE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.Feed.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_feed(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)
    assert response.name == 'name_value'
    assert response.asset_names == ['asset_names_value']
    assert response.asset_types == ['asset_types_value']
    assert response.content_type == asset_service.ContentType.RESOURCE


def test_create_feed_rest_required_fields(request_type=asset_service.CreateFeedRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["feed_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_feed._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["feedId"] = 'feed_id_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_feed._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "feedId" in jsonified_request
    assert jsonified_request["feedId"] == 'feed_id_value'

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = asset_service.Feed()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = asset_service.Feed.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_feed(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_feed_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_feed._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent", "feedId", "feed", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_feed_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_create_feed") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_create_feed") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.CreateFeedRequest.pb(asset_service.CreateFeedRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = asset_service.Feed.to_json(asset_service.Feed())

        request = asset_service.CreateFeedRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = asset_service.Feed()

        client.create_feed(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_feed_rest_bad_request(transport: str = 'rest', request_type=asset_service.CreateFeedRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_feed(request)


def test_create_feed_rest_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.Feed()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'sample1/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.Feed.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_feed(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=*/*}/feeds" % client.transport._host, args[1])


def test_create_feed_rest_flattened_error(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_feed(
            asset_service.CreateFeedRequest(),
            parent='parent_value',
        )


def test_create_feed_rest_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    asset_service.GetFeedRequest,
    dict,
])
def test_get_feed_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'sample1/sample2/feeds/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.Feed(
              name='name_value',
              asset_names=['asset_names_value'],
              asset_types=['asset_types_value'],
              content_type=asset_service.ContentType.RESOURCE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.Feed.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_feed(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)
    assert response.name == 'name_value'
    assert response.asset_names == ['asset_names_value']
    assert response.asset_types == ['asset_types_value']
    assert response.content_type == asset_service.ContentType.RESOURCE


def test_get_feed_rest_required_fields(request_type=asset_service.GetFeedRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_feed._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_feed._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = asset_service.Feed()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = asset_service.Feed.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_feed(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_feed_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_feed._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_feed_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_get_feed") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_get_feed") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.GetFeedRequest.pb(asset_service.GetFeedRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = asset_service.Feed.to_json(asset_service.Feed())

        request = asset_service.GetFeedRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = asset_service.Feed()

        client.get_feed(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_feed_rest_bad_request(transport: str = 'rest', request_type=asset_service.GetFeedRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'sample1/sample2/feeds/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_feed(request)


def test_get_feed_rest_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.Feed()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'sample1/sample2/feeds/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.Feed.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_feed(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=*/*/feeds/*}" % client.transport._host, args[1])


def test_get_feed_rest_flattened_error(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_feed(
            asset_service.GetFeedRequest(),
            name='name_value',
        )


def test_get_feed_rest_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    asset_service.ListFeedsRequest,
    dict,
])
def test_list_feeds_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.ListFeedsResponse(
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.ListFeedsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_feeds(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.ListFeedsResponse)


def test_list_feeds_rest_required_fields(request_type=asset_service.ListFeedsRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_feeds._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_feeds._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = asset_service.ListFeedsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = asset_service.ListFeedsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_feeds(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_feeds_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_feeds._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_feeds_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_list_feeds") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_list_feeds") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.ListFeedsRequest.pb(asset_service.ListFeedsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = asset_service.ListFeedsResponse.to_json(asset_service.ListFeedsResponse())

        request = asset_service.ListFeedsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = asset_service.ListFeedsResponse()

        client.list_feeds(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_feeds_rest_bad_request(transport: str = 'rest', request_type=asset_service.ListFeedsRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_feeds(request)


def test_list_feeds_rest_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.ListFeedsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'sample1/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.ListFeedsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_feeds(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=*/*}/feeds" % client.transport._host, args[1])


def test_list_feeds_rest_flattened_error(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_feeds(
            asset_service.ListFeedsRequest(),
            parent='parent_value',
        )


def test_list_feeds_rest_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    asset_service.UpdateFeedRequest,
    dict,
])
def test_update_feed_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'feed': {'name': 'sample1/sample2/feeds/sample3'}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.Feed(
              name='name_value',
              asset_names=['asset_names_value'],
              asset_types=['asset_types_value'],
              content_type=asset_service.ContentType.RESOURCE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.Feed.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_feed(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.Feed)
    assert response.name == 'name_value'
    assert response.asset_names == ['asset_names_value']
    assert response.asset_types == ['asset_types_value']
    assert response.content_type == asset_service.ContentType.RESOURCE


def test_update_feed_rest_required_fields(request_type=asset_service.UpdateFeedRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_feed._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_feed._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = asset_service.Feed()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = asset_service.Feed.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_feed(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_feed_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_feed._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("feed", "updateMask", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_feed_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_update_feed") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_update_feed") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.UpdateFeedRequest.pb(asset_service.UpdateFeedRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = asset_service.Feed.to_json(asset_service.Feed())

        request = asset_service.UpdateFeedRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = asset_service.Feed()

        client.update_feed(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_feed_rest_bad_request(transport: str = 'rest', request_type=asset_service.UpdateFeedRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'feed': {'name': 'sample1/sample2/feeds/sample3'}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_feed(request)


def test_update_feed_rest_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.Feed()

        # get arguments that satisfy an http rule for this method
        sample_request = {'feed': {'name': 'sample1/sample2/feeds/sample3'}}

        # get truthy value for each flattened field
        mock_args = dict(
            feed=asset_service.Feed(name='name_value'),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.Feed.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_feed(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{feed.name=*/*/feeds/*}" % client.transport._host, args[1])


def test_update_feed_rest_flattened_error(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_feed(
            asset_service.UpdateFeedRequest(),
            feed=asset_service.Feed(name='name_value'),
        )


def test_update_feed_rest_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    asset_service.DeleteFeedRequest,
    dict,
])
def test_delete_feed_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'sample1/sample2/feeds/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ''

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_feed(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_feed_rest_required_fields(request_type=asset_service.DeleteFeedRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_feed._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_feed._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ''

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_feed(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_feed_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_feed._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_feed_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_delete_feed") as pre:
        pre.assert_not_called()
        pb_message = asset_service.DeleteFeedRequest.pb(asset_service.DeleteFeedRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = asset_service.DeleteFeedRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_feed(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()


def test_delete_feed_rest_bad_request(transport: str = 'rest', request_type=asset_service.DeleteFeedRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'sample1/sample2/feeds/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_feed(request)


def test_delete_feed_rest_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'sample1/sample2/feeds/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ''
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_feed(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=*/*/feeds/*}" % client.transport._host, args[1])


def test_delete_feed_rest_flattened_error(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_feed(
            asset_service.DeleteFeedRequest(),
            name='name_value',
        )


def test_delete_feed_rest_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    asset_service.SearchAllResourcesRequest,
    dict,
])
def test_search_all_resources_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'scope': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.SearchAllResourcesResponse(
              next_page_token='next_page_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.SearchAllResourcesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.search_all_resources(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAllResourcesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_search_all_resources_rest_required_fields(request_type=asset_service.SearchAllResourcesRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request_init["scope"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).search_all_resources._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["scope"] = 'scope_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).search_all_resources._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("asset_types", "order_by", "page_size", "page_token", "query", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "scope" in jsonified_request
    assert jsonified_request["scope"] == 'scope_value'

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = asset_service.SearchAllResourcesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = asset_service.SearchAllResourcesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.search_all_resources(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_search_all_resources_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.search_all_resources._get_unset_required_fields({})
    assert set(unset_fields) == (set(("assetTypes", "orderBy", "pageSize", "pageToken", "query", )) & set(("scope", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_search_all_resources_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_search_all_resources") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_search_all_resources") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.SearchAllResourcesRequest.pb(asset_service.SearchAllResourcesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = asset_service.SearchAllResourcesResponse.to_json(asset_service.SearchAllResourcesResponse())

        request = asset_service.SearchAllResourcesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = asset_service.SearchAllResourcesResponse()

        client.search_all_resources(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_search_all_resources_rest_bad_request(transport: str = 'rest', request_type=asset_service.SearchAllResourcesRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'scope': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.search_all_resources(request)


def test_search_all_resources_rest_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.SearchAllResourcesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'scope': 'sample1/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            scope='scope_value',
            query='query_value',
            asset_types=['asset_types_value'],
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.SearchAllResourcesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.search_all_resources(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{scope=*/*}:searchAllResources" % client.transport._host, args[1])


def test_search_all_resources_rest_flattened_error(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_all_resources(
            asset_service.SearchAllResourcesRequest(),
            scope='scope_value',
            query='query_value',
            asset_types=['asset_types_value'],
        )


def test_search_all_resources_rest_pager(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
                next_page_token='abc',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[],
                next_page_token='def',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                ],
                next_page_token='ghi',
            ),
            asset_service.SearchAllResourcesResponse(
                results=[
                    assets.ResourceSearchResult(),
                    assets.ResourceSearchResult(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(asset_service.SearchAllResourcesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'scope': 'sample1/sample2'}

        pager = client.search_all_resources(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, assets.ResourceSearchResult)
                for i in results)

        pages = list(client.search_all_resources(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    asset_service.SearchAllIamPoliciesRequest,
    dict,
])
def test_search_all_iam_policies_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'scope': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.SearchAllIamPoliciesResponse(
              next_page_token='next_page_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.SearchAllIamPoliciesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.search_all_iam_policies(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAllIamPoliciesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_search_all_iam_policies_rest_required_fields(request_type=asset_service.SearchAllIamPoliciesRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request_init["scope"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).search_all_iam_policies._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["scope"] = 'scope_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).search_all_iam_policies._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("asset_types", "order_by", "page_size", "page_token", "query", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "scope" in jsonified_request
    assert jsonified_request["scope"] == 'scope_value'

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = asset_service.SearchAllIamPoliciesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = asset_service.SearchAllIamPoliciesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.search_all_iam_policies(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_search_all_iam_policies_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.search_all_iam_policies._get_unset_required_fields({})
    assert set(unset_fields) == (set(("assetTypes", "orderBy", "pageSize", "pageToken", "query", )) & set(("scope", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_search_all_iam_policies_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_search_all_iam_policies") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_search_all_iam_policies") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.SearchAllIamPoliciesRequest.pb(asset_service.SearchAllIamPoliciesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = asset_service.SearchAllIamPoliciesResponse.to_json(asset_service.SearchAllIamPoliciesResponse())

        request = asset_service.SearchAllIamPoliciesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = asset_service.SearchAllIamPoliciesResponse()

        client.search_all_iam_policies(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_search_all_iam_policies_rest_bad_request(transport: str = 'rest', request_type=asset_service.SearchAllIamPoliciesRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'scope': 'sample1/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.search_all_iam_policies(request)


def test_search_all_iam_policies_rest_flattened():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.SearchAllIamPoliciesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'scope': 'sample1/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            scope='scope_value',
            query='query_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.SearchAllIamPoliciesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.search_all_iam_policies(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{scope=*/*}:searchAllIamPolicies" % client.transport._host, args[1])


def test_search_all_iam_policies_rest_flattened_error(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_all_iam_policies(
            asset_service.SearchAllIamPoliciesRequest(),
            scope='scope_value',
            query='query_value',
        )


def test_search_all_iam_policies_rest_pager(transport: str = 'rest'):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
                next_page_token='abc',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[],
                next_page_token='def',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                ],
                next_page_token='ghi',
            ),
            asset_service.SearchAllIamPoliciesResponse(
                results=[
                    assets.IamPolicySearchResult(),
                    assets.IamPolicySearchResult(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(asset_service.SearchAllIamPoliciesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'scope': 'sample1/sample2'}

        pager = client.search_all_iam_policies(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, assets.IamPolicySearchResult)
                for i in results)

        pages = list(client.search_all_iam_policies(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    asset_service.AnalyzeIamPolicyRequest,
    dict,
])
def test_analyze_iam_policy_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'analysis_query': {'scope': 'sample1/sample2'}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = asset_service.AnalyzeIamPolicyResponse(
              fully_explored=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = asset_service.AnalyzeIamPolicyResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.analyze_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, asset_service.AnalyzeIamPolicyResponse)
    assert response.fully_explored is True


def test_analyze_iam_policy_rest_required_fields(request_type=asset_service.AnalyzeIamPolicyRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).analyze_iam_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).analyze_iam_policy._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("analysis_query", "execution_timeout", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = asset_service.AnalyzeIamPolicyResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = asset_service.AnalyzeIamPolicyResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.analyze_iam_policy(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_analyze_iam_policy_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.analyze_iam_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(("analysisQuery", "executionTimeout", )) & set(("analysisQuery", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_analyze_iam_policy_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_analyze_iam_policy") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_analyze_iam_policy") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.AnalyzeIamPolicyRequest.pb(asset_service.AnalyzeIamPolicyRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = asset_service.AnalyzeIamPolicyResponse.to_json(asset_service.AnalyzeIamPolicyResponse())

        request = asset_service.AnalyzeIamPolicyRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = asset_service.AnalyzeIamPolicyResponse()

        client.analyze_iam_policy(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_analyze_iam_policy_rest_bad_request(transport: str = 'rest', request_type=asset_service.AnalyzeIamPolicyRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'analysis_query': {'scope': 'sample1/sample2'}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.analyze_iam_policy(request)


def test_analyze_iam_policy_rest_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    asset_service.AnalyzeIamPolicyLongrunningRequest,
    dict,
])
def test_analyze_iam_policy_longrunning_rest(request_type):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'analysis_query': {'scope': 'sample1/sample2'}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.analyze_iam_policy_longrunning(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_analyze_iam_policy_longrunning_rest_required_fields(request_type=asset_service.AnalyzeIamPolicyLongrunningRequest):
    transport_class = transports.AssetServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).analyze_iam_policy_longrunning._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).analyze_iam_policy_longrunning._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.analyze_iam_policy_longrunning(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_analyze_iam_policy_longrunning_rest_unset_required_fields():
    transport = transports.AssetServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.analyze_iam_policy_longrunning._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("analysisQuery", "outputConfig", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_analyze_iam_policy_longrunning_rest_interceptors(null_interceptor):
    transport = transports.AssetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AssetServiceRestInterceptor(),
        )
    client = AssetServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AssetServiceRestInterceptor, "post_analyze_iam_policy_longrunning") as post, \
         mock.patch.object(transports.AssetServiceRestInterceptor, "pre_analyze_iam_policy_longrunning") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = asset_service.AnalyzeIamPolicyLongrunningRequest.pb(asset_service.AnalyzeIamPolicyLongrunningRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = asset_service.AnalyzeIamPolicyLongrunningRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.analyze_iam_policy_longrunning(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_analyze_iam_policy_longrunning_rest_bad_request(transport: str = 'rest', request_type=asset_service.AnalyzeIamPolicyLongrunningRequest):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'analysis_query': {'scope': 'sample1/sample2'}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.analyze_iam_policy_longrunning(request)


def test_analyze_iam_policy_longrunning_rest_error():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AssetServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AssetServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AssetServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AssetServiceClient(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AssetServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AssetServiceClient(transport=transport)
    assert client.transport is transport

def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AssetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AssetServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

@pytest.mark.parametrize("transport_class", [
    transports.AssetServiceGrpcTransport,
    transports.AssetServiceGrpcAsyncIOTransport,
    transports.AssetServiceRestTransport,
])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, 'default') as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "rest",
])
def test_transport_kind(transport_name):
    transport = AssetServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name

def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.AssetServiceGrpcTransport,
    )

def test_asset_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AssetServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json"
        )


def test_asset_service_base_transport():
    # Instantiate the base transport.
    with mock.patch('google.cloud.asset_v1.services.asset_service.transports.AssetServiceTransport.__init__') as Transport:
        Transport.return_value = None
        transport = transports.AssetServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'export_assets',
        'list_assets',
        'batch_get_assets_history',
        'create_feed',
        'get_feed',
        'list_feeds',
        'update_feed',
        'delete_feed',
        'search_all_resources',
        'search_all_iam_policies',
        'analyze_iam_policy',
        'analyze_iam_policy_longrunning',
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        'kind',
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_asset_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(google.auth, 'load_credentials_from_file', autospec=True) as load_creds, mock.patch('google.cloud.asset_v1.services.asset_service.transports.AssetServiceTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AssetServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with("credentials.json",
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id="octopus",
        )


def test_asset_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc, mock.patch('google.cloud.asset_v1.services.asset_service.transports.AssetServiceTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AssetServiceTransport()
        adc.assert_called_once()


def test_asset_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AssetServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AssetServiceGrpcTransport,
        transports.AssetServiceGrpcAsyncIOTransport,
    ],
)
def test_asset_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(                'https://www.googleapis.com/auth/cloud-platform',),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AssetServiceGrpcTransport,
        transports.AssetServiceGrpcAsyncIOTransport,
        transports.AssetServiceRestTransport,
    ],
)
def test_asset_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.AssetServiceGrpcTransport, grpc_helpers),
        (transports.AssetServiceGrpcAsyncIOTransport, grpc_helpers_async)
    ],
)
def test_asset_service_transport_create_channel(transport_class, grpc_helpers):
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
            "cloudasset.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=["1", "2"],
            default_host="cloudasset.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("transport_class", [transports.AssetServiceGrpcTransport, transports.AssetServiceGrpcAsyncIOTransport])
def test_asset_service_grpc_transport_client_cert_source_for_mtls(
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

def test_asset_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch("google.auth.transport.requests.AuthorizedSession.configure_mtls_channel") as mock_configure_mtls_channel:
        transports.AssetServiceRestTransport (
            credentials=cred,
            client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_asset_service_rest_lro_client():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_asset_service_host_no_port(transport_name):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='cloudasset.googleapis.com'),
         transport=transport_name,
    )
    assert client.transport._host == (
        'cloudasset.googleapis.com:443'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://cloudasset.googleapis.com'
    )

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_asset_service_host_with_port(transport_name):
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='cloudasset.googleapis.com:8000'),
        transport=transport_name,
    )
    assert client.transport._host == (
        'cloudasset.googleapis.com:8000'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://cloudasset.googleapis.com:8000'
    )

@pytest.mark.parametrize("transport_name", [
    "rest",
])
def test_asset_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = AssetServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = AssetServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.export_assets._session
    session2 = client2.transport.export_assets._session
    assert session1 != session2
    session1 = client1.transport.list_assets._session
    session2 = client2.transport.list_assets._session
    assert session1 != session2
    session1 = client1.transport.batch_get_assets_history._session
    session2 = client2.transport.batch_get_assets_history._session
    assert session1 != session2
    session1 = client1.transport.create_feed._session
    session2 = client2.transport.create_feed._session
    assert session1 != session2
    session1 = client1.transport.get_feed._session
    session2 = client2.transport.get_feed._session
    assert session1 != session2
    session1 = client1.transport.list_feeds._session
    session2 = client2.transport.list_feeds._session
    assert session1 != session2
    session1 = client1.transport.update_feed._session
    session2 = client2.transport.update_feed._session
    assert session1 != session2
    session1 = client1.transport.delete_feed._session
    session2 = client2.transport.delete_feed._session
    assert session1 != session2
    session1 = client1.transport.search_all_resources._session
    session2 = client2.transport.search_all_resources._session
    assert session1 != session2
    session1 = client1.transport.search_all_iam_policies._session
    session2 = client2.transport.search_all_iam_policies._session
    assert session1 != session2
    session1 = client1.transport.analyze_iam_policy._session
    session2 = client2.transport.analyze_iam_policy._session
    assert session1 != session2
    session1 = client1.transport.analyze_iam_policy_longrunning._session
    session2 = client2.transport.analyze_iam_policy_longrunning._session
    assert session1 != session2
def test_asset_service_grpc_transport_channel():
    channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AssetServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_asset_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AssetServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.AssetServiceGrpcTransport, transports.AssetServiceGrpcAsyncIOTransport])
def test_asset_service_transport_channel_mtls_with_client_cert_source(
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
@pytest.mark.parametrize("transport_class", [transports.AssetServiceGrpcTransport, transports.AssetServiceGrpcAsyncIOTransport])
def test_asset_service_transport_channel_mtls_with_adc(
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


def test_asset_service_grpc_lro_client():
    client = AssetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_asset_service_grpc_lro_async_client():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc_asyncio',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_asset_path():
    expected = "*".format()
    actual = AssetServiceClient.asset_path()
    assert expected == actual


def test_parse_asset_path():
    expected = {
    }
    path = AssetServiceClient.asset_path(**expected)

    # Check that the path construction is reversible.
    actual = AssetServiceClient.parse_asset_path(path)
    assert expected == actual

def test_feed_path():
    project = "squid"
    feed = "clam"
    expected = "projects/{project}/feeds/{feed}".format(project=project, feed=feed, )
    actual = AssetServiceClient.feed_path(project, feed)
    assert expected == actual


def test_parse_feed_path():
    expected = {
        "project": "whelk",
        "feed": "octopus",
    }
    path = AssetServiceClient.feed_path(**expected)

    # Check that the path construction is reversible.
    actual = AssetServiceClient.parse_feed_path(path)
    assert expected == actual

def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(billing_account=billing_account, )
    actual = AssetServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = AssetServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AssetServiceClient.parse_common_billing_account_path(path)
    assert expected == actual

def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(folder=folder, )
    actual = AssetServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = AssetServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AssetServiceClient.parse_common_folder_path(path)
    assert expected == actual

def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(organization=organization, )
    actual = AssetServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = AssetServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AssetServiceClient.parse_common_organization_path(path)
    assert expected == actual

def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(project=project, )
    actual = AssetServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = AssetServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AssetServiceClient.parse_common_project_path(path)
    assert expected == actual

def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(project=project, location=location, )
    actual = AssetServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = AssetServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AssetServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.AssetServiceTransport, '_prep_wrapped_messages') as prep:
        client = AssetServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.AssetServiceTransport, '_prep_wrapped_messages') as prep:
        transport_class = AssetServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

@pytest.mark.asyncio
async def test_transport_close_async():
    client = AssetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(type(getattr(client.transport, "grpc_channel")), "close") as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = AssetServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        with mock.patch.object(type(getattr(client.transport, close_name)), "close") as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()

def test_client_ctx():
    transports = [
        'rest',
        'grpc',
    ]
    for transport in transports:
        client = AssetServiceClient(
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
    (AssetServiceClient, transports.AssetServiceGrpcTransport),
    (AssetServiceAsyncClient, transports.AssetServiceGrpcAsyncIOTransport),
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
