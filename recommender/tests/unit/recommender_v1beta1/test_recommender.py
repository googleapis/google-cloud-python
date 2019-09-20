# -*- coding: utf-8 -*-
from unittest import mock

import grpc

import pytest

from google import auth
from google.auth import credentials
from google.cloud.recommender_v1beta1.services.recommender import Recommender
from google.cloud.recommender_v1beta1.services.recommender import pagers
from google.cloud.recommender_v1beta1.services.recommender import transports
from google.cloud.recommender_v1beta1.types import recommendation
from google.cloud.recommender_v1beta1.types import recommender_service


def test_list_recommendations(transport: str = "grpc"):
    client = Recommender(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recommender_service.ListRecommendationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_recommendations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommender_service.ListRecommendationsResponse(
            next_page_token="next_page_token_value"
        )
        response = client.list_recommendations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRecommendationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_recommendations_field_headers():
    client = Recommender(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.ListRecommendationsRequest(parent="parent/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_recommendations), "__call__"
    ) as call:
        call.return_value = recommender_service.ListRecommendationsResponse()
        client.list_recommendations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_recommendations_pager():
    client = Recommender(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_recommendations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recommender_service.ListRecommendationsResponse(
                recommendations=[
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                ],
                next_page_token="abc",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[], next_page_token="def"
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[recommendation.Recommendation()], next_page_token="ghi"
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                ]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_recommendations(request={})]
        assert len(results) == 6
        assert all([isinstance(i, recommendation.Recommendation) for i in results])


def test_get_recommendation(transport: str = "grpc"):
    client = Recommender(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recommender_service.GetRecommendationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_recommendation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation(
            name="name_value",
            description="description_value",
            recommender_subtype="recommender_subtype_value",
            etag="etag_value",
        )
        response = client.get_recommendation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


def test_get_recommendation_field_headers():
    client = Recommender(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.GetRecommendationRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_recommendation), "__call__"
    ) as call:
        call.return_value = recommendation.Recommendation()
        client.get_recomemndation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_mark_recommendation_claimed(transport: str = "grpc"):
    client = Recommender(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recommender_service.MarkRecommendationClaimedRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.mark_recommendation_claimed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation(
            name="name_value",
            description="description_value",
            recommender_subtype="recommender_subtype_value",
            etag="etag_value",
        )
        response = client.mark_recommendation_claimed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


def test_mark_recommendation_succeeded(transport: str = "grpc"):
    client = Recommender(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recommender_service.MarkRecommendationSucceededRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.mark_recommendation_succeeded), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation(
            name="name_value",
            description="description_value",
            recommender_subtype="recommender_subtype_value",
            etag="etag_value",
        )
        response = client.mark_recommendation_succeeded(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


def test_mark_recommendation_failed(transport: str = "grpc"):
    client = Recommender(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recommender_service.MarkRecommendationFailedRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.mark_recommendation_failed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation(
            name="name_value",
            description="description_value",
            recommender_subtype="recommender_subtype_value",
            etag="etag_value",
        )
        response = client.mark_recommendation_failed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.RecommenderGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        Recommender(credentials=credentials.AnonymousCredentials(), transport=transport)


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RecommenderGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = Recommender(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = Recommender(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.RecommenderGrpcTransport)


def test_recommender_base_transport():
    # Instantiate the base transport.
    transport = transports.RecommenderTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_recommendations",
        "get_recommendation",
        "mark_recommendation_claimed",
        "mark_recommendation_succeeded",
        "mark_recommendation_failed",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_recommender_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        Recommender()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_recommender_host_no_port():
    client = Recommender(
        credentials=credentials.AnonymousCredentials(),
        host="recommender.googleapis.com",
        transport="grpc",
    )
    assert client._transport._host == "recommender.googleapis.com:443"


def test_recommender_host_with_port():
    client = Recommender(
        credentials=credentials.AnonymousCredentials(),
        host="recommender.googleapis.com:8000",
        transport="grpc",
    )
    assert client._transport._host == "recommender.googleapis.com:8000"


def test_recommender_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.RecommenderGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel
