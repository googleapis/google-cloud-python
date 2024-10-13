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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.discoveryengine_v1beta.types import (
    site_search_engine,
    site_search_engine_service,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSiteSearchEngineServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class SiteSearchEngineServiceRestInterceptor:
    """Interceptor for SiteSearchEngineService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SiteSearchEngineServiceRestTransport.

    .. code-block:: python
        class MyCustomSiteSearchEngineServiceInterceptor(SiteSearchEngineServiceRestInterceptor):
            def pre_batch_create_target_sites(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_target_sites(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_verify_target_sites(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_verify_target_sites(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_target_site(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_target_site(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_target_site(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_target_site(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_disable_advanced_site_search(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_disable_advanced_site_search(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_enable_advanced_site_search(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_enable_advanced_site_search(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_domain_verification_status(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_domain_verification_status(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_site_search_engine(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_site_search_engine(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_target_site(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_target_site(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_target_sites(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_target_sites(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_recrawl_uris(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_recrawl_uris(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_target_site(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_target_site(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SiteSearchEngineServiceRestTransport(interceptor=MyCustomSiteSearchEngineServiceInterceptor())
        client = SiteSearchEngineServiceClient(transport=transport)


    """

    def pre_batch_create_target_sites(
        self,
        request: site_search_engine_service.BatchCreateTargetSitesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.BatchCreateTargetSitesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for batch_create_target_sites

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_batch_create_target_sites(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_create_target_sites

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_batch_verify_target_sites(
        self,
        request: site_search_engine_service.BatchVerifyTargetSitesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.BatchVerifyTargetSitesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for batch_verify_target_sites

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_batch_verify_target_sites(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_verify_target_sites

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_create_target_site(
        self,
        request: site_search_engine_service.CreateTargetSiteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.CreateTargetSiteRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_target_site

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_create_target_site(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_target_site

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_target_site(
        self,
        request: site_search_engine_service.DeleteTargetSiteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.DeleteTargetSiteRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_target_site

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_delete_target_site(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_target_site

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_disable_advanced_site_search(
        self,
        request: site_search_engine_service.DisableAdvancedSiteSearchRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.DisableAdvancedSiteSearchRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for disable_advanced_site_search

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_disable_advanced_site_search(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for disable_advanced_site_search

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_enable_advanced_site_search(
        self,
        request: site_search_engine_service.EnableAdvancedSiteSearchRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.EnableAdvancedSiteSearchRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for enable_advanced_site_search

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_enable_advanced_site_search(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for enable_advanced_site_search

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_domain_verification_status(
        self,
        request: site_search_engine_service.FetchDomainVerificationStatusRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.FetchDomainVerificationStatusRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for fetch_domain_verification_status

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_fetch_domain_verification_status(
        self, response: site_search_engine_service.FetchDomainVerificationStatusResponse
    ) -> site_search_engine_service.FetchDomainVerificationStatusResponse:
        """Post-rpc interceptor for fetch_domain_verification_status

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_get_site_search_engine(
        self,
        request: site_search_engine_service.GetSiteSearchEngineRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.GetSiteSearchEngineRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_site_search_engine

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_get_site_search_engine(
        self, response: site_search_engine.SiteSearchEngine
    ) -> site_search_engine.SiteSearchEngine:
        """Post-rpc interceptor for get_site_search_engine

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_get_target_site(
        self,
        request: site_search_engine_service.GetTargetSiteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.GetTargetSiteRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_target_site

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_get_target_site(
        self, response: site_search_engine.TargetSite
    ) -> site_search_engine.TargetSite:
        """Post-rpc interceptor for get_target_site

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_list_target_sites(
        self,
        request: site_search_engine_service.ListTargetSitesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.ListTargetSitesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_target_sites

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_list_target_sites(
        self, response: site_search_engine_service.ListTargetSitesResponse
    ) -> site_search_engine_service.ListTargetSitesResponse:
        """Post-rpc interceptor for list_target_sites

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_recrawl_uris(
        self,
        request: site_search_engine_service.RecrawlUrisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.RecrawlUrisRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for recrawl_uris

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_recrawl_uris(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for recrawl_uris

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_update_target_site(
        self,
        request: site_search_engine_service.UpdateTargetSiteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        site_search_engine_service.UpdateTargetSiteRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_target_site

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_update_target_site(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_target_site

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SiteSearchEngineService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the SiteSearchEngineService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SiteSearchEngineServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SiteSearchEngineServiceRestInterceptor


class SiteSearchEngineServiceRestTransport(_BaseSiteSearchEngineServiceRestTransport):
    """REST backend synchronous transport for SiteSearchEngineService.

    Service for managing site search related resources.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "discoveryengine.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SiteSearchEngineServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'discoveryengine.googleapis.com').
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or SiteSearchEngineServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}:cancel",
                        "body": "*",
                    },
                    {
                        "method": "post",
                        "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataConnector/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/models/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/engines/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/models/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/evaluations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/sampleQuerySets/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataConnector}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/models/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/dataStores/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*/engines/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/collections/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/branches/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*/models/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/dataStores/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1beta",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchCreateTargetSites(
        _BaseSiteSearchEngineServiceRestTransport._BaseBatchCreateTargetSites,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.BatchCreateTargetSites")

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
            request: site_search_engine_service.BatchCreateTargetSitesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch create target sites method over HTTP.

            Args:
                request (~.site_search_engine_service.BatchCreateTargetSitesRequest):
                    The request object. Request message for
                [SiteSearchEngineService.BatchCreateTargetSites][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.BatchCreateTargetSites]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseBatchCreateTargetSites._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_create_target_sites(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseBatchCreateTargetSites._get_transcoded_request(
                http_options, request
            )

            body = _BaseSiteSearchEngineServiceRestTransport._BaseBatchCreateTargetSites._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseBatchCreateTargetSites._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SiteSearchEngineServiceRestTransport._BatchCreateTargetSites._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_create_target_sites(resp)
            return resp

    class _BatchVerifyTargetSites(
        _BaseSiteSearchEngineServiceRestTransport._BaseBatchVerifyTargetSites,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.BatchVerifyTargetSites")

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
            request: site_search_engine_service.BatchVerifyTargetSitesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch verify target sites method over HTTP.

            Args:
                request (~.site_search_engine_service.BatchVerifyTargetSitesRequest):
                    The request object. Request message for
                [SiteSearchEngineService.BatchVerifyTargetSites][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.BatchVerifyTargetSites]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseBatchVerifyTargetSites._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_verify_target_sites(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseBatchVerifyTargetSites._get_transcoded_request(
                http_options, request
            )

            body = _BaseSiteSearchEngineServiceRestTransport._BaseBatchVerifyTargetSites._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseBatchVerifyTargetSites._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SiteSearchEngineServiceRestTransport._BatchVerifyTargetSites._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_verify_target_sites(resp)
            return resp

    class _CreateTargetSite(
        _BaseSiteSearchEngineServiceRestTransport._BaseCreateTargetSite,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.CreateTargetSite")

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
            request: site_search_engine_service.CreateTargetSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create target site method over HTTP.

            Args:
                request (~.site_search_engine_service.CreateTargetSiteRequest):
                    The request object. Request message for
                [SiteSearchEngineService.CreateTargetSite][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.CreateTargetSite]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseCreateTargetSite._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_target_site(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseCreateTargetSite._get_transcoded_request(
                http_options, request
            )

            body = _BaseSiteSearchEngineServiceRestTransport._BaseCreateTargetSite._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseCreateTargetSite._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SiteSearchEngineServiceRestTransport._CreateTargetSite._get_response(
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

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_target_site(resp)
            return resp

    class _DeleteTargetSite(
        _BaseSiteSearchEngineServiceRestTransport._BaseDeleteTargetSite,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.DeleteTargetSite")

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
            request: site_search_engine_service.DeleteTargetSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete target site method over HTTP.

            Args:
                request (~.site_search_engine_service.DeleteTargetSiteRequest):
                    The request object. Request message for
                [SiteSearchEngineService.DeleteTargetSite][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.DeleteTargetSite]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseDeleteTargetSite._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_target_site(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseDeleteTargetSite._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseDeleteTargetSite._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SiteSearchEngineServiceRestTransport._DeleteTargetSite._get_response(
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

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_target_site(resp)
            return resp

    class _DisableAdvancedSiteSearch(
        _BaseSiteSearchEngineServiceRestTransport._BaseDisableAdvancedSiteSearch,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "SiteSearchEngineServiceRestTransport.DisableAdvancedSiteSearch"
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
            request: site_search_engine_service.DisableAdvancedSiteSearchRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the disable advanced site
            search method over HTTP.

                Args:
                    request (~.site_search_engine_service.DisableAdvancedSiteSearchRequest):
                        The request object. Request message for
                    [SiteSearchEngineService.DisableAdvancedSiteSearch][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.DisableAdvancedSiteSearch]
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseDisableAdvancedSiteSearch._get_http_options()
            )
            request, metadata = self._interceptor.pre_disable_advanced_site_search(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseDisableAdvancedSiteSearch._get_transcoded_request(
                http_options, request
            )

            body = _BaseSiteSearchEngineServiceRestTransport._BaseDisableAdvancedSiteSearch._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseDisableAdvancedSiteSearch._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SiteSearchEngineServiceRestTransport._DisableAdvancedSiteSearch._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_disable_advanced_site_search(resp)
            return resp

    class _EnableAdvancedSiteSearch(
        _BaseSiteSearchEngineServiceRestTransport._BaseEnableAdvancedSiteSearch,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.EnableAdvancedSiteSearch")

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
            request: site_search_engine_service.EnableAdvancedSiteSearchRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the enable advanced site
            search method over HTTP.

                Args:
                    request (~.site_search_engine_service.EnableAdvancedSiteSearchRequest):
                        The request object. Request message for
                    [SiteSearchEngineService.EnableAdvancedSiteSearch][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.EnableAdvancedSiteSearch]
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseEnableAdvancedSiteSearch._get_http_options()
            )
            request, metadata = self._interceptor.pre_enable_advanced_site_search(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseEnableAdvancedSiteSearch._get_transcoded_request(
                http_options, request
            )

            body = _BaseSiteSearchEngineServiceRestTransport._BaseEnableAdvancedSiteSearch._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseEnableAdvancedSiteSearch._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SiteSearchEngineServiceRestTransport._EnableAdvancedSiteSearch._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_enable_advanced_site_search(resp)
            return resp

    class _FetchDomainVerificationStatus(
        _BaseSiteSearchEngineServiceRestTransport._BaseFetchDomainVerificationStatus,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "SiteSearchEngineServiceRestTransport.FetchDomainVerificationStatus"
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
            )
            return response

        def __call__(
            self,
            request: site_search_engine_service.FetchDomainVerificationStatusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> site_search_engine_service.FetchDomainVerificationStatusResponse:
            r"""Call the fetch domain verification
            status method over HTTP.

                Args:
                    request (~.site_search_engine_service.FetchDomainVerificationStatusRequest):
                        The request object. Request message for
                    [SiteSearchEngineService.FetchDomainVerificationStatus][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.FetchDomainVerificationStatus]
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.site_search_engine_service.FetchDomainVerificationStatusResponse:
                        Response message for
                    [SiteSearchEngineService.FetchDomainVerificationStatus][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.FetchDomainVerificationStatus]
                    method.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseFetchDomainVerificationStatus._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_domain_verification_status(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseFetchDomainVerificationStatus._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseFetchDomainVerificationStatus._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SiteSearchEngineServiceRestTransport._FetchDomainVerificationStatus._get_response(
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

            # Return the response
            resp = site_search_engine_service.FetchDomainVerificationStatusResponse()
            pb_resp = (
                site_search_engine_service.FetchDomainVerificationStatusResponse.pb(
                    resp
                )
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_domain_verification_status(resp)
            return resp

    class _GetSiteSearchEngine(
        _BaseSiteSearchEngineServiceRestTransport._BaseGetSiteSearchEngine,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.GetSiteSearchEngine")

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
            request: site_search_engine_service.GetSiteSearchEngineRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> site_search_engine.SiteSearchEngine:
            r"""Call the get site search engine method over HTTP.

            Args:
                request (~.site_search_engine_service.GetSiteSearchEngineRequest):
                    The request object. Request message for
                [SiteSearchEngineService.GetSiteSearchEngine][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.GetSiteSearchEngine]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.site_search_engine.SiteSearchEngine:
                    SiteSearchEngine captures DataStore
                level site search persisting
                configurations. It is a singleton value
                per data store.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseGetSiteSearchEngine._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_site_search_engine(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseGetSiteSearchEngine._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseGetSiteSearchEngine._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SiteSearchEngineServiceRestTransport._GetSiteSearchEngine._get_response(
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

            # Return the response
            resp = site_search_engine.SiteSearchEngine()
            pb_resp = site_search_engine.SiteSearchEngine.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_site_search_engine(resp)
            return resp

    class _GetTargetSite(
        _BaseSiteSearchEngineServiceRestTransport._BaseGetTargetSite,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.GetTargetSite")

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
            request: site_search_engine_service.GetTargetSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> site_search_engine.TargetSite:
            r"""Call the get target site method over HTTP.

            Args:
                request (~.site_search_engine_service.GetTargetSiteRequest):
                    The request object. Request message for
                [SiteSearchEngineService.GetTargetSite][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.GetTargetSite]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.site_search_engine.TargetSite:
                    A target site for the
                SiteSearchEngine.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseGetTargetSite._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_target_site(request, metadata)
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseGetTargetSite._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseGetTargetSite._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SiteSearchEngineServiceRestTransport._GetTargetSite._get_response(
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

            # Return the response
            resp = site_search_engine.TargetSite()
            pb_resp = site_search_engine.TargetSite.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_target_site(resp)
            return resp

    class _ListTargetSites(
        _BaseSiteSearchEngineServiceRestTransport._BaseListTargetSites,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.ListTargetSites")

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
            request: site_search_engine_service.ListTargetSitesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> site_search_engine_service.ListTargetSitesResponse:
            r"""Call the list target sites method over HTTP.

            Args:
                request (~.site_search_engine_service.ListTargetSitesRequest):
                    The request object. Request message for
                [SiteSearchEngineService.ListTargetSites][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.ListTargetSites]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.site_search_engine_service.ListTargetSitesResponse:
                    Response message for
                [SiteSearchEngineService.ListTargetSites][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.ListTargetSites]
                method.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseListTargetSites._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_target_sites(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseListTargetSites._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseListTargetSites._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SiteSearchEngineServiceRestTransport._ListTargetSites._get_response(
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

            # Return the response
            resp = site_search_engine_service.ListTargetSitesResponse()
            pb_resp = site_search_engine_service.ListTargetSitesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_target_sites(resp)
            return resp

    class _RecrawlUris(
        _BaseSiteSearchEngineServiceRestTransport._BaseRecrawlUris,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.RecrawlUris")

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
            request: site_search_engine_service.RecrawlUrisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the recrawl uris method over HTTP.

            Args:
                request (~.site_search_engine_service.RecrawlUrisRequest):
                    The request object. Request message for
                [SiteSearchEngineService.RecrawlUris][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.RecrawlUris]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseRecrawlUris._get_http_options()
            )
            request, metadata = self._interceptor.pre_recrawl_uris(request, metadata)
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseRecrawlUris._get_transcoded_request(
                http_options, request
            )

            body = _BaseSiteSearchEngineServiceRestTransport._BaseRecrawlUris._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseRecrawlUris._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SiteSearchEngineServiceRestTransport._RecrawlUris._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_recrawl_uris(resp)
            return resp

    class _UpdateTargetSite(
        _BaseSiteSearchEngineServiceRestTransport._BaseUpdateTargetSite,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.UpdateTargetSite")

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
            request: site_search_engine_service.UpdateTargetSiteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update target site method over HTTP.

            Args:
                request (~.site_search_engine_service.UpdateTargetSiteRequest):
                    The request object. Request message for
                [SiteSearchEngineService.UpdateTargetSite][google.cloud.discoveryengine.v1beta.SiteSearchEngineService.UpdateTargetSite]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseUpdateTargetSite._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_target_site(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseUpdateTargetSite._get_transcoded_request(
                http_options, request
            )

            body = _BaseSiteSearchEngineServiceRestTransport._BaseUpdateTargetSite._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseUpdateTargetSite._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SiteSearchEngineServiceRestTransport._UpdateTargetSite._get_response(
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

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_target_site(resp)
            return resp

    @property
    def batch_create_target_sites(
        self,
    ) -> Callable[
        [site_search_engine_service.BatchCreateTargetSitesRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateTargetSites(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_verify_target_sites(
        self,
    ) -> Callable[
        [site_search_engine_service.BatchVerifyTargetSitesRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchVerifyTargetSites(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_target_site(
        self,
    ) -> Callable[
        [site_search_engine_service.CreateTargetSiteRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTargetSite(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_target_site(
        self,
    ) -> Callable[
        [site_search_engine_service.DeleteTargetSiteRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTargetSite(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def disable_advanced_site_search(
        self,
    ) -> Callable[
        [site_search_engine_service.DisableAdvancedSiteSearchRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DisableAdvancedSiteSearch(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enable_advanced_site_search(
        self,
    ) -> Callable[
        [site_search_engine_service.EnableAdvancedSiteSearchRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnableAdvancedSiteSearch(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_domain_verification_status(
        self,
    ) -> Callable[
        [site_search_engine_service.FetchDomainVerificationStatusRequest],
        site_search_engine_service.FetchDomainVerificationStatusResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchDomainVerificationStatus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_site_search_engine(
        self,
    ) -> Callable[
        [site_search_engine_service.GetSiteSearchEngineRequest],
        site_search_engine.SiteSearchEngine,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSiteSearchEngine(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_target_site(
        self,
    ) -> Callable[
        [site_search_engine_service.GetTargetSiteRequest], site_search_engine.TargetSite
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTargetSite(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_target_sites(
        self,
    ) -> Callable[
        [site_search_engine_service.ListTargetSitesRequest],
        site_search_engine_service.ListTargetSitesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTargetSites(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def recrawl_uris(
        self,
    ) -> Callable[
        [site_search_engine_service.RecrawlUrisRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RecrawlUris(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_target_site(
        self,
    ) -> Callable[
        [site_search_engine_service.UpdateTargetSiteRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTargetSite(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseSiteSearchEngineServiceRestTransport._BaseCancelOperation,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.CancelOperation")

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseSiteSearchEngineServiceRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SiteSearchEngineServiceRestTransport._CancelOperation._get_response(
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
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseSiteSearchEngineServiceRestTransport._BaseGetOperation,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.GetOperation")

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SiteSearchEngineServiceRestTransport._GetOperation._get_response(
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
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseSiteSearchEngineServiceRestTransport._BaseListOperations,
        SiteSearchEngineServiceRestStub,
    ):
        def __hash__(self):
            return hash("SiteSearchEngineServiceRestTransport.ListOperations")

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
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseSiteSearchEngineServiceRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseSiteSearchEngineServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSiteSearchEngineServiceRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SiteSearchEngineServiceRestTransport._ListOperations._get_response(
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
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SiteSearchEngineServiceRestTransport",)
