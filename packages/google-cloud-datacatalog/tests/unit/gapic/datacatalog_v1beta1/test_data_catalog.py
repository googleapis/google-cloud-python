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
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.datacatalog_v1beta1.services.data_catalog import (
    DataCatalogAsyncClient,
)
from google.cloud.datacatalog_v1beta1.services.data_catalog import DataCatalogClient
from google.cloud.datacatalog_v1beta1.services.data_catalog import pagers
from google.cloud.datacatalog_v1beta1.services.data_catalog import transports
from google.cloud.datacatalog_v1beta1.types import common
from google.cloud.datacatalog_v1beta1.types import datacatalog
from google.cloud.datacatalog_v1beta1.types import gcs_fileset_spec
from google.cloud.datacatalog_v1beta1.types import schema
from google.cloud.datacatalog_v1beta1.types import search
from google.cloud.datacatalog_v1beta1.types import table_spec
from google.cloud.datacatalog_v1beta1.types import tags
from google.cloud.datacatalog_v1beta1.types import timestamps
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import options_pb2 as options  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.type import expr_pb2 as expr  # type: ignore


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

    assert DataCatalogClient._get_default_mtls_endpoint(None) is None
    assert (
        DataCatalogClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        DataCatalogClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataCatalogClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataCatalogClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert DataCatalogClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [DataCatalogClient, DataCatalogAsyncClient])
def test_data_catalog_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "datacatalog.googleapis.com:443"


def test_data_catalog_client_get_transport_class():
    transport = DataCatalogClient.get_transport_class()
    assert transport == transports.DataCatalogGrpcTransport

    transport = DataCatalogClient.get_transport_class("grpc")
    assert transport == transports.DataCatalogGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc"),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    DataCatalogClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DataCatalogClient)
)
@mock.patch.object(
    DataCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataCatalogAsyncClient),
)
def test_data_catalog_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DataCatalogClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DataCatalogClient, "get_transport_class") as gtc:
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
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc", "true"),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc", "false"),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    DataCatalogClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DataCatalogClient)
)
@mock.patch.object(
    DataCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataCatalogAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_data_catalog_client_mtls_env_auto(
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
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc"),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_data_catalog_client_client_options_scopes(
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
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc"),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_data_catalog_client_client_options_credentials_file(
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


def test_data_catalog_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.datacatalog_v1beta1.services.data_catalog.transports.DataCatalogGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DataCatalogClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_search_catalog(
    transport: str = "grpc", request_type=datacatalog.SearchCatalogRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.SearchCatalogResponse(
            next_page_token="next_page_token_value",
        )

        response = client.search_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.SearchCatalogRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.SearchCatalogPager)

    assert response.next_page_token == "next_page_token_value"


def test_search_catalog_from_dict():
    test_search_catalog(request_type=dict)


@pytest.mark.asyncio
async def test_search_catalog_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.SearchCatalogRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.SearchCatalogResponse(next_page_token="next_page_token_value",)
        )

        response = await client.search_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.SearchCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchCatalogAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_catalog_async_from_dict():
    await test_search_catalog_async(request_type=dict)


def test_search_catalog_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.SearchCatalogResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_catalog(
            scope=datacatalog.SearchCatalogRequest.Scope(
                include_org_ids=["include_org_ids_value"]
            ),
            query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].scope == datacatalog.SearchCatalogRequest.Scope(
            include_org_ids=["include_org_ids_value"]
        )

        assert args[0].query == "query_value"


def test_search_catalog_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_catalog(
            datacatalog.SearchCatalogRequest(),
            scope=datacatalog.SearchCatalogRequest.Scope(
                include_org_ids=["include_org_ids_value"]
            ),
            query="query_value",
        )


@pytest.mark.asyncio
async def test_search_catalog_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.SearchCatalogResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.SearchCatalogResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_catalog(
            scope=datacatalog.SearchCatalogRequest.Scope(
                include_org_ids=["include_org_ids_value"]
            ),
            query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].scope == datacatalog.SearchCatalogRequest.Scope(
            include_org_ids=["include_org_ids_value"]
        )

        assert args[0].query == "query_value"


@pytest.mark.asyncio
async def test_search_catalog_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_catalog(
            datacatalog.SearchCatalogRequest(),
            scope=datacatalog.SearchCatalogRequest.Scope(
                include_org_ids=["include_org_ids_value"]
            ),
            query="query_value",
        )


def test_search_catalog_pager():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
                next_page_token="abc",
            ),
            datacatalog.SearchCatalogResponse(results=[], next_page_token="def",),
            datacatalog.SearchCatalogResponse(
                results=[search.SearchCatalogResult(),], next_page_token="ghi",
            ),
            datacatalog.SearchCatalogResponse(
                results=[search.SearchCatalogResult(), search.SearchCatalogResult(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.search_catalog(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, search.SearchCatalogResult) for i in results)


def test_search_catalog_pages():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
                next_page_token="abc",
            ),
            datacatalog.SearchCatalogResponse(results=[], next_page_token="def",),
            datacatalog.SearchCatalogResponse(
                results=[search.SearchCatalogResult(),], next_page_token="ghi",
            ),
            datacatalog.SearchCatalogResponse(
                results=[search.SearchCatalogResult(), search.SearchCatalogResult(),],
            ),
            RuntimeError,
        )
        pages = list(client.search_catalog(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_catalog_async_pager():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_catalog), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
                next_page_token="abc",
            ),
            datacatalog.SearchCatalogResponse(results=[], next_page_token="def",),
            datacatalog.SearchCatalogResponse(
                results=[search.SearchCatalogResult(),], next_page_token="ghi",
            ),
            datacatalog.SearchCatalogResponse(
                results=[search.SearchCatalogResult(), search.SearchCatalogResult(),],
            ),
            RuntimeError,
        )
        async_pager = await client.search_catalog(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, search.SearchCatalogResult) for i in responses)


@pytest.mark.asyncio
async def test_search_catalog_async_pages():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_catalog), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
                next_page_token="abc",
            ),
            datacatalog.SearchCatalogResponse(results=[], next_page_token="def",),
            datacatalog.SearchCatalogResponse(
                results=[search.SearchCatalogResult(),], next_page_token="ghi",
            ),
            datacatalog.SearchCatalogResponse(
                results=[search.SearchCatalogResult(), search.SearchCatalogResult(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.search_catalog(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_entry_group(
    transport: str = "grpc", request_type=datacatalog.CreateEntryGroupRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )

        response = client.create_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.CreateEntryGroupRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datacatalog.EntryGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


def test_create_entry_group_from_dict():
    test_create_entry_group(request_type=dict)


@pytest.mark.asyncio
async def test_create_entry_group_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.CreateEntryGroupRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )

        response = await client.create_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.CreateEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_create_entry_group_async_from_dict():
    await test_create_entry_group_async(request_type=dict)


def test_create_entry_group_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateEntryGroupRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        call.return_value = datacatalog.EntryGroup()

        client.create_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_entry_group_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateEntryGroupRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )

        await client.create_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_entry_group_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_entry_group(
            parent="parent_value",
            entry_group_id="entry_group_id_value",
            entry_group=datacatalog.EntryGroup(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].entry_group_id == "entry_group_id_value"

        assert args[0].entry_group == datacatalog.EntryGroup(name="name_value")


def test_create_entry_group_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_entry_group(
            datacatalog.CreateEntryGroupRequest(),
            parent="parent_value",
            entry_group_id="entry_group_id_value",
            entry_group=datacatalog.EntryGroup(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_entry_group_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_entry_group(
            parent="parent_value",
            entry_group_id="entry_group_id_value",
            entry_group=datacatalog.EntryGroup(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].entry_group_id == "entry_group_id_value"

        assert args[0].entry_group == datacatalog.EntryGroup(name="name_value")


@pytest.mark.asyncio
async def test_create_entry_group_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_entry_group(
            datacatalog.CreateEntryGroupRequest(),
            parent="parent_value",
            entry_group_id="entry_group_id_value",
            entry_group=datacatalog.EntryGroup(name="name_value"),
        )


def test_update_entry_group(
    transport: str = "grpc", request_type=datacatalog.UpdateEntryGroupRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )

        response = client.update_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.UpdateEntryGroupRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datacatalog.EntryGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


def test_update_entry_group_from_dict():
    test_update_entry_group(request_type=dict)


@pytest.mark.asyncio
async def test_update_entry_group_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.UpdateEntryGroupRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )

        response = await client.update_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.UpdateEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_update_entry_group_async_from_dict():
    await test_update_entry_group_async(request_type=dict)


def test_update_entry_group_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateEntryGroupRequest()
    request.entry_group.name = "entry_group.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        call.return_value = datacatalog.EntryGroup()

        client.update_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "entry_group.name=entry_group.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_entry_group_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateEntryGroupRequest()
    request.entry_group.name = "entry_group.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )

        await client.update_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "entry_group.name=entry_group.name/value",) in kw[
        "metadata"
    ]


def test_update_entry_group_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_entry_group(
            entry_group=datacatalog.EntryGroup(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].entry_group == datacatalog.EntryGroup(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_entry_group_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_entry_group(
            datacatalog.UpdateEntryGroupRequest(),
            entry_group=datacatalog.EntryGroup(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_entry_group_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_entry_group(
            entry_group=datacatalog.EntryGroup(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].entry_group == datacatalog.EntryGroup(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_entry_group_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_entry_group(
            datacatalog.UpdateEntryGroupRequest(),
            entry_group=datacatalog.EntryGroup(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_get_entry_group(
    transport: str = "grpc", request_type=datacatalog.GetEntryGroupRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )

        response = client.get_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.GetEntryGroupRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datacatalog.EntryGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


def test_get_entry_group_from_dict():
    test_get_entry_group(request_type=dict)


@pytest.mark.asyncio
async def test_get_entry_group_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.GetEntryGroupRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )

        response = await client.get_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.GetEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_entry_group_async_from_dict():
    await test_get_entry_group_async(request_type=dict)


def test_get_entry_group_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetEntryGroupRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        call.return_value = datacatalog.EntryGroup()

        client.get_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_entry_group_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetEntryGroupRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )

        await client.get_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_entry_group_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_entry_group(
            name="name_value", read_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].read_mask == field_mask.FieldMask(paths=["paths_value"])


def test_get_entry_group_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_entry_group(
            datacatalog.GetEntryGroupRequest(),
            name="name_value",
            read_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_get_entry_group_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_entry_group(
            name="name_value", read_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].read_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_get_entry_group_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_entry_group(
            datacatalog.GetEntryGroupRequest(),
            name="name_value",
            read_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_entry_group(
    transport: str = "grpc", request_type=datacatalog.DeleteEntryGroupRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.DeleteEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_entry_group_from_dict():
    test_delete_entry_group(request_type=dict)


@pytest.mark.asyncio
async def test_delete_entry_group_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.DeleteEntryGroupRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.DeleteEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_entry_group_async_from_dict():
    await test_delete_entry_group_async(request_type=dict)


def test_delete_entry_group_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteEntryGroupRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        call.return_value = None

        client.delete_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_entry_group_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteEntryGroupRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_entry_group_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_entry_group(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_entry_group_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_entry_group(
            datacatalog.DeleteEntryGroupRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_entry_group_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_entry_group(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_entry_group_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_entry_group(
            datacatalog.DeleteEntryGroupRequest(), name="name_value",
        )


def test_list_entry_groups(
    transport: str = "grpc", request_type=datacatalog.ListEntryGroupsRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntryGroupsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_entry_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.ListEntryGroupsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListEntryGroupsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_entry_groups_from_dict():
    test_list_entry_groups(request_type=dict)


@pytest.mark.asyncio
async def test_list_entry_groups_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.ListEntryGroupsRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntryGroupsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_entry_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.ListEntryGroupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntryGroupsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_entry_groups_async_from_dict():
    await test_list_entry_groups_async(request_type=dict)


def test_list_entry_groups_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListEntryGroupsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        call.return_value = datacatalog.ListEntryGroupsResponse()

        client.list_entry_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_entry_groups_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListEntryGroupsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntryGroupsResponse()
        )

        await client.list_entry_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_entry_groups_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntryGroupsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_entry_groups(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_entry_groups_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_entry_groups(
            datacatalog.ListEntryGroupsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_entry_groups_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntryGroupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntryGroupsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_entry_groups(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_entry_groups_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_entry_groups(
            datacatalog.ListEntryGroupsRequest(), parent="parent_value",
        )


def test_list_entry_groups_pager():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[], next_page_token="def",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[datacatalog.EntryGroup(),], next_page_token="ghi",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[datacatalog.EntryGroup(), datacatalog.EntryGroup(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_entry_groups(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, datacatalog.EntryGroup) for i in results)


def test_list_entry_groups_pages():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[], next_page_token="def",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[datacatalog.EntryGroup(),], next_page_token="ghi",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[datacatalog.EntryGroup(), datacatalog.EntryGroup(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_entry_groups(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_entry_groups_async_pager():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[], next_page_token="def",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[datacatalog.EntryGroup(),], next_page_token="ghi",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[datacatalog.EntryGroup(), datacatalog.EntryGroup(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_entry_groups(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, datacatalog.EntryGroup) for i in responses)


@pytest.mark.asyncio
async def test_list_entry_groups_async_pages():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[], next_page_token="def",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[datacatalog.EntryGroup(),], next_page_token="ghi",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[datacatalog.EntryGroup(), datacatalog.EntryGroup(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_entry_groups(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_entry(
    transport: str = "grpc", request_type=datacatalog.CreateEntryRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry(
            name="name_value",
            linked_resource="linked_resource_value",
            display_name="display_name_value",
            description="description_value",
            type_=datacatalog.EntryType.TABLE,
            integrated_system=common.IntegratedSystem.BIGQUERY,
            gcs_fileset_spec=gcs_fileset_spec.GcsFilesetSpec(
                file_patterns=["file_patterns_value"]
            ),
        )

        response = client.create_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.CreateEntryRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datacatalog.Entry)

    assert response.name == "name_value"

    assert response.linked_resource == "linked_resource_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


def test_create_entry_from_dict():
    test_create_entry(request_type=dict)


@pytest.mark.asyncio
async def test_create_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.CreateEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.Entry(
                name="name_value",
                linked_resource="linked_resource_value",
                display_name="display_name_value",
                description="description_value",
            )
        )

        response = await client.create_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.CreateEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)

    assert response.name == "name_value"

    assert response.linked_resource == "linked_resource_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_create_entry_async_from_dict():
    await test_create_entry_async(request_type=dict)


def test_create_entry_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateEntryRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        call.return_value = datacatalog.Entry()

        client.create_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_entry_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateEntryRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())

        await client.create_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_entry_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_entry(
            parent="parent_value",
            entry_id="entry_id_value",
            entry=datacatalog.Entry(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].entry_id == "entry_id_value"

        assert args[0].entry == datacatalog.Entry(name="name_value")


def test_create_entry_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_entry(
            datacatalog.CreateEntryRequest(),
            parent="parent_value",
            entry_id="entry_id_value",
            entry=datacatalog.Entry(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_entry_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_entry(
            parent="parent_value",
            entry_id="entry_id_value",
            entry=datacatalog.Entry(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].entry_id == "entry_id_value"

        assert args[0].entry == datacatalog.Entry(name="name_value")


@pytest.mark.asyncio
async def test_create_entry_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_entry(
            datacatalog.CreateEntryRequest(),
            parent="parent_value",
            entry_id="entry_id_value",
            entry=datacatalog.Entry(name="name_value"),
        )


def test_update_entry(
    transport: str = "grpc", request_type=datacatalog.UpdateEntryRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry(
            name="name_value",
            linked_resource="linked_resource_value",
            display_name="display_name_value",
            description="description_value",
            type_=datacatalog.EntryType.TABLE,
            integrated_system=common.IntegratedSystem.BIGQUERY,
            gcs_fileset_spec=gcs_fileset_spec.GcsFilesetSpec(
                file_patterns=["file_patterns_value"]
            ),
        )

        response = client.update_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.UpdateEntryRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datacatalog.Entry)

    assert response.name == "name_value"

    assert response.linked_resource == "linked_resource_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


def test_update_entry_from_dict():
    test_update_entry(request_type=dict)


@pytest.mark.asyncio
async def test_update_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.UpdateEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.Entry(
                name="name_value",
                linked_resource="linked_resource_value",
                display_name="display_name_value",
                description="description_value",
            )
        )

        response = await client.update_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.UpdateEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)

    assert response.name == "name_value"

    assert response.linked_resource == "linked_resource_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_update_entry_async_from_dict():
    await test_update_entry_async(request_type=dict)


def test_update_entry_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateEntryRequest()
    request.entry.name = "entry.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        call.return_value = datacatalog.Entry()

        client.update_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "entry.name=entry.name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_entry_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateEntryRequest()
    request.entry.name = "entry.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())

        await client.update_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "entry.name=entry.name/value",) in kw["metadata"]


def test_update_entry_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_entry(
            entry=datacatalog.Entry(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].entry == datacatalog.Entry(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_entry_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_entry(
            datacatalog.UpdateEntryRequest(),
            entry=datacatalog.Entry(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_entry_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_entry(
            entry=datacatalog.Entry(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].entry == datacatalog.Entry(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_entry_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_entry(
            datacatalog.UpdateEntryRequest(),
            entry=datacatalog.Entry(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_entry(
    transport: str = "grpc", request_type=datacatalog.DeleteEntryRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.DeleteEntryRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_entry_from_dict():
    test_delete_entry(request_type=dict)


@pytest.mark.asyncio
async def test_delete_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.DeleteEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.DeleteEntryRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_entry_async_from_dict():
    await test_delete_entry_async(request_type=dict)


def test_delete_entry_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteEntryRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        call.return_value = None

        client.delete_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_entry_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteEntryRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_entry_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_entry(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_entry_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_entry(
            datacatalog.DeleteEntryRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_entry_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_entry(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_entry_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_entry(
            datacatalog.DeleteEntryRequest(), name="name_value",
        )


def test_get_entry(transport: str = "grpc", request_type=datacatalog.GetEntryRequest):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry(
            name="name_value",
            linked_resource="linked_resource_value",
            display_name="display_name_value",
            description="description_value",
            type_=datacatalog.EntryType.TABLE,
            integrated_system=common.IntegratedSystem.BIGQUERY,
            gcs_fileset_spec=gcs_fileset_spec.GcsFilesetSpec(
                file_patterns=["file_patterns_value"]
            ),
        )

        response = client.get_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.GetEntryRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datacatalog.Entry)

    assert response.name == "name_value"

    assert response.linked_resource == "linked_resource_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


def test_get_entry_from_dict():
    test_get_entry(request_type=dict)


@pytest.mark.asyncio
async def test_get_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.GetEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.Entry(
                name="name_value",
                linked_resource="linked_resource_value",
                display_name="display_name_value",
                description="description_value",
            )
        )

        response = await client.get_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.GetEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)

    assert response.name == "name_value"

    assert response.linked_resource == "linked_resource_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_entry_async_from_dict():
    await test_get_entry_async(request_type=dict)


def test_get_entry_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetEntryRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        call.return_value = datacatalog.Entry()

        client.get_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_entry_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetEntryRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())

        await client.get_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_entry_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_entry(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_entry_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_entry(
            datacatalog.GetEntryRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_entry_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_entry(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_entry_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_entry(
            datacatalog.GetEntryRequest(), name="name_value",
        )


def test_lookup_entry(
    transport: str = "grpc", request_type=datacatalog.LookupEntryRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry(
            name="name_value",
            linked_resource="linked_resource_value",
            display_name="display_name_value",
            description="description_value",
            type_=datacatalog.EntryType.TABLE,
            integrated_system=common.IntegratedSystem.BIGQUERY,
            gcs_fileset_spec=gcs_fileset_spec.GcsFilesetSpec(
                file_patterns=["file_patterns_value"]
            ),
        )

        response = client.lookup_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.LookupEntryRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, datacatalog.Entry)

    assert response.name == "name_value"

    assert response.linked_resource == "linked_resource_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


def test_lookup_entry_from_dict():
    test_lookup_entry(request_type=dict)


@pytest.mark.asyncio
async def test_lookup_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.LookupEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.Entry(
                name="name_value",
                linked_resource="linked_resource_value",
                display_name="display_name_value",
                description="description_value",
            )
        )

        response = await client.lookup_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.LookupEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)

    assert response.name == "name_value"

    assert response.linked_resource == "linked_resource_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_lookup_entry_async_from_dict():
    await test_lookup_entry_async(request_type=dict)


def test_list_entries(
    transport: str = "grpc", request_type=datacatalog.ListEntriesRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntriesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.ListEntriesRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListEntriesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_entries_from_dict():
    test_list_entries(request_type=dict)


@pytest.mark.asyncio
async def test_list_entries_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.ListEntriesRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntriesResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.ListEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntriesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_entries_async_from_dict():
    await test_list_entries_async(request_type=dict)


def test_list_entries_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListEntriesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        call.return_value = datacatalog.ListEntriesResponse()

        client.list_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_entries_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListEntriesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntriesResponse()
        )

        await client.list_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_entries_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntriesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_entries(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_entries_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_entries(
            datacatalog.ListEntriesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_entries_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_entries(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_entries_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_entries(
            datacatalog.ListEntriesRequest(), parent="parent_value",
        )


def test_list_entries_pager():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntriesResponse(entries=[], next_page_token="def",),
            datacatalog.ListEntriesResponse(
                entries=[datacatalog.Entry(),], next_page_token="ghi",
            ),
            datacatalog.ListEntriesResponse(
                entries=[datacatalog.Entry(), datacatalog.Entry(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_entries(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, datacatalog.Entry) for i in results)


def test_list_entries_pages():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntriesResponse(entries=[], next_page_token="def",),
            datacatalog.ListEntriesResponse(
                entries=[datacatalog.Entry(),], next_page_token="ghi",
            ),
            datacatalog.ListEntriesResponse(
                entries=[datacatalog.Entry(), datacatalog.Entry(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_entries(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_entries_async_pager():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entries), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntriesResponse(entries=[], next_page_token="def",),
            datacatalog.ListEntriesResponse(
                entries=[datacatalog.Entry(),], next_page_token="ghi",
            ),
            datacatalog.ListEntriesResponse(
                entries=[datacatalog.Entry(), datacatalog.Entry(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_entries(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, datacatalog.Entry) for i in responses)


@pytest.mark.asyncio
async def test_list_entries_async_pages():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entries), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntriesResponse(entries=[], next_page_token="def",),
            datacatalog.ListEntriesResponse(
                entries=[datacatalog.Entry(),], next_page_token="ghi",
            ),
            datacatalog.ListEntriesResponse(
                entries=[datacatalog.Entry(), datacatalog.Entry(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_entries(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_tag_template(
    transport: str = "grpc", request_type=datacatalog.CreateTagTemplateRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate(
            name="name_value", display_name="display_name_value",
        )

        response = client.create_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.CreateTagTemplateRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, tags.TagTemplate)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_create_tag_template_from_dict():
    test_create_tag_template(request_type=dict)


@pytest.mark.asyncio
async def test_create_tag_template_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.CreateTagTemplateRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplate(name="name_value", display_name="display_name_value",)
        )

        response = await client.create_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.CreateTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplate)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_create_tag_template_async_from_dict():
    await test_create_tag_template_async(request_type=dict)


def test_create_tag_template_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagTemplateRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        call.return_value = tags.TagTemplate()

        client.create_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_tag_template_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagTemplateRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())

        await client.create_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_tag_template_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tag_template(
            parent="parent_value",
            tag_template_id="tag_template_id_value",
            tag_template=tags.TagTemplate(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].tag_template_id == "tag_template_id_value"

        assert args[0].tag_template == tags.TagTemplate(name="name_value")


def test_create_tag_template_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tag_template(
            datacatalog.CreateTagTemplateRequest(),
            parent="parent_value",
            tag_template_id="tag_template_id_value",
            tag_template=tags.TagTemplate(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_tag_template_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tag_template(
            parent="parent_value",
            tag_template_id="tag_template_id_value",
            tag_template=tags.TagTemplate(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].tag_template_id == "tag_template_id_value"

        assert args[0].tag_template == tags.TagTemplate(name="name_value")


@pytest.mark.asyncio
async def test_create_tag_template_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tag_template(
            datacatalog.CreateTagTemplateRequest(),
            parent="parent_value",
            tag_template_id="tag_template_id_value",
            tag_template=tags.TagTemplate(name="name_value"),
        )


def test_get_tag_template(
    transport: str = "grpc", request_type=datacatalog.GetTagTemplateRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate(
            name="name_value", display_name="display_name_value",
        )

        response = client.get_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.GetTagTemplateRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, tags.TagTemplate)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_get_tag_template_from_dict():
    test_get_tag_template(request_type=dict)


@pytest.mark.asyncio
async def test_get_tag_template_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.GetTagTemplateRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplate(name="name_value", display_name="display_name_value",)
        )

        response = await client.get_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.GetTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplate)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_tag_template_async_from_dict():
    await test_get_tag_template_async(request_type=dict)


def test_get_tag_template_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetTagTemplateRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        call.return_value = tags.TagTemplate()

        client.get_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_tag_template_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetTagTemplateRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())

        await client.get_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_tag_template_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_tag_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_tag_template_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tag_template(
            datacatalog.GetTagTemplateRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_tag_template_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_tag_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_tag_template_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_tag_template(
            datacatalog.GetTagTemplateRequest(), name="name_value",
        )


def test_update_tag_template(
    transport: str = "grpc", request_type=datacatalog.UpdateTagTemplateRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate(
            name="name_value", display_name="display_name_value",
        )

        response = client.update_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.UpdateTagTemplateRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, tags.TagTemplate)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_update_tag_template_from_dict():
    test_update_tag_template(request_type=dict)


@pytest.mark.asyncio
async def test_update_tag_template_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.UpdateTagTemplateRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplate(name="name_value", display_name="display_name_value",)
        )

        response = await client.update_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.UpdateTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplate)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_tag_template_async_from_dict():
    await test_update_tag_template_async(request_type=dict)


def test_update_tag_template_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagTemplateRequest()
    request.tag_template.name = "tag_template.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        call.return_value = tags.TagTemplate()

        client.update_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tag_template.name=tag_template.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tag_template_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagTemplateRequest()
    request.tag_template.name = "tag_template.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())

        await client.update_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tag_template.name=tag_template.name/value",
    ) in kw["metadata"]


def test_update_tag_template_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tag_template(
            tag_template=tags.TagTemplate(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].tag_template == tags.TagTemplate(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_tag_template_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tag_template(
            datacatalog.UpdateTagTemplateRequest(),
            tag_template=tags.TagTemplate(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tag_template_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tag_template(
            tag_template=tags.TagTemplate(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].tag_template == tags.TagTemplate(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_tag_template_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tag_template(
            datacatalog.UpdateTagTemplateRequest(),
            tag_template=tags.TagTemplate(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_tag_template(
    transport: str = "grpc", request_type=datacatalog.DeleteTagTemplateRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.DeleteTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_tag_template_from_dict():
    test_delete_tag_template(request_type=dict)


@pytest.mark.asyncio
async def test_delete_tag_template_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.DeleteTagTemplateRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.DeleteTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_tag_template_async_from_dict():
    await test_delete_tag_template_async(request_type=dict)


def test_delete_tag_template_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagTemplateRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        call.return_value = None

        client.delete_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_tag_template_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagTemplateRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_tag_template_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tag_template(
            name="name_value", force=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].force == True


def test_delete_tag_template_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tag_template(
            datacatalog.DeleteTagTemplateRequest(), name="name_value", force=True,
        )


@pytest.mark.asyncio
async def test_delete_tag_template_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tag_template(name="name_value", force=True,)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].force == True


@pytest.mark.asyncio
async def test_delete_tag_template_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tag_template(
            datacatalog.DeleteTagTemplateRequest(), name="name_value", force=True,
        )


def test_create_tag_template_field(
    transport: str = "grpc", request_type=datacatalog.CreateTagTemplateFieldRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField(
            name="name_value",
            display_name="display_name_value",
            is_required=True,
            order=540,
        )

        response = client.create_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.CreateTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, tags.TagTemplateField)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.is_required is True

    assert response.order == 540


def test_create_tag_template_field_from_dict():
    test_create_tag_template_field(request_type=dict)


@pytest.mark.asyncio
async def test_create_tag_template_field_async(
    transport: str = "grpc_asyncio",
    request_type=datacatalog.CreateTagTemplateFieldRequest,
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField(
                name="name_value",
                display_name="display_name_value",
                is_required=True,
                order=540,
            )
        )

        response = await client.create_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.CreateTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.is_required is True

    assert response.order == 540


@pytest.mark.asyncio
async def test_create_tag_template_field_async_from_dict():
    await test_create_tag_template_field_async(request_type=dict)


def test_create_tag_template_field_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagTemplateFieldRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        call.return_value = tags.TagTemplateField()

        client.create_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_tag_template_field_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagTemplateFieldRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )

        await client.create_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_tag_template_field_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tag_template_field(
            parent="parent_value",
            tag_template_field_id="tag_template_field_id_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].tag_template_field_id == "tag_template_field_id_value"

        assert args[0].tag_template_field == tags.TagTemplateField(name="name_value")


def test_create_tag_template_field_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tag_template_field(
            datacatalog.CreateTagTemplateFieldRequest(),
            parent="parent_value",
            tag_template_field_id="tag_template_field_id_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_tag_template_field_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tag_template_field(
            parent="parent_value",
            tag_template_field_id="tag_template_field_id_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].tag_template_field_id == "tag_template_field_id_value"

        assert args[0].tag_template_field == tags.TagTemplateField(name="name_value")


@pytest.mark.asyncio
async def test_create_tag_template_field_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tag_template_field(
            datacatalog.CreateTagTemplateFieldRequest(),
            parent="parent_value",
            tag_template_field_id="tag_template_field_id_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
        )


def test_update_tag_template_field(
    transport: str = "grpc", request_type=datacatalog.UpdateTagTemplateFieldRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField(
            name="name_value",
            display_name="display_name_value",
            is_required=True,
            order=540,
        )

        response = client.update_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.UpdateTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, tags.TagTemplateField)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.is_required is True

    assert response.order == 540


def test_update_tag_template_field_from_dict():
    test_update_tag_template_field(request_type=dict)


@pytest.mark.asyncio
async def test_update_tag_template_field_async(
    transport: str = "grpc_asyncio",
    request_type=datacatalog.UpdateTagTemplateFieldRequest,
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField(
                name="name_value",
                display_name="display_name_value",
                is_required=True,
                order=540,
            )
        )

        response = await client.update_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.UpdateTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.is_required is True

    assert response.order == 540


@pytest.mark.asyncio
async def test_update_tag_template_field_async_from_dict():
    await test_update_tag_template_field_async(request_type=dict)


def test_update_tag_template_field_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagTemplateFieldRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        call.return_value = tags.TagTemplateField()

        client.update_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tag_template_field_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagTemplateFieldRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )

        await client.update_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_tag_template_field_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tag_template_field(
            name="name_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].tag_template_field == tags.TagTemplateField(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_tag_template_field_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tag_template_field(
            datacatalog.UpdateTagTemplateFieldRequest(),
            name="name_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tag_template_field_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tag_template_field(
            name="name_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].tag_template_field == tags.TagTemplateField(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_tag_template_field_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tag_template_field(
            datacatalog.UpdateTagTemplateFieldRequest(),
            name="name_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_rename_tag_template_field(
    transport: str = "grpc", request_type=datacatalog.RenameTagTemplateFieldRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField(
            name="name_value",
            display_name="display_name_value",
            is_required=True,
            order=540,
        )

        response = client.rename_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.RenameTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, tags.TagTemplateField)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.is_required is True

    assert response.order == 540


def test_rename_tag_template_field_from_dict():
    test_rename_tag_template_field(request_type=dict)


@pytest.mark.asyncio
async def test_rename_tag_template_field_async(
    transport: str = "grpc_asyncio",
    request_type=datacatalog.RenameTagTemplateFieldRequest,
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField(
                name="name_value",
                display_name="display_name_value",
                is_required=True,
                order=540,
            )
        )

        response = await client.rename_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.RenameTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.is_required is True

    assert response.order == 540


@pytest.mark.asyncio
async def test_rename_tag_template_field_async_from_dict():
    await test_rename_tag_template_field_async(request_type=dict)


def test_rename_tag_template_field_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.RenameTagTemplateFieldRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        call.return_value = tags.TagTemplateField()

        client.rename_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_rename_tag_template_field_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.RenameTagTemplateFieldRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )

        await client.rename_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_rename_tag_template_field_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rename_tag_template_field(
            name="name_value",
            new_tag_template_field_id="new_tag_template_field_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].new_tag_template_field_id == "new_tag_template_field_id_value"


def test_rename_tag_template_field_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rename_tag_template_field(
            datacatalog.RenameTagTemplateFieldRequest(),
            name="name_value",
            new_tag_template_field_id="new_tag_template_field_id_value",
        )


@pytest.mark.asyncio
async def test_rename_tag_template_field_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rename_tag_template_field(
            name="name_value",
            new_tag_template_field_id="new_tag_template_field_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].new_tag_template_field_id == "new_tag_template_field_id_value"


@pytest.mark.asyncio
async def test_rename_tag_template_field_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rename_tag_template_field(
            datacatalog.RenameTagTemplateFieldRequest(),
            name="name_value",
            new_tag_template_field_id="new_tag_template_field_id_value",
        )


def test_delete_tag_template_field(
    transport: str = "grpc", request_type=datacatalog.DeleteTagTemplateFieldRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.DeleteTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_tag_template_field_from_dict():
    test_delete_tag_template_field(request_type=dict)


@pytest.mark.asyncio
async def test_delete_tag_template_field_async(
    transport: str = "grpc_asyncio",
    request_type=datacatalog.DeleteTagTemplateFieldRequest,
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.DeleteTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_tag_template_field_async_from_dict():
    await test_delete_tag_template_field_async(request_type=dict)


def test_delete_tag_template_field_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagTemplateFieldRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        call.return_value = None

        client.delete_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_tag_template_field_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagTemplateFieldRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_tag_template_field_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tag_template_field(
            name="name_value", force=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].force == True


def test_delete_tag_template_field_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tag_template_field(
            datacatalog.DeleteTagTemplateFieldRequest(), name="name_value", force=True,
        )


@pytest.mark.asyncio
async def test_delete_tag_template_field_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tag_template_field(
            name="name_value", force=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].force == True


@pytest.mark.asyncio
async def test_delete_tag_template_field_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tag_template_field(
            datacatalog.DeleteTagTemplateFieldRequest(), name="name_value", force=True,
        )


def test_create_tag(transport: str = "grpc", request_type=datacatalog.CreateTagRequest):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag(
            name="name_value",
            template="template_value",
            template_display_name="template_display_name_value",
            column="column_value",
        )

        response = client.create_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.CreateTagRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, tags.Tag)

    assert response.name == "name_value"

    assert response.template == "template_value"

    assert response.template_display_name == "template_display_name_value"


def test_create_tag_from_dict():
    test_create_tag(request_type=dict)


@pytest.mark.asyncio
async def test_create_tag_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.CreateTagRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.Tag(
                name="name_value",
                template="template_value",
                template_display_name="template_display_name_value",
            )
        )

        response = await client.create_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.CreateTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.Tag)

    assert response.name == "name_value"

    assert response.template == "template_value"

    assert response.template_display_name == "template_display_name_value"


@pytest.mark.asyncio
async def test_create_tag_async_from_dict():
    await test_create_tag_async(request_type=dict)


def test_create_tag_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        call.return_value = tags.Tag()

        client.create_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_tag_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.Tag())

        await client.create_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_tag_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tag(
            parent="parent_value", tag=tags.Tag(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].tag == tags.Tag(name="name_value")


def test_create_tag_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tag(
            datacatalog.CreateTagRequest(),
            parent="parent_value",
            tag=tags.Tag(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_tag_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.Tag())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tag(
            parent="parent_value", tag=tags.Tag(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].tag == tags.Tag(name="name_value")


@pytest.mark.asyncio
async def test_create_tag_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tag(
            datacatalog.CreateTagRequest(),
            parent="parent_value",
            tag=tags.Tag(name="name_value"),
        )


def test_update_tag(transport: str = "grpc", request_type=datacatalog.UpdateTagRequest):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag(
            name="name_value",
            template="template_value",
            template_display_name="template_display_name_value",
            column="column_value",
        )

        response = client.update_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.UpdateTagRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, tags.Tag)

    assert response.name == "name_value"

    assert response.template == "template_value"

    assert response.template_display_name == "template_display_name_value"


def test_update_tag_from_dict():
    test_update_tag(request_type=dict)


@pytest.mark.asyncio
async def test_update_tag_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.UpdateTagRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.Tag(
                name="name_value",
                template="template_value",
                template_display_name="template_display_name_value",
            )
        )

        response = await client.update_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.UpdateTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.Tag)

    assert response.name == "name_value"

    assert response.template == "template_value"

    assert response.template_display_name == "template_display_name_value"


@pytest.mark.asyncio
async def test_update_tag_async_from_dict():
    await test_update_tag_async(request_type=dict)


def test_update_tag_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagRequest()
    request.tag.name = "tag.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        call.return_value = tags.Tag()

        client.update_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "tag.name=tag.name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tag_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagRequest()
    request.tag.name = "tag.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.Tag())

        await client.update_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "tag.name=tag.name/value",) in kw["metadata"]


def test_update_tag_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tag(
            tag=tags.Tag(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].tag == tags.Tag(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_tag_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tag(
            datacatalog.UpdateTagRequest(),
            tag=tags.Tag(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tag_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.Tag())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tag(
            tag=tags.Tag(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].tag == tags.Tag(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_tag_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tag(
            datacatalog.UpdateTagRequest(),
            tag=tags.Tag(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_tag(transport: str = "grpc", request_type=datacatalog.DeleteTagRequest):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.DeleteTagRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_tag_from_dict():
    test_delete_tag(request_type=dict)


@pytest.mark.asyncio
async def test_delete_tag_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.DeleteTagRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.DeleteTagRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_tag_async_from_dict():
    await test_delete_tag_async(request_type=dict)


def test_delete_tag_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        call.return_value = None

        client.delete_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_tag_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_tag_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tag(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_tag_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tag(
            datacatalog.DeleteTagRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_tag_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tag(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_tag_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tag(
            datacatalog.DeleteTagRequest(), name="name_value",
        )


def test_list_tags(transport: str = "grpc", request_type=datacatalog.ListTagsRequest):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListTagsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.ListTagsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListTagsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_tags_from_dict():
    test_list_tags(request_type=dict)


@pytest.mark.asyncio
async def test_list_tags_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.ListTagsRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListTagsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == datacatalog.ListTagsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTagsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tags_async_from_dict():
    await test_list_tags_async(request_type=dict)


def test_list_tags_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListTagsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        call.return_value = datacatalog.ListTagsResponse()

        client.list_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_tags_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListTagsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListTagsResponse()
        )

        await client.list_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_tags_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListTagsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tags(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_tags_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tags(
            datacatalog.ListTagsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tags_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListTagsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListTagsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tags(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_tags_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tags(
            datacatalog.ListTagsRequest(), parent="parent_value",
        )


def test_list_tags_pager():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListTagsResponse(
                tags=[tags.Tag(), tags.Tag(), tags.Tag(),], next_page_token="abc",
            ),
            datacatalog.ListTagsResponse(tags=[], next_page_token="def",),
            datacatalog.ListTagsResponse(tags=[tags.Tag(),], next_page_token="ghi",),
            datacatalog.ListTagsResponse(tags=[tags.Tag(), tags.Tag(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tags(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, tags.Tag) for i in results)


def test_list_tags_pages():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListTagsResponse(
                tags=[tags.Tag(), tags.Tag(), tags.Tag(),], next_page_token="abc",
            ),
            datacatalog.ListTagsResponse(tags=[], next_page_token="def",),
            datacatalog.ListTagsResponse(tags=[tags.Tag(),], next_page_token="ghi",),
            datacatalog.ListTagsResponse(tags=[tags.Tag(), tags.Tag(),],),
            RuntimeError,
        )
        pages = list(client.list_tags(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tags_async_pager():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tags), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListTagsResponse(
                tags=[tags.Tag(), tags.Tag(), tags.Tag(),], next_page_token="abc",
            ),
            datacatalog.ListTagsResponse(tags=[], next_page_token="def",),
            datacatalog.ListTagsResponse(tags=[tags.Tag(),], next_page_token="ghi",),
            datacatalog.ListTagsResponse(tags=[tags.Tag(), tags.Tag(),],),
            RuntimeError,
        )
        async_pager = await client.list_tags(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, tags.Tag) for i in responses)


@pytest.mark.asyncio
async def test_list_tags_async_pages():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tags), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListTagsResponse(
                tags=[tags.Tag(), tags.Tag(), tags.Tag(),], next_page_token="abc",
            ),
            datacatalog.ListTagsResponse(tags=[], next_page_token="def",),
            datacatalog.ListTagsResponse(tags=[tags.Tag(),], next_page_token="ghi",),
            datacatalog.ListTagsResponse(tags=[tags.Tag(), tags.Tag(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_tags(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_set_iam_policy(
    transport: str = "grpc", request_type=iam_policy.SetIamPolicyRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob",)

        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_from_dict():
    test_set_iam_policy(request_type=dict)


@pytest.mark.asyncio
async def test_set_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=iam_policy.SetIamPolicyRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy.Policy(version=774, etag=b"etag_blob",)
        )

        response = await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async_from_dict():
    await test_set_iam_policy_async(request_type=dict)


def test_set_iam_policy_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())

        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_set_iam_policy_from_dict_foreign():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy.Policy(version=774),
            }
        )
        call.assert_called()


def test_set_iam_policy_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_iam_policy(resource="resource_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].resource == "resource_value"


def test_set_iam_policy_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            iam_policy.SetIamPolicyRequest(), resource="resource_value",
        )


@pytest.mark.asyncio
async def test_set_iam_policy_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_iam_policy(resource="resource_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].resource == "resource_value"


@pytest.mark.asyncio
async def test_set_iam_policy_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_iam_policy(
            iam_policy.SetIamPolicyRequest(), resource="resource_value",
        )


def test_get_iam_policy(
    transport: str = "grpc", request_type=iam_policy.GetIamPolicyRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob",)

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_from_dict():
    test_get_iam_policy(request_type=dict)


@pytest.mark.asyncio
async def test_get_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=iam_policy.GetIamPolicyRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy.Policy(version=774, etag=b"etag_blob",)
        )

        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async_from_dict():
    await test_get_iam_policy_async(request_type=dict)


def test_get_iam_policy_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_get_iam_policy_from_dict_foreign():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_get_iam_policy_flattened():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_iam_policy(resource="resource_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].resource == "resource_value"


def test_get_iam_policy_flattened_error():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            iam_policy.GetIamPolicyRequest(), resource="resource_value",
        )


@pytest.mark.asyncio
async def test_get_iam_policy_flattened_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_iam_policy(resource="resource_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].resource == "resource_value"


@pytest.mark.asyncio
async def test_get_iam_policy_flattened_error_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_iam_policy(
            iam_policy.GetIamPolicyRequest(), resource="resource_value",
        )


def test_test_iam_permissions(
    transport: str = "grpc", request_type=iam_policy.TestIamPermissionsRequest
):
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, iam_policy.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_from_dict():
    test_test_iam_permissions(request_type=dict)


@pytest.mark.asyncio
async def test_test_iam_permissions_async(
    transport: str = "grpc_asyncio", request_type=iam_policy.TestIamPermissionsRequest
):
    client = DataCatalogAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy.TestIamPermissionsResponse(permissions=["permissions_value"],)
        )

        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async_from_dict():
    await test_test_iam_permissions_async(request_type=dict)


def test_test_iam_permissions_field_headers():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy.TestIamPermissionsResponse()

        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = DataCatalogAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy.TestIamPermissionsResponse()
        )

        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_test_iam_permissions_from_dict_foreign():
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataCatalogClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataCatalogClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataCatalogClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = DataCatalogClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DataCatalogGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.DataCatalogGrpcTransport, transports.DataCatalogGrpcAsyncIOTransport],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DataCatalogClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.DataCatalogGrpcTransport,)


def test_data_catalog_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.DataCatalogTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_data_catalog_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.datacatalog_v1beta1.services.data_catalog.transports.DataCatalogTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DataCatalogTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "search_catalog",
        "create_entry_group",
        "update_entry_group",
        "get_entry_group",
        "delete_entry_group",
        "list_entry_groups",
        "create_entry",
        "update_entry",
        "delete_entry",
        "get_entry",
        "lookup_entry",
        "list_entries",
        "create_tag_template",
        "get_tag_template",
        "update_tag_template",
        "delete_tag_template",
        "create_tag_template_field",
        "update_tag_template_field",
        "rename_tag_template_field",
        "delete_tag_template_field",
        "create_tag",
        "update_tag",
        "delete_tag",
        "list_tags",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_data_catalog_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.datacatalog_v1beta1.services.data_catalog.transports.DataCatalogTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.DataCatalogTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_data_catalog_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.datacatalog_v1beta1.services.data_catalog.transports.DataCatalogTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.DataCatalogTransport()
        adc.assert_called_once()


def test_data_catalog_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        DataCatalogClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_data_catalog_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.DataCatalogGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_data_catalog_host_no_port():
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datacatalog.googleapis.com"
        ),
    )
    assert client.transport._host == "datacatalog.googleapis.com:443"


def test_data_catalog_host_with_port():
    client = DataCatalogClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datacatalog.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "datacatalog.googleapis.com:8000"


def test_data_catalog_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.DataCatalogGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_data_catalog_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.DataCatalogGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [transports.DataCatalogGrpcTransport, transports.DataCatalogGrpcAsyncIOTransport],
)
def test_data_catalog_transport_channel_mtls_with_client_cert_source(transport_class):
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
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [transports.DataCatalogGrpcTransport, transports.DataCatalogGrpcAsyncIOTransport],
)
def test_data_catalog_transport_channel_mtls_with_adc(transport_class):
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
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_entry_path():
    project = "squid"
    location = "clam"
    entry_group = "whelk"
    entry = "octopus"

    expected = "projects/{project}/locations/{location}/entryGroups/{entry_group}/entries/{entry}".format(
        project=project, location=location, entry_group=entry_group, entry=entry,
    )
    actual = DataCatalogClient.entry_path(project, location, entry_group, entry)
    assert expected == actual


def test_parse_entry_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "entry_group": "cuttlefish",
        "entry": "mussel",
    }
    path = DataCatalogClient.entry_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_entry_path(path)
    assert expected == actual


def test_entry_group_path():
    project = "winkle"
    location = "nautilus"
    entry_group = "scallop"

    expected = "projects/{project}/locations/{location}/entryGroups/{entry_group}".format(
        project=project, location=location, entry_group=entry_group,
    )
    actual = DataCatalogClient.entry_group_path(project, location, entry_group)
    assert expected == actual


def test_parse_entry_group_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "entry_group": "clam",
    }
    path = DataCatalogClient.entry_group_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_entry_group_path(path)
    assert expected == actual


def test_tag_path():
    project = "whelk"
    location = "octopus"
    entry_group = "oyster"
    entry = "nudibranch"
    tag = "cuttlefish"

    expected = "projects/{project}/locations/{location}/entryGroups/{entry_group}/entries/{entry}/tags/{tag}".format(
        project=project,
        location=location,
        entry_group=entry_group,
        entry=entry,
        tag=tag,
    )
    actual = DataCatalogClient.tag_path(project, location, entry_group, entry, tag)
    assert expected == actual


def test_parse_tag_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "entry_group": "nautilus",
        "entry": "scallop",
        "tag": "abalone",
    }
    path = DataCatalogClient.tag_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_tag_path(path)
    assert expected == actual


def test_tag_template_path():
    project = "squid"
    location = "clam"
    tag_template = "whelk"

    expected = "projects/{project}/locations/{location}/tagTemplates/{tag_template}".format(
        project=project, location=location, tag_template=tag_template,
    )
    actual = DataCatalogClient.tag_template_path(project, location, tag_template)
    assert expected == actual


def test_parse_tag_template_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "tag_template": "nudibranch",
    }
    path = DataCatalogClient.tag_template_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_tag_template_path(path)
    assert expected == actual


def test_tag_template_field_path():
    project = "cuttlefish"
    location = "mussel"
    tag_template = "winkle"
    field = "nautilus"

    expected = "projects/{project}/locations/{location}/tagTemplates/{tag_template}/fields/{field}".format(
        project=project, location=location, tag_template=tag_template, field=field,
    )
    actual = DataCatalogClient.tag_template_field_path(
        project, location, tag_template, field
    )
    assert expected == actual


def test_parse_tag_template_field_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "tag_template": "squid",
        "field": "clam",
    }
    path = DataCatalogClient.tag_template_field_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_tag_template_field_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DataCatalogClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = DataCatalogClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"

    expected = "folders/{folder}".format(folder=folder,)
    actual = DataCatalogClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = DataCatalogClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = DataCatalogClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = DataCatalogClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"

    expected = "projects/{project}".format(project=project,)
    actual = DataCatalogClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = DataCatalogClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = DataCatalogClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = DataCatalogClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DataCatalogTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DataCatalogClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DataCatalogTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DataCatalogClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
