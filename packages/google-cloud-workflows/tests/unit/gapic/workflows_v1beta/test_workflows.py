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
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.workflows_v1beta.services.workflows import WorkflowsAsyncClient
from google.cloud.workflows_v1beta.services.workflows import WorkflowsClient
from google.cloud.workflows_v1beta.services.workflows import pagers
from google.cloud.workflows_v1beta.services.workflows import transports
from google.cloud.workflows_v1beta.types import workflows
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
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

    assert WorkflowsClient._get_default_mtls_endpoint(None) is None
    assert WorkflowsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        WorkflowsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        WorkflowsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        WorkflowsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert WorkflowsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test_workflows_client_from_service_account_info():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = WorkflowsClient.from_service_account_info(info)
        assert client.transport._credentials == creds

        assert client.transport._host == "workflows.googleapis.com:443"


@pytest.mark.parametrize("client_class", [WorkflowsClient, WorkflowsAsyncClient,])
def test_workflows_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "workflows.googleapis.com:443"


def test_workflows_client_get_transport_class():
    transport = WorkflowsClient.get_transport_class()
    available_transports = [
        transports.WorkflowsGrpcTransport,
    ]
    assert transport in available_transports

    transport = WorkflowsClient.get_transport_class("grpc")
    assert transport == transports.WorkflowsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (WorkflowsClient, transports.WorkflowsGrpcTransport, "grpc"),
        (
            WorkflowsAsyncClient,
            transports.WorkflowsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    WorkflowsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(WorkflowsClient)
)
@mock.patch.object(
    WorkflowsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(WorkflowsAsyncClient),
)
def test_workflows_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(WorkflowsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(WorkflowsClient, "get_transport_class") as gtc:
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
        (WorkflowsClient, transports.WorkflowsGrpcTransport, "grpc", "true"),
        (
            WorkflowsAsyncClient,
            transports.WorkflowsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (WorkflowsClient, transports.WorkflowsGrpcTransport, "grpc", "false"),
        (
            WorkflowsAsyncClient,
            transports.WorkflowsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    WorkflowsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(WorkflowsClient)
)
@mock.patch.object(
    WorkflowsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(WorkflowsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_workflows_client_mtls_env_auto(
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
        (WorkflowsClient, transports.WorkflowsGrpcTransport, "grpc"),
        (
            WorkflowsAsyncClient,
            transports.WorkflowsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_workflows_client_client_options_scopes(
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
        (WorkflowsClient, transports.WorkflowsGrpcTransport, "grpc"),
        (
            WorkflowsAsyncClient,
            transports.WorkflowsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_workflows_client_client_options_credentials_file(
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


def test_workflows_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.workflows_v1beta.services.workflows.transports.WorkflowsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = WorkflowsClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_list_workflows(
    transport: str = "grpc", request_type=workflows.ListWorkflowsRequest
):
    client = WorkflowsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workflows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflows.ListWorkflowsResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )

        response = client.list_workflows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == workflows.ListWorkflowsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListWorkflowsPager)

    assert response.next_page_token == "next_page_token_value"

    assert response.unreachable == ["unreachable_value"]


def test_list_workflows_from_dict():
    test_list_workflows(request_type=dict)


@pytest.mark.asyncio
async def test_list_workflows_async(
    transport: str = "grpc_asyncio", request_type=workflows.ListWorkflowsRequest
):
    client = WorkflowsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workflows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflows.ListWorkflowsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )

        response = await client.list_workflows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == workflows.ListWorkflowsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkflowsAsyncPager)

    assert response.next_page_token == "next_page_token_value"

    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_workflows_async_from_dict():
    await test_list_workflows_async(request_type=dict)


def test_list_workflows_field_headers():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflows.ListWorkflowsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workflows), "__call__") as call:
        call.return_value = workflows.ListWorkflowsResponse()

        client.list_workflows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_workflows_field_headers_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflows.ListWorkflowsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workflows), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflows.ListWorkflowsResponse()
        )

        await client.list_workflows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_workflows_flattened():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workflows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflows.ListWorkflowsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_workflows(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_workflows_flattened_error():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_workflows(
            workflows.ListWorkflowsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_workflows_flattened_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workflows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflows.ListWorkflowsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflows.ListWorkflowsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_workflows(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_workflows_flattened_error_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_workflows(
            workflows.ListWorkflowsRequest(), parent="parent_value",
        )


def test_list_workflows_pager():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workflows), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            workflows.ListWorkflowsResponse(
                workflows=[
                    workflows.Workflow(),
                    workflows.Workflow(),
                    workflows.Workflow(),
                ],
                next_page_token="abc",
            ),
            workflows.ListWorkflowsResponse(workflows=[], next_page_token="def",),
            workflows.ListWorkflowsResponse(
                workflows=[workflows.Workflow(),], next_page_token="ghi",
            ),
            workflows.ListWorkflowsResponse(
                workflows=[workflows.Workflow(), workflows.Workflow(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_workflows(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, workflows.Workflow) for i in results)


def test_list_workflows_pages():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workflows), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            workflows.ListWorkflowsResponse(
                workflows=[
                    workflows.Workflow(),
                    workflows.Workflow(),
                    workflows.Workflow(),
                ],
                next_page_token="abc",
            ),
            workflows.ListWorkflowsResponse(workflows=[], next_page_token="def",),
            workflows.ListWorkflowsResponse(
                workflows=[workflows.Workflow(),], next_page_token="ghi",
            ),
            workflows.ListWorkflowsResponse(
                workflows=[workflows.Workflow(), workflows.Workflow(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_workflows(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_workflows_async_pager():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflows), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            workflows.ListWorkflowsResponse(
                workflows=[
                    workflows.Workflow(),
                    workflows.Workflow(),
                    workflows.Workflow(),
                ],
                next_page_token="abc",
            ),
            workflows.ListWorkflowsResponse(workflows=[], next_page_token="def",),
            workflows.ListWorkflowsResponse(
                workflows=[workflows.Workflow(),], next_page_token="ghi",
            ),
            workflows.ListWorkflowsResponse(
                workflows=[workflows.Workflow(), workflows.Workflow(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_workflows(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, workflows.Workflow) for i in responses)


@pytest.mark.asyncio
async def test_list_workflows_async_pages():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflows), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            workflows.ListWorkflowsResponse(
                workflows=[
                    workflows.Workflow(),
                    workflows.Workflow(),
                    workflows.Workflow(),
                ],
                next_page_token="abc",
            ),
            workflows.ListWorkflowsResponse(workflows=[], next_page_token="def",),
            workflows.ListWorkflowsResponse(
                workflows=[workflows.Workflow(),], next_page_token="ghi",
            ),
            workflows.ListWorkflowsResponse(
                workflows=[workflows.Workflow(), workflows.Workflow(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_workflows(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_workflow(
    transport: str = "grpc", request_type=workflows.GetWorkflowRequest
):
    client = WorkflowsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflows.Workflow(
            name="name_value",
            description="description_value",
            state=workflows.Workflow.State.ACTIVE,
            revision_id="revision_id_value",
            service_account="service_account_value",
            source_contents="source_contents_value",
        )

        response = client.get_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == workflows.GetWorkflowRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, workflows.Workflow)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.state == workflows.Workflow.State.ACTIVE

    assert response.revision_id == "revision_id_value"

    assert response.service_account == "service_account_value"


def test_get_workflow_from_dict():
    test_get_workflow(request_type=dict)


@pytest.mark.asyncio
async def test_get_workflow_async(
    transport: str = "grpc_asyncio", request_type=workflows.GetWorkflowRequest
):
    client = WorkflowsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflows.Workflow(
                name="name_value",
                description="description_value",
                state=workflows.Workflow.State.ACTIVE,
                revision_id="revision_id_value",
                service_account="service_account_value",
            )
        )

        response = await client.get_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == workflows.GetWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, workflows.Workflow)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.state == workflows.Workflow.State.ACTIVE

    assert response.revision_id == "revision_id_value"

    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_get_workflow_async_from_dict():
    await test_get_workflow_async(request_type=dict)


def test_get_workflow_field_headers():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflows.GetWorkflowRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workflow), "__call__") as call:
        call.return_value = workflows.Workflow()

        client.get_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_workflow_field_headers_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflows.GetWorkflowRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workflow), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(workflows.Workflow())

        await client.get_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_workflow_flattened():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflows.Workflow()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_workflow(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_workflow_flattened_error():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_workflow(
            workflows.GetWorkflowRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_workflow_flattened_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflows.Workflow()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(workflows.Workflow())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_workflow(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_workflow_flattened_error_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_workflow(
            workflows.GetWorkflowRequest(), name="name_value",
        )


def test_create_workflow(
    transport: str = "grpc", request_type=workflows.CreateWorkflowRequest
):
    client = WorkflowsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.create_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == workflows.CreateWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_workflow_from_dict():
    test_create_workflow(request_type=dict)


@pytest.mark.asyncio
async def test_create_workflow_async(
    transport: str = "grpc_asyncio", request_type=workflows.CreateWorkflowRequest
):
    client = WorkflowsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.create_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == workflows.CreateWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_workflow_async_from_dict():
    await test_create_workflow_async(request_type=dict)


def test_create_workflow_field_headers():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflows.CreateWorkflowRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workflow), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.create_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_workflow_field_headers_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflows.CreateWorkflowRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workflow), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.create_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_workflow_flattened():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_workflow(
            parent="parent_value",
            workflow=workflows.Workflow(name="name_value"),
            workflow_id="workflow_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].workflow == workflows.Workflow(name="name_value")

        assert args[0].workflow_id == "workflow_id_value"


def test_create_workflow_flattened_error():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_workflow(
            workflows.CreateWorkflowRequest(),
            parent="parent_value",
            workflow=workflows.Workflow(name="name_value"),
            workflow_id="workflow_id_value",
        )


@pytest.mark.asyncio
async def test_create_workflow_flattened_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_workflow(
            parent="parent_value",
            workflow=workflows.Workflow(name="name_value"),
            workflow_id="workflow_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].workflow == workflows.Workflow(name="name_value")

        assert args[0].workflow_id == "workflow_id_value"


@pytest.mark.asyncio
async def test_create_workflow_flattened_error_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_workflow(
            workflows.CreateWorkflowRequest(),
            parent="parent_value",
            workflow=workflows.Workflow(name="name_value"),
            workflow_id="workflow_id_value",
        )


def test_delete_workflow(
    transport: str = "grpc", request_type=workflows.DeleteWorkflowRequest
):
    client = WorkflowsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.delete_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == workflows.DeleteWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_workflow_from_dict():
    test_delete_workflow(request_type=dict)


@pytest.mark.asyncio
async def test_delete_workflow_async(
    transport: str = "grpc_asyncio", request_type=workflows.DeleteWorkflowRequest
):
    client = WorkflowsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.delete_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == workflows.DeleteWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_workflow_async_from_dict():
    await test_delete_workflow_async(request_type=dict)


def test_delete_workflow_field_headers():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflows.DeleteWorkflowRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workflow), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.delete_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_workflow_field_headers_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflows.DeleteWorkflowRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workflow), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.delete_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_workflow_flattened():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_workflow(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_workflow_flattened_error():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_workflow(
            workflows.DeleteWorkflowRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_workflow_flattened_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_workflow(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_workflow_flattened_error_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_workflow(
            workflows.DeleteWorkflowRequest(), name="name_value",
        )


def test_update_workflow(
    transport: str = "grpc", request_type=workflows.UpdateWorkflowRequest
):
    client = WorkflowsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.update_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == workflows.UpdateWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_workflow_from_dict():
    test_update_workflow(request_type=dict)


@pytest.mark.asyncio
async def test_update_workflow_async(
    transport: str = "grpc_asyncio", request_type=workflows.UpdateWorkflowRequest
):
    client = WorkflowsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.update_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == workflows.UpdateWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_workflow_async_from_dict():
    await test_update_workflow_async(request_type=dict)


def test_update_workflow_field_headers():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflows.UpdateWorkflowRequest()
    request.workflow.name = "workflow.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_workflow), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.update_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "workflow.name=workflow.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_workflow_field_headers_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflows.UpdateWorkflowRequest()
    request.workflow.name = "workflow.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_workflow), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.update_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "workflow.name=workflow.name/value",) in kw[
        "metadata"
    ]


def test_update_workflow_flattened():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_workflow(
            workflow=workflows.Workflow(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].workflow == workflows.Workflow(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_workflow_flattened_error():
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_workflow(
            workflows.UpdateWorkflowRequest(),
            workflow=workflows.Workflow(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_workflow_flattened_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_workflow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_workflow(
            workflow=workflows.Workflow(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].workflow == workflows.Workflow(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_workflow_flattened_error_async():
    client = WorkflowsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_workflow(
            workflows.UpdateWorkflowRequest(),
            workflow=workflows.Workflow(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.WorkflowsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WorkflowsClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.WorkflowsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WorkflowsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.WorkflowsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WorkflowsClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.WorkflowsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = WorkflowsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.WorkflowsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.WorkflowsGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.WorkflowsGrpcTransport, transports.WorkflowsGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = WorkflowsClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.WorkflowsGrpcTransport,)


def test_workflows_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.WorkflowsTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_workflows_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.workflows_v1beta.services.workflows.transports.WorkflowsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.WorkflowsTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_workflows",
        "get_workflow",
        "create_workflow",
        "delete_workflow",
        "update_workflow",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_workflows_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.workflows_v1beta.services.workflows.transports.WorkflowsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.WorkflowsTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_workflows_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.workflows_v1beta.services.workflows.transports.WorkflowsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.WorkflowsTransport()
        adc.assert_called_once()


def test_workflows_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        WorkflowsClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_workflows_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.WorkflowsGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_workflows_host_no_port():
    client = WorkflowsClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="workflows.googleapis.com"
        ),
    )
    assert client.transport._host == "workflows.googleapis.com:443"


def test_workflows_host_with_port():
    client = WorkflowsClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="workflows.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "workflows.googleapis.com:8000"


def test_workflows_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.WorkflowsGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_workflows_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.WorkflowsGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [transports.WorkflowsGrpcTransport, transports.WorkflowsGrpcAsyncIOTransport],
)
def test_workflows_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.WorkflowsGrpcTransport, transports.WorkflowsGrpcAsyncIOTransport],
)
def test_workflows_transport_channel_mtls_with_adc(transport_class):
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


def test_workflows_grpc_lro_client():
    client = WorkflowsClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_workflows_grpc_lro_async_client():
    client = WorkflowsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_workflow_path():
    project = "squid"
    location = "clam"
    workflow = "whelk"

    expected = "projects/{project}/locations/{location}/workflows/{workflow}".format(
        project=project, location=location, workflow=workflow,
    )
    actual = WorkflowsClient.workflow_path(project, location, workflow)
    assert expected == actual


def test_parse_workflow_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "workflow": "nudibranch",
    }
    path = WorkflowsClient.workflow_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowsClient.parse_workflow_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = WorkflowsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = WorkflowsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"

    expected = "folders/{folder}".format(folder=folder,)
    actual = WorkflowsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = WorkflowsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = WorkflowsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = WorkflowsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"

    expected = "projects/{project}".format(project=project,)
    actual = WorkflowsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = WorkflowsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = WorkflowsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = WorkflowsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.WorkflowsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = WorkflowsClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.WorkflowsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = WorkflowsClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
