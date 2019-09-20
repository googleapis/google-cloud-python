# -*- coding: utf-8 -*-
from typing import Callable, Dict

from google.api_core import grpc_helpers  # type: ignore
from google.auth import credentials  # type: ignore

import grpc  # type: ignore

from google.cloud.recommender_v1beta1.types import recommendation
from google.cloud.recommender_v1beta1.types import recommender_service

from .base import RecommenderTransport


class RecommenderGrpcTransport(RecommenderTransport):
    """gRPC backend transport for Recommender.

    Provides recommendations for cloud customers for various
    categories like performance optimization, cost savings,
    reliability, feature discovery, etc. These recommendations are
    generated automatically based on analysis of user resources,
    configuration and monitoring metrics.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "recommender.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
        """
        # Sanity check: Ensure that channel and credentials are not both
        # provided.
        if channel:
            credentials = False

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

        # If a channel was explicitly provided, set it.
        if channel:
            self._grpc_channel = channel

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = grpc_helpers.create_channel(
                self._host, credentials=self._credentials, scopes=self.AUTH_SCOPES
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def list_recommendations(
        self
    ) -> Callable[
        [recommender_service.ListRecommendationsRequest],
        recommender_service.ListRecommendationsResponse,
    ]:
        r"""Return a callable for the list recommendations method over gRPC.

        Lists recommendations for a Cloud project. Requires the
        recommender.*.list IAM permission for the specified recommender.

        Returns:
            Callable[[~.ListRecommendationsRequest],
                    ~.ListRecommendationsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_recommendations" not in self._stubs:
            self._stubs["list_recommendations"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1beta1.Recommender/ListRecommendations",
                request_serializer=recommender_service.ListRecommendationsRequest.serialize,
                response_deserializer=recommender_service.ListRecommendationsResponse.deserialize,
            )
        return self._stubs["list_recommendations"]

    @property
    def get_recommendation(
        self
    ) -> Callable[
        [recommender_service.GetRecommendationRequest], recommendation.Recommendation
    ]:
        r"""Return a callable for the get recommendation method over gRPC.

        Gets the requested recommendation. Requires the
        recommender.*.get IAM permission for the specified recommender.

        Returns:
            Callable[[~.GetRecommendationRequest],
                    ~.Recommendation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_recommendation" not in self._stubs:
            self._stubs["get_recommendation"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1beta1.Recommender/GetRecommendation",
                request_serializer=recommender_service.GetRecommendationRequest.serialize,
                response_deserializer=recommendation.Recommendation.deserialize,
            )
        return self._stubs["get_recommendation"]

    @property
    def mark_recommendation_claimed(
        self
    ) -> Callable[
        [recommender_service.MarkRecommendationClaimedRequest],
        recommendation.Recommendation,
    ]:
        r"""Return a callable for the mark recommendation claimed method over gRPC.

        Mark the Recommendation State as Claimed. Users can use this
        method to indicate to the Recommender API that they are starting
        to apply the recommendation themselves. This stops the
        recommendation content from being updated.

        MarkRecommendationClaimed can be applied to recommendations in
        CLAIMED, SUCCEEDED, FAILED, or ACTIVE state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Returns:
            Callable[[~.MarkRecommendationClaimedRequest],
                    ~.Recommendation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mark_recommendation_claimed" not in self._stubs:
            self._stubs["mark_recommendation_claimed"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1beta1.Recommender/MarkRecommendationClaimed",
                request_serializer=recommender_service.MarkRecommendationClaimedRequest.serialize,
                response_deserializer=recommendation.Recommendation.deserialize,
            )
        return self._stubs["mark_recommendation_claimed"]

    @property
    def mark_recommendation_succeeded(
        self
    ) -> Callable[
        [recommender_service.MarkRecommendationSucceededRequest],
        recommendation.Recommendation,
    ]:
        r"""Return a callable for the mark recommendation succeeded method over gRPC.

        Mark the Recommendation State as Succeeded. Users can use this
        method to indicate to the Recommender API that they have applied
        the recommendation themselves, and the operation was successful.
        This stops the recommendation content from being updated.

        MarkRecommendationSucceeded can be applied to recommendations in
        ACTIVE, CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Returns:
            Callable[[~.MarkRecommendationSucceededRequest],
                    ~.Recommendation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mark_recommendation_succeeded" not in self._stubs:
            self._stubs[
                "mark_recommendation_succeeded"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1beta1.Recommender/MarkRecommendationSucceeded",
                request_serializer=recommender_service.MarkRecommendationSucceededRequest.serialize,
                response_deserializer=recommendation.Recommendation.deserialize,
            )
        return self._stubs["mark_recommendation_succeeded"]

    @property
    def mark_recommendation_failed(
        self
    ) -> Callable[
        [recommender_service.MarkRecommendationFailedRequest],
        recommendation.Recommendation,
    ]:
        r"""Return a callable for the mark recommendation failed method over gRPC.

        Mark the Recommendation State as Failed. Users can use this
        method to indicate to the Recommender API that they have applied
        the recommendation themselves, and the operation failed. This
        stops the recommendation content from being updated.

        MarkRecommendationFailed can be applied to recommendations in
        ACTIVE, CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Returns:
            Callable[[~.MarkRecommendationFailedRequest],
                    ~.Recommendation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mark_recommendation_failed" not in self._stubs:
            self._stubs["mark_recommendation_failed"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1beta1.Recommender/MarkRecommendationFailed",
                request_serializer=recommender_service.MarkRecommendationFailedRequest.serialize,
                response_deserializer=recommendation.Recommendation.deserialize,
            )
        return self._stubs["mark_recommendation_failed"]


__all__ = ("RecommenderGrpcTransport",)
