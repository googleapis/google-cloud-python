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
from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.recommender_v1.services.recommender import pagers
from google.cloud.recommender_v1.types import insight
from google.cloud.recommender_v1.types import recommendation
from google.cloud.recommender_v1.types import recommender_service
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import RecommenderTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import RecommenderGrpcAsyncIOTransport
from .client import RecommenderClient


class RecommenderAsyncClient:
    """Provides insights and recommendations for cloud customers for
    various categories like performance optimization, cost savings,
    reliability, feature discovery, etc. Insights and
    recommendations are generated automatically based on analysis of
    user resources, configuration and monitoring metrics.
    """

    _client: RecommenderClient

    DEFAULT_ENDPOINT = RecommenderClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = RecommenderClient.DEFAULT_MTLS_ENDPOINT

    insight_path = staticmethod(RecommenderClient.insight_path)
    parse_insight_path = staticmethod(RecommenderClient.parse_insight_path)
    insight_type_path = staticmethod(RecommenderClient.insight_type_path)
    parse_insight_type_path = staticmethod(RecommenderClient.parse_insight_type_path)
    recommendation_path = staticmethod(RecommenderClient.recommendation_path)
    parse_recommendation_path = staticmethod(
        RecommenderClient.parse_recommendation_path
    )
    recommender_path = staticmethod(RecommenderClient.recommender_path)
    parse_recommender_path = staticmethod(RecommenderClient.parse_recommender_path)
    common_billing_account_path = staticmethod(
        RecommenderClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        RecommenderClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(RecommenderClient.common_folder_path)
    parse_common_folder_path = staticmethod(RecommenderClient.parse_common_folder_path)
    common_organization_path = staticmethod(RecommenderClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        RecommenderClient.parse_common_organization_path
    )
    common_project_path = staticmethod(RecommenderClient.common_project_path)
    parse_common_project_path = staticmethod(
        RecommenderClient.parse_common_project_path
    )
    common_location_path = staticmethod(RecommenderClient.common_location_path)
    parse_common_location_path = staticmethod(
        RecommenderClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            RecommenderAsyncClient: The constructed client.
        """
        return RecommenderClient.from_service_account_info.__func__(RecommenderAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            RecommenderAsyncClient: The constructed client.
        """
        return RecommenderClient.from_service_account_file.__func__(RecommenderAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> RecommenderTransport:
        """Returns the transport used by the client instance.

        Returns:
            RecommenderTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(RecommenderClient).get_transport_class, type(RecommenderClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, RecommenderTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the recommender client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.RecommenderTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = RecommenderClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_insights(
        self,
        request: recommender_service.ListInsightsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInsightsAsyncPager:
        r"""Lists insights for a Cloud project. Requires the
        recommender.*.list IAM permission for the specified insight
        type.

        Args:
            request (:class:`google.cloud.recommender_v1.types.ListInsightsRequest`):
                The request object. Request for the `ListInsights`
                method.
            parent (:class:`str`):
                Required. The container resource on which to execute the
                request. Acceptable formats:

                1.

                "projects/[PROJECT_NUMBER]/locations/[LOCATION]/insightTypes/[INSIGHT_TYPE_ID]",

                LOCATION here refers to GCP Locations:
                https://cloud.google.com/about/locations/
                INSIGHT_TYPE_ID refers to supported insight types:
                https://cloud.google.com/recommender/docs/insights/insight-types.)

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.services.recommender.pagers.ListInsightsAsyncPager:
                Response to the ListInsights method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recommender_service.ListInsightsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_insights,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListInsightsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_insight(
        self,
        request: recommender_service.GetInsightRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> insight.Insight:
        r"""Gets the requested insight. Requires the recommender.*.get IAM
        permission for the specified insight type.

        Args:
            request (:class:`google.cloud.recommender_v1.types.GetInsightRequest`):
                The request object. Request to the `GetInsight` method.
            name (:class:`str`):
                Required. Name of the insight.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Insight:
                An insight along with the information
                used to derive the insight. The insight
                may have associated recomendations as
                well.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recommender_service.GetInsightRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_insight,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def mark_insight_accepted(
        self,
        request: recommender_service.MarkInsightAcceptedRequest = None,
        *,
        name: str = None,
        state_metadata: Sequence[
            recommender_service.MarkInsightAcceptedRequest.StateMetadataEntry
        ] = None,
        etag: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> insight.Insight:
        r"""Marks the Insight State as Accepted. Users can use this method
        to indicate to the Recommender API that they have applied some
        action based on the insight. This stops the insight content from
        being updated.

        MarkInsightAccepted can be applied to insights in ACTIVE state.
        Requires the recommender.*.update IAM permission for the
        specified insight.

        Args:
            request (:class:`google.cloud.recommender_v1.types.MarkInsightAcceptedRequest`):
                The request object. Request for the
                `MarkInsightAccepted` method.
            name (:class:`str`):
                Required. Name of the insight.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            state_metadata (:class:`Sequence[google.cloud.recommender_v1.types.MarkInsightAcceptedRequest.StateMetadataEntry]`):
                Optional. State properties user wish to include with
                this state. Full replace of the current state_metadata.

                This corresponds to the ``state_metadata`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            etag (:class:`str`):
                Required. Fingerprint of the Insight.
                Provides optimistic locking.

                This corresponds to the ``etag`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Insight:
                An insight along with the information
                used to derive the insight. The insight
                may have associated recomendations as
                well.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, state_metadata, etag])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recommender_service.MarkInsightAcceptedRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if etag is not None:
            request.etag = etag

        if state_metadata:
            request.state_metadata.update(state_metadata)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.mark_insight_accepted,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_recommendations(
        self,
        request: recommender_service.ListRecommendationsRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRecommendationsAsyncPager:
        r"""Lists recommendations for a Cloud project. Requires the
        recommender.*.list IAM permission for the specified recommender.

        Args:
            request (:class:`google.cloud.recommender_v1.types.ListRecommendationsRequest`):
                The request object. Request for the
                `ListRecommendations` method.
            parent (:class:`str`):
                Required. The container resource on which to execute the
                request. Acceptable formats:

                1.

                "projects/[PROJECT_NUMBER]/locations/[LOCATION]/recommenders/[RECOMMENDER_ID]",

                LOCATION here refers to GCP Locations:
                https://cloud.google.com/about/locations/ RECOMMENDER_ID
                refers to supported recommenders:
                https://cloud.google.com/recommender/docs/recommenders.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
                Filter expression to restrict the recommendations
                returned. Supported filter fields: state_info.state Eg:
                \`state_info.state:"DISMISSED" or
                state_info.state:"FAILED"

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.services.recommender.pagers.ListRecommendationsAsyncPager:
                Response to the ListRecommendations method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recommender_service.ListRecommendationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if filter is not None:
            request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_recommendations,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListRecommendationsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_recommendation(
        self,
        request: recommender_service.GetRecommendationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation.Recommendation:
        r"""Gets the requested recommendation. Requires the
        recommender.*.get IAM permission for the specified recommender.

        Args:
            request (:class:`google.cloud.recommender_v1.types.GetRecommendationRequest`):
                The request object. Request to the `GetRecommendation`
                method.
            name (:class:`str`):
                Required. Name of the recommendation.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recommender_service.GetRecommendationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_recommendation,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def mark_recommendation_claimed(
        self,
        request: recommender_service.MarkRecommendationClaimedRequest = None,
        *,
        name: str = None,
        state_metadata: Sequence[
            recommender_service.MarkRecommendationClaimedRequest.StateMetadataEntry
        ] = None,
        etag: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation.Recommendation:
        r"""Marks the Recommendation State as Claimed. Users can use this
        method to indicate to the Recommender API that they are starting
        to apply the recommendation themselves. This stops the
        recommendation content from being updated. Associated insights
        are frozen and placed in the ACCEPTED state.

        MarkRecommendationClaimed can be applied to recommendations in
        CLAIMED, SUCCEEDED, FAILED, or ACTIVE state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Args:
            request (:class:`google.cloud.recommender_v1.types.MarkRecommendationClaimedRequest`):
                The request object. Request for the
                `MarkRecommendationClaimed` Method.
            name (:class:`str`):
                Required. Name of the recommendation.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            state_metadata (:class:`Sequence[google.cloud.recommender_v1.types.MarkRecommendationClaimedRequest.StateMetadataEntry]`):
                State properties to include with this state. Overwrites
                any existing ``state_metadata``. Keys must match the
                regex ``/^[a-z0-9][a-z0-9_.-]{0,62}$/``. Values must match
                the regex ``/^[a-zA-Z0-9_./-]{0,255}$/``.

                This corresponds to the ``state_metadata`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            etag (:class:`str`):
                Required. Fingerprint of the
                Recommendation. Provides optimistic
                locking.

                This corresponds to the ``etag`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, state_metadata, etag])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recommender_service.MarkRecommendationClaimedRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if etag is not None:
            request.etag = etag

        if state_metadata:
            request.state_metadata.update(state_metadata)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.mark_recommendation_claimed,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def mark_recommendation_succeeded(
        self,
        request: recommender_service.MarkRecommendationSucceededRequest = None,
        *,
        name: str = None,
        state_metadata: Sequence[
            recommender_service.MarkRecommendationSucceededRequest.StateMetadataEntry
        ] = None,
        etag: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation.Recommendation:
        r"""Marks the Recommendation State as Succeeded. Users can use this
        method to indicate to the Recommender API that they have applied
        the recommendation themselves, and the operation was successful.
        This stops the recommendation content from being updated.
        Associated insights are frozen and placed in the ACCEPTED state.

        MarkRecommendationSucceeded can be applied to recommendations in
        ACTIVE, CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Args:
            request (:class:`google.cloud.recommender_v1.types.MarkRecommendationSucceededRequest`):
                The request object. Request for the
                `MarkRecommendationSucceeded` Method.
            name (:class:`str`):
                Required. Name of the recommendation.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            state_metadata (:class:`Sequence[google.cloud.recommender_v1.types.MarkRecommendationSucceededRequest.StateMetadataEntry]`):
                State properties to include with this state. Overwrites
                any existing ``state_metadata``. Keys must match the
                regex ``/^[a-z0-9][a-z0-9_.-]{0,62}$/``. Values must match
                the regex ``/^[a-zA-Z0-9_./-]{0,255}$/``.

                This corresponds to the ``state_metadata`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            etag (:class:`str`):
                Required. Fingerprint of the
                Recommendation. Provides optimistic
                locking.

                This corresponds to the ``etag`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, state_metadata, etag])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recommender_service.MarkRecommendationSucceededRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if etag is not None:
            request.etag = etag

        if state_metadata:
            request.state_metadata.update(state_metadata)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.mark_recommendation_succeeded,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def mark_recommendation_failed(
        self,
        request: recommender_service.MarkRecommendationFailedRequest = None,
        *,
        name: str = None,
        state_metadata: Sequence[
            recommender_service.MarkRecommendationFailedRequest.StateMetadataEntry
        ] = None,
        etag: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation.Recommendation:
        r"""Marks the Recommendation State as Failed. Users can use this
        method to indicate to the Recommender API that they have applied
        the recommendation themselves, and the operation failed. This
        stops the recommendation content from being updated. Associated
        insights are frozen and placed in the ACCEPTED state.

        MarkRecommendationFailed can be applied to recommendations in
        ACTIVE, CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Args:
            request (:class:`google.cloud.recommender_v1.types.MarkRecommendationFailedRequest`):
                The request object. Request for the
                `MarkRecommendationFailed` Method.
            name (:class:`str`):
                Required. Name of the recommendation.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            state_metadata (:class:`Sequence[google.cloud.recommender_v1.types.MarkRecommendationFailedRequest.StateMetadataEntry]`):
                State properties to include with this state. Overwrites
                any existing ``state_metadata``. Keys must match the
                regex ``/^[a-z0-9][a-z0-9_.-]{0,62}$/``. Values must match
                the regex ``/^[a-zA-Z0-9_./-]{0,255}$/``.

                This corresponds to the ``state_metadata`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            etag (:class:`str`):
                Required. Fingerprint of the
                Recommendation. Provides optimistic
                locking.

                This corresponds to the ``etag`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, state_metadata, etag])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recommender_service.MarkRecommendationFailedRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if etag is not None:
            request.etag = etag

        if state_metadata:
            request.state_metadata.update(state_metadata)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.mark_recommendation_failed,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-recommender",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("RecommenderAsyncClient",)
