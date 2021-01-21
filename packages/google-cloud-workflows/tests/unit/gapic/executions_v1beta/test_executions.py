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
from google.cloud.workflows.executions_v1beta.services.executions import (
    ExecutionsAsyncClient,
)
from google.cloud.workflows.executions_v1beta.services.executions import (
    ExecutionsClient,
)
from google.cloud.workflows.executions_v1beta.services.executions import pagers
from google.cloud.workflows.executions_v1beta.services.executions import transports
from google.cloud.workflows.executions_v1beta.types import executions
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


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

    assert ExecutionsClient._get_default_mtls_endpoint(None) is None
    assert (
        ExecutionsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        ExecutionsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ExecutionsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ExecutionsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert ExecutionsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test_executions_client_from_service_account_info():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = ExecutionsClient.from_service_account_info(info)
        assert client.transport._credentials == creds

        assert client.transport._host == "workflowexecutions.googleapis.com:443"


@pytest.mark.parametrize("client_class", [ExecutionsClient, ExecutionsAsyncClient,])
def test_executions_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "workflowexecutions.googleapis.com:443"


def test_executions_client_get_transport_class():
    transport = ExecutionsClient.get_transport_class()
    available_transports = [
        transports.ExecutionsGrpcTransport,
    ]
    assert transport in available_transports

    transport = ExecutionsClient.get_transport_class("grpc")
    assert transport == transports.ExecutionsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ExecutionsClient, transports.ExecutionsGrpcTransport, "grpc"),
        (
            ExecutionsAsyncClient,
            transports.ExecutionsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ExecutionsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ExecutionsClient)
)
@mock.patch.object(
    ExecutionsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ExecutionsAsyncClient),
)
def test_executions_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ExecutionsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ExecutionsClient, "get_transport_class") as gtc:
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
        (ExecutionsClient, transports.ExecutionsGrpcTransport, "grpc", "true"),
        (
            ExecutionsAsyncClient,
            transports.ExecutionsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ExecutionsClient, transports.ExecutionsGrpcTransport, "grpc", "false"),
        (
            ExecutionsAsyncClient,
            transports.ExecutionsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ExecutionsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ExecutionsClient)
)
@mock.patch.object(
    ExecutionsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ExecutionsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_executions_client_mtls_env_auto(
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
        (ExecutionsClient, transports.ExecutionsGrpcTransport, "grpc"),
        (
            ExecutionsAsyncClient,
            transports.ExecutionsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_executions_client_client_options_scopes(
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
        (ExecutionsClient, transports.ExecutionsGrpcTransport, "grpc"),
        (
            ExecutionsAsyncClient,
            transports.ExecutionsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_executions_client_client_options_credentials_file(
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


def test_executions_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.workflows.executions_v1beta.services.executions.transports.ExecutionsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ExecutionsClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_list_executions(
    transport: str = "grpc", request_type=executions.ListExecutionsRequest
):
    client = ExecutionsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_executions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.ListExecutionsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_executions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == executions.ListExecutionsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListExecutionsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_executions_from_dict():
    test_list_executions(request_type=dict)


@pytest.mark.asyncio
async def test_list_executions_async(
    transport: str = "grpc_asyncio", request_type=executions.ListExecutionsRequest
):
    client = ExecutionsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_executions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.ListExecutionsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_executions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == executions.ListExecutionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListExecutionsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_executions_async_from_dict():
    await test_list_executions_async(request_type=dict)


def test_list_executions_field_headers():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = executions.ListExecutionsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_executions), "__call__") as call:
        call.return_value = executions.ListExecutionsResponse()

        client.list_executions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_executions_field_headers_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = executions.ListExecutionsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_executions), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.ListExecutionsResponse()
        )

        await client.list_executions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_executions_flattened():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_executions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.ListExecutionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_executions(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_executions_flattened_error():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_executions(
            executions.ListExecutionsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_executions_flattened_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_executions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.ListExecutionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.ListExecutionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_executions(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_executions_flattened_error_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_executions(
            executions.ListExecutionsRequest(), parent="parent_value",
        )


def test_list_executions_pager():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_executions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            executions.ListExecutionsResponse(
                executions=[
                    executions.Execution(),
                    executions.Execution(),
                    executions.Execution(),
                ],
                next_page_token="abc",
            ),
            executions.ListExecutionsResponse(executions=[], next_page_token="def",),
            executions.ListExecutionsResponse(
                executions=[executions.Execution(),], next_page_token="ghi",
            ),
            executions.ListExecutionsResponse(
                executions=[executions.Execution(), executions.Execution(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_executions(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, executions.Execution) for i in results)


def test_list_executions_pages():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_executions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            executions.ListExecutionsResponse(
                executions=[
                    executions.Execution(),
                    executions.Execution(),
                    executions.Execution(),
                ],
                next_page_token="abc",
            ),
            executions.ListExecutionsResponse(executions=[], next_page_token="def",),
            executions.ListExecutionsResponse(
                executions=[executions.Execution(),], next_page_token="ghi",
            ),
            executions.ListExecutionsResponse(
                executions=[executions.Execution(), executions.Execution(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_executions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_executions_async_pager():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_executions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            executions.ListExecutionsResponse(
                executions=[
                    executions.Execution(),
                    executions.Execution(),
                    executions.Execution(),
                ],
                next_page_token="abc",
            ),
            executions.ListExecutionsResponse(executions=[], next_page_token="def",),
            executions.ListExecutionsResponse(
                executions=[executions.Execution(),], next_page_token="ghi",
            ),
            executions.ListExecutionsResponse(
                executions=[executions.Execution(), executions.Execution(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_executions(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, executions.Execution) for i in responses)


@pytest.mark.asyncio
async def test_list_executions_async_pages():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_executions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            executions.ListExecutionsResponse(
                executions=[
                    executions.Execution(),
                    executions.Execution(),
                    executions.Execution(),
                ],
                next_page_token="abc",
            ),
            executions.ListExecutionsResponse(executions=[], next_page_token="def",),
            executions.ListExecutionsResponse(
                executions=[executions.Execution(),], next_page_token="ghi",
            ),
            executions.ListExecutionsResponse(
                executions=[executions.Execution(), executions.Execution(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_executions(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_execution(
    transport: str = "grpc", request_type=executions.CreateExecutionRequest
):
    client = ExecutionsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.Execution(
            name="name_value",
            state=executions.Execution.State.ACTIVE,
            argument="argument_value",
            result="result_value",
            workflow_revision_id="workflow_revision_id_value",
        )

        response = client.create_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == executions.CreateExecutionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, executions.Execution)

    assert response.name == "name_value"

    assert response.state == executions.Execution.State.ACTIVE

    assert response.argument == "argument_value"

    assert response.result == "result_value"

    assert response.workflow_revision_id == "workflow_revision_id_value"


def test_create_execution_from_dict():
    test_create_execution(request_type=dict)


@pytest.mark.asyncio
async def test_create_execution_async(
    transport: str = "grpc_asyncio", request_type=executions.CreateExecutionRequest
):
    client = ExecutionsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.Execution(
                name="name_value",
                state=executions.Execution.State.ACTIVE,
                argument="argument_value",
                result="result_value",
                workflow_revision_id="workflow_revision_id_value",
            )
        )

        response = await client.create_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == executions.CreateExecutionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, executions.Execution)

    assert response.name == "name_value"

    assert response.state == executions.Execution.State.ACTIVE

    assert response.argument == "argument_value"

    assert response.result == "result_value"

    assert response.workflow_revision_id == "workflow_revision_id_value"


@pytest.mark.asyncio
async def test_create_execution_async_from_dict():
    await test_create_execution_async(request_type=dict)


def test_create_execution_field_headers():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = executions.CreateExecutionRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_execution), "__call__") as call:
        call.return_value = executions.Execution()

        client.create_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_execution_field_headers_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = executions.CreateExecutionRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_execution), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.Execution()
        )

        await client.create_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_execution_flattened():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.Execution()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_execution(
            parent="parent_value", execution=executions.Execution(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].execution == executions.Execution(name="name_value")


def test_create_execution_flattened_error():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_execution(
            executions.CreateExecutionRequest(),
            parent="parent_value",
            execution=executions.Execution(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_execution_flattened_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.Execution()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.Execution()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_execution(
            parent="parent_value", execution=executions.Execution(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].execution == executions.Execution(name="name_value")


@pytest.mark.asyncio
async def test_create_execution_flattened_error_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_execution(
            executions.CreateExecutionRequest(),
            parent="parent_value",
            execution=executions.Execution(name="name_value"),
        )


def test_get_execution(
    transport: str = "grpc", request_type=executions.GetExecutionRequest
):
    client = ExecutionsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.Execution(
            name="name_value",
            state=executions.Execution.State.ACTIVE,
            argument="argument_value",
            result="result_value",
            workflow_revision_id="workflow_revision_id_value",
        )

        response = client.get_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == executions.GetExecutionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, executions.Execution)

    assert response.name == "name_value"

    assert response.state == executions.Execution.State.ACTIVE

    assert response.argument == "argument_value"

    assert response.result == "result_value"

    assert response.workflow_revision_id == "workflow_revision_id_value"


def test_get_execution_from_dict():
    test_get_execution(request_type=dict)


@pytest.mark.asyncio
async def test_get_execution_async(
    transport: str = "grpc_asyncio", request_type=executions.GetExecutionRequest
):
    client = ExecutionsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.Execution(
                name="name_value",
                state=executions.Execution.State.ACTIVE,
                argument="argument_value",
                result="result_value",
                workflow_revision_id="workflow_revision_id_value",
            )
        )

        response = await client.get_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == executions.GetExecutionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, executions.Execution)

    assert response.name == "name_value"

    assert response.state == executions.Execution.State.ACTIVE

    assert response.argument == "argument_value"

    assert response.result == "result_value"

    assert response.workflow_revision_id == "workflow_revision_id_value"


@pytest.mark.asyncio
async def test_get_execution_async_from_dict():
    await test_get_execution_async(request_type=dict)


def test_get_execution_field_headers():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = executions.GetExecutionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_execution), "__call__") as call:
        call.return_value = executions.Execution()

        client.get_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_execution_field_headers_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = executions.GetExecutionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_execution), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.Execution()
        )

        await client.get_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_execution_flattened():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.Execution()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_execution(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_execution_flattened_error():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_execution(
            executions.GetExecutionRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_execution_flattened_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.Execution()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.Execution()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_execution(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_execution_flattened_error_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_execution(
            executions.GetExecutionRequest(), name="name_value",
        )


def test_cancel_execution(
    transport: str = "grpc", request_type=executions.CancelExecutionRequest
):
    client = ExecutionsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.Execution(
            name="name_value",
            state=executions.Execution.State.ACTIVE,
            argument="argument_value",
            result="result_value",
            workflow_revision_id="workflow_revision_id_value",
        )

        response = client.cancel_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == executions.CancelExecutionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, executions.Execution)

    assert response.name == "name_value"

    assert response.state == executions.Execution.State.ACTIVE

    assert response.argument == "argument_value"

    assert response.result == "result_value"

    assert response.workflow_revision_id == "workflow_revision_id_value"


def test_cancel_execution_from_dict():
    test_cancel_execution(request_type=dict)


@pytest.mark.asyncio
async def test_cancel_execution_async(
    transport: str = "grpc_asyncio", request_type=executions.CancelExecutionRequest
):
    client = ExecutionsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.Execution(
                name="name_value",
                state=executions.Execution.State.ACTIVE,
                argument="argument_value",
                result="result_value",
                workflow_revision_id="workflow_revision_id_value",
            )
        )

        response = await client.cancel_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == executions.CancelExecutionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, executions.Execution)

    assert response.name == "name_value"

    assert response.state == executions.Execution.State.ACTIVE

    assert response.argument == "argument_value"

    assert response.result == "result_value"

    assert response.workflow_revision_id == "workflow_revision_id_value"


@pytest.mark.asyncio
async def test_cancel_execution_async_from_dict():
    await test_cancel_execution_async(request_type=dict)


def test_cancel_execution_field_headers():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = executions.CancelExecutionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_execution), "__call__") as call:
        call.return_value = executions.Execution()

        client.cancel_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_execution_field_headers_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = executions.CancelExecutionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_execution), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.Execution()
        )

        await client.cancel_execution(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_cancel_execution_flattened():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.Execution()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_execution(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_cancel_execution_flattened_error():
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_execution(
            executions.CancelExecutionRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_cancel_execution_flattened_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_execution), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = executions.Execution()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            executions.Execution()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_execution(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_cancel_execution_flattened_error_async():
    client = ExecutionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_execution(
            executions.CancelExecutionRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ExecutionsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ExecutionsClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ExecutionsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ExecutionsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ExecutionsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ExecutionsClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ExecutionsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = ExecutionsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ExecutionsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ExecutionsGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.ExecutionsGrpcTransport, transports.ExecutionsGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ExecutionsClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.ExecutionsGrpcTransport,)


def test_executions_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.ExecutionsTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_executions_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.workflows.executions_v1beta.services.executions.transports.ExecutionsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ExecutionsTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_executions",
        "create_execution",
        "get_execution",
        "cancel_execution",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_executions_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.workflows.executions_v1beta.services.executions.transports.ExecutionsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.ExecutionsTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_executions_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.workflows.executions_v1beta.services.executions.transports.ExecutionsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.ExecutionsTransport()
        adc.assert_called_once()


def test_executions_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        ExecutionsClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_executions_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.ExecutionsGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_executions_host_no_port():
    client = ExecutionsClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="workflowexecutions.googleapis.com"
        ),
    )
    assert client.transport._host == "workflowexecutions.googleapis.com:443"


def test_executions_host_with_port():
    client = ExecutionsClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="workflowexecutions.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "workflowexecutions.googleapis.com:8000"


def test_executions_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ExecutionsGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_executions_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ExecutionsGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [transports.ExecutionsGrpcTransport, transports.ExecutionsGrpcAsyncIOTransport],
)
def test_executions_transport_channel_mtls_with_client_cert_source(transport_class):
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
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [transports.ExecutionsGrpcTransport, transports.ExecutionsGrpcAsyncIOTransport],
)
def test_executions_transport_channel_mtls_with_adc(transport_class):
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
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_execution_path():
    project = "squid"
    location = "clam"
    workflow = "whelk"
    execution = "octopus"

    expected = "projects/{project}/locations/{location}/workflows/{workflow}/executions/{execution}".format(
        project=project, location=location, workflow=workflow, execution=execution,
    )
    actual = ExecutionsClient.execution_path(project, location, workflow, execution)
    assert expected == actual


def test_parse_execution_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "workflow": "cuttlefish",
        "execution": "mussel",
    }
    path = ExecutionsClient.execution_path(**expected)

    # Check that the path construction is reversible.
    actual = ExecutionsClient.parse_execution_path(path)
    assert expected == actual


def test_workflow_path():
    project = "winkle"
    location = "nautilus"
    workflow = "scallop"

    expected = "projects/{project}/locations/{location}/workflows/{workflow}".format(
        project=project, location=location, workflow=workflow,
    )
    actual = ExecutionsClient.workflow_path(project, location, workflow)
    assert expected == actual


def test_parse_workflow_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "workflow": "clam",
    }
    path = ExecutionsClient.workflow_path(**expected)

    # Check that the path construction is reversible.
    actual = ExecutionsClient.parse_workflow_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ExecutionsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = ExecutionsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ExecutionsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"

    expected = "folders/{folder}".format(folder=folder,)
    actual = ExecutionsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = ExecutionsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ExecutionsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = ExecutionsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = ExecutionsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ExecutionsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"

    expected = "projects/{project}".format(project=project,)
    actual = ExecutionsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = ExecutionsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ExecutionsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = ExecutionsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = ExecutionsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ExecutionsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ExecutionsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ExecutionsClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ExecutionsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ExecutionsClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
