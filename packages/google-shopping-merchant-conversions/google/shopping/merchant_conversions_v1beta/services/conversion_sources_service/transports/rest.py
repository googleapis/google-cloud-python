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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.shopping.merchant_conversions_v1beta.types import conversionsources

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseConversionSourcesServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ConversionSourcesServiceRestInterceptor:
    """Interceptor for ConversionSourcesService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ConversionSourcesServiceRestTransport.

    .. code-block:: python
        class MyCustomConversionSourcesServiceInterceptor(ConversionSourcesServiceRestInterceptor):
            def pre_create_conversion_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_conversion_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_conversion_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_conversion_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_conversion_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_conversion_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_conversion_sources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_conversion_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undelete_conversion_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_conversion_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_conversion_source(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ConversionSourcesServiceRestTransport(interceptor=MyCustomConversionSourcesServiceInterceptor())
        client = ConversionSourcesServiceClient(transport=transport)


    """

    def pre_create_conversion_source(
        self,
        request: conversionsources.CreateConversionSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        conversionsources.CreateConversionSourceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_conversion_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversionSourcesService server.
        """
        return request, metadata

    def post_create_conversion_source(
        self, response: conversionsources.ConversionSource
    ) -> conversionsources.ConversionSource:
        """Post-rpc interceptor for create_conversion_source

        Override in a subclass to manipulate the response
        after it is returned by the ConversionSourcesService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_conversion_source(
        self,
        request: conversionsources.DeleteConversionSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        conversionsources.DeleteConversionSourceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_conversion_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversionSourcesService server.
        """
        return request, metadata

    def pre_get_conversion_source(
        self,
        request: conversionsources.GetConversionSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[conversionsources.GetConversionSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_conversion_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversionSourcesService server.
        """
        return request, metadata

    def post_get_conversion_source(
        self, response: conversionsources.ConversionSource
    ) -> conversionsources.ConversionSource:
        """Post-rpc interceptor for get_conversion_source

        Override in a subclass to manipulate the response
        after it is returned by the ConversionSourcesService server but before
        it is returned to user code.
        """
        return response

    def pre_list_conversion_sources(
        self,
        request: conversionsources.ListConversionSourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        conversionsources.ListConversionSourcesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_conversion_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversionSourcesService server.
        """
        return request, metadata

    def post_list_conversion_sources(
        self, response: conversionsources.ListConversionSourcesResponse
    ) -> conversionsources.ListConversionSourcesResponse:
        """Post-rpc interceptor for list_conversion_sources

        Override in a subclass to manipulate the response
        after it is returned by the ConversionSourcesService server but before
        it is returned to user code.
        """
        return response

    def pre_undelete_conversion_source(
        self,
        request: conversionsources.UndeleteConversionSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        conversionsources.UndeleteConversionSourceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for undelete_conversion_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversionSourcesService server.
        """
        return request, metadata

    def post_undelete_conversion_source(
        self, response: conversionsources.ConversionSource
    ) -> conversionsources.ConversionSource:
        """Post-rpc interceptor for undelete_conversion_source

        Override in a subclass to manipulate the response
        after it is returned by the ConversionSourcesService server but before
        it is returned to user code.
        """
        return response

    def pre_update_conversion_source(
        self,
        request: conversionsources.UpdateConversionSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        conversionsources.UpdateConversionSourceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_conversion_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversionSourcesService server.
        """
        return request, metadata

    def post_update_conversion_source(
        self, response: conversionsources.ConversionSource
    ) -> conversionsources.ConversionSource:
        """Post-rpc interceptor for update_conversion_source

        Override in a subclass to manipulate the response
        after it is returned by the ConversionSourcesService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ConversionSourcesServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ConversionSourcesServiceRestInterceptor


class ConversionSourcesServiceRestTransport(_BaseConversionSourcesServiceRestTransport):
    """REST backend synchronous transport for ConversionSourcesService.

    Service for managing conversion sources for a merchant
    account.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "merchantapi.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ConversionSourcesServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'merchantapi.googleapis.com').
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
        self._interceptor = interceptor or ConversionSourcesServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateConversionSource(
        _BaseConversionSourcesServiceRestTransport._BaseCreateConversionSource,
        ConversionSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConversionSourcesServiceRestTransport.CreateConversionSource")

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
            request: conversionsources.CreateConversionSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversionsources.ConversionSource:
            r"""Call the create conversion source method over HTTP.

            Args:
                request (~.conversionsources.CreateConversionSourceRequest):
                    The request object. Request message for the
                CreateConversionSource method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.conversionsources.ConversionSource:
                    Represents a conversion source owned
                by a Merchant account. A merchant
                account can have up to 200 conversion
                sources.

            """

            http_options = (
                _BaseConversionSourcesServiceRestTransport._BaseCreateConversionSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_conversion_source(
                request, metadata
            )
            transcoded_request = _BaseConversionSourcesServiceRestTransport._BaseCreateConversionSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseConversionSourcesServiceRestTransport._BaseCreateConversionSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseConversionSourcesServiceRestTransport._BaseCreateConversionSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConversionSourcesServiceRestTransport._CreateConversionSource._get_response(
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
            resp = conversionsources.ConversionSource()
            pb_resp = conversionsources.ConversionSource.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_conversion_source(resp)
            return resp

    class _DeleteConversionSource(
        _BaseConversionSourcesServiceRestTransport._BaseDeleteConversionSource,
        ConversionSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConversionSourcesServiceRestTransport.DeleteConversionSource")

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
            request: conversionsources.DeleteConversionSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete conversion source method over HTTP.

            Args:
                request (~.conversionsources.DeleteConversionSourceRequest):
                    The request object. Request message for the
                DeleteConversionSource method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseConversionSourcesServiceRestTransport._BaseDeleteConversionSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_conversion_source(
                request, metadata
            )
            transcoded_request = _BaseConversionSourcesServiceRestTransport._BaseDeleteConversionSource._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConversionSourcesServiceRestTransport._BaseDeleteConversionSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConversionSourcesServiceRestTransport._DeleteConversionSource._get_response(
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

    class _GetConversionSource(
        _BaseConversionSourcesServiceRestTransport._BaseGetConversionSource,
        ConversionSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConversionSourcesServiceRestTransport.GetConversionSource")

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
            request: conversionsources.GetConversionSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversionsources.ConversionSource:
            r"""Call the get conversion source method over HTTP.

            Args:
                request (~.conversionsources.GetConversionSourceRequest):
                    The request object. Request message for the
                GetConversionSource method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.conversionsources.ConversionSource:
                    Represents a conversion source owned
                by a Merchant account. A merchant
                account can have up to 200 conversion
                sources.

            """

            http_options = (
                _BaseConversionSourcesServiceRestTransport._BaseGetConversionSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_conversion_source(
                request, metadata
            )
            transcoded_request = _BaseConversionSourcesServiceRestTransport._BaseGetConversionSource._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConversionSourcesServiceRestTransport._BaseGetConversionSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConversionSourcesServiceRestTransport._GetConversionSource._get_response(
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
            resp = conversionsources.ConversionSource()
            pb_resp = conversionsources.ConversionSource.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_conversion_source(resp)
            return resp

    class _ListConversionSources(
        _BaseConversionSourcesServiceRestTransport._BaseListConversionSources,
        ConversionSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConversionSourcesServiceRestTransport.ListConversionSources")

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
            request: conversionsources.ListConversionSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversionsources.ListConversionSourcesResponse:
            r"""Call the list conversion sources method over HTTP.

            Args:
                request (~.conversionsources.ListConversionSourcesRequest):
                    The request object. Request message for the
                ListConversionSources method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.conversionsources.ListConversionSourcesResponse:
                    Response message for the
                ListConversionSources method.

            """

            http_options = (
                _BaseConversionSourcesServiceRestTransport._BaseListConversionSources._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_conversion_sources(
                request, metadata
            )
            transcoded_request = _BaseConversionSourcesServiceRestTransport._BaseListConversionSources._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConversionSourcesServiceRestTransport._BaseListConversionSources._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConversionSourcesServiceRestTransport._ListConversionSources._get_response(
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
            resp = conversionsources.ListConversionSourcesResponse()
            pb_resp = conversionsources.ListConversionSourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_conversion_sources(resp)
            return resp

    class _UndeleteConversionSource(
        _BaseConversionSourcesServiceRestTransport._BaseUndeleteConversionSource,
        ConversionSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "ConversionSourcesServiceRestTransport.UndeleteConversionSource"
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
            request: conversionsources.UndeleteConversionSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversionsources.ConversionSource:
            r"""Call the undelete conversion
            source method over HTTP.

                Args:
                    request (~.conversionsources.UndeleteConversionSourceRequest):
                        The request object. Request message for the
                    UndeleteConversionSource method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.conversionsources.ConversionSource:
                        Represents a conversion source owned
                    by a Merchant account. A merchant
                    account can have up to 200 conversion
                    sources.

            """

            http_options = (
                _BaseConversionSourcesServiceRestTransport._BaseUndeleteConversionSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_undelete_conversion_source(
                request, metadata
            )
            transcoded_request = _BaseConversionSourcesServiceRestTransport._BaseUndeleteConversionSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseConversionSourcesServiceRestTransport._BaseUndeleteConversionSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseConversionSourcesServiceRestTransport._BaseUndeleteConversionSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConversionSourcesServiceRestTransport._UndeleteConversionSource._get_response(
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
            resp = conversionsources.ConversionSource()
            pb_resp = conversionsources.ConversionSource.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_undelete_conversion_source(resp)
            return resp

    class _UpdateConversionSource(
        _BaseConversionSourcesServiceRestTransport._BaseUpdateConversionSource,
        ConversionSourcesServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConversionSourcesServiceRestTransport.UpdateConversionSource")

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
            request: conversionsources.UpdateConversionSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversionsources.ConversionSource:
            r"""Call the update conversion source method over HTTP.

            Args:
                request (~.conversionsources.UpdateConversionSourceRequest):
                    The request object. Request message for the
                UpdateConversionSource method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.conversionsources.ConversionSource:
                    Represents a conversion source owned
                by a Merchant account. A merchant
                account can have up to 200 conversion
                sources.

            """

            http_options = (
                _BaseConversionSourcesServiceRestTransport._BaseUpdateConversionSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_conversion_source(
                request, metadata
            )
            transcoded_request = _BaseConversionSourcesServiceRestTransport._BaseUpdateConversionSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseConversionSourcesServiceRestTransport._BaseUpdateConversionSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseConversionSourcesServiceRestTransport._BaseUpdateConversionSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConversionSourcesServiceRestTransport._UpdateConversionSource._get_response(
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
            resp = conversionsources.ConversionSource()
            pb_resp = conversionsources.ConversionSource.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_conversion_source(resp)
            return resp

    @property
    def create_conversion_source(
        self,
    ) -> Callable[
        [conversionsources.CreateConversionSourceRequest],
        conversionsources.ConversionSource,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateConversionSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_conversion_source(
        self,
    ) -> Callable[[conversionsources.DeleteConversionSourceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteConversionSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_conversion_source(
        self,
    ) -> Callable[
        [conversionsources.GetConversionSourceRequest],
        conversionsources.ConversionSource,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConversionSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_conversion_sources(
        self,
    ) -> Callable[
        [conversionsources.ListConversionSourcesRequest],
        conversionsources.ListConversionSourcesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConversionSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undelete_conversion_source(
        self,
    ) -> Callable[
        [conversionsources.UndeleteConversionSourceRequest],
        conversionsources.ConversionSource,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeleteConversionSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_conversion_source(
        self,
    ) -> Callable[
        [conversionsources.UpdateConversionSourceRequest],
        conversionsources.ConversionSource,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateConversionSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ConversionSourcesServiceRestTransport",)
