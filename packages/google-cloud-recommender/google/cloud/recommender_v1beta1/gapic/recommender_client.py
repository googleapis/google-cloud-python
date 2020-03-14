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

"""Accesses the google.cloud.recommender.v1beta1 Recommender API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.recommender_v1beta1.gapic import enums
from google.cloud.recommender_v1beta1.gapic import recommender_client_config
from google.cloud.recommender_v1beta1.gapic.transports import recommender_grpc_transport
from google.cloud.recommender_v1beta1.proto import insight_pb2
from google.cloud.recommender_v1beta1.proto import recommendation_pb2
from google.cloud.recommender_v1beta1.proto import recommender_service_pb2
from google.cloud.recommender_v1beta1.proto import recommender_service_pb2_grpc


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-recommender"
).version


class RecommenderClient(object):
    """
    Provides insights and recommendations for cloud customers for various
    categories like performance optimization, cost savings, reliability, feature
    discovery, etc. Insights and recommendations are generated automatically
    based on analysis of user resources, configuration and monitoring metrics.
    """

    SERVICE_ADDRESS = "recommender.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.recommender.v1beta1.Recommender"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            RecommenderClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def insight_path(cls, project, location, insight_type, insight):
        """Return a fully-qualified insight string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/insightTypes/{insight_type}/insights/{insight}",
            project=project,
            location=location,
            insight_type=insight_type,
            insight=insight,
        )

    @classmethod
    def insight_type_path(cls, project, location, insight_type):
        """Return a fully-qualified insight_type string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/insightTypes/{insight_type}",
            project=project,
            location=location,
            insight_type=insight_type,
        )

    @classmethod
    def recommendation_path(cls, project, location, recommender, recommendation):
        """Return a fully-qualified recommendation string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/recommenders/{recommender}/recommendations/{recommendation}",
            project=project,
            location=location,
            recommender=recommender,
            recommendation=recommendation,
        )

    @classmethod
    def recommender_path(cls, project, location, recommender):
        """Return a fully-qualified recommender string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/recommenders/{recommender}",
            project=project,
            location=location,
            recommender=recommender,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.RecommenderGrpcTransport,
                    Callable[[~.Credentials, type], ~.RecommenderGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = recommender_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=recommender_grpc_transport.RecommenderGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = recommender_grpc_transport.RecommenderGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def list_insights(
        self,
        parent,
        page_size=None,
        filter_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists insights for a Cloud project. Requires the recommender.*.list
        IAM permission for the specified insight type.

        Example:
            >>> from google.cloud import recommender_v1beta1
            >>>
            >>> client = recommender_v1beta1.RecommenderClient()
            >>>
            >>> parent = client.insight_type_path('[PROJECT]', '[LOCATION]', '[INSIGHT_TYPE]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_insights(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_insights(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The container resource on which to execute the request.
                Acceptable formats:

                1.

                "projects/[PROJECT_NUMBER]/locations/[LOCATION]/insightTypes/[INSIGHT_TYPE_ID]",

                LOCATION here refers to GCP Locations:
                https://cloud.google.com/about/locations/
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            filter_ (str): Optional. Filter expression to restrict the insights returned.
                Supported filter fields: state Eg: \`state:"DISMISSED" or state:"ACTIVE"
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.recommender_v1beta1.types.Insight` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_insights" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_insights"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_insights,
                default_retry=self._method_configs["ListInsights"].retry,
                default_timeout=self._method_configs["ListInsights"].timeout,
                client_info=self._client_info,
            )

        request = recommender_service_pb2.ListInsightsRequest(
            parent=parent, page_size=page_size, filter=filter_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_insights"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="insights",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_insight(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the requested insight. Requires the recommender.*.get IAM
        permission for the specified insight type.

        Example:
            >>> from google.cloud import recommender_v1beta1
            >>>
            >>> client = recommender_v1beta1.RecommenderClient()
            >>>
            >>> name = client.insight_path('[PROJECT]', '[LOCATION]', '[INSIGHT_TYPE]', '[INSIGHT]')
            >>>
            >>> response = client.get_insight(name)

        Args:
            name (str): Required. Name of the insight.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.recommender_v1beta1.types.Insight` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_insight" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_insight"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_insight,
                default_retry=self._method_configs["GetInsight"].retry,
                default_timeout=self._method_configs["GetInsight"].timeout,
                client_info=self._client_info,
            )

        request = recommender_service_pb2.GetInsightRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_insight"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def mark_insight_accepted(
        self,
        name,
        etag,
        state_metadata=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Marks the Insight State as Accepted. Users can use this method to
        indicate to the Recommender API that they have applied some action based
        on the insight. This stops the insight content from being updated.

        MarkInsightAccepted can be applied to insights in ACTIVE state. Requires
        the recommender.*.update IAM permission for the specified insight.

        Example:
            >>> from google.cloud import recommender_v1beta1
            >>>
            >>> client = recommender_v1beta1.RecommenderClient()
            >>>
            >>> name = client.insight_path('[PROJECT]', '[LOCATION]', '[INSIGHT_TYPE]', '[INSIGHT]')
            >>>
            >>> # TODO: Initialize `etag`:
            >>> etag = ''
            >>>
            >>> response = client.mark_insight_accepted(name, etag)

        Args:
            name (str): Required. Name of the insight.
            etag (str): Required. Fingerprint of the Insight. Provides optimistic locking.
            state_metadata (dict[str -> str]): Optional. State properties user wish to include with this state.
                Full replace of the current state_metadata.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.recommender_v1beta1.types.Insight` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "mark_insight_accepted" not in self._inner_api_calls:
            self._inner_api_calls[
                "mark_insight_accepted"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.mark_insight_accepted,
                default_retry=self._method_configs["MarkInsightAccepted"].retry,
                default_timeout=self._method_configs["MarkInsightAccepted"].timeout,
                client_info=self._client_info,
            )

        request = recommender_service_pb2.MarkInsightAcceptedRequest(
            name=name, etag=etag, state_metadata=state_metadata
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["mark_insight_accepted"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_recommendations(
        self,
        parent,
        page_size=None,
        filter_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists recommendations for a Cloud project. Requires the
        recommender.*.list IAM permission for the specified recommender.

        Example:
            >>> from google.cloud import recommender_v1beta1
            >>>
            >>> client = recommender_v1beta1.RecommenderClient()
            >>>
            >>> parent = client.recommender_path('[PROJECT]', '[LOCATION]', '[RECOMMENDER]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_recommendations(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_recommendations(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The container resource on which to execute the request.
                Acceptable formats:

                1.

                "projects/[PROJECT_NUMBER]/locations/[LOCATION]/recommenders/[RECOMMENDER_ID]",

                LOCATION here refers to GCP Locations:
                https://cloud.google.com/about/locations/
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            filter_ (str): Filter expression to restrict the recommendations returned.
                Supported filter fields: state_info.state Eg:
                \`state_info.state:"DISMISSED" or state_info.state:"FAILED"
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.recommender_v1beta1.types.Recommendation` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_recommendations" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_recommendations"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_recommendations,
                default_retry=self._method_configs["ListRecommendations"].retry,
                default_timeout=self._method_configs["ListRecommendations"].timeout,
                client_info=self._client_info,
            )

        request = recommender_service_pb2.ListRecommendationsRequest(
            parent=parent, page_size=page_size, filter=filter_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_recommendations"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="recommendations",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_recommendation(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the requested recommendation. Requires the recommender.*.get
        IAM permission for the specified recommender.

        Example:
            >>> from google.cloud import recommender_v1beta1
            >>>
            >>> client = recommender_v1beta1.RecommenderClient()
            >>>
            >>> name = client.recommendation_path('[PROJECT]', '[LOCATION]', '[RECOMMENDER]', '[RECOMMENDATION]')
            >>>
            >>> response = client.get_recommendation(name)

        Args:
            name (str): Required. Name of the recommendation.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.recommender_v1beta1.types.Recommendation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_recommendation" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_recommendation"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_recommendation,
                default_retry=self._method_configs["GetRecommendation"].retry,
                default_timeout=self._method_configs["GetRecommendation"].timeout,
                client_info=self._client_info,
            )

        request = recommender_service_pb2.GetRecommendationRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_recommendation"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def mark_recommendation_claimed(
        self,
        name,
        etag,
        state_metadata=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Marks the Recommendation State as Claimed. Users can use this method
        to indicate to the Recommender API that they are starting to apply the
        recommendation themselves. This stops the recommendation content from
        being updated. Associated insights are frozen and placed in the ACCEPTED
        state.

        MarkRecommendationClaimed can be applied to recommendations in CLAIMED
        or ACTIVE state.

        Requires the recommender.*.update IAM permission for the specified
        recommender.

        Example:
            >>> from google.cloud import recommender_v1beta1
            >>>
            >>> client = recommender_v1beta1.RecommenderClient()
            >>>
            >>> name = client.recommendation_path('[PROJECT]', '[LOCATION]', '[RECOMMENDER]', '[RECOMMENDATION]')
            >>>
            >>> # TODO: Initialize `etag`:
            >>> etag = ''
            >>>
            >>> response = client.mark_recommendation_claimed(name, etag)

        Args:
            name (str): Required. Name of the recommendation.
            etag (str): Required. Fingerprint of the Recommendation. Provides optimistic locking.
            state_metadata (dict[str -> str]): State properties to include with this state. Overwrites any existing
                ``state_metadata``. Keys must match the regex
                ``/^[a-z0-9][a-z0-9_.-]{0,62}$/``. Values must match the regex
                ``/^[a-zA-Z0-9_./-]{0,255}$/``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.recommender_v1beta1.types.Recommendation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "mark_recommendation_claimed" not in self._inner_api_calls:
            self._inner_api_calls[
                "mark_recommendation_claimed"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.mark_recommendation_claimed,
                default_retry=self._method_configs["MarkRecommendationClaimed"].retry,
                default_timeout=self._method_configs[
                    "MarkRecommendationClaimed"
                ].timeout,
                client_info=self._client_info,
            )

        request = recommender_service_pb2.MarkRecommendationClaimedRequest(
            name=name, etag=etag, state_metadata=state_metadata
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["mark_recommendation_claimed"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def mark_recommendation_succeeded(
        self,
        name,
        etag,
        state_metadata=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Marks the Recommendation State as Succeeded. Users can use this
        method to indicate to the Recommender API that they have applied the
        recommendation themselves, and the operation was successful. This stops
        the recommendation content from being updated. Associated insights are
        frozen and placed in the ACCEPTED state.

        MarkRecommendationSucceeded can be applied to recommendations in ACTIVE,
        CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the specified
        recommender.

        Example:
            >>> from google.cloud import recommender_v1beta1
            >>>
            >>> client = recommender_v1beta1.RecommenderClient()
            >>>
            >>> name = client.recommendation_path('[PROJECT]', '[LOCATION]', '[RECOMMENDER]', '[RECOMMENDATION]')
            >>>
            >>> # TODO: Initialize `etag`:
            >>> etag = ''
            >>>
            >>> response = client.mark_recommendation_succeeded(name, etag)

        Args:
            name (str): Required. Name of the recommendation.
            etag (str): Required. Fingerprint of the Recommendation. Provides optimistic locking.
            state_metadata (dict[str -> str]): State properties to include with this state. Overwrites any existing
                ``state_metadata``. Keys must match the regex
                ``/^[a-z0-9][a-z0-9_.-]{0,62}$/``. Values must match the regex
                ``/^[a-zA-Z0-9_./-]{0,255}$/``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.recommender_v1beta1.types.Recommendation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "mark_recommendation_succeeded" not in self._inner_api_calls:
            self._inner_api_calls[
                "mark_recommendation_succeeded"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.mark_recommendation_succeeded,
                default_retry=self._method_configs["MarkRecommendationSucceeded"].retry,
                default_timeout=self._method_configs[
                    "MarkRecommendationSucceeded"
                ].timeout,
                client_info=self._client_info,
            )

        request = recommender_service_pb2.MarkRecommendationSucceededRequest(
            name=name, etag=etag, state_metadata=state_metadata
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["mark_recommendation_succeeded"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def mark_recommendation_failed(
        self,
        name,
        etag,
        state_metadata=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Marks the Recommendation State as Failed. Users can use this method
        to indicate to the Recommender API that they have applied the
        recommendation themselves, and the operation failed. This stops the
        recommendation content from being updated. Associated insights are
        frozen and placed in the ACCEPTED state.

        MarkRecommendationFailed can be applied to recommendations in ACTIVE,
        CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the specified
        recommender.

        Example:
            >>> from google.cloud import recommender_v1beta1
            >>>
            >>> client = recommender_v1beta1.RecommenderClient()
            >>>
            >>> name = client.recommendation_path('[PROJECT]', '[LOCATION]', '[RECOMMENDER]', '[RECOMMENDATION]')
            >>>
            >>> # TODO: Initialize `etag`:
            >>> etag = ''
            >>>
            >>> response = client.mark_recommendation_failed(name, etag)

        Args:
            name (str): Required. Name of the recommendation.
            etag (str): Required. Fingerprint of the Recommendation. Provides optimistic locking.
            state_metadata (dict[str -> str]): State properties to include with this state. Overwrites any existing
                ``state_metadata``. Keys must match the regex
                ``/^[a-z0-9][a-z0-9_.-]{0,62}$/``. Values must match the regex
                ``/^[a-zA-Z0-9_./-]{0,255}$/``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.recommender_v1beta1.types.Recommendation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "mark_recommendation_failed" not in self._inner_api_calls:
            self._inner_api_calls[
                "mark_recommendation_failed"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.mark_recommendation_failed,
                default_retry=self._method_configs["MarkRecommendationFailed"].retry,
                default_timeout=self._method_configs[
                    "MarkRecommendationFailed"
                ].timeout,
                client_info=self._client_info,
            )

        request = recommender_service_pb2.MarkRecommendationFailedRequest(
            name=name, etag=etag, state_metadata=state_metadata
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["mark_recommendation_failed"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
