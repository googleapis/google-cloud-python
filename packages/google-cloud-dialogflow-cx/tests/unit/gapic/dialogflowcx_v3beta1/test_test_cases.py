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


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.dialogflowcx_v3beta1.services.test_cases import TestCasesAsyncClient
from google.cloud.dialogflowcx_v3beta1.services.test_cases import TestCasesClient
from google.cloud.dialogflowcx_v3beta1.services.test_cases import pagers
from google.cloud.dialogflowcx_v3beta1.services.test_cases import transports
from google.cloud.dialogflowcx_v3beta1.types import audio_config
from google.cloud.dialogflowcx_v3beta1.types import fulfillment
from google.cloud.dialogflowcx_v3beta1.types import intent
from google.cloud.dialogflowcx_v3beta1.types import page
from google.cloud.dialogflowcx_v3beta1.types import response_message
from google.cloud.dialogflowcx_v3beta1.types import session
from google.cloud.dialogflowcx_v3beta1.types import test_case
from google.cloud.dialogflowcx_v3beta1.types import test_case as gcdc_test_case
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import google.auth


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

    assert TestCasesClient._get_default_mtls_endpoint(None) is None
    assert TestCasesClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        TestCasesClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        TestCasesClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        TestCasesClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert TestCasesClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [TestCasesClient, TestCasesAsyncClient,])
def test_test_cases_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "dialogflow.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.TestCasesGrpcTransport, "grpc"),
        (transports.TestCasesGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_test_cases_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class", [TestCasesClient, TestCasesAsyncClient,])
def test_test_cases_client_from_service_account_file(client_class):
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

        assert client.transport._host == "dialogflow.googleapis.com:443"


def test_test_cases_client_get_transport_class():
    transport = TestCasesClient.get_transport_class()
    available_transports = [
        transports.TestCasesGrpcTransport,
    ]
    assert transport in available_transports

    transport = TestCasesClient.get_transport_class("grpc")
    assert transport == transports.TestCasesGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (TestCasesClient, transports.TestCasesGrpcTransport, "grpc"),
        (
            TestCasesAsyncClient,
            transports.TestCasesGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    TestCasesClient, "DEFAULT_ENDPOINT", modify_default_endpoint(TestCasesClient)
)
@mock.patch.object(
    TestCasesAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TestCasesAsyncClient),
)
def test_test_cases_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(TestCasesClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(TestCasesClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
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
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
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
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
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
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
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
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (TestCasesClient, transports.TestCasesGrpcTransport, "grpc", "true"),
        (
            TestCasesAsyncClient,
            transports.TestCasesGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (TestCasesClient, transports.TestCasesGrpcTransport, "grpc", "false"),
        (
            TestCasesAsyncClient,
            transports.TestCasesGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    TestCasesClient, "DEFAULT_ENDPOINT", modify_default_endpoint(TestCasesClient)
)
@mock.patch.object(
    TestCasesAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TestCasesAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_test_cases_client_mtls_env_auto(
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
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (TestCasesClient, transports.TestCasesGrpcTransport, "grpc"),
        (
            TestCasesAsyncClient,
            transports.TestCasesGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_test_cases_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
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
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (TestCasesClient, transports.TestCasesGrpcTransport, "grpc"),
        (
            TestCasesAsyncClient,
            transports.TestCasesGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_test_cases_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
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
        )


def test_test_cases_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.test_cases.transports.TestCasesGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = TestCasesClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize("request_type", [test_case.ListTestCasesRequest, dict,])
def test_list_test_cases(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_test_cases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.ListTestCasesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ListTestCasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTestCasesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_test_cases_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_test_cases), "__call__") as call:
        client.list_test_cases()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ListTestCasesRequest()


@pytest.mark.asyncio
async def test_list_test_cases_async(
    transport: str = "grpc_asyncio", request_type=test_case.ListTestCasesRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_test_cases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.ListTestCasesResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ListTestCasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTestCasesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_test_cases_async_from_dict():
    await test_list_test_cases_async(request_type=dict)


def test_list_test_cases_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.ListTestCasesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_test_cases), "__call__") as call:
        call.return_value = test_case.ListTestCasesResponse()
        client.list_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_test_cases_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.ListTestCasesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_test_cases), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.ListTestCasesResponse()
        )
        await client.list_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_test_cases_flattened():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_test_cases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.ListTestCasesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_test_cases(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_test_cases_flattened_error():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_test_cases(
            test_case.ListTestCasesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_test_cases_flattened_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_test_cases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.ListTestCasesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.ListTestCasesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_test_cases(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_test_cases_flattened_error_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_test_cases(
            test_case.ListTestCasesRequest(), parent="parent_value",
        )


def test_list_test_cases_pager(transport_name: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_test_cases), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            test_case.ListTestCasesResponse(
                test_cases=[
                    test_case.TestCase(),
                    test_case.TestCase(),
                    test_case.TestCase(),
                ],
                next_page_token="abc",
            ),
            test_case.ListTestCasesResponse(test_cases=[], next_page_token="def",),
            test_case.ListTestCasesResponse(
                test_cases=[test_case.TestCase(),], next_page_token="ghi",
            ),
            test_case.ListTestCasesResponse(
                test_cases=[test_case.TestCase(), test_case.TestCase(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_test_cases(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, test_case.TestCase) for i in results)


def test_list_test_cases_pages(transport_name: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_test_cases), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            test_case.ListTestCasesResponse(
                test_cases=[
                    test_case.TestCase(),
                    test_case.TestCase(),
                    test_case.TestCase(),
                ],
                next_page_token="abc",
            ),
            test_case.ListTestCasesResponse(test_cases=[], next_page_token="def",),
            test_case.ListTestCasesResponse(
                test_cases=[test_case.TestCase(),], next_page_token="ghi",
            ),
            test_case.ListTestCasesResponse(
                test_cases=[test_case.TestCase(), test_case.TestCase(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_test_cases(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_test_cases_async_pager():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_cases), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            test_case.ListTestCasesResponse(
                test_cases=[
                    test_case.TestCase(),
                    test_case.TestCase(),
                    test_case.TestCase(),
                ],
                next_page_token="abc",
            ),
            test_case.ListTestCasesResponse(test_cases=[], next_page_token="def",),
            test_case.ListTestCasesResponse(
                test_cases=[test_case.TestCase(),], next_page_token="ghi",
            ),
            test_case.ListTestCasesResponse(
                test_cases=[test_case.TestCase(), test_case.TestCase(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_test_cases(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, test_case.TestCase) for i in responses)


@pytest.mark.asyncio
async def test_list_test_cases_async_pages():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_cases), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            test_case.ListTestCasesResponse(
                test_cases=[
                    test_case.TestCase(),
                    test_case.TestCase(),
                    test_case.TestCase(),
                ],
                next_page_token="abc",
            ),
            test_case.ListTestCasesResponse(test_cases=[], next_page_token="def",),
            test_case.ListTestCasesResponse(
                test_cases=[test_case.TestCase(),], next_page_token="ghi",
            ),
            test_case.ListTestCasesResponse(
                test_cases=[test_case.TestCase(), test_case.TestCase(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_test_cases(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [test_case.BatchDeleteTestCasesRequest, dict,])
def test_batch_delete_test_cases(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_test_cases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.batch_delete_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.BatchDeleteTestCasesRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_batch_delete_test_cases_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_test_cases), "__call__"
    ) as call:
        client.batch_delete_test_cases()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.BatchDeleteTestCasesRequest()


@pytest.mark.asyncio
async def test_batch_delete_test_cases_async(
    transport: str = "grpc_asyncio", request_type=test_case.BatchDeleteTestCasesRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_test_cases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.batch_delete_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.BatchDeleteTestCasesRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_batch_delete_test_cases_async_from_dict():
    await test_batch_delete_test_cases_async(request_type=dict)


def test_batch_delete_test_cases_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.BatchDeleteTestCasesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_test_cases), "__call__"
    ) as call:
        call.return_value = None
        client.batch_delete_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_delete_test_cases_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.BatchDeleteTestCasesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_test_cases), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.batch_delete_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_batch_delete_test_cases_flattened():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_test_cases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_delete_test_cases(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_batch_delete_test_cases_flattened_error():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_delete_test_cases(
            test_case.BatchDeleteTestCasesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_batch_delete_test_cases_flattened_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_test_cases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_delete_test_cases(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_batch_delete_test_cases_flattened_error_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_delete_test_cases(
            test_case.BatchDeleteTestCasesRequest(), parent="parent_value",
        )


@pytest.mark.parametrize("request_type", [test_case.GetTestCaseRequest, dict,])
def test_get_test_case(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.TestCase(
            name="name_value",
            tags=["tags_value"],
            display_name="display_name_value",
            notes="notes_value",
        )
        response = client.get_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.GetTestCaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, test_case.TestCase)
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.display_name == "display_name_value"
    assert response.notes == "notes_value"


def test_get_test_case_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_test_case), "__call__") as call:
        client.get_test_case()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.GetTestCaseRequest()


@pytest.mark.asyncio
async def test_get_test_case_async(
    transport: str = "grpc_asyncio", request_type=test_case.GetTestCaseRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.TestCase(
                name="name_value",
                tags=["tags_value"],
                display_name="display_name_value",
                notes="notes_value",
            )
        )
        response = await client.get_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.GetTestCaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, test_case.TestCase)
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.display_name == "display_name_value"
    assert response.notes == "notes_value"


@pytest.mark.asyncio
async def test_get_test_case_async_from_dict():
    await test_get_test_case_async(request_type=dict)


def test_get_test_case_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.GetTestCaseRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_test_case), "__call__") as call:
        call.return_value = test_case.TestCase()
        client.get_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_test_case_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.GetTestCaseRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_test_case), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(test_case.TestCase())
        await client.get_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_test_case_flattened():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.TestCase()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_test_case(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_test_case_flattened_error():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_test_case(
            test_case.GetTestCaseRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_test_case_flattened_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.TestCase()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(test_case.TestCase())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_test_case(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_test_case_flattened_error_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_test_case(
            test_case.GetTestCaseRequest(), name="name_value",
        )


@pytest.mark.parametrize("request_type", [gcdc_test_case.CreateTestCaseRequest, dict,])
def test_create_test_case(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_test_case.TestCase(
            name="name_value",
            tags=["tags_value"],
            display_name="display_name_value",
            notes="notes_value",
        )
        response = client.create_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcdc_test_case.CreateTestCaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_test_case.TestCase)
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.display_name == "display_name_value"
    assert response.notes == "notes_value"


def test_create_test_case_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_test_case), "__call__") as call:
        client.create_test_case()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcdc_test_case.CreateTestCaseRequest()


@pytest.mark.asyncio
async def test_create_test_case_async(
    transport: str = "grpc_asyncio", request_type=gcdc_test_case.CreateTestCaseRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_test_case.TestCase(
                name="name_value",
                tags=["tags_value"],
                display_name="display_name_value",
                notes="notes_value",
            )
        )
        response = await client.create_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcdc_test_case.CreateTestCaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_test_case.TestCase)
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.display_name == "display_name_value"
    assert response.notes == "notes_value"


@pytest.mark.asyncio
async def test_create_test_case_async_from_dict():
    await test_create_test_case_async(request_type=dict)


def test_create_test_case_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_test_case.CreateTestCaseRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_test_case), "__call__") as call:
        call.return_value = gcdc_test_case.TestCase()
        client.create_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_test_case_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_test_case.CreateTestCaseRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_test_case), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_test_case.TestCase()
        )
        await client.create_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_test_case_flattened():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_test_case.TestCase()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_test_case(
            parent="parent_value", test_case=gcdc_test_case.TestCase(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].test_case
        mock_val = gcdc_test_case.TestCase(name="name_value")
        assert arg == mock_val


def test_create_test_case_flattened_error():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_test_case(
            gcdc_test_case.CreateTestCaseRequest(),
            parent="parent_value",
            test_case=gcdc_test_case.TestCase(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_test_case_flattened_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_test_case.TestCase()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_test_case.TestCase()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_test_case(
            parent="parent_value", test_case=gcdc_test_case.TestCase(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].test_case
        mock_val = gcdc_test_case.TestCase(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_test_case_flattened_error_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_test_case(
            gcdc_test_case.CreateTestCaseRequest(),
            parent="parent_value",
            test_case=gcdc_test_case.TestCase(name="name_value"),
        )


@pytest.mark.parametrize("request_type", [gcdc_test_case.UpdateTestCaseRequest, dict,])
def test_update_test_case(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_test_case.TestCase(
            name="name_value",
            tags=["tags_value"],
            display_name="display_name_value",
            notes="notes_value",
        )
        response = client.update_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcdc_test_case.UpdateTestCaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_test_case.TestCase)
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.display_name == "display_name_value"
    assert response.notes == "notes_value"


def test_update_test_case_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_test_case), "__call__") as call:
        client.update_test_case()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcdc_test_case.UpdateTestCaseRequest()


@pytest.mark.asyncio
async def test_update_test_case_async(
    transport: str = "grpc_asyncio", request_type=gcdc_test_case.UpdateTestCaseRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_test_case.TestCase(
                name="name_value",
                tags=["tags_value"],
                display_name="display_name_value",
                notes="notes_value",
            )
        )
        response = await client.update_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcdc_test_case.UpdateTestCaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcdc_test_case.TestCase)
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.display_name == "display_name_value"
    assert response.notes == "notes_value"


@pytest.mark.asyncio
async def test_update_test_case_async_from_dict():
    await test_update_test_case_async(request_type=dict)


def test_update_test_case_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_test_case.UpdateTestCaseRequest()

    request.test_case.name = "test_case.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_test_case), "__call__") as call:
        call.return_value = gcdc_test_case.TestCase()
        client.update_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "test_case.name=test_case.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_test_case_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_test_case.UpdateTestCaseRequest()

    request.test_case.name = "test_case.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_test_case), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_test_case.TestCase()
        )
        await client.update_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "test_case.name=test_case.name/value",) in kw[
        "metadata"
    ]


def test_update_test_case_flattened():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_test_case.TestCase()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_test_case(
            test_case=gcdc_test_case.TestCase(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].test_case
        mock_val = gcdc_test_case.TestCase(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_test_case_flattened_error():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_test_case(
            gcdc_test_case.UpdateTestCaseRequest(),
            test_case=gcdc_test_case.TestCase(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_test_case_flattened_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcdc_test_case.TestCase()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcdc_test_case.TestCase()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_test_case(
            test_case=gcdc_test_case.TestCase(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].test_case
        mock_val = gcdc_test_case.TestCase(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_test_case_flattened_error_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_test_case(
            gcdc_test_case.UpdateTestCaseRequest(),
            test_case=gcdc_test_case.TestCase(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize("request_type", [test_case.RunTestCaseRequest, dict,])
def test_run_test_case(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.run_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.RunTestCaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_run_test_case_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_test_case), "__call__") as call:
        client.run_test_case()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.RunTestCaseRequest()


@pytest.mark.asyncio
async def test_run_test_case_async(
    transport: str = "grpc_asyncio", request_type=test_case.RunTestCaseRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_test_case), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.run_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.RunTestCaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_run_test_case_async_from_dict():
    await test_run_test_case_async(request_type=dict)


def test_run_test_case_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.RunTestCaseRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_test_case), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.run_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_run_test_case_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.RunTestCaseRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_test_case), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.run_test_case(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [test_case.BatchRunTestCasesRequest, dict,])
def test_batch_run_test_cases(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_test_cases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.batch_run_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.BatchRunTestCasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_batch_run_test_cases_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_test_cases), "__call__"
    ) as call:
        client.batch_run_test_cases()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.BatchRunTestCasesRequest()


@pytest.mark.asyncio
async def test_batch_run_test_cases_async(
    transport: str = "grpc_asyncio", request_type=test_case.BatchRunTestCasesRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_test_cases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.batch_run_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.BatchRunTestCasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_batch_run_test_cases_async_from_dict():
    await test_batch_run_test_cases_async(request_type=dict)


def test_batch_run_test_cases_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.BatchRunTestCasesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_test_cases), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.batch_run_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_run_test_cases_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.BatchRunTestCasesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_test_cases), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.batch_run_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [test_case.CalculateCoverageRequest, dict,])
def test_calculate_coverage(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_coverage), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.CalculateCoverageResponse(
            agent="agent_value",
            intent_coverage=test_case.IntentCoverage(
                intents=[test_case.IntentCoverage.Intent(intent="intent_value")]
            ),
        )
        response = client.calculate_coverage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.CalculateCoverageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, test_case.CalculateCoverageResponse)
    assert response.agent == "agent_value"


def test_calculate_coverage_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_coverage), "__call__"
    ) as call:
        client.calculate_coverage()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.CalculateCoverageRequest()


@pytest.mark.asyncio
async def test_calculate_coverage_async(
    transport: str = "grpc_asyncio", request_type=test_case.CalculateCoverageRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_coverage), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.CalculateCoverageResponse(agent="agent_value",)
        )
        response = await client.calculate_coverage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.CalculateCoverageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, test_case.CalculateCoverageResponse)
    assert response.agent == "agent_value"


@pytest.mark.asyncio
async def test_calculate_coverage_async_from_dict():
    await test_calculate_coverage_async(request_type=dict)


def test_calculate_coverage_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.CalculateCoverageRequest()

    request.agent = "agent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_coverage), "__call__"
    ) as call:
        call.return_value = test_case.CalculateCoverageResponse()
        client.calculate_coverage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "agent=agent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_calculate_coverage_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.CalculateCoverageRequest()

    request.agent = "agent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_coverage), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.CalculateCoverageResponse()
        )
        await client.calculate_coverage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "agent=agent/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [test_case.ImportTestCasesRequest, dict,])
def test_import_test_cases(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_test_cases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ImportTestCasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_test_cases_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_test_cases), "__call__"
    ) as call:
        client.import_test_cases()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ImportTestCasesRequest()


@pytest.mark.asyncio
async def test_import_test_cases_async(
    transport: str = "grpc_asyncio", request_type=test_case.ImportTestCasesRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_test_cases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ImportTestCasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_import_test_cases_async_from_dict():
    await test_import_test_cases_async(request_type=dict)


def test_import_test_cases_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.ImportTestCasesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_test_cases), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.import_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_test_cases_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.ImportTestCasesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_test_cases), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.import_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [test_case.ExportTestCasesRequest, dict,])
def test_export_test_cases(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_test_cases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.export_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ExportTestCasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_test_cases_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_test_cases), "__call__"
    ) as call:
        client.export_test_cases()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ExportTestCasesRequest()


@pytest.mark.asyncio
async def test_export_test_cases_async(
    transport: str = "grpc_asyncio", request_type=test_case.ExportTestCasesRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_test_cases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.export_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ExportTestCasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_export_test_cases_async_from_dict():
    await test_export_test_cases_async(request_type=dict)


def test_export_test_cases_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.ExportTestCasesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_test_cases), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.export_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_test_cases_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.ExportTestCasesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_test_cases), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.export_test_cases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [test_case.ListTestCaseResultsRequest, dict,])
def test_list_test_case_results(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.ListTestCaseResultsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_test_case_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ListTestCaseResultsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTestCaseResultsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_test_case_results_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results), "__call__"
    ) as call:
        client.list_test_case_results()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ListTestCaseResultsRequest()


@pytest.mark.asyncio
async def test_list_test_case_results_async(
    transport: str = "grpc_asyncio", request_type=test_case.ListTestCaseResultsRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.ListTestCaseResultsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_test_case_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.ListTestCaseResultsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTestCaseResultsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_test_case_results_async_from_dict():
    await test_list_test_case_results_async(request_type=dict)


def test_list_test_case_results_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.ListTestCaseResultsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results), "__call__"
    ) as call:
        call.return_value = test_case.ListTestCaseResultsResponse()
        client.list_test_case_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_test_case_results_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.ListTestCaseResultsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.ListTestCaseResultsResponse()
        )
        await client.list_test_case_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_test_case_results_flattened():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.ListTestCaseResultsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_test_case_results(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_test_case_results_flattened_error():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_test_case_results(
            test_case.ListTestCaseResultsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_test_case_results_flattened_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.ListTestCaseResultsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.ListTestCaseResultsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_test_case_results(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_test_case_results_flattened_error_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_test_case_results(
            test_case.ListTestCaseResultsRequest(), parent="parent_value",
        )


def test_list_test_case_results_pager(transport_name: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            test_case.ListTestCaseResultsResponse(
                test_case_results=[
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                ],
                next_page_token="abc",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[], next_page_token="def",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[test_case.TestCaseResult(),], next_page_token="ghi",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_test_case_results(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, test_case.TestCaseResult) for i in results)


def test_list_test_case_results_pages(transport_name: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            test_case.ListTestCaseResultsResponse(
                test_case_results=[
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                ],
                next_page_token="abc",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[], next_page_token="def",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[test_case.TestCaseResult(),], next_page_token="ghi",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_test_case_results(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_test_case_results_async_pager():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            test_case.ListTestCaseResultsResponse(
                test_case_results=[
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                ],
                next_page_token="abc",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[], next_page_token="def",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[test_case.TestCaseResult(),], next_page_token="ghi",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_test_case_results(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, test_case.TestCaseResult) for i in responses)


@pytest.mark.asyncio
async def test_list_test_case_results_async_pages():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_test_case_results),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            test_case.ListTestCaseResultsResponse(
                test_case_results=[
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                ],
                next_page_token="abc",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[], next_page_token="def",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[test_case.TestCaseResult(),], next_page_token="ghi",
            ),
            test_case.ListTestCaseResultsResponse(
                test_case_results=[
                    test_case.TestCaseResult(),
                    test_case.TestCaseResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_test_case_results(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [test_case.GetTestCaseResultRequest, dict,])
def test_get_test_case_result(request_type, transport: str = "grpc"):
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_test_case_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.TestCaseResult(
            name="name_value",
            environment="environment_value",
            test_result=test_case.TestResult.PASSED,
        )
        response = client.get_test_case_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.GetTestCaseResultRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, test_case.TestCaseResult)
    assert response.name == "name_value"
    assert response.environment == "environment_value"
    assert response.test_result == test_case.TestResult.PASSED


def test_get_test_case_result_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_test_case_result), "__call__"
    ) as call:
        client.get_test_case_result()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.GetTestCaseResultRequest()


@pytest.mark.asyncio
async def test_get_test_case_result_async(
    transport: str = "grpc_asyncio", request_type=test_case.GetTestCaseResultRequest
):
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_test_case_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.TestCaseResult(
                name="name_value",
                environment="environment_value",
                test_result=test_case.TestResult.PASSED,
            )
        )
        response = await client.get_test_case_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == test_case.GetTestCaseResultRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, test_case.TestCaseResult)
    assert response.name == "name_value"
    assert response.environment == "environment_value"
    assert response.test_result == test_case.TestResult.PASSED


@pytest.mark.asyncio
async def test_get_test_case_result_async_from_dict():
    await test_get_test_case_result_async(request_type=dict)


def test_get_test_case_result_field_headers():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.GetTestCaseResultRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_test_case_result), "__call__"
    ) as call:
        call.return_value = test_case.TestCaseResult()
        client.get_test_case_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_test_case_result_field_headers_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = test_case.GetTestCaseResultRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_test_case_result), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.TestCaseResult()
        )
        await client.get_test_case_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_test_case_result_flattened():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_test_case_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.TestCaseResult()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_test_case_result(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_test_case_result_flattened_error():
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_test_case_result(
            test_case.GetTestCaseResultRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_test_case_result_flattened_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_test_case_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = test_case.TestCaseResult()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            test_case.TestCaseResult()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_test_case_result(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_test_case_result_flattened_error_async():
    client = TestCasesAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_test_case_result(
            test_case.GetTestCaseResultRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.TestCasesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TestCasesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.TestCasesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TestCasesClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.TestCasesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TestCasesClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TestCasesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = TestCasesClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TestCasesGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.TestCasesGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.TestCasesGrpcTransport, transports.TestCasesGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = TestCasesClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.TestCasesGrpcTransport,)


def test_test_cases_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.TestCasesTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_test_cases_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.test_cases.transports.TestCasesTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.TestCasesTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_test_cases",
        "batch_delete_test_cases",
        "get_test_case",
        "create_test_case",
        "update_test_case",
        "run_test_case",
        "batch_run_test_cases",
        "calculate_coverage",
        "import_test_cases",
        "export_test_cases",
        "list_test_case_results",
        "get_test_case_result",
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


def test_test_cases_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.test_cases.transports.TestCasesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.TestCasesTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


def test_test_cases_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.test_cases.transports.TestCasesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.TestCasesTransport()
        adc.assert_called_once()


def test_test_cases_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        TestCasesClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.TestCasesGrpcTransport, transports.TestCasesGrpcAsyncIOTransport,],
)
def test_test_cases_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.TestCasesGrpcTransport, grpc_helpers),
        (transports.TestCasesGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_test_cases_transport_create_channel(transport_class, grpc_helpers):
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
            "dialogflow.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            scopes=["1", "2"],
            default_host="dialogflow.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.TestCasesGrpcTransport, transports.TestCasesGrpcAsyncIOTransport],
)
def test_test_cases_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_test_cases_host_no_port():
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:443"


def test_test_cases_host_with_port():
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:8000"


def test_test_cases_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.TestCasesGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_test_cases_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.TestCasesGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.TestCasesGrpcTransport, transports.TestCasesGrpcAsyncIOTransport],
)
def test_test_cases_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.TestCasesGrpcTransport, transports.TestCasesGrpcAsyncIOTransport],
)
def test_test_cases_transport_channel_mtls_with_adc(transport_class):
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


def test_test_cases_grpc_lro_client():
    client = TestCasesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_test_cases_grpc_lro_async_client():
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_agent_path():
    project = "squid"
    location = "clam"
    agent = "whelk"
    expected = "projects/{project}/locations/{location}/agents/{agent}".format(
        project=project, location=location, agent=agent,
    )
    actual = TestCasesClient.agent_path(project, location, agent)
    assert expected == actual


def test_parse_agent_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "agent": "nudibranch",
    }
    path = TestCasesClient.agent_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_agent_path(path)
    assert expected == actual


def test_entity_type_path():
    project = "cuttlefish"
    location = "mussel"
    agent = "winkle"
    entity_type = "nautilus"
    expected = "projects/{project}/locations/{location}/agents/{agent}/entityTypes/{entity_type}".format(
        project=project, location=location, agent=agent, entity_type=entity_type,
    )
    actual = TestCasesClient.entity_type_path(project, location, agent, entity_type)
    assert expected == actual


def test_parse_entity_type_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "agent": "squid",
        "entity_type": "clam",
    }
    path = TestCasesClient.entity_type_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_entity_type_path(path)
    assert expected == actual


def test_environment_path():
    project = "whelk"
    location = "octopus"
    agent = "oyster"
    environment = "nudibranch"
    expected = "projects/{project}/locations/{location}/agents/{agent}/environments/{environment}".format(
        project=project, location=location, agent=agent, environment=environment,
    )
    actual = TestCasesClient.environment_path(project, location, agent, environment)
    assert expected == actual


def test_parse_environment_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "agent": "winkle",
        "environment": "nautilus",
    }
    path = TestCasesClient.environment_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_environment_path(path)
    assert expected == actual


def test_flow_path():
    project = "scallop"
    location = "abalone"
    agent = "squid"
    flow = "clam"
    expected = "projects/{project}/locations/{location}/agents/{agent}/flows/{flow}".format(
        project=project, location=location, agent=agent, flow=flow,
    )
    actual = TestCasesClient.flow_path(project, location, agent, flow)
    assert expected == actual


def test_parse_flow_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
        "agent": "oyster",
        "flow": "nudibranch",
    }
    path = TestCasesClient.flow_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_flow_path(path)
    assert expected == actual


def test_intent_path():
    project = "cuttlefish"
    location = "mussel"
    agent = "winkle"
    intent = "nautilus"
    expected = "projects/{project}/locations/{location}/agents/{agent}/intents/{intent}".format(
        project=project, location=location, agent=agent, intent=intent,
    )
    actual = TestCasesClient.intent_path(project, location, agent, intent)
    assert expected == actual


def test_parse_intent_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "agent": "squid",
        "intent": "clam",
    }
    path = TestCasesClient.intent_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_intent_path(path)
    assert expected == actual


def test_page_path():
    project = "whelk"
    location = "octopus"
    agent = "oyster"
    flow = "nudibranch"
    page = "cuttlefish"
    expected = "projects/{project}/locations/{location}/agents/{agent}/flows/{flow}/pages/{page}".format(
        project=project, location=location, agent=agent, flow=flow, page=page,
    )
    actual = TestCasesClient.page_path(project, location, agent, flow, page)
    assert expected == actual


def test_parse_page_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "agent": "nautilus",
        "flow": "scallop",
        "page": "abalone",
    }
    path = TestCasesClient.page_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_page_path(path)
    assert expected == actual


def test_test_case_path():
    project = "squid"
    location = "clam"
    agent = "whelk"
    test_case = "octopus"
    expected = "projects/{project}/locations/{location}/agents/{agent}/testCases/{test_case}".format(
        project=project, location=location, agent=agent, test_case=test_case,
    )
    actual = TestCasesClient.test_case_path(project, location, agent, test_case)
    assert expected == actual


def test_parse_test_case_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "agent": "cuttlefish",
        "test_case": "mussel",
    }
    path = TestCasesClient.test_case_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_test_case_path(path)
    assert expected == actual


def test_test_case_result_path():
    project = "winkle"
    location = "nautilus"
    agent = "scallop"
    test_case = "abalone"
    result = "squid"
    expected = "projects/{project}/locations/{location}/agents/{agent}/testCases/{test_case}/results/{result}".format(
        project=project,
        location=location,
        agent=agent,
        test_case=test_case,
        result=result,
    )
    actual = TestCasesClient.test_case_result_path(
        project, location, agent, test_case, result
    )
    assert expected == actual


def test_parse_test_case_result_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "agent": "octopus",
        "test_case": "oyster",
        "result": "nudibranch",
    }
    path = TestCasesClient.test_case_result_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_test_case_result_path(path)
    assert expected == actual


def test_transition_route_group_path():
    project = "cuttlefish"
    location = "mussel"
    agent = "winkle"
    flow = "nautilus"
    transition_route_group = "scallop"
    expected = "projects/{project}/locations/{location}/agents/{agent}/flows/{flow}/transitionRouteGroups/{transition_route_group}".format(
        project=project,
        location=location,
        agent=agent,
        flow=flow,
        transition_route_group=transition_route_group,
    )
    actual = TestCasesClient.transition_route_group_path(
        project, location, agent, flow, transition_route_group
    )
    assert expected == actual


def test_parse_transition_route_group_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "agent": "clam",
        "flow": "whelk",
        "transition_route_group": "octopus",
    }
    path = TestCasesClient.transition_route_group_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_transition_route_group_path(path)
    assert expected == actual


def test_webhook_path():
    project = "oyster"
    location = "nudibranch"
    agent = "cuttlefish"
    webhook = "mussel"
    expected = "projects/{project}/locations/{location}/agents/{agent}/webhooks/{webhook}".format(
        project=project, location=location, agent=agent, webhook=webhook,
    )
    actual = TestCasesClient.webhook_path(project, location, agent, webhook)
    assert expected == actual


def test_parse_webhook_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "agent": "scallop",
        "webhook": "abalone",
    }
    path = TestCasesClient.webhook_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_webhook_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = TestCasesClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = TestCasesClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = TestCasesClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = TestCasesClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = TestCasesClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = TestCasesClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = TestCasesClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = TestCasesClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = TestCasesClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = TestCasesClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = TestCasesClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.TestCasesTransport, "_prep_wrapped_messages"
    ) as prep:
        client = TestCasesClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.TestCasesTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = TestCasesClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = TestCasesAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = TestCasesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = TestCasesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()
