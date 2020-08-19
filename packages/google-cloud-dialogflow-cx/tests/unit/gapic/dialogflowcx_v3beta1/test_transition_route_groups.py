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
from google.cloud.dialogflowcx_v3beta1.services.transition_route_groups import (
    TransitionRouteGroupsAsyncClient,
)
from google.cloud.dialogflowcx_v3beta1.services.transition_route_groups import (
    TransitionRouteGroupsClient,
)
from google.cloud.dialogflowcx_v3beta1.services.transition_route_groups import pagers
from google.cloud.dialogflowcx_v3beta1.services.transition_route_groups import (
    transports,
)
from google.cloud.dialogflowcx_v3beta1.types import fulfillment
from google.cloud.dialogflowcx_v3beta1.types import page
from google.cloud.dialogflowcx_v3beta1.types import page as gcdc_page
from google.cloud.dialogflowcx_v3beta1.types import response_message
from google.cloud.dialogflowcx_v3beta1.types import transition_route_group
from google.cloud.dialogflowcx_v3beta1.types import (
    transition_route_group as gcdc_transition_route_group,
)
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore


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

    assert TransitionRouteGroupsClient._get_default_mtls_endpoint(None) is None
    assert (
        TransitionRouteGroupsClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        TransitionRouteGroupsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        TransitionRouteGroupsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        TransitionRouteGroupsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        TransitionRouteGroupsClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [TransitionRouteGroupsClient, TransitionRouteGroupsAsyncClient]
)
def test_transition_route_groups_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "dialogflow.googleapis.com:443"


def test_transition_route_groups_client_get_transport_class():
    transport = TransitionRouteGroupsClient.get_transport_class()
    assert transport == transports.TransitionRouteGroupsGrpcTransport

    transport = TransitionRouteGroupsClient.get_transport_class("grpc")
    assert transport == transports.TransitionRouteGroupsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            TransitionRouteGroupsClient,
            transports.TransitionRouteGroupsGrpcTransport,
            "grpc",
        ),
        (
            TransitionRouteGroupsAsyncClient,
            transports.TransitionRouteGroupsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    TransitionRouteGroupsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TransitionRouteGroupsClient),
)
@mock.patch.object(
    TransitionRouteGroupsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TransitionRouteGroupsAsyncClient),
)
def test_transition_route_groups_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(TransitionRouteGroupsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(TransitionRouteGroupsClient, "get_transport_class") as gtc:
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
            client_info=transports.base.DEFAULT_CLIENT_INFO,
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
                client_info=transports.base.DEFAULT_CLIENT_INFO,
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
                client_info=transports.base.DEFAULT_CLIENT_INFO,
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
                client_info=transports.base.DEFAULT_CLIENT_INFO,
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
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
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
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
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
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            TransitionRouteGroupsClient,
            transports.TransitionRouteGroupsGrpcTransport,
            "grpc",
        ),
        (
            TransitionRouteGroupsAsyncClient,
            transports.TransitionRouteGroupsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_transition_route_groups_client_client_options_scopes(
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
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            TransitionRouteGroupsClient,
            transports.TransitionRouteGroupsGrpcTransport,
            "grpc",
        ),
        (
            TransitionRouteGroupsAsyncClient,
            transports.TransitionRouteGroupsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_transition_route_groups_client_client_options_credentials_file(
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
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_transition_route_groups_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.transition_route_groups.transports.TransitionRouteGroupsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = TransitionRouteGroupsClient(
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
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_list_transition_route_groups(
    transport: str = "grpc",
    request_type=transition_route_group.ListTransitionRouteGroupsRequest,
):
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_transition_route_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transition_route_group.ListTransitionRouteGroupsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_transition_route_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == transition_route_group.ListTransitionRouteGroupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTransitionRouteGroupsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_transition_route_groups_from_dict():
    test_list_transition_route_groups(request_type=dict)


@pytest.mark.asyncio
async def test_list_transition_route_groups_async(transport: str = "grpc_asyncio"):
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = transition_route_group.ListTransitionRouteGroupsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_transition_route_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transition_route_group.ListTransitionRouteGroupsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_transition_route_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTransitionRouteGroupsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_transition_route_groups_field_headers():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transition_route_group.ListTransitionRouteGroupsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_transition_route_groups), "__call__"
    ) as call:
        call.return_value = transition_route_group.ListTransitionRouteGroupsResponse()

        client.list_transition_route_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_transition_route_groups_field_headers_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transition_route_group.ListTransitionRouteGroupsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_transition_route_groups), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transition_route_group.ListTransitionRouteGroupsResponse()
        )

        await client.list_transition_route_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_transition_route_groups_flattened():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_transition_route_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transition_route_group.ListTransitionRouteGroupsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_transition_route_groups(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_transition_route_groups_flattened_error():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_transition_route_groups(
            transition_route_group.ListTransitionRouteGroupsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_transition_route_groups_flattened_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_transition_route_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transition_route_group.ListTransitionRouteGroupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transition_route_group.ListTransitionRouteGroupsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_transition_route_groups(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_transition_route_groups_flattened_error_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_transition_route_groups(
            transition_route_group.ListTransitionRouteGroupsRequest(),
            parent="parent_value",
        )


def test_list_transition_route_groups_pager():
    client = TransitionRouteGroupsClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_transition_route_groups), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                ],
                next_page_token="abc",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[], next_page_token="def",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                ],
                next_page_token="ghi",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_transition_route_groups(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, transition_route_group.TransitionRouteGroup) for i in results
        )


def test_list_transition_route_groups_pages():
    client = TransitionRouteGroupsClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_transition_route_groups), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                ],
                next_page_token="abc",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[], next_page_token="def",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                ],
                next_page_token="ghi",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_transition_route_groups(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_transition_route_groups_async_pager():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_transition_route_groups),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                ],
                next_page_token="abc",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[], next_page_token="def",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                ],
                next_page_token="ghi",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_transition_route_groups(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, transition_route_group.TransitionRouteGroup)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_transition_route_groups_async_pages():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_transition_route_groups),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                ],
                next_page_token="abc",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[], next_page_token="def",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                ],
                next_page_token="ghi",
            ),
            transition_route_group.ListTransitionRouteGroupsResponse(
                transition_route_groups=[
                    transition_route_group.TransitionRouteGroup(),
                    transition_route_group.TransitionRouteGroup(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_transition_route_groups(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_transition_route_group(
    transport: str = "grpc",
    request_type=transition_route_group.GetTransitionRouteGroupRequest,
):
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transition_route_group.TransitionRouteGroup(
            name="name_value", display_name="display_name_value",
        )

        response = client.get_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == transition_route_group.GetTransitionRouteGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, transition_route_group.TransitionRouteGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_get_transition_route_group_from_dict():
    test_get_transition_route_group(request_type=dict)


@pytest.mark.asyncio
async def test_get_transition_route_group_async(transport: str = "grpc_asyncio"):
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = transition_route_group.GetTransitionRouteGroupRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transition_route_group.TransitionRouteGroup(
                name="name_value", display_name="display_name_value",
            )
        )

        response = await client.get_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, transition_route_group.TransitionRouteGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_get_transition_route_group_field_headers():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transition_route_group.GetTransitionRouteGroupRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_transition_route_group), "__call__"
    ) as call:
        call.return_value = transition_route_group.TransitionRouteGroup()

        client.get_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_transition_route_group_field_headers_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transition_route_group.GetTransitionRouteGroupRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_transition_route_group), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transition_route_group.TransitionRouteGroup()
        )

        await client.get_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_transition_route_group_flattened():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transition_route_group.TransitionRouteGroup()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_transition_route_group(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_transition_route_group_flattened_error():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_transition_route_group(
            transition_route_group.GetTransitionRouteGroupRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_transition_route_group_flattened_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = transition_route_group.TransitionRouteGroup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            transition_route_group.TransitionRouteGroup()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_transition_route_group(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_transition_route_group_flattened_error_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_transition_route_group(
            transition_route_group.GetTransitionRouteGroupRequest(), name="name_value",
        )


def test_create_transition_route_group(
    transport: str = "grpc",
    request_type=gcdc_transition_route_group.CreateTransitionRouteGroupRequest,
):
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_transition_route_group.TransitionRouteGroup(
            name="name_value", display_name="display_name_value",
        )

        response = client.create_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert (
            args[0] == gcdc_transition_route_group.CreateTransitionRouteGroupRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_transition_route_group.TransitionRouteGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_create_transition_route_group_from_dict():
    test_create_transition_route_group(request_type=dict)


@pytest.mark.asyncio
async def test_create_transition_route_group_async(transport: str = "grpc_asyncio"):
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gcdc_transition_route_group.CreateTransitionRouteGroupRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_transition_route_group.TransitionRouteGroup(
                name="name_value", display_name="display_name_value",
            )
        )

        response = await client.create_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_transition_route_group.TransitionRouteGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_create_transition_route_group_field_headers():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_transition_route_group.CreateTransitionRouteGroupRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_transition_route_group), "__call__"
    ) as call:
        call.return_value = gcdc_transition_route_group.TransitionRouteGroup()

        client.create_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_transition_route_group_field_headers_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_transition_route_group.CreateTransitionRouteGroupRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_transition_route_group), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_transition_route_group.TransitionRouteGroup()
        )

        await client.create_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_transition_route_group_flattened():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_transition_route_group.TransitionRouteGroup()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_transition_route_group(
            parent="parent_value",
            transition_route_group=gcdc_transition_route_group.TransitionRouteGroup(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[
            0
        ].transition_route_group == gcdc_transition_route_group.TransitionRouteGroup(
            name="name_value"
        )


def test_create_transition_route_group_flattened_error():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_transition_route_group(
            gcdc_transition_route_group.CreateTransitionRouteGroupRequest(),
            parent="parent_value",
            transition_route_group=gcdc_transition_route_group.TransitionRouteGroup(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_create_transition_route_group_flattened_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_transition_route_group.TransitionRouteGroup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_transition_route_group.TransitionRouteGroup()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_transition_route_group(
            parent="parent_value",
            transition_route_group=gcdc_transition_route_group.TransitionRouteGroup(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[
            0
        ].transition_route_group == gcdc_transition_route_group.TransitionRouteGroup(
            name="name_value"
        )


@pytest.mark.asyncio
async def test_create_transition_route_group_flattened_error_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_transition_route_group(
            gcdc_transition_route_group.CreateTransitionRouteGroupRequest(),
            parent="parent_value",
            transition_route_group=gcdc_transition_route_group.TransitionRouteGroup(
                name="name_value"
            ),
        )


def test_update_transition_route_group(
    transport: str = "grpc",
    request_type=gcdc_transition_route_group.UpdateTransitionRouteGroupRequest,
):
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_transition_route_group.TransitionRouteGroup(
            name="name_value", display_name="display_name_value",
        )

        response = client.update_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert (
            args[0] == gcdc_transition_route_group.UpdateTransitionRouteGroupRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_transition_route_group.TransitionRouteGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_update_transition_route_group_from_dict():
    test_update_transition_route_group(request_type=dict)


@pytest.mark.asyncio
async def test_update_transition_route_group_async(transport: str = "grpc_asyncio"):
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gcdc_transition_route_group.UpdateTransitionRouteGroupRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_transition_route_group.TransitionRouteGroup(
                name="name_value", display_name="display_name_value",
            )
        )

        response = await client.update_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_transition_route_group.TransitionRouteGroup)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_update_transition_route_group_field_headers():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_transition_route_group.UpdateTransitionRouteGroupRequest()
    request.transition_route_group.name = "transition_route_group.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_transition_route_group), "__call__"
    ) as call:
        call.return_value = gcdc_transition_route_group.TransitionRouteGroup()

        client.update_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "transition_route_group.name=transition_route_group.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_transition_route_group_field_headers_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_transition_route_group.UpdateTransitionRouteGroupRequest()
    request.transition_route_group.name = "transition_route_group.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_transition_route_group), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_transition_route_group.TransitionRouteGroup()
        )

        await client.update_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "transition_route_group.name=transition_route_group.name/value",
    ) in kw["metadata"]


def test_update_transition_route_group_flattened():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_transition_route_group.TransitionRouteGroup()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_transition_route_group(
            transition_route_group=gcdc_transition_route_group.TransitionRouteGroup(
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
        ].transition_route_group == gcdc_transition_route_group.TransitionRouteGroup(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_transition_route_group_flattened_error():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_transition_route_group(
            gcdc_transition_route_group.UpdateTransitionRouteGroupRequest(),
            transition_route_group=gcdc_transition_route_group.TransitionRouteGroup(
                name="name_value"
            ),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_transition_route_group_flattened_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_transition_route_group.TransitionRouteGroup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_transition_route_group.TransitionRouteGroup()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_transition_route_group(
            transition_route_group=gcdc_transition_route_group.TransitionRouteGroup(
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
        ].transition_route_group == gcdc_transition_route_group.TransitionRouteGroup(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_transition_route_group_flattened_error_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_transition_route_group(
            gcdc_transition_route_group.UpdateTransitionRouteGroupRequest(),
            transition_route_group=gcdc_transition_route_group.TransitionRouteGroup(
                name="name_value"
            ),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_transition_route_group(
    transport: str = "grpc",
    request_type=transition_route_group.DeleteTransitionRouteGroupRequest,
):
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == transition_route_group.DeleteTransitionRouteGroupRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_transition_route_group_from_dict():
    test_delete_transition_route_group(request_type=dict)


@pytest.mark.asyncio
async def test_delete_transition_route_group_async(transport: str = "grpc_asyncio"):
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = transition_route_group.DeleteTransitionRouteGroupRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_transition_route_group_field_headers():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transition_route_group.DeleteTransitionRouteGroupRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_transition_route_group), "__call__"
    ) as call:
        call.return_value = None

        client.delete_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_transition_route_group_field_headers_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = transition_route_group.DeleteTransitionRouteGroupRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_transition_route_group), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_transition_route_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_transition_route_group_flattened():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_transition_route_group(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_transition_route_group_flattened_error():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_transition_route_group(
            transition_route_group.DeleteTransitionRouteGroupRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_transition_route_group_flattened_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_transition_route_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_transition_route_group(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_transition_route_group_flattened_error_async():
    client = TransitionRouteGroupsAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_transition_route_group(
            transition_route_group.DeleteTransitionRouteGroupRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.TransitionRouteGroupsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TransitionRouteGroupsClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.TransitionRouteGroupsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TransitionRouteGroupsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.TransitionRouteGroupsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TransitionRouteGroupsClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TransitionRouteGroupsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = TransitionRouteGroupsClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TransitionRouteGroupsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.TransitionRouteGroupsGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
    )
    assert isinstance(client._transport, transports.TransitionRouteGroupsGrpcTransport,)


def test_transition_route_groups_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.TransitionRouteGroupsTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_transition_route_groups_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.transition_route_groups.transports.TransitionRouteGroupsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.TransitionRouteGroupsTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_transition_route_groups",
        "get_transition_route_group",
        "create_transition_route_group",
        "update_transition_route_group",
        "delete_transition_route_group",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_transition_route_groups_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.transition_route_groups.transports.TransitionRouteGroupsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.TransitionRouteGroupsTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


def test_transition_route_groups_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        TransitionRouteGroupsClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


def test_transition_route_groups_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.TransitionRouteGroupsGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


def test_transition_route_groups_host_no_port():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
    )
    assert client._transport._host == "dialogflow.googleapis.com:443"


def test_transition_route_groups_host_with_port():
    client = TransitionRouteGroupsClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "dialogflow.googleapis.com:8000"


def test_transition_route_groups_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.TransitionRouteGroupsGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_transition_route_groups_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.TransitionRouteGroupsGrpcAsyncIOTransport(
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
def test_transition_route_groups_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.TransitionRouteGroupsGrpcTransport(
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
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/dialogflow",
        ),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_transition_route_groups_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.TransitionRouteGroupsGrpcAsyncIOTransport(
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
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/dialogflow",
        ),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_transition_route_groups_grpc_transport_channel_mtls_with_adc(
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
        transport = transports.TransitionRouteGroupsGrpcTransport(
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
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_transition_route_groups_grpc_asyncio_transport_channel_mtls_with_adc(
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
        transport = transports.TransitionRouteGroupsGrpcAsyncIOTransport(
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
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_transition_route_group_path():
    project = "squid"
    location = "clam"
    agent = "whelk"
    flow = "octopus"
    transition_route_group = "oyster"

    expected = "projects/{project}/locations/{location}/agents/{agent}/flows/{flow}/transitionRouteGroups/{transition_route_group}".format(
        project=project,
        location=location,
        agent=agent,
        flow=flow,
        transition_route_group=transition_route_group,
    )
    actual = TransitionRouteGroupsClient.transition_route_group_path(
        project, location, agent, flow, transition_route_group
    )
    assert expected == actual


def test_parse_transition_route_group_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "agent": "mussel",
        "flow": "winkle",
        "transition_route_group": "nautilus",
    }
    path = TransitionRouteGroupsClient.transition_route_group_path(**expected)

    # Check that the path construction is reversible.
    actual = TransitionRouteGroupsClient.parse_transition_route_group_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.TransitionRouteGroupsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = TransitionRouteGroupsClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.TransitionRouteGroupsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = TransitionRouteGroupsClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
