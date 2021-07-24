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
from google.cloud.firestore_v1.services.firestore import FirestoreAsyncClient
from google.cloud.firestore_v1.services.firestore import FirestoreClient
from google.cloud.firestore_v1.services.firestore import pagers
from google.cloud.firestore_v1.services.firestore import transports
from google.cloud.firestore_v1.services.firestore.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.firestore_v1.types import common
from google.cloud.firestore_v1.types import document
from google.cloud.firestore_v1.types import document as gf_document
from google.cloud.firestore_v1.types import firestore
from google.cloud.firestore_v1.types import query
from google.cloud.firestore_v1.types import write as gf_write
from google.oauth2 import service_account
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from google.type import latlng_pb2  # type: ignore
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

    assert FirestoreClient._get_default_mtls_endpoint(None) is None
    assert FirestoreClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        FirestoreClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        FirestoreClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        FirestoreClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert FirestoreClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [FirestoreClient, FirestoreAsyncClient,])
def test_firestore_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "firestore.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.FirestoreGrpcTransport, "grpc"),
        (transports.FirestoreGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_firestore_client_service_account_always_use_jwt(
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


@pytest.mark.parametrize("client_class", [FirestoreClient, FirestoreAsyncClient,])
def test_firestore_client_from_service_account_file(client_class):
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

        assert client.transport._host == "firestore.googleapis.com:443"


def test_firestore_client_get_transport_class():
    transport = FirestoreClient.get_transport_class()
    available_transports = [
        transports.FirestoreGrpcTransport,
    ]
    assert transport in available_transports

    transport = FirestoreClient.get_transport_class("grpc")
    assert transport == transports.FirestoreGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (FirestoreClient, transports.FirestoreGrpcTransport, "grpc"),
        (
            FirestoreAsyncClient,
            transports.FirestoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    FirestoreClient, "DEFAULT_ENDPOINT", modify_default_endpoint(FirestoreClient)
)
@mock.patch.object(
    FirestoreAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(FirestoreAsyncClient),
)
def test_firestore_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(FirestoreClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(FirestoreClient, "get_transport_class") as gtc:
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
        (FirestoreClient, transports.FirestoreGrpcTransport, "grpc", "true"),
        (
            FirestoreAsyncClient,
            transports.FirestoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (FirestoreClient, transports.FirestoreGrpcTransport, "grpc", "false"),
        (
            FirestoreAsyncClient,
            transports.FirestoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    FirestoreClient, "DEFAULT_ENDPOINT", modify_default_endpoint(FirestoreClient)
)
@mock.patch.object(
    FirestoreAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(FirestoreAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_firestore_client_mtls_env_auto(
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
        (FirestoreClient, transports.FirestoreGrpcTransport, "grpc"),
        (
            FirestoreAsyncClient,
            transports.FirestoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_firestore_client_client_options_scopes(
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
        (FirestoreClient, transports.FirestoreGrpcTransport, "grpc"),
        (
            FirestoreAsyncClient,
            transports.FirestoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_firestore_client_client_options_credentials_file(
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


def test_firestore_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.firestore_v1.services.firestore.transports.FirestoreGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = FirestoreClient(client_options={"api_endpoint": "squid.clam.whelk"})
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


def test_get_document(
    transport: str = "grpc", request_type=firestore.GetDocumentRequest
):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = document.Document(name="name_value",)
        response = client.get_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.GetDocumentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, document.Document)
    assert response.name == "name_value"


def test_get_document_from_dict():
    test_get_document(request_type=dict)


def test_get_document_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_document), "__call__") as call:
        client.get_document()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.GetDocumentRequest()


@pytest.mark.asyncio
async def test_get_document_async(
    transport: str = "grpc_asyncio", request_type=firestore.GetDocumentRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            document.Document(name="name_value",)
        )
        response = await client.get_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.GetDocumentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, document.Document)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_document_async_from_dict():
    await test_get_document_async(request_type=dict)


def test_get_document_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.GetDocumentRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_document), "__call__") as call:
        call.return_value = document.Document()
        client.get_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_document_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.GetDocumentRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_document), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(document.Document())
        await client.get_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_list_documents(
    transport: str = "grpc", request_type=firestore.ListDocumentsRequest
):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_documents), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.ListDocumentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.ListDocumentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDocumentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_documents_from_dict():
    test_list_documents(request_type=dict)


def test_list_documents_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_documents), "__call__") as call:
        client.list_documents()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.ListDocumentsRequest()


@pytest.mark.asyncio
async def test_list_documents_async(
    transport: str = "grpc_asyncio", request_type=firestore.ListDocumentsRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_documents), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.ListDocumentsResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.ListDocumentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDocumentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_documents_async_from_dict():
    await test_list_documents_async(request_type=dict)


def test_list_documents_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.ListDocumentsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_documents), "__call__") as call:
        call.return_value = firestore.ListDocumentsResponse()
        client.list_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_documents_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.ListDocumentsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_documents), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.ListDocumentsResponse()
        )
        await client.list_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_documents_pager():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_documents), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.ListDocumentsResponse(
                documents=[
                    document.Document(),
                    document.Document(),
                    document.Document(),
                ],
                next_page_token="abc",
            ),
            firestore.ListDocumentsResponse(documents=[], next_page_token="def",),
            firestore.ListDocumentsResponse(
                documents=[document.Document(),], next_page_token="ghi",
            ),
            firestore.ListDocumentsResponse(
                documents=[document.Document(), document.Document(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_documents(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, document.Document) for i in results)


def test_list_documents_pages():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_documents), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.ListDocumentsResponse(
                documents=[
                    document.Document(),
                    document.Document(),
                    document.Document(),
                ],
                next_page_token="abc",
            ),
            firestore.ListDocumentsResponse(documents=[], next_page_token="def",),
            firestore.ListDocumentsResponse(
                documents=[document.Document(),], next_page_token="ghi",
            ),
            firestore.ListDocumentsResponse(
                documents=[document.Document(), document.Document(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_documents(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_documents_async_pager():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_documents), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.ListDocumentsResponse(
                documents=[
                    document.Document(),
                    document.Document(),
                    document.Document(),
                ],
                next_page_token="abc",
            ),
            firestore.ListDocumentsResponse(documents=[], next_page_token="def",),
            firestore.ListDocumentsResponse(
                documents=[document.Document(),], next_page_token="ghi",
            ),
            firestore.ListDocumentsResponse(
                documents=[document.Document(), document.Document(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_documents(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, document.Document) for i in responses)


@pytest.mark.asyncio
async def test_list_documents_async_pages():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_documents), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.ListDocumentsResponse(
                documents=[
                    document.Document(),
                    document.Document(),
                    document.Document(),
                ],
                next_page_token="abc",
            ),
            firestore.ListDocumentsResponse(documents=[], next_page_token="def",),
            firestore.ListDocumentsResponse(
                documents=[document.Document(),], next_page_token="ghi",
            ),
            firestore.ListDocumentsResponse(
                documents=[document.Document(), document.Document(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_documents(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_document(
    transport: str = "grpc", request_type=firestore.UpdateDocumentRequest
):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gf_document.Document(name="name_value",)
        response = client.update_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.UpdateDocumentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gf_document.Document)
    assert response.name == "name_value"


def test_update_document_from_dict():
    test_update_document(request_type=dict)


def test_update_document_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_document), "__call__") as call:
        client.update_document()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.UpdateDocumentRequest()


@pytest.mark.asyncio
async def test_update_document_async(
    transport: str = "grpc_asyncio", request_type=firestore.UpdateDocumentRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gf_document.Document(name="name_value",)
        )
        response = await client.update_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.UpdateDocumentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gf_document.Document)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_update_document_async_from_dict():
    await test_update_document_async(request_type=dict)


def test_update_document_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.UpdateDocumentRequest()

    request.document.name = "document.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_document), "__call__") as call:
        call.return_value = gf_document.Document()
        client.update_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "document.name=document.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_document_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.UpdateDocumentRequest()

    request.document.name = "document.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_document), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gf_document.Document()
        )
        await client.update_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "document.name=document.name/value",) in kw[
        "metadata"
    ]


def test_update_document_flattened():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gf_document.Document()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_document(
            document=gf_document.Document(name="name_value"),
            update_mask=common.DocumentMask(field_paths=["field_paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].document == gf_document.Document(name="name_value")
        assert args[0].update_mask == common.DocumentMask(
            field_paths=["field_paths_value"]
        )


def test_update_document_flattened_error():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_document(
            firestore.UpdateDocumentRequest(),
            document=gf_document.Document(name="name_value"),
            update_mask=common.DocumentMask(field_paths=["field_paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_document_flattened_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gf_document.Document()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gf_document.Document()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_document(
            document=gf_document.Document(name="name_value"),
            update_mask=common.DocumentMask(field_paths=["field_paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].document == gf_document.Document(name="name_value")
        assert args[0].update_mask == common.DocumentMask(
            field_paths=["field_paths_value"]
        )


@pytest.mark.asyncio
async def test_update_document_flattened_error_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_document(
            firestore.UpdateDocumentRequest(),
            document=gf_document.Document(name="name_value"),
            update_mask=common.DocumentMask(field_paths=["field_paths_value"]),
        )


def test_delete_document(
    transport: str = "grpc", request_type=firestore.DeleteDocumentRequest
):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.DeleteDocumentRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_document_from_dict():
    test_delete_document(request_type=dict)


def test_delete_document_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_document), "__call__") as call:
        client.delete_document()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.DeleteDocumentRequest()


@pytest.mark.asyncio
async def test_delete_document_async(
    transport: str = "grpc_asyncio", request_type=firestore.DeleteDocumentRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.DeleteDocumentRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_document_async_from_dict():
    await test_delete_document_async(request_type=dict)


def test_delete_document_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.DeleteDocumentRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_document), "__call__") as call:
        call.return_value = None
        client.delete_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_document_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.DeleteDocumentRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_document), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_document_flattened():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_document(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_document_flattened_error():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_document(
            firestore.DeleteDocumentRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_document_flattened_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_document(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_document_flattened_error_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_document(
            firestore.DeleteDocumentRequest(), name="name_value",
        )


def test_batch_get_documents(
    transport: str = "grpc", request_type=firestore.BatchGetDocumentsRequest
):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_get_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([firestore.BatchGetDocumentsResponse()])
        response = client.batch_get_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.BatchGetDocumentsRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, firestore.BatchGetDocumentsResponse)


def test_batch_get_documents_from_dict():
    test_batch_get_documents(request_type=dict)


def test_batch_get_documents_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_get_documents), "__call__"
    ) as call:
        client.batch_get_documents()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.BatchGetDocumentsRequest()


@pytest.mark.asyncio
async def test_batch_get_documents_async(
    transport: str = "grpc_asyncio", request_type=firestore.BatchGetDocumentsRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_get_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[firestore.BatchGetDocumentsResponse()]
        )
        response = await client.batch_get_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.BatchGetDocumentsRequest()

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, firestore.BatchGetDocumentsResponse)


@pytest.mark.asyncio
async def test_batch_get_documents_async_from_dict():
    await test_batch_get_documents_async(request_type=dict)


def test_batch_get_documents_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.BatchGetDocumentsRequest()

    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_get_documents), "__call__"
    ) as call:
        call.return_value = iter([firestore.BatchGetDocumentsResponse()])
        client.batch_get_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_get_documents_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.BatchGetDocumentsRequest()

    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_get_documents), "__call__"
    ) as call:
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[firestore.BatchGetDocumentsResponse()]
        )
        await client.batch_get_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


def test_begin_transaction(
    transport: str = "grpc", request_type=firestore.BeginTransactionRequest
):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.BeginTransactionResponse(
            transaction=b"transaction_blob",
        )
        response = client.begin_transaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.BeginTransactionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, firestore.BeginTransactionResponse)
    assert response.transaction == b"transaction_blob"


def test_begin_transaction_from_dict():
    test_begin_transaction(request_type=dict)


def test_begin_transaction_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        client.begin_transaction()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.BeginTransactionRequest()


@pytest.mark.asyncio
async def test_begin_transaction_async(
    transport: str = "grpc_asyncio", request_type=firestore.BeginTransactionRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.BeginTransactionResponse(transaction=b"transaction_blob",)
        )
        response = await client.begin_transaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.BeginTransactionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, firestore.BeginTransactionResponse)
    assert response.transaction == b"transaction_blob"


@pytest.mark.asyncio
async def test_begin_transaction_async_from_dict():
    await test_begin_transaction_async(request_type=dict)


def test_begin_transaction_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.BeginTransactionRequest()

    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        call.return_value = firestore.BeginTransactionResponse()
        client.begin_transaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_begin_transaction_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.BeginTransactionRequest()

    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.BeginTransactionResponse()
        )
        await client.begin_transaction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


def test_begin_transaction_flattened():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.BeginTransactionResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.begin_transaction(database="database_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].database == "database_value"


def test_begin_transaction_flattened_error():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.begin_transaction(
            firestore.BeginTransactionRequest(), database="database_value",
        )


@pytest.mark.asyncio
async def test_begin_transaction_flattened_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.begin_transaction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.BeginTransactionResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.BeginTransactionResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.begin_transaction(database="database_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].database == "database_value"


@pytest.mark.asyncio
async def test_begin_transaction_flattened_error_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.begin_transaction(
            firestore.BeginTransactionRequest(), database="database_value",
        )


def test_commit(transport: str = "grpc", request_type=firestore.CommitRequest):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.CommitResponse()
        response = client.commit(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.CommitRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, firestore.CommitResponse)


def test_commit_from_dict():
    test_commit(request_type=dict)


def test_commit_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        client.commit()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.CommitRequest()


@pytest.mark.asyncio
async def test_commit_async(
    transport: str = "grpc_asyncio", request_type=firestore.CommitRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.CommitResponse()
        )
        response = await client.commit(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.CommitRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, firestore.CommitResponse)


@pytest.mark.asyncio
async def test_commit_async_from_dict():
    await test_commit_async(request_type=dict)


def test_commit_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.CommitRequest()

    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        call.return_value = firestore.CommitResponse()
        client.commit(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_commit_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.CommitRequest()

    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.CommitResponse()
        )
        await client.commit(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


def test_commit_flattened():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.CommitResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.commit(
            database="database_value",
            writes=[gf_write.Write(update=document.Document(name="name_value"))],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].database == "database_value"
        assert args[0].writes == [
            gf_write.Write(update=document.Document(name="name_value"))
        ]


def test_commit_flattened_error():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.commit(
            firestore.CommitRequest(),
            database="database_value",
            writes=[gf_write.Write(update=document.Document(name="name_value"))],
        )


@pytest.mark.asyncio
async def test_commit_flattened_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.CommitResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.CommitResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.commit(
            database="database_value",
            writes=[gf_write.Write(update=document.Document(name="name_value"))],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].database == "database_value"
        assert args[0].writes == [
            gf_write.Write(update=document.Document(name="name_value"))
        ]


@pytest.mark.asyncio
async def test_commit_flattened_error_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.commit(
            firestore.CommitRequest(),
            database="database_value",
            writes=[gf_write.Write(update=document.Document(name="name_value"))],
        )


def test_rollback(transport: str = "grpc", request_type=firestore.RollbackRequest):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.rollback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.RollbackRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_rollback_from_dict():
    test_rollback(request_type=dict)


def test_rollback_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        client.rollback()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.RollbackRequest()


@pytest.mark.asyncio
async def test_rollback_async(
    transport: str = "grpc_asyncio", request_type=firestore.RollbackRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.rollback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.RollbackRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_rollback_async_from_dict():
    await test_rollback_async(request_type=dict)


def test_rollback_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.RollbackRequest()

    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        call.return_value = None
        client.rollback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_rollback_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.RollbackRequest()

    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.rollback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


def test_rollback_flattened():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rollback(
            database="database_value", transaction=b"transaction_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].database == "database_value"
        assert args[0].transaction == b"transaction_blob"


def test_rollback_flattened_error():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rollback(
            firestore.RollbackRequest(),
            database="database_value",
            transaction=b"transaction_blob",
        )


@pytest.mark.asyncio
async def test_rollback_flattened_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rollback(
            database="database_value", transaction=b"transaction_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].database == "database_value"
        assert args[0].transaction == b"transaction_blob"


@pytest.mark.asyncio
async def test_rollback_flattened_error_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rollback(
            firestore.RollbackRequest(),
            database="database_value",
            transaction=b"transaction_blob",
        )


def test_run_query(transport: str = "grpc", request_type=firestore.RunQueryRequest):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_query), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([firestore.RunQueryResponse()])
        response = client.run_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.RunQueryRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, firestore.RunQueryResponse)


def test_run_query_from_dict():
    test_run_query(request_type=dict)


def test_run_query_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_query), "__call__") as call:
        client.run_query()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.RunQueryRequest()


@pytest.mark.asyncio
async def test_run_query_async(
    transport: str = "grpc_asyncio", request_type=firestore.RunQueryRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_query), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[firestore.RunQueryResponse()]
        )
        response = await client.run_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.RunQueryRequest()

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, firestore.RunQueryResponse)


@pytest.mark.asyncio
async def test_run_query_async_from_dict():
    await test_run_query_async(request_type=dict)


def test_run_query_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.RunQueryRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_query), "__call__") as call:
        call.return_value = iter([firestore.RunQueryResponse()])
        client.run_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_run_query_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.RunQueryRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_query), "__call__") as call:
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[firestore.RunQueryResponse()]
        )
        await client.run_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_partition_query(
    transport: str = "grpc", request_type=firestore.PartitionQueryRequest
):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.PartitionQueryResponse(
            next_page_token="next_page_token_value",
        )
        response = client.partition_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.PartitionQueryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.PartitionQueryPager)
    assert response.next_page_token == "next_page_token_value"


def test_partition_query_from_dict():
    test_partition_query(request_type=dict)


def test_partition_query_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        client.partition_query()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.PartitionQueryRequest()


@pytest.mark.asyncio
async def test_partition_query_async(
    transport: str = "grpc_asyncio", request_type=firestore.PartitionQueryRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.PartitionQueryResponse(next_page_token="next_page_token_value",)
        )
        response = await client.partition_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.PartitionQueryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.PartitionQueryAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_partition_query_async_from_dict():
    await test_partition_query_async(request_type=dict)


def test_partition_query_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.PartitionQueryRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        call.return_value = firestore.PartitionQueryResponse()
        client.partition_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_partition_query_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.PartitionQueryRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.PartitionQueryResponse()
        )
        await client.partition_query(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_partition_query_pager():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(), query.Cursor(), query.Cursor(),],
                next_page_token="abc",
            ),
            firestore.PartitionQueryResponse(partitions=[], next_page_token="def",),
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(),], next_page_token="ghi",
            ),
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(), query.Cursor(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.partition_query(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, query.Cursor) for i in results)


def test_partition_query_pages():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.partition_query), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(), query.Cursor(), query.Cursor(),],
                next_page_token="abc",
            ),
            firestore.PartitionQueryResponse(partitions=[], next_page_token="def",),
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(),], next_page_token="ghi",
            ),
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(), query.Cursor(),],
            ),
            RuntimeError,
        )
        pages = list(client.partition_query(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_partition_query_async_pager():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.partition_query), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(), query.Cursor(), query.Cursor(),],
                next_page_token="abc",
            ),
            firestore.PartitionQueryResponse(partitions=[], next_page_token="def",),
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(),], next_page_token="ghi",
            ),
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(), query.Cursor(),],
            ),
            RuntimeError,
        )
        async_pager = await client.partition_query(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, query.Cursor) for i in responses)


@pytest.mark.asyncio
async def test_partition_query_async_pages():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.partition_query), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(), query.Cursor(), query.Cursor(),],
                next_page_token="abc",
            ),
            firestore.PartitionQueryResponse(partitions=[], next_page_token="def",),
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(),], next_page_token="ghi",
            ),
            firestore.PartitionQueryResponse(
                partitions=[query.Cursor(), query.Cursor(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.partition_query(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_write(transport: str = "grpc", request_type=firestore.WriteRequest):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.write), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([firestore.WriteResponse()])
        response = client.write(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, firestore.WriteResponse)


def test_write_from_dict():
    test_write(request_type=dict)


@pytest.mark.asyncio
async def test_write_async(
    transport: str = "grpc_asyncio", request_type=firestore.WriteRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.write), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(side_effect=[firestore.WriteResponse()])
        response = await client.write(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, firestore.WriteResponse)


@pytest.mark.asyncio
async def test_write_async_from_dict():
    await test_write_async(request_type=dict)


def test_listen(transport: str = "grpc", request_type=firestore.ListenRequest):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.listen), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([firestore.ListenResponse()])
        response = client.listen(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, firestore.ListenResponse)


def test_listen_from_dict():
    test_listen(request_type=dict)


@pytest.mark.asyncio
async def test_listen_async(
    transport: str = "grpc_asyncio", request_type=firestore.ListenRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.listen), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[firestore.ListenResponse()]
        )
        response = await client.listen(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, firestore.ListenResponse)


@pytest.mark.asyncio
async def test_listen_async_from_dict():
    await test_listen_async(request_type=dict)


def test_list_collection_ids(
    transport: str = "grpc", request_type=firestore.ListCollectionIdsRequest
):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.ListCollectionIdsResponse(
            collection_ids=["collection_ids_value"],
            next_page_token="next_page_token_value",
        )
        response = client.list_collection_ids(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.ListCollectionIdsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCollectionIdsPager)
    assert response.collection_ids == ["collection_ids_value"]
    assert response.next_page_token == "next_page_token_value"


def test_list_collection_ids_from_dict():
    test_list_collection_ids(request_type=dict)


def test_list_collection_ids_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids), "__call__"
    ) as call:
        client.list_collection_ids()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.ListCollectionIdsRequest()


@pytest.mark.asyncio
async def test_list_collection_ids_async(
    transport: str = "grpc_asyncio", request_type=firestore.ListCollectionIdsRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.ListCollectionIdsResponse(
                collection_ids=["collection_ids_value"],
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_collection_ids(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.ListCollectionIdsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCollectionIdsAsyncPager)
    assert response.collection_ids == ["collection_ids_value"]
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_collection_ids_async_from_dict():
    await test_list_collection_ids_async(request_type=dict)


def test_list_collection_ids_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.ListCollectionIdsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids), "__call__"
    ) as call:
        call.return_value = firestore.ListCollectionIdsResponse()
        client.list_collection_ids(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_collection_ids_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.ListCollectionIdsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.ListCollectionIdsResponse()
        )
        await client.list_collection_ids(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_collection_ids_flattened():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.ListCollectionIdsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_collection_ids(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_collection_ids_flattened_error():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_collection_ids(
            firestore.ListCollectionIdsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_collection_ids_flattened_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.ListCollectionIdsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.ListCollectionIdsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_collection_ids(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_collection_ids_flattened_error_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_collection_ids(
            firestore.ListCollectionIdsRequest(), parent="parent_value",
        )


def test_list_collection_ids_pager():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.ListCollectionIdsResponse(
                collection_ids=[str(), str(), str(),], next_page_token="abc",
            ),
            firestore.ListCollectionIdsResponse(
                collection_ids=[], next_page_token="def",
            ),
            firestore.ListCollectionIdsResponse(
                collection_ids=[str(),], next_page_token="ghi",
            ),
            firestore.ListCollectionIdsResponse(collection_ids=[str(), str(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_collection_ids(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, str) for i in results)


def test_list_collection_ids_pages():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.ListCollectionIdsResponse(
                collection_ids=[str(), str(), str(),], next_page_token="abc",
            ),
            firestore.ListCollectionIdsResponse(
                collection_ids=[], next_page_token="def",
            ),
            firestore.ListCollectionIdsResponse(
                collection_ids=[str(),], next_page_token="ghi",
            ),
            firestore.ListCollectionIdsResponse(collection_ids=[str(), str(),],),
            RuntimeError,
        )
        pages = list(client.list_collection_ids(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_collection_ids_async_pager():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.ListCollectionIdsResponse(
                collection_ids=[str(), str(), str(),], next_page_token="abc",
            ),
            firestore.ListCollectionIdsResponse(
                collection_ids=[], next_page_token="def",
            ),
            firestore.ListCollectionIdsResponse(
                collection_ids=[str(),], next_page_token="ghi",
            ),
            firestore.ListCollectionIdsResponse(collection_ids=[str(), str(),],),
            RuntimeError,
        )
        async_pager = await client.list_collection_ids(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, str) for i in responses)


@pytest.mark.asyncio
async def test_list_collection_ids_async_pages():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_collection_ids),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            firestore.ListCollectionIdsResponse(
                collection_ids=[str(), str(), str(),], next_page_token="abc",
            ),
            firestore.ListCollectionIdsResponse(
                collection_ids=[], next_page_token="def",
            ),
            firestore.ListCollectionIdsResponse(
                collection_ids=[str(),], next_page_token="ghi",
            ),
            firestore.ListCollectionIdsResponse(collection_ids=[str(), str(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_collection_ids(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_batch_write(transport: str = "grpc", request_type=firestore.BatchWriteRequest):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_write), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = firestore.BatchWriteResponse()
        response = client.batch_write(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.BatchWriteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, firestore.BatchWriteResponse)


def test_batch_write_from_dict():
    test_batch_write(request_type=dict)


def test_batch_write_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_write), "__call__") as call:
        client.batch_write()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.BatchWriteRequest()


@pytest.mark.asyncio
async def test_batch_write_async(
    transport: str = "grpc_asyncio", request_type=firestore.BatchWriteRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_write), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.BatchWriteResponse()
        )
        response = await client.batch_write(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.BatchWriteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, firestore.BatchWriteResponse)


@pytest.mark.asyncio
async def test_batch_write_async_from_dict():
    await test_batch_write_async(request_type=dict)


def test_batch_write_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.BatchWriteRequest()

    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_write), "__call__") as call:
        call.return_value = firestore.BatchWriteResponse()
        client.batch_write(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_write_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.BatchWriteRequest()

    request.database = "database/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_write), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            firestore.BatchWriteResponse()
        )
        await client.batch_write(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "database=database/value",) in kw["metadata"]


def test_create_document(
    transport: str = "grpc", request_type=firestore.CreateDocumentRequest
):
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = document.Document(name="name_value",)
        response = client.create_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.CreateDocumentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, document.Document)
    assert response.name == "name_value"


def test_create_document_from_dict():
    test_create_document(request_type=dict)


def test_create_document_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_document), "__call__") as call:
        client.create_document()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.CreateDocumentRequest()


@pytest.mark.asyncio
async def test_create_document_async(
    transport: str = "grpc_asyncio", request_type=firestore.CreateDocumentRequest
):
    client = FirestoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_document), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            document.Document(name="name_value",)
        )
        response = await client.create_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == firestore.CreateDocumentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, document.Document)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_create_document_async_from_dict():
    await test_create_document_async(request_type=dict)


def test_create_document_field_headers():
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.CreateDocumentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_document), "__call__") as call:
        call.return_value = document.Document()
        client.create_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_document_field_headers_async():
    client = FirestoreAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = firestore.CreateDocumentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_document), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(document.Document())
        await client.create_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.FirestoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirestoreClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.FirestoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirestoreClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.FirestoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirestoreClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.FirestoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = FirestoreClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.FirestoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.FirestoreGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.FirestoreGrpcTransport, transports.FirestoreGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = FirestoreClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.FirestoreGrpcTransport,)


def test_firestore_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.FirestoreTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_firestore_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.firestore_v1.services.firestore.transports.FirestoreTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.FirestoreTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_document",
        "list_documents",
        "update_document",
        "delete_document",
        "batch_get_documents",
        "begin_transaction",
        "commit",
        "rollback",
        "run_query",
        "partition_query",
        "write",
        "listen",
        "list_collection_ids",
        "batch_write",
        "create_document",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_firestore_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.firestore_v1.services.firestore.transports.FirestoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.FirestoreTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_firestore_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.firestore_v1.services.firestore.transports.FirestoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.FirestoreTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id="octopus",
        )


def test_firestore_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.firestore_v1.services.firestore.transports.FirestoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.FirestoreTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_firestore_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        FirestoreClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_firestore_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        FirestoreClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.FirestoreGrpcTransport, transports.FirestoreGrpcAsyncIOTransport,],
)
@requires_google_auth_gte_1_25_0
def test_firestore_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.FirestoreGrpcTransport, transports.FirestoreGrpcAsyncIOTransport,],
)
@requires_google_auth_lt_1_25_0
def test_firestore_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.FirestoreGrpcTransport, grpc_helpers),
        (transports.FirestoreGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_firestore_transport_create_channel(transport_class, grpc_helpers):
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
            "firestore.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore",
            ),
            scopes=["1", "2"],
            default_host="firestore.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.FirestoreGrpcTransport, transports.FirestoreGrpcAsyncIOTransport],
)
def test_firestore_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_firestore_host_no_port():
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="firestore.googleapis.com"
        ),
    )
    assert client.transport._host == "firestore.googleapis.com:443"


def test_firestore_host_with_port():
    client = FirestoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="firestore.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "firestore.googleapis.com:8000"


def test_firestore_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.FirestoreGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_firestore_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.FirestoreGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.FirestoreGrpcTransport, transports.FirestoreGrpcAsyncIOTransport],
)
def test_firestore_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.FirestoreGrpcTransport, transports.FirestoreGrpcAsyncIOTransport],
)
def test_firestore_transport_channel_mtls_with_adc(transport_class):
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


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = FirestoreClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = FirestoreClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = FirestoreClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = FirestoreClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = FirestoreClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = FirestoreClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = FirestoreClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = FirestoreClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = FirestoreClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = FirestoreClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = FirestoreClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = FirestoreClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = FirestoreClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = FirestoreClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = FirestoreClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.FirestoreTransport, "_prep_wrapped_messages"
    ) as prep:
        client = FirestoreClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.FirestoreTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = FirestoreClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
