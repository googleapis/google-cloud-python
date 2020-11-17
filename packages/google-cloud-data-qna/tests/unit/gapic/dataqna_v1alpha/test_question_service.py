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
from google.cloud.dataqna_v1alpha.services.question_service import (
    QuestionServiceAsyncClient,
)
from google.cloud.dataqna_v1alpha.services.question_service import QuestionServiceClient
from google.cloud.dataqna_v1alpha.services.question_service import transports
from google.cloud.dataqna_v1alpha.types import annotated_string
from google.cloud.dataqna_v1alpha.types import question
from google.cloud.dataqna_v1alpha.types import question as gcd_question
from google.cloud.dataqna_v1alpha.types import question_service
from google.cloud.dataqna_v1alpha.types import user_feedback
from google.cloud.dataqna_v1alpha.types import user_feedback as gcd_user_feedback
from google.oauth2 import service_account
from google.protobuf import any_pb2 as gp_any  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore


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

    assert QuestionServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        QuestionServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        QuestionServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        QuestionServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        QuestionServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        QuestionServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [QuestionServiceClient, QuestionServiceAsyncClient]
)
def test_question_service_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "dataqna.googleapis.com:443"


def test_question_service_client_get_transport_class():
    transport = QuestionServiceClient.get_transport_class()
    assert transport == transports.QuestionServiceGrpcTransport

    transport = QuestionServiceClient.get_transport_class("grpc")
    assert transport == transports.QuestionServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (QuestionServiceClient, transports.QuestionServiceGrpcTransport, "grpc"),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    QuestionServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(QuestionServiceClient),
)
@mock.patch.object(
    QuestionServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(QuestionServiceAsyncClient),
)
def test_question_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(QuestionServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(QuestionServiceClient, "get_transport_class") as gtc:
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
            QuestionServiceClient,
            transports.QuestionServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            QuestionServiceClient,
            transports.QuestionServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    QuestionServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(QuestionServiceClient),
)
@mock.patch.object(
    QuestionServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(QuestionServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_question_service_client_mtls_env_auto(
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
        (QuestionServiceClient, transports.QuestionServiceGrpcTransport, "grpc"),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_question_service_client_client_options_scopes(
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
        (QuestionServiceClient, transports.QuestionServiceGrpcTransport, "grpc"),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_question_service_client_client_options_credentials_file(
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


def test_question_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dataqna_v1alpha.services.question_service.transports.QuestionServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = QuestionServiceClient(
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


def test_get_question(
    transport: str = "grpc", request_type=question_service.GetQuestionRequest
):
    client = QuestionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question(
            name="name_value",
            scopes=["scopes_value"],
            query="query_value",
            data_source_annotations=["data_source_annotations_value"],
            user_email="user_email_value",
        )

        response = client.get_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == question_service.GetQuestionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, question.Question)

    assert response.name == "name_value"

    assert response.scopes == ["scopes_value"]

    assert response.query == "query_value"

    assert response.data_source_annotations == ["data_source_annotations_value"]

    assert response.user_email == "user_email_value"


def test_get_question_from_dict():
    test_get_question(request_type=dict)


@pytest.mark.asyncio
async def test_get_question_async(
    transport: str = "grpc_asyncio", request_type=question_service.GetQuestionRequest
):
    client = QuestionServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            question.Question(
                name="name_value",
                scopes=["scopes_value"],
                query="query_value",
                data_source_annotations=["data_source_annotations_value"],
                user_email="user_email_value",
            )
        )

        response = await client.get_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == question_service.GetQuestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, question.Question)

    assert response.name == "name_value"

    assert response.scopes == ["scopes_value"]

    assert response.query == "query_value"

    assert response.data_source_annotations == ["data_source_annotations_value"]

    assert response.user_email == "user_email_value"


@pytest.mark.asyncio
async def test_get_question_async_from_dict():
    await test_get_question_async(request_type=dict)


def test_get_question_field_headers():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.GetQuestionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        call.return_value = question.Question()

        client.get_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_question_field_headers_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.GetQuestionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(question.Question())

        await client.get_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_question_flattened():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_question(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_question_flattened_error():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_question(
            question_service.GetQuestionRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_question_flattened_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(question.Question())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_question(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_question_flattened_error_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_question(
            question_service.GetQuestionRequest(), name="name_value",
        )


def test_create_question(
    transport: str = "grpc", request_type=question_service.CreateQuestionRequest
):
    client = QuestionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_question.Question(
            name="name_value",
            scopes=["scopes_value"],
            query="query_value",
            data_source_annotations=["data_source_annotations_value"],
            user_email="user_email_value",
        )

        response = client.create_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == question_service.CreateQuestionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, gcd_question.Question)

    assert response.name == "name_value"

    assert response.scopes == ["scopes_value"]

    assert response.query == "query_value"

    assert response.data_source_annotations == ["data_source_annotations_value"]

    assert response.user_email == "user_email_value"


def test_create_question_from_dict():
    test_create_question(request_type=dict)


@pytest.mark.asyncio
async def test_create_question_async(
    transport: str = "grpc_asyncio", request_type=question_service.CreateQuestionRequest
):
    client = QuestionServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_question.Question(
                name="name_value",
                scopes=["scopes_value"],
                query="query_value",
                data_source_annotations=["data_source_annotations_value"],
                user_email="user_email_value",
            )
        )

        response = await client.create_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == question_service.CreateQuestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_question.Question)

    assert response.name == "name_value"

    assert response.scopes == ["scopes_value"]

    assert response.query == "query_value"

    assert response.data_source_annotations == ["data_source_annotations_value"]

    assert response.user_email == "user_email_value"


@pytest.mark.asyncio
async def test_create_question_async_from_dict():
    await test_create_question_async(request_type=dict)


def test_create_question_field_headers():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.CreateQuestionRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        call.return_value = gcd_question.Question()

        client.create_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_question_field_headers_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.CreateQuestionRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_question.Question()
        )

        await client.create_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_question_flattened():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_question.Question()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_question(
            parent="parent_value", question=gcd_question.Question(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].question == gcd_question.Question(name="name_value")


def test_create_question_flattened_error():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_question(
            question_service.CreateQuestionRequest(),
            parent="parent_value",
            question=gcd_question.Question(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_question_flattened_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_question.Question()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_question.Question()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_question(
            parent="parent_value", question=gcd_question.Question(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].question == gcd_question.Question(name="name_value")


@pytest.mark.asyncio
async def test_create_question_flattened_error_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_question(
            question_service.CreateQuestionRequest(),
            parent="parent_value",
            question=gcd_question.Question(name="name_value"),
        )


def test_execute_question(
    transport: str = "grpc", request_type=question_service.ExecuteQuestionRequest
):
    client = QuestionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question(
            name="name_value",
            scopes=["scopes_value"],
            query="query_value",
            data_source_annotations=["data_source_annotations_value"],
            user_email="user_email_value",
        )

        response = client.execute_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == question_service.ExecuteQuestionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, question.Question)

    assert response.name == "name_value"

    assert response.scopes == ["scopes_value"]

    assert response.query == "query_value"

    assert response.data_source_annotations == ["data_source_annotations_value"]

    assert response.user_email == "user_email_value"


def test_execute_question_from_dict():
    test_execute_question(request_type=dict)


@pytest.mark.asyncio
async def test_execute_question_async(
    transport: str = "grpc_asyncio",
    request_type=question_service.ExecuteQuestionRequest,
):
    client = QuestionServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            question.Question(
                name="name_value",
                scopes=["scopes_value"],
                query="query_value",
                data_source_annotations=["data_source_annotations_value"],
                user_email="user_email_value",
            )
        )

        response = await client.execute_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == question_service.ExecuteQuestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, question.Question)

    assert response.name == "name_value"

    assert response.scopes == ["scopes_value"]

    assert response.query == "query_value"

    assert response.data_source_annotations == ["data_source_annotations_value"]

    assert response.user_email == "user_email_value"


@pytest.mark.asyncio
async def test_execute_question_async_from_dict():
    await test_execute_question_async(request_type=dict)


def test_execute_question_field_headers():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.ExecuteQuestionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        call.return_value = question.Question()

        client.execute_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_execute_question_field_headers_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.ExecuteQuestionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(question.Question())

        await client.execute_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_execute_question_flattened():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.execute_question(
            name="name_value", interpretation_index=2159,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].interpretation_index == 2159


def test_execute_question_flattened_error():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.execute_question(
            question_service.ExecuteQuestionRequest(),
            name="name_value",
            interpretation_index=2159,
        )


@pytest.mark.asyncio
async def test_execute_question_flattened_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(question.Question())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.execute_question(
            name="name_value", interpretation_index=2159,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].interpretation_index == 2159


@pytest.mark.asyncio
async def test_execute_question_flattened_error_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.execute_question(
            question_service.ExecuteQuestionRequest(),
            name="name_value",
            interpretation_index=2159,
        )


def test_get_user_feedback(
    transport: str = "grpc", request_type=question_service.GetUserFeedbackRequest
):
    client = QuestionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = user_feedback.UserFeedback(
            name="name_value",
            free_form_feedback="free_form_feedback_value",
            rating=user_feedback.UserFeedback.UserFeedbackRating.POSITIVE,
        )

        response = client.get_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == question_service.GetUserFeedbackRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, user_feedback.UserFeedback)

    assert response.name == "name_value"

    assert response.free_form_feedback == "free_form_feedback_value"

    assert response.rating == user_feedback.UserFeedback.UserFeedbackRating.POSITIVE


def test_get_user_feedback_from_dict():
    test_get_user_feedback(request_type=dict)


@pytest.mark.asyncio
async def test_get_user_feedback_async(
    transport: str = "grpc_asyncio",
    request_type=question_service.GetUserFeedbackRequest,
):
    client = QuestionServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            user_feedback.UserFeedback(
                name="name_value",
                free_form_feedback="free_form_feedback_value",
                rating=user_feedback.UserFeedback.UserFeedbackRating.POSITIVE,
            )
        )

        response = await client.get_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == question_service.GetUserFeedbackRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, user_feedback.UserFeedback)

    assert response.name == "name_value"

    assert response.free_form_feedback == "free_form_feedback_value"

    assert response.rating == user_feedback.UserFeedback.UserFeedbackRating.POSITIVE


@pytest.mark.asyncio
async def test_get_user_feedback_async_from_dict():
    await test_get_user_feedback_async(request_type=dict)


def test_get_user_feedback_field_headers():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.GetUserFeedbackRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        call.return_value = user_feedback.UserFeedback()

        client.get_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_user_feedback_field_headers_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.GetUserFeedbackRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            user_feedback.UserFeedback()
        )

        await client.get_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_user_feedback_flattened():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = user_feedback.UserFeedback()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_user_feedback(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_user_feedback_flattened_error():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_user_feedback(
            question_service.GetUserFeedbackRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_user_feedback_flattened_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = user_feedback.UserFeedback()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            user_feedback.UserFeedback()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_user_feedback(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_user_feedback_flattened_error_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_user_feedback(
            question_service.GetUserFeedbackRequest(), name="name_value",
        )


def test_update_user_feedback(
    transport: str = "grpc", request_type=question_service.UpdateUserFeedbackRequest
):
    client = QuestionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_user_feedback.UserFeedback(
            name="name_value",
            free_form_feedback="free_form_feedback_value",
            rating=gcd_user_feedback.UserFeedback.UserFeedbackRating.POSITIVE,
        )

        response = client.update_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == question_service.UpdateUserFeedbackRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, gcd_user_feedback.UserFeedback)

    assert response.name == "name_value"

    assert response.free_form_feedback == "free_form_feedback_value"

    assert response.rating == gcd_user_feedback.UserFeedback.UserFeedbackRating.POSITIVE


def test_update_user_feedback_from_dict():
    test_update_user_feedback(request_type=dict)


@pytest.mark.asyncio
async def test_update_user_feedback_async(
    transport: str = "grpc_asyncio",
    request_type=question_service.UpdateUserFeedbackRequest,
):
    client = QuestionServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_user_feedback.UserFeedback(
                name="name_value",
                free_form_feedback="free_form_feedback_value",
                rating=gcd_user_feedback.UserFeedback.UserFeedbackRating.POSITIVE,
            )
        )

        response = await client.update_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == question_service.UpdateUserFeedbackRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_user_feedback.UserFeedback)

    assert response.name == "name_value"

    assert response.free_form_feedback == "free_form_feedback_value"

    assert response.rating == gcd_user_feedback.UserFeedback.UserFeedbackRating.POSITIVE


@pytest.mark.asyncio
async def test_update_user_feedback_async_from_dict():
    await test_update_user_feedback_async(request_type=dict)


def test_update_user_feedback_field_headers():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.UpdateUserFeedbackRequest()
    request.user_feedback.name = "user_feedback.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        call.return_value = gcd_user_feedback.UserFeedback()

        client.update_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "user_feedback.name=user_feedback.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_user_feedback_field_headers_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.UpdateUserFeedbackRequest()
    request.user_feedback.name = "user_feedback.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_user_feedback.UserFeedback()
        )

        await client.update_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "user_feedback.name=user_feedback.name/value",
    ) in kw["metadata"]


def test_update_user_feedback_flattened():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_user_feedback.UserFeedback()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_user_feedback(
            user_feedback=gcd_user_feedback.UserFeedback(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].user_feedback == gcd_user_feedback.UserFeedback(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_user_feedback_flattened_error():
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_user_feedback(
            question_service.UpdateUserFeedbackRequest(),
            user_feedback=gcd_user_feedback.UserFeedback(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_user_feedback_flattened_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_user_feedback.UserFeedback()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_user_feedback.UserFeedback()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_user_feedback(
            user_feedback=gcd_user_feedback.UserFeedback(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].user_feedback == gcd_user_feedback.UserFeedback(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_user_feedback_flattened_error_async():
    client = QuestionServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_user_feedback(
            question_service.UpdateUserFeedbackRequest(),
            user_feedback=gcd_user_feedback.UserFeedback(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = QuestionServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = QuestionServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = QuestionServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = QuestionServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.QuestionServiceGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.QuestionServiceGrpcTransport,
        transports.QuestionServiceGrpcAsyncIOTransport,
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
    client = QuestionServiceClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.QuestionServiceGrpcTransport,)


def test_question_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.QuestionServiceTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_question_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dataqna_v1alpha.services.question_service.transports.QuestionServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.QuestionServiceTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_question",
        "create_question",
        "execute_question",
        "get_user_feedback",
        "update_user_feedback",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_question_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.dataqna_v1alpha.services.question_service.transports.QuestionServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.QuestionServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_question_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.dataqna_v1alpha.services.question_service.transports.QuestionServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.QuestionServiceTransport()
        adc.assert_called_once()


def test_question_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        QuestionServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_question_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.QuestionServiceGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_question_service_host_no_port():
    client = QuestionServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataqna.googleapis.com"
        ),
    )
    assert client.transport._host == "dataqna.googleapis.com:443"


def test_question_service_host_with_port():
    client = QuestionServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataqna.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "dataqna.googleapis.com:8000"


def test_question_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.QuestionServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_question_service_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.QuestionServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.QuestionServiceGrpcTransport,
        transports.QuestionServiceGrpcAsyncIOTransport,
    ],
)
def test_question_service_transport_channel_mtls_with_client_cert_source(
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
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.QuestionServiceGrpcTransport,
        transports.QuestionServiceGrpcAsyncIOTransport,
    ],
)
def test_question_service_transport_channel_mtls_with_adc(transport_class):
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


def test_question_path():
    project = "squid"
    location = "clam"
    question = "whelk"

    expected = "projects/{project}/locations/{location}/questions/{question}".format(
        project=project, location=location, question=question,
    )
    actual = QuestionServiceClient.question_path(project, location, question)
    assert expected == actual


def test_parse_question_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "question": "nudibranch",
    }
    path = QuestionServiceClient.question_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_question_path(path)
    assert expected == actual


def test_user_feedback_path():
    project = "cuttlefish"
    location = "mussel"
    question = "winkle"

    expected = "projects/{project}/locations/{location}/questions/{question}/userFeedback".format(
        project=project, location=location, question=question,
    )
    actual = QuestionServiceClient.user_feedback_path(project, location, question)
    assert expected == actual


def test_parse_user_feedback_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "question": "abalone",
    }
    path = QuestionServiceClient.user_feedback_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_user_feedback_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = QuestionServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = QuestionServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"

    expected = "folders/{folder}".format(folder=folder,)
    actual = QuestionServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = QuestionServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = QuestionServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = QuestionServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"

    expected = "projects/{project}".format(project=project,)
    actual = QuestionServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = QuestionServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = QuestionServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = QuestionServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.QuestionServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = QuestionServiceClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.QuestionServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = QuestionServiceClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
