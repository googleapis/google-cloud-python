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

from google.cloud.contentwarehouse_v1.types import document_link_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseDocumentLinkServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class DocumentLinkServiceRestInterceptor:
    """Interceptor for DocumentLinkService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DocumentLinkServiceRestTransport.

    .. code-block:: python
        class MyCustomDocumentLinkServiceInterceptor(DocumentLinkServiceRestInterceptor):
            def pre_create_document_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_document_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_document_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_list_linked_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_linked_sources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_linked_targets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_linked_targets(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DocumentLinkServiceRestTransport(interceptor=MyCustomDocumentLinkServiceInterceptor())
        client = DocumentLinkServiceClient(transport=transport)


    """

    def pre_create_document_link(
        self,
        request: document_link_service.CreateDocumentLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_link_service.CreateDocumentLinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_document_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentLinkService server.
        """
        return request, metadata

    def post_create_document_link(
        self, response: document_link_service.DocumentLink
    ) -> document_link_service.DocumentLink:
        """Post-rpc interceptor for create_document_link

        Override in a subclass to manipulate the response
        after it is returned by the DocumentLinkService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_document_link(
        self,
        request: document_link_service.DeleteDocumentLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_link_service.DeleteDocumentLinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_document_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentLinkService server.
        """
        return request, metadata

    def pre_list_linked_sources(
        self,
        request: document_link_service.ListLinkedSourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_link_service.ListLinkedSourcesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_linked_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentLinkService server.
        """
        return request, metadata

    def post_list_linked_sources(
        self, response: document_link_service.ListLinkedSourcesResponse
    ) -> document_link_service.ListLinkedSourcesResponse:
        """Post-rpc interceptor for list_linked_sources

        Override in a subclass to manipulate the response
        after it is returned by the DocumentLinkService server but before
        it is returned to user code.
        """
        return response

    def pre_list_linked_targets(
        self,
        request: document_link_service.ListLinkedTargetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_link_service.ListLinkedTargetsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_linked_targets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentLinkService server.
        """
        return request, metadata

    def post_list_linked_targets(
        self, response: document_link_service.ListLinkedTargetsResponse
    ) -> document_link_service.ListLinkedTargetsResponse:
        """Post-rpc interceptor for list_linked_targets

        Override in a subclass to manipulate the response
        after it is returned by the DocumentLinkService server but before
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
        before they are sent to the DocumentLinkService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the DocumentLinkService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DocumentLinkServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DocumentLinkServiceRestInterceptor


class DocumentLinkServiceRestTransport(_BaseDocumentLinkServiceRestTransport):
    """REST backend synchronous transport for DocumentLinkService.

    This service lets you manage document-links.
    Document-Links are treated as sub-resources under source
    documents.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "contentwarehouse.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DocumentLinkServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'contentwarehouse.googleapis.com').
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
        self._interceptor = interceptor or DocumentLinkServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateDocumentLink(
        _BaseDocumentLinkServiceRestTransport._BaseCreateDocumentLink,
        DocumentLinkServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentLinkServiceRestTransport.CreateDocumentLink")

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
            request: document_link_service.CreateDocumentLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_link_service.DocumentLink:
            r"""Call the create document link method over HTTP.

            Args:
                request (~.document_link_service.CreateDocumentLinkRequest):
                    The request object. Request message for
                DocumentLinkService.CreateDocumentLink.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_link_service.DocumentLink:
                    A document-link between source and
                target document.

            """

            http_options = (
                _BaseDocumentLinkServiceRestTransport._BaseCreateDocumentLink._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_document_link(
                request, metadata
            )
            transcoded_request = _BaseDocumentLinkServiceRestTransport._BaseCreateDocumentLink._get_transcoded_request(
                http_options, request
            )

            body = _BaseDocumentLinkServiceRestTransport._BaseCreateDocumentLink._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDocumentLinkServiceRestTransport._BaseCreateDocumentLink._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DocumentLinkServiceRestTransport._CreateDocumentLink._get_response(
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
            resp = document_link_service.DocumentLink()
            pb_resp = document_link_service.DocumentLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_document_link(resp)
            return resp

    class _DeleteDocumentLink(
        _BaseDocumentLinkServiceRestTransport._BaseDeleteDocumentLink,
        DocumentLinkServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentLinkServiceRestTransport.DeleteDocumentLink")

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
            request: document_link_service.DeleteDocumentLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete document link method over HTTP.

            Args:
                request (~.document_link_service.DeleteDocumentLinkRequest):
                    The request object. Request message for
                DocumentLinkService.DeleteDocumentLink.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseDocumentLinkServiceRestTransport._BaseDeleteDocumentLink._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_document_link(
                request, metadata
            )
            transcoded_request = _BaseDocumentLinkServiceRestTransport._BaseDeleteDocumentLink._get_transcoded_request(
                http_options, request
            )

            body = _BaseDocumentLinkServiceRestTransport._BaseDeleteDocumentLink._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDocumentLinkServiceRestTransport._BaseDeleteDocumentLink._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DocumentLinkServiceRestTransport._DeleteDocumentLink._get_response(
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

    class _ListLinkedSources(
        _BaseDocumentLinkServiceRestTransport._BaseListLinkedSources,
        DocumentLinkServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentLinkServiceRestTransport.ListLinkedSources")

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
            request: document_link_service.ListLinkedSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_link_service.ListLinkedSourcesResponse:
            r"""Call the list linked sources method over HTTP.

            Args:
                request (~.document_link_service.ListLinkedSourcesRequest):
                    The request object. Response message for
                DocumentLinkService.ListLinkedSources.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_link_service.ListLinkedSourcesResponse:
                    Response message for
                DocumentLinkService.ListLinkedSources.

            """

            http_options = (
                _BaseDocumentLinkServiceRestTransport._BaseListLinkedSources._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_linked_sources(
                request, metadata
            )
            transcoded_request = _BaseDocumentLinkServiceRestTransport._BaseListLinkedSources._get_transcoded_request(
                http_options, request
            )

            body = _BaseDocumentLinkServiceRestTransport._BaseListLinkedSources._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDocumentLinkServiceRestTransport._BaseListLinkedSources._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DocumentLinkServiceRestTransport._ListLinkedSources._get_response(
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
            resp = document_link_service.ListLinkedSourcesResponse()
            pb_resp = document_link_service.ListLinkedSourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_linked_sources(resp)
            return resp

    class _ListLinkedTargets(
        _BaseDocumentLinkServiceRestTransport._BaseListLinkedTargets,
        DocumentLinkServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentLinkServiceRestTransport.ListLinkedTargets")

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
            request: document_link_service.ListLinkedTargetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_link_service.ListLinkedTargetsResponse:
            r"""Call the list linked targets method over HTTP.

            Args:
                request (~.document_link_service.ListLinkedTargetsRequest):
                    The request object. Request message for
                DocumentLinkService.ListLinkedTargets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_link_service.ListLinkedTargetsResponse:
                    Response message for
                DocumentLinkService.ListLinkedTargets.

            """

            http_options = (
                _BaseDocumentLinkServiceRestTransport._BaseListLinkedTargets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_linked_targets(
                request, metadata
            )
            transcoded_request = _BaseDocumentLinkServiceRestTransport._BaseListLinkedTargets._get_transcoded_request(
                http_options, request
            )

            body = _BaseDocumentLinkServiceRestTransport._BaseListLinkedTargets._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDocumentLinkServiceRestTransport._BaseListLinkedTargets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DocumentLinkServiceRestTransport._ListLinkedTargets._get_response(
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
            resp = document_link_service.ListLinkedTargetsResponse()
            pb_resp = document_link_service.ListLinkedTargetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_linked_targets(resp)
            return resp

    @property
    def create_document_link(
        self,
    ) -> Callable[
        [document_link_service.CreateDocumentLinkRequest],
        document_link_service.DocumentLink,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDocumentLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_document_link(
        self,
    ) -> Callable[[document_link_service.DeleteDocumentLinkRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDocumentLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_linked_sources(
        self,
    ) -> Callable[
        [document_link_service.ListLinkedSourcesRequest],
        document_link_service.ListLinkedSourcesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListLinkedSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_linked_targets(
        self,
    ) -> Callable[
        [document_link_service.ListLinkedTargetsRequest],
        document_link_service.ListLinkedTargetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListLinkedTargets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseDocumentLinkServiceRestTransport._BaseGetOperation,
        DocumentLinkServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentLinkServiceRestTransport.GetOperation")

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
                _BaseDocumentLinkServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseDocumentLinkServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDocumentLinkServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DocumentLinkServiceRestTransport._GetOperation._get_response(
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
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DocumentLinkServiceRestTransport",)
