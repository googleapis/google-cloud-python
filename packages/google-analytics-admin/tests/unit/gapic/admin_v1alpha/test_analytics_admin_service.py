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
from google.analytics.admin_v1alpha.services.analytics_admin_service import (
    AnalyticsAdminServiceAsyncClient,
)
from google.analytics.admin_v1alpha.services.analytics_admin_service import (
    AnalyticsAdminServiceClient,
)
from google.analytics.admin_v1alpha.services.analytics_admin_service import pagers
from google.analytics.admin_v1alpha.services.analytics_admin_service import transports
from google.analytics.admin_v1alpha.types import analytics_admin
from google.analytics.admin_v1alpha.types import resources
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert AnalyticsAdminServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [AnalyticsAdminServiceClient, AnalyticsAdminServiceAsyncClient]
)
def test_analytics_admin_service_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "analyticsadmin.googleapis.com:443"


def test_analytics_admin_service_client_get_transport_class():
    transport = AnalyticsAdminServiceClient.get_transport_class()
    assert transport == transports.AnalyticsAdminServiceGrpcTransport

    transport = AnalyticsAdminServiceClient.get_transport_class("grpc")
    assert transport == transports.AnalyticsAdminServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_analytics_admin_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AnalyticsAdminServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AnalyticsAdminServiceClient, "get_transport_class") as gtc:
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
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=client_cert_source_callback,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_MTLS_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
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
                    api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_analytics_admin_service_client_client_options_scopes(
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_analytics_admin_service_client_client_options_credentials_file(
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
        )


def test_analytics_admin_service_client_client_options_from_dict():
    with mock.patch(
        "google.analytics.admin_v1alpha.services.analytics_admin_service.transports.AnalyticsAdminServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AnalyticsAdminServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )


def test_get_account(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account(
            name="name_value",
            display_name="display_name_value",
            country_code="country_code_value",
            deleted=True,
        )

        response = client.get_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.country_code == "country_code_value"

    assert response.deleted is True


@pytest.mark.asyncio
async def test_get_account_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Account(
                name="name_value",
                display_name="display_name_value",
                country_code="country_code_value",
                deleted=True,
            )
        )

        response = await client.get_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.country_code == "country_code_value"

    assert response.deleted is True


def test_get_account_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetAccountRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_account), "__call__") as call:
        call.return_value = resources.Account()

        client.get_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_account_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetAccountRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_account), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())

        await client.get_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_account_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_account(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_account_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_account(
            analytics_admin.GetAccountRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_account_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_account(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_account_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_account(
            analytics_admin.GetAccountRequest(), name="name_value",
        )


def test_list_accounts(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListAccountsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_accounts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAccountsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_accounts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccountsPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_accounts_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListAccountsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_accounts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAccountsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_accounts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccountsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_accounts_pager():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_accounts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(accounts=[], next_page_token="def",),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(), resources.Account(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_accounts(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.Account) for i in results)


def test_list_accounts_pages():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_accounts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(accounts=[], next_page_token="def",),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(), resources.Account(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_accounts(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_accounts_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_accounts),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(accounts=[], next_page_token="def",),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(), resources.Account(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_accounts(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Account) for i in responses)


@pytest.mark.asyncio
async def test_list_accounts_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_accounts),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(accounts=[], next_page_token="def",),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(), resources.Account(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_accounts(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_delete_account(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_account_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_account_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteAccountRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_account), "__call__") as call:
        call.return_value = None

        client.delete_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_account_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteAccountRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_account), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_account_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_account(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_account_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_account(
            analytics_admin.DeleteAccountRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_account_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_account(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_account_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_account(
            analytics_admin.DeleteAccountRequest(), name="name_value",
        )


def test_update_account(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account(
            name="name_value",
            display_name="display_name_value",
            country_code="country_code_value",
            deleted=True,
        )

        response = client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.country_code == "country_code_value"

    assert response.deleted is True


@pytest.mark.asyncio
async def test_update_account_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Account(
                name="name_value",
                display_name="display_name_value",
                country_code="country_code_value",
                deleted=True,
            )
        )

        response = await client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.country_code == "country_code_value"

    assert response.deleted is True


def test_update_account_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateAccountRequest()
    request.account.name = "account.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_account), "__call__") as call:
        call.return_value = resources.Account()

        client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account.name=account.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_account_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateAccountRequest()
    request.account.name = "account.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_account), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())

        await client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account.name=account.name/value",) in kw[
        "metadata"
    ]


def test_update_account_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_account(
            account=resources.Account(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].account == resources.Account(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_account_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_account(
            analytics_admin.UpdateAccountRequest(),
            account=resources.Account(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_account_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_account(
            account=resources.Account(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].account == resources.Account(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_account_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_account(
            analytics_admin.UpdateAccountRequest(),
            account=resources.Account(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_provision_account_ticket(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ProvisionAccountTicketRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.provision_account_ticket), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ProvisionAccountTicketResponse(
            account_ticket_id="account_ticket_id_value",
        )

        response = client.provision_account_ticket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.ProvisionAccountTicketResponse)

    assert response.account_ticket_id == "account_ticket_id_value"


@pytest.mark.asyncio
async def test_provision_account_ticket_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ProvisionAccountTicketRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.provision_account_ticket), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ProvisionAccountTicketResponse(
                account_ticket_id="account_ticket_id_value",
            )
        )

        response = await client.provision_account_ticket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.ProvisionAccountTicketResponse)

    assert response.account_ticket_id == "account_ticket_id_value"


def test_get_property(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetPropertyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
            deleted=True,
        )

        response = client.get_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)

    assert response.name == "name_value"

    assert response.parent == "parent_value"

    assert response.display_name == "display_name_value"

    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE

    assert response.time_zone == "time_zone_value"

    assert response.currency_code == "currency_code_value"

    assert response.deleted is True


@pytest.mark.asyncio
async def test_get_property_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetPropertyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_property), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
                deleted=True,
            )
        )

        response = await client.get_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)

    assert response.name == "name_value"

    assert response.parent == "parent_value"

    assert response.display_name == "display_name_value"

    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE

    assert response.time_zone == "time_zone_value"

    assert response.currency_code == "currency_code_value"

    assert response.deleted is True


def test_get_property_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetPropertyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_property), "__call__") as call:
        call.return_value = resources.Property()

        client.get_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_property_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetPropertyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_property), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())

        await client.get_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_property(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_property(
            analytics_admin.GetPropertyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_property), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_property(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_property(
            analytics_admin.GetPropertyRequest(), name="name_value",
        )


def test_list_properties(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListPropertiesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_properties), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListPropertiesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_properties(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPropertiesPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_properties_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListPropertiesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_properties), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListPropertiesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_properties(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPropertiesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_properties_pager():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_properties), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[], next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(),], next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(), resources.Property(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_properties(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.Property) for i in results)


def test_list_properties_pages():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_properties), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[], next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(),], next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(), resources.Property(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_properties(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_properties_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_properties),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[], next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(),], next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(), resources.Property(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_properties(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Property) for i in responses)


@pytest.mark.asyncio
async def test_list_properties_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_properties),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[], next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(),], next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(), resources.Property(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_properties(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_create_property(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreatePropertyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
            deleted=True,
        )

        response = client.create_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)

    assert response.name == "name_value"

    assert response.parent == "parent_value"

    assert response.display_name == "display_name_value"

    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE

    assert response.time_zone == "time_zone_value"

    assert response.currency_code == "currency_code_value"

    assert response.deleted is True


@pytest.mark.asyncio
async def test_create_property_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreatePropertyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_property), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
                deleted=True,
            )
        )

        response = await client.create_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)

    assert response.name == "name_value"

    assert response.parent == "parent_value"

    assert response.display_name == "display_name_value"

    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE

    assert response.time_zone == "time_zone_value"

    assert response.currency_code == "currency_code_value"

    assert response.deleted is True


def test_create_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_property(property=resources.Property(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].property == resources.Property(name="name_value")


def test_create_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_property(
            analytics_admin.CreatePropertyRequest(),
            property=resources.Property(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_property), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_property(
            property=resources.Property(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].property == resources.Property(name="name_value")


@pytest.mark.asyncio
async def test_create_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_property(
            analytics_admin.CreatePropertyRequest(),
            property=resources.Property(name="name_value"),
        )


def test_delete_property(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeletePropertyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_property_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeletePropertyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_property), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_property_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeletePropertyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_property), "__call__") as call:
        call.return_value = None

        client.delete_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_property_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeletePropertyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_property), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_property(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_property(
            analytics_admin.DeletePropertyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_property), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_property(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_property(
            analytics_admin.DeletePropertyRequest(), name="name_value",
        )


def test_update_property(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdatePropertyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
            deleted=True,
        )

        response = client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)

    assert response.name == "name_value"

    assert response.parent == "parent_value"

    assert response.display_name == "display_name_value"

    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE

    assert response.time_zone == "time_zone_value"

    assert response.currency_code == "currency_code_value"

    assert response.deleted is True


@pytest.mark.asyncio
async def test_update_property_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdatePropertyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_property), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
                deleted=True,
            )
        )

        response = await client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)

    assert response.name == "name_value"

    assert response.parent == "parent_value"

    assert response.display_name == "display_name_value"

    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE

    assert response.time_zone == "time_zone_value"

    assert response.currency_code == "currency_code_value"

    assert response.deleted is True


def test_update_property_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdatePropertyRequest()
    request.property.name = "property.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_property), "__call__") as call:
        call.return_value = resources.Property()

        client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "property.name=property.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_property_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdatePropertyRequest()
    request.property.name = "property.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_property), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())

        await client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "property.name=property.name/value",) in kw[
        "metadata"
    ]


def test_update_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_property(
            property=resources.Property(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].property == resources.Property(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_property(
            analytics_admin.UpdatePropertyRequest(),
            property=resources.Property(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_property), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_property(
            property=resources.Property(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].property == resources.Property(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_property(
            analytics_admin.UpdatePropertyRequest(),
            property=resources.Property(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_get_user_link(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetUserLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink(
            name="name_value",
            email_address="email_address_value",
            direct_roles=["direct_roles_value"],
        )

        response = client.get_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)

    assert response.name == "name_value"

    assert response.email_address == "email_address_value"

    assert response.direct_roles == ["direct_roles_value"]


@pytest.mark.asyncio
async def test_get_user_link_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetUserLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.UserLink(
                name="name_value",
                email_address="email_address_value",
                direct_roles=["direct_roles_value"],
            )
        )

        response = await client.get_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)

    assert response.name == "name_value"

    assert response.email_address == "email_address_value"

    assert response.direct_roles == ["direct_roles_value"]


def test_get_user_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetUserLinkRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_user_link), "__call__") as call:
        call.return_value = resources.UserLink()

        client.get_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_user_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetUserLinkRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_user_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())

        await client.get_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_user_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_user_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_user_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_user_link(
            analytics_admin.GetUserLinkRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_user_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_user_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_user_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_user_link(
            analytics_admin.GetUserLinkRequest(), name="name_value",
        )


def test_batch_get_user_links(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.BatchGetUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_get_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.BatchGetUserLinksResponse()

        response = client.batch_get_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchGetUserLinksResponse)


@pytest.mark.asyncio
async def test_batch_get_user_links_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.BatchGetUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_get_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchGetUserLinksResponse()
        )

        response = await client.batch_get_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchGetUserLinksResponse)


def test_batch_get_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchGetUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_get_user_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.BatchGetUserLinksResponse()

        client.batch_get_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_get_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchGetUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_get_user_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchGetUserLinksResponse()
        )

        await client.batch_get_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_user_links(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_user_links), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListUserLinksResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUserLinksPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_user_links_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListUserLinksResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUserLinksAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_user_links), "__call__") as call:
        call.return_value = analytics_admin.ListUserLinksResponse()

        client.list_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_user_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListUserLinksResponse()
        )

        await client.list_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_user_links_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_user_links), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListUserLinksResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_user_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_user_links_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_user_links(
            analytics_admin.ListUserLinksRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_user_links_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListUserLinksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListUserLinksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_user_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_user_links_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_user_links(
            analytics_admin.ListUserLinksRequest(), parent="parent_value",
        )


def test_list_user_links_pager():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_user_links), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListUserLinksResponse(
                user_links=[
                    resources.UserLink(),
                    resources.UserLink(),
                    resources.UserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(), resources.UserLink(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_user_links(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.UserLink) for i in results)


def test_list_user_links_pages():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_user_links), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListUserLinksResponse(
                user_links=[
                    resources.UserLink(),
                    resources.UserLink(),
                    resources.UserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(), resources.UserLink(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_user_links(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_user_links_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_user_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListUserLinksResponse(
                user_links=[
                    resources.UserLink(),
                    resources.UserLink(),
                    resources.UserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(), resources.UserLink(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_user_links(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.UserLink) for i in responses)


@pytest.mark.asyncio
async def test_list_user_links_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_user_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListUserLinksResponse(
                user_links=[
                    resources.UserLink(),
                    resources.UserLink(),
                    resources.UserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(), resources.UserLink(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_user_links(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_audit_user_links(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.AuditUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.audit_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.AuditUserLinksResponse(
            next_page_token="next_page_token_value",
        )

        response = client.audit_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.AuditUserLinksPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_audit_user_links_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.AuditUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.audit_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.AuditUserLinksResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.audit_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.AuditUserLinksAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_audit_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.AuditUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.audit_user_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.AuditUserLinksResponse()

        client.audit_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_audit_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.AuditUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.audit_user_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.AuditUserLinksResponse()
        )

        await client.audit_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_audit_user_links_pager():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.audit_user_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.AuditUserLinksResponse(
                user_links=[
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(),], next_page_token="ghi",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(), resources.AuditUserLink(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.audit_user_links(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.AuditUserLink) for i in results)


def test_audit_user_links_pages():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.audit_user_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.AuditUserLinksResponse(
                user_links=[
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(),], next_page_token="ghi",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(), resources.AuditUserLink(),],
            ),
            RuntimeError,
        )
        pages = list(client.audit_user_links(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_audit_user_links_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.audit_user_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.AuditUserLinksResponse(
                user_links=[
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(),], next_page_token="ghi",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(), resources.AuditUserLink(),],
            ),
            RuntimeError,
        )
        async_pager = await client.audit_user_links(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.AuditUserLink) for i in responses)


@pytest.mark.asyncio
async def test_audit_user_links_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.audit_user_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.AuditUserLinksResponse(
                user_links=[
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(),], next_page_token="ghi",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(), resources.AuditUserLink(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.audit_user_links(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_create_user_link(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateUserLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink(
            name="name_value",
            email_address="email_address_value",
            direct_roles=["direct_roles_value"],
        )

        response = client.create_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)

    assert response.name == "name_value"

    assert response.email_address == "email_address_value"

    assert response.direct_roles == ["direct_roles_value"]


@pytest.mark.asyncio
async def test_create_user_link_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateUserLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.UserLink(
                name="name_value",
                email_address="email_address_value",
                direct_roles=["direct_roles_value"],
            )
        )

        response = await client.create_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)

    assert response.name == "name_value"

    assert response.email_address == "email_address_value"

    assert response.direct_roles == ["direct_roles_value"]


def test_create_user_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateUserLinkRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_user_link), "__call__"
    ) as call:
        call.return_value = resources.UserLink()

        client.create_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_user_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateUserLinkRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_user_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())

        await client.create_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_user_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_user_link(
            parent="parent_value", user_link=resources.UserLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].user_link == resources.UserLink(name="name_value")


def test_create_user_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_user_link(
            analytics_admin.CreateUserLinkRequest(),
            parent="parent_value",
            user_link=resources.UserLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_user_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_user_link(
            parent="parent_value", user_link=resources.UserLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].user_link == resources.UserLink(name="name_value")


@pytest.mark.asyncio
async def test_create_user_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_user_link(
            analytics_admin.CreateUserLinkRequest(),
            parent="parent_value",
            user_link=resources.UserLink(name="name_value"),
        )


def test_batch_create_user_links(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.BatchCreateUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.BatchCreateUserLinksResponse()

        response = client.batch_create_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchCreateUserLinksResponse)


@pytest.mark.asyncio
async def test_batch_create_user_links_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.BatchCreateUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchCreateUserLinksResponse()
        )

        response = await client.batch_create_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchCreateUserLinksResponse)


def test_batch_create_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchCreateUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_user_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.BatchCreateUserLinksResponse()

        client.batch_create_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_create_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchCreateUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_user_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchCreateUserLinksResponse()
        )

        await client.batch_create_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_update_user_link(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateUserLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink(
            name="name_value",
            email_address="email_address_value",
            direct_roles=["direct_roles_value"],
        )

        response = client.update_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)

    assert response.name == "name_value"

    assert response.email_address == "email_address_value"

    assert response.direct_roles == ["direct_roles_value"]


@pytest.mark.asyncio
async def test_update_user_link_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateUserLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.UserLink(
                name="name_value",
                email_address="email_address_value",
                direct_roles=["direct_roles_value"],
            )
        )

        response = await client.update_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)

    assert response.name == "name_value"

    assert response.email_address == "email_address_value"

    assert response.direct_roles == ["direct_roles_value"]


def test_update_user_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateUserLinkRequest()
    request.user_link.name = "user_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_user_link), "__call__"
    ) as call:
        call.return_value = resources.UserLink()

        client.update_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "user_link.name=user_link.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_user_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateUserLinkRequest()
    request.user_link.name = "user_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_user_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())

        await client.update_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "user_link.name=user_link.name/value",) in kw[
        "metadata"
    ]


def test_update_user_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_user_link(user_link=resources.UserLink(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].user_link == resources.UserLink(name="name_value")


def test_update_user_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_user_link(
            analytics_admin.UpdateUserLinkRequest(),
            user_link=resources.UserLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_user_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_user_link(
            user_link=resources.UserLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].user_link == resources.UserLink(name="name_value")


@pytest.mark.asyncio
async def test_update_user_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_user_link(
            analytics_admin.UpdateUserLinkRequest(),
            user_link=resources.UserLink(name="name_value"),
        )


def test_batch_update_user_links(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.BatchUpdateUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_update_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.BatchUpdateUserLinksResponse()

        response = client.batch_update_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchUpdateUserLinksResponse)


@pytest.mark.asyncio
async def test_batch_update_user_links_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.BatchUpdateUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_update_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchUpdateUserLinksResponse()
        )

        response = await client.batch_update_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchUpdateUserLinksResponse)


def test_batch_update_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchUpdateUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_update_user_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.BatchUpdateUserLinksResponse()

        client.batch_update_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_update_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchUpdateUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_update_user_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchUpdateUserLinksResponse()
        )

        await client.batch_update_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_delete_user_link(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteUserLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_user_link_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteUserLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_user_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteUserLinkRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_user_link), "__call__"
    ) as call:
        call.return_value = None

        client.delete_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_user_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteUserLinkRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_user_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_user_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_user_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_user_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_user_link(
            analytics_admin.DeleteUserLinkRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_user_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_user_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_user_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_user_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_user_link(
            analytics_admin.DeleteUserLinkRequest(), name="name_value",
        )


def test_batch_delete_user_links(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.BatchDeleteUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_delete_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.batch_delete_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_batch_delete_user_links_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.BatchDeleteUserLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_delete_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.batch_delete_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_batch_delete_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchDeleteUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_delete_user_links), "__call__"
    ) as call:
        call.return_value = None

        client.batch_delete_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_delete_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchDeleteUserLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_delete_user_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.batch_delete_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_get_web_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetWebDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream(
            name="name_value",
            measurement_id="measurement_id_value",
            firebase_app_id="firebase_app_id_value",
            default_uri="default_uri_value",
            display_name="display_name_value",
        )

        response = client.get_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)

    assert response.name == "name_value"

    assert response.measurement_id == "measurement_id_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.default_uri == "default_uri_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_web_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetWebDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream(
                name="name_value",
                measurement_id="measurement_id_value",
                firebase_app_id="firebase_app_id_value",
                default_uri="default_uri_value",
                display_name="display_name_value",
            )
        )

        response = await client.get_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)

    assert response.name == "name_value"

    assert response.measurement_id == "measurement_id_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.default_uri == "default_uri_value"

    assert response.display_name == "display_name_value"


def test_get_web_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetWebDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_web_data_stream), "__call__"
    ) as call:
        call.return_value = resources.WebDataStream()

        client.get_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_web_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetWebDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_web_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )

        await client.get_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_web_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_web_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_web_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_web_data_stream(
            analytics_admin.GetWebDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_web_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_web_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_web_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_web_data_stream(
            analytics_admin.GetWebDataStreamRequest(), name="name_value",
        )


def test_delete_web_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteWebDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_web_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteWebDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_web_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteWebDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_web_data_stream), "__call__"
    ) as call:
        call.return_value = None

        client.delete_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_web_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteWebDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_web_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_web_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_web_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_web_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_web_data_stream(
            analytics_admin.DeleteWebDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_web_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_web_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_web_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_web_data_stream(
            analytics_admin.DeleteWebDataStreamRequest(), name="name_value",
        )


def test_update_web_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateWebDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream(
            name="name_value",
            measurement_id="measurement_id_value",
            firebase_app_id="firebase_app_id_value",
            default_uri="default_uri_value",
            display_name="display_name_value",
        )

        response = client.update_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)

    assert response.name == "name_value"

    assert response.measurement_id == "measurement_id_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.default_uri == "default_uri_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_web_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateWebDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream(
                name="name_value",
                measurement_id="measurement_id_value",
                firebase_app_id="firebase_app_id_value",
                default_uri="default_uri_value",
                display_name="display_name_value",
            )
        )

        response = await client.update_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)

    assert response.name == "name_value"

    assert response.measurement_id == "measurement_id_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.default_uri == "default_uri_value"

    assert response.display_name == "display_name_value"


def test_update_web_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateWebDataStreamRequest()
    request.web_data_stream.name = "web_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_web_data_stream), "__call__"
    ) as call:
        call.return_value = resources.WebDataStream()

        client.update_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "web_data_stream.name=web_data_stream.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_web_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateWebDataStreamRequest()
    request.web_data_stream.name = "web_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_web_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )

        await client.update_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "web_data_stream.name=web_data_stream.name/value",
    ) in kw["metadata"]


def test_update_web_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_web_data_stream(
            web_data_stream=resources.WebDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].web_data_stream == resources.WebDataStream(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_web_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_web_data_stream(
            analytics_admin.UpdateWebDataStreamRequest(),
            web_data_stream=resources.WebDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_web_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_web_data_stream(
            web_data_stream=resources.WebDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].web_data_stream == resources.WebDataStream(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_web_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_web_data_stream(
            analytics_admin.UpdateWebDataStreamRequest(),
            web_data_stream=resources.WebDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_create_web_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateWebDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream(
            name="name_value",
            measurement_id="measurement_id_value",
            firebase_app_id="firebase_app_id_value",
            default_uri="default_uri_value",
            display_name="display_name_value",
        )

        response = client.create_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)

    assert response.name == "name_value"

    assert response.measurement_id == "measurement_id_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.default_uri == "default_uri_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_create_web_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateWebDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream(
                name="name_value",
                measurement_id="measurement_id_value",
                firebase_app_id="firebase_app_id_value",
                default_uri="default_uri_value",
                display_name="display_name_value",
            )
        )

        response = await client.create_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)

    assert response.name == "name_value"

    assert response.measurement_id == "measurement_id_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.default_uri == "default_uri_value"

    assert response.display_name == "display_name_value"


def test_create_web_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateWebDataStreamRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_web_data_stream), "__call__"
    ) as call:
        call.return_value = resources.WebDataStream()

        client.create_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_web_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateWebDataStreamRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_web_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )

        await client.create_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_web_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_web_data_stream(
            parent="parent_value",
            web_data_stream=resources.WebDataStream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].web_data_stream == resources.WebDataStream(name="name_value")


def test_create_web_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_web_data_stream(
            analytics_admin.CreateWebDataStreamRequest(),
            parent="parent_value",
            web_data_stream=resources.WebDataStream(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_web_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_web_data_stream(
            parent="parent_value",
            web_data_stream=resources.WebDataStream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].web_data_stream == resources.WebDataStream(name="name_value")


@pytest.mark.asyncio
async def test_create_web_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_web_data_stream(
            analytics_admin.CreateWebDataStreamRequest(),
            parent="parent_value",
            web_data_stream=resources.WebDataStream(name="name_value"),
        )


def test_list_web_data_streams(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListWebDataStreamsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_web_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListWebDataStreamsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_web_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWebDataStreamsPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_web_data_streams_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListWebDataStreamsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_web_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListWebDataStreamsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_web_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWebDataStreamsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_web_data_streams_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListWebDataStreamsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_web_data_streams), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListWebDataStreamsResponse()

        client.list_web_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_web_data_streams_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListWebDataStreamsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_web_data_streams), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListWebDataStreamsResponse()
        )

        await client.list_web_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_web_data_streams_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_web_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListWebDataStreamsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_web_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_web_data_streams_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_web_data_streams(
            analytics_admin.ListWebDataStreamsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_web_data_streams_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_web_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListWebDataStreamsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListWebDataStreamsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_web_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_web_data_streams_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_web_data_streams(
            analytics_admin.ListWebDataStreamsRequest(), parent="parent_value",
        )


def test_list_web_data_streams_pager():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_web_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[resources.WebDataStream(),], next_page_token="ghi",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_web_data_streams(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.WebDataStream) for i in results)


def test_list_web_data_streams_pages():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_web_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[resources.WebDataStream(),], next_page_token="ghi",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_web_data_streams(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_web_data_streams_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_web_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[resources.WebDataStream(),], next_page_token="ghi",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_web_data_streams(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.WebDataStream) for i in responses)


@pytest.mark.asyncio
async def test_list_web_data_streams_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_web_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[resources.WebDataStream(),], next_page_token="ghi",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_web_data_streams(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_ios_app_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetIosAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream(
            name="name_value",
            firebase_app_id="firebase_app_id_value",
            bundle_id="bundle_id_value",
            display_name="display_name_value",
        )

        response = client.get_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IosAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.bundle_id == "bundle_id_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_ios_app_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetIosAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream(
                name="name_value",
                firebase_app_id="firebase_app_id_value",
                bundle_id="bundle_id_value",
                display_name="display_name_value",
            )
        )

        response = await client.get_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IosAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.bundle_id == "bundle_id_value"

    assert response.display_name == "display_name_value"


def test_get_ios_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetIosAppDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = resources.IosAppDataStream()

        client.get_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_ios_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetIosAppDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream()
        )

        await client.get_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_ios_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_ios_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_ios_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_ios_app_data_stream(
            analytics_admin.GetIosAppDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_ios_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_ios_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_ios_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_ios_app_data_stream(
            analytics_admin.GetIosAppDataStreamRequest(), name="name_value",
        )


def test_delete_ios_app_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteIosAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_ios_app_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteIosAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_ios_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteIosAppDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = None

        client.delete_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_ios_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteIosAppDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_ios_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_ios_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_ios_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_ios_app_data_stream(
            analytics_admin.DeleteIosAppDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_ios_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_ios_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_ios_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_ios_app_data_stream(
            analytics_admin.DeleteIosAppDataStreamRequest(), name="name_value",
        )


def test_update_ios_app_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateIosAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream(
            name="name_value",
            firebase_app_id="firebase_app_id_value",
            bundle_id="bundle_id_value",
            display_name="display_name_value",
        )

        response = client.update_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IosAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.bundle_id == "bundle_id_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_ios_app_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateIosAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream(
                name="name_value",
                firebase_app_id="firebase_app_id_value",
                bundle_id="bundle_id_value",
                display_name="display_name_value",
            )
        )

        response = await client.update_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IosAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.bundle_id == "bundle_id_value"

    assert response.display_name == "display_name_value"


def test_update_ios_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateIosAppDataStreamRequest()
    request.ios_app_data_stream.name = "ios_app_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = resources.IosAppDataStream()

        client.update_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "ios_app_data_stream.name=ios_app_data_stream.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_ios_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateIosAppDataStreamRequest()
    request.ios_app_data_stream.name = "ios_app_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream()
        )

        await client.update_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "ios_app_data_stream.name=ios_app_data_stream.name/value",
    ) in kw["metadata"]


def test_update_ios_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_ios_app_data_stream(
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].ios_app_data_stream == resources.IosAppDataStream(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_ios_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_ios_app_data_stream(
            analytics_admin.UpdateIosAppDataStreamRequest(),
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_ios_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_ios_app_data_stream(
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].ios_app_data_stream == resources.IosAppDataStream(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_ios_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_ios_app_data_stream(
            analytics_admin.UpdateIosAppDataStreamRequest(),
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_create_ios_app_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateIosAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream(
            name="name_value",
            firebase_app_id="firebase_app_id_value",
            bundle_id="bundle_id_value",
            display_name="display_name_value",
        )

        response = client.create_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IosAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.bundle_id == "bundle_id_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_create_ios_app_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateIosAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream(
                name="name_value",
                firebase_app_id="firebase_app_id_value",
                bundle_id="bundle_id_value",
                display_name="display_name_value",
            )
        )

        response = await client.create_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IosAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.bundle_id == "bundle_id_value"

    assert response.display_name == "display_name_value"


def test_create_ios_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateIosAppDataStreamRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = resources.IosAppDataStream()

        client.create_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_ios_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateIosAppDataStreamRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream()
        )

        await client.create_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_ios_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_ios_app_data_stream(
            parent="parent_value",
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].ios_app_data_stream == resources.IosAppDataStream(
            name="name_value"
        )


def test_create_ios_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_ios_app_data_stream(
            analytics_admin.CreateIosAppDataStreamRequest(),
            parent="parent_value",
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_ios_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_ios_app_data_stream(
            parent="parent_value",
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].ios_app_data_stream == resources.IosAppDataStream(
            name="name_value"
        )


@pytest.mark.asyncio
async def test_create_ios_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_ios_app_data_stream(
            analytics_admin.CreateIosAppDataStreamRequest(),
            parent="parent_value",
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
        )


def test_list_ios_app_data_streams(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListIosAppDataStreamsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListIosAppDataStreamsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_ios_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListIosAppDataStreamsPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListIosAppDataStreamsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListIosAppDataStreamsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_ios_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListIosAppDataStreamsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_ios_app_data_streams_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListIosAppDataStreamsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_ios_app_data_streams), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListIosAppDataStreamsResponse()

        client.list_ios_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListIosAppDataStreamsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_ios_app_data_streams), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListIosAppDataStreamsResponse()
        )

        await client.list_ios_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_ios_app_data_streams_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListIosAppDataStreamsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_ios_app_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_ios_app_data_streams_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_ios_app_data_streams(
            analytics_admin.ListIosAppDataStreamsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListIosAppDataStreamsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListIosAppDataStreamsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_ios_app_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_ios_app_data_streams(
            analytics_admin.ListIosAppDataStreamsRequest(), parent="parent_value",
        )


def test_list_ios_app_data_streams_pager():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[resources.IosAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_ios_app_data_streams(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.IosAppDataStream) for i in results)


def test_list_ios_app_data_streams_pages():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[resources.IosAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_ios_app_data_streams(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_ios_app_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[resources.IosAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_ios_app_data_streams(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.IosAppDataStream) for i in responses)


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_ios_app_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[resources.IosAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_ios_app_data_streams(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_android_app_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetAndroidAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream(
            name="name_value",
            firebase_app_id="firebase_app_id_value",
            package_name="package_name_value",
            display_name="display_name_value",
        )

        response = client.get_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AndroidAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.package_name == "package_name_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_android_app_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetAndroidAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream(
                name="name_value",
                firebase_app_id="firebase_app_id_value",
                package_name="package_name_value",
                display_name="display_name_value",
            )
        )

        response = await client.get_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AndroidAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.package_name == "package_name_value"

    assert response.display_name == "display_name_value"


def test_get_android_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetAndroidAppDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = resources.AndroidAppDataStream()

        client.get_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_android_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetAndroidAppDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream()
        )

        await client.get_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_android_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_android_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_android_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_android_app_data_stream(
            analytics_admin.GetAndroidAppDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_android_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_android_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_android_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_android_app_data_stream(
            analytics_admin.GetAndroidAppDataStreamRequest(), name="name_value",
        )


def test_delete_android_app_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteAndroidAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_android_app_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteAndroidAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_android_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteAndroidAppDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = None

        client.delete_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_android_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteAndroidAppDataStreamRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_android_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_android_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_android_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_android_app_data_stream(
            analytics_admin.DeleteAndroidAppDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_android_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_android_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_android_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_android_app_data_stream(
            analytics_admin.DeleteAndroidAppDataStreamRequest(), name="name_value",
        )


def test_update_android_app_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateAndroidAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream(
            name="name_value",
            firebase_app_id="firebase_app_id_value",
            package_name="package_name_value",
            display_name="display_name_value",
        )

        response = client.update_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AndroidAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.package_name == "package_name_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_android_app_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateAndroidAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream(
                name="name_value",
                firebase_app_id="firebase_app_id_value",
                package_name="package_name_value",
                display_name="display_name_value",
            )
        )

        response = await client.update_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AndroidAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.package_name == "package_name_value"

    assert response.display_name == "display_name_value"


def test_update_android_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateAndroidAppDataStreamRequest()
    request.android_app_data_stream.name = "android_app_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = resources.AndroidAppDataStream()

        client.update_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "android_app_data_stream.name=android_app_data_stream.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_android_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateAndroidAppDataStreamRequest()
    request.android_app_data_stream.name = "android_app_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream()
        )

        await client.update_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "android_app_data_stream.name=android_app_data_stream.name/value",
    ) in kw["metadata"]


def test_update_android_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_android_app_data_stream(
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].android_app_data_stream == resources.AndroidAppDataStream(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_android_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_android_app_data_stream(
            analytics_admin.UpdateAndroidAppDataStreamRequest(),
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_android_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_android_app_data_stream(
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].android_app_data_stream == resources.AndroidAppDataStream(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_android_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_android_app_data_stream(
            analytics_admin.UpdateAndroidAppDataStreamRequest(),
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_create_android_app_data_stream(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateAndroidAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream(
            name="name_value",
            firebase_app_id="firebase_app_id_value",
            package_name="package_name_value",
            display_name="display_name_value",
        )

        response = client.create_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AndroidAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.package_name == "package_name_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_create_android_app_data_stream_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateAndroidAppDataStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream(
                name="name_value",
                firebase_app_id="firebase_app_id_value",
                package_name="package_name_value",
                display_name="display_name_value",
            )
        )

        response = await client.create_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AndroidAppDataStream)

    assert response.name == "name_value"

    assert response.firebase_app_id == "firebase_app_id_value"

    assert response.package_name == "package_name_value"

    assert response.display_name == "display_name_value"


def test_create_android_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateAndroidAppDataStreamRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = resources.AndroidAppDataStream()

        client.create_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_android_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateAndroidAppDataStreamRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream()
        )

        await client.create_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_android_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_android_app_data_stream(
            parent="parent_value",
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].android_app_data_stream == resources.AndroidAppDataStream(
            name="name_value"
        )


def test_create_android_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_android_app_data_stream(
            analytics_admin.CreateAndroidAppDataStreamRequest(),
            parent="parent_value",
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_android_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_android_app_data_stream(
            parent="parent_value",
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].android_app_data_stream == resources.AndroidAppDataStream(
            name="name_value"
        )


@pytest.mark.asyncio
async def test_create_android_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_android_app_data_stream(
            analytics_admin.CreateAndroidAppDataStreamRequest(),
            parent="parent_value",
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
        )


def test_list_android_app_data_streams(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListAndroidAppDataStreamsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAndroidAppDataStreamsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_android_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAndroidAppDataStreamsPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_android_app_data_streams_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListAndroidAppDataStreamsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAndroidAppDataStreamsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_android_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAndroidAppDataStreamsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_android_app_data_streams_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListAndroidAppDataStreamsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_android_app_data_streams), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListAndroidAppDataStreamsResponse()

        client.list_android_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_android_app_data_streams_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListAndroidAppDataStreamsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_android_app_data_streams), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAndroidAppDataStreamsResponse()
        )

        await client.list_android_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_android_app_data_streams_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAndroidAppDataStreamsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_android_app_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_android_app_data_streams_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_android_app_data_streams(
            analytics_admin.ListAndroidAppDataStreamsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_android_app_data_streams_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAndroidAppDataStreamsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAndroidAppDataStreamsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_android_app_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_android_app_data_streams_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_android_app_data_streams(
            analytics_admin.ListAndroidAppDataStreamsRequest(), parent="parent_value",
        )


def test_list_android_app_data_streams_pager():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[resources.AndroidAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_android_app_data_streams(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.AndroidAppDataStream) for i in results)


def test_list_android_app_data_streams_pages():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[resources.AndroidAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_android_app_data_streams(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_android_app_data_streams_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_android_app_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[resources.AndroidAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_android_app_data_streams(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.AndroidAppDataStream) for i in responses)


@pytest.mark.asyncio
async def test_list_android_app_data_streams_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_android_app_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[resources.AndroidAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (
            await client.list_android_app_data_streams(request={})
        ).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_enhanced_measurement_settings(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetEnhancedMeasurementSettingsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings(
            name="name_value",
            stream_enabled=True,
            page_views_enabled=True,
            scrolls_enabled=True,
            outbound_clicks_enabled=True,
            content_views_enabled=True,
            site_search_enabled=True,
            form_interactions_enabled=True,
            video_engagement_enabled=True,
            file_downloads_enabled=True,
            data_tagged_element_clicks_enabled=True,
            page_loads_enabled=True,
            page_changes_enabled=True,
            articles_and_blogs_enabled=True,
            products_and_ecommerce_enabled=True,
            search_query_parameter="search_query_parameter_value",
            url_query_parameter="url_query_parameter_value",
            excluded_domains="excluded_domains_value",
        )

        response = client.get_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.EnhancedMeasurementSettings)

    assert response.name == "name_value"

    assert response.stream_enabled is True

    assert response.page_views_enabled is True

    assert response.scrolls_enabled is True

    assert response.outbound_clicks_enabled is True

    assert response.content_views_enabled is True

    assert response.site_search_enabled is True

    assert response.form_interactions_enabled is True

    assert response.video_engagement_enabled is True

    assert response.file_downloads_enabled is True

    assert response.data_tagged_element_clicks_enabled is True

    assert response.page_loads_enabled is True

    assert response.page_changes_enabled is True

    assert response.articles_and_blogs_enabled is True

    assert response.products_and_ecommerce_enabled is True

    assert response.search_query_parameter == "search_query_parameter_value"

    assert response.url_query_parameter == "url_query_parameter_value"

    assert response.excluded_domains == "excluded_domains_value"


@pytest.mark.asyncio
async def test_get_enhanced_measurement_settings_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetEnhancedMeasurementSettingsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings(
                name="name_value",
                stream_enabled=True,
                page_views_enabled=True,
                scrolls_enabled=True,
                outbound_clicks_enabled=True,
                content_views_enabled=True,
                site_search_enabled=True,
                form_interactions_enabled=True,
                video_engagement_enabled=True,
                file_downloads_enabled=True,
                data_tagged_element_clicks_enabled=True,
                page_loads_enabled=True,
                page_changes_enabled=True,
                articles_and_blogs_enabled=True,
                products_and_ecommerce_enabled=True,
                search_query_parameter="search_query_parameter_value",
                url_query_parameter="url_query_parameter_value",
                excluded_domains="excluded_domains_value",
            )
        )

        response = await client.get_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.EnhancedMeasurementSettings)

    assert response.name == "name_value"

    assert response.stream_enabled is True

    assert response.page_views_enabled is True

    assert response.scrolls_enabled is True

    assert response.outbound_clicks_enabled is True

    assert response.content_views_enabled is True

    assert response.site_search_enabled is True

    assert response.form_interactions_enabled is True

    assert response.video_engagement_enabled is True

    assert response.file_downloads_enabled is True

    assert response.data_tagged_element_clicks_enabled is True

    assert response.page_loads_enabled is True

    assert response.page_changes_enabled is True

    assert response.articles_and_blogs_enabled is True

    assert response.products_and_ecommerce_enabled is True

    assert response.search_query_parameter == "search_query_parameter_value"

    assert response.url_query_parameter == "url_query_parameter_value"

    assert response.excluded_domains == "excluded_domains_value"


def test_get_enhanced_measurement_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetEnhancedMeasurementSettingsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        call.return_value = resources.EnhancedMeasurementSettings()

        client.get_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_enhanced_measurement_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetEnhancedMeasurementSettingsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings()
        )

        await client.get_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_enhanced_measurement_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_enhanced_measurement_settings(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_enhanced_measurement_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_enhanced_measurement_settings(
            analytics_admin.GetEnhancedMeasurementSettingsRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_enhanced_measurement_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_enhanced_measurement_settings(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_enhanced_measurement_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_enhanced_measurement_settings(
            analytics_admin.GetEnhancedMeasurementSettingsRequest(), name="name_value",
        )


def test_update_enhanced_measurement_settings(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateEnhancedMeasurementSettingsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings(
            name="name_value",
            stream_enabled=True,
            page_views_enabled=True,
            scrolls_enabled=True,
            outbound_clicks_enabled=True,
            content_views_enabled=True,
            site_search_enabled=True,
            form_interactions_enabled=True,
            video_engagement_enabled=True,
            file_downloads_enabled=True,
            data_tagged_element_clicks_enabled=True,
            page_loads_enabled=True,
            page_changes_enabled=True,
            articles_and_blogs_enabled=True,
            products_and_ecommerce_enabled=True,
            search_query_parameter="search_query_parameter_value",
            url_query_parameter="url_query_parameter_value",
            excluded_domains="excluded_domains_value",
        )

        response = client.update_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.EnhancedMeasurementSettings)

    assert response.name == "name_value"

    assert response.stream_enabled is True

    assert response.page_views_enabled is True

    assert response.scrolls_enabled is True

    assert response.outbound_clicks_enabled is True

    assert response.content_views_enabled is True

    assert response.site_search_enabled is True

    assert response.form_interactions_enabled is True

    assert response.video_engagement_enabled is True

    assert response.file_downloads_enabled is True

    assert response.data_tagged_element_clicks_enabled is True

    assert response.page_loads_enabled is True

    assert response.page_changes_enabled is True

    assert response.articles_and_blogs_enabled is True

    assert response.products_and_ecommerce_enabled is True

    assert response.search_query_parameter == "search_query_parameter_value"

    assert response.url_query_parameter == "url_query_parameter_value"

    assert response.excluded_domains == "excluded_domains_value"


@pytest.mark.asyncio
async def test_update_enhanced_measurement_settings_async(
    transport: str = "grpc_asyncio",
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateEnhancedMeasurementSettingsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings(
                name="name_value",
                stream_enabled=True,
                page_views_enabled=True,
                scrolls_enabled=True,
                outbound_clicks_enabled=True,
                content_views_enabled=True,
                site_search_enabled=True,
                form_interactions_enabled=True,
                video_engagement_enabled=True,
                file_downloads_enabled=True,
                data_tagged_element_clicks_enabled=True,
                page_loads_enabled=True,
                page_changes_enabled=True,
                articles_and_blogs_enabled=True,
                products_and_ecommerce_enabled=True,
                search_query_parameter="search_query_parameter_value",
                url_query_parameter="url_query_parameter_value",
                excluded_domains="excluded_domains_value",
            )
        )

        response = await client.update_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.EnhancedMeasurementSettings)

    assert response.name == "name_value"

    assert response.stream_enabled is True

    assert response.page_views_enabled is True

    assert response.scrolls_enabled is True

    assert response.outbound_clicks_enabled is True

    assert response.content_views_enabled is True

    assert response.site_search_enabled is True

    assert response.form_interactions_enabled is True

    assert response.video_engagement_enabled is True

    assert response.file_downloads_enabled is True

    assert response.data_tagged_element_clicks_enabled is True

    assert response.page_loads_enabled is True

    assert response.page_changes_enabled is True

    assert response.articles_and_blogs_enabled is True

    assert response.products_and_ecommerce_enabled is True

    assert response.search_query_parameter == "search_query_parameter_value"

    assert response.url_query_parameter == "url_query_parameter_value"

    assert response.excluded_domains == "excluded_domains_value"


def test_update_enhanced_measurement_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateEnhancedMeasurementSettingsRequest()
    request.enhanced_measurement_settings.name = (
        "enhanced_measurement_settings.name/value"
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        call.return_value = resources.EnhancedMeasurementSettings()

        client.update_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "enhanced_measurement_settings.name=enhanced_measurement_settings.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_enhanced_measurement_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateEnhancedMeasurementSettingsRequest()
    request.enhanced_measurement_settings.name = (
        "enhanced_measurement_settings.name/value"
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings()
        )

        await client.update_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "enhanced_measurement_settings.name=enhanced_measurement_settings.name/value",
    ) in kw["metadata"]


def test_update_enhanced_measurement_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_enhanced_measurement_settings(
            enhanced_measurement_settings=resources.EnhancedMeasurementSettings(
                name="name_value"
            ),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[
            0
        ].enhanced_measurement_settings == resources.EnhancedMeasurementSettings(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_enhanced_measurement_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_enhanced_measurement_settings(
            analytics_admin.UpdateEnhancedMeasurementSettingsRequest(),
            enhanced_measurement_settings=resources.EnhancedMeasurementSettings(
                name="name_value"
            ),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_enhanced_measurement_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_enhanced_measurement_settings(
            enhanced_measurement_settings=resources.EnhancedMeasurementSettings(
                name="name_value"
            ),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[
            0
        ].enhanced_measurement_settings == resources.EnhancedMeasurementSettings(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_enhanced_measurement_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_enhanced_measurement_settings(
            analytics_admin.UpdateEnhancedMeasurementSettingsRequest(),
            enhanced_measurement_settings=resources.EnhancedMeasurementSettings(
                name="name_value"
            ),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_create_firebase_link(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateFirebaseLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink(
            name="name_value",
            project="project_value",
            maximum_user_access=resources.MaximumUserAccess.NO_ACCESS,
        )

        response = client.create_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.FirebaseLink)

    assert response.name == "name_value"

    assert response.project == "project_value"

    assert response.maximum_user_access == resources.MaximumUserAccess.NO_ACCESS


@pytest.mark.asyncio
async def test_create_firebase_link_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateFirebaseLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink(
                name="name_value",
                project="project_value",
                maximum_user_access=resources.MaximumUserAccess.NO_ACCESS,
            )
        )

        response = await client.create_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.FirebaseLink)

    assert response.name == "name_value"

    assert response.project == "project_value"

    assert response.maximum_user_access == resources.MaximumUserAccess.NO_ACCESS


def test_create_firebase_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateFirebaseLinkRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_firebase_link), "__call__"
    ) as call:
        call.return_value = resources.FirebaseLink()

        client.create_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_firebase_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateFirebaseLinkRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_firebase_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink()
        )

        await client.create_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_firebase_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_firebase_link(
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].firebase_link == resources.FirebaseLink(name="name_value")


def test_create_firebase_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_firebase_link(
            analytics_admin.CreateFirebaseLinkRequest(),
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_firebase_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_firebase_link(
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].firebase_link == resources.FirebaseLink(name="name_value")


@pytest.mark.asyncio
async def test_create_firebase_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_firebase_link(
            analytics_admin.CreateFirebaseLinkRequest(),
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )


def test_update_firebase_link(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateFirebaseLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink(
            name="name_value",
            project="project_value",
            maximum_user_access=resources.MaximumUserAccess.NO_ACCESS,
        )

        response = client.update_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.FirebaseLink)

    assert response.name == "name_value"

    assert response.project == "project_value"

    assert response.maximum_user_access == resources.MaximumUserAccess.NO_ACCESS


@pytest.mark.asyncio
async def test_update_firebase_link_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateFirebaseLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink(
                name="name_value",
                project="project_value",
                maximum_user_access=resources.MaximumUserAccess.NO_ACCESS,
            )
        )

        response = await client.update_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.FirebaseLink)

    assert response.name == "name_value"

    assert response.project == "project_value"

    assert response.maximum_user_access == resources.MaximumUserAccess.NO_ACCESS


def test_update_firebase_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateFirebaseLinkRequest()
    request.firebase_link.name = "firebase_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_firebase_link), "__call__"
    ) as call:
        call.return_value = resources.FirebaseLink()

        client.update_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "firebase_link.name=firebase_link.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_firebase_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateFirebaseLinkRequest()
    request.firebase_link.name = "firebase_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_firebase_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink()
        )

        await client.update_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "firebase_link.name=firebase_link.name/value",
    ) in kw["metadata"]


def test_update_firebase_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_firebase_link(
            firebase_link=resources.FirebaseLink(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].firebase_link == resources.FirebaseLink(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_firebase_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_firebase_link(
            analytics_admin.UpdateFirebaseLinkRequest(),
            firebase_link=resources.FirebaseLink(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_firebase_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_firebase_link(
            firebase_link=resources.FirebaseLink(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].firebase_link == resources.FirebaseLink(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_firebase_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_firebase_link(
            analytics_admin.UpdateFirebaseLinkRequest(),
            firebase_link=resources.FirebaseLink(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_firebase_link(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteFirebaseLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_firebase_link_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteFirebaseLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_firebase_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteFirebaseLinkRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_firebase_link), "__call__"
    ) as call:
        call.return_value = None

        client.delete_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_firebase_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteFirebaseLinkRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_firebase_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_firebase_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_firebase_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_firebase_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_firebase_link(
            analytics_admin.DeleteFirebaseLinkRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_firebase_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_firebase_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_firebase_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_firebase_link(
            analytics_admin.DeleteFirebaseLinkRequest(), name="name_value",
        )


def test_list_firebase_links(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListFirebaseLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListFirebaseLinksResponse()

        response = client.list_firebase_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.ListFirebaseLinksResponse)


@pytest.mark.asyncio
async def test_list_firebase_links_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListFirebaseLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListFirebaseLinksResponse()
        )

        response = await client.list_firebase_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.ListFirebaseLinksResponse)


def test_list_firebase_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListFirebaseLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_firebase_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListFirebaseLinksResponse()

        client.list_firebase_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_firebase_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListFirebaseLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_firebase_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListFirebaseLinksResponse()
        )

        await client.list_firebase_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_firebase_links_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListFirebaseLinksResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_firebase_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_firebase_links_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_firebase_links(
            analytics_admin.ListFirebaseLinksRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_firebase_links_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListFirebaseLinksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListFirebaseLinksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_firebase_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_firebase_links_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_firebase_links(
            analytics_admin.ListFirebaseLinksRequest(), parent="parent_value",
        )


def test_get_global_site_tag(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetGlobalSiteTagRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_global_site_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GlobalSiteTag(snippet="snippet_value",)

        response = client.get_global_site_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GlobalSiteTag)

    assert response.snippet == "snippet_value"


@pytest.mark.asyncio
async def test_get_global_site_tag_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetGlobalSiteTagRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_global_site_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GlobalSiteTag(snippet="snippet_value",)
        )

        response = await client.get_global_site_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GlobalSiteTag)

    assert response.snippet == "snippet_value"


def test_get_global_site_tag_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetGlobalSiteTagRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_global_site_tag), "__call__"
    ) as call:
        call.return_value = resources.GlobalSiteTag()

        client.get_global_site_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_global_site_tag_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetGlobalSiteTagRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_global_site_tag), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GlobalSiteTag()
        )

        await client.get_global_site_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_global_site_tag_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_global_site_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GlobalSiteTag()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_global_site_tag(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_global_site_tag_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_global_site_tag(
            analytics_admin.GetGlobalSiteTagRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_global_site_tag_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_global_site_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GlobalSiteTag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GlobalSiteTag()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_global_site_tag(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_global_site_tag_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_global_site_tag(
            analytics_admin.GetGlobalSiteTagRequest(), name="name_value",
        )


def test_create_google_ads_link(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateGoogleAdsLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink(
            name="name_value",
            parent="parent_value",
            customer_id="customer_id_value",
            can_manage_clients=True,
            email_address="email_address_value",
        )

        response = client.create_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)

    assert response.name == "name_value"

    assert response.parent == "parent_value"

    assert response.customer_id == "customer_id_value"

    assert response.can_manage_clients is True

    assert response.email_address == "email_address_value"


@pytest.mark.asyncio
async def test_create_google_ads_link_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.CreateGoogleAdsLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink(
                name="name_value",
                parent="parent_value",
                customer_id="customer_id_value",
                can_manage_clients=True,
                email_address="email_address_value",
            )
        )

        response = await client.create_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)

    assert response.name == "name_value"

    assert response.parent == "parent_value"

    assert response.customer_id == "customer_id_value"

    assert response.can_manage_clients is True

    assert response.email_address == "email_address_value"


def test_create_google_ads_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateGoogleAdsLinkRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_google_ads_link), "__call__"
    ) as call:
        call.return_value = resources.GoogleAdsLink()

        client.create_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_google_ads_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateGoogleAdsLinkRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_google_ads_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )

        await client.create_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_google_ads_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_google_ads_link(
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].google_ads_link == resources.GoogleAdsLink(name="name_value")


def test_create_google_ads_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_google_ads_link(
            analytics_admin.CreateGoogleAdsLinkRequest(),
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_google_ads_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_google_ads_link(
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].google_ads_link == resources.GoogleAdsLink(name="name_value")


@pytest.mark.asyncio
async def test_create_google_ads_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_google_ads_link(
            analytics_admin.CreateGoogleAdsLinkRequest(),
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )


def test_update_google_ads_link(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateGoogleAdsLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink(
            name="name_value",
            parent="parent_value",
            customer_id="customer_id_value",
            can_manage_clients=True,
            email_address="email_address_value",
        )

        response = client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)

    assert response.name == "name_value"

    assert response.parent == "parent_value"

    assert response.customer_id == "customer_id_value"

    assert response.can_manage_clients is True

    assert response.email_address == "email_address_value"


@pytest.mark.asyncio
async def test_update_google_ads_link_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.UpdateGoogleAdsLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink(
                name="name_value",
                parent="parent_value",
                customer_id="customer_id_value",
                can_manage_clients=True,
                email_address="email_address_value",
            )
        )

        response = await client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)

    assert response.name == "name_value"

    assert response.parent == "parent_value"

    assert response.customer_id == "customer_id_value"

    assert response.can_manage_clients is True

    assert response.email_address == "email_address_value"


def test_update_google_ads_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateGoogleAdsLinkRequest()
    request.google_ads_link.name = "google_ads_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_google_ads_link), "__call__"
    ) as call:
        call.return_value = resources.GoogleAdsLink()

        client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "google_ads_link.name=google_ads_link.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_google_ads_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateGoogleAdsLinkRequest()
    request.google_ads_link.name = "google_ads_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_google_ads_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )

        await client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "google_ads_link.name=google_ads_link.name/value",
    ) in kw["metadata"]


def test_update_google_ads_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_google_ads_link(
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].google_ads_link == resources.GoogleAdsLink(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_google_ads_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_google_ads_link(
            analytics_admin.UpdateGoogleAdsLinkRequest(),
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_google_ads_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_google_ads_link(
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].google_ads_link == resources.GoogleAdsLink(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_google_ads_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_google_ads_link(
            analytics_admin.UpdateGoogleAdsLinkRequest(),
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_google_ads_link(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteGoogleAdsLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_google_ads_link_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.DeleteGoogleAdsLinkRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_google_ads_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteGoogleAdsLinkRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_google_ads_link), "__call__"
    ) as call:
        call.return_value = None

        client.delete_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_google_ads_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteGoogleAdsLinkRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_google_ads_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_google_ads_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_google_ads_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_google_ads_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_google_ads_link(
            analytics_admin.DeleteGoogleAdsLinkRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_google_ads_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_google_ads_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_google_ads_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_google_ads_link(
            analytics_admin.DeleteGoogleAdsLinkRequest(), name="name_value",
        )


def test_list_google_ads_links(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListGoogleAdsLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_google_ads_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGoogleAdsLinksPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_google_ads_links_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.ListGoogleAdsLinksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListGoogleAdsLinksResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_google_ads_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGoogleAdsLinksAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_google_ads_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListGoogleAdsLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_google_ads_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse()

        client.list_google_ads_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_google_ads_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListGoogleAdsLinksRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_google_ads_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListGoogleAdsLinksResponse()
        )

        await client.list_google_ads_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_google_ads_links_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_google_ads_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_google_ads_links_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_google_ads_links(
            analytics_admin.ListGoogleAdsLinksRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_google_ads_links_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListGoogleAdsLinksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_google_ads_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_google_ads_links_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_google_ads_links(
            analytics_admin.ListGoogleAdsLinksRequest(), parent="parent_value",
        )


def test_list_google_ads_links_pager():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_google_ads_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[], next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[resources.GoogleAdsLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_google_ads_links(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.GoogleAdsLink) for i in results)


def test_list_google_ads_links_pages():
    client = AnalyticsAdminServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_google_ads_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[], next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[resources.GoogleAdsLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_google_ads_links(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_google_ads_links_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_google_ads_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[], next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[resources.GoogleAdsLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_google_ads_links(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.GoogleAdsLink) for i in responses)


@pytest.mark.asyncio
async def test_list_google_ads_links_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_google_ads_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[], next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[resources.GoogleAdsLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_google_ads_links(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_data_sharing_settings(transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetDataSharingSettingsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataSharingSettings(
            name="name_value",
            sharing_with_google_support_enabled=True,
            sharing_with_google_assigned_sales_enabled=True,
            sharing_with_google_any_sales_enabled=True,
            sharing_with_google_products_enabled=True,
            sharing_with_others_enabled=True,
        )

        response = client.get_data_sharing_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataSharingSettings)

    assert response.name == "name_value"

    assert response.sharing_with_google_support_enabled is True

    assert response.sharing_with_google_assigned_sales_enabled is True

    assert response.sharing_with_google_any_sales_enabled is True

    assert response.sharing_with_google_products_enabled is True

    assert response.sharing_with_others_enabled is True


@pytest.mark.asyncio
async def test_get_data_sharing_settings_async(transport: str = "grpc_asyncio"):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = analytics_admin.GetDataSharingSettingsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataSharingSettings(
                name="name_value",
                sharing_with_google_support_enabled=True,
                sharing_with_google_assigned_sales_enabled=True,
                sharing_with_google_any_sales_enabled=True,
                sharing_with_google_products_enabled=True,
                sharing_with_others_enabled=True,
            )
        )

        response = await client.get_data_sharing_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataSharingSettings)

    assert response.name == "name_value"

    assert response.sharing_with_google_support_enabled is True

    assert response.sharing_with_google_assigned_sales_enabled is True

    assert response.sharing_with_google_any_sales_enabled is True

    assert response.sharing_with_google_products_enabled is True

    assert response.sharing_with_others_enabled is True


def test_get_data_sharing_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetDataSharingSettingsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_data_sharing_settings), "__call__"
    ) as call:
        call.return_value = resources.DataSharingSettings()

        client.get_data_sharing_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_data_sharing_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetDataSharingSettingsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_data_sharing_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataSharingSettings()
        )

        await client.get_data_sharing_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_data_sharing_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataSharingSettings()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_data_sharing_settings(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_data_sharing_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_data_sharing_settings(
            analytics_admin.GetDataSharingSettingsRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_data_sharing_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataSharingSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataSharingSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_data_sharing_settings(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_data_sharing_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_data_sharing_settings(
            analytics_admin.GetDataSharingSettingsRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = AnalyticsAdminServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AnalyticsAdminServiceGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )
    assert isinstance(client._transport, transports.AnalyticsAdminServiceGrpcTransport,)


def test_analytics_admin_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.AnalyticsAdminServiceTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_analytics_admin_service_base_transport():
    # Instantiate the base transport.
    transport = transports.AnalyticsAdminServiceTransport(
        credentials=credentials.AnonymousCredentials(),
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_account",
        "list_accounts",
        "delete_account",
        "update_account",
        "provision_account_ticket",
        "get_property",
        "list_properties",
        "create_property",
        "delete_property",
        "update_property",
        "get_user_link",
        "batch_get_user_links",
        "list_user_links",
        "audit_user_links",
        "create_user_link",
        "batch_create_user_links",
        "update_user_link",
        "batch_update_user_links",
        "delete_user_link",
        "batch_delete_user_links",
        "get_web_data_stream",
        "delete_web_data_stream",
        "update_web_data_stream",
        "create_web_data_stream",
        "list_web_data_streams",
        "get_ios_app_data_stream",
        "delete_ios_app_data_stream",
        "update_ios_app_data_stream",
        "create_ios_app_data_stream",
        "list_ios_app_data_streams",
        "get_android_app_data_stream",
        "delete_android_app_data_stream",
        "update_android_app_data_stream",
        "create_android_app_data_stream",
        "list_android_app_data_streams",
        "get_enhanced_measurement_settings",
        "update_enhanced_measurement_settings",
        "create_firebase_link",
        "update_firebase_link",
        "delete_firebase_link",
        "list_firebase_links",
        "get_global_site_tag",
        "create_google_ads_link",
        "update_google_ads_link",
        "delete_google_ads_link",
        "list_google_ads_links",
        "get_data_sharing_settings",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_analytics_admin_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(auth, "load_credentials_from_file") as load_creds:
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.AnalyticsAdminServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


def test_analytics_admin_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        AnalyticsAdminServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id=None,
        )


def test_analytics_admin_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.AnalyticsAdminServiceGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


def test_analytics_admin_service_host_no_port():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticsadmin.googleapis.com"
        ),
    )
    assert client._transport._host == "analyticsadmin.googleapis.com:443"


def test_analytics_admin_service_host_with_port():
    client = AnalyticsAdminServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticsadmin.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "analyticsadmin.googleapis.com:8000"


def test_analytics_admin_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_analytics_admin_service_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.AnalyticsAdminServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_analytics_admin_service_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.AnalyticsAdminServiceGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=(
            "https://www.googleapis.com/auth/analytics.edit",
            "https://www.googleapis.com/auth/analytics.manage.users",
            "https://www.googleapis.com/auth/analytics.manage.users.readonly",
            "https://www.googleapis.com/auth/analytics.readonly",
        ),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_analytics_admin_service_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.AnalyticsAdminServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=(
            "https://www.googleapis.com/auth/analytics.edit",
            "https://www.googleapis.com/auth/analytics.manage.users",
            "https://www.googleapis.com/auth/analytics.manage.users.readonly",
            "https://www.googleapis.com/auth/analytics.readonly",
        ),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_analytics_admin_service_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.AnalyticsAdminServiceGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_analytics_admin_service_grpc_asyncio_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.AnalyticsAdminServiceGrpcAsyncIOTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_android_app_data_stream_path():
    property = "squid"
    android_app_data_stream = "clam"

    expected = "properties/{property}/androidAppDataStreams/{android_app_data_stream}".format(
        property=property, android_app_data_stream=android_app_data_stream,
    )
    actual = AnalyticsAdminServiceClient.android_app_data_stream_path(
        property, android_app_data_stream
    )
    assert expected == actual


def test_parse_android_app_data_stream_path():
    expected = {
        "property": "whelk",
        "android_app_data_stream": "octopus",
    }
    path = AnalyticsAdminServiceClient.android_app_data_stream_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_android_app_data_stream_path(path)
    assert expected == actual


def test_property_path():
    property = "squid"

    expected = "properties/{property}".format(property=property,)
    actual = AnalyticsAdminServiceClient.property_path(property)
    assert expected == actual


def test_parse_property_path():
    expected = {
        "property": "clam",
    }
    path = AnalyticsAdminServiceClient.property_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_property_path(path)
    assert expected == actual


def test_user_link_path():
    account = "squid"
    user_link = "clam"

    expected = "accounts/{account}/userLinks/{user_link}".format(
        account=account, user_link=user_link,
    )
    actual = AnalyticsAdminServiceClient.user_link_path(account, user_link)
    assert expected == actual


def test_parse_user_link_path():
    expected = {
        "account": "whelk",
        "user_link": "octopus",
    }
    path = AnalyticsAdminServiceClient.user_link_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_user_link_path(path)
    assert expected == actual


def test_enhanced_measurement_settings_path():
    property = "squid"
    web_data_stream = "clam"

    expected = "properties/{property}/webDataStreams/{web_data_stream}/enhancedMeasurementSettings".format(
        property=property, web_data_stream=web_data_stream,
    )
    actual = AnalyticsAdminServiceClient.enhanced_measurement_settings_path(
        property, web_data_stream
    )
    assert expected == actual


def test_parse_enhanced_measurement_settings_path():
    expected = {
        "property": "whelk",
        "web_data_stream": "octopus",
    }
    path = AnalyticsAdminServiceClient.enhanced_measurement_settings_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_enhanced_measurement_settings_path(path)
    assert expected == actual


def test_google_ads_link_path():
    property = "squid"
    google_ads_link = "clam"

    expected = "properties/{property}/googleAdsLinks/{google_ads_link}".format(
        property=property, google_ads_link=google_ads_link,
    )
    actual = AnalyticsAdminServiceClient.google_ads_link_path(property, google_ads_link)
    assert expected == actual


def test_parse_google_ads_link_path():
    expected = {
        "property": "whelk",
        "google_ads_link": "octopus",
    }
    path = AnalyticsAdminServiceClient.google_ads_link_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_google_ads_link_path(path)
    assert expected == actual


def test_firebase_link_path():
    property = "squid"
    firebase_link = "clam"

    expected = "properties/{property}/firebaseLinks/{firebase_link}".format(
        property=property, firebase_link=firebase_link,
    )
    actual = AnalyticsAdminServiceClient.firebase_link_path(property, firebase_link)
    assert expected == actual


def test_parse_firebase_link_path():
    expected = {
        "property": "whelk",
        "firebase_link": "octopus",
    }
    path = AnalyticsAdminServiceClient.firebase_link_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_firebase_link_path(path)
    assert expected == actual


def test_web_data_stream_path():
    property = "squid"
    web_data_stream = "clam"

    expected = "properties/{property}/webDataStreams/{web_data_stream}".format(
        property=property, web_data_stream=web_data_stream,
    )
    actual = AnalyticsAdminServiceClient.web_data_stream_path(property, web_data_stream)
    assert expected == actual


def test_parse_web_data_stream_path():
    expected = {
        "property": "whelk",
        "web_data_stream": "octopus",
    }
    path = AnalyticsAdminServiceClient.web_data_stream_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_web_data_stream_path(path)
    assert expected == actual


def test_ios_app_data_stream_path():
    property = "squid"
    ios_app_data_stream = "clam"

    expected = "properties/{property}/iosAppDataStreams/{ios_app_data_stream}".format(
        property=property, ios_app_data_stream=ios_app_data_stream,
    )
    actual = AnalyticsAdminServiceClient.ios_app_data_stream_path(
        property, ios_app_data_stream
    )
    assert expected == actual


def test_parse_ios_app_data_stream_path():
    expected = {
        "property": "whelk",
        "ios_app_data_stream": "octopus",
    }
    path = AnalyticsAdminServiceClient.ios_app_data_stream_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_ios_app_data_stream_path(path)
    assert expected == actual


def test_account_path():
    account = "squid"

    expected = "accounts/{account}".format(account=account,)
    actual = AnalyticsAdminServiceClient.account_path(account)
    assert expected == actual


def test_parse_account_path():
    expected = {
        "account": "clam",
    }
    path = AnalyticsAdminServiceClient.account_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_account_path(path)
    assert expected == actual
