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
from .rest_base import _BasePublicDelegatedPrefixesRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class PublicDelegatedPrefixesRestInterceptor:
    """Interceptor for PublicDelegatedPrefixes.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the PublicDelegatedPrefixesRestTransport.

    .. code-block:: python
        class MyCustomPublicDelegatedPrefixesInterceptor(PublicDelegatedPrefixesRestInterceptor):
            def pre_aggregated_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregated_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_announce(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_announce(self, response):
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

            def pre_withdraw(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_withdraw(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = PublicDelegatedPrefixesRestTransport(interceptor=MyCustomPublicDelegatedPrefixesInterceptor())
        client = PublicDelegatedPrefixesClient(transport=transport)


    """

    def pre_aggregated_list(
        self,
        request: compute.AggregatedListPublicDelegatedPrefixesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AggregatedListPublicDelegatedPrefixesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PublicDelegatedPrefixes server.
        """
        return request, metadata

    def post_aggregated_list(
        self, response: compute.PublicDelegatedPrefixAggregatedList
    ) -> compute.PublicDelegatedPrefixAggregatedList:
        """Post-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the response
        after it is returned by the PublicDelegatedPrefixes server but before
        it is returned to user code.
        """
        return response

    def pre_announce(
        self,
        request: compute.AnnouncePublicDelegatedPrefixeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AnnouncePublicDelegatedPrefixeRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for announce

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PublicDelegatedPrefixes server.
        """
        return request, metadata

    def post_announce(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for announce

        Override in a subclass to manipulate the response
        after it is returned by the PublicDelegatedPrefixes server but before
        it is returned to user code.
        """
        return response

    def pre_delete(
        self,
        request: compute.DeletePublicDelegatedPrefixeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.DeletePublicDelegatedPrefixeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PublicDelegatedPrefixes server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        Override in a subclass to manipulate the response
        after it is returned by the PublicDelegatedPrefixes server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetPublicDelegatedPrefixeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetPublicDelegatedPrefixeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PublicDelegatedPrefixes server.
        """
        return request, metadata

    def post_get(
        self, response: compute.PublicDelegatedPrefix
    ) -> compute.PublicDelegatedPrefix:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the PublicDelegatedPrefixes server but before
        it is returned to user code.
        """
        return response

    def pre_insert(
        self,
        request: compute.InsertPublicDelegatedPrefixeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.InsertPublicDelegatedPrefixeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PublicDelegatedPrefixes server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        Override in a subclass to manipulate the response
        after it is returned by the PublicDelegatedPrefixes server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListPublicDelegatedPrefixesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ListPublicDelegatedPrefixesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PublicDelegatedPrefixes server.
        """
        return request, metadata

    def post_list(
        self, response: compute.PublicDelegatedPrefixList
    ) -> compute.PublicDelegatedPrefixList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the PublicDelegatedPrefixes server but before
        it is returned to user code.
        """
        return response

    def pre_patch(
        self,
        request: compute.PatchPublicDelegatedPrefixeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.PatchPublicDelegatedPrefixeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for patch

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PublicDelegatedPrefixes server.
        """
        return request, metadata

    def post_patch(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for patch

        Override in a subclass to manipulate the response
        after it is returned by the PublicDelegatedPrefixes server but before
        it is returned to user code.
        """
        return response

    def pre_withdraw(
        self,
        request: compute.WithdrawPublicDelegatedPrefixeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.WithdrawPublicDelegatedPrefixeRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for withdraw

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PublicDelegatedPrefixes server.
        """
        return request, metadata

    def post_withdraw(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for withdraw

        Override in a subclass to manipulate the response
        after it is returned by the PublicDelegatedPrefixes server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class PublicDelegatedPrefixesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: PublicDelegatedPrefixesRestInterceptor


class PublicDelegatedPrefixesRestTransport(_BasePublicDelegatedPrefixesRestTransport):
    """REST backend synchronous transport for PublicDelegatedPrefixes.

    The PublicDelegatedPrefixes API.

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
        interceptor: Optional[PublicDelegatedPrefixesRestInterceptor] = None,
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
        self._interceptor = interceptor or PublicDelegatedPrefixesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AggregatedList(
        _BasePublicDelegatedPrefixesRestTransport._BaseAggregatedList,
        PublicDelegatedPrefixesRestStub,
    ):
        def __hash__(self):
            return hash("PublicDelegatedPrefixesRestTransport.AggregatedList")

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
            request: compute.AggregatedListPublicDelegatedPrefixesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.PublicDelegatedPrefixAggregatedList:
            r"""Call the aggregated list method over HTTP.

            Args:
                request (~.compute.AggregatedListPublicDelegatedPrefixesRequest):
                    The request object. A request message for
                PublicDelegatedPrefixes.AggregatedList.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.PublicDelegatedPrefixAggregatedList:

            """

            http_options = (
                _BasePublicDelegatedPrefixesRestTransport._BaseAggregatedList._get_http_options()
            )
            request, metadata = self._interceptor.pre_aggregated_list(request, metadata)
            transcoded_request = _BasePublicDelegatedPrefixesRestTransport._BaseAggregatedList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePublicDelegatedPrefixesRestTransport._BaseAggregatedList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                PublicDelegatedPrefixesRestTransport._AggregatedList._get_response(
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
            resp = compute.PublicDelegatedPrefixAggregatedList()
            pb_resp = compute.PublicDelegatedPrefixAggregatedList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_aggregated_list(resp)
            return resp

    class _Announce(
        _BasePublicDelegatedPrefixesRestTransport._BaseAnnounce,
        PublicDelegatedPrefixesRestStub,
    ):
        def __hash__(self):
            return hash("PublicDelegatedPrefixesRestTransport.Announce")

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
            request: compute.AnnouncePublicDelegatedPrefixeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the announce method over HTTP.

            Args:
                request (~.compute.AnnouncePublicDelegatedPrefixeRequest):
                    The request object. A request message for
                PublicDelegatedPrefixes.Announce. See
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
                _BasePublicDelegatedPrefixesRestTransport._BaseAnnounce._get_http_options()
            )
            request, metadata = self._interceptor.pre_announce(request, metadata)
            transcoded_request = _BasePublicDelegatedPrefixesRestTransport._BaseAnnounce._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePublicDelegatedPrefixesRestTransport._BaseAnnounce._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PublicDelegatedPrefixesRestTransport._Announce._get_response(
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
            resp = self._interceptor.post_announce(resp)
            return resp

    class _Delete(
        _BasePublicDelegatedPrefixesRestTransport._BaseDelete,
        PublicDelegatedPrefixesRestStub,
    ):
        def __hash__(self):
            return hash("PublicDelegatedPrefixesRestTransport.Delete")

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
            request: compute.DeletePublicDelegatedPrefixeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeletePublicDelegatedPrefixeRequest):
                    The request object. A request message for
                PublicDelegatedPrefixes.Delete. See the
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
                _BasePublicDelegatedPrefixesRestTransport._BaseDelete._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = _BasePublicDelegatedPrefixesRestTransport._BaseDelete._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePublicDelegatedPrefixesRestTransport._BaseDelete._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PublicDelegatedPrefixesRestTransport._Delete._get_response(
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
        _BasePublicDelegatedPrefixesRestTransport._BaseGet,
        PublicDelegatedPrefixesRestStub,
    ):
        def __hash__(self):
            return hash("PublicDelegatedPrefixesRestTransport.Get")

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
            request: compute.GetPublicDelegatedPrefixeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.PublicDelegatedPrefix:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetPublicDelegatedPrefixeRequest):
                    The request object. A request message for
                PublicDelegatedPrefixes.Get. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.PublicDelegatedPrefix:
                    A PublicDelegatedPrefix resource
                represents an IP block within a
                PublicAdvertisedPrefix that is
                configured within a single cloud scope
                (global or region). IPs in the block can
                be allocated to resources within that
                scope. Public delegated prefixes may be
                further broken up into smaller IP blocks
                in the same scope as the parent block.

            """

            http_options = (
                _BasePublicDelegatedPrefixesRestTransport._BaseGet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = _BasePublicDelegatedPrefixesRestTransport._BaseGet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePublicDelegatedPrefixesRestTransport._BaseGet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PublicDelegatedPrefixesRestTransport._Get._get_response(
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
            resp = compute.PublicDelegatedPrefix()
            pb_resp = compute.PublicDelegatedPrefix.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get(resp)
            return resp

    class _Insert(
        _BasePublicDelegatedPrefixesRestTransport._BaseInsert,
        PublicDelegatedPrefixesRestStub,
    ):
        def __hash__(self):
            return hash("PublicDelegatedPrefixesRestTransport.Insert")

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
            request: compute.InsertPublicDelegatedPrefixeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertPublicDelegatedPrefixeRequest):
                    The request object. A request message for
                PublicDelegatedPrefixes.Insert. See the
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
                _BasePublicDelegatedPrefixesRestTransport._BaseInsert._get_http_options()
            )
            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = _BasePublicDelegatedPrefixesRestTransport._BaseInsert._get_transcoded_request(
                http_options, request
            )

            body = _BasePublicDelegatedPrefixesRestTransport._BaseInsert._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BasePublicDelegatedPrefixesRestTransport._BaseInsert._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PublicDelegatedPrefixesRestTransport._Insert._get_response(
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
        _BasePublicDelegatedPrefixesRestTransport._BaseList,
        PublicDelegatedPrefixesRestStub,
    ):
        def __hash__(self):
            return hash("PublicDelegatedPrefixesRestTransport.List")

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
            request: compute.ListPublicDelegatedPrefixesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.PublicDelegatedPrefixList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListPublicDelegatedPrefixesRequest):
                    The request object. A request message for
                PublicDelegatedPrefixes.List. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.PublicDelegatedPrefixList:

            """

            http_options = (
                _BasePublicDelegatedPrefixesRestTransport._BaseList._get_http_options()
            )
            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = _BasePublicDelegatedPrefixesRestTransport._BaseList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePublicDelegatedPrefixesRestTransport._BaseList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PublicDelegatedPrefixesRestTransport._List._get_response(
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
            resp = compute.PublicDelegatedPrefixList()
            pb_resp = compute.PublicDelegatedPrefixList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list(resp)
            return resp

    class _Patch(
        _BasePublicDelegatedPrefixesRestTransport._BasePatch,
        PublicDelegatedPrefixesRestStub,
    ):
        def __hash__(self):
            return hash("PublicDelegatedPrefixesRestTransport.Patch")

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
            request: compute.PatchPublicDelegatedPrefixeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the patch method over HTTP.

            Args:
                request (~.compute.PatchPublicDelegatedPrefixeRequest):
                    The request object. A request message for
                PublicDelegatedPrefixes.Patch. See the
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
                _BasePublicDelegatedPrefixesRestTransport._BasePatch._get_http_options()
            )
            request, metadata = self._interceptor.pre_patch(request, metadata)
            transcoded_request = _BasePublicDelegatedPrefixesRestTransport._BasePatch._get_transcoded_request(
                http_options, request
            )

            body = _BasePublicDelegatedPrefixesRestTransport._BasePatch._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BasePublicDelegatedPrefixesRestTransport._BasePatch._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PublicDelegatedPrefixesRestTransport._Patch._get_response(
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

    class _Withdraw(
        _BasePublicDelegatedPrefixesRestTransport._BaseWithdraw,
        PublicDelegatedPrefixesRestStub,
    ):
        def __hash__(self):
            return hash("PublicDelegatedPrefixesRestTransport.Withdraw")

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
            request: compute.WithdrawPublicDelegatedPrefixeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.Operation:
            r"""Call the withdraw method over HTTP.

            Args:
                request (~.compute.WithdrawPublicDelegatedPrefixeRequest):
                    The request object. A request message for
                PublicDelegatedPrefixes.Withdraw. See
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
                _BasePublicDelegatedPrefixesRestTransport._BaseWithdraw._get_http_options()
            )
            request, metadata = self._interceptor.pre_withdraw(request, metadata)
            transcoded_request = _BasePublicDelegatedPrefixesRestTransport._BaseWithdraw._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePublicDelegatedPrefixesRestTransport._BaseWithdraw._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PublicDelegatedPrefixesRestTransport._Withdraw._get_response(
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
            resp = self._interceptor.post_withdraw(resp)
            return resp

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListPublicDelegatedPrefixesRequest],
        compute.PublicDelegatedPrefixAggregatedList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AggregatedList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def announce(
        self,
    ) -> Callable[[compute.AnnouncePublicDelegatedPrefixeRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Announce(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeletePublicDelegatedPrefixeRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetPublicDelegatedPrefixeRequest], compute.PublicDelegatedPrefix
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertPublicDelegatedPrefixeRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListPublicDelegatedPrefixesRequest], compute.PublicDelegatedPrefixList
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def patch(
        self,
    ) -> Callable[[compute.PatchPublicDelegatedPrefixeRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Patch(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def withdraw(
        self,
    ) -> Callable[[compute.WithdrawPublicDelegatedPrefixeRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Withdraw(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("PublicDelegatedPrefixesRestTransport",)
