# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.cloud.recommender_v1beta1.types import (
    insight_type_config as gcr_insight_type_config,
)
from google.cloud.recommender_v1beta1.types import (
    recommender_config as gcr_recommender_config,
)
from google.cloud.recommender_v1beta1.types import insight
from google.cloud.recommender_v1beta1.types import insight_type_config
from google.cloud.recommender_v1beta1.types import recommendation
from google.cloud.recommender_v1beta1.types import recommender_config
from google.cloud.recommender_v1beta1.types import recommender_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import RecommenderTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class RecommenderRestInterceptor:
    """Interceptor for Recommender.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RecommenderRestTransport.

    .. code-block:: python
        class MyCustomRecommenderInterceptor(RecommenderRestInterceptor):
            def pre_get_insight(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_insight(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_insight_type_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_insight_type_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_recommendation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_recommendation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_recommender_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_recommender_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_insights(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_insights(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_insight_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_insight_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_recommendations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_recommendations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_recommenders(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_recommenders(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_mark_insight_accepted(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_mark_insight_accepted(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_mark_recommendation_claimed(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_mark_recommendation_claimed(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_mark_recommendation_failed(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_mark_recommendation_failed(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_mark_recommendation_succeeded(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_mark_recommendation_succeeded(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_insight_type_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_insight_type_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_recommender_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_recommender_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RecommenderRestTransport(interceptor=MyCustomRecommenderInterceptor())
        client = RecommenderClient(transport=transport)


    """

    def pre_get_insight(
        self,
        request: recommender_service.GetInsightRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[recommender_service.GetInsightRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_insight

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_get_insight(self, response: insight.Insight) -> insight.Insight:
        """Post-rpc interceptor for get_insight

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_get_insight_type_config(
        self,
        request: recommender_service.GetInsightTypeConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        recommender_service.GetInsightTypeConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_insight_type_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_get_insight_type_config(
        self, response: insight_type_config.InsightTypeConfig
    ) -> insight_type_config.InsightTypeConfig:
        """Post-rpc interceptor for get_insight_type_config

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_get_recommendation(
        self,
        request: recommender_service.GetRecommendationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[recommender_service.GetRecommendationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_recommendation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_get_recommendation(
        self, response: recommendation.Recommendation
    ) -> recommendation.Recommendation:
        """Post-rpc interceptor for get_recommendation

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_get_recommender_config(
        self,
        request: recommender_service.GetRecommenderConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        recommender_service.GetRecommenderConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_recommender_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_get_recommender_config(
        self, response: recommender_config.RecommenderConfig
    ) -> recommender_config.RecommenderConfig:
        """Post-rpc interceptor for get_recommender_config

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_list_insights(
        self,
        request: recommender_service.ListInsightsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[recommender_service.ListInsightsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_insights

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_list_insights(
        self, response: recommender_service.ListInsightsResponse
    ) -> recommender_service.ListInsightsResponse:
        """Post-rpc interceptor for list_insights

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_list_insight_types(
        self,
        request: recommender_service.ListInsightTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[recommender_service.ListInsightTypesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_insight_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_list_insight_types(
        self, response: recommender_service.ListInsightTypesResponse
    ) -> recommender_service.ListInsightTypesResponse:
        """Post-rpc interceptor for list_insight_types

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_list_recommendations(
        self,
        request: recommender_service.ListRecommendationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        recommender_service.ListRecommendationsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_recommendations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_list_recommendations(
        self, response: recommender_service.ListRecommendationsResponse
    ) -> recommender_service.ListRecommendationsResponse:
        """Post-rpc interceptor for list_recommendations

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_list_recommenders(
        self,
        request: recommender_service.ListRecommendersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[recommender_service.ListRecommendersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_recommenders

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_list_recommenders(
        self, response: recommender_service.ListRecommendersResponse
    ) -> recommender_service.ListRecommendersResponse:
        """Post-rpc interceptor for list_recommenders

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_mark_insight_accepted(
        self,
        request: recommender_service.MarkInsightAcceptedRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        recommender_service.MarkInsightAcceptedRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for mark_insight_accepted

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_mark_insight_accepted(self, response: insight.Insight) -> insight.Insight:
        """Post-rpc interceptor for mark_insight_accepted

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_mark_recommendation_claimed(
        self,
        request: recommender_service.MarkRecommendationClaimedRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        recommender_service.MarkRecommendationClaimedRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for mark_recommendation_claimed

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_mark_recommendation_claimed(
        self, response: recommendation.Recommendation
    ) -> recommendation.Recommendation:
        """Post-rpc interceptor for mark_recommendation_claimed

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_mark_recommendation_failed(
        self,
        request: recommender_service.MarkRecommendationFailedRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        recommender_service.MarkRecommendationFailedRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for mark_recommendation_failed

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_mark_recommendation_failed(
        self, response: recommendation.Recommendation
    ) -> recommendation.Recommendation:
        """Post-rpc interceptor for mark_recommendation_failed

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_mark_recommendation_succeeded(
        self,
        request: recommender_service.MarkRecommendationSucceededRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        recommender_service.MarkRecommendationSucceededRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for mark_recommendation_succeeded

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_mark_recommendation_succeeded(
        self, response: recommendation.Recommendation
    ) -> recommendation.Recommendation:
        """Post-rpc interceptor for mark_recommendation_succeeded

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_update_insight_type_config(
        self,
        request: recommender_service.UpdateInsightTypeConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        recommender_service.UpdateInsightTypeConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_insight_type_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_update_insight_type_config(
        self, response: gcr_insight_type_config.InsightTypeConfig
    ) -> gcr_insight_type_config.InsightTypeConfig:
        """Post-rpc interceptor for update_insight_type_config

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response

    def pre_update_recommender_config(
        self,
        request: recommender_service.UpdateRecommenderConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        recommender_service.UpdateRecommenderConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_recommender_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Recommender server.
        """
        return request, metadata

    def post_update_recommender_config(
        self, response: gcr_recommender_config.RecommenderConfig
    ) -> gcr_recommender_config.RecommenderConfig:
        """Post-rpc interceptor for update_recommender_config

        Override in a subclass to manipulate the response
        after it is returned by the Recommender server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RecommenderRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RecommenderRestInterceptor


class RecommenderRestTransport(RecommenderTransport):
    """REST backend transport for Recommender.

    Provides insights and recommendations for cloud customers for
    various categories like performance optimization, cost savings,
    reliability, feature discovery, etc. Insights and
    recommendations are generated automatically based on analysis of
    user resources, configuration and monitoring metrics.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "recommender.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RecommenderRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'recommender.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or RecommenderRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetInsight(RecommenderRestStub):
        def __hash__(self):
            return hash("GetInsight")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.GetInsightRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> insight.Insight:
            r"""Call the get insight method over HTTP.

            Args:
                request (~.recommender_service.GetInsightRequest):
                    The request object. Request to the ``GetInsight`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.insight.Insight:
                    An insight along with the information
                used to derive the insight. The insight
                may have associated recommendations as
                well.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/insightTypes/*/insights/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=billingAccounts/*/locations/*/insightTypes/*/insights/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=folders/*/locations/*/insightTypes/*/insights/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=organizations/*/locations/*/insightTypes/*/insights/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_insight(request, metadata)
            pb_request = recommender_service.GetInsightRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = insight.Insight()
            pb_resp = insight.Insight.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_insight(resp)
            return resp

    class _GetInsightTypeConfig(RecommenderRestStub):
        def __hash__(self):
            return hash("GetInsightTypeConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.GetInsightTypeConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> insight_type_config.InsightTypeConfig:
            r"""Call the get insight type config method over HTTP.

            Args:
                request (~.recommender_service.GetInsightTypeConfigRequest):
                    The request object. Request for the GetInsightTypeConfig\` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.insight_type_config.InsightTypeConfig:
                    Configuration for an InsightType.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/insightTypes/*/config}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=organizations/*/locations/*/insightTypes/*/config}",
                },
            ]
            request, metadata = self._interceptor.pre_get_insight_type_config(
                request, metadata
            )
            pb_request = recommender_service.GetInsightTypeConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = insight_type_config.InsightTypeConfig()
            pb_resp = insight_type_config.InsightTypeConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_insight_type_config(resp)
            return resp

    class _GetRecommendation(RecommenderRestStub):
        def __hash__(self):
            return hash("GetRecommendation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.GetRecommendationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> recommendation.Recommendation:
            r"""Call the get recommendation method over HTTP.

            Args:
                request (~.recommender_service.GetRecommendationRequest):
                    The request object. Request to the ``GetRecommendation`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.recommendation.Recommendation:
                    A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/recommenders/*/recommendations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=billingAccounts/*/locations/*/recommenders/*/recommendations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=folders/*/locations/*/recommenders/*/recommendations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=organizations/*/locations/*/recommenders/*/recommendations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_recommendation(
                request, metadata
            )
            pb_request = recommender_service.GetRecommendationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = recommendation.Recommendation()
            pb_resp = recommendation.Recommendation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_recommendation(resp)
            return resp

    class _GetRecommenderConfig(RecommenderRestStub):
        def __hash__(self):
            return hash("GetRecommenderConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.GetRecommenderConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> recommender_config.RecommenderConfig:
            r"""Call the get recommender config method over HTTP.

            Args:
                request (~.recommender_service.GetRecommenderConfigRequest):
                    The request object. Request for the GetRecommenderConfig\` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.recommender_config.RecommenderConfig:
                    Configuration for a Recommender.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/recommenders/*/config}",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=organizations/*/locations/*/recommenders/*/config}",
                },
            ]
            request, metadata = self._interceptor.pre_get_recommender_config(
                request, metadata
            )
            pb_request = recommender_service.GetRecommenderConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = recommender_config.RecommenderConfig()
            pb_resp = recommender_config.RecommenderConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_recommender_config(resp)
            return resp

    class _ListInsights(RecommenderRestStub):
        def __hash__(self):
            return hash("ListInsights")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.ListInsightsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> recommender_service.ListInsightsResponse:
            r"""Call the list insights method over HTTP.

            Args:
                request (~.recommender_service.ListInsightsRequest):
                    The request object. Request for the ``ListInsights`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.recommender_service.ListInsightsResponse:
                    Response to the ``ListInsights`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=projects/*/locations/*/insightTypes/*}/insights",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=billingAccounts/*/locations/*/insightTypes/*}/insights",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=folders/*/locations/*/insightTypes/*}/insights",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=organizations/*/locations/*/insightTypes/*}/insights",
                },
            ]
            request, metadata = self._interceptor.pre_list_insights(request, metadata)
            pb_request = recommender_service.ListInsightsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = recommender_service.ListInsightsResponse()
            pb_resp = recommender_service.ListInsightsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_insights(resp)
            return resp

    class _ListInsightTypes(RecommenderRestStub):
        def __hash__(self):
            return hash("ListInsightTypes")

        def __call__(
            self,
            request: recommender_service.ListInsightTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> recommender_service.ListInsightTypesResponse:
            r"""Call the list insight types method over HTTP.

            Args:
                request (~.recommender_service.ListInsightTypesRequest):
                    The request object. Request for the ``ListInsightTypes`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.recommender_service.ListInsightTypesResponse:
                    Response for the ``ListInsightTypes`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/insightTypes",
                },
            ]
            request, metadata = self._interceptor.pre_list_insight_types(
                request, metadata
            )
            pb_request = recommender_service.ListInsightTypesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = recommender_service.ListInsightTypesResponse()
            pb_resp = recommender_service.ListInsightTypesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_insight_types(resp)
            return resp

    class _ListRecommendations(RecommenderRestStub):
        def __hash__(self):
            return hash("ListRecommendations")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.ListRecommendationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> recommender_service.ListRecommendationsResponse:
            r"""Call the list recommendations method over HTTP.

            Args:
                request (~.recommender_service.ListRecommendationsRequest):
                    The request object. Request for the ``ListRecommendations`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.recommender_service.ListRecommendationsResponse:
                    Response to the ``ListRecommendations`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=projects/*/locations/*/recommenders/*}/recommendations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=billingAccounts/*/locations/*/recommenders/*}/recommendations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=folders/*/locations/*/recommenders/*}/recommendations",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=organizations/*/locations/*/recommenders/*}/recommendations",
                },
            ]
            request, metadata = self._interceptor.pre_list_recommendations(
                request, metadata
            )
            pb_request = recommender_service.ListRecommendationsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = recommender_service.ListRecommendationsResponse()
            pb_resp = recommender_service.ListRecommendationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_recommendations(resp)
            return resp

    class _ListRecommenders(RecommenderRestStub):
        def __hash__(self):
            return hash("ListRecommenders")

        def __call__(
            self,
            request: recommender_service.ListRecommendersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> recommender_service.ListRecommendersResponse:
            r"""Call the list recommenders method over HTTP.

            Args:
                request (~.recommender_service.ListRecommendersRequest):
                    The request object. Request for the ``ListRecommender`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.recommender_service.ListRecommendersResponse:
                    Response for the ``ListRecommender`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/recommenders",
                },
            ]
            request, metadata = self._interceptor.pre_list_recommenders(
                request, metadata
            )
            pb_request = recommender_service.ListRecommendersRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = recommender_service.ListRecommendersResponse()
            pb_resp = recommender_service.ListRecommendersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_recommenders(resp)
            return resp

    class _MarkInsightAccepted(RecommenderRestStub):
        def __hash__(self):
            return hash("MarkInsightAccepted")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.MarkInsightAcceptedRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> insight.Insight:
            r"""Call the mark insight accepted method over HTTP.

            Args:
                request (~.recommender_service.MarkInsightAcceptedRequest):
                    The request object. Request for the ``MarkInsightAccepted`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.insight.Insight:
                    An insight along with the information
                used to derive the insight. The insight
                may have associated recommendations as
                well.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=projects/*/locations/*/insightTypes/*/insights/*}:markAccepted",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=billingAccounts/*/locations/*/insightTypes/*/insights/*}:markAccepted",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=folders/*/locations/*/insightTypes/*/insights/*}:markAccepted",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=organizations/*/locations/*/insightTypes/*/insights/*}:markAccepted",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_mark_insight_accepted(
                request, metadata
            )
            pb_request = recommender_service.MarkInsightAcceptedRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = insight.Insight()
            pb_resp = insight.Insight.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_mark_insight_accepted(resp)
            return resp

    class _MarkRecommendationClaimed(RecommenderRestStub):
        def __hash__(self):
            return hash("MarkRecommendationClaimed")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.MarkRecommendationClaimedRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> recommendation.Recommendation:
            r"""Call the mark recommendation
            claimed method over HTTP.

                Args:
                    request (~.recommender_service.MarkRecommendationClaimedRequest):
                        The request object. Request for the ``MarkRecommendationClaimed`` Method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.recommendation.Recommendation:
                        A recommendation along with a
                    suggested action. E.g., a rightsizing
                    recommendation for an underutilized VM,
                    IAM role recommendations, etc

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=projects/*/locations/*/recommenders/*/recommendations/*}:markClaimed",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=billingAccounts/*/locations/*/recommenders/*/recommendations/*}:markClaimed",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=folders/*/locations/*/recommenders/*/recommendations/*}:markClaimed",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=organizations/*/locations/*/recommenders/*/recommendations/*}:markClaimed",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_mark_recommendation_claimed(
                request, metadata
            )
            pb_request = recommender_service.MarkRecommendationClaimedRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = recommendation.Recommendation()
            pb_resp = recommendation.Recommendation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_mark_recommendation_claimed(resp)
            return resp

    class _MarkRecommendationFailed(RecommenderRestStub):
        def __hash__(self):
            return hash("MarkRecommendationFailed")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.MarkRecommendationFailedRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> recommendation.Recommendation:
            r"""Call the mark recommendation
            failed method over HTTP.

                Args:
                    request (~.recommender_service.MarkRecommendationFailedRequest):
                        The request object. Request for the ``MarkRecommendationFailed`` Method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.recommendation.Recommendation:
                        A recommendation along with a
                    suggested action. E.g., a rightsizing
                    recommendation for an underutilized VM,
                    IAM role recommendations, etc

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=projects/*/locations/*/recommenders/*/recommendations/*}:markFailed",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=billingAccounts/*/locations/*/recommenders/*/recommendations/*}:markFailed",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=folders/*/locations/*/recommenders/*/recommendations/*}:markFailed",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=organizations/*/locations/*/recommenders/*/recommendations/*}:markFailed",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_mark_recommendation_failed(
                request, metadata
            )
            pb_request = recommender_service.MarkRecommendationFailedRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = recommendation.Recommendation()
            pb_resp = recommendation.Recommendation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_mark_recommendation_failed(resp)
            return resp

    class _MarkRecommendationSucceeded(RecommenderRestStub):
        def __hash__(self):
            return hash("MarkRecommendationSucceeded")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.MarkRecommendationSucceededRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> recommendation.Recommendation:
            r"""Call the mark recommendation
            succeeded method over HTTP.

                Args:
                    request (~.recommender_service.MarkRecommendationSucceededRequest):
                        The request object. Request for the ``MarkRecommendationSucceeded`` Method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.recommendation.Recommendation:
                        A recommendation along with a
                    suggested action. E.g., a rightsizing
                    recommendation for an underutilized VM,
                    IAM role recommendations, etc

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=projects/*/locations/*/recommenders/*/recommendations/*}:markSucceeded",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=billingAccounts/*/locations/*/recommenders/*/recommendations/*}:markSucceeded",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=folders/*/locations/*/recommenders/*/recommendations/*}:markSucceeded",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=organizations/*/locations/*/recommenders/*/recommendations/*}:markSucceeded",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_mark_recommendation_succeeded(
                request, metadata
            )
            pb_request = recommender_service.MarkRecommendationSucceededRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = recommendation.Recommendation()
            pb_resp = recommendation.Recommendation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_mark_recommendation_succeeded(resp)
            return resp

    class _UpdateInsightTypeConfig(RecommenderRestStub):
        def __hash__(self):
            return hash("UpdateInsightTypeConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.UpdateInsightTypeConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcr_insight_type_config.InsightTypeConfig:
            r"""Call the update insight type
            config method over HTTP.

                Args:
                    request (~.recommender_service.UpdateInsightTypeConfigRequest):
                        The request object. Request for the ``UpdateInsightTypeConfig`` method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcr_insight_type_config.InsightTypeConfig:
                        Configuration for an InsightType.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta1/{insight_type_config.name=projects/*/locations/*/insightTypes/*/config}",
                    "body": "insight_type_config",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{insight_type_config.name=organizations/*/locations/*/insightTypes/*/config}",
                    "body": "insight_type_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_insight_type_config(
                request, metadata
            )
            pb_request = recommender_service.UpdateInsightTypeConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcr_insight_type_config.InsightTypeConfig()
            pb_resp = gcr_insight_type_config.InsightTypeConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_insight_type_config(resp)
            return resp

    class _UpdateRecommenderConfig(RecommenderRestStub):
        def __hash__(self):
            return hash("UpdateRecommenderConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: recommender_service.UpdateRecommenderConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcr_recommender_config.RecommenderConfig:
            r"""Call the update recommender config method over HTTP.

            Args:
                request (~.recommender_service.UpdateRecommenderConfigRequest):
                    The request object. Request for the ``UpdateRecommenderConfig`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcr_recommender_config.RecommenderConfig:
                    Configuration for a Recommender.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta1/{recommender_config.name=projects/*/locations/*/recommenders/*/config}",
                    "body": "recommender_config",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{recommender_config.name=organizations/*/locations/*/recommenders/*/config}",
                    "body": "recommender_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_recommender_config(
                request, metadata
            )
            pb_request = recommender_service.UpdateRecommenderConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcr_recommender_config.RecommenderConfig()
            pb_resp = gcr_recommender_config.RecommenderConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_recommender_config(resp)
            return resp

    @property
    def get_insight(
        self,
    ) -> Callable[[recommender_service.GetInsightRequest], insight.Insight]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInsight(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_insight_type_config(
        self,
    ) -> Callable[
        [recommender_service.GetInsightTypeConfigRequest],
        insight_type_config.InsightTypeConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInsightTypeConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_recommendation(
        self,
    ) -> Callable[
        [recommender_service.GetRecommendationRequest], recommendation.Recommendation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRecommendation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_recommender_config(
        self,
    ) -> Callable[
        [recommender_service.GetRecommenderConfigRequest],
        recommender_config.RecommenderConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRecommenderConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_insights(
        self,
    ) -> Callable[
        [recommender_service.ListInsightsRequest],
        recommender_service.ListInsightsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInsights(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_insight_types(
        self,
    ) -> Callable[
        [recommender_service.ListInsightTypesRequest],
        recommender_service.ListInsightTypesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInsightTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_recommendations(
        self,
    ) -> Callable[
        [recommender_service.ListRecommendationsRequest],
        recommender_service.ListRecommendationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRecommendations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_recommenders(
        self,
    ) -> Callable[
        [recommender_service.ListRecommendersRequest],
        recommender_service.ListRecommendersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRecommenders(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def mark_insight_accepted(
        self,
    ) -> Callable[[recommender_service.MarkInsightAcceptedRequest], insight.Insight]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MarkInsightAccepted(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def mark_recommendation_claimed(
        self,
    ) -> Callable[
        [recommender_service.MarkRecommendationClaimedRequest],
        recommendation.Recommendation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MarkRecommendationClaimed(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def mark_recommendation_failed(
        self,
    ) -> Callable[
        [recommender_service.MarkRecommendationFailedRequest],
        recommendation.Recommendation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MarkRecommendationFailed(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def mark_recommendation_succeeded(
        self,
    ) -> Callable[
        [recommender_service.MarkRecommendationSucceededRequest],
        recommendation.Recommendation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MarkRecommendationSucceeded(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_insight_type_config(
        self,
    ) -> Callable[
        [recommender_service.UpdateInsightTypeConfigRequest],
        gcr_insight_type_config.InsightTypeConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateInsightTypeConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_recommender_config(
        self,
    ) -> Callable[
        [recommender_service.UpdateRecommenderConfigRequest],
        gcr_recommender_config.RecommenderConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRecommenderConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RecommenderRestTransport",)
