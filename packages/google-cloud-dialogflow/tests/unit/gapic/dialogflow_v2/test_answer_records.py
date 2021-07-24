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
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.dialogflow_v2.services.answer_records import AnswerRecordsAsyncClient
from google.cloud.dialogflow_v2.services.answer_records import AnswerRecordsClient
from google.cloud.dialogflow_v2.services.answer_records import pagers
from google.cloud.dialogflow_v2.services.answer_records import transports
from google.cloud.dialogflow_v2.services.answer_records.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.dialogflow_v2.types import answer_record
from google.cloud.dialogflow_v2.types import answer_record as gcd_answer_record
from google.cloud.dialogflow_v2.types import participant
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
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

    assert AnswerRecordsClient._get_default_mtls_endpoint(None) is None
    assert (
        AnswerRecordsClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AnswerRecordsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AnswerRecordsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AnswerRecordsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AnswerRecordsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [AnswerRecordsClient, AnswerRecordsAsyncClient,]
)
def test_answer_records_client_from_service_account_info(client_class):
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
        (transports.AnswerRecordsGrpcTransport, "grpc"),
        (transports.AnswerRecordsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_answer_records_client_service_account_always_use_jwt(
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


@pytest.mark.parametrize(
    "client_class", [AnswerRecordsClient, AnswerRecordsAsyncClient,]
)
def test_answer_records_client_from_service_account_file(client_class):
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


def test_answer_records_client_get_transport_class():
    transport = AnswerRecordsClient.get_transport_class()
    available_transports = [
        transports.AnswerRecordsGrpcTransport,
    ]
    assert transport in available_transports

    transport = AnswerRecordsClient.get_transport_class("grpc")
    assert transport == transports.AnswerRecordsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AnswerRecordsClient, transports.AnswerRecordsGrpcTransport, "grpc"),
        (
            AnswerRecordsAsyncClient,
            transports.AnswerRecordsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    AnswerRecordsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnswerRecordsClient),
)
@mock.patch.object(
    AnswerRecordsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnswerRecordsAsyncClient),
)
def test_answer_records_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AnswerRecordsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AnswerRecordsClient, "get_transport_class") as gtc:
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
            always_use_jwt_access=True,
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
                always_use_jwt_access=True,
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
                always_use_jwt_access=True,
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
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (AnswerRecordsClient, transports.AnswerRecordsGrpcTransport, "grpc", "true"),
        (
            AnswerRecordsAsyncClient,
            transports.AnswerRecordsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (AnswerRecordsClient, transports.AnswerRecordsGrpcTransport, "grpc", "false"),
        (
            AnswerRecordsAsyncClient,
            transports.AnswerRecordsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    AnswerRecordsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnswerRecordsClient),
)
@mock.patch.object(
    AnswerRecordsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnswerRecordsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_answer_records_client_mtls_env_auto(
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
                    client = client_class()
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
                client = client_class()
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
        (AnswerRecordsClient, transports.AnswerRecordsGrpcTransport, "grpc"),
        (
            AnswerRecordsAsyncClient,
            transports.AnswerRecordsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_answer_records_client_client_options_scopes(
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
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AnswerRecordsClient, transports.AnswerRecordsGrpcTransport, "grpc"),
        (
            AnswerRecordsAsyncClient,
            transports.AnswerRecordsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_answer_records_client_client_options_credentials_file(
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
            always_use_jwt_access=True,
        )


def test_answer_records_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflow_v2.services.answer_records.transports.AnswerRecordsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AnswerRecordsClient(
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
            always_use_jwt_access=True,
        )


def test_list_answer_records(
    transport: str = "grpc", request_type=answer_record.ListAnswerRecordsRequest
):
    client = AnswerRecordsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = answer_record.ListAnswerRecordsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_answer_records(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == answer_record.ListAnswerRecordsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnswerRecordsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_answer_records_from_dict():
    test_list_answer_records(request_type=dict)


def test_list_answer_records_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnswerRecordsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records), "__call__"
    ) as call:
        client.list_answer_records()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == answer_record.ListAnswerRecordsRequest()


@pytest.mark.asyncio
async def test_list_answer_records_async(
    transport: str = "grpc_asyncio", request_type=answer_record.ListAnswerRecordsRequest
):
    client = AnswerRecordsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            answer_record.ListAnswerRecordsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_answer_records(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == answer_record.ListAnswerRecordsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnswerRecordsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_answer_records_async_from_dict():
    await test_list_answer_records_async(request_type=dict)


def test_list_answer_records_field_headers():
    client = AnswerRecordsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = answer_record.ListAnswerRecordsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records), "__call__"
    ) as call:
        call.return_value = answer_record.ListAnswerRecordsResponse()
        client.list_answer_records(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_answer_records_field_headers_async():
    client = AnswerRecordsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = answer_record.ListAnswerRecordsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            answer_record.ListAnswerRecordsResponse()
        )
        await client.list_answer_records(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_answer_records_flattened():
    client = AnswerRecordsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = answer_record.ListAnswerRecordsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_answer_records(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_answer_records_flattened_error():
    client = AnswerRecordsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_answer_records(
            answer_record.ListAnswerRecordsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_answer_records_flattened_async():
    client = AnswerRecordsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = answer_record.ListAnswerRecordsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            answer_record.ListAnswerRecordsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_answer_records(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_answer_records_flattened_error_async():
    client = AnswerRecordsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_answer_records(
            answer_record.ListAnswerRecordsRequest(), parent="parent_value",
        )


def test_list_answer_records_pager():
    client = AnswerRecordsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            answer_record.ListAnswerRecordsResponse(
                answer_records=[
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                ],
                next_page_token="abc",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[], next_page_token="def",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[answer_record.AnswerRecord(),], next_page_token="ghi",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_answer_records(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, answer_record.AnswerRecord) for i in results)


def test_list_answer_records_pages():
    client = AnswerRecordsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            answer_record.ListAnswerRecordsResponse(
                answer_records=[
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                ],
                next_page_token="abc",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[], next_page_token="def",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[answer_record.AnswerRecord(),], next_page_token="ghi",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_answer_records(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_answer_records_async_pager():
    client = AnswerRecordsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            answer_record.ListAnswerRecordsResponse(
                answer_records=[
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                ],
                next_page_token="abc",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[], next_page_token="def",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[answer_record.AnswerRecord(),], next_page_token="ghi",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_answer_records(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, answer_record.AnswerRecord) for i in responses)


@pytest.mark.asyncio
async def test_list_answer_records_async_pages():
    client = AnswerRecordsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_answer_records),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            answer_record.ListAnswerRecordsResponse(
                answer_records=[
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                ],
                next_page_token="abc",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[], next_page_token="def",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[answer_record.AnswerRecord(),], next_page_token="ghi",
            ),
            answer_record.ListAnswerRecordsResponse(
                answer_records=[
                    answer_record.AnswerRecord(),
                    answer_record.AnswerRecord(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_answer_records(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_answer_record(
    transport: str = "grpc", request_type=gcd_answer_record.UpdateAnswerRecordRequest
):
    client = AnswerRecordsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_answer_record), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_answer_record.AnswerRecord(
            name="name_value",
            agent_assistant_record=gcd_answer_record.AgentAssistantRecord(
                article_suggestion_answer=participant.ArticleAnswer(title="title_value")
            ),
        )
        response = client.update_answer_record(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_answer_record.UpdateAnswerRecordRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_answer_record.AnswerRecord)
    assert response.name == "name_value"


def test_update_answer_record_from_dict():
    test_update_answer_record(request_type=dict)


def test_update_answer_record_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnswerRecordsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_answer_record), "__call__"
    ) as call:
        client.update_answer_record()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_answer_record.UpdateAnswerRecordRequest()


@pytest.mark.asyncio
async def test_update_answer_record_async(
    transport: str = "grpc_asyncio",
    request_type=gcd_answer_record.UpdateAnswerRecordRequest,
):
    client = AnswerRecordsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_answer_record), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_answer_record.AnswerRecord(name="name_value",)
        )
        response = await client.update_answer_record(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_answer_record.UpdateAnswerRecordRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_answer_record.AnswerRecord)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_update_answer_record_async_from_dict():
    await test_update_answer_record_async(request_type=dict)


def test_update_answer_record_field_headers():
    client = AnswerRecordsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_answer_record.UpdateAnswerRecordRequest()

    request.answer_record.name = "answer_record.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_answer_record), "__call__"
    ) as call:
        call.return_value = gcd_answer_record.AnswerRecord()
        client.update_answer_record(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "answer_record.name=answer_record.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_answer_record_field_headers_async():
    client = AnswerRecordsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_answer_record.UpdateAnswerRecordRequest()

    request.answer_record.name = "answer_record.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_answer_record), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_answer_record.AnswerRecord()
        )
        await client.update_answer_record(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "answer_record.name=answer_record.name/value",
    ) in kw["metadata"]


def test_update_answer_record_flattened():
    client = AnswerRecordsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_answer_record), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_answer_record.AnswerRecord()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_answer_record(
            answer_record=gcd_answer_record.AnswerRecord(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].answer_record == gcd_answer_record.AnswerRecord(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_answer_record_flattened_error():
    client = AnswerRecordsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_answer_record(
            gcd_answer_record.UpdateAnswerRecordRequest(),
            answer_record=gcd_answer_record.AnswerRecord(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_answer_record_flattened_async():
    client = AnswerRecordsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_answer_record), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_answer_record.AnswerRecord()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_answer_record.AnswerRecord()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_answer_record(
            answer_record=gcd_answer_record.AnswerRecord(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].answer_record == gcd_answer_record.AnswerRecord(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_answer_record_flattened_error_async():
    client = AnswerRecordsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_answer_record(
            gcd_answer_record.UpdateAnswerRecordRequest(),
            answer_record=gcd_answer_record.AnswerRecord(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AnswerRecordsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnswerRecordsClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AnswerRecordsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnswerRecordsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AnswerRecordsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnswerRecordsClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AnswerRecordsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AnswerRecordsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AnswerRecordsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AnswerRecordsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnswerRecordsGrpcTransport,
        transports.AnswerRecordsGrpcAsyncIOTransport,
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
    client = AnswerRecordsClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.AnswerRecordsGrpcTransport,)


def test_answer_records_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AnswerRecordsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_answer_records_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dialogflow_v2.services.answer_records.transports.AnswerRecordsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AnswerRecordsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_answer_records",
        "update_answer_record",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_answer_records_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflow_v2.services.answer_records.transports.AnswerRecordsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AnswerRecordsTransport(
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


@requires_google_auth_lt_1_25_0
def test_answer_records_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflow_v2.services.answer_records.transports.AnswerRecordsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AnswerRecordsTransport(
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


def test_answer_records_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dialogflow_v2.services.answer_records.transports.AnswerRecordsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AnswerRecordsTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_answer_records_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AnswerRecordsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_answer_records_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AnswerRecordsClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnswerRecordsGrpcTransport,
        transports.AnswerRecordsGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_answer_records_transport_auth_adc(transport_class):
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
    "transport_class",
    [
        transports.AnswerRecordsGrpcTransport,
        transports.AnswerRecordsGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_answer_records_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.AnswerRecordsGrpcTransport, grpc_helpers),
        (transports.AnswerRecordsGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_answer_records_transport_create_channel(transport_class, grpc_helpers):
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
    [
        transports.AnswerRecordsGrpcTransport,
        transports.AnswerRecordsGrpcAsyncIOTransport,
    ],
)
def test_answer_records_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_answer_records_host_no_port():
    client = AnswerRecordsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:443"


def test_answer_records_host_with_port():
    client = AnswerRecordsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:8000"


def test_answer_records_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AnswerRecordsGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_answer_records_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AnswerRecordsGrpcAsyncIOTransport(
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
        transports.AnswerRecordsGrpcTransport,
        transports.AnswerRecordsGrpcAsyncIOTransport,
    ],
)
def test_answer_records_transport_channel_mtls_with_client_cert_source(transport_class):
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
        transports.AnswerRecordsGrpcTransport,
        transports.AnswerRecordsGrpcAsyncIOTransport,
    ],
)
def test_answer_records_transport_channel_mtls_with_adc(transport_class):
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


def test_answer_record_path():
    project = "squid"
    answer_record = "clam"
    expected = "projects/{project}/answerRecords/{answer_record}".format(
        project=project, answer_record=answer_record,
    )
    actual = AnswerRecordsClient.answer_record_path(project, answer_record)
    assert expected == actual


def test_parse_answer_record_path():
    expected = {
        "project": "whelk",
        "answer_record": "octopus",
    }
    path = AnswerRecordsClient.answer_record_path(**expected)

    # Check that the path construction is reversible.
    actual = AnswerRecordsClient.parse_answer_record_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AnswerRecordsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = AnswerRecordsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AnswerRecordsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(folder=folder,)
    actual = AnswerRecordsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = AnswerRecordsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AnswerRecordsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = AnswerRecordsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = AnswerRecordsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AnswerRecordsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(project=project,)
    actual = AnswerRecordsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = AnswerRecordsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AnswerRecordsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = AnswerRecordsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = AnswerRecordsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AnswerRecordsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.AnswerRecordsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = AnswerRecordsClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.AnswerRecordsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AnswerRecordsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
