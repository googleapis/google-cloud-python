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

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.contentwarehouse_v1.types import (
    document_service,
    document_service_request,
)
from google.cloud.contentwarehouse_v1.types import document as gcc_document

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import DocumentServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class DocumentServiceRestInterceptor:
    """Interceptor for DocumentService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DocumentServiceRestTransport.

    .. code-block:: python
        class MyCustomDocumentServiceInterceptor(DocumentServiceRestInterceptor):
            def pre_create_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_document(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_fetch_acl(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_acl(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_document(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_lock_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_lock_document(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_documents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_documents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_acl(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_acl(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_document(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DocumentServiceRestTransport(interceptor=MyCustomDocumentServiceInterceptor())
        client = DocumentServiceClient(transport=transport)


    """

    def pre_create_document(
        self,
        request: document_service_request.CreateDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_service_request.CreateDocumentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentService server.
        """
        return request, metadata

    def post_create_document(
        self, response: document_service.CreateDocumentResponse
    ) -> document_service.CreateDocumentResponse:
        """Post-rpc interceptor for create_document

        Override in a subclass to manipulate the response
        after it is returned by the DocumentService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_document(
        self,
        request: document_service_request.DeleteDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_service_request.DeleteDocumentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentService server.
        """
        return request, metadata

    def pre_fetch_acl(
        self,
        request: document_service_request.FetchAclRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[document_service_request.FetchAclRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_acl

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentService server.
        """
        return request, metadata

    def post_fetch_acl(
        self, response: document_service.FetchAclResponse
    ) -> document_service.FetchAclResponse:
        """Post-rpc interceptor for fetch_acl

        Override in a subclass to manipulate the response
        after it is returned by the DocumentService server but before
        it is returned to user code.
        """
        return response

    def pre_get_document(
        self,
        request: document_service_request.GetDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[document_service_request.GetDocumentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentService server.
        """
        return request, metadata

    def post_get_document(
        self, response: gcc_document.Document
    ) -> gcc_document.Document:
        """Post-rpc interceptor for get_document

        Override in a subclass to manipulate the response
        after it is returned by the DocumentService server but before
        it is returned to user code.
        """
        return response

    def pre_lock_document(
        self,
        request: document_service_request.LockDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[document_service_request.LockDocumentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for lock_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentService server.
        """
        return request, metadata

    def post_lock_document(
        self, response: gcc_document.Document
    ) -> gcc_document.Document:
        """Post-rpc interceptor for lock_document

        Override in a subclass to manipulate the response
        after it is returned by the DocumentService server but before
        it is returned to user code.
        """
        return response

    def pre_search_documents(
        self,
        request: document_service_request.SearchDocumentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_service_request.SearchDocumentsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for search_documents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentService server.
        """
        return request, metadata

    def post_search_documents(
        self, response: document_service.SearchDocumentsResponse
    ) -> document_service.SearchDocumentsResponse:
        """Post-rpc interceptor for search_documents

        Override in a subclass to manipulate the response
        after it is returned by the DocumentService server but before
        it is returned to user code.
        """
        return response

    def pre_set_acl(
        self,
        request: document_service_request.SetAclRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[document_service_request.SetAclRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_acl

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentService server.
        """
        return request, metadata

    def post_set_acl(
        self, response: document_service.SetAclResponse
    ) -> document_service.SetAclResponse:
        """Post-rpc interceptor for set_acl

        Override in a subclass to manipulate the response
        after it is returned by the DocumentService server but before
        it is returned to user code.
        """
        return response

    def pre_update_document(
        self,
        request: document_service_request.UpdateDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        document_service_request.UpdateDocumentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DocumentService server.
        """
        return request, metadata

    def post_update_document(
        self, response: document_service.UpdateDocumentResponse
    ) -> document_service.UpdateDocumentResponse:
        """Post-rpc interceptor for update_document

        Override in a subclass to manipulate the response
        after it is returned by the DocumentService server but before
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
        before they are sent to the DocumentService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the DocumentService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DocumentServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DocumentServiceRestInterceptor


class DocumentServiceRestTransport(DocumentServiceTransport):
    """REST backend transport for DocumentService.

    This service lets you manage document.

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
        interceptor: Optional[DocumentServiceRestInterceptor] = None,
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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or DocumentServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateDocument(DocumentServiceRestStub):
        def __hash__(self):
            return hash("CreateDocument")

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
            request: document_service_request.CreateDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_service.CreateDocumentResponse:
            r"""Call the create document method over HTTP.

            Args:
                request (~.document_service_request.CreateDocumentRequest):
                    The request object. Request message for
                DocumentService.CreateDocument.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_service.CreateDocumentResponse:
                    Response message for
                DocumentService.CreateDocument.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/documents",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_create_document(request, metadata)
            pb_request = document_service_request.CreateDocumentRequest.pb(request)
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
            resp = document_service.CreateDocumentResponse()
            pb_resp = document_service.CreateDocumentResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_document(resp)
            return resp

    class _DeleteDocument(DocumentServiceRestStub):
        def __hash__(self):
            return hash("DeleteDocument")

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
            request: document_service_request.DeleteDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete document method over HTTP.

            Args:
                request (~.document_service_request.DeleteDocumentRequest):
                    The request object. Request message for
                DocumentService.DeleteDocument.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/documents/*}:delete",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/documents/referenceId/*}:delete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_delete_document(request, metadata)
            pb_request = document_service_request.DeleteDocumentRequest.pb(request)
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

    class _FetchAcl(DocumentServiceRestStub):
        def __hash__(self):
            return hash("FetchAcl")

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
            request: document_service_request.FetchAclRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_service.FetchAclResponse:
            r"""Call the fetch acl method over HTTP.

            Args:
                request (~.document_service_request.FetchAclRequest):
                    The request object. Request message for
                DocumentService.FetchAcl
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_service.FetchAclResponse:
                    Response message for
                DocumentService.FetchAcl.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/documents/*}:fetchAcl",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*}:fetchAcl",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_acl(request, metadata)
            pb_request = document_service_request.FetchAclRequest.pb(request)
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
            resp = document_service.FetchAclResponse()
            pb_resp = document_service.FetchAclResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_acl(resp)
            return resp

    class _GetDocument(DocumentServiceRestStub):
        def __hash__(self):
            return hash("GetDocument")

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
            request: document_service_request.GetDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcc_document.Document:
            r"""Call the get document method over HTTP.

            Args:
                request (~.document_service_request.GetDocumentRequest):
                    The request object. Request message for
                DocumentService.GetDocument.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcc_document.Document:
                    Defines the structure for content
                warehouse document proto.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/documents/*}:get",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/documents/referenceId/*}:get",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_get_document(request, metadata)
            pb_request = document_service_request.GetDocumentRequest.pb(request)
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
            resp = gcc_document.Document()
            pb_resp = gcc_document.Document.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_document(resp)
            return resp

    class _LockDocument(DocumentServiceRestStub):
        def __hash__(self):
            return hash("LockDocument")

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
            request: document_service_request.LockDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcc_document.Document:
            r"""Call the lock document method over HTTP.

            Args:
                request (~.document_service_request.LockDocumentRequest):
                    The request object. Request message for
                DocumentService.LockDocument.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcc_document.Document:
                    Defines the structure for content
                warehouse document proto.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/documents/*}:lock",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_lock_document(request, metadata)
            pb_request = document_service_request.LockDocumentRequest.pb(request)
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
            resp = gcc_document.Document()
            pb_resp = gcc_document.Document.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_lock_document(resp)
            return resp

    class _SearchDocuments(DocumentServiceRestStub):
        def __hash__(self):
            return hash("SearchDocuments")

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
            request: document_service_request.SearchDocumentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_service.SearchDocumentsResponse:
            r"""Call the search documents method over HTTP.

            Args:
                request (~.document_service_request.SearchDocumentsRequest):
                    The request object. Request message for
                DocumentService.SearchDocuments.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_service.SearchDocumentsResponse:
                    Response message for
                DocumentService.SearchDocuments.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/documents:search",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_search_documents(
                request, metadata
            )
            pb_request = document_service_request.SearchDocumentsRequest.pb(request)
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
            resp = document_service.SearchDocumentsResponse()
            pb_resp = document_service.SearchDocumentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_documents(resp)
            return resp

    class _SetAcl(DocumentServiceRestStub):
        def __hash__(self):
            return hash("SetAcl")

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
            request: document_service_request.SetAclRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_service.SetAclResponse:
            r"""Call the set acl method over HTTP.

            Args:
                request (~.document_service_request.SetAclRequest):
                    The request object. Request message for
                DocumentService.SetAcl.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_service.SetAclResponse:
                    Response message for
                DocumentService.SetAcl.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/documents/*}:setAcl",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*}:setAcl",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_acl(request, metadata)
            pb_request = document_service_request.SetAclRequest.pb(request)
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
            resp = document_service.SetAclResponse()
            pb_resp = document_service.SetAclResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_acl(resp)
            return resp

    class _UpdateDocument(DocumentServiceRestStub):
        def __hash__(self):
            return hash("UpdateDocument")

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
            request: document_service_request.UpdateDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_service.UpdateDocumentResponse:
            r"""Call the update document method over HTTP.

            Args:
                request (~.document_service_request.UpdateDocumentRequest):
                    The request object. Request message for
                DocumentService.UpdateDocument.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document_service.UpdateDocumentResponse:
                    Response message for
                DocumentService.UpdateDocument.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{name=projects/*/locations/*/documents/*}",
                    "body": "*",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{name=projects/*/locations/*/documents/referenceId/*}",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_update_document(request, metadata)
            pb_request = document_service_request.UpdateDocumentRequest.pb(request)
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
            resp = document_service.UpdateDocumentResponse()
            pb_resp = document_service.UpdateDocumentResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_document(resp)
            return resp

    @property
    def create_document(
        self,
    ) -> Callable[
        [document_service_request.CreateDocumentRequest],
        document_service.CreateDocumentResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_document(
        self,
    ) -> Callable[[document_service_request.DeleteDocumentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_acl(
        self,
    ) -> Callable[
        [document_service_request.FetchAclRequest], document_service.FetchAclResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchAcl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_document(
        self,
    ) -> Callable[[document_service_request.GetDocumentRequest], gcc_document.Document]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def lock_document(
        self,
    ) -> Callable[
        [document_service_request.LockDocumentRequest], gcc_document.Document
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._LockDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_documents(
        self,
    ) -> Callable[
        [document_service_request.SearchDocumentsRequest],
        document_service.SearchDocumentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchDocuments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_acl(
        self,
    ) -> Callable[
        [document_service_request.SetAclRequest], document_service.SetAclResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetAcl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_document(
        self,
    ) -> Callable[
        [document_service_request.UpdateDocumentRequest],
        document_service.UpdateDocumentResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(DocumentServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
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
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DocumentServiceRestTransport",)
