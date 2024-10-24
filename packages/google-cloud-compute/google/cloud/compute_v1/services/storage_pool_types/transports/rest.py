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
from .rest_base import _BaseStoragePoolTypesRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class StoragePoolTypesRestInterceptor:
    """Interceptor for StoragePoolTypes.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the StoragePoolTypesRestTransport.

    .. code-block:: python
        class MyCustomStoragePoolTypesInterceptor(StoragePoolTypesRestInterceptor):
            def pre_aggregated_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregated_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = StoragePoolTypesRestTransport(interceptor=MyCustomStoragePoolTypesInterceptor())
        client = StoragePoolTypesClient(transport=transport)


    """

    def pre_aggregated_list(
        self,
        request: compute.AggregatedListStoragePoolTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        compute.AggregatedListStoragePoolTypesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StoragePoolTypes server.
        """
        return request, metadata

    def post_aggregated_list(
        self, response: compute.StoragePoolTypeAggregatedList
    ) -> compute.StoragePoolTypeAggregatedList:
        """Post-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the response
        after it is returned by the StoragePoolTypes server but before
        it is returned to user code.
        """
        return response

    def pre_get(
        self,
        request: compute.GetStoragePoolTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.GetStoragePoolTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StoragePoolTypes server.
        """
        return request, metadata

    def post_get(self, response: compute.StoragePoolType) -> compute.StoragePoolType:
        """Post-rpc interceptor for get

        Override in a subclass to manipulate the response
        after it is returned by the StoragePoolTypes server but before
        it is returned to user code.
        """
        return response

    def pre_list(
        self,
        request: compute.ListStoragePoolTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[compute.ListStoragePoolTypesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StoragePoolTypes server.
        """
        return request, metadata

    def post_list(
        self, response: compute.StoragePoolTypeList
    ) -> compute.StoragePoolTypeList:
        """Post-rpc interceptor for list

        Override in a subclass to manipulate the response
        after it is returned by the StoragePoolTypes server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class StoragePoolTypesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: StoragePoolTypesRestInterceptor


class StoragePoolTypesRestTransport(_BaseStoragePoolTypesRestTransport):
    """REST backend synchronous transport for StoragePoolTypes.

    The StoragePoolTypes API.

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
        interceptor: Optional[StoragePoolTypesRestInterceptor] = None,
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
        self._interceptor = interceptor or StoragePoolTypesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AggregatedList(
        _BaseStoragePoolTypesRestTransport._BaseAggregatedList, StoragePoolTypesRestStub
    ):
        def __hash__(self):
            return hash("StoragePoolTypesRestTransport.AggregatedList")

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
            request: compute.AggregatedListStoragePoolTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.StoragePoolTypeAggregatedList:
            r"""Call the aggregated list method over HTTP.

            Args:
                request (~.compute.AggregatedListStoragePoolTypesRequest):
                    The request object. A request message for
                StoragePoolTypes.AggregatedList. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.StoragePoolTypeAggregatedList:

            """

            http_options = (
                _BaseStoragePoolTypesRestTransport._BaseAggregatedList._get_http_options()
            )
            request, metadata = self._interceptor.pre_aggregated_list(request, metadata)
            transcoded_request = _BaseStoragePoolTypesRestTransport._BaseAggregatedList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseStoragePoolTypesRestTransport._BaseAggregatedList._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = StoragePoolTypesRestTransport._AggregatedList._get_response(
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
            resp = compute.StoragePoolTypeAggregatedList()
            pb_resp = compute.StoragePoolTypeAggregatedList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_aggregated_list(resp)
            return resp

    class _Get(_BaseStoragePoolTypesRestTransport._BaseGet, StoragePoolTypesRestStub):
        def __hash__(self):
            return hash("StoragePoolTypesRestTransport.Get")

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
            request: compute.GetStoragePoolTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.StoragePoolType:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetStoragePoolTypeRequest):
                    The request object. A request message for
                StoragePoolTypes.Get. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.StoragePoolType:

            """

            http_options = (
                _BaseStoragePoolTypesRestTransport._BaseGet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = (
                _BaseStoragePoolTypesRestTransport._BaseGet._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseStoragePoolTypesRestTransport._BaseGet._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = StoragePoolTypesRestTransport._Get._get_response(
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
            resp = compute.StoragePoolType()
            pb_resp = compute.StoragePoolType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get(resp)
            return resp

    class _List(_BaseStoragePoolTypesRestTransport._BaseList, StoragePoolTypesRestStub):
        def __hash__(self):
            return hash("StoragePoolTypesRestTransport.List")

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
            request: compute.ListStoragePoolTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> compute.StoragePoolTypeList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListStoragePoolTypesRequest):
                    The request object. A request message for
                StoragePoolTypes.List. See the method
                description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.StoragePoolTypeList:
                    Contains a list of storage pool
                types.

            """

            http_options = (
                _BaseStoragePoolTypesRestTransport._BaseList._get_http_options()
            )
            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = (
                _BaseStoragePoolTypesRestTransport._BaseList._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseStoragePoolTypesRestTransport._BaseList._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = StoragePoolTypesRestTransport._List._get_response(
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
            resp = compute.StoragePoolTypeList()
            pb_resp = compute.StoragePoolTypeList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list(resp)
            return resp

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListStoragePoolTypesRequest],
        compute.StoragePoolTypeAggregatedList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AggregatedList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[[compute.GetStoragePoolTypeRequest], compute.StoragePoolType]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[[compute.ListStoragePoolTypesRequest], compute.StoragePoolTypeList]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("StoragePoolTypesRestTransport",)
