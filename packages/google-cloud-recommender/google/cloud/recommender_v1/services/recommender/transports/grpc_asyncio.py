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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import packaging.version

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.recommender_v1.types import insight
from google.cloud.recommender_v1.types import recommendation
from google.cloud.recommender_v1.types import recommender_service
from .base import RecommenderTransport, DEFAULT_CLIENT_INFO
from .grpc import RecommenderGrpcTransport


class RecommenderGrpcAsyncIOTransport(RecommenderTransport):
    """gRPC AsyncIO backend transport for Recommender.

    Provides insights and recommendations for cloud customers for
    various categories like performance optimization, cost savings,
    reliability, feature discovery, etc. Insights and
    recommendations are generated automatically based on analysis of
    user resources, configuration and monitoring metrics.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "recommender.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "recommender.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def list_insights(
        self,
    ) -> Callable[
        [recommender_service.ListInsightsRequest],
        Awaitable[recommender_service.ListInsightsResponse],
    ]:
        r"""Return a callable for the list insights method over gRPC.

        Lists insights for a Cloud project. Requires the
        recommender.*.list IAM permission for the specified insight
        type.

        Returns:
            Callable[[~.ListInsightsRequest],
                    Awaitable[~.ListInsightsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_insights" not in self._stubs:
            self._stubs["list_insights"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1.Recommender/ListInsights",
                request_serializer=recommender_service.ListInsightsRequest.serialize,
                response_deserializer=recommender_service.ListInsightsResponse.deserialize,
            )
        return self._stubs["list_insights"]

    @property
    def get_insight(
        self,
    ) -> Callable[[recommender_service.GetInsightRequest], Awaitable[insight.Insight]]:
        r"""Return a callable for the get insight method over gRPC.

        Gets the requested insight. Requires the recommender.*.get IAM
        permission for the specified insight type.

        Returns:
            Callable[[~.GetInsightRequest],
                    Awaitable[~.Insight]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_insight" not in self._stubs:
            self._stubs["get_insight"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1.Recommender/GetInsight",
                request_serializer=recommender_service.GetInsightRequest.serialize,
                response_deserializer=insight.Insight.deserialize,
            )
        return self._stubs["get_insight"]

    @property
    def mark_insight_accepted(
        self,
    ) -> Callable[
        [recommender_service.MarkInsightAcceptedRequest], Awaitable[insight.Insight]
    ]:
        r"""Return a callable for the mark insight accepted method over gRPC.

        Marks the Insight State as Accepted. Users can use this method
        to indicate to the Recommender API that they have applied some
        action based on the insight. This stops the insight content from
        being updated.

        MarkInsightAccepted can be applied to insights in ACTIVE state.
        Requires the recommender.*.update IAM permission for the
        specified insight.

        Returns:
            Callable[[~.MarkInsightAcceptedRequest],
                    Awaitable[~.Insight]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mark_insight_accepted" not in self._stubs:
            self._stubs["mark_insight_accepted"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1.Recommender/MarkInsightAccepted",
                request_serializer=recommender_service.MarkInsightAcceptedRequest.serialize,
                response_deserializer=insight.Insight.deserialize,
            )
        return self._stubs["mark_insight_accepted"]

    @property
    def list_recommendations(
        self,
    ) -> Callable[
        [recommender_service.ListRecommendationsRequest],
        Awaitable[recommender_service.ListRecommendationsResponse],
    ]:
        r"""Return a callable for the list recommendations method over gRPC.

        Lists recommendations for a Cloud project. Requires the
        recommender.*.list IAM permission for the specified recommender.

        Returns:
            Callable[[~.ListRecommendationsRequest],
                    Awaitable[~.ListRecommendationsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_recommendations" not in self._stubs:
            self._stubs["list_recommendations"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1.Recommender/ListRecommendations",
                request_serializer=recommender_service.ListRecommendationsRequest.serialize,
                response_deserializer=recommender_service.ListRecommendationsResponse.deserialize,
            )
        return self._stubs["list_recommendations"]

    @property
    def get_recommendation(
        self,
    ) -> Callable[
        [recommender_service.GetRecommendationRequest],
        Awaitable[recommendation.Recommendation],
    ]:
        r"""Return a callable for the get recommendation method over gRPC.

        Gets the requested recommendation. Requires the
        recommender.*.get IAM permission for the specified recommender.

        Returns:
            Callable[[~.GetRecommendationRequest],
                    Awaitable[~.Recommendation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_recommendation" not in self._stubs:
            self._stubs["get_recommendation"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1.Recommender/GetRecommendation",
                request_serializer=recommender_service.GetRecommendationRequest.serialize,
                response_deserializer=recommendation.Recommendation.deserialize,
            )
        return self._stubs["get_recommendation"]

    @property
    def mark_recommendation_claimed(
        self,
    ) -> Callable[
        [recommender_service.MarkRecommendationClaimedRequest],
        Awaitable[recommendation.Recommendation],
    ]:
        r"""Return a callable for the mark recommendation claimed method over gRPC.

        Marks the Recommendation State as Claimed. Users can use this
        method to indicate to the Recommender API that they are starting
        to apply the recommendation themselves. This stops the
        recommendation content from being updated. Associated insights
        are frozen and placed in the ACCEPTED state.

        MarkRecommendationClaimed can be applied to recommendations in
        CLAIMED, SUCCEEDED, FAILED, or ACTIVE state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Returns:
            Callable[[~.MarkRecommendationClaimedRequest],
                    Awaitable[~.Recommendation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mark_recommendation_claimed" not in self._stubs:
            self._stubs["mark_recommendation_claimed"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1.Recommender/MarkRecommendationClaimed",
                request_serializer=recommender_service.MarkRecommendationClaimedRequest.serialize,
                response_deserializer=recommendation.Recommendation.deserialize,
            )
        return self._stubs["mark_recommendation_claimed"]

    @property
    def mark_recommendation_succeeded(
        self,
    ) -> Callable[
        [recommender_service.MarkRecommendationSucceededRequest],
        Awaitable[recommendation.Recommendation],
    ]:
        r"""Return a callable for the mark recommendation succeeded method over gRPC.

        Marks the Recommendation State as Succeeded. Users can use this
        method to indicate to the Recommender API that they have applied
        the recommendation themselves, and the operation was successful.
        This stops the recommendation content from being updated.
        Associated insights are frozen and placed in the ACCEPTED state.

        MarkRecommendationSucceeded can be applied to recommendations in
        ACTIVE, CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Returns:
            Callable[[~.MarkRecommendationSucceededRequest],
                    Awaitable[~.Recommendation]]:
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
                "/google.cloud.recommender.v1.Recommender/MarkRecommendationSucceeded",
                request_serializer=recommender_service.MarkRecommendationSucceededRequest.serialize,
                response_deserializer=recommendation.Recommendation.deserialize,
            )
        return self._stubs["mark_recommendation_succeeded"]

    @property
    def mark_recommendation_failed(
        self,
    ) -> Callable[
        [recommender_service.MarkRecommendationFailedRequest],
        Awaitable[recommendation.Recommendation],
    ]:
        r"""Return a callable for the mark recommendation failed method over gRPC.

        Marks the Recommendation State as Failed. Users can use this
        method to indicate to the Recommender API that they have applied
        the recommendation themselves, and the operation failed. This
        stops the recommendation content from being updated. Associated
        insights are frozen and placed in the ACCEPTED state.

        MarkRecommendationFailed can be applied to recommendations in
        ACTIVE, CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Returns:
            Callable[[~.MarkRecommendationFailedRequest],
                    Awaitable[~.Recommendation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mark_recommendation_failed" not in self._stubs:
            self._stubs["mark_recommendation_failed"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommender.v1.Recommender/MarkRecommendationFailed",
                request_serializer=recommender_service.MarkRecommendationFailedRequest.serialize,
                response_deserializer=recommendation.Recommendation.deserialize,
            )
        return self._stubs["mark_recommendation_failed"]


__all__ = ("RecommenderGrpcAsyncIOTransport",)
