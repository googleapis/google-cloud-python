# -*- coding: utf-8 -*-
from unittest import mock

import grpc

import pytest

from google import auth
from google.api_core import future
from google.api_core import operation
from google.api_core import operations_v1
from google.auth import credentials
from google.cloud.vision_v1.services.image_annotator import ImageAnnotator
from google.cloud.vision_v1.services.image_annotator import transports
from google.cloud.vision_v1.types import image_annotator
from google.longrunning import operations_pb2


def test_batch_annotate_images(transport: str = "grpc"):
    client = ImageAnnotator(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = image_annotator.BatchAnnotateImagesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_annotate_images), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = image_annotator.BatchAnnotateImagesResponse()
        response = client.batch_annotate_images(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, image_annotator.BatchAnnotateImagesResponse)


def test_batch_annotate_files(transport: str = "grpc"):
    client = ImageAnnotator(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = image_annotator.BatchAnnotateFilesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_annotate_files), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = image_annotator.BatchAnnotateFilesResponse()
        response = client.batch_annotate_files(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, image_annotator.BatchAnnotateFilesResponse)


def test_async_batch_annotate_images(transport: str = "grpc"):
    client = ImageAnnotator(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = image_annotator.AsyncBatchAnnotateImagesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.async_batch_annotate_images), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.async_batch_annotate_images(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_async_batch_annotate_files(transport: str = "grpc"):
    client = ImageAnnotator(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = image_annotator.AsyncBatchAnnotateFilesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.async_batch_annotate_files), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.async_batch_annotate_files(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ImageAnnotatorGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = ImageAnnotator(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ImageAnnotatorGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = ImageAnnotator(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ImageAnnotator(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.ImageAnnotatorGrpcTransport)


def test_image_annotator_base_transport():
    # Instantiate the base transport.
    transport = transports.ImageAnnotatorTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "batch_annotate_images",
        "batch_annotate_files",
        "async_batch_annotate_images",
        "async_batch_annotate_files",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_image_annotator_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        client = ImageAnnotator()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-vision",
            )
        )


def test_image_annotator_host_no_port():
    client = ImageAnnotator(
        credentials=credentials.AnonymousCredentials(),
        host="vision.googleapis.com",
        transport="grpc",
    )
    assert client._transport._host == "vision.googleapis.com:443"


def test_image_annotator_host_with_port():
    client = ImageAnnotator(
        credentials=credentials.AnonymousCredentials(),
        host="vision.googleapis.com:8000",
        transport="grpc",
    )
    assert client._transport._host == "vision.googleapis.com:8000"


def test_image_annotator_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.ImageAnnotatorGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel


def test_image_annotator_grpc_lro_client():
    client = ImageAnnotator(
        credentials=credentials.AnonymousCredentials(), transport="grpc"
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client
