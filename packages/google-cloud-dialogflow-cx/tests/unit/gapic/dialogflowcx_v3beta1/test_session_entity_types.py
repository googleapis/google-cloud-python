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
from google.cloud.dialogflowcx_v3beta1.services.session_entity_types import (
    SessionEntityTypesAsyncClient,
)
from google.cloud.dialogflowcx_v3beta1.services.session_entity_types import (
    SessionEntityTypesClient,
)
from google.cloud.dialogflowcx_v3beta1.services.session_entity_types import pagers
from google.cloud.dialogflowcx_v3beta1.services.session_entity_types import transports
from google.cloud.dialogflowcx_v3beta1.types import entity_type
from google.cloud.dialogflowcx_v3beta1.types import entity_type as gcdc_entity_type
from google.cloud.dialogflowcx_v3beta1.types import session_entity_type
from google.cloud.dialogflowcx_v3beta1.types import (
    session_entity_type as gcdc_session_entity_type,
)
from google.oauth2 import service_account
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

    assert SessionEntityTypesClient._get_default_mtls_endpoint(None) is None
    assert (
        SessionEntityTypesClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SessionEntityTypesClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SessionEntityTypesClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SessionEntityTypesClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SessionEntityTypesClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [SessionEntityTypesClient, SessionEntityTypesAsyncClient]
)
def test_session_entity_types_client_from_service_account_file(client_class):
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


def test_session_entity_types_client_get_transport_class():
    transport = SessionEntityTypesClient.get_transport_class()
    assert transport == transports.SessionEntityTypesGrpcTransport

    transport = SessionEntityTypesClient.get_transport_class("grpc")
    assert transport == transports.SessionEntityTypesGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SessionEntityTypesClient, transports.SessionEntityTypesGrpcTransport, "grpc"),
        (
            SessionEntityTypesAsyncClient,
            transports.SessionEntityTypesGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    SessionEntityTypesClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SessionEntityTypesClient),
)
@mock.patch.object(
    SessionEntityTypesAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SessionEntityTypesAsyncClient),
)
def test_session_entity_types_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(SessionEntityTypesClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(SessionEntityTypesClient, "get_transport_class") as gtc:
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
        (SessionEntityTypesClient, transports.SessionEntityTypesGrpcTransport, "grpc"),
        (
            SessionEntityTypesAsyncClient,
            transports.SessionEntityTypesGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_session_entity_types_client_client_options_scopes(
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
        (SessionEntityTypesClient, transports.SessionEntityTypesGrpcTransport, "grpc"),
        (
            SessionEntityTypesAsyncClient,
            transports.SessionEntityTypesGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_session_entity_types_client_client_options_credentials_file(
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


def test_session_entity_types_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.session_entity_types.transports.SessionEntityTypesGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = SessionEntityTypesClient(
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


def test_list_session_entity_types(
    transport: str = "grpc",
    request_type=session_entity_type.ListSessionEntityTypesRequest,
):
    client = SessionEntityTypesClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_session_entity_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = session_entity_type.ListSessionEntityTypesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_session_entity_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == session_entity_type.ListSessionEntityTypesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSessionEntityTypesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_session_entity_types_from_dict():
    test_list_session_entity_types(request_type=dict)


@pytest.mark.asyncio
async def test_list_session_entity_types_async(transport: str = "grpc_asyncio"):
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = session_entity_type.ListSessionEntityTypesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_session_entity_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session_entity_type.ListSessionEntityTypesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_session_entity_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSessionEntityTypesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_session_entity_types_field_headers():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session_entity_type.ListSessionEntityTypesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_session_entity_types), "__call__"
    ) as call:
        call.return_value = session_entity_type.ListSessionEntityTypesResponse()

        client.list_session_entity_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_session_entity_types_field_headers_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session_entity_type.ListSessionEntityTypesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_session_entity_types), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session_entity_type.ListSessionEntityTypesResponse()
        )

        await client.list_session_entity_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_session_entity_types_flattened():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_session_entity_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = session_entity_type.ListSessionEntityTypesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_session_entity_types(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_session_entity_types_flattened_error():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_session_entity_types(
            session_entity_type.ListSessionEntityTypesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_session_entity_types_flattened_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_session_entity_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = session_entity_type.ListSessionEntityTypesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session_entity_type.ListSessionEntityTypesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_session_entity_types(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_session_entity_types_flattened_error_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_session_entity_types(
            session_entity_type.ListSessionEntityTypesRequest(), parent="parent_value",
        )


def test_list_session_entity_types_pager():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_session_entity_types), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                ],
                next_page_token="abc",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[], next_page_token="def",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[session_entity_type.SessionEntityType(),],
                next_page_token="ghi",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_session_entity_types(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, session_entity_type.SessionEntityType) for i in results
        )


def test_list_session_entity_types_pages():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_session_entity_types), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                ],
                next_page_token="abc",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[], next_page_token="def",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[session_entity_type.SessionEntityType(),],
                next_page_token="ghi",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_session_entity_types(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_session_entity_types_async_pager():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_session_entity_types),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                ],
                next_page_token="abc",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[], next_page_token="def",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[session_entity_type.SessionEntityType(),],
                next_page_token="ghi",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_session_entity_types(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, session_entity_type.SessionEntityType) for i in responses
        )


@pytest.mark.asyncio
async def test_list_session_entity_types_async_pages():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_session_entity_types),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                ],
                next_page_token="abc",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[], next_page_token="def",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[session_entity_type.SessionEntityType(),],
                next_page_token="ghi",
            ),
            session_entity_type.ListSessionEntityTypesResponse(
                session_entity_types=[
                    session_entity_type.SessionEntityType(),
                    session_entity_type.SessionEntityType(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_session_entity_types(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_session_entity_type(
    transport: str = "grpc",
    request_type=session_entity_type.GetSessionEntityTypeRequest,
):
    client = SessionEntityTypesClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = session_entity_type.SessionEntityType(
            name="name_value",
            entity_override_mode=session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE,
        )

        response = client.get_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == session_entity_type.GetSessionEntityTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, session_entity_type.SessionEntityType)

    assert response.name == "name_value"

    assert (
        response.entity_override_mode
        == session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE
    )


def test_get_session_entity_type_from_dict():
    test_get_session_entity_type(request_type=dict)


@pytest.mark.asyncio
async def test_get_session_entity_type_async(transport: str = "grpc_asyncio"):
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = session_entity_type.GetSessionEntityTypeRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session_entity_type.SessionEntityType(
                name="name_value",
                entity_override_mode=session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE,
            )
        )

        response = await client.get_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, session_entity_type.SessionEntityType)

    assert response.name == "name_value"

    assert (
        response.entity_override_mode
        == session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE
    )


def test_get_session_entity_type_field_headers():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session_entity_type.GetSessionEntityTypeRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_session_entity_type), "__call__"
    ) as call:
        call.return_value = session_entity_type.SessionEntityType()

        client.get_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_session_entity_type_field_headers_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session_entity_type.GetSessionEntityTypeRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_session_entity_type), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session_entity_type.SessionEntityType()
        )

        await client.get_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_session_entity_type_flattened():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = session_entity_type.SessionEntityType()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_session_entity_type(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_session_entity_type_flattened_error():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_session_entity_type(
            session_entity_type.GetSessionEntityTypeRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_session_entity_type_flattened_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = session_entity_type.SessionEntityType()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session_entity_type.SessionEntityType()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_session_entity_type(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_session_entity_type_flattened_error_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_session_entity_type(
            session_entity_type.GetSessionEntityTypeRequest(), name="name_value",
        )


def test_create_session_entity_type(
    transport: str = "grpc",
    request_type=gcdc_session_entity_type.CreateSessionEntityTypeRequest,
):
    client = SessionEntityTypesClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_session_entity_type.SessionEntityType(
            name="name_value",
            entity_override_mode=gcdc_session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE,
        )

        response = client.create_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == gcdc_session_entity_type.CreateSessionEntityTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_session_entity_type.SessionEntityType)

    assert response.name == "name_value"

    assert (
        response.entity_override_mode
        == gcdc_session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE
    )


def test_create_session_entity_type_from_dict():
    test_create_session_entity_type(request_type=dict)


@pytest.mark.asyncio
async def test_create_session_entity_type_async(transport: str = "grpc_asyncio"):
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gcdc_session_entity_type.CreateSessionEntityTypeRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_session_entity_type.SessionEntityType(
                name="name_value",
                entity_override_mode=gcdc_session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE,
            )
        )

        response = await client.create_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_session_entity_type.SessionEntityType)

    assert response.name == "name_value"

    assert (
        response.entity_override_mode
        == gcdc_session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE
    )


def test_create_session_entity_type_field_headers():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_session_entity_type.CreateSessionEntityTypeRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_session_entity_type), "__call__"
    ) as call:
        call.return_value = gcdc_session_entity_type.SessionEntityType()

        client.create_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_session_entity_type_field_headers_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_session_entity_type.CreateSessionEntityTypeRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_session_entity_type), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_session_entity_type.SessionEntityType()
        )

        await client.create_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_session_entity_type_flattened():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_session_entity_type.SessionEntityType()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_session_entity_type(
            parent="parent_value",
            session_entity_type=gcdc_session_entity_type.SessionEntityType(
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
        ].session_entity_type == gcdc_session_entity_type.SessionEntityType(
            name="name_value"
        )


def test_create_session_entity_type_flattened_error():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_session_entity_type(
            gcdc_session_entity_type.CreateSessionEntityTypeRequest(),
            parent="parent_value",
            session_entity_type=gcdc_session_entity_type.SessionEntityType(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_create_session_entity_type_flattened_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_session_entity_type.SessionEntityType()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_session_entity_type.SessionEntityType()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_session_entity_type(
            parent="parent_value",
            session_entity_type=gcdc_session_entity_type.SessionEntityType(
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
        ].session_entity_type == gcdc_session_entity_type.SessionEntityType(
            name="name_value"
        )


@pytest.mark.asyncio
async def test_create_session_entity_type_flattened_error_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_session_entity_type(
            gcdc_session_entity_type.CreateSessionEntityTypeRequest(),
            parent="parent_value",
            session_entity_type=gcdc_session_entity_type.SessionEntityType(
                name="name_value"
            ),
        )


def test_update_session_entity_type(
    transport: str = "grpc",
    request_type=gcdc_session_entity_type.UpdateSessionEntityTypeRequest,
):
    client = SessionEntityTypesClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_session_entity_type.SessionEntityType(
            name="name_value",
            entity_override_mode=gcdc_session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE,
        )

        response = client.update_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == gcdc_session_entity_type.UpdateSessionEntityTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_session_entity_type.SessionEntityType)

    assert response.name == "name_value"

    assert (
        response.entity_override_mode
        == gcdc_session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE
    )


def test_update_session_entity_type_from_dict():
    test_update_session_entity_type(request_type=dict)


@pytest.mark.asyncio
async def test_update_session_entity_type_async(transport: str = "grpc_asyncio"):
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gcdc_session_entity_type.UpdateSessionEntityTypeRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_session_entity_type.SessionEntityType(
                name="name_value",
                entity_override_mode=gcdc_session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE,
            )
        )

        response = await client.update_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_session_entity_type.SessionEntityType)

    assert response.name == "name_value"

    assert (
        response.entity_override_mode
        == gcdc_session_entity_type.SessionEntityType.EntityOverrideMode.ENTITY_OVERRIDE_MODE_OVERRIDE
    )


def test_update_session_entity_type_field_headers():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_session_entity_type.UpdateSessionEntityTypeRequest()
    request.session_entity_type.name = "session_entity_type.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_session_entity_type), "__call__"
    ) as call:
        call.return_value = gcdc_session_entity_type.SessionEntityType()

        client.update_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "session_entity_type.name=session_entity_type.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_session_entity_type_field_headers_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_session_entity_type.UpdateSessionEntityTypeRequest()
    request.session_entity_type.name = "session_entity_type.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_session_entity_type), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_session_entity_type.SessionEntityType()
        )

        await client.update_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "session_entity_type.name=session_entity_type.name/value",
    ) in kw["metadata"]


def test_update_session_entity_type_flattened():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_session_entity_type.SessionEntityType()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_session_entity_type(
            session_entity_type=gcdc_session_entity_type.SessionEntityType(
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
        ].session_entity_type == gcdc_session_entity_type.SessionEntityType(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_session_entity_type_flattened_error():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_session_entity_type(
            gcdc_session_entity_type.UpdateSessionEntityTypeRequest(),
            session_entity_type=gcdc_session_entity_type.SessionEntityType(
                name="name_value"
            ),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_session_entity_type_flattened_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_session_entity_type.SessionEntityType()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_session_entity_type.SessionEntityType()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_session_entity_type(
            session_entity_type=gcdc_session_entity_type.SessionEntityType(
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
        ].session_entity_type == gcdc_session_entity_type.SessionEntityType(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_session_entity_type_flattened_error_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_session_entity_type(
            gcdc_session_entity_type.UpdateSessionEntityTypeRequest(),
            session_entity_type=gcdc_session_entity_type.SessionEntityType(
                name="name_value"
            ),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_session_entity_type(
    transport: str = "grpc",
    request_type=session_entity_type.DeleteSessionEntityTypeRequest,
):
    client = SessionEntityTypesClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == session_entity_type.DeleteSessionEntityTypeRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_session_entity_type_from_dict():
    test_delete_session_entity_type(request_type=dict)


@pytest.mark.asyncio
async def test_delete_session_entity_type_async(transport: str = "grpc_asyncio"):
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = session_entity_type.DeleteSessionEntityTypeRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_session_entity_type_field_headers():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session_entity_type.DeleteSessionEntityTypeRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_session_entity_type), "__call__"
    ) as call:
        call.return_value = None

        client.delete_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_session_entity_type_field_headers_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session_entity_type.DeleteSessionEntityTypeRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_session_entity_type), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_session_entity_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_session_entity_type_flattened():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_session_entity_type(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_session_entity_type_flattened_error():
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_session_entity_type(
            session_entity_type.DeleteSessionEntityTypeRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_session_entity_type_flattened_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_session_entity_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_session_entity_type(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_session_entity_type_flattened_error_async():
    client = SessionEntityTypesAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_session_entity_type(
            session_entity_type.DeleteSessionEntityTypeRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SessionEntityTypesGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SessionEntityTypesClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.SessionEntityTypesGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SessionEntityTypesClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.SessionEntityTypesGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SessionEntityTypesClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SessionEntityTypesGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = SessionEntityTypesClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SessionEntityTypesGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.SessionEntityTypesGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = SessionEntityTypesClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.SessionEntityTypesGrpcTransport,)


def test_session_entity_types_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.SessionEntityTypesTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_session_entity_types_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.session_entity_types.transports.SessionEntityTypesTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.SessionEntityTypesTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_session_entity_types",
        "get_session_entity_type",
        "create_session_entity_type",
        "update_session_entity_type",
        "delete_session_entity_type",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_session_entity_types_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.session_entity_types.transports.SessionEntityTypesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.SessionEntityTypesTransport(
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


def test_session_entity_types_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        SessionEntityTypesClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


def test_session_entity_types_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.SessionEntityTypesGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


def test_session_entity_types_host_no_port():
    client = SessionEntityTypesClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
    )
    assert client._transport._host == "dialogflow.googleapis.com:443"


def test_session_entity_types_host_with_port():
    client = SessionEntityTypesClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "dialogflow.googleapis.com:8000"


def test_session_entity_types_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.SessionEntityTypesGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_session_entity_types_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.SessionEntityTypesGrpcAsyncIOTransport(
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
def test_session_entity_types_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.SessionEntityTypesGrpcTransport(
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
def test_session_entity_types_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.SessionEntityTypesGrpcAsyncIOTransport(
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
def test_session_entity_types_grpc_transport_channel_mtls_with_adc(
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
        transport = transports.SessionEntityTypesGrpcTransport(
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
def test_session_entity_types_grpc_asyncio_transport_channel_mtls_with_adc(
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
        transport = transports.SessionEntityTypesGrpcAsyncIOTransport(
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


def test_session_entity_type_path():
    project = "squid"
    location = "clam"
    agent = "whelk"
    session = "octopus"
    entity_type = "oyster"

    expected = "projects/{project}/locations/{location}/agents/{agent}/sessions/{session}/entityTypes/{entity_type}".format(
        project=project,
        location=location,
        agent=agent,
        session=session,
        entity_type=entity_type,
    )
    actual = SessionEntityTypesClient.session_entity_type_path(
        project, location, agent, session, entity_type
    )
    assert expected == actual


def test_parse_session_entity_type_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "agent": "mussel",
        "session": "winkle",
        "entity_type": "nautilus",
    }
    path = SessionEntityTypesClient.session_entity_type_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionEntityTypesClient.parse_session_entity_type_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.SessionEntityTypesTransport, "_prep_wrapped_messages"
    ) as prep:
        client = SessionEntityTypesClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.SessionEntityTypesTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = SessionEntityTypesClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
