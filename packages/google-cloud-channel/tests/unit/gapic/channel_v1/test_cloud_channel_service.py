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
import packaging.version

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.channel_v1.services.cloud_channel_service import (
    CloudChannelServiceAsyncClient,
)
from google.cloud.channel_v1.services.cloud_channel_service import (
    CloudChannelServiceClient,
)
from google.cloud.channel_v1.services.cloud_channel_service import pagers
from google.cloud.channel_v1.services.cloud_channel_service import transports
from google.cloud.channel_v1.services.cloud_channel_service.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.channel_v1.types import channel_partner_links
from google.cloud.channel_v1.types import common
from google.cloud.channel_v1.types import customers
from google.cloud.channel_v1.types import entitlements
from google.cloud.channel_v1.types import offers
from google.cloud.channel_v1.types import operations
from google.cloud.channel_v1.types import products
from google.cloud.channel_v1.types import service
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import postal_address_pb2  # type: ignore
import google.auth


# TODO(busunkim): Once google-auth >= 1.25.0 is required transitively
# through google-api-core:
# - Delete the auth "less than" test cases
# - Delete these pytest markers (Make the "greater than or equal to" tests the default).
requires_google_auth_lt_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) >= packaging.version.parse("1.25.0"),
    reason="This test requires google-auth < 1.25.0",
)
requires_google_auth_gte_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) < packaging.version.parse("1.25.0"),
    reason="This test requires google-auth >= 1.25.0",
)


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

    assert CloudChannelServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudChannelServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudChannelServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudChannelServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudChannelServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudChannelServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [CloudChannelServiceClient, CloudChannelServiceAsyncClient,]
)
def test_cloud_channel_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "cloudchannel.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [CloudChannelServiceClient, CloudChannelServiceAsyncClient,]
)
def test_cloud_channel_service_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CloudChannelServiceGrpcTransport, "grpc"),
        (transports.CloudChannelServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_cloud_channel_service_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize(
    "client_class", [CloudChannelServiceClient, CloudChannelServiceAsyncClient,]
)
def test_cloud_channel_service_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "cloudchannel.googleapis.com:443"


def test_cloud_channel_service_client_get_transport_class():
    transport = CloudChannelServiceClient.get_transport_class()
    available_transports = [
        transports.CloudChannelServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = CloudChannelServiceClient.get_transport_class("grpc")
    assert transport == transports.CloudChannelServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            CloudChannelServiceClient,
            transports.CloudChannelServiceGrpcTransport,
            "grpc",
        ),
        (
            CloudChannelServiceAsyncClient,
            transports.CloudChannelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    CloudChannelServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudChannelServiceClient),
)
@mock.patch.object(
    CloudChannelServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudChannelServiceAsyncClient),
)
def test_cloud_channel_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CloudChannelServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CloudChannelServiceClient, "get_transport_class") as gtc:
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
            client_cert_source_for_mtls=None,
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
                client_cert_source_for_mtls=None,
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
                client_cert_source_for_mtls=None,
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
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            CloudChannelServiceClient,
            transports.CloudChannelServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            CloudChannelServiceAsyncClient,
            transports.CloudChannelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            CloudChannelServiceClient,
            transports.CloudChannelServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            CloudChannelServiceAsyncClient,
            transports.CloudChannelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    CloudChannelServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudChannelServiceClient),
)
@mock.patch.object(
    CloudChannelServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudChannelServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cloud_channel_service_client_mtls_env_auto(
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
            patched.return_value = None
            client = client_class(client_options=options)

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
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            CloudChannelServiceClient,
            transports.CloudChannelServiceGrpcTransport,
            "grpc",
        ),
        (
            CloudChannelServiceAsyncClient,
            transports.CloudChannelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_channel_service_client_client_options_scopes(
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
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            CloudChannelServiceClient,
            transports.CloudChannelServiceGrpcTransport,
            "grpc",
        ),
        (
            CloudChannelServiceAsyncClient,
            transports.CloudChannelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_channel_service_client_client_options_credentials_file(
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
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_cloud_channel_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.channel_v1.services.cloud_channel_service.transports.CloudChannelServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudChannelServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_list_customers(
    transport: str = "grpc", request_type=service.ListCustomersRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCustomersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_customers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCustomersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_customers_from_dict():
    test_list_customers(request_type=dict)


def test_list_customers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        client.list_customers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCustomersRequest()


@pytest.mark.asyncio
async def test_list_customers_async(
    transport: str = "grpc_asyncio", request_type=service.ListCustomersRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCustomersResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_customers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCustomersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_customers_async_from_dict():
    await test_list_customers_async(request_type=dict)


def test_list_customers_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCustomersRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        call.return_value = service.ListCustomersResponse()
        client.list_customers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_customers_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCustomersRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCustomersResponse()
        )
        await client.list_customers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_customers_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                    customers.Customer(),
                ],
                next_page_token="abc",
            ),
            service.ListCustomersResponse(customers=[], next_page_token="def",),
            service.ListCustomersResponse(
                customers=[customers.Customer(),], next_page_token="ghi",
            ),
            service.ListCustomersResponse(
                customers=[customers.Customer(), customers.Customer(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_customers(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, customers.Customer) for i in results)


def test_list_customers_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                    customers.Customer(),
                ],
                next_page_token="abc",
            ),
            service.ListCustomersResponse(customers=[], next_page_token="def",),
            service.ListCustomersResponse(
                customers=[customers.Customer(),], next_page_token="ghi",
            ),
            service.ListCustomersResponse(
                customers=[customers.Customer(), customers.Customer(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_customers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_customers_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_customers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                    customers.Customer(),
                ],
                next_page_token="abc",
            ),
            service.ListCustomersResponse(customers=[], next_page_token="def",),
            service.ListCustomersResponse(
                customers=[customers.Customer(),], next_page_token="ghi",
            ),
            service.ListCustomersResponse(
                customers=[customers.Customer(), customers.Customer(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_customers(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, customers.Customer) for i in responses)


@pytest.mark.asyncio
async def test_list_customers_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_customers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                    customers.Customer(),
                ],
                next_page_token="abc",
            ),
            service.ListCustomersResponse(customers=[], next_page_token="def",),
            service.ListCustomersResponse(
                customers=[customers.Customer(),], next_page_token="ghi",
            ),
            service.ListCustomersResponse(
                customers=[customers.Customer(), customers.Customer(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_customers(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_customer(transport: str = "grpc", request_type=service.GetCustomerRequest):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.Customer(
            name="name_value",
            org_display_name="org_display_name_value",
            alternate_email="alternate_email_value",
            domain="domain_value",
            cloud_identity_id="cloud_identity_id_value",
            language_code="language_code_value",
            channel_partner_id="channel_partner_id_value",
        )
        response = client.get_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCustomerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, customers.Customer)
    assert response.name == "name_value"
    assert response.org_display_name == "org_display_name_value"
    assert response.alternate_email == "alternate_email_value"
    assert response.domain == "domain_value"
    assert response.cloud_identity_id == "cloud_identity_id_value"
    assert response.language_code == "language_code_value"
    assert response.channel_partner_id == "channel_partner_id_value"


def test_get_customer_from_dict():
    test_get_customer(request_type=dict)


def test_get_customer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        client.get_customer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCustomerRequest()


@pytest.mark.asyncio
async def test_get_customer_async(
    transport: str = "grpc_asyncio", request_type=service.GetCustomerRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customers.Customer(
                name="name_value",
                org_display_name="org_display_name_value",
                alternate_email="alternate_email_value",
                domain="domain_value",
                cloud_identity_id="cloud_identity_id_value",
                language_code="language_code_value",
                channel_partner_id="channel_partner_id_value",
            )
        )
        response = await client.get_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCustomerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, customers.Customer)
    assert response.name == "name_value"
    assert response.org_display_name == "org_display_name_value"
    assert response.alternate_email == "alternate_email_value"
    assert response.domain == "domain_value"
    assert response.cloud_identity_id == "cloud_identity_id_value"
    assert response.language_code == "language_code_value"
    assert response.channel_partner_id == "channel_partner_id_value"


@pytest.mark.asyncio
async def test_get_customer_async_from_dict():
    await test_get_customer_async(request_type=dict)


def test_get_customer_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCustomerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        call.return_value = customers.Customer()
        client.get_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_customer_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCustomerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(customers.Customer())
        await client.get_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_customer_flattened():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.Customer()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_customer(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_customer_flattened_error():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_customer(
            service.GetCustomerRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_customer_flattened_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.Customer()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(customers.Customer())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_customer(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_customer_flattened_error_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_customer(
            service.GetCustomerRequest(), name="name_value",
        )


def test_check_cloud_identity_accounts_exist(
    transport: str = "grpc", request_type=service.CheckCloudIdentityAccountsExistRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_cloud_identity_accounts_exist), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.CheckCloudIdentityAccountsExistResponse()
        response = client.check_cloud_identity_accounts_exist(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CheckCloudIdentityAccountsExistRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.CheckCloudIdentityAccountsExistResponse)


def test_check_cloud_identity_accounts_exist_from_dict():
    test_check_cloud_identity_accounts_exist(request_type=dict)


def test_check_cloud_identity_accounts_exist_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_cloud_identity_accounts_exist), "__call__"
    ) as call:
        client.check_cloud_identity_accounts_exist()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CheckCloudIdentityAccountsExistRequest()


@pytest.mark.asyncio
async def test_check_cloud_identity_accounts_exist_async(
    transport: str = "grpc_asyncio",
    request_type=service.CheckCloudIdentityAccountsExistRequest,
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_cloud_identity_accounts_exist), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.CheckCloudIdentityAccountsExistResponse()
        )
        response = await client.check_cloud_identity_accounts_exist(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CheckCloudIdentityAccountsExistRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.CheckCloudIdentityAccountsExistResponse)


@pytest.mark.asyncio
async def test_check_cloud_identity_accounts_exist_async_from_dict():
    await test_check_cloud_identity_accounts_exist_async(request_type=dict)


def test_check_cloud_identity_accounts_exist_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CheckCloudIdentityAccountsExistRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_cloud_identity_accounts_exist), "__call__"
    ) as call:
        call.return_value = service.CheckCloudIdentityAccountsExistResponse()
        client.check_cloud_identity_accounts_exist(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_check_cloud_identity_accounts_exist_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CheckCloudIdentityAccountsExistRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_cloud_identity_accounts_exist), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.CheckCloudIdentityAccountsExistResponse()
        )
        await client.check_cloud_identity_accounts_exist(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_customer(
    transport: str = "grpc", request_type=service.CreateCustomerRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.Customer(
            name="name_value",
            org_display_name="org_display_name_value",
            alternate_email="alternate_email_value",
            domain="domain_value",
            cloud_identity_id="cloud_identity_id_value",
            language_code="language_code_value",
            channel_partner_id="channel_partner_id_value",
        )
        response = client.create_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCustomerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, customers.Customer)
    assert response.name == "name_value"
    assert response.org_display_name == "org_display_name_value"
    assert response.alternate_email == "alternate_email_value"
    assert response.domain == "domain_value"
    assert response.cloud_identity_id == "cloud_identity_id_value"
    assert response.language_code == "language_code_value"
    assert response.channel_partner_id == "channel_partner_id_value"


def test_create_customer_from_dict():
    test_create_customer(request_type=dict)


def test_create_customer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_customer), "__call__") as call:
        client.create_customer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCustomerRequest()


@pytest.mark.asyncio
async def test_create_customer_async(
    transport: str = "grpc_asyncio", request_type=service.CreateCustomerRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customers.Customer(
                name="name_value",
                org_display_name="org_display_name_value",
                alternate_email="alternate_email_value",
                domain="domain_value",
                cloud_identity_id="cloud_identity_id_value",
                language_code="language_code_value",
                channel_partner_id="channel_partner_id_value",
            )
        )
        response = await client.create_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCustomerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, customers.Customer)
    assert response.name == "name_value"
    assert response.org_display_name == "org_display_name_value"
    assert response.alternate_email == "alternate_email_value"
    assert response.domain == "domain_value"
    assert response.cloud_identity_id == "cloud_identity_id_value"
    assert response.language_code == "language_code_value"
    assert response.channel_partner_id == "channel_partner_id_value"


@pytest.mark.asyncio
async def test_create_customer_async_from_dict():
    await test_create_customer_async(request_type=dict)


def test_create_customer_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCustomerRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_customer), "__call__") as call:
        call.return_value = customers.Customer()
        client.create_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_customer_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCustomerRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_customer), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(customers.Customer())
        await client.create_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_update_customer(
    transport: str = "grpc", request_type=service.UpdateCustomerRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.Customer(
            name="name_value",
            org_display_name="org_display_name_value",
            alternate_email="alternate_email_value",
            domain="domain_value",
            cloud_identity_id="cloud_identity_id_value",
            language_code="language_code_value",
            channel_partner_id="channel_partner_id_value",
        )
        response = client.update_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCustomerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, customers.Customer)
    assert response.name == "name_value"
    assert response.org_display_name == "org_display_name_value"
    assert response.alternate_email == "alternate_email_value"
    assert response.domain == "domain_value"
    assert response.cloud_identity_id == "cloud_identity_id_value"
    assert response.language_code == "language_code_value"
    assert response.channel_partner_id == "channel_partner_id_value"


def test_update_customer_from_dict():
    test_update_customer(request_type=dict)


def test_update_customer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_customer), "__call__") as call:
        client.update_customer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCustomerRequest()


@pytest.mark.asyncio
async def test_update_customer_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateCustomerRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customers.Customer(
                name="name_value",
                org_display_name="org_display_name_value",
                alternate_email="alternate_email_value",
                domain="domain_value",
                cloud_identity_id="cloud_identity_id_value",
                language_code="language_code_value",
                channel_partner_id="channel_partner_id_value",
            )
        )
        response = await client.update_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCustomerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, customers.Customer)
    assert response.name == "name_value"
    assert response.org_display_name == "org_display_name_value"
    assert response.alternate_email == "alternate_email_value"
    assert response.domain == "domain_value"
    assert response.cloud_identity_id == "cloud_identity_id_value"
    assert response.language_code == "language_code_value"
    assert response.channel_partner_id == "channel_partner_id_value"


@pytest.mark.asyncio
async def test_update_customer_async_from_dict():
    await test_update_customer_async(request_type=dict)


def test_update_customer_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCustomerRequest()

    request.customer.name = "customer.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_customer), "__call__") as call:
        call.return_value = customers.Customer()
        client.update_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "customer.name=customer.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_customer_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCustomerRequest()

    request.customer.name = "customer.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_customer), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(customers.Customer())
        await client.update_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "customer.name=customer.name/value",) in kw[
        "metadata"
    ]


def test_delete_customer(
    transport: str = "grpc", request_type=service.DeleteCustomerRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCustomerRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_customer_from_dict():
    test_delete_customer(request_type=dict)


def test_delete_customer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_customer), "__call__") as call:
        client.delete_customer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCustomerRequest()


@pytest.mark.asyncio
async def test_delete_customer_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteCustomerRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCustomerRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_customer_async_from_dict():
    await test_delete_customer_async(request_type=dict)


def test_delete_customer_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteCustomerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_customer), "__call__") as call:
        call.return_value = None
        client.delete_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_customer_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteCustomerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_customer), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_customer_flattened():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_customer(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_customer_flattened_error():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_customer(
            service.DeleteCustomerRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_customer_flattened_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_customer(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_customer_flattened_error_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_customer(
            service.DeleteCustomerRequest(), name="name_value",
        )


def test_provision_cloud_identity(
    transport: str = "grpc", request_type=service.ProvisionCloudIdentityRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_cloud_identity), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.provision_cloud_identity(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ProvisionCloudIdentityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_provision_cloud_identity_from_dict():
    test_provision_cloud_identity(request_type=dict)


def test_provision_cloud_identity_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_cloud_identity), "__call__"
    ) as call:
        client.provision_cloud_identity()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ProvisionCloudIdentityRequest()


@pytest.mark.asyncio
async def test_provision_cloud_identity_async(
    transport: str = "grpc_asyncio", request_type=service.ProvisionCloudIdentityRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_cloud_identity), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.provision_cloud_identity(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ProvisionCloudIdentityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_provision_cloud_identity_async_from_dict():
    await test_provision_cloud_identity_async(request_type=dict)


def test_provision_cloud_identity_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ProvisionCloudIdentityRequest()

    request.customer = "customer/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_cloud_identity), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.provision_cloud_identity(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "customer=customer/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_provision_cloud_identity_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ProvisionCloudIdentityRequest()

    request.customer = "customer/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_cloud_identity), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.provision_cloud_identity(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "customer=customer/value",) in kw["metadata"]


def test_list_entitlements(
    transport: str = "grpc", request_type=service.ListEntitlementsRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListEntitlementsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListEntitlementsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntitlementsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_entitlements_from_dict():
    test_list_entitlements(request_type=dict)


def test_list_entitlements_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        client.list_entitlements()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListEntitlementsRequest()


@pytest.mark.asyncio
async def test_list_entitlements_async(
    transport: str = "grpc_asyncio", request_type=service.ListEntitlementsRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListEntitlementsResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListEntitlementsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntitlementsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_entitlements_async_from_dict():
    await test_list_entitlements_async(request_type=dict)


def test_list_entitlements_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListEntitlementsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        call.return_value = service.ListEntitlementsResponse()
        client.list_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_entitlements_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListEntitlementsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListEntitlementsResponse()
        )
        await client.list_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_entitlements_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListEntitlementsResponse(
                entitlements=[
                    entitlements.Entitlement(),
                    entitlements.Entitlement(),
                    entitlements.Entitlement(),
                ],
                next_page_token="abc",
            ),
            service.ListEntitlementsResponse(entitlements=[], next_page_token="def",),
            service.ListEntitlementsResponse(
                entitlements=[entitlements.Entitlement(),], next_page_token="ghi",
            ),
            service.ListEntitlementsResponse(
                entitlements=[entitlements.Entitlement(), entitlements.Entitlement(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_entitlements(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, entitlements.Entitlement) for i in results)


def test_list_entitlements_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListEntitlementsResponse(
                entitlements=[
                    entitlements.Entitlement(),
                    entitlements.Entitlement(),
                    entitlements.Entitlement(),
                ],
                next_page_token="abc",
            ),
            service.ListEntitlementsResponse(entitlements=[], next_page_token="def",),
            service.ListEntitlementsResponse(
                entitlements=[entitlements.Entitlement(),], next_page_token="ghi",
            ),
            service.ListEntitlementsResponse(
                entitlements=[entitlements.Entitlement(), entitlements.Entitlement(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_entitlements(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_entitlements_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListEntitlementsResponse(
                entitlements=[
                    entitlements.Entitlement(),
                    entitlements.Entitlement(),
                    entitlements.Entitlement(),
                ],
                next_page_token="abc",
            ),
            service.ListEntitlementsResponse(entitlements=[], next_page_token="def",),
            service.ListEntitlementsResponse(
                entitlements=[entitlements.Entitlement(),], next_page_token="ghi",
            ),
            service.ListEntitlementsResponse(
                entitlements=[entitlements.Entitlement(), entitlements.Entitlement(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_entitlements(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, entitlements.Entitlement) for i in responses)


@pytest.mark.asyncio
async def test_list_entitlements_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListEntitlementsResponse(
                entitlements=[
                    entitlements.Entitlement(),
                    entitlements.Entitlement(),
                    entitlements.Entitlement(),
                ],
                next_page_token="abc",
            ),
            service.ListEntitlementsResponse(entitlements=[], next_page_token="def",),
            service.ListEntitlementsResponse(
                entitlements=[entitlements.Entitlement(),], next_page_token="ghi",
            ),
            service.ListEntitlementsResponse(
                entitlements=[entitlements.Entitlement(), entitlements.Entitlement(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_entitlements(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_transferable_skus(
    transport: str = "grpc", request_type=service.ListTransferableSkusRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_skus), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListTransferableSkusResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_transferable_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTransferableSkusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTransferableSkusPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_transferable_skus_from_dict():
    test_list_transferable_skus(request_type=dict)


def test_list_transferable_skus_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_skus), "__call__"
    ) as call:
        client.list_transferable_skus()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTransferableSkusRequest()


@pytest.mark.asyncio
async def test_list_transferable_skus_async(
    transport: str = "grpc_asyncio", request_type=service.ListTransferableSkusRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_skus), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListTransferableSkusResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_transferable_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTransferableSkusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTransferableSkusAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_transferable_skus_async_from_dict():
    await test_list_transferable_skus_async(request_type=dict)


def test_list_transferable_skus_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListTransferableSkusRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_skus), "__call__"
    ) as call:
        call.return_value = service.ListTransferableSkusResponse()
        client.list_transferable_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_transferable_skus_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListTransferableSkusRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_skus), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListTransferableSkusResponse()
        )
        await client.list_transferable_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_transferable_skus_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_skus), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTransferableSkusResponse(
                transferable_skus=[
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                ],
                next_page_token="abc",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[], next_page_token="def",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[entitlements.TransferableSku(),],
                next_page_token="ghi",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_transferable_skus(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, entitlements.TransferableSku) for i in results)


def test_list_transferable_skus_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_skus), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTransferableSkusResponse(
                transferable_skus=[
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                ],
                next_page_token="abc",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[], next_page_token="def",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[entitlements.TransferableSku(),],
                next_page_token="ghi",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_transferable_skus(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_transferable_skus_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_skus),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTransferableSkusResponse(
                transferable_skus=[
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                ],
                next_page_token="abc",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[], next_page_token="def",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[entitlements.TransferableSku(),],
                next_page_token="ghi",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_transferable_skus(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, entitlements.TransferableSku) for i in responses)


@pytest.mark.asyncio
async def test_list_transferable_skus_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_skus),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTransferableSkusResponse(
                transferable_skus=[
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                ],
                next_page_token="abc",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[], next_page_token="def",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[entitlements.TransferableSku(),],
                next_page_token="ghi",
            ),
            service.ListTransferableSkusResponse(
                transferable_skus=[
                    entitlements.TransferableSku(),
                    entitlements.TransferableSku(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_transferable_skus(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_transferable_offers(
    transport: str = "grpc", request_type=service.ListTransferableOffersRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_offers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListTransferableOffersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_transferable_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTransferableOffersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTransferableOffersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_transferable_offers_from_dict():
    test_list_transferable_offers(request_type=dict)


def test_list_transferable_offers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_offers), "__call__"
    ) as call:
        client.list_transferable_offers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTransferableOffersRequest()


@pytest.mark.asyncio
async def test_list_transferable_offers_async(
    transport: str = "grpc_asyncio", request_type=service.ListTransferableOffersRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_offers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListTransferableOffersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_transferable_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTransferableOffersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTransferableOffersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_transferable_offers_async_from_dict():
    await test_list_transferable_offers_async(request_type=dict)


def test_list_transferable_offers_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListTransferableOffersRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_offers), "__call__"
    ) as call:
        call.return_value = service.ListTransferableOffersResponse()
        client.list_transferable_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_transferable_offers_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListTransferableOffersRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_offers), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListTransferableOffersResponse()
        )
        await client.list_transferable_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_transferable_offers_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_offers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTransferableOffersResponse(
                transferable_offers=[
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                ],
                next_page_token="abc",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[], next_page_token="def",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[service.TransferableOffer(),],
                next_page_token="ghi",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_transferable_offers(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, service.TransferableOffer) for i in results)


def test_list_transferable_offers_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_offers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTransferableOffersResponse(
                transferable_offers=[
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                ],
                next_page_token="abc",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[], next_page_token="def",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[service.TransferableOffer(),],
                next_page_token="ghi",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_transferable_offers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_transferable_offers_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_offers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTransferableOffersResponse(
                transferable_offers=[
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                ],
                next_page_token="abc",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[], next_page_token="def",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[service.TransferableOffer(),],
                next_page_token="ghi",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_transferable_offers(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, service.TransferableOffer) for i in responses)


@pytest.mark.asyncio
async def test_list_transferable_offers_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_transferable_offers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTransferableOffersResponse(
                transferable_offers=[
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                ],
                next_page_token="abc",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[], next_page_token="def",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[service.TransferableOffer(),],
                next_page_token="ghi",
            ),
            service.ListTransferableOffersResponse(
                transferable_offers=[
                    service.TransferableOffer(),
                    service.TransferableOffer(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_transferable_offers(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_entitlement(
    transport: str = "grpc", request_type=service.GetEntitlementRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entitlement), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = entitlements.Entitlement(
            name="name_value",
            offer="offer_value",
            provisioning_state=entitlements.Entitlement.ProvisioningState.ACTIVE,
            suspension_reasons=[
                entitlements.Entitlement.SuspensionReason.RESELLER_INITIATED
            ],
            purchase_order_id="purchase_order_id_value",
        )
        response = client.get_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetEntitlementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, entitlements.Entitlement)
    assert response.name == "name_value"
    assert response.offer == "offer_value"
    assert (
        response.provisioning_state == entitlements.Entitlement.ProvisioningState.ACTIVE
    )
    assert response.suspension_reasons == [
        entitlements.Entitlement.SuspensionReason.RESELLER_INITIATED
    ]
    assert response.purchase_order_id == "purchase_order_id_value"


def test_get_entitlement_from_dict():
    test_get_entitlement(request_type=dict)


def test_get_entitlement_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entitlement), "__call__") as call:
        client.get_entitlement()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetEntitlementRequest()


@pytest.mark.asyncio
async def test_get_entitlement_async(
    transport: str = "grpc_asyncio", request_type=service.GetEntitlementRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entitlement), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            entitlements.Entitlement(
                name="name_value",
                offer="offer_value",
                provisioning_state=entitlements.Entitlement.ProvisioningState.ACTIVE,
                suspension_reasons=[
                    entitlements.Entitlement.SuspensionReason.RESELLER_INITIATED
                ],
                purchase_order_id="purchase_order_id_value",
            )
        )
        response = await client.get_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetEntitlementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, entitlements.Entitlement)
    assert response.name == "name_value"
    assert response.offer == "offer_value"
    assert (
        response.provisioning_state == entitlements.Entitlement.ProvisioningState.ACTIVE
    )
    assert response.suspension_reasons == [
        entitlements.Entitlement.SuspensionReason.RESELLER_INITIATED
    ]
    assert response.purchase_order_id == "purchase_order_id_value"


@pytest.mark.asyncio
async def test_get_entitlement_async_from_dict():
    await test_get_entitlement_async(request_type=dict)


def test_get_entitlement_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetEntitlementRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entitlement), "__call__") as call:
        call.return_value = entitlements.Entitlement()
        client.get_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_entitlement_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetEntitlementRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entitlement), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            entitlements.Entitlement()
        )
        await client.get_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_create_entitlement(
    transport: str = "grpc", request_type=service.CreateEntitlementRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entitlement), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateEntitlementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_entitlement_from_dict():
    test_create_entitlement(request_type=dict)


def test_create_entitlement_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entitlement), "__call__"
    ) as call:
        client.create_entitlement()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateEntitlementRequest()


@pytest.mark.asyncio
async def test_create_entitlement_async(
    transport: str = "grpc_asyncio", request_type=service.CreateEntitlementRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entitlement), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateEntitlementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_entitlement_async_from_dict():
    await test_create_entitlement_async(request_type=dict)


def test_create_entitlement_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateEntitlementRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entitlement), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_entitlement_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateEntitlementRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entitlement), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_change_parameters(
    transport: str = "grpc", request_type=service.ChangeParametersRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.change_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.change_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ChangeParametersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_change_parameters_from_dict():
    test_change_parameters(request_type=dict)


def test_change_parameters_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.change_parameters), "__call__"
    ) as call:
        client.change_parameters()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ChangeParametersRequest()


@pytest.mark.asyncio
async def test_change_parameters_async(
    transport: str = "grpc_asyncio", request_type=service.ChangeParametersRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.change_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.change_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ChangeParametersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_change_parameters_async_from_dict():
    await test_change_parameters_async(request_type=dict)


def test_change_parameters_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ChangeParametersRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.change_parameters), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.change_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_change_parameters_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ChangeParametersRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.change_parameters), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.change_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_change_renewal_settings(
    transport: str = "grpc", request_type=service.ChangeRenewalSettingsRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.change_renewal_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.change_renewal_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ChangeRenewalSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_change_renewal_settings_from_dict():
    test_change_renewal_settings(request_type=dict)


def test_change_renewal_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.change_renewal_settings), "__call__"
    ) as call:
        client.change_renewal_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ChangeRenewalSettingsRequest()


@pytest.mark.asyncio
async def test_change_renewal_settings_async(
    transport: str = "grpc_asyncio", request_type=service.ChangeRenewalSettingsRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.change_renewal_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.change_renewal_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ChangeRenewalSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_change_renewal_settings_async_from_dict():
    await test_change_renewal_settings_async(request_type=dict)


def test_change_renewal_settings_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ChangeRenewalSettingsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.change_renewal_settings), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.change_renewal_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_change_renewal_settings_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ChangeRenewalSettingsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.change_renewal_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.change_renewal_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_change_offer(transport: str = "grpc", request_type=service.ChangeOfferRequest):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.change_offer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.change_offer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ChangeOfferRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_change_offer_from_dict():
    test_change_offer(request_type=dict)


def test_change_offer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.change_offer), "__call__") as call:
        client.change_offer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ChangeOfferRequest()


@pytest.mark.asyncio
async def test_change_offer_async(
    transport: str = "grpc_asyncio", request_type=service.ChangeOfferRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.change_offer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.change_offer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ChangeOfferRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_change_offer_async_from_dict():
    await test_change_offer_async(request_type=dict)


def test_change_offer_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ChangeOfferRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.change_offer), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.change_offer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_change_offer_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ChangeOfferRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.change_offer), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.change_offer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_start_paid_service(
    transport: str = "grpc", request_type=service.StartPaidServiceRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_paid_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.start_paid_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.StartPaidServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_start_paid_service_from_dict():
    test_start_paid_service(request_type=dict)


def test_start_paid_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_paid_service), "__call__"
    ) as call:
        client.start_paid_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.StartPaidServiceRequest()


@pytest.mark.asyncio
async def test_start_paid_service_async(
    transport: str = "grpc_asyncio", request_type=service.StartPaidServiceRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_paid_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.start_paid_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.StartPaidServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_start_paid_service_async_from_dict():
    await test_start_paid_service_async(request_type=dict)


def test_start_paid_service_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.StartPaidServiceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_paid_service), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.start_paid_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_start_paid_service_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.StartPaidServiceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_paid_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.start_paid_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_suspend_entitlement(
    transport: str = "grpc", request_type=service.SuspendEntitlementRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suspend_entitlement), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.suspend_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.SuspendEntitlementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_suspend_entitlement_from_dict():
    test_suspend_entitlement(request_type=dict)


def test_suspend_entitlement_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suspend_entitlement), "__call__"
    ) as call:
        client.suspend_entitlement()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.SuspendEntitlementRequest()


@pytest.mark.asyncio
async def test_suspend_entitlement_async(
    transport: str = "grpc_asyncio", request_type=service.SuspendEntitlementRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suspend_entitlement), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.suspend_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.SuspendEntitlementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_suspend_entitlement_async_from_dict():
    await test_suspend_entitlement_async(request_type=dict)


def test_suspend_entitlement_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.SuspendEntitlementRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suspend_entitlement), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.suspend_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_suspend_entitlement_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.SuspendEntitlementRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suspend_entitlement), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.suspend_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_cancel_entitlement(
    transport: str = "grpc", request_type=service.CancelEntitlementRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_entitlement), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.cancel_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CancelEntitlementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_cancel_entitlement_from_dict():
    test_cancel_entitlement(request_type=dict)


def test_cancel_entitlement_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_entitlement), "__call__"
    ) as call:
        client.cancel_entitlement()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CancelEntitlementRequest()


@pytest.mark.asyncio
async def test_cancel_entitlement_async(
    transport: str = "grpc_asyncio", request_type=service.CancelEntitlementRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_entitlement), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.cancel_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CancelEntitlementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_cancel_entitlement_async_from_dict():
    await test_cancel_entitlement_async(request_type=dict)


def test_cancel_entitlement_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CancelEntitlementRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_entitlement), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.cancel_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_entitlement_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CancelEntitlementRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_entitlement), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.cancel_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_activate_entitlement(
    transport: str = "grpc", request_type=service.ActivateEntitlementRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_entitlement), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.activate_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ActivateEntitlementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_activate_entitlement_from_dict():
    test_activate_entitlement(request_type=dict)


def test_activate_entitlement_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_entitlement), "__call__"
    ) as call:
        client.activate_entitlement()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ActivateEntitlementRequest()


@pytest.mark.asyncio
async def test_activate_entitlement_async(
    transport: str = "grpc_asyncio", request_type=service.ActivateEntitlementRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_entitlement), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.activate_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ActivateEntitlementRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_activate_entitlement_async_from_dict():
    await test_activate_entitlement_async(request_type=dict)


def test_activate_entitlement_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ActivateEntitlementRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_entitlement), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.activate_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_activate_entitlement_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ActivateEntitlementRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_entitlement), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.activate_entitlement(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_transfer_entitlements(
    transport: str = "grpc", request_type=service.TransferEntitlementsRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.transfer_entitlements), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.transfer_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.TransferEntitlementsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_transfer_entitlements_from_dict():
    test_transfer_entitlements(request_type=dict)


def test_transfer_entitlements_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.transfer_entitlements), "__call__"
    ) as call:
        client.transfer_entitlements()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.TransferEntitlementsRequest()


@pytest.mark.asyncio
async def test_transfer_entitlements_async(
    transport: str = "grpc_asyncio", request_type=service.TransferEntitlementsRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.transfer_entitlements), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.transfer_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.TransferEntitlementsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_transfer_entitlements_async_from_dict():
    await test_transfer_entitlements_async(request_type=dict)


def test_transfer_entitlements_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.TransferEntitlementsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.transfer_entitlements), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.transfer_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_transfer_entitlements_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.TransferEntitlementsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.transfer_entitlements), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.transfer_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_transfer_entitlements_to_google(
    transport: str = "grpc", request_type=service.TransferEntitlementsToGoogleRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.transfer_entitlements_to_google), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.transfer_entitlements_to_google(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.TransferEntitlementsToGoogleRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_transfer_entitlements_to_google_from_dict():
    test_transfer_entitlements_to_google(request_type=dict)


def test_transfer_entitlements_to_google_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.transfer_entitlements_to_google), "__call__"
    ) as call:
        client.transfer_entitlements_to_google()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.TransferEntitlementsToGoogleRequest()


@pytest.mark.asyncio
async def test_transfer_entitlements_to_google_async(
    transport: str = "grpc_asyncio",
    request_type=service.TransferEntitlementsToGoogleRequest,
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.transfer_entitlements_to_google), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.transfer_entitlements_to_google(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.TransferEntitlementsToGoogleRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_transfer_entitlements_to_google_async_from_dict():
    await test_transfer_entitlements_to_google_async(request_type=dict)


def test_transfer_entitlements_to_google_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.TransferEntitlementsToGoogleRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.transfer_entitlements_to_google), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.transfer_entitlements_to_google(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_transfer_entitlements_to_google_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.TransferEntitlementsToGoogleRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.transfer_entitlements_to_google), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.transfer_entitlements_to_google(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_channel_partner_links(
    transport: str = "grpc", request_type=service.ListChannelPartnerLinksRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_channel_partner_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListChannelPartnerLinksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_channel_partner_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListChannelPartnerLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListChannelPartnerLinksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_channel_partner_links_from_dict():
    test_list_channel_partner_links(request_type=dict)


def test_list_channel_partner_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_channel_partner_links), "__call__"
    ) as call:
        client.list_channel_partner_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListChannelPartnerLinksRequest()


@pytest.mark.asyncio
async def test_list_channel_partner_links_async(
    transport: str = "grpc_asyncio", request_type=service.ListChannelPartnerLinksRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_channel_partner_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListChannelPartnerLinksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_channel_partner_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListChannelPartnerLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListChannelPartnerLinksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_channel_partner_links_async_from_dict():
    await test_list_channel_partner_links_async(request_type=dict)


def test_list_channel_partner_links_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListChannelPartnerLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_channel_partner_links), "__call__"
    ) as call:
        call.return_value = service.ListChannelPartnerLinksResponse()
        client.list_channel_partner_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_channel_partner_links_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListChannelPartnerLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_channel_partner_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListChannelPartnerLinksResponse()
        )
        await client.list_channel_partner_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_channel_partner_links_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_channel_partner_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                ],
                next_page_token="abc",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[], next_page_token="def",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[channel_partner_links.ChannelPartnerLink(),],
                next_page_token="ghi",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_channel_partner_links(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, channel_partner_links.ChannelPartnerLink) for i in results
        )


def test_list_channel_partner_links_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_channel_partner_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                ],
                next_page_token="abc",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[], next_page_token="def",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[channel_partner_links.ChannelPartnerLink(),],
                next_page_token="ghi",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_channel_partner_links(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_channel_partner_links_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_channel_partner_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                ],
                next_page_token="abc",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[], next_page_token="def",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[channel_partner_links.ChannelPartnerLink(),],
                next_page_token="ghi",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_channel_partner_links(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, channel_partner_links.ChannelPartnerLink) for i in responses
        )


@pytest.mark.asyncio
async def test_list_channel_partner_links_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_channel_partner_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                ],
                next_page_token="abc",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[], next_page_token="def",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[channel_partner_links.ChannelPartnerLink(),],
                next_page_token="ghi",
            ),
            service.ListChannelPartnerLinksResponse(
                channel_partner_links=[
                    channel_partner_links.ChannelPartnerLink(),
                    channel_partner_links.ChannelPartnerLink(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_channel_partner_links(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_channel_partner_link(
    transport: str = "grpc", request_type=service.GetChannelPartnerLinkRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_channel_partner_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = channel_partner_links.ChannelPartnerLink(
            name="name_value",
            reseller_cloud_identity_id="reseller_cloud_identity_id_value",
            link_state=channel_partner_links.ChannelPartnerLinkState.INVITED,
            invite_link_uri="invite_link_uri_value",
            public_id="public_id_value",
        )
        response = client.get_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetChannelPartnerLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel_partner_links.ChannelPartnerLink)
    assert response.name == "name_value"
    assert response.reseller_cloud_identity_id == "reseller_cloud_identity_id_value"
    assert response.link_state == channel_partner_links.ChannelPartnerLinkState.INVITED
    assert response.invite_link_uri == "invite_link_uri_value"
    assert response.public_id == "public_id_value"


def test_get_channel_partner_link_from_dict():
    test_get_channel_partner_link(request_type=dict)


def test_get_channel_partner_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_channel_partner_link), "__call__"
    ) as call:
        client.get_channel_partner_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetChannelPartnerLinkRequest()


@pytest.mark.asyncio
async def test_get_channel_partner_link_async(
    transport: str = "grpc_asyncio", request_type=service.GetChannelPartnerLinkRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_channel_partner_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            channel_partner_links.ChannelPartnerLink(
                name="name_value",
                reseller_cloud_identity_id="reseller_cloud_identity_id_value",
                link_state=channel_partner_links.ChannelPartnerLinkState.INVITED,
                invite_link_uri="invite_link_uri_value",
                public_id="public_id_value",
            )
        )
        response = await client.get_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetChannelPartnerLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel_partner_links.ChannelPartnerLink)
    assert response.name == "name_value"
    assert response.reseller_cloud_identity_id == "reseller_cloud_identity_id_value"
    assert response.link_state == channel_partner_links.ChannelPartnerLinkState.INVITED
    assert response.invite_link_uri == "invite_link_uri_value"
    assert response.public_id == "public_id_value"


@pytest.mark.asyncio
async def test_get_channel_partner_link_async_from_dict():
    await test_get_channel_partner_link_async(request_type=dict)


def test_get_channel_partner_link_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetChannelPartnerLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_channel_partner_link), "__call__"
    ) as call:
        call.return_value = channel_partner_links.ChannelPartnerLink()
        client.get_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_channel_partner_link_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetChannelPartnerLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_channel_partner_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            channel_partner_links.ChannelPartnerLink()
        )
        await client.get_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_create_channel_partner_link(
    transport: str = "grpc", request_type=service.CreateChannelPartnerLinkRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_channel_partner_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = channel_partner_links.ChannelPartnerLink(
            name="name_value",
            reseller_cloud_identity_id="reseller_cloud_identity_id_value",
            link_state=channel_partner_links.ChannelPartnerLinkState.INVITED,
            invite_link_uri="invite_link_uri_value",
            public_id="public_id_value",
        )
        response = client.create_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateChannelPartnerLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel_partner_links.ChannelPartnerLink)
    assert response.name == "name_value"
    assert response.reseller_cloud_identity_id == "reseller_cloud_identity_id_value"
    assert response.link_state == channel_partner_links.ChannelPartnerLinkState.INVITED
    assert response.invite_link_uri == "invite_link_uri_value"
    assert response.public_id == "public_id_value"


def test_create_channel_partner_link_from_dict():
    test_create_channel_partner_link(request_type=dict)


def test_create_channel_partner_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_channel_partner_link), "__call__"
    ) as call:
        client.create_channel_partner_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateChannelPartnerLinkRequest()


@pytest.mark.asyncio
async def test_create_channel_partner_link_async(
    transport: str = "grpc_asyncio",
    request_type=service.CreateChannelPartnerLinkRequest,
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_channel_partner_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            channel_partner_links.ChannelPartnerLink(
                name="name_value",
                reseller_cloud_identity_id="reseller_cloud_identity_id_value",
                link_state=channel_partner_links.ChannelPartnerLinkState.INVITED,
                invite_link_uri="invite_link_uri_value",
                public_id="public_id_value",
            )
        )
        response = await client.create_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateChannelPartnerLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel_partner_links.ChannelPartnerLink)
    assert response.name == "name_value"
    assert response.reseller_cloud_identity_id == "reseller_cloud_identity_id_value"
    assert response.link_state == channel_partner_links.ChannelPartnerLinkState.INVITED
    assert response.invite_link_uri == "invite_link_uri_value"
    assert response.public_id == "public_id_value"


@pytest.mark.asyncio
async def test_create_channel_partner_link_async_from_dict():
    await test_create_channel_partner_link_async(request_type=dict)


def test_create_channel_partner_link_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateChannelPartnerLinkRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_channel_partner_link), "__call__"
    ) as call:
        call.return_value = channel_partner_links.ChannelPartnerLink()
        client.create_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_channel_partner_link_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateChannelPartnerLinkRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_channel_partner_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            channel_partner_links.ChannelPartnerLink()
        )
        await client.create_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_update_channel_partner_link(
    transport: str = "grpc", request_type=service.UpdateChannelPartnerLinkRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_channel_partner_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = channel_partner_links.ChannelPartnerLink(
            name="name_value",
            reseller_cloud_identity_id="reseller_cloud_identity_id_value",
            link_state=channel_partner_links.ChannelPartnerLinkState.INVITED,
            invite_link_uri="invite_link_uri_value",
            public_id="public_id_value",
        )
        response = client.update_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateChannelPartnerLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel_partner_links.ChannelPartnerLink)
    assert response.name == "name_value"
    assert response.reseller_cloud_identity_id == "reseller_cloud_identity_id_value"
    assert response.link_state == channel_partner_links.ChannelPartnerLinkState.INVITED
    assert response.invite_link_uri == "invite_link_uri_value"
    assert response.public_id == "public_id_value"


def test_update_channel_partner_link_from_dict():
    test_update_channel_partner_link(request_type=dict)


def test_update_channel_partner_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_channel_partner_link), "__call__"
    ) as call:
        client.update_channel_partner_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateChannelPartnerLinkRequest()


@pytest.mark.asyncio
async def test_update_channel_partner_link_async(
    transport: str = "grpc_asyncio",
    request_type=service.UpdateChannelPartnerLinkRequest,
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_channel_partner_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            channel_partner_links.ChannelPartnerLink(
                name="name_value",
                reseller_cloud_identity_id="reseller_cloud_identity_id_value",
                link_state=channel_partner_links.ChannelPartnerLinkState.INVITED,
                invite_link_uri="invite_link_uri_value",
                public_id="public_id_value",
            )
        )
        response = await client.update_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateChannelPartnerLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel_partner_links.ChannelPartnerLink)
    assert response.name == "name_value"
    assert response.reseller_cloud_identity_id == "reseller_cloud_identity_id_value"
    assert response.link_state == channel_partner_links.ChannelPartnerLinkState.INVITED
    assert response.invite_link_uri == "invite_link_uri_value"
    assert response.public_id == "public_id_value"


@pytest.mark.asyncio
async def test_update_channel_partner_link_async_from_dict():
    await test_update_channel_partner_link_async(request_type=dict)


def test_update_channel_partner_link_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateChannelPartnerLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_channel_partner_link), "__call__"
    ) as call:
        call.return_value = channel_partner_links.ChannelPartnerLink()
        client.update_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_channel_partner_link_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateChannelPartnerLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_channel_partner_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            channel_partner_links.ChannelPartnerLink()
        )
        await client.update_channel_partner_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_lookup_offer(transport: str = "grpc", request_type=service.LookupOfferRequest):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup_offer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = offers.Offer(name="name_value",)
        response = client.lookup_offer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.LookupOfferRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, offers.Offer)
    assert response.name == "name_value"


def test_lookup_offer_from_dict():
    test_lookup_offer(request_type=dict)


def test_lookup_offer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup_offer), "__call__") as call:
        client.lookup_offer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.LookupOfferRequest()


@pytest.mark.asyncio
async def test_lookup_offer_async(
    transport: str = "grpc_asyncio", request_type=service.LookupOfferRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup_offer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            offers.Offer(name="name_value",)
        )
        response = await client.lookup_offer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.LookupOfferRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, offers.Offer)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_lookup_offer_async_from_dict():
    await test_lookup_offer_async(request_type=dict)


def test_lookup_offer_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.LookupOfferRequest()

    request.entitlement = "entitlement/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup_offer), "__call__") as call:
        call.return_value = offers.Offer()
        client.lookup_offer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "entitlement=entitlement/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_lookup_offer_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.LookupOfferRequest()

    request.entitlement = "entitlement/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup_offer), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(offers.Offer())
        await client.lookup_offer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "entitlement=entitlement/value",) in kw["metadata"]


def test_list_products(
    transport: str = "grpc", request_type=service.ListProductsRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListProductsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListProductsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProductsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_products_from_dict():
    test_list_products(request_type=dict)


def test_list_products_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        client.list_products()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListProductsRequest()


@pytest.mark.asyncio
async def test_list_products_async(
    transport: str = "grpc_asyncio", request_type=service.ListProductsRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListProductsResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListProductsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProductsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_products_async_from_dict():
    await test_list_products_async(request_type=dict)


def test_list_products_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListProductsResponse(
                products=[products.Product(), products.Product(), products.Product(),],
                next_page_token="abc",
            ),
            service.ListProductsResponse(products=[], next_page_token="def",),
            service.ListProductsResponse(
                products=[products.Product(),], next_page_token="ghi",
            ),
            service.ListProductsResponse(
                products=[products.Product(), products.Product(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_products(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, products.Product) for i in results)


def test_list_products_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListProductsResponse(
                products=[products.Product(), products.Product(), products.Product(),],
                next_page_token="abc",
            ),
            service.ListProductsResponse(products=[], next_page_token="def",),
            service.ListProductsResponse(
                products=[products.Product(),], next_page_token="ghi",
            ),
            service.ListProductsResponse(
                products=[products.Product(), products.Product(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_products(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_products_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_products), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListProductsResponse(
                products=[products.Product(), products.Product(), products.Product(),],
                next_page_token="abc",
            ),
            service.ListProductsResponse(products=[], next_page_token="def",),
            service.ListProductsResponse(
                products=[products.Product(),], next_page_token="ghi",
            ),
            service.ListProductsResponse(
                products=[products.Product(), products.Product(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_products(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, products.Product) for i in responses)


@pytest.mark.asyncio
async def test_list_products_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_products), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListProductsResponse(
                products=[products.Product(), products.Product(), products.Product(),],
                next_page_token="abc",
            ),
            service.ListProductsResponse(products=[], next_page_token="def",),
            service.ListProductsResponse(
                products=[products.Product(),], next_page_token="ghi",
            ),
            service.ListProductsResponse(
                products=[products.Product(), products.Product(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_products(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_skus(transport: str = "grpc", request_type=service.ListSkusRequest):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListSkusResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListSkusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSkusPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_skus_from_dict():
    test_list_skus(request_type=dict)


def test_list_skus_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        client.list_skus()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListSkusRequest()


@pytest.mark.asyncio
async def test_list_skus_async(
    transport: str = "grpc_asyncio", request_type=service.ListSkusRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListSkusResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListSkusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSkusAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_skus_async_from_dict():
    await test_list_skus_async(request_type=dict)


def test_list_skus_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListSkusRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        call.return_value = service.ListSkusResponse()
        client.list_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_skus_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListSkusRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListSkusResponse()
        )
        await client.list_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_skus_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSkusResponse(
                skus=[products.Sku(), products.Sku(), products.Sku(),],
                next_page_token="abc",
            ),
            service.ListSkusResponse(skus=[], next_page_token="def",),
            service.ListSkusResponse(skus=[products.Sku(),], next_page_token="ghi",),
            service.ListSkusResponse(skus=[products.Sku(), products.Sku(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_skus(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, products.Sku) for i in results)


def test_list_skus_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSkusResponse(
                skus=[products.Sku(), products.Sku(), products.Sku(),],
                next_page_token="abc",
            ),
            service.ListSkusResponse(skus=[], next_page_token="def",),
            service.ListSkusResponse(skus=[products.Sku(),], next_page_token="ghi",),
            service.ListSkusResponse(skus=[products.Sku(), products.Sku(),],),
            RuntimeError,
        )
        pages = list(client.list_skus(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_skus_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_skus), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSkusResponse(
                skus=[products.Sku(), products.Sku(), products.Sku(),],
                next_page_token="abc",
            ),
            service.ListSkusResponse(skus=[], next_page_token="def",),
            service.ListSkusResponse(skus=[products.Sku(),], next_page_token="ghi",),
            service.ListSkusResponse(skus=[products.Sku(), products.Sku(),],),
            RuntimeError,
        )
        async_pager = await client.list_skus(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, products.Sku) for i in responses)


@pytest.mark.asyncio
async def test_list_skus_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_skus), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSkusResponse(
                skus=[products.Sku(), products.Sku(), products.Sku(),],
                next_page_token="abc",
            ),
            service.ListSkusResponse(skus=[], next_page_token="def",),
            service.ListSkusResponse(skus=[products.Sku(),], next_page_token="ghi",),
            service.ListSkusResponse(skus=[products.Sku(), products.Sku(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_skus(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_offers(transport: str = "grpc", request_type=service.ListOffersRequest):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_offers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListOffersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListOffersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOffersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_offers_from_dict():
    test_list_offers(request_type=dict)


def test_list_offers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_offers), "__call__") as call:
        client.list_offers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListOffersRequest()


@pytest.mark.asyncio
async def test_list_offers_async(
    transport: str = "grpc_asyncio", request_type=service.ListOffersRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_offers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListOffersResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListOffersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOffersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_offers_async_from_dict():
    await test_list_offers_async(request_type=dict)


def test_list_offers_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListOffersRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_offers), "__call__") as call:
        call.return_value = service.ListOffersResponse()
        client.list_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_offers_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListOffersRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_offers), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListOffersResponse()
        )
        await client.list_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_offers_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_offers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListOffersResponse(
                offers=[offers.Offer(), offers.Offer(), offers.Offer(),],
                next_page_token="abc",
            ),
            service.ListOffersResponse(offers=[], next_page_token="def",),
            service.ListOffersResponse(
                offers=[offers.Offer(),], next_page_token="ghi",
            ),
            service.ListOffersResponse(offers=[offers.Offer(), offers.Offer(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_offers(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, offers.Offer) for i in results)


def test_list_offers_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_offers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListOffersResponse(
                offers=[offers.Offer(), offers.Offer(), offers.Offer(),],
                next_page_token="abc",
            ),
            service.ListOffersResponse(offers=[], next_page_token="def",),
            service.ListOffersResponse(
                offers=[offers.Offer(),], next_page_token="ghi",
            ),
            service.ListOffersResponse(offers=[offers.Offer(), offers.Offer(),],),
            RuntimeError,
        )
        pages = list(client.list_offers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_offers_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_offers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListOffersResponse(
                offers=[offers.Offer(), offers.Offer(), offers.Offer(),],
                next_page_token="abc",
            ),
            service.ListOffersResponse(offers=[], next_page_token="def",),
            service.ListOffersResponse(
                offers=[offers.Offer(),], next_page_token="ghi",
            ),
            service.ListOffersResponse(offers=[offers.Offer(), offers.Offer(),],),
            RuntimeError,
        )
        async_pager = await client.list_offers(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, offers.Offer) for i in responses)


@pytest.mark.asyncio
async def test_list_offers_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_offers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListOffersResponse(
                offers=[offers.Offer(), offers.Offer(), offers.Offer(),],
                next_page_token="abc",
            ),
            service.ListOffersResponse(offers=[], next_page_token="def",),
            service.ListOffersResponse(
                offers=[offers.Offer(),], next_page_token="ghi",
            ),
            service.ListOffersResponse(offers=[offers.Offer(), offers.Offer(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_offers(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_purchasable_skus(
    transport: str = "grpc", request_type=service.ListPurchasableSkusRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_skus), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListPurchasableSkusResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_purchasable_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListPurchasableSkusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPurchasableSkusPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_purchasable_skus_from_dict():
    test_list_purchasable_skus(request_type=dict)


def test_list_purchasable_skus_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_skus), "__call__"
    ) as call:
        client.list_purchasable_skus()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListPurchasableSkusRequest()


@pytest.mark.asyncio
async def test_list_purchasable_skus_async(
    transport: str = "grpc_asyncio", request_type=service.ListPurchasableSkusRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_skus), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListPurchasableSkusResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_purchasable_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListPurchasableSkusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPurchasableSkusAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_purchasable_skus_async_from_dict():
    await test_list_purchasable_skus_async(request_type=dict)


def test_list_purchasable_skus_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListPurchasableSkusRequest()

    request.customer = "customer/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_skus), "__call__"
    ) as call:
        call.return_value = service.ListPurchasableSkusResponse()
        client.list_purchasable_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "customer=customer/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_purchasable_skus_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListPurchasableSkusRequest()

    request.customer = "customer/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_skus), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListPurchasableSkusResponse()
        )
        await client.list_purchasable_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "customer=customer/value",) in kw["metadata"]


def test_list_purchasable_skus_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_skus), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListPurchasableSkusResponse(
                purchasable_skus=[
                    service.PurchasableSku(),
                    service.PurchasableSku(),
                    service.PurchasableSku(),
                ],
                next_page_token="abc",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[], next_page_token="def",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[service.PurchasableSku(),], next_page_token="ghi",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[service.PurchasableSku(), service.PurchasableSku(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("customer", ""),)),
        )
        pager = client.list_purchasable_skus(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, service.PurchasableSku) for i in results)


def test_list_purchasable_skus_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_skus), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListPurchasableSkusResponse(
                purchasable_skus=[
                    service.PurchasableSku(),
                    service.PurchasableSku(),
                    service.PurchasableSku(),
                ],
                next_page_token="abc",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[], next_page_token="def",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[service.PurchasableSku(),], next_page_token="ghi",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[service.PurchasableSku(), service.PurchasableSku(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_purchasable_skus(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_purchasable_skus_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_skus),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListPurchasableSkusResponse(
                purchasable_skus=[
                    service.PurchasableSku(),
                    service.PurchasableSku(),
                    service.PurchasableSku(),
                ],
                next_page_token="abc",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[], next_page_token="def",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[service.PurchasableSku(),], next_page_token="ghi",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[service.PurchasableSku(), service.PurchasableSku(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_purchasable_skus(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, service.PurchasableSku) for i in responses)


@pytest.mark.asyncio
async def test_list_purchasable_skus_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_skus),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListPurchasableSkusResponse(
                purchasable_skus=[
                    service.PurchasableSku(),
                    service.PurchasableSku(),
                    service.PurchasableSku(),
                ],
                next_page_token="abc",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[], next_page_token="def",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[service.PurchasableSku(),], next_page_token="ghi",
            ),
            service.ListPurchasableSkusResponse(
                purchasable_skus=[service.PurchasableSku(), service.PurchasableSku(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_purchasable_skus(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_purchasable_offers(
    transport: str = "grpc", request_type=service.ListPurchasableOffersRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_offers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListPurchasableOffersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_purchasable_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListPurchasableOffersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPurchasableOffersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_purchasable_offers_from_dict():
    test_list_purchasable_offers(request_type=dict)


def test_list_purchasable_offers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_offers), "__call__"
    ) as call:
        client.list_purchasable_offers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListPurchasableOffersRequest()


@pytest.mark.asyncio
async def test_list_purchasable_offers_async(
    transport: str = "grpc_asyncio", request_type=service.ListPurchasableOffersRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_offers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListPurchasableOffersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_purchasable_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListPurchasableOffersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPurchasableOffersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_purchasable_offers_async_from_dict():
    await test_list_purchasable_offers_async(request_type=dict)


def test_list_purchasable_offers_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListPurchasableOffersRequest()

    request.customer = "customer/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_offers), "__call__"
    ) as call:
        call.return_value = service.ListPurchasableOffersResponse()
        client.list_purchasable_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "customer=customer/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_purchasable_offers_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListPurchasableOffersRequest()

    request.customer = "customer/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_offers), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListPurchasableOffersResponse()
        )
        await client.list_purchasable_offers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "customer=customer/value",) in kw["metadata"]


def test_list_purchasable_offers_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_offers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListPurchasableOffersResponse(
                purchasable_offers=[
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                ],
                next_page_token="abc",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[], next_page_token="def",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[service.PurchasableOffer(),], next_page_token="ghi",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("customer", ""),)),
        )
        pager = client.list_purchasable_offers(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, service.PurchasableOffer) for i in results)


def test_list_purchasable_offers_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_offers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListPurchasableOffersResponse(
                purchasable_offers=[
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                ],
                next_page_token="abc",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[], next_page_token="def",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[service.PurchasableOffer(),], next_page_token="ghi",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_purchasable_offers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_purchasable_offers_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_offers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListPurchasableOffersResponse(
                purchasable_offers=[
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                ],
                next_page_token="abc",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[], next_page_token="def",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[service.PurchasableOffer(),], next_page_token="ghi",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_purchasable_offers(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, service.PurchasableOffer) for i in responses)


@pytest.mark.asyncio
async def test_list_purchasable_offers_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_purchasable_offers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListPurchasableOffersResponse(
                purchasable_offers=[
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                ],
                next_page_token="abc",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[], next_page_token="def",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[service.PurchasableOffer(),], next_page_token="ghi",
            ),
            service.ListPurchasableOffersResponse(
                purchasable_offers=[
                    service.PurchasableOffer(),
                    service.PurchasableOffer(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_purchasable_offers(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_register_subscriber(
    transport: str = "grpc", request_type=service.RegisterSubscriberRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.register_subscriber), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.RegisterSubscriberResponse(topic="topic_value",)
        response = client.register_subscriber(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RegisterSubscriberRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.RegisterSubscriberResponse)
    assert response.topic == "topic_value"


def test_register_subscriber_from_dict():
    test_register_subscriber(request_type=dict)


def test_register_subscriber_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.register_subscriber), "__call__"
    ) as call:
        client.register_subscriber()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RegisterSubscriberRequest()


@pytest.mark.asyncio
async def test_register_subscriber_async(
    transport: str = "grpc_asyncio", request_type=service.RegisterSubscriberRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.register_subscriber), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RegisterSubscriberResponse(topic="topic_value",)
        )
        response = await client.register_subscriber(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RegisterSubscriberRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.RegisterSubscriberResponse)
    assert response.topic == "topic_value"


@pytest.mark.asyncio
async def test_register_subscriber_async_from_dict():
    await test_register_subscriber_async(request_type=dict)


def test_register_subscriber_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RegisterSubscriberRequest()

    request.account = "account/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.register_subscriber), "__call__"
    ) as call:
        call.return_value = service.RegisterSubscriberResponse()
        client.register_subscriber(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account=account/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_register_subscriber_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RegisterSubscriberRequest()

    request.account = "account/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.register_subscriber), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RegisterSubscriberResponse()
        )
        await client.register_subscriber(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account=account/value",) in kw["metadata"]


def test_unregister_subscriber(
    transport: str = "grpc", request_type=service.UnregisterSubscriberRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unregister_subscriber), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.UnregisterSubscriberResponse(topic="topic_value",)
        response = client.unregister_subscriber(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UnregisterSubscriberRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.UnregisterSubscriberResponse)
    assert response.topic == "topic_value"


def test_unregister_subscriber_from_dict():
    test_unregister_subscriber(request_type=dict)


def test_unregister_subscriber_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unregister_subscriber), "__call__"
    ) as call:
        client.unregister_subscriber()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UnregisterSubscriberRequest()


@pytest.mark.asyncio
async def test_unregister_subscriber_async(
    transport: str = "grpc_asyncio", request_type=service.UnregisterSubscriberRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unregister_subscriber), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.UnregisterSubscriberResponse(topic="topic_value",)
        )
        response = await client.unregister_subscriber(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UnregisterSubscriberRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.UnregisterSubscriberResponse)
    assert response.topic == "topic_value"


@pytest.mark.asyncio
async def test_unregister_subscriber_async_from_dict():
    await test_unregister_subscriber_async(request_type=dict)


def test_unregister_subscriber_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UnregisterSubscriberRequest()

    request.account = "account/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unregister_subscriber), "__call__"
    ) as call:
        call.return_value = service.UnregisterSubscriberResponse()
        client.unregister_subscriber(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account=account/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_unregister_subscriber_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UnregisterSubscriberRequest()

    request.account = "account/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unregister_subscriber), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.UnregisterSubscriberResponse()
        )
        await client.unregister_subscriber(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account=account/value",) in kw["metadata"]


def test_list_subscribers(
    transport: str = "grpc", request_type=service.ListSubscribersRequest
):
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_subscribers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListSubscribersResponse(
            topic="topic_value",
            service_accounts=["service_accounts_value"],
            next_page_token="next_page_token_value",
        )
        response = client.list_subscribers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListSubscribersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSubscribersPager)
    assert response.topic == "topic_value"
    assert response.service_accounts == ["service_accounts_value"]
    assert response.next_page_token == "next_page_token_value"


def test_list_subscribers_from_dict():
    test_list_subscribers(request_type=dict)


def test_list_subscribers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_subscribers), "__call__") as call:
        client.list_subscribers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListSubscribersRequest()


@pytest.mark.asyncio
async def test_list_subscribers_async(
    transport: str = "grpc_asyncio", request_type=service.ListSubscribersRequest
):
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_subscribers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListSubscribersResponse(
                topic="topic_value",
                service_accounts=["service_accounts_value"],
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_subscribers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListSubscribersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSubscribersAsyncPager)
    assert response.topic == "topic_value"
    assert response.service_accounts == ["service_accounts_value"]
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_subscribers_async_from_dict():
    await test_list_subscribers_async(request_type=dict)


def test_list_subscribers_field_headers():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListSubscribersRequest()

    request.account = "account/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_subscribers), "__call__") as call:
        call.return_value = service.ListSubscribersResponse()
        client.list_subscribers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account=account/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_subscribers_field_headers_async():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListSubscribersRequest()

    request.account = "account/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_subscribers), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListSubscribersResponse()
        )
        await client.list_subscribers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account=account/value",) in kw["metadata"]


def test_list_subscribers_pager():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_subscribers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSubscribersResponse(
                service_accounts=[str(), str(), str(),], next_page_token="abc",
            ),
            service.ListSubscribersResponse(
                service_accounts=[], next_page_token="def",
            ),
            service.ListSubscribersResponse(
                service_accounts=[str(),], next_page_token="ghi",
            ),
            service.ListSubscribersResponse(service_accounts=[str(), str(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("account", ""),)),
        )
        pager = client.list_subscribers(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, str) for i in results)


def test_list_subscribers_pages():
    client = CloudChannelServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_subscribers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSubscribersResponse(
                service_accounts=[str(), str(), str(),], next_page_token="abc",
            ),
            service.ListSubscribersResponse(
                service_accounts=[], next_page_token="def",
            ),
            service.ListSubscribersResponse(
                service_accounts=[str(),], next_page_token="ghi",
            ),
            service.ListSubscribersResponse(service_accounts=[str(), str(),],),
            RuntimeError,
        )
        pages = list(client.list_subscribers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_subscribers_async_pager():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscribers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSubscribersResponse(
                service_accounts=[str(), str(), str(),], next_page_token="abc",
            ),
            service.ListSubscribersResponse(
                service_accounts=[], next_page_token="def",
            ),
            service.ListSubscribersResponse(
                service_accounts=[str(),], next_page_token="ghi",
            ),
            service.ListSubscribersResponse(service_accounts=[str(), str(),],),
            RuntimeError,
        )
        async_pager = await client.list_subscribers(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, str) for i in responses)


@pytest.mark.asyncio
async def test_list_subscribers_async_pages():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscribers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSubscribersResponse(
                service_accounts=[str(), str(), str(),], next_page_token="abc",
            ),
            service.ListSubscribersResponse(
                service_accounts=[], next_page_token="def",
            ),
            service.ListSubscribersResponse(
                service_accounts=[str(),], next_page_token="ghi",
            ),
            service.ListSubscribersResponse(service_accounts=[str(), str(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_subscribers(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudChannelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudChannelServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CloudChannelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudChannelServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CloudChannelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudChannelServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudChannelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CloudChannelServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudChannelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CloudChannelServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudChannelServiceGrpcTransport,
        transports.CloudChannelServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(client.transport, transports.CloudChannelServiceGrpcTransport,)


def test_cloud_channel_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CloudChannelServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cloud_channel_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.channel_v1.services.cloud_channel_service.transports.CloudChannelServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CloudChannelServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_customers",
        "get_customer",
        "check_cloud_identity_accounts_exist",
        "create_customer",
        "update_customer",
        "delete_customer",
        "provision_cloud_identity",
        "list_entitlements",
        "list_transferable_skus",
        "list_transferable_offers",
        "get_entitlement",
        "create_entitlement",
        "change_parameters",
        "change_renewal_settings",
        "change_offer",
        "start_paid_service",
        "suspend_entitlement",
        "cancel_entitlement",
        "activate_entitlement",
        "transfer_entitlements",
        "transfer_entitlements_to_google",
        "list_channel_partner_links",
        "get_channel_partner_link",
        "create_channel_partner_link",
        "update_channel_partner_link",
        "lookup_offer",
        "list_products",
        "list_skus",
        "list_offers",
        "list_purchasable_skus",
        "list_purchasable_offers",
        "register_subscriber",
        "unregister_subscriber",
        "list_subscribers",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


@requires_google_auth_gte_1_25_0
def test_cloud_channel_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.channel_v1.services.cloud_channel_service.transports.CloudChannelServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudChannelServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/apps.order",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_cloud_channel_service_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.channel_v1.services.cloud_channel_service.transports.CloudChannelServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudChannelServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/apps.order",),
            quota_project_id="octopus",
        )


def test_cloud_channel_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.channel_v1.services.cloud_channel_service.transports.CloudChannelServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudChannelServiceTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_cloud_channel_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CloudChannelServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/apps.order",),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_cloud_channel_service_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CloudChannelServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/apps.order",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudChannelServiceGrpcTransport,
        transports.CloudChannelServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_cloud_channel_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/apps.order",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudChannelServiceGrpcTransport,
        transports.CloudChannelServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_cloud_channel_service_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/apps.order",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.CloudChannelServiceGrpcTransport, grpc_helpers),
        (transports.CloudChannelServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_cloud_channel_service_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "cloudchannel.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/apps.order",),
            scopes=["1", "2"],
            default_host="cloudchannel.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudChannelServiceGrpcTransport,
        transports.CloudChannelServiceGrpcAsyncIOTransport,
    ],
)
def test_cloud_channel_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
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
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_cloud_channel_service_host_no_port():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudchannel.googleapis.com"
        ),
    )
    assert client.transport._host == "cloudchannel.googleapis.com:443"


def test_cloud_channel_service_host_with_port():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudchannel.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "cloudchannel.googleapis.com:8000"


def test_cloud_channel_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudChannelServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cloud_channel_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudChannelServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudChannelServiceGrpcTransport,
        transports.CloudChannelServiceGrpcAsyncIOTransport,
    ],
)
def test_cloud_channel_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
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
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudChannelServiceGrpcTransport,
        transports.CloudChannelServiceGrpcAsyncIOTransport,
    ],
)
def test_cloud_channel_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
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
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_cloud_channel_service_grpc_lro_client():
    client = CloudChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_cloud_channel_service_grpc_lro_async_client():
    client = CloudChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_customer_path():
    account = "squid"
    customer = "clam"
    expected = "accounts/{account}/customers/{customer}".format(
        account=account, customer=customer,
    )
    actual = CloudChannelServiceClient.customer_path(account, customer)
    assert expected == actual


def test_parse_customer_path():
    expected = {
        "account": "whelk",
        "customer": "octopus",
    }
    path = CloudChannelServiceClient.customer_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudChannelServiceClient.parse_customer_path(path)
    assert expected == actual


def test_entitlement_path():
    account = "oyster"
    customer = "nudibranch"
    entitlement = "cuttlefish"
    expected = "accounts/{account}/customers/{customer}/entitlements/{entitlement}".format(
        account=account, customer=customer, entitlement=entitlement,
    )
    actual = CloudChannelServiceClient.entitlement_path(account, customer, entitlement)
    assert expected == actual


def test_parse_entitlement_path():
    expected = {
        "account": "mussel",
        "customer": "winkle",
        "entitlement": "nautilus",
    }
    path = CloudChannelServiceClient.entitlement_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudChannelServiceClient.parse_entitlement_path(path)
    assert expected == actual


def test_offer_path():
    account = "scallop"
    offer = "abalone"
    expected = "accounts/{account}/offers/{offer}".format(account=account, offer=offer,)
    actual = CloudChannelServiceClient.offer_path(account, offer)
    assert expected == actual


def test_parse_offer_path():
    expected = {
        "account": "squid",
        "offer": "clam",
    }
    path = CloudChannelServiceClient.offer_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudChannelServiceClient.parse_offer_path(path)
    assert expected == actual


def test_product_path():
    product = "whelk"
    expected = "products/{product}".format(product=product,)
    actual = CloudChannelServiceClient.product_path(product)
    assert expected == actual


def test_parse_product_path():
    expected = {
        "product": "octopus",
    }
    path = CloudChannelServiceClient.product_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudChannelServiceClient.parse_product_path(path)
    assert expected == actual


def test_sku_path():
    product = "oyster"
    sku = "nudibranch"
    expected = "products/{product}/skus/{sku}".format(product=product, sku=sku,)
    actual = CloudChannelServiceClient.sku_path(product, sku)
    assert expected == actual


def test_parse_sku_path():
    expected = {
        "product": "cuttlefish",
        "sku": "mussel",
    }
    path = CloudChannelServiceClient.sku_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudChannelServiceClient.parse_sku_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CloudChannelServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = CloudChannelServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudChannelServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(folder=folder,)
    actual = CloudChannelServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = CloudChannelServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudChannelServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = CloudChannelServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = CloudChannelServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudChannelServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(project=project,)
    actual = CloudChannelServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = CloudChannelServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudChannelServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = CloudChannelServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = CloudChannelServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudChannelServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CloudChannelServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CloudChannelServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CloudChannelServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CloudChannelServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
