# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import google.api_core.grpc_helpers

from google.cloud.recommender_v1beta1.proto import recommender_service_pb2_grpc


class RecommenderGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.recommender.v1beta1 Recommender API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="recommender.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "recommender_stub": recommender_service_pb2_grpc.RecommenderStub(channel)
        }

    @classmethod
    def create_channel(
        cls, address="recommender.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_insights(self):
        """Return the gRPC stub for :meth:`RecommenderClient.list_insights`.

        Lists insights for a Cloud project. Requires the recommender.*.list
        IAM permission for the specified insight type.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["recommender_stub"].ListInsights

    @property
    def get_insight(self):
        """Return the gRPC stub for :meth:`RecommenderClient.get_insight`.

        Gets the requested insight. Requires the recommender.*.get IAM
        permission for the specified insight type.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["recommender_stub"].GetInsight

    @property
    def mark_insight_accepted(self):
        """Return the gRPC stub for :meth:`RecommenderClient.mark_insight_accepted`.

        Marks the Insight State as Accepted. Users can use this method to
        indicate to the Recommender API that they have applied some action based
        on the insight. This stops the insight content from being updated.

        MarkInsightAccepted can be applied to insights in ACTIVE state. Requires
        the recommender.*.update IAM permission for the specified insight.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["recommender_stub"].MarkInsightAccepted

    @property
    def list_recommendations(self):
        """Return the gRPC stub for :meth:`RecommenderClient.list_recommendations`.

        Lists recommendations for a Cloud project. Requires the
        recommender.*.list IAM permission for the specified recommender.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["recommender_stub"].ListRecommendations

    @property
    def get_recommendation(self):
        """Return the gRPC stub for :meth:`RecommenderClient.get_recommendation`.

        Gets the requested recommendation. Requires the recommender.*.get
        IAM permission for the specified recommender.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["recommender_stub"].GetRecommendation

    @property
    def mark_recommendation_claimed(self):
        """Return the gRPC stub for :meth:`RecommenderClient.mark_recommendation_claimed`.

        Marks the Recommendation State as Claimed. Users can use this method
        to indicate to the Recommender API that they are starting to apply the
        recommendation themselves. This stops the recommendation content from
        being updated. Associated insights are frozen and placed in the ACCEPTED
        state.

        MarkRecommendationClaimed can be applied to recommendations in CLAIMED
        or ACTIVE state.

        Requires the recommender.*.update IAM permission for the specified
        recommender.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["recommender_stub"].MarkRecommendationClaimed

    @property
    def mark_recommendation_succeeded(self):
        """Return the gRPC stub for :meth:`RecommenderClient.mark_recommendation_succeeded`.

        Marks the Recommendation State as Succeeded. Users can use this
        method to indicate to the Recommender API that they have applied the
        recommendation themselves, and the operation was successful. This stops
        the recommendation content from being updated. Associated insights are
        frozen and placed in the ACCEPTED state.

        MarkRecommendationSucceeded can be applied to recommendations in ACTIVE,
        CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the specified
        recommender.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["recommender_stub"].MarkRecommendationSucceeded

    @property
    def mark_recommendation_failed(self):
        """Return the gRPC stub for :meth:`RecommenderClient.mark_recommendation_failed`.

        Marks the Recommendation State as Failed. Users can use this method
        to indicate to the Recommender API that they have applied the
        recommendation themselves, and the operation failed. This stops the
        recommendation content from being updated. Associated insights are
        frozen and placed in the ACCEPTED state.

        MarkRecommendationFailed can be applied to recommendations in ACTIVE,
        CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the specified
        recommender.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["recommender_stub"].MarkRecommendationFailed
