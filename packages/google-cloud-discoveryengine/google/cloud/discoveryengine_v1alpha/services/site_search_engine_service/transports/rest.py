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

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.discoveryengine_v1alpha.types import (
    site_search_engine,
    site_search_engine_service,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import SiteSearchEngineServiceTransport

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


class SiteSearchEngineServiceRestTransport(SiteSearchEngineServiceTransport):
    """REST backend transport for SiteSearchEngineService.

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
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataConnector/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/models/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/engines/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/models/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataConnector}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/models/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/engines/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/branches/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/models/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1alpha",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchCreateTargetSites(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("BatchCreateTargetSites")

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
                [SiteSearchEngineService.BatchCreateTargetSites][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.BatchCreateTargetSites]
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/dataStores/*/siteSearchEngine}/targetSites:batchCreate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/targetSites:batchCreate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_create_target_sites(
                request, metadata
            )
            pb_request = site_search_engine_service.BatchCreateTargetSitesRequest.pb(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_create_target_sites(resp)
            return resp

    class _BatchVerifyTargetSites(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("BatchVerifyTargetSites")

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
                [SiteSearchEngineService.BatchVerifyTargetSites][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.BatchVerifyTargetSites]
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}:batchVerifyTargetSites",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_verify_target_sites(
                request, metadata
            )
            pb_request = site_search_engine_service.BatchVerifyTargetSitesRequest.pb(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_verify_target_sites(resp)
            return resp

    class _CreateTargetSite(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("CreateTargetSite")

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
                [SiteSearchEngineService.CreateTargetSite][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.CreateTargetSite]
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/dataStores/*/siteSearchEngine}/targetSites",
                    "body": "target_site",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/targetSites",
                    "body": "target_site",
                },
            ]
            request, metadata = self._interceptor.pre_create_target_site(
                request, metadata
            )
            pb_request = site_search_engine_service.CreateTargetSiteRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_target_site(resp)
            return resp

    class _DeleteTargetSite(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("DeleteTargetSite")

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
                [SiteSearchEngineService.DeleteTargetSite][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.DeleteTargetSite]
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/siteSearchEngine/targetSites/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_target_site(
                request, metadata
            )
            pb_request = site_search_engine_service.DeleteTargetSiteRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_target_site(resp)
            return resp

    class _DisableAdvancedSiteSearch(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("DisableAdvancedSiteSearch")

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
                    [SiteSearchEngineService.DisableAdvancedSiteSearch][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.DisableAdvancedSiteSearch]
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{site_search_engine=projects/*/locations/*/dataStores/*/siteSearchEngine}:disableAdvancedSiteSearch",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{site_search_engine=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}:disableAdvancedSiteSearch",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_disable_advanced_site_search(
                request, metadata
            )
            pb_request = site_search_engine_service.DisableAdvancedSiteSearchRequest.pb(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_disable_advanced_site_search(resp)
            return resp

    class _EnableAdvancedSiteSearch(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("EnableAdvancedSiteSearch")

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
                    [SiteSearchEngineService.EnableAdvancedSiteSearch][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.EnableAdvancedSiteSearch]
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{site_search_engine=projects/*/locations/*/dataStores/*/siteSearchEngine}:enableAdvancedSiteSearch",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{site_search_engine=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}:enableAdvancedSiteSearch",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_enable_advanced_site_search(
                request, metadata
            )
            pb_request = site_search_engine_service.EnableAdvancedSiteSearchRequest.pb(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_enable_advanced_site_search(resp)
            return resp

    class _FetchDomainVerificationStatus(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("FetchDomainVerificationStatus")

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
                    [SiteSearchEngineService.FetchDomainVerificationStatus][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.FetchDomainVerificationStatus]
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.site_search_engine_service.FetchDomainVerificationStatusResponse:
                        Response message for
                    [SiteSearchEngineService.FetchDomainVerificationStatus][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.FetchDomainVerificationStatus]
                    method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{site_search_engine=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}:fetchDomainVerificationStatus",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_domain_verification_status(
                request, metadata
            )
            pb_request = (
                site_search_engine_service.FetchDomainVerificationStatusRequest.pb(
                    request
                )
            )
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
            resp = site_search_engine_service.FetchDomainVerificationStatusResponse()
            pb_resp = (
                site_search_engine_service.FetchDomainVerificationStatusResponse.pb(
                    resp
                )
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_domain_verification_status(resp)
            return resp

    class _GetSiteSearchEngine(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("GetSiteSearchEngine")

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
                [SiteSearchEngineService.GetSiteSearchEngine][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.GetSiteSearchEngine]
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/siteSearchEngine}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}",
                },
            ]
            request, metadata = self._interceptor.pre_get_site_search_engine(
                request, metadata
            )
            pb_request = site_search_engine_service.GetSiteSearchEngineRequest.pb(
                request
            )
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
            resp = site_search_engine.SiteSearchEngine()
            pb_resp = site_search_engine.SiteSearchEngine.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_site_search_engine(resp)
            return resp

    class _GetTargetSite(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("GetTargetSite")

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
                [SiteSearchEngineService.GetTargetSite][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.GetTargetSite]
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/siteSearchEngine/targetSites/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_target_site(request, metadata)
            pb_request = site_search_engine_service.GetTargetSiteRequest.pb(request)
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
            resp = site_search_engine.TargetSite()
            pb_resp = site_search_engine.TargetSite.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_target_site(resp)
            return resp

    class _ListTargetSites(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("ListTargetSites")

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
                [SiteSearchEngineService.ListTargetSites][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.ListTargetSites]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.site_search_engine_service.ListTargetSitesResponse:
                    Response message for
                [SiteSearchEngineService.ListTargetSites][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.ListTargetSites]
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/dataStores/*/siteSearchEngine}/targetSites",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/targetSites",
                },
            ]
            request, metadata = self._interceptor.pre_list_target_sites(
                request, metadata
            )
            pb_request = site_search_engine_service.ListTargetSitesRequest.pb(request)
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
            resp = site_search_engine_service.ListTargetSitesResponse()
            pb_resp = site_search_engine_service.ListTargetSitesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_target_sites(resp)
            return resp

    class _RecrawlUris(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("RecrawlUris")

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
                [SiteSearchEngineService.RecrawlUris][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.RecrawlUris]
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{site_search_engine=projects/*/locations/*/dataStores/*/siteSearchEngine}:recrawlUris",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{site_search_engine=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}:recrawlUris",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_recrawl_uris(request, metadata)
            pb_request = site_search_engine_service.RecrawlUrisRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_recrawl_uris(resp)
            return resp

    class _UpdateTargetSite(SiteSearchEngineServiceRestStub):
        def __hash__(self):
            return hash("UpdateTargetSite")

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
                [SiteSearchEngineService.UpdateTargetSite][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.UpdateTargetSite]
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{target_site.name=projects/*/locations/*/dataStores/*/siteSearchEngine/targetSites/*}",
                    "body": "target_site",
                },
                {
                    "method": "patch",
                    "uri": "/v1alpha/{target_site.name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/*}",
                    "body": "target_site",
                },
            ]
            request, metadata = self._interceptor.pre_update_target_site(
                request, metadata
            )
            pb_request = site_search_engine_service.UpdateTargetSiteRequest.pb(request)
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
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(SiteSearchEngineServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataConnector/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/models/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/engines/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/models/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(SiteSearchEngineServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataConnector}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/models/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/engines/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/branches/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/models/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SiteSearchEngineServiceRestTransport",)
