# -*- coding: utf-8 -*-
from unittest import mock

import grpc

import pytest

from google import auth
from google.auth import credentials
from google.cloud.language_v1.services.language_service import LanguageService
from google.cloud.language_v1.services.language_service import transports
from google.cloud.language_v1.types import language_service


def test_analyze_sentiment(transport: str = "grpc"):
    client = LanguageService(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = language_service.AnalyzeSentimentRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.analyze_sentiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeSentimentResponse(
            language="language_value"
        )
        response = client.analyze_sentiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeSentimentResponse)
    assert response.language == "language_value"


def test_analyze_entities(transport: str = "grpc"):
    client = LanguageService(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = language_service.AnalyzeEntitiesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.analyze_entities), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeEntitiesResponse(
            language="language_value"
        )
        response = client.analyze_entities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeEntitiesResponse)
    assert response.language == "language_value"


def test_analyze_entity_sentiment(transport: str = "grpc"):
    client = LanguageService(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = language_service.AnalyzeEntitySentimentRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.analyze_entity_sentiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeEntitySentimentResponse(
            language="language_value"
        )
        response = client.analyze_entity_sentiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeEntitySentimentResponse)
    assert response.language == "language_value"


def test_analyze_syntax(transport: str = "grpc"):
    client = LanguageService(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = language_service.AnalyzeSyntaxRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.analyze_syntax), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeSyntaxResponse(
            language="language_value"
        )
        response = client.analyze_syntax(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeSyntaxResponse)
    assert response.language == "language_value"


def test_classify_text(transport: str = "grpc"):
    client = LanguageService(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = language_service.ClassifyTextRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.classify_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.ClassifyTextResponse()
        response = client.classify_text(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.ClassifyTextResponse)


def test_annotate_text(transport: str = "grpc"):
    client = LanguageService(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = language_service.AnnotateTextRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.annotate_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnnotateTextResponse(
            language="language_value"
        )
        response = client.annotate_text(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnnotateTextResponse)
    assert response.language == "language_value"


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.LanguageServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = LanguageService(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.LanguageServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = LanguageService(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = LanguageService(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.LanguageServiceGrpcTransport)


def test_language_service_base_transport():
    # Instantiate the base transport.
    transport = transports.LanguageServiceTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "analyze_sentiment",
        "analyze_entities",
        "analyze_entity_sentiment",
        "analyze_syntax",
        "classify_text",
        "annotate_text",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_language_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        client = LanguageService()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-language",
                "https://www.googleapis.com/auth/cloud-platform",
            )
        )


def test_language_service_host_no_port():
    client = LanguageService(
        credentials=credentials.AnonymousCredentials(),
        host="language.googleapis.com",
        transport="grpc",
    )
    assert client._transport._host == "language.googleapis.com:443"


def test_language_service_host_with_port():
    client = LanguageService(
        credentials=credentials.AnonymousCredentials(),
        host="language.googleapis.com:8000",
        transport="grpc",
    )
    assert client._transport._host == "language.googleapis.com:8000"


def test_language_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.LanguageServiceGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel
