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
from .rest_base import _BaseRegionUrlMapsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class RegionUrlMapsRestInterceptor:
    """Interceptor for RegionUrlMaps.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegionUrlMapsRestTransport.

    .. code-block:: python
        class MyCustomRegionUrlMapsInterceptor(RegionUrlMapsRestInterceptor):
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

            def pre_update(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_validate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_validate(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RegionUrlMapsRestTransport(interceptor=MyCustomRegionUrlMapsInterceptor())
        client = RegionUrlMapsClient(transport=transport)


    """

    def pre_delete(
        self,
        request: compute.DeleteRegionUrlMapRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.DeleteRegionUrlMapRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionUrlMaps server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        Override in a subclass to manipulate the response
        after it is returned by the RegionUrlMaps server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetRegionUrlMapRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetRegionUrlMapRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionUrlMaps server.
        """
        return request, metadata

    def post_get(self, response: compute.UrlMap) -> compute.UrlMap:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the RegionUrlMaps server but before
        it is returned to user code.
        """
        return response

    def pre_insert(
        self,
        request: compute.InsertRegionUrlMapRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.InsertRegionUrlMapRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionUrlMaps server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the RegionUrlMaps server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListRegionUrlMapsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ListRegionUrlMapsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionUrlMaps server.
        """
        return request, metadata

    def post_list(self, response: compute.UrlMapList) -> compute.UrlMapList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the RegionUrlMaps server but before
        it is returned to user code.
        """
        return response

    def pre_patch(
        self,
        request: compute.PatchRegionUrlMapRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.PatchRegionUrlMapRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for patch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionUrlMaps server.
        """
        return request, metadata

    def post_patch(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch

        Override in a subclass to manipulate the response
        after it is returned by the RegionUrlMaps server but before
        it is returned to user code.
        """
        return response

    def pre_update(
        self,
        request: compute.UpdateRegionUrlMapRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.UpdateRegionUrlMapRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionUrlMaps server.
        """
        return request, metadata

    def post_update(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for update

        Override in a subclass to manipulate the response
        after it is returned by the RegionUrlMaps server but before
        it is returned to user code.
        """
        return response

    def pre_validate(
        self,
        request: compute.ValidateRegionUrlMapRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ValidateRegionUrlMapRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for validate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the RegionUrlMaps server.
        """
        return request, metadata

    def post_validate(
        self, response: compute.UrlMapsValidateResponse
    ) -> compute.UrlMapsValidateResponse:
        """Post-rpc interceptor for validate

        Override in a subclass to manipulate the response
        after it is returned by the RegionUrlMaps server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegionUrlMapsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegionUrlMapsRestInterceptor


class RegionUrlMapsRestTransport(_BaseRegionUrlMapsRestTransport):
    """REST backend synchronous transport for RegionUrlMaps.

    The RegionUrlMaps API.

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
        interceptor: Optional[RegionUrlMapsRestInterceptor] = None,
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
        self._interceptor = interceptor or RegionUrlMapsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _Delete(_BaseRegionUrlMapsRestTransport._BaseDelete, RegionUrlMapsRestStub):
        def __hash__(self):
            return hash("RegionUrlMapsRestTransport.Delete")

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
            request: compute.DeleteRegionUrlMapRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteRegionUrlMapRequest):
                    The request object. A request message for
                RegionUrlMaps.Delete. See the method
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
                _BaseRegionUrlMapsRestTransport._BaseDelete._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = (
                _BaseRegionUrlMapsRestTransport._BaseDelete._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionUrlMapsRestTransport._BaseDelete._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RegionUrlMapsRestTransport._Delete._get_response(
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

    class _Get(_BaseRegionUrlMapsRestTransport._BaseGet, RegionUrlMapsRestStub):
        def __hash__(self):
            return hash("RegionUrlMapsRestTransport.Get")

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
            request: compute.GetRegionUrlMapRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.UrlMap:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetRegionUrlMapRequest):
                    The request object. A request message for
                RegionUrlMaps.Get. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.UrlMap:
                    Represents a URL Map resource. Compute Engine has two
                URL Map resources: \*
                `Global </compute/docs/reference/rest/v1/urlMaps>`__ \*
                `Regional </compute/docs/reference/rest/v1/regionUrlMaps>`__
                A URL map resource is a component of certain types of
                cloud load balancers and Traffic Director: \* urlMaps
                are used by global external Application Load Balancers,
                classic Application Load Balancers, and cross-region
                internal Application Load Balancers. \* regionUrlMaps
                are used by internal Application Load Balancers,
                regional external Application Load Balancers and
                regional internal Application Load Balancers. For a list
                of supported URL map features by the load balancer type,
                see the Load balancing features: Routing and traffic
                management table. For a list of supported URL map
                features for Traffic Director, see the Traffic Director
                features: Routing and traffic management table. This
                resource defines mappings from hostnames and URL paths
                to either a backend service or a backend bucket. To use
                the global urlMaps resource, the backend service must
                have a loadBalancingScheme of either EXTERNAL or
                INTERNAL_SELF_MANAGED. To use the regionUrlMaps
                resource, the backend service must have a
                loadBalancingScheme of INTERNAL_MANAGED. For more
                information, read URL Map Concepts.

            """

            http_options = _BaseRegionUrlMapsRestTransport._BaseGet._get_http_options()
            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = (
                _BaseRegionUrlMapsRestTransport._BaseGet._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionUrlMapsRestTransport._BaseGet._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RegionUrlMapsRestTransport._Get._get_response(
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
            resp = compute.UrlMap()
            pb_resp = compute.UrlMap.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get(resp)
            return resp

    class _Insert(_BaseRegionUrlMapsRestTransport._BaseInsert, RegionUrlMapsRestStub):
        def __hash__(self):
            return hash("RegionUrlMapsRestTransport.Insert")

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
            request: compute.InsertRegionUrlMapRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertRegionUrlMapRequest):
                    The request object. A request message for
                RegionUrlMaps.Insert. See the method
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
                _BaseRegionUrlMapsRestTransport._BaseInsert._get_http_options()
            )
            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = (
                _BaseRegionUrlMapsRestTransport._BaseInsert._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegionUrlMapsRestTransport._BaseInsert._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionUrlMapsRestTransport._BaseInsert._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RegionUrlMapsRestTransport._Insert._get_response(
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

    class _List(_BaseRegionUrlMapsRestTransport._BaseList, RegionUrlMapsRestStub):
        def __hash__(self):
            return hash("RegionUrlMapsRestTransport.List")

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
            request: compute.ListRegionUrlMapsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.UrlMapList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListRegionUrlMapsRequest):
                    The request object. A request message for
                RegionUrlMaps.List. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.UrlMapList:
                    Contains a list of UrlMap resources.
            """

            http_options = _BaseRegionUrlMapsRestTransport._BaseList._get_http_options()
            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = (
                _BaseRegionUrlMapsRestTransport._BaseList._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionUrlMapsRestTransport._BaseList._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RegionUrlMapsRestTransport._List._get_response(
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
            resp = compute.UrlMapList()
            pb_resp = compute.UrlMapList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list(resp)
            return resp

    class _Patch(_BaseRegionUrlMapsRestTransport._BasePatch, RegionUrlMapsRestStub):
        def __hash__(self):
            return hash("RegionUrlMapsRestTransport.Patch")

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
            request: compute.PatchRegionUrlMapRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch method over HTTP.

            Args:
                request (~.compute.PatchRegionUrlMapRequest):
                    The request object. A request message for
                RegionUrlMaps.Patch. See the method
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
                _BaseRegionUrlMapsRestTransport._BasePatch._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch(request, metadata)
            transcoded_request = (
                _BaseRegionUrlMapsRestTransport._BasePatch._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegionUrlMapsRestTransport._BasePatch._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionUrlMapsRestTransport._BasePatch._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RegionUrlMapsRestTransport._Patch._get_response(
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

    class _Update(_BaseRegionUrlMapsRestTransport._BaseUpdate, RegionUrlMapsRestStub):
        def __hash__(self):
            return hash("RegionUrlMapsRestTransport.Update")

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
            request: compute.UpdateRegionUrlMapRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the update method over HTTP.

            Args:
                request (~.compute.UpdateRegionUrlMapRequest):
                    The request object. A request message for
                RegionUrlMaps.Update. See the method
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
                _BaseRegionUrlMapsRestTransport._BaseUpdate._get_http_options()
            )
            request, metadata = self._interceptor.pre_update(request, metadata)
            transcoded_request = (
                _BaseRegionUrlMapsRestTransport._BaseUpdate._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegionUrlMapsRestTransport._BaseUpdate._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionUrlMapsRestTransport._BaseUpdate._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RegionUrlMapsRestTransport._Update._get_response(
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
            resp = self._interceptor.post_update(resp)
            return resp

    class _Validate(
        _BaseRegionUrlMapsRestTransport._BaseValidate, RegionUrlMapsRestStub
    ):
        def __hash__(self):
            return hash("RegionUrlMapsRestTransport.Validate")

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
            request: compute.ValidateRegionUrlMapRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.UrlMapsValidateResponse:
            r"""Call the validate method over HTTP.

            Args:
                request (~.compute.ValidateRegionUrlMapRequest):
                    The request object. A request message for
                RegionUrlMaps.Validate. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.UrlMapsValidateResponse:

            """

            http_options = (
                _BaseRegionUrlMapsRestTransport._BaseValidate._get_http_options()
            )
            request, metadata = self._interceptor.pre_validate(request, metadata)
            transcoded_request = (
                _BaseRegionUrlMapsRestTransport._BaseValidate._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegionUrlMapsRestTransport._BaseValidate._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegionUrlMapsRestTransport._BaseValidate._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RegionUrlMapsRestTransport._Validate._get_response(
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
            resp = compute.UrlMapsValidateResponse()
            pb_resp = compute.UrlMapsValidateResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_validate(resp)
            return resp

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeleteRegionUrlMapRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(self) -> Callable[[compute.GetRegionUrlMapRequest], compute.UrlMap]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertRegionUrlMapRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(self) -> Callable[[compute.ListRegionUrlMapsRequest], compute.UrlMapList]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch(self) -> Callable[[compute.PatchRegionUrlMapRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Patch(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update(
        self,
    ) -> Callable[[compute.UpdateRegionUrlMapRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Update(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def validate(
        self,
    ) -> Callable[
        [compute.ValidateRegionUrlMapRequest], compute.UrlMapsValidateResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Validate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RegionUrlMapsRestTransport",)
