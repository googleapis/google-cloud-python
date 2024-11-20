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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.ai.generativelanguage_v1beta.types import (
    cached_content as gag_cached_content,
)
from google.ai.generativelanguage_v1beta.types import cache_service
from google.ai.generativelanguage_v1beta.types import cached_content

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseCacheServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class CacheServiceRestInterceptor:
    """Interceptor for CacheService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CacheServiceRestTransport.

    .. code-block:: python
        class MyCustomCacheServiceInterceptor(CacheServiceRestInterceptor):
            def pre_create_cached_content(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cached_content(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_cached_content(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_cached_content(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cached_content(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_cached_contents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_cached_contents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_cached_content(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_cached_content(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CacheServiceRestTransport(interceptor=MyCustomCacheServiceInterceptor())
        client = CacheServiceClient(transport=transport)


    """

    def pre_create_cached_content(
        self,
        request: cache_service.CreateCachedContentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cache_service.CreateCachedContentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_cached_content

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CacheService server.
        """
        return request, metadata

    def post_create_cached_content(
        self, response: gag_cached_content.CachedContent
    ) -> gag_cached_content.CachedContent:
        """Post-rpc interceptor for create_cached_content

        Override in a subclass to manipulate the response
        after it is returned by the CacheService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_cached_content(
        self,
        request: cache_service.DeleteCachedContentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cache_service.DeleteCachedContentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_cached_content

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CacheService server.
        """
        return request, metadata

    def pre_get_cached_content(
        self,
        request: cache_service.GetCachedContentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cache_service.GetCachedContentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_cached_content

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CacheService server.
        """
        return request, metadata

    def post_get_cached_content(
        self, response: cached_content.CachedContent
    ) -> cached_content.CachedContent:
        """Post-rpc interceptor for get_cached_content

        Override in a subclass to manipulate the response
        after it is returned by the CacheService server but before
        it is returned to user code.
        """
        return response

    def pre_list_cached_contents(
        self,
        request: cache_service.ListCachedContentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cache_service.ListCachedContentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_cached_contents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CacheService server.
        """
        return request, metadata

    def post_list_cached_contents(
        self, response: cache_service.ListCachedContentsResponse
    ) -> cache_service.ListCachedContentsResponse:
        """Post-rpc interceptor for list_cached_contents

        Override in a subclass to manipulate the response
        after it is returned by the CacheService server but before
        it is returned to user code.
        """
        return response

    def pre_update_cached_content(
        self,
        request: cache_service.UpdateCachedContentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cache_service.UpdateCachedContentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_cached_content

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CacheService server.
        """
        return request, metadata

    def post_update_cached_content(
        self, response: gag_cached_content.CachedContent
    ) -> gag_cached_content.CachedContent:
        """Post-rpc interceptor for update_cached_content

        Override in a subclass to manipulate the response
        after it is returned by the CacheService server but before
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
        before they are sent to the CacheService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the CacheService server but before
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
        before they are sent to the CacheService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the CacheService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CacheServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CacheServiceRestInterceptor


class CacheServiceRestTransport(_BaseCacheServiceRestTransport):
    """REST backend synchronous transport for CacheService.

    API for managing cache of content (CachedContent resources)
    that can be used in GenerativeService requests. This way
    generate content requests can benefit from preprocessing work
    being done earlier, possibly lowering their computational cost.
    It is intended to be used with large contexts.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "generativelanguage.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CacheServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'generativelanguage.googleapis.com').
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
        self._interceptor = interceptor or CacheServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateCachedContent(
        _BaseCacheServiceRestTransport._BaseCreateCachedContent, CacheServiceRestStub
    ):
        def __hash__(self):
            return hash("CacheServiceRestTransport.CreateCachedContent")

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
            request: cache_service.CreateCachedContentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gag_cached_content.CachedContent:
            r"""Call the create cached content method over HTTP.

            Args:
                request (~.cache_service.CreateCachedContentRequest):
                    The request object. Request to create CachedContent.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gag_cached_content.CachedContent:
                    Content that has been preprocessed
                and can be used in subsequent request to
                GenerativeService.

                Cached content can be only used with
                model it was created for.

            """

            http_options = (
                _BaseCacheServiceRestTransport._BaseCreateCachedContent._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_cached_content(
                request, metadata
            )
            transcoded_request = _BaseCacheServiceRestTransport._BaseCreateCachedContent._get_transcoded_request(
                http_options, request
            )

            body = _BaseCacheServiceRestTransport._BaseCreateCachedContent._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCacheServiceRestTransport._BaseCreateCachedContent._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CacheServiceRestTransport._CreateCachedContent._get_response(
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
            resp = gag_cached_content.CachedContent()
            pb_resp = gag_cached_content.CachedContent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_cached_content(resp)
            return resp

    class _DeleteCachedContent(
        _BaseCacheServiceRestTransport._BaseDeleteCachedContent, CacheServiceRestStub
    ):
        def __hash__(self):
            return hash("CacheServiceRestTransport.DeleteCachedContent")

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
            request: cache_service.DeleteCachedContentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete cached content method over HTTP.

            Args:
                request (~.cache_service.DeleteCachedContentRequest):
                    The request object. Request to delete CachedContent.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseCacheServiceRestTransport._BaseDeleteCachedContent._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_cached_content(
                request, metadata
            )
            transcoded_request = _BaseCacheServiceRestTransport._BaseDeleteCachedContent._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCacheServiceRestTransport._BaseDeleteCachedContent._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CacheServiceRestTransport._DeleteCachedContent._get_response(
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

    class _GetCachedContent(
        _BaseCacheServiceRestTransport._BaseGetCachedContent, CacheServiceRestStub
    ):
        def __hash__(self):
            return hash("CacheServiceRestTransport.GetCachedContent")

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
            request: cache_service.GetCachedContentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cached_content.CachedContent:
            r"""Call the get cached content method over HTTP.

            Args:
                request (~.cache_service.GetCachedContentRequest):
                    The request object. Request to read CachedContent.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cached_content.CachedContent:
                    Content that has been preprocessed
                and can be used in subsequent request to
                GenerativeService.

                Cached content can be only used with
                model it was created for.

            """

            http_options = (
                _BaseCacheServiceRestTransport._BaseGetCachedContent._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_cached_content(
                request, metadata
            )
            transcoded_request = _BaseCacheServiceRestTransport._BaseGetCachedContent._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCacheServiceRestTransport._BaseGetCachedContent._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CacheServiceRestTransport._GetCachedContent._get_response(
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
            resp = cached_content.CachedContent()
            pb_resp = cached_content.CachedContent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_cached_content(resp)
            return resp

    class _ListCachedContents(
        _BaseCacheServiceRestTransport._BaseListCachedContents, CacheServiceRestStub
    ):
        def __hash__(self):
            return hash("CacheServiceRestTransport.ListCachedContents")

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
            request: cache_service.ListCachedContentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cache_service.ListCachedContentsResponse:
            r"""Call the list cached contents method over HTTP.

            Args:
                request (~.cache_service.ListCachedContentsRequest):
                    The request object. Request to list CachedContents.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cache_service.ListCachedContentsResponse:
                    Response with CachedContents list.
            """

            http_options = (
                _BaseCacheServiceRestTransport._BaseListCachedContents._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_cached_contents(
                request, metadata
            )
            transcoded_request = _BaseCacheServiceRestTransport._BaseListCachedContents._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCacheServiceRestTransport._BaseListCachedContents._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CacheServiceRestTransport._ListCachedContents._get_response(
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
            resp = cache_service.ListCachedContentsResponse()
            pb_resp = cache_service.ListCachedContentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_cached_contents(resp)
            return resp

    class _UpdateCachedContent(
        _BaseCacheServiceRestTransport._BaseUpdateCachedContent, CacheServiceRestStub
    ):
        def __hash__(self):
            return hash("CacheServiceRestTransport.UpdateCachedContent")

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
            request: cache_service.UpdateCachedContentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gag_cached_content.CachedContent:
            r"""Call the update cached content method over HTTP.

            Args:
                request (~.cache_service.UpdateCachedContentRequest):
                    The request object. Request to update CachedContent.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gag_cached_content.CachedContent:
                    Content that has been preprocessed
                and can be used in subsequent request to
                GenerativeService.

                Cached content can be only used with
                model it was created for.

            """

            http_options = (
                _BaseCacheServiceRestTransport._BaseUpdateCachedContent._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_cached_content(
                request, metadata
            )
            transcoded_request = _BaseCacheServiceRestTransport._BaseUpdateCachedContent._get_transcoded_request(
                http_options, request
            )

            body = _BaseCacheServiceRestTransport._BaseUpdateCachedContent._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCacheServiceRestTransport._BaseUpdateCachedContent._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CacheServiceRestTransport._UpdateCachedContent._get_response(
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
            resp = gag_cached_content.CachedContent()
            pb_resp = gag_cached_content.CachedContent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_cached_content(resp)
            return resp

    @property
    def create_cached_content(
        self,
    ) -> Callable[
        [cache_service.CreateCachedContentRequest], gag_cached_content.CachedContent
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCachedContent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_cached_content(
        self,
    ) -> Callable[[cache_service.DeleteCachedContentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCachedContent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cached_content(
        self,
    ) -> Callable[
        [cache_service.GetCachedContentRequest], cached_content.CachedContent
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCachedContent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_cached_contents(
        self,
    ) -> Callable[
        [cache_service.ListCachedContentsRequest],
        cache_service.ListCachedContentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCachedContents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_cached_content(
        self,
    ) -> Callable[
        [cache_service.UpdateCachedContentRequest], gag_cached_content.CachedContent
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCachedContent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseCacheServiceRestTransport._BaseGetOperation, CacheServiceRestStub
    ):
        def __hash__(self):
            return hash("CacheServiceRestTransport.GetOperation")

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
                _BaseCacheServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseCacheServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseCacheServiceRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CacheServiceRestTransport._GetOperation._get_response(
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
        _BaseCacheServiceRestTransport._BaseListOperations, CacheServiceRestStub
    ):
        def __hash__(self):
            return hash("CacheServiceRestTransport.ListOperations")

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
                _BaseCacheServiceRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseCacheServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCacheServiceRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CacheServiceRestTransport._ListOperations._get_response(
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
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CacheServiceRestTransport",)
