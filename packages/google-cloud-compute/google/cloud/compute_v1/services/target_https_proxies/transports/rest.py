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

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.compute_v1.types import compute

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseTargetHttpsProxiesRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class TargetHttpsProxiesRestInterceptor:
    """Interceptor for TargetHttpsProxies.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the TargetHttpsProxiesRestTransport.

    .. code-block:: python
        class MyCustomTargetHttpsProxiesInterceptor(TargetHttpsProxiesRestInterceptor):
            def pre_aggregated_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregated_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete(self, response):
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

            def pre_patch(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_patch(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_certificate_map(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_certificate_map(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_quic_override(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_quic_override(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_ssl_certificates(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_ssl_certificates(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_ssl_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_ssl_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_url_map(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_url_map(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = TargetHttpsProxiesRestTransport(interceptor=MyCustomTargetHttpsProxiesInterceptor())
        client = TargetHttpsProxiesClient(transport=transport)


    """

    def pre_aggregated_list(
        self,
        request: compute.AggregatedListTargetHttpsProxiesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AggregatedListTargetHttpsProxiesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_aggregated_list(
        self, response: compute.TargetHttpsProxyAggregatedList
    ) -> compute.TargetHttpsProxyAggregatedList:
        """Post-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response

    def pre_delete(
        self,
        request: compute.DeleteTargetHttpsProxyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.DeleteTargetHttpsProxyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetTargetHttpsProxyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetTargetHttpsProxyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_get(self, response: compute.TargetHttpsProxy) -> compute.TargetHttpsProxy:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response

    def pre_insert(
        self,
        request: compute.InsertTargetHttpsProxyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.InsertTargetHttpsProxyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListTargetHttpsProxiesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ListTargetHttpsProxiesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_list(
        self, response: compute.TargetHttpsProxyList
    ) -> compute.TargetHttpsProxyList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response

    def pre_patch(
        self,
        request: compute.PatchTargetHttpsProxyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.PatchTargetHttpsProxyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for patch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_patch(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response

    def pre_set_certificate_map(
        self,
        request: compute.SetCertificateMapTargetHttpsProxyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.SetCertificateMapTargetHttpsProxyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for set_certificate_map

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_set_certificate_map(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for set_certificate_map

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response

    def pre_set_quic_override(
        self,
        request: compute.SetQuicOverrideTargetHttpsProxyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.SetQuicOverrideTargetHttpsProxyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for set_quic_override

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_set_quic_override(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for set_quic_override

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response

    def pre_set_ssl_certificates(
        self,
        request: compute.SetSslCertificatesTargetHttpsProxyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.SetSslCertificatesTargetHttpsProxyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for set_ssl_certificates

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_set_ssl_certificates(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for set_ssl_certificates

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response

    def pre_set_ssl_policy(
        self,
        request: compute.SetSslPolicyTargetHttpsProxyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.SetSslPolicyTargetHttpsProxyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_ssl_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_set_ssl_policy(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for set_ssl_policy

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response

    def pre_set_url_map(
        self,
        request: compute.SetUrlMapTargetHttpsProxyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.SetUrlMapTargetHttpsProxyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_url_map

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TargetHttpsProxies server.
        """
        return request, metadata

    def post_set_url_map(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for set_url_map

        Override in a subclass to manipulate the response
        after it is returned by the TargetHttpsProxies server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class TargetHttpsProxiesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: TargetHttpsProxiesRestInterceptor


class TargetHttpsProxiesRestTransport(_BaseTargetHttpsProxiesRestTransport):
    """REST backend synchronous transport for TargetHttpsProxies.

    The TargetHttpsProxies API.

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
        interceptor: Optional[TargetHttpsProxiesRestInterceptor] = None,
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
        self._interceptor = interceptor or TargetHttpsProxiesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AggregatedList(
        _BaseTargetHttpsProxiesRestTransport._BaseAggregatedList,
        TargetHttpsProxiesRestStub,
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.AggregatedList")

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
            request: compute.AggregatedListTargetHttpsProxiesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.TargetHttpsProxyAggregatedList:
            r"""Call the aggregated list method over HTTP.

            Args:
                request (~.compute.AggregatedListTargetHttpsProxiesRequest):
                    The request object. A request message for
                TargetHttpsProxies.AggregatedList. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TargetHttpsProxyAggregatedList:

            """

            http_options = (
                _BaseTargetHttpsProxiesRestTransport._BaseAggregatedList._get_http_options()
            )
            request, metadata = self._interceptor.pre_aggregated_list(request, metadata)
            transcoded_request = _BaseTargetHttpsProxiesRestTransport._BaseAggregatedList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseTargetHttpsProxiesRestTransport._BaseAggregatedList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = TargetHttpsProxiesRestTransport._AggregatedList._get_response(
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
            resp = compute.TargetHttpsProxyAggregatedList()
            pb_resp = compute.TargetHttpsProxyAggregatedList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_aggregated_list(resp)
            return resp

    class _Delete(
        _BaseTargetHttpsProxiesRestTransport._BaseDelete, TargetHttpsProxiesRestStub
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.Delete")

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
            request: compute.DeleteTargetHttpsProxyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteTargetHttpsProxyRequest):
                    The request object. A request message for
                TargetHttpsProxies.Delete. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
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
                _BaseTargetHttpsProxiesRestTransport._BaseDelete._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = _BaseTargetHttpsProxiesRestTransport._BaseDelete._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseTargetHttpsProxiesRestTransport._BaseDelete._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = TargetHttpsProxiesRestTransport._Delete._get_response(
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
            return resp

    class _Get(
        _BaseTargetHttpsProxiesRestTransport._BaseGet, TargetHttpsProxiesRestStub
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.Get")

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
            request: compute.GetTargetHttpsProxyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.TargetHttpsProxy:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetTargetHttpsProxyRequest):
                    The request object. A request message for
                TargetHttpsProxies.Get. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TargetHttpsProxy:
                    Represents a Target HTTPS Proxy resource. Google Compute
                Engine has two Target HTTPS Proxy resources: \*
                `Global </compute/docs/reference/rest/v1/targetHttpsProxies>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionTargetHttpsProxies>`__
                A target HTTPS proxy is a component of GCP HTTPS load
                balancers. \* targetHttpProxies are used by global
                external Application Load Balancers, classic Application
                Load Balancers, cross-region internal Application Load
                Balancers, and Traffic Director. \*
                regionTargetHttpProxies are used by regional internal
                Application Load Balancers and regional external
                Application Load Balancers. Forwarding rules reference a
                target HTTPS proxy, and the target proxy then references
                a URL map. For more information, read Using Target
                Proxies and Forwarding rule concepts.

            """

            http_options = (
                _BaseTargetHttpsProxiesRestTransport._BaseGet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = (
                _BaseTargetHttpsProxiesRestTransport._BaseGet._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTargetHttpsProxiesRestTransport._BaseGet._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = TargetHttpsProxiesRestTransport._Get._get_response(
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
            resp = compute.TargetHttpsProxy()
            pb_resp = compute.TargetHttpsProxy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get(resp)
            return resp

    class _Insert(
        _BaseTargetHttpsProxiesRestTransport._BaseInsert, TargetHttpsProxiesRestStub
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.Insert")

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
            request: compute.InsertTargetHttpsProxyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertTargetHttpsProxyRequest):
                    The request object. A request message for
                TargetHttpsProxies.Insert. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
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
                _BaseTargetHttpsProxiesRestTransport._BaseInsert._get_http_options()
            )
            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = _BaseTargetHttpsProxiesRestTransport._BaseInsert._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseTargetHttpsProxiesRestTransport._BaseInsert._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTargetHttpsProxiesRestTransport._BaseInsert._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = TargetHttpsProxiesRestTransport._Insert._get_response(
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
            return resp

    class _List(
        _BaseTargetHttpsProxiesRestTransport._BaseList, TargetHttpsProxiesRestStub
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.List")

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
            request: compute.ListTargetHttpsProxiesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.TargetHttpsProxyList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListTargetHttpsProxiesRequest):
                    The request object. A request message for
                TargetHttpsProxies.List. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TargetHttpsProxyList:
                    Contains a list of TargetHttpsProxy
                resources.

            """

            http_options = (
                _BaseTargetHttpsProxiesRestTransport._BaseList._get_http_options()
            )
            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = (
                _BaseTargetHttpsProxiesRestTransport._BaseList._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTargetHttpsProxiesRestTransport._BaseList._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = TargetHttpsProxiesRestTransport._List._get_response(
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
            resp = compute.TargetHttpsProxyList()
            pb_resp = compute.TargetHttpsProxyList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list(resp)
            return resp

    class _Patch(
        _BaseTargetHttpsProxiesRestTransport._BasePatch, TargetHttpsProxiesRestStub
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.Patch")

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
            request: compute.PatchTargetHttpsProxyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch method over HTTP.

            Args:
                request (~.compute.PatchTargetHttpsProxyRequest):
                    The request object. A request message for
                TargetHttpsProxies.Patch. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
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
                _BaseTargetHttpsProxiesRestTransport._BasePatch._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch(request, metadata)
            transcoded_request = (
                _BaseTargetHttpsProxiesRestTransport._BasePatch._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseTargetHttpsProxiesRestTransport._BasePatch._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseTargetHttpsProxiesRestTransport._BasePatch._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = TargetHttpsProxiesRestTransport._Patch._get_response(
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
            resp = self._interceptor.post_patch(resp)
            return resp

    class _SetCertificateMap(
        _BaseTargetHttpsProxiesRestTransport._BaseSetCertificateMap,
        TargetHttpsProxiesRestStub,
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.SetCertificateMap")

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
            request: compute.SetCertificateMapTargetHttpsProxyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set certificate map method over HTTP.

            Args:
                request (~.compute.SetCertificateMapTargetHttpsProxyRequest):
                    The request object. A request message for
                TargetHttpsProxies.SetCertificateMap.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
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
                _BaseTargetHttpsProxiesRestTransport._BaseSetCertificateMap._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_certificate_map(
                request, metadata
            )
            transcoded_request = _BaseTargetHttpsProxiesRestTransport._BaseSetCertificateMap._get_transcoded_request(
                http_options, request
            )

            body = _BaseTargetHttpsProxiesRestTransport._BaseSetCertificateMap._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseTargetHttpsProxiesRestTransport._BaseSetCertificateMap._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = TargetHttpsProxiesRestTransport._SetCertificateMap._get_response(
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
            resp = self._interceptor.post_set_certificate_map(resp)
            return resp

    class _SetQuicOverride(
        _BaseTargetHttpsProxiesRestTransport._BaseSetQuicOverride,
        TargetHttpsProxiesRestStub,
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.SetQuicOverride")

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
            request: compute.SetQuicOverrideTargetHttpsProxyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set quic override method over HTTP.

            Args:
                request (~.compute.SetQuicOverrideTargetHttpsProxyRequest):
                    The request object. A request message for
                TargetHttpsProxies.SetQuicOverride. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
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
                _BaseTargetHttpsProxiesRestTransport._BaseSetQuicOverride._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_quic_override(
                request, metadata
            )
            transcoded_request = _BaseTargetHttpsProxiesRestTransport._BaseSetQuicOverride._get_transcoded_request(
                http_options, request
            )

            body = _BaseTargetHttpsProxiesRestTransport._BaseSetQuicOverride._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseTargetHttpsProxiesRestTransport._BaseSetQuicOverride._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = TargetHttpsProxiesRestTransport._SetQuicOverride._get_response(
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
            resp = self._interceptor.post_set_quic_override(resp)
            return resp

    class _SetSslCertificates(
        _BaseTargetHttpsProxiesRestTransport._BaseSetSslCertificates,
        TargetHttpsProxiesRestStub,
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.SetSslCertificates")

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
            request: compute.SetSslCertificatesTargetHttpsProxyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set ssl certificates method over HTTP.

            Args:
                request (~.compute.SetSslCertificatesTargetHttpsProxyRequest):
                    The request object. A request message for
                TargetHttpsProxies.SetSslCertificates.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
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
                _BaseTargetHttpsProxiesRestTransport._BaseSetSslCertificates._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_ssl_certificates(
                request, metadata
            )
            transcoded_request = _BaseTargetHttpsProxiesRestTransport._BaseSetSslCertificates._get_transcoded_request(
                http_options, request
            )

            body = _BaseTargetHttpsProxiesRestTransport._BaseSetSslCertificates._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseTargetHttpsProxiesRestTransport._BaseSetSslCertificates._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                TargetHttpsProxiesRestTransport._SetSslCertificates._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_ssl_certificates(resp)
            return resp

    class _SetSslPolicy(
        _BaseTargetHttpsProxiesRestTransport._BaseSetSslPolicy,
        TargetHttpsProxiesRestStub,
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.SetSslPolicy")

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
            request: compute.SetSslPolicyTargetHttpsProxyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set ssl policy method over HTTP.

            Args:
                request (~.compute.SetSslPolicyTargetHttpsProxyRequest):
                    The request object. A request message for
                TargetHttpsProxies.SetSslPolicy. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
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
                _BaseTargetHttpsProxiesRestTransport._BaseSetSslPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_ssl_policy(request, metadata)
            transcoded_request = _BaseTargetHttpsProxiesRestTransport._BaseSetSslPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseTargetHttpsProxiesRestTransport._BaseSetSslPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseTargetHttpsProxiesRestTransport._BaseSetSslPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = TargetHttpsProxiesRestTransport._SetSslPolicy._get_response(
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
            resp = self._interceptor.post_set_ssl_policy(resp)
            return resp

    class _SetUrlMap(
        _BaseTargetHttpsProxiesRestTransport._BaseSetUrlMap, TargetHttpsProxiesRestStub
    ):
        def __hash__(self):
            return hash("TargetHttpsProxiesRestTransport.SetUrlMap")

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
            request: compute.SetUrlMapTargetHttpsProxyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the set url map method over HTTP.

            Args:
                request (~.compute.SetUrlMapTargetHttpsProxyRequest):
                    The request object. A request message for
                TargetHttpsProxies.SetUrlMap. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
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
                _BaseTargetHttpsProxiesRestTransport._BaseSetUrlMap._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_url_map(request, metadata)
            transcoded_request = _BaseTargetHttpsProxiesRestTransport._BaseSetUrlMap._get_transcoded_request(
                http_options, request
            )

            body = _BaseTargetHttpsProxiesRestTransport._BaseSetUrlMap._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseTargetHttpsProxiesRestTransport._BaseSetUrlMap._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = TargetHttpsProxiesRestTransport._SetUrlMap._get_response(
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
            resp = self._interceptor.post_set_url_map(resp)
            return resp

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListTargetHttpsProxiesRequest],
        compute.TargetHttpsProxyAggregatedList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AggregatedList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeleteTargetHttpsProxyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[[compute.GetTargetHttpsProxyRequest], compute.TargetHttpsProxy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertTargetHttpsProxyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListTargetHttpsProxiesRequest], compute.TargetHttpsProxyList
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch(
        self,
    ) -> Callable[[compute.PatchTargetHttpsProxyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Patch(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_certificate_map(
        self,
    ) -> Callable[
        [compute.SetCertificateMapTargetHttpsProxyRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetCertificateMap(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_quic_override(
        self,
    ) -> Callable[[compute.SetQuicOverrideTargetHttpsProxyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetQuicOverride(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_ssl_certificates(
        self,
    ) -> Callable[
        [compute.SetSslCertificatesTargetHttpsProxyRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetSslCertificates(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_ssl_policy(
        self,
    ) -> Callable[[compute.SetSslPolicyTargetHttpsProxyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetSslPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_url_map(
        self,
    ) -> Callable[[compute.SetUrlMapTargetHttpsProxyRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetUrlMap(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("TargetHttpsProxiesRestTransport",)
