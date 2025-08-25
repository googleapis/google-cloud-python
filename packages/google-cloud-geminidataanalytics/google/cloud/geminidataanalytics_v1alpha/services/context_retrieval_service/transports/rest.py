# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import google.protobuf
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.geminidataanalytics_v1alpha.types import context_retrieval_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseContextRetrievalServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class ContextRetrievalServiceRestInterceptor:
    """Interceptor for ContextRetrievalService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ContextRetrievalServiceRestTransport.

    .. code-block:: python
        class MyCustomContextRetrievalServiceInterceptor(ContextRetrievalServiceRestInterceptor):
            def pre_retrieve_big_query_recent_relevant_tables(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_retrieve_big_query_recent_relevant_tables(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_retrieve_big_query_table_contexts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_retrieve_big_query_table_contexts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_retrieve_big_query_table_contexts_from_recent_tables(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_retrieve_big_query_table_contexts_from_recent_tables(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_retrieve_big_query_table_suggested_descriptions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_retrieve_big_query_table_suggested_descriptions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_retrieve_big_query_table_suggested_examples(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_retrieve_big_query_table_suggested_examples(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ContextRetrievalServiceRestTransport(interceptor=MyCustomContextRetrievalServiceInterceptor())
        client = ContextRetrievalServiceClient(transport=transport)


    """

    def pre_retrieve_big_query_recent_relevant_tables(
        self,
        request: context_retrieval_service.RetrieveBigQueryRecentRelevantTablesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        context_retrieval_service.RetrieveBigQueryRecentRelevantTablesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for retrieve_big_query_recent_relevant_tables

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_retrieve_big_query_recent_relevant_tables(
        self,
        response: context_retrieval_service.RetrieveBigQueryRecentRelevantTablesResponse,
    ) -> context_retrieval_service.RetrieveBigQueryRecentRelevantTablesResponse:
        """Post-rpc interceptor for retrieve_big_query_recent_relevant_tables

        DEPRECATED. Please use the `post_retrieve_big_query_recent_relevant_tables_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code. This `post_retrieve_big_query_recent_relevant_tables` interceptor runs
        before the `post_retrieve_big_query_recent_relevant_tables_with_metadata` interceptor.
        """
        return response

    def post_retrieve_big_query_recent_relevant_tables_with_metadata(
        self,
        response: context_retrieval_service.RetrieveBigQueryRecentRelevantTablesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        context_retrieval_service.RetrieveBigQueryRecentRelevantTablesResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for retrieve_big_query_recent_relevant_tables

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContextRetrievalService server but before it is returned to user code.

        We recommend only using this `post_retrieve_big_query_recent_relevant_tables_with_metadata`
        interceptor in new development instead of the `post_retrieve_big_query_recent_relevant_tables` interceptor.
        When both interceptors are used, this `post_retrieve_big_query_recent_relevant_tables_with_metadata` interceptor runs after the
        `post_retrieve_big_query_recent_relevant_tables` interceptor. The (possibly modified) response returned by
        `post_retrieve_big_query_recent_relevant_tables` will be passed to
        `post_retrieve_big_query_recent_relevant_tables_with_metadata`.
        """
        return response, metadata

    def pre_retrieve_big_query_table_contexts(
        self,
        request: context_retrieval_service.RetrieveBigQueryTableContextsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        context_retrieval_service.RetrieveBigQueryTableContextsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for retrieve_big_query_table_contexts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_retrieve_big_query_table_contexts(
        self, response: context_retrieval_service.RetrieveBigQueryTableContextsResponse
    ) -> context_retrieval_service.RetrieveBigQueryTableContextsResponse:
        """Post-rpc interceptor for retrieve_big_query_table_contexts

        DEPRECATED. Please use the `post_retrieve_big_query_table_contexts_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code. This `post_retrieve_big_query_table_contexts` interceptor runs
        before the `post_retrieve_big_query_table_contexts_with_metadata` interceptor.
        """
        return response

    def post_retrieve_big_query_table_contexts_with_metadata(
        self,
        response: context_retrieval_service.RetrieveBigQueryTableContextsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        context_retrieval_service.RetrieveBigQueryTableContextsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for retrieve_big_query_table_contexts

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContextRetrievalService server but before it is returned to user code.

        We recommend only using this `post_retrieve_big_query_table_contexts_with_metadata`
        interceptor in new development instead of the `post_retrieve_big_query_table_contexts` interceptor.
        When both interceptors are used, this `post_retrieve_big_query_table_contexts_with_metadata` interceptor runs after the
        `post_retrieve_big_query_table_contexts` interceptor. The (possibly modified) response returned by
        `post_retrieve_big_query_table_contexts` will be passed to
        `post_retrieve_big_query_table_contexts_with_metadata`.
        """
        return response, metadata

    def pre_retrieve_big_query_table_contexts_from_recent_tables(
        self,
        request: context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for retrieve_big_query_table_contexts_from_recent_tables

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_retrieve_big_query_table_contexts_from_recent_tables(
        self,
        response: context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesResponse,
    ) -> (
        context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesResponse
    ):
        """Post-rpc interceptor for retrieve_big_query_table_contexts_from_recent_tables

        DEPRECATED. Please use the `post_retrieve_big_query_table_contexts_from_recent_tables_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code. This `post_retrieve_big_query_table_contexts_from_recent_tables` interceptor runs
        before the `post_retrieve_big_query_table_contexts_from_recent_tables_with_metadata` interceptor.
        """
        return response

    def post_retrieve_big_query_table_contexts_from_recent_tables_with_metadata(
        self,
        response: context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for retrieve_big_query_table_contexts_from_recent_tables

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContextRetrievalService server but before it is returned to user code.

        We recommend only using this `post_retrieve_big_query_table_contexts_from_recent_tables_with_metadata`
        interceptor in new development instead of the `post_retrieve_big_query_table_contexts_from_recent_tables` interceptor.
        When both interceptors are used, this `post_retrieve_big_query_table_contexts_from_recent_tables_with_metadata` interceptor runs after the
        `post_retrieve_big_query_table_contexts_from_recent_tables` interceptor. The (possibly modified) response returned by
        `post_retrieve_big_query_table_contexts_from_recent_tables` will be passed to
        `post_retrieve_big_query_table_contexts_from_recent_tables_with_metadata`.
        """
        return response, metadata

    def pre_retrieve_big_query_table_suggested_descriptions(
        self,
        request: context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for retrieve_big_query_table_suggested_descriptions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_retrieve_big_query_table_suggested_descriptions(
        self,
        response: context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsResponse,
    ) -> context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsResponse:
        """Post-rpc interceptor for retrieve_big_query_table_suggested_descriptions

        DEPRECATED. Please use the `post_retrieve_big_query_table_suggested_descriptions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code. This `post_retrieve_big_query_table_suggested_descriptions` interceptor runs
        before the `post_retrieve_big_query_table_suggested_descriptions_with_metadata` interceptor.
        """
        return response

    def post_retrieve_big_query_table_suggested_descriptions_with_metadata(
        self,
        response: context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for retrieve_big_query_table_suggested_descriptions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContextRetrievalService server but before it is returned to user code.

        We recommend only using this `post_retrieve_big_query_table_suggested_descriptions_with_metadata`
        interceptor in new development instead of the `post_retrieve_big_query_table_suggested_descriptions` interceptor.
        When both interceptors are used, this `post_retrieve_big_query_table_suggested_descriptions_with_metadata` interceptor runs after the
        `post_retrieve_big_query_table_suggested_descriptions` interceptor. The (possibly modified) response returned by
        `post_retrieve_big_query_table_suggested_descriptions` will be passed to
        `post_retrieve_big_query_table_suggested_descriptions_with_metadata`.
        """
        return response, metadata

    def pre_retrieve_big_query_table_suggested_examples(
        self,
        request: context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for retrieve_big_query_table_suggested_examples

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_retrieve_big_query_table_suggested_examples(
        self,
        response: context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesResponse,
    ) -> context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesResponse:
        """Post-rpc interceptor for retrieve_big_query_table_suggested_examples

        DEPRECATED. Please use the `post_retrieve_big_query_table_suggested_examples_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code. This `post_retrieve_big_query_table_suggested_examples` interceptor runs
        before the `post_retrieve_big_query_table_suggested_examples_with_metadata` interceptor.
        """
        return response

    def post_retrieve_big_query_table_suggested_examples_with_metadata(
        self,
        response: context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for retrieve_big_query_table_suggested_examples

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ContextRetrievalService server but before it is returned to user code.

        We recommend only using this `post_retrieve_big_query_table_suggested_examples_with_metadata`
        interceptor in new development instead of the `post_retrieve_big_query_table_suggested_examples` interceptor.
        When both interceptors are used, this `post_retrieve_big_query_table_suggested_examples_with_metadata` interceptor runs after the
        `post_retrieve_big_query_table_suggested_examples` interceptor. The (possibly modified) response returned by
        `post_retrieve_big_query_table_suggested_examples` will be passed to
        `post_retrieve_big_query_table_suggested_examples_with_metadata`.
        """
        return response, metadata

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.CancelOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ContextRetrievalService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ContextRetrievalService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ContextRetrievalServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ContextRetrievalServiceRestInterceptor


class ContextRetrievalServiceRestTransport(_BaseContextRetrievalServiceRestTransport):
    """REST backend synchronous transport for ContextRetrievalService.

    Service to ask a natural language question with a provided
    project, returns BigQuery tables that are relevant to the
    question within the project scope that is accessible to the
    user, along with contextual data including table schema
    information as well as sample values.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "geminidataanalytics.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ContextRetrievalServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'geminidataanalytics.googleapis.com').
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
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ContextRetrievalServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _RetrieveBigQueryRecentRelevantTables(
        _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryRecentRelevantTables,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "ContextRetrievalServiceRestTransport.RetrieveBigQueryRecentRelevantTables"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: context_retrieval_service.RetrieveBigQueryRecentRelevantTablesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> context_retrieval_service.RetrieveBigQueryRecentRelevantTablesResponse:
            r"""Call the retrieve big query recent
            relevant tables method over HTTP.

                Args:
                    request (~.context_retrieval_service.RetrieveBigQueryRecentRelevantTablesRequest):
                        The request object. Request for retrieving BigQuery table
                    references from recently accessed
                    tables. Response is sorted by semantic
                    similarity to the query.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.context_retrieval_service.RetrieveBigQueryRecentRelevantTablesResponse:
                        Response for retrieving BigQuery
                    table references from recently accessed
                    tables. Response is sorted by semantic
                    similarity to the query.

            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryRecentRelevantTables._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_retrieve_big_query_recent_relevant_tables(
                request, metadata
            )
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryRecentRelevantTables._get_transcoded_request(
                http_options, request
            )

            body = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryRecentRelevantTables._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryRecentRelevantTables._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.RetrieveBigQueryRecentRelevantTables",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "RetrieveBigQueryRecentRelevantTables",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContextRetrievalServiceRestTransport._RetrieveBigQueryRecentRelevantTables._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = (
                context_retrieval_service.RetrieveBigQueryRecentRelevantTablesResponse()
            )
            pb_resp = context_retrieval_service.RetrieveBigQueryRecentRelevantTablesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_retrieve_big_query_recent_relevant_tables(
                resp
            )
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_retrieve_big_query_recent_relevant_tables_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = context_retrieval_service.RetrieveBigQueryRecentRelevantTablesResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.retrieve_big_query_recent_relevant_tables",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "RetrieveBigQueryRecentRelevantTables",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RetrieveBigQueryTableContexts(
        _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableContexts,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "ContextRetrievalServiceRestTransport.RetrieveBigQueryTableContexts"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: context_retrieval_service.RetrieveBigQueryTableContextsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> context_retrieval_service.RetrieveBigQueryTableContextsResponse:
            r"""Call the retrieve big query table
            contexts method over HTTP.

                Args:
                    request (~.context_retrieval_service.RetrieveBigQueryTableContextsRequest):
                        The request object. Request for retrieving BigQuery table
                    contextual data via direct lookup.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.context_retrieval_service.RetrieveBigQueryTableContextsResponse:
                        Response for retrieving BigQuery
                    table contextual data via direct lookup.

            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableContexts._get_http_options()
            )

            request, metadata = self._interceptor.pre_retrieve_big_query_table_contexts(
                request, metadata
            )
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableContexts._get_transcoded_request(
                http_options, request
            )

            body = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableContexts._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableContexts._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.RetrieveBigQueryTableContexts",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "RetrieveBigQueryTableContexts",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContextRetrievalServiceRestTransport._RetrieveBigQueryTableContexts._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = context_retrieval_service.RetrieveBigQueryTableContextsResponse()
            pb_resp = (
                context_retrieval_service.RetrieveBigQueryTableContextsResponse.pb(resp)
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_retrieve_big_query_table_contexts(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_retrieve_big_query_table_contexts_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = context_retrieval_service.RetrieveBigQueryTableContextsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.retrieve_big_query_table_contexts",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "RetrieveBigQueryTableContexts",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RetrieveBigQueryTableContextsFromRecentTables(
        _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableContextsFromRecentTables,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "ContextRetrievalServiceRestTransport.RetrieveBigQueryTableContextsFromRecentTables"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> (
            context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesResponse
        ):
            r"""Call the retrieve big query table
            contexts from recent tables method over HTTP.

                Args:
                    request (~.context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesRequest):
                        The request object. Request for retrieving BigQuery table
                    contextual data from recently accessed
                    tables. Response is sorted by semantic
                    similarity to the query.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesResponse:
                        Response for retrieving BigQuery
                    table contextual data from recently
                    accessed tables. Response is sorted by
                    semantic similarity to the query.

            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableContextsFromRecentTables._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_retrieve_big_query_table_contexts_from_recent_tables(
                request, metadata
            )
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableContextsFromRecentTables._get_transcoded_request(
                http_options, request
            )

            body = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableContextsFromRecentTables._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableContextsFromRecentTables._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.RetrieveBigQueryTableContextsFromRecentTables",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "RetrieveBigQueryTableContextsFromRecentTables",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContextRetrievalServiceRestTransport._RetrieveBigQueryTableContextsFromRecentTables._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = (
                context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesResponse()
            )
            pb_resp = context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_retrieve_big_query_table_contexts_from_recent_tables(
                resp
            )
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_retrieve_big_query_table_contexts_from_recent_tables_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.retrieve_big_query_table_contexts_from_recent_tables",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "RetrieveBigQueryTableContextsFromRecentTables",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RetrieveBigQueryTableSuggestedDescriptions(
        _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableSuggestedDescriptions,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "ContextRetrievalServiceRestTransport.RetrieveBigQueryTableSuggestedDescriptions"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> (
            context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsResponse
        ):
            r"""Call the retrieve big query table
            suggested descriptions method over HTTP.

                Args:
                    request (~.context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsRequest):
                        The request object. Request for retrieving BigQuery table
                    schema with suggested table and column
                    descriptions. Columns are sorted by
                    default BigQuery table schema order.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsResponse:
                        Response for retrieving BigQuery
                    table schema with suggested table and
                    column descriptions. Columns are sorted
                    by default BigQuery table schema order.

            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableSuggestedDescriptions._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_retrieve_big_query_table_suggested_descriptions(
                request, metadata
            )
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableSuggestedDescriptions._get_transcoded_request(
                http_options, request
            )

            body = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableSuggestedDescriptions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableSuggestedDescriptions._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.RetrieveBigQueryTableSuggestedDescriptions",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "RetrieveBigQueryTableSuggestedDescriptions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContextRetrievalServiceRestTransport._RetrieveBigQueryTableSuggestedDescriptions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = (
                context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsResponse()
            )
            pb_resp = context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = (
                self._interceptor.post_retrieve_big_query_table_suggested_descriptions(
                    resp
                )
            )
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_retrieve_big_query_table_suggested_descriptions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.retrieve_big_query_table_suggested_descriptions",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "RetrieveBigQueryTableSuggestedDescriptions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RetrieveBigQueryTableSuggestedExamples(
        _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableSuggestedExamples,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "ContextRetrievalServiceRestTransport.RetrieveBigQueryTableSuggestedExamples"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesResponse:
            r"""Call the retrieve big query table
            suggested examples method over HTTP.

                Args:
                    request (~.context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesRequest):
                        The request object. Request for retrieving BigQuery table
                    schema with suggested NL-SQL examples.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesResponse:
                        Request for retrieving BigQuery table
                    schema with suggested NL-SQL examples.

            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableSuggestedExamples._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_retrieve_big_query_table_suggested_examples(
                request, metadata
            )
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableSuggestedExamples._get_transcoded_request(
                http_options, request
            )

            body = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableSuggestedExamples._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseRetrieveBigQueryTableSuggestedExamples._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.RetrieveBigQueryTableSuggestedExamples",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "RetrieveBigQueryTableSuggestedExamples",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContextRetrievalServiceRestTransport._RetrieveBigQueryTableSuggestedExamples._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = (
                context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesResponse()
            )
            pb_resp = context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_retrieve_big_query_table_suggested_examples(
                resp
            )
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_retrieve_big_query_table_suggested_examples_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.retrieve_big_query_table_suggested_examples",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "RetrieveBigQueryTableSuggestedExamples",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def retrieve_big_query_recent_relevant_tables(
        self,
    ) -> Callable[
        [context_retrieval_service.RetrieveBigQueryRecentRelevantTablesRequest],
        context_retrieval_service.RetrieveBigQueryRecentRelevantTablesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RetrieveBigQueryRecentRelevantTables(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def retrieve_big_query_table_contexts(
        self,
    ) -> Callable[
        [context_retrieval_service.RetrieveBigQueryTableContextsRequest],
        context_retrieval_service.RetrieveBigQueryTableContextsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RetrieveBigQueryTableContexts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def retrieve_big_query_table_contexts_from_recent_tables(
        self,
    ) -> Callable[
        [
            context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesRequest
        ],
        context_retrieval_service.RetrieveBigQueryTableContextsFromRecentTablesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RetrieveBigQueryTableContextsFromRecentTables(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def retrieve_big_query_table_suggested_descriptions(
        self,
    ) -> Callable[
        [context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsRequest],
        context_retrieval_service.RetrieveBigQueryTableSuggestedDescriptionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RetrieveBigQueryTableSuggestedDescriptions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def retrieve_big_query_table_suggested_examples(
        self,
    ) -> Callable[
        [context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesRequest],
        context_retrieval_service.RetrieveBigQueryTableSuggestedExamplesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RetrieveBigQueryTableSuggestedExamples(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseContextRetrievalServiceRestTransport._BaseGetLocation,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContextRetrievalServiceRestTransport.GetLocation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContextRetrievalServiceRestTransport._GetLocation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseContextRetrievalServiceRestTransport._BaseListLocations,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContextRetrievalServiceRestTransport.ListLocations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ContextRetrievalServiceRestTransport._ListLocations._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseContextRetrievalServiceRestTransport._BaseCancelOperation,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContextRetrievalServiceRestTransport.CancelOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseCancelOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseContextRetrievalServiceRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.CancelOperation",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ContextRetrievalServiceRestTransport._CancelOperation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseContextRetrievalServiceRestTransport._BaseDeleteOperation,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContextRetrievalServiceRestTransport.DeleteOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseDeleteOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.DeleteOperation",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "DeleteOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ContextRetrievalServiceRestTransport._DeleteOperation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseContextRetrievalServiceRestTransport._BaseGetOperation,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContextRetrievalServiceRestTransport.GetOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ContextRetrievalServiceRestTransport._GetOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseContextRetrievalServiceRestTransport._BaseListOperations,
        ContextRetrievalServiceRestStub,
    ):
        def __hash__(self):
            return hash("ContextRetrievalServiceRestTransport.ListOperations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseContextRetrievalServiceRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseContextRetrievalServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseContextRetrievalServiceRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ContextRetrievalServiceRestTransport._ListOperations._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.geminidataanalytics_v1alpha.ContextRetrievalServiceAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.geminidataanalytics.v1alpha.ContextRetrievalService",
                        "rpcName": "ListOperations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ContextRetrievalServiceRestTransport",)
