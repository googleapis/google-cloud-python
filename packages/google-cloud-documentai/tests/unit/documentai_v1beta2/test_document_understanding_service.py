# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api_core import client_options
from google.api_core import future
from google.api_core import operations_v1
from google.auth import credentials
from google.cloud.documentai_v1beta2.services.document_understanding_service import (
    DocumentUnderstandingServiceClient,
)
from google.cloud.documentai_v1beta2.services.document_understanding_service import (
    transports,
)
from google.cloud.documentai_v1beta2.types import document
from google.cloud.documentai_v1beta2.types import document_understanding
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.rpc import status_pb2 as status  # type: ignore


def test_document_understanding_service_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = DocumentUnderstandingServiceClient.from_service_account_file(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        client = DocumentUnderstandingServiceClient.from_service_account_json(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        assert client._transport._host == "us-documentai.googleapis.com:443"


def test_document_understanding_service_client_client_options():
    # Check the default options have their expected values.
    assert (
        DocumentUnderstandingServiceClient.DEFAULT_OPTIONS.api_endpoint
        == "us-documentai.googleapis.com"
    )

    # Check that options can be customized.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.documentai_v1beta2.services.document_understanding_service.DocumentUnderstandingServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = DocumentUnderstandingServiceClient(client_options=options)
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_document_understanding_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.documentai_v1beta2.services.document_understanding_service.DocumentUnderstandingServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = DocumentUnderstandingServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_batch_process_documents(transport: str = "grpc"):
    client = DocumentUnderstandingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = document_understanding.BatchProcessDocumentsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_process_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.batch_process_documents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_batch_process_documents_flattened():
    client = DocumentUnderstandingServiceClient(
        credentials=credentials.AnonymousCredentials()
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_process_documents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.batch_process_documents(
            requests=[
                document_understanding.ProcessDocumentRequest(parent="parent_value")
            ]
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].requests == [
            document_understanding.ProcessDocumentRequest(parent="parent_value")
        ]


def test_batch_process_documents_flattened_error():
    client = DocumentUnderstandingServiceClient(
        credentials=credentials.AnonymousCredentials()
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_process_documents(
            document_understanding.BatchProcessDocumentsRequest(),
            requests=[
                document_understanding.ProcessDocumentRequest(parent="parent_value")
            ],
        )


def test_process_document(transport: str = "grpc"):
    client = DocumentUnderstandingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = document_understanding.ProcessDocumentRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.process_document), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = document.Document(
            uri="uri_value",
            content=b"content_blob",
            mime_type="mime_type_value",
            text="text_value",
        )

        response = client.process_document(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, document.Document)
    assert response.uri == "uri_value"
    assert response.content == b"content_blob"
    assert response.mime_type == "mime_type_value"
    assert response.text == "text_value"


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DocumentUnderstandingServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = DocumentUnderstandingServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DocumentUnderstandingServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = DocumentUnderstandingServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DocumentUnderstandingServiceClient(
        credentials=credentials.AnonymousCredentials()
    )
    assert isinstance(
        client._transport, transports.DocumentUnderstandingServiceGrpcTransport
    )


def test_document_understanding_service_base_transport():
    # Instantiate the base transport.
    transport = transports.DocumentUnderstandingServiceTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = ("batch_process_documents", "process_document")
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_document_understanding_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        DocumentUnderstandingServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_document_understanding_service_host_no_port():
    client = DocumentUnderstandingServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="us-documentai.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "us-documentai.googleapis.com:443"


def test_document_understanding_service_host_with_port():
    client = DocumentUnderstandingServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="us-documentai.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "us-documentai.googleapis.com:8000"


def test_document_understanding_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.DocumentUnderstandingServiceGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel


def test_document_understanding_service_grpc_lro_client():
    client = DocumentUnderstandingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc"
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client
