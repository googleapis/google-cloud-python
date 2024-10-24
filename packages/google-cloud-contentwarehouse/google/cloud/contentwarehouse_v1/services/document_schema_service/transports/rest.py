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

from google.cloud.contentwarehouse_v1.types import (
    document_schema as gcc_document_schema,
)
from google.cloud.contentwarehouse_v1.types import document_schema
from google.cloud.contentwarehouse_v1.types import document_schema_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseDocumentSchemaServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class DocumentSchemaServiceRestInterceptor:
    """Interceptor for DocumentSchemaService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DocumentSchemaServiceRestTransport.

    .. code-block:: python
        class MyCustomDocumentSchemaServiceInterceptor(DocumentSchemaServiceRestInterceptor):
            def pre_create_document_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_document_schema(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_document_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_document_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_document_schema(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_document_schemas(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_document_schemas(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_document_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_document_schema(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DocumentSchemaServiceRestTransport(interceptor=MyCustomDocumentSchemaServiceInterceptor())
        client = DocumentSchemaServiceClient(transport=transport)


    """

    def pre_create_document_schema(
        self,
        request: document_schema_service.CreateDocumentSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_schema_service.CreateDocumentSchemaRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_document_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentSchemaService server.
        """
        return request, metadata

    def post_create_document_schema(
        self, response: gcc_document_schema.DocumentSchema
    ) -> gcc_document_schema.DocumentSchema:
        """Post-rpc interceptor for create_document_schema

        Override in a subclass to manipulate the response
        after it is returned by the DocumentSchemaService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_document_schema(
        self,
        request: document_schema_service.DeleteDocumentSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_schema_service.DeleteDocumentSchemaRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_document_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentSchemaService server.
        """
        return request, metadata

    def pre_get_document_schema(
        self,
        request: document_schema_service.GetDocumentSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_schema_service.GetDocumentSchemaRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_document_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentSchemaService server.
        """
        return request, metadata

    def post_get_document_schema(
        self, response: document_schema.DocumentSchema
    ) -> document_schema.DocumentSchema:
        """Post-rpc interceptor for get_document_schema

        Override in a subclass to manipulate the response
        after it is returned by the DocumentSchemaService server but before
        it is returned to user code.
        """
        return response

    def pre_list_document_schemas(
        self,
        request: document_schema_service.ListDocumentSchemasRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_schema_service.ListDocumentSchemasRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_document_schemas

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentSchemaService server.
        """
        return request, metadata

    def post_list_document_schemas(
        self, response: document_schema_service.ListDocumentSchemasResponse
    ) -> document_schema_service.ListDocumentSchemasResponse:
        """Post-rpc interceptor for list_document_schemas

        Override in a subclass to manipulate the response
        after it is returned by the DocumentSchemaService server but before
        it is returned to user code.
        """
        return response

    def pre_update_document_schema(
        self,
        request: document_schema_service.UpdateDocumentSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_schema_service.UpdateDocumentSchemaRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_document_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentSchemaService server.
        """
        return request, metadata

    def post_update_document_schema(
        self, response: gcc_document_schema.DocumentSchema
    ) -> gcc_document_schema.DocumentSchema:
        """Post-rpc interceptor for update_document_schema

        Override in a subclass to manipulate the response
        after it is returned by the DocumentSchemaService server but before
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
        before they are sent to the DocumentSchemaService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the DocumentSchemaService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DocumentSchemaServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DocumentSchemaServiceRestInterceptor


class DocumentSchemaServiceRestTransport(_BaseDocumentSchemaServiceRestTransport):
    """REST backend synchronous transport for DocumentSchemaService.

    This service lets you manage document schema.

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
        interceptor: Optional[DocumentSchemaServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or DocumentSchemaServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateDocumentSchema(
        _BaseDocumentSchemaServiceRestTransport._BaseCreateDocumentSchema,
        DocumentSchemaServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentSchemaServiceRestTransport.CreateDocumentSchema")

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
            request: document_schema_service.CreateDocumentSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcc_document_schema.DocumentSchema:
            r"""Call the create document schema method over HTTP.

            Args:
                request (~.document_schema_service.CreateDocumentSchemaRequest):
                    The request object. Request message for
                DocumentSchemaService.CreateDocumentSchema.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcc_document_schema.DocumentSchema:
                    A document schema used to define
                document structure.

            """

            http_options = (
                _BaseDocumentSchemaServiceRestTransport._BaseCreateDocumentSchema._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_document_schema(
                request, metadata
            )
            transcoded_request = _BaseDocumentSchemaServiceRestTransport._BaseCreateDocumentSchema._get_transcoded_request(
                http_options, request
            )

            body = _BaseDocumentSchemaServiceRestTransport._BaseCreateDocumentSchema._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDocumentSchemaServiceRestTransport._BaseCreateDocumentSchema._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DocumentSchemaServiceRestTransport._CreateDocumentSchema._get_response(
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
            resp = gcc_document_schema.DocumentSchema()
            pb_resp = gcc_document_schema.DocumentSchema.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_document_schema(resp)
            return resp

    class _DeleteDocumentSchema(
        _BaseDocumentSchemaServiceRestTransport._BaseDeleteDocumentSchema,
        DocumentSchemaServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentSchemaServiceRestTransport.DeleteDocumentSchema")

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
            request: document_schema_service.DeleteDocumentSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete document schema method over HTTP.

            Args:
                request (~.document_schema_service.DeleteDocumentSchemaRequest):
                    The request object. Request message for
                DocumentSchemaService.DeleteDocumentSchema.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseDocumentSchemaServiceRestTransport._BaseDeleteDocumentSchema._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_document_schema(
                request, metadata
            )
            transcoded_request = _BaseDocumentSchemaServiceRestTransport._BaseDeleteDocumentSchema._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDocumentSchemaServiceRestTransport._BaseDeleteDocumentSchema._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DocumentSchemaServiceRestTransport._DeleteDocumentSchema._get_response(
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

    class _GetDocumentSchema(
        _BaseDocumentSchemaServiceRestTransport._BaseGetDocumentSchema,
        DocumentSchemaServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentSchemaServiceRestTransport.GetDocumentSchema")

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
            request: document_schema_service.GetDocumentSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_schema.DocumentSchema:
            r"""Call the get document schema method over HTTP.

            Args:
                request (~.document_schema_service.GetDocumentSchemaRequest):
                    The request object. Request message for
                DocumentSchemaService.GetDocumentSchema.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_schema.DocumentSchema:
                    A document schema used to define
                document structure.

            """

            http_options = (
                _BaseDocumentSchemaServiceRestTransport._BaseGetDocumentSchema._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_document_schema(
                request, metadata
            )
            transcoded_request = _BaseDocumentSchemaServiceRestTransport._BaseGetDocumentSchema._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDocumentSchemaServiceRestTransport._BaseGetDocumentSchema._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DocumentSchemaServiceRestTransport._GetDocumentSchema._get_response(
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
            resp = document_schema.DocumentSchema()
            pb_resp = document_schema.DocumentSchema.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_document_schema(resp)
            return resp

    class _ListDocumentSchemas(
        _BaseDocumentSchemaServiceRestTransport._BaseListDocumentSchemas,
        DocumentSchemaServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentSchemaServiceRestTransport.ListDocumentSchemas")

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
            request: document_schema_service.ListDocumentSchemasRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_schema_service.ListDocumentSchemasResponse:
            r"""Call the list document schemas method over HTTP.

            Args:
                request (~.document_schema_service.ListDocumentSchemasRequest):
                    The request object. Request message for
                DocumentSchemaService.ListDocumentSchemas.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_schema_service.ListDocumentSchemasResponse:
                    Response message for
                DocumentSchemaService.ListDocumentSchemas.

            """

            http_options = (
                _BaseDocumentSchemaServiceRestTransport._BaseListDocumentSchemas._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_document_schemas(
                request, metadata
            )
            transcoded_request = _BaseDocumentSchemaServiceRestTransport._BaseListDocumentSchemas._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDocumentSchemaServiceRestTransport._BaseListDocumentSchemas._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DocumentSchemaServiceRestTransport._ListDocumentSchemas._get_response(
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
            resp = document_schema_service.ListDocumentSchemasResponse()
            pb_resp = document_schema_service.ListDocumentSchemasResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_document_schemas(resp)
            return resp

    class _UpdateDocumentSchema(
        _BaseDocumentSchemaServiceRestTransport._BaseUpdateDocumentSchema,
        DocumentSchemaServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentSchemaServiceRestTransport.UpdateDocumentSchema")

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
            request: document_schema_service.UpdateDocumentSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcc_document_schema.DocumentSchema:
            r"""Call the update document schema method over HTTP.

            Args:
                request (~.document_schema_service.UpdateDocumentSchemaRequest):
                    The request object. Request message for
                DocumentSchemaService.UpdateDocumentSchema.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcc_document_schema.DocumentSchema:
                    A document schema used to define
                document structure.

            """

            http_options = (
                _BaseDocumentSchemaServiceRestTransport._BaseUpdateDocumentSchema._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_document_schema(
                request, metadata
            )
            transcoded_request = _BaseDocumentSchemaServiceRestTransport._BaseUpdateDocumentSchema._get_transcoded_request(
                http_options, request
            )

            body = _BaseDocumentSchemaServiceRestTransport._BaseUpdateDocumentSchema._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDocumentSchemaServiceRestTransport._BaseUpdateDocumentSchema._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DocumentSchemaServiceRestTransport._UpdateDocumentSchema._get_response(
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
            resp = gcc_document_schema.DocumentSchema()
            pb_resp = gcc_document_schema.DocumentSchema.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_document_schema(resp)
            return resp

    @property
    def create_document_schema(
        self,
    ) -> Callable[
        [document_schema_service.CreateDocumentSchemaRequest],
        gcc_document_schema.DocumentSchema,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDocumentSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_document_schema(
        self,
    ) -> Callable[
        [document_schema_service.DeleteDocumentSchemaRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDocumentSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_document_schema(
        self,
    ) -> Callable[
        [document_schema_service.GetDocumentSchemaRequest],
        document_schema.DocumentSchema,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDocumentSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_document_schemas(
        self,
    ) -> Callable[
        [document_schema_service.ListDocumentSchemasRequest],
        document_schema_service.ListDocumentSchemasResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDocumentSchemas(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_document_schema(
        self,
    ) -> Callable[
        [document_schema_service.UpdateDocumentSchemaRequest],
        gcc_document_schema.DocumentSchema,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDocumentSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseDocumentSchemaServiceRestTransport._BaseGetOperation,
        DocumentSchemaServiceRestStub,
    ):
        def __hash__(self):
            return hash("DocumentSchemaServiceRestTransport.GetOperation")

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
                _BaseDocumentSchemaServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseDocumentSchemaServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDocumentSchemaServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DocumentSchemaServiceRestTransport._GetOperation._get_response(
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


__all__ = ("DocumentSchemaServiceRestTransport",)
