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
import google.protobuf
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.compute_v1beta.types import compute

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseGlobalNetworkEndpointGroupsRestTransport

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


class GlobalNetworkEndpointGroupsRestInterceptor:
    """Interceptor for GlobalNetworkEndpointGroups.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the GlobalNetworkEndpointGroupsRestTransport.

    .. code-block:: python
        class MyCustomGlobalNetworkEndpointGroupsInterceptor(GlobalNetworkEndpointGroupsRestInterceptor):
            def pre_attach_network_endpoints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_attach_network_endpoints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_detach_network_endpoints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_detach_network_endpoints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_insert(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_network_endpoints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_network_endpoints(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = GlobalNetworkEndpointGroupsRestTransport(interceptor=MyCustomGlobalNetworkEndpointGroupsInterceptor())
        client = GlobalNetworkEndpointGroupsClient(transport=transport)


    """

    def pre_attach_network_endpoints(
        self,
        request: compute.AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for attach_network_endpoints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GlobalNetworkEndpointGroups server.
        """
        return request, metadata

    def post_attach_network_endpoints(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for attach_network_endpoints

        DEPRECATED. Please use the `post_attach_network_endpoints_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GlobalNetworkEndpointGroups server but before
        it is returned to user code. This `post_attach_network_endpoints` interceptor runs
        before the `post_attach_network_endpoints_with_metadata` interceptor.
        """
        return response

    def post_attach_network_endpoints_with_metadata(
        self,
        response: compute.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for attach_network_endpoints

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GlobalNetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_attach_network_endpoints_with_metadata`
        interceptor in new development instead of the `post_attach_network_endpoints` interceptor.
        When both interceptors are used, this `post_attach_network_endpoints_with_metadata` interceptor runs after the
        `post_attach_network_endpoints` interceptor. The (possibly modified) response returned by
        `post_attach_network_endpoints` will be passed to
        `post_attach_network_endpoints_with_metadata`.
        """
        return response, metadata

    def pre_delete(
        self,
        request: compute.DeleteGlobalNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.DeleteGlobalNetworkEndpointGroupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GlobalNetworkEndpointGroups server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        DEPRECATED. Please use the `post_delete_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GlobalNetworkEndpointGroups server but before
        it is returned to user code. This `post_delete` interceptor runs
        before the `post_delete_with_metadata` interceptor.
        """
        return response

    def post_delete_with_metadata(
        self,
        response: compute.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GlobalNetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_delete_with_metadata`
        interceptor in new development instead of the `post_delete` interceptor.
        When both interceptors are used, this `post_delete_with_metadata` interceptor runs after the
        `post_delete` interceptor. The (possibly modified) response returned by
        `post_delete` will be passed to
        `post_delete_with_metadata`.
        """
        return response, metadata

    def pre_detach_network_endpoints(
        self,
        request: compute.DetachNetworkEndpointsGlobalNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.DetachNetworkEndpointsGlobalNetworkEndpointGroupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for detach_network_endpoints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GlobalNetworkEndpointGroups server.
        """
        return request, metadata

    def post_detach_network_endpoints(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for detach_network_endpoints

        DEPRECATED. Please use the `post_detach_network_endpoints_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GlobalNetworkEndpointGroups server but before
        it is returned to user code. This `post_detach_network_endpoints` interceptor runs
        before the `post_detach_network_endpoints_with_metadata` interceptor.
        """
        return response

    def post_detach_network_endpoints_with_metadata(
        self,
        response: compute.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for detach_network_endpoints

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GlobalNetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_detach_network_endpoints_with_metadata`
        interceptor in new development instead of the `post_detach_network_endpoints` interceptor.
        When both interceptors are used, this `post_detach_network_endpoints_with_metadata` interceptor runs after the
        `post_detach_network_endpoints` interceptor. The (possibly modified) response returned by
        `post_detach_network_endpoints` will be passed to
        `post_detach_network_endpoints_with_metadata`.
        """
        return response, metadata

    def pre_get(
        self,
        request: compute.GetGlobalNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.GetGlobalNetworkEndpointGroupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GlobalNetworkEndpointGroups server.
        """
        return request, metadata

    def post_get(
        self, response: compute.NetworkEndpointGroup
    ) -> compute.NetworkEndpointGroup:
        """Post-rpc interceptor for get

        DEPRECATED. Please use the `post_get_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GlobalNetworkEndpointGroups server but before
        it is returned to user code. This `post_get` interceptor runs
        before the `post_get_with_metadata` interceptor.
        """
        return response

    def post_get_with_metadata(
        self,
        response: compute.NetworkEndpointGroup,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.NetworkEndpointGroup, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GlobalNetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_get_with_metadata`
        interceptor in new development instead of the `post_get` interceptor.
        When both interceptors are used, this `post_get_with_metadata` interceptor runs after the
        `post_get` interceptor. The (possibly modified) response returned by
        `post_get` will be passed to
        `post_get_with_metadata`.
        """
        return response, metadata

    def pre_insert(
        self,
        request: compute.InsertGlobalNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.InsertGlobalNetworkEndpointGroupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GlobalNetworkEndpointGroups server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        DEPRECATED. Please use the `post_insert_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GlobalNetworkEndpointGroups server but before
        it is returned to user code. This `post_insert` interceptor runs
        before the `post_insert_with_metadata` interceptor.
        """
        return response

    def post_insert_with_metadata(
        self,
        response: compute.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for insert

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GlobalNetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_insert_with_metadata`
        interceptor in new development instead of the `post_insert` interceptor.
        When both interceptors are used, this `post_insert_with_metadata` interceptor runs after the
        `post_insert` interceptor. The (possibly modified) response returned by
        `post_insert` will be passed to
        `post_insert_with_metadata`.
        """
        return response, metadata

    def pre_list(
        self,
        request: compute.ListGlobalNetworkEndpointGroupsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.ListGlobalNetworkEndpointGroupsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GlobalNetworkEndpointGroups server.
        """
        return request, metadata

    def post_list(
        self, response: compute.NetworkEndpointGroupList
    ) -> compute.NetworkEndpointGroupList:
        """Post-rpc interceptor for list

        DEPRECATED. Please use the `post_list_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GlobalNetworkEndpointGroups server but before
        it is returned to user code. This `post_list` interceptor runs
        before the `post_list_with_metadata` interceptor.
        """
        return response

    def post_list_with_metadata(
        self,
        response: compute.NetworkEndpointGroupList,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.NetworkEndpointGroupList, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GlobalNetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_list_with_metadata`
        interceptor in new development instead of the `post_list` interceptor.
        When both interceptors are used, this `post_list_with_metadata` interceptor runs after the
        `post_list` interceptor. The (possibly modified) response returned by
        `post_list` will be passed to
        `post_list_with_metadata`.
        """
        return response, metadata

    def pre_list_network_endpoints(
        self,
        request: compute.ListNetworkEndpointsGlobalNetworkEndpointGroupsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.ListNetworkEndpointsGlobalNetworkEndpointGroupsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_network_endpoints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GlobalNetworkEndpointGroups server.
        """
        return request, metadata

    def post_list_network_endpoints(
        self, response: compute.NetworkEndpointGroupsListNetworkEndpoints
    ) -> compute.NetworkEndpointGroupsListNetworkEndpoints:
        """Post-rpc interceptor for list_network_endpoints

        DEPRECATED. Please use the `post_list_network_endpoints_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the GlobalNetworkEndpointGroups server but before
        it is returned to user code. This `post_list_network_endpoints` interceptor runs
        before the `post_list_network_endpoints_with_metadata` interceptor.
        """
        return response

    def post_list_network_endpoints_with_metadata(
        self,
        response: compute.NetworkEndpointGroupsListNetworkEndpoints,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.NetworkEndpointGroupsListNetworkEndpoints,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_network_endpoints

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the GlobalNetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_list_network_endpoints_with_metadata`
        interceptor in new development instead of the `post_list_network_endpoints` interceptor.
        When both interceptors are used, this `post_list_network_endpoints_with_metadata` interceptor runs after the
        `post_list_network_endpoints` interceptor. The (possibly modified) response returned by
        `post_list_network_endpoints` will be passed to
        `post_list_network_endpoints_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class GlobalNetworkEndpointGroupsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: GlobalNetworkEndpointGroupsRestInterceptor


class GlobalNetworkEndpointGroupsRestTransport(
    _BaseGlobalNetworkEndpointGroupsRestTransport
):
    """REST backend synchronous transport for GlobalNetworkEndpointGroups.

    The GlobalNetworkEndpointGroups API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[GlobalNetworkEndpointGroupsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to (default: 'compute.googleapis.com').
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
        self._interceptor = interceptor or GlobalNetworkEndpointGroupsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AttachNetworkEndpoints(
        _BaseGlobalNetworkEndpointGroupsRestTransport._BaseAttachNetworkEndpoints,
        GlobalNetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash(
                "GlobalNetworkEndpointGroupsRestTransport.AttachNetworkEndpoints"
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
            request: compute.AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the attach network endpoints method over HTTP.

            Args:
                request (~.compute.AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest):
                    The request object. A request message for
                GlobalNetworkEndpointGroups.AttachNetworkEndpoints.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/beta/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/beta/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/beta/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseGlobalNetworkEndpointGroupsRestTransport._BaseAttachNetworkEndpoints._get_http_options()
            )

            request, metadata = self._interceptor.pre_attach_network_endpoints(
                request, metadata
            )
            transcoded_request = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseAttachNetworkEndpoints._get_transcoded_request(
                http_options, request
            )

            body = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseAttachNetworkEndpoints._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseAttachNetworkEndpoints._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.AttachNetworkEndpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "AttachNetworkEndpoints",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GlobalNetworkEndpointGroupsRestTransport._AttachNetworkEndpoints._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_attach_network_endpoints(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_attach_network_endpoints_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.attach_network_endpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "AttachNetworkEndpoints",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Delete(
        _BaseGlobalNetworkEndpointGroupsRestTransport._BaseDelete,
        GlobalNetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("GlobalNetworkEndpointGroupsRestTransport.Delete")

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
            request: compute.DeleteGlobalNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteGlobalNetworkEndpointGroupRequest):
                    The request object. A request message for
                GlobalNetworkEndpointGroups.Delete. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/beta/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/beta/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/beta/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseGlobalNetworkEndpointGroupsRestTransport._BaseDelete._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseDelete._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseDelete._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.Delete",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "Delete",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GlobalNetworkEndpointGroupsRestTransport._Delete._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.delete",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "Delete",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DetachNetworkEndpoints(
        _BaseGlobalNetworkEndpointGroupsRestTransport._BaseDetachNetworkEndpoints,
        GlobalNetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash(
                "GlobalNetworkEndpointGroupsRestTransport.DetachNetworkEndpoints"
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
            request: compute.DetachNetworkEndpointsGlobalNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the detach network endpoints method over HTTP.

            Args:
                request (~.compute.DetachNetworkEndpointsGlobalNetworkEndpointGroupRequest):
                    The request object. A request message for
                GlobalNetworkEndpointGroups.DetachNetworkEndpoints.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/beta/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/beta/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/beta/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseGlobalNetworkEndpointGroupsRestTransport._BaseDetachNetworkEndpoints._get_http_options()
            )

            request, metadata = self._interceptor.pre_detach_network_endpoints(
                request, metadata
            )
            transcoded_request = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseDetachNetworkEndpoints._get_transcoded_request(
                http_options, request
            )

            body = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseDetachNetworkEndpoints._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseDetachNetworkEndpoints._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.DetachNetworkEndpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "DetachNetworkEndpoints",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GlobalNetworkEndpointGroupsRestTransport._DetachNetworkEndpoints._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_detach_network_endpoints(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_detach_network_endpoints_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.detach_network_endpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "DetachNetworkEndpoints",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Get(
        _BaseGlobalNetworkEndpointGroupsRestTransport._BaseGet,
        GlobalNetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("GlobalNetworkEndpointGroupsRestTransport.Get")

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
            request: compute.GetGlobalNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.NetworkEndpointGroup:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetGlobalNetworkEndpointGroupRequest):
                    The request object. A request message for
                GlobalNetworkEndpointGroups.Get. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.NetworkEndpointGroup:
                    Represents a collection of network
                endpoints. A network endpoint group
                (NEG) defines how a set of endpoints
                should be reached, whether they are
                reachable, and where they are located.
                For more information about using NEGs
                for different use cases, see Network
                endpoint groups overview.

            """

            http_options = (
                _BaseGlobalNetworkEndpointGroupsRestTransport._BaseGet._get_http_options()
            )

            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseGet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseGet._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.Get",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "Get",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GlobalNetworkEndpointGroupsRestTransport._Get._get_response(
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
            resp = compute.NetworkEndpointGroup()
            pb_resp = compute.NetworkEndpointGroup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.NetworkEndpointGroup.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.get",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "Get",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Insert(
        _BaseGlobalNetworkEndpointGroupsRestTransport._BaseInsert,
        GlobalNetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("GlobalNetworkEndpointGroupsRestTransport.Insert")

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
            request: compute.InsertGlobalNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertGlobalNetworkEndpointGroupRequest):
                    The request object. A request message for
                GlobalNetworkEndpointGroups.Insert. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/beta/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/beta/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/beta/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseGlobalNetworkEndpointGroupsRestTransport._BaseInsert._get_http_options()
            )

            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseInsert._get_transcoded_request(
                http_options, request
            )

            body = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseInsert._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseInsert._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.Insert",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "Insert",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GlobalNetworkEndpointGroupsRestTransport._Insert._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_insert(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_insert_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.insert",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "Insert",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _List(
        _BaseGlobalNetworkEndpointGroupsRestTransport._BaseList,
        GlobalNetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("GlobalNetworkEndpointGroupsRestTransport.List")

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
            request: compute.ListGlobalNetworkEndpointGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.NetworkEndpointGroupList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListGlobalNetworkEndpointGroupsRequest):
                    The request object. A request message for
                GlobalNetworkEndpointGroups.List. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.NetworkEndpointGroupList:

            """

            http_options = (
                _BaseGlobalNetworkEndpointGroupsRestTransport._BaseList._get_http_options()
            )

            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseList._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.List",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "List",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GlobalNetworkEndpointGroupsRestTransport._List._get_response(
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
            resp = compute.NetworkEndpointGroupList()
            pb_resp = compute.NetworkEndpointGroupList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.NetworkEndpointGroupList.to_json(
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
                    "Received response for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.list",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "List",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListNetworkEndpoints(
        _BaseGlobalNetworkEndpointGroupsRestTransport._BaseListNetworkEndpoints,
        GlobalNetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("GlobalNetworkEndpointGroupsRestTransport.ListNetworkEndpoints")

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
            request: compute.ListNetworkEndpointsGlobalNetworkEndpointGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.NetworkEndpointGroupsListNetworkEndpoints:
            r"""Call the list network endpoints method over HTTP.

            Args:
                request (~.compute.ListNetworkEndpointsGlobalNetworkEndpointGroupsRequest):
                    The request object. A request message for
                GlobalNetworkEndpointGroups.ListNetworkEndpoints.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.NetworkEndpointGroupsListNetworkEndpoints:

            """

            http_options = (
                _BaseGlobalNetworkEndpointGroupsRestTransport._BaseListNetworkEndpoints._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_network_endpoints(
                request, metadata
            )
            transcoded_request = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseListNetworkEndpoints._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseGlobalNetworkEndpointGroupsRestTransport._BaseListNetworkEndpoints._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.ListNetworkEndpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "ListNetworkEndpoints",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = GlobalNetworkEndpointGroupsRestTransport._ListNetworkEndpoints._get_response(
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
            resp = compute.NetworkEndpointGroupsListNetworkEndpoints()
            pb_resp = compute.NetworkEndpointGroupsListNetworkEndpoints.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_network_endpoints(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_network_endpoints_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        compute.NetworkEndpointGroupsListNetworkEndpoints.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.GlobalNetworkEndpointGroupsClient.list_network_endpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.GlobalNetworkEndpointGroups",
                        "rpcName": "ListNetworkEndpoints",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def attach_network_endpoints(
        self,
    ) -> Callable[
        [compute.AttachNetworkEndpointsGlobalNetworkEndpointGroupRequest],
        compute.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AttachNetworkEndpoints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeleteGlobalNetworkEndpointGroupRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def detach_network_endpoints(
        self,
    ) -> Callable[
        [compute.DetachNetworkEndpointsGlobalNetworkEndpointGroupRequest],
        compute.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DetachNetworkEndpoints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetGlobalNetworkEndpointGroupRequest], compute.NetworkEndpointGroup
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertGlobalNetworkEndpointGroupRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListGlobalNetworkEndpointGroupsRequest],
        compute.NetworkEndpointGroupList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_network_endpoints(
        self,
    ) -> Callable[
        [compute.ListNetworkEndpointsGlobalNetworkEndpointGroupsRequest],
        compute.NetworkEndpointGroupsListNetworkEndpoints,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNetworkEndpoints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("GlobalNetworkEndpointGroupsRestTransport",)
