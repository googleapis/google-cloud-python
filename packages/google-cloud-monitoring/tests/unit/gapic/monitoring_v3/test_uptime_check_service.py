# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api import monitored_resource_pb2 as ga_monitored_resource  # type: ignore
from google.api import monitored_resource_pb2 as monitored_resource  # type: ignore
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.monitoring_v3.services.uptime_check_service import (
    UptimeCheckServiceAsyncClient,
)
from google.cloud.monitoring_v3.services.uptime_check_service import (
    UptimeCheckServiceClient,
)
from google.cloud.monitoring_v3.services.uptime_check_service import pagers
from google.cloud.monitoring_v3.services.uptime_check_service import transports
from google.cloud.monitoring_v3.types import uptime
from google.cloud.monitoring_v3.types import uptime_service
from google.oauth2 import service_account
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert UptimeCheckServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        UptimeCheckServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        UptimeCheckServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        UptimeCheckServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        UptimeCheckServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        UptimeCheckServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [UptimeCheckServiceClient, UptimeCheckServiceAsyncClient]
)
def test_uptime_check_service_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "monitoring.googleapis.com:443"


def test_uptime_check_service_client_get_transport_class():
    transport = UptimeCheckServiceClient.get_transport_class()
    assert transport == transports.UptimeCheckServiceGrpcTransport

    transport = UptimeCheckServiceClient.get_transport_class("grpc")
    assert transport == transports.UptimeCheckServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (UptimeCheckServiceClient, transports.UptimeCheckServiceGrpcTransport, "grpc"),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    UptimeCheckServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(UptimeCheckServiceClient),
)
@mock.patch.object(
    UptimeCheckServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(UptimeCheckServiceAsyncClient),
)
def test_uptime_check_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(UptimeCheckServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(UptimeCheckServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            UptimeCheckServiceClient,
            transports.UptimeCheckServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            UptimeCheckServiceClient,
            transports.UptimeCheckServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    UptimeCheckServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(UptimeCheckServiceClient),
)
@mock.patch.object(
    UptimeCheckServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(UptimeCheckServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_uptime_check_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (UptimeCheckServiceClient, transports.UptimeCheckServiceGrpcTransport, "grpc"),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_uptime_check_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (UptimeCheckServiceClient, transports.UptimeCheckServiceGrpcTransport, "grpc"),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_uptime_check_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_uptime_check_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.monitoring_v3.services.uptime_check_service.transports.UptimeCheckServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = UptimeCheckServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_list_uptime_check_configs(
    transport: str = "grpc", request_type=uptime_service.ListUptimeCheckConfigsRequest
):
    client = UptimeCheckServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime_service.ListUptimeCheckConfigsResponse(
            next_page_token="next_page_token_value", total_size=1086,
        )

        response = client.list_uptime_check_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == uptime_service.ListUptimeCheckConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUptimeCheckConfigsPager)

    assert response.next_page_token == "next_page_token_value"

    assert response.total_size == 1086


def test_list_uptime_check_configs_from_dict():
    test_list_uptime_check_configs(request_type=dict)


@pytest.mark.asyncio
async def test_list_uptime_check_configs_async(transport: str = "grpc_asyncio"):
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = uptime_service.ListUptimeCheckConfigsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime_service.ListUptimeCheckConfigsResponse(
                next_page_token="next_page_token_value", total_size=1086,
            )
        )

        response = await client.list_uptime_check_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUptimeCheckConfigsAsyncPager)

    assert response.next_page_token == "next_page_token_value"

    assert response.total_size == 1086


def test_list_uptime_check_configs_field_headers():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.ListUptimeCheckConfigsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_uptime_check_configs), "__call__"
    ) as call:
        call.return_value = uptime_service.ListUptimeCheckConfigsResponse()

        client.list_uptime_check_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_uptime_check_configs_field_headers_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.ListUptimeCheckConfigsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_uptime_check_configs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime_service.ListUptimeCheckConfigsResponse()
        )

        await client.list_uptime_check_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_uptime_check_configs_flattened():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime_service.ListUptimeCheckConfigsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_uptime_check_configs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_uptime_check_configs_flattened_error():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_uptime_check_configs(
            uptime_service.ListUptimeCheckConfigsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_uptime_check_configs_flattened_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime_service.ListUptimeCheckConfigsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime_service.ListUptimeCheckConfigsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_uptime_check_configs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_uptime_check_configs_flattened_error_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_uptime_check_configs(
            uptime_service.ListUptimeCheckConfigsRequest(), parent="parent_value",
        )


def test_list_uptime_check_configs_pager():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[], next_page_token="def",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[uptime.UptimeCheckConfig(),],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_uptime_check_configs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, uptime.UptimeCheckConfig) for i in results)


def test_list_uptime_check_configs_pages():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[], next_page_token="def",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[uptime.UptimeCheckConfig(),],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_uptime_check_configs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_uptime_check_configs_async_pager():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_uptime_check_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[], next_page_token="def",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[uptime.UptimeCheckConfig(),],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_uptime_check_configs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, uptime.UptimeCheckConfig) for i in responses)


@pytest.mark.asyncio
async def test_list_uptime_check_configs_async_pages():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_uptime_check_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[], next_page_token="def",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[uptime.UptimeCheckConfig(),],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_uptime_check_configs(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_uptime_check_config(
    transport: str = "grpc", request_type=uptime_service.GetUptimeCheckConfigRequest
):
    client = UptimeCheckServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig(
            name="name_value",
            display_name="display_name_value",
            selected_regions=[uptime.UptimeCheckRegion.USA],
            is_internal=True,
            monitored_resource=monitored_resource.MonitoredResource(type="type_value"),
            http_check=uptime.UptimeCheckConfig.HttpCheck(
                request_method=uptime.UptimeCheckConfig.HttpCheck.RequestMethod.GET
            ),
        )

        response = client.get_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == uptime_service.GetUptimeCheckConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]

    assert response.is_internal is True


def test_get_uptime_check_config_from_dict():
    test_get_uptime_check_config(request_type=dict)


@pytest.mark.asyncio
async def test_get_uptime_check_config_async(transport: str = "grpc_asyncio"):
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = uptime_service.GetUptimeCheckConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig(
                name="name_value",
                display_name="display_name_value",
                selected_regions=[uptime.UptimeCheckRegion.USA],
                is_internal=True,
            )
        )

        response = await client.get_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]

    assert response.is_internal is True


def test_get_uptime_check_config_field_headers():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.GetUptimeCheckConfigRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_uptime_check_config), "__call__"
    ) as call:
        call.return_value = uptime.UptimeCheckConfig()

        client.get_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_uptime_check_config_field_headers_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.GetUptimeCheckConfigRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_uptime_check_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )

        await client.get_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_uptime_check_config_flattened():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_uptime_check_config(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_uptime_check_config_flattened_error():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_uptime_check_config(
            uptime_service.GetUptimeCheckConfigRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_uptime_check_config_flattened_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_uptime_check_config(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_uptime_check_config_flattened_error_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_uptime_check_config(
            uptime_service.GetUptimeCheckConfigRequest(), name="name_value",
        )


def test_create_uptime_check_config(
    transport: str = "grpc", request_type=uptime_service.CreateUptimeCheckConfigRequest
):
    client = UptimeCheckServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig(
            name="name_value",
            display_name="display_name_value",
            selected_regions=[uptime.UptimeCheckRegion.USA],
            is_internal=True,
            monitored_resource=monitored_resource.MonitoredResource(type="type_value"),
            http_check=uptime.UptimeCheckConfig.HttpCheck(
                request_method=uptime.UptimeCheckConfig.HttpCheck.RequestMethod.GET
            ),
        )

        response = client.create_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == uptime_service.CreateUptimeCheckConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]

    assert response.is_internal is True


def test_create_uptime_check_config_from_dict():
    test_create_uptime_check_config(request_type=dict)


@pytest.mark.asyncio
async def test_create_uptime_check_config_async(transport: str = "grpc_asyncio"):
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = uptime_service.CreateUptimeCheckConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig(
                name="name_value",
                display_name="display_name_value",
                selected_regions=[uptime.UptimeCheckRegion.USA],
                is_internal=True,
            )
        )

        response = await client.create_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]

    assert response.is_internal is True


def test_create_uptime_check_config_field_headers():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.CreateUptimeCheckConfigRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_uptime_check_config), "__call__"
    ) as call:
        call.return_value = uptime.UptimeCheckConfig()

        client.create_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_uptime_check_config_field_headers_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.CreateUptimeCheckConfigRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_uptime_check_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )

        await client.create_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_uptime_check_config_flattened():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_uptime_check_config(
            parent="parent_value",
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].uptime_check_config == uptime.UptimeCheckConfig(
            name="name_value"
        )


def test_create_uptime_check_config_flattened_error():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_uptime_check_config(
            uptime_service.CreateUptimeCheckConfigRequest(),
            parent="parent_value",
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_uptime_check_config_flattened_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_uptime_check_config(
            parent="parent_value",
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].uptime_check_config == uptime.UptimeCheckConfig(
            name="name_value"
        )


@pytest.mark.asyncio
async def test_create_uptime_check_config_flattened_error_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_uptime_check_config(
            uptime_service.CreateUptimeCheckConfigRequest(),
            parent="parent_value",
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )


def test_update_uptime_check_config(
    transport: str = "grpc", request_type=uptime_service.UpdateUptimeCheckConfigRequest
):
    client = UptimeCheckServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig(
            name="name_value",
            display_name="display_name_value",
            selected_regions=[uptime.UptimeCheckRegion.USA],
            is_internal=True,
            monitored_resource=monitored_resource.MonitoredResource(type="type_value"),
            http_check=uptime.UptimeCheckConfig.HttpCheck(
                request_method=uptime.UptimeCheckConfig.HttpCheck.RequestMethod.GET
            ),
        )

        response = client.update_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == uptime_service.UpdateUptimeCheckConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]

    assert response.is_internal is True


def test_update_uptime_check_config_from_dict():
    test_update_uptime_check_config(request_type=dict)


@pytest.mark.asyncio
async def test_update_uptime_check_config_async(transport: str = "grpc_asyncio"):
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = uptime_service.UpdateUptimeCheckConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig(
                name="name_value",
                display_name="display_name_value",
                selected_regions=[uptime.UptimeCheckRegion.USA],
                is_internal=True,
            )
        )

        response = await client.update_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]

    assert response.is_internal is True


def test_update_uptime_check_config_field_headers():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.UpdateUptimeCheckConfigRequest()
    request.uptime_check_config.name = "uptime_check_config.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_uptime_check_config), "__call__"
    ) as call:
        call.return_value = uptime.UptimeCheckConfig()

        client.update_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "uptime_check_config.name=uptime_check_config.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_uptime_check_config_field_headers_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.UpdateUptimeCheckConfigRequest()
    request.uptime_check_config.name = "uptime_check_config.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_uptime_check_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )

        await client.update_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "uptime_check_config.name=uptime_check_config.name/value",
    ) in kw["metadata"]


def test_update_uptime_check_config_flattened():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_uptime_check_config(
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].uptime_check_config == uptime.UptimeCheckConfig(
            name="name_value"
        )


def test_update_uptime_check_config_flattened_error():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_uptime_check_config(
            uptime_service.UpdateUptimeCheckConfigRequest(),
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_uptime_check_config_flattened_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_uptime_check_config(
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].uptime_check_config == uptime.UptimeCheckConfig(
            name="name_value"
        )


@pytest.mark.asyncio
async def test_update_uptime_check_config_flattened_error_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_uptime_check_config(
            uptime_service.UpdateUptimeCheckConfigRequest(),
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )


def test_delete_uptime_check_config(
    transport: str = "grpc", request_type=uptime_service.DeleteUptimeCheckConfigRequest
):
    client = UptimeCheckServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == uptime_service.DeleteUptimeCheckConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_uptime_check_config_from_dict():
    test_delete_uptime_check_config(request_type=dict)


@pytest.mark.asyncio
async def test_delete_uptime_check_config_async(transport: str = "grpc_asyncio"):
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = uptime_service.DeleteUptimeCheckConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_uptime_check_config_field_headers():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.DeleteUptimeCheckConfigRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_uptime_check_config), "__call__"
    ) as call:
        call.return_value = None

        client.delete_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_uptime_check_config_field_headers_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.DeleteUptimeCheckConfigRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_uptime_check_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_uptime_check_config_flattened():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_uptime_check_config(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_uptime_check_config_flattened_error():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_uptime_check_config(
            uptime_service.DeleteUptimeCheckConfigRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_uptime_check_config_flattened_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_uptime_check_config(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_uptime_check_config_flattened_error_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_uptime_check_config(
            uptime_service.DeleteUptimeCheckConfigRequest(), name="name_value",
        )


def test_list_uptime_check_ips(
    transport: str = "grpc", request_type=uptime_service.ListUptimeCheckIpsRequest
):
    client = UptimeCheckServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_uptime_check_ips), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime_service.ListUptimeCheckIpsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_uptime_check_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == uptime_service.ListUptimeCheckIpsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUptimeCheckIpsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_uptime_check_ips_from_dict():
    test_list_uptime_check_ips(request_type=dict)


@pytest.mark.asyncio
async def test_list_uptime_check_ips_async(transport: str = "grpc_asyncio"):
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = uptime_service.ListUptimeCheckIpsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_uptime_check_ips), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime_service.ListUptimeCheckIpsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_uptime_check_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUptimeCheckIpsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_uptime_check_ips_pager():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_uptime_check_ips), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[], next_page_token="def",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[uptime.UptimeCheckIp(),], next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[uptime.UptimeCheckIp(), uptime.UptimeCheckIp(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_uptime_check_ips(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, uptime.UptimeCheckIp) for i in results)


def test_list_uptime_check_ips_pages():
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_uptime_check_ips), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[], next_page_token="def",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[uptime.UptimeCheckIp(),], next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[uptime.UptimeCheckIp(), uptime.UptimeCheckIp(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_uptime_check_ips(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_uptime_check_ips_async_pager():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_uptime_check_ips),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[], next_page_token="def",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[uptime.UptimeCheckIp(),], next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[uptime.UptimeCheckIp(), uptime.UptimeCheckIp(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_uptime_check_ips(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, uptime.UptimeCheckIp) for i in responses)


@pytest.mark.asyncio
async def test_list_uptime_check_ips_async_pages():
    client = UptimeCheckServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_uptime_check_ips),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[], next_page_token="def",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[uptime.UptimeCheckIp(),], next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[uptime.UptimeCheckIp(), uptime.UptimeCheckIp(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_uptime_check_ips(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = UptimeCheckServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = UptimeCheckServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = UptimeCheckServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = UptimeCheckServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.UptimeCheckServiceGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.UptimeCheckServiceGrpcTransport,
        transports.UptimeCheckServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = UptimeCheckServiceClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.UptimeCheckServiceGrpcTransport,)


def test_uptime_check_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.UptimeCheckServiceTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_uptime_check_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.monitoring_v3.services.uptime_check_service.transports.UptimeCheckServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.UptimeCheckServiceTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_uptime_check_configs",
        "get_uptime_check_config",
        "create_uptime_check_config",
        "update_uptime_check_config",
        "delete_uptime_check_config",
        "list_uptime_check_ips",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_uptime_check_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.monitoring_v3.services.uptime_check_service.transports.UptimeCheckServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.UptimeCheckServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id="octopus",
        )


def test_uptime_check_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.monitoring_v3.services.uptime_check_service.transports.UptimeCheckServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.UptimeCheckServiceTransport()
        adc.assert_called_once()


def test_uptime_check_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        UptimeCheckServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id=None,
        )


def test_uptime_check_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.UptimeCheckServiceGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id="octopus",
        )


def test_uptime_check_service_host_no_port():
    client = UptimeCheckServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="monitoring.googleapis.com"
        ),
    )
    assert client._transport._host == "monitoring.googleapis.com:443"


def test_uptime_check_service_host_with_port():
    client = UptimeCheckServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="monitoring.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "monitoring.googleapis.com:8000"


def test_uptime_check_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.UptimeCheckServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


def test_uptime_check_service_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.UptimeCheckServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.UptimeCheckServiceGrpcTransport,
        transports.UptimeCheckServiceGrpcAsyncIOTransport,
    ],
)
def test_uptime_check_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
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
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/monitoring",
                    "https://www.googleapis.com/auth/monitoring.read",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.UptimeCheckServiceGrpcTransport,
        transports.UptimeCheckServiceGrpcAsyncIOTransport,
    ],
)
def test_uptime_check_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
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
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/monitoring",
                    "https://www.googleapis.com/auth/monitoring.read",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_uptime_check_config_path():
    project = "squid"
    uptime_check_config = "clam"

    expected = "projects/{project}/uptimeCheckConfigs/{uptime_check_config}".format(
        project=project, uptime_check_config=uptime_check_config,
    )
    actual = UptimeCheckServiceClient.uptime_check_config_path(
        project, uptime_check_config
    )
    assert expected == actual


def test_parse_uptime_check_config_path():
    expected = {
        "project": "whelk",
        "uptime_check_config": "octopus",
    }
    path = UptimeCheckServiceClient.uptime_check_config_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_uptime_check_config_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"

    expected = "projects/{project}".format(project=project,)
    actual = UptimeCheckServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = UptimeCheckServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = UptimeCheckServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = UptimeCheckServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"

    expected = "folders/{folder}".format(folder=folder,)
    actual = UptimeCheckServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = UptimeCheckServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = UptimeCheckServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = UptimeCheckServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = UptimeCheckServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = UptimeCheckServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.UptimeCheckServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = UptimeCheckServiceClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.UptimeCheckServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = UptimeCheckServiceClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
