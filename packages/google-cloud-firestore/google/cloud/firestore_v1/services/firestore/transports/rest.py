# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.firestore_v1.types import document
from google.cloud.firestore_v1.types import document as gf_document
from google.cloud.firestore_v1.types import firestore
from google.protobuf import empty_pb2  # type: ignore

from .base import FirestoreTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class FirestoreRestInterceptor:
    """Interceptor for Firestore.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the FirestoreRestTransport.

    .. code-block:: python
        class MyCustomFirestoreInterceptor(FirestoreRestInterceptor):
            def pre_batch_get_documents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_get_documents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_write(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_write(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_begin_transaction(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_begin_transaction(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_commit(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_commit(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_document(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_document(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_collection_ids(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_collection_ids(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_documents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_documents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_partition_query(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_partition_query(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rollback(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_run_aggregation_query(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_aggregation_query(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_query(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_query(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_document(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_document(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = FirestoreRestTransport(interceptor=MyCustomFirestoreInterceptor())
        client = FirestoreClient(transport=transport)


    """

    def pre_batch_get_documents(
        self,
        request: firestore.BatchGetDocumentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[firestore.BatchGetDocumentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_get_documents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_batch_get_documents(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        """Post-rpc interceptor for batch_get_documents

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_batch_write(
        self, request: firestore.BatchWriteRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[firestore.BatchWriteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_write

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_batch_write(
        self, response: firestore.BatchWriteResponse
    ) -> firestore.BatchWriteResponse:
        """Post-rpc interceptor for batch_write

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_begin_transaction(
        self,
        request: firestore.BeginTransactionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[firestore.BeginTransactionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for begin_transaction

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_begin_transaction(
        self, response: firestore.BeginTransactionResponse
    ) -> firestore.BeginTransactionResponse:
        """Post-rpc interceptor for begin_transaction

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_commit(
        self, request: firestore.CommitRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[firestore.CommitRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for commit

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_commit(
        self, response: firestore.CommitResponse
    ) -> firestore.CommitResponse:
        """Post-rpc interceptor for commit

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_create_document(
        self,
        request: firestore.CreateDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[firestore.CreateDocumentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_create_document(self, response: document.Document) -> document.Document:
        """Post-rpc interceptor for create_document

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_delete_document(
        self,
        request: firestore.DeleteDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[firestore.DeleteDocumentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def pre_get_document(
        self, request: firestore.GetDocumentRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[firestore.GetDocumentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_get_document(self, response: document.Document) -> document.Document:
        """Post-rpc interceptor for get_document

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_list_collection_ids(
        self,
        request: firestore.ListCollectionIdsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[firestore.ListCollectionIdsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_collection_ids

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_list_collection_ids(
        self, response: firestore.ListCollectionIdsResponse
    ) -> firestore.ListCollectionIdsResponse:
        """Post-rpc interceptor for list_collection_ids

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_list_documents(
        self,
        request: firestore.ListDocumentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[firestore.ListDocumentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_documents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_list_documents(
        self, response: firestore.ListDocumentsResponse
    ) -> firestore.ListDocumentsResponse:
        """Post-rpc interceptor for list_documents

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_partition_query(
        self,
        request: firestore.PartitionQueryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[firestore.PartitionQueryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for partition_query

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_partition_query(
        self, response: firestore.PartitionQueryResponse
    ) -> firestore.PartitionQueryResponse:
        """Post-rpc interceptor for partition_query

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_rollback(
        self, request: firestore.RollbackRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[firestore.RollbackRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for rollback

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def pre_run_aggregation_query(
        self,
        request: firestore.RunAggregationQueryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[firestore.RunAggregationQueryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_aggregation_query

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_run_aggregation_query(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        """Post-rpc interceptor for run_aggregation_query

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_run_query(
        self, request: firestore.RunQueryRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[firestore.RunQueryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_query

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_run_query(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        """Post-rpc interceptor for run_query

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_update_document(
        self,
        request: firestore.UpdateDocumentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[firestore.UpdateDocumentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_document

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_update_document(
        self, response: gf_document.Document
    ) -> gf_document.Document:
        """Post-rpc interceptor for update_document

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
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
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
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
        before they are sent to the Firestore server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Firestore server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class FirestoreRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: FirestoreRestInterceptor


class FirestoreRestTransport(FirestoreTransport):
    """REST backend transport for Firestore.

    The Cloud Firestore service.
    Cloud Firestore is a fast, fully managed, serverless,
    cloud-native NoSQL document database that simplifies storing,
    syncing, and querying data for your mobile, web, and IoT apps at
    global scale. Its client libraries provide live synchronization
    and offline support, while its security features and
    integrations with Firebase and Google Cloud Platform accelerate
    building truly serverless apps.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "firestore.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[FirestoreRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
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
        self._interceptor = interceptor or FirestoreRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BatchGetDocuments(FirestoreRestStub):
        def __hash__(self):
            return hash("BatchGetDocuments")

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
            request: firestore.BatchGetDocumentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the batch get documents method over HTTP.

            Args:
                request (~.firestore.BatchGetDocumentsRequest):
                    The request object. The request for
                [Firestore.BatchGetDocuments][google.firestore.v1.Firestore.BatchGetDocuments].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firestore.BatchGetDocumentsResponse:
                    The streamed response for
                [Firestore.BatchGetDocuments][google.firestore.v1.Firestore.BatchGetDocuments].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{database=projects/*/databases/*}/documents:batchGet",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_get_documents(
                request, metadata
            )
            pb_request = firestore.BatchGetDocumentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = rest_streaming.ResponseIterator(
                response, firestore.BatchGetDocumentsResponse
            )
            resp = self._interceptor.post_batch_get_documents(resp)
            return resp

    class _BatchWrite(FirestoreRestStub):
        def __hash__(self):
            return hash("BatchWrite")

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
            request: firestore.BatchWriteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> firestore.BatchWriteResponse:
            r"""Call the batch write method over HTTP.

            Args:
                request (~.firestore.BatchWriteRequest):
                    The request object. The request for
                [Firestore.BatchWrite][google.firestore.v1.Firestore.BatchWrite].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firestore.BatchWriteResponse:
                    The response from
                [Firestore.BatchWrite][google.firestore.v1.Firestore.BatchWrite].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{database=projects/*/databases/*}/documents:batchWrite",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_write(request, metadata)
            pb_request = firestore.BatchWriteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = firestore.BatchWriteResponse()
            pb_resp = firestore.BatchWriteResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_write(resp)
            return resp

    class _BeginTransaction(FirestoreRestStub):
        def __hash__(self):
            return hash("BeginTransaction")

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
            request: firestore.BeginTransactionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> firestore.BeginTransactionResponse:
            r"""Call the begin transaction method over HTTP.

            Args:
                request (~.firestore.BeginTransactionRequest):
                    The request object. The request for
                [Firestore.BeginTransaction][google.firestore.v1.Firestore.BeginTransaction].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firestore.BeginTransactionResponse:
                    The response for
                [Firestore.BeginTransaction][google.firestore.v1.Firestore.BeginTransaction].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{database=projects/*/databases/*}/documents:beginTransaction",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_begin_transaction(
                request, metadata
            )
            pb_request = firestore.BeginTransactionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = firestore.BeginTransactionResponse()
            pb_resp = firestore.BeginTransactionResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_begin_transaction(resp)
            return resp

    class _Commit(FirestoreRestStub):
        def __hash__(self):
            return hash("Commit")

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
            request: firestore.CommitRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> firestore.CommitResponse:
            r"""Call the commit method over HTTP.

            Args:
                request (~.firestore.CommitRequest):
                    The request object. The request for
                [Firestore.Commit][google.firestore.v1.Firestore.Commit].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firestore.CommitResponse:
                    The response for
                [Firestore.Commit][google.firestore.v1.Firestore.Commit].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{database=projects/*/databases/*}/documents:commit",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_commit(request, metadata)
            pb_request = firestore.CommitRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = firestore.CommitResponse()
            pb_resp = firestore.CommitResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_commit(resp)
            return resp

    class _CreateDocument(FirestoreRestStub):
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
            request: firestore.CreateDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document.Document:
            r"""Call the create document method over HTTP.

            Args:
                request (~.firestore.CreateDocumentRequest):
                    The request object. The request for
                [Firestore.CreateDocument][google.firestore.v1.Firestore.CreateDocument].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document.Document:
                    A Firestore document.
                Must not exceed 1 MiB - 4 bytes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/databases/*/documents/**}/{collection_id}",
                    "body": "document",
                },
            ]
            request, metadata = self._interceptor.pre_create_document(request, metadata)
            pb_request = firestore.CreateDocumentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = document.Document()
            pb_resp = document.Document.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_document(resp)
            return resp

    class _DeleteDocument(FirestoreRestStub):
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
            request: firestore.DeleteDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete document method over HTTP.

            Args:
                request (~.firestore.DeleteDocumentRequest):
                    The request object. The request for
                [Firestore.DeleteDocument][google.firestore.v1.Firestore.DeleteDocument].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/databases/*/documents/*/**}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_document(request, metadata)
            pb_request = firestore.DeleteDocumentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetDocument(FirestoreRestStub):
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
            request: firestore.GetDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document.Document:
            r"""Call the get document method over HTTP.

            Args:
                request (~.firestore.GetDocumentRequest):
                    The request object. The request for
                [Firestore.GetDocument][google.firestore.v1.Firestore.GetDocument].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.document.Document:
                    A Firestore document.
                Must not exceed 1 MiB - 4 bytes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/databases/*/documents/*/**}",
                },
            ]
            request, metadata = self._interceptor.pre_get_document(request, metadata)
            pb_request = firestore.GetDocumentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = document.Document()
            pb_resp = document.Document.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_document(resp)
            return resp

    class _ListCollectionIds(FirestoreRestStub):
        def __hash__(self):
            return hash("ListCollectionIds")

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
            request: firestore.ListCollectionIdsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> firestore.ListCollectionIdsResponse:
            r"""Call the list collection ids method over HTTP.

            Args:
                request (~.firestore.ListCollectionIdsRequest):
                    The request object. The request for
                [Firestore.ListCollectionIds][google.firestore.v1.Firestore.ListCollectionIds].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firestore.ListCollectionIdsResponse:
                    The response from
                [Firestore.ListCollectionIds][google.firestore.v1.Firestore.ListCollectionIds].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/databases/*/documents}:listCollectionIds",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/databases/*/documents/*/**}:listCollectionIds",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_list_collection_ids(
                request, metadata
            )
            pb_request = firestore.ListCollectionIdsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = firestore.ListCollectionIdsResponse()
            pb_resp = firestore.ListCollectionIdsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_collection_ids(resp)
            return resp

    class _ListDocuments(FirestoreRestStub):
        def __hash__(self):
            return hash("ListDocuments")

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
            request: firestore.ListDocumentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> firestore.ListDocumentsResponse:
            r"""Call the list documents method over HTTP.

            Args:
                request (~.firestore.ListDocumentsRequest):
                    The request object. The request for
                [Firestore.ListDocuments][google.firestore.v1.Firestore.ListDocuments].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firestore.ListDocumentsResponse:
                    The response for
                [Firestore.ListDocuments][google.firestore.v1.Firestore.ListDocuments].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/databases/*/documents/*/**}/{collection_id}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/databases/*/documents}/{collection_id}",
                },
            ]
            request, metadata = self._interceptor.pre_list_documents(request, metadata)
            pb_request = firestore.ListDocumentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = firestore.ListDocumentsResponse()
            pb_resp = firestore.ListDocumentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_documents(resp)
            return resp

    class _Listen(FirestoreRestStub):
        def __hash__(self):
            return hash("Listen")

        def __call__(
            self,
            request: firestore.ListenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            raise NotImplementedError(
                "Method Listen is not available over REST transport"
            )

    class _PartitionQuery(FirestoreRestStub):
        def __hash__(self):
            return hash("PartitionQuery")

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
            request: firestore.PartitionQueryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> firestore.PartitionQueryResponse:
            r"""Call the partition query method over HTTP.

            Args:
                request (~.firestore.PartitionQueryRequest):
                    The request object. The request for
                [Firestore.PartitionQuery][google.firestore.v1.Firestore.PartitionQuery].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firestore.PartitionQueryResponse:
                    The response for
                [Firestore.PartitionQuery][google.firestore.v1.Firestore.PartitionQuery].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/databases/*/documents}:partitionQuery",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/databases/*/documents/*/**}:partitionQuery",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_partition_query(request, metadata)
            pb_request = firestore.PartitionQueryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = firestore.PartitionQueryResponse()
            pb_resp = firestore.PartitionQueryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_partition_query(resp)
            return resp

    class _Rollback(FirestoreRestStub):
        def __hash__(self):
            return hash("Rollback")

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
            request: firestore.RollbackRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the rollback method over HTTP.

            Args:
                request (~.firestore.RollbackRequest):
                    The request object. The request for
                [Firestore.Rollback][google.firestore.v1.Firestore.Rollback].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{database=projects/*/databases/*}/documents:rollback",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rollback(request, metadata)
            pb_request = firestore.RollbackRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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

    class _RunAggregationQuery(FirestoreRestStub):
        def __hash__(self):
            return hash("RunAggregationQuery")

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
            request: firestore.RunAggregationQueryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the run aggregation query method over HTTP.

            Args:
                request (~.firestore.RunAggregationQueryRequest):
                    The request object. The request for
                [Firestore.RunAggregationQuery][google.firestore.v1.Firestore.RunAggregationQuery].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firestore.RunAggregationQueryResponse:
                    The response for
                [Firestore.RunAggregationQuery][google.firestore.v1.Firestore.RunAggregationQuery].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/databases/*/documents}:runAggregationQuery",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/databases/*/documents/*/**}:runAggregationQuery",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_run_aggregation_query(
                request, metadata
            )
            pb_request = firestore.RunAggregationQueryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = rest_streaming.ResponseIterator(
                response, firestore.RunAggregationQueryResponse
            )
            resp = self._interceptor.post_run_aggregation_query(resp)
            return resp

    class _RunQuery(FirestoreRestStub):
        def __hash__(self):
            return hash("RunQuery")

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
            request: firestore.RunQueryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the run query method over HTTP.

            Args:
                request (~.firestore.RunQueryRequest):
                    The request object. The request for
                [Firestore.RunQuery][google.firestore.v1.Firestore.RunQuery].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.firestore.RunQueryResponse:
                    The response for
                [Firestore.RunQuery][google.firestore.v1.Firestore.RunQuery].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/databases/*/documents}:runQuery",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/databases/*/documents/*/**}:runQuery",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_run_query(request, metadata)
            pb_request = firestore.RunQueryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = rest_streaming.ResponseIterator(response, firestore.RunQueryResponse)
            resp = self._interceptor.post_run_query(resp)
            return resp

    class _UpdateDocument(FirestoreRestStub):
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
            request: firestore.UpdateDocumentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gf_document.Document:
            r"""Call the update document method over HTTP.

            Args:
                request (~.firestore.UpdateDocumentRequest):
                    The request object. The request for
                [Firestore.UpdateDocument][google.firestore.v1.Firestore.UpdateDocument].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gf_document.Document:
                    A Firestore document.
                Must not exceed 1 MiB - 4 bytes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{document.name=projects/*/databases/*/documents/*/**}",
                    "body": "document",
                },
            ]
            request, metadata = self._interceptor.pre_update_document(request, metadata)
            pb_request = firestore.UpdateDocumentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = gf_document.Document()
            pb_resp = gf_document.Document.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_document(resp)
            return resp

    class _Write(FirestoreRestStub):
        def __hash__(self):
            return hash("Write")

        def __call__(
            self,
            request: firestore.WriteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            raise NotImplementedError(
                "Method Write is not available over REST transport"
            )

    @property
    def batch_get_documents(
        self,
    ) -> Callable[
        [firestore.BatchGetDocumentsRequest], firestore.BatchGetDocumentsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchGetDocuments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_write(
        self,
    ) -> Callable[[firestore.BatchWriteRequest], firestore.BatchWriteResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchWrite(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def begin_transaction(
        self,
    ) -> Callable[
        [firestore.BeginTransactionRequest], firestore.BeginTransactionResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BeginTransaction(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def commit(self) -> Callable[[firestore.CommitRequest], firestore.CommitResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Commit(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_document(
        self,
    ) -> Callable[[firestore.CreateDocumentRequest], document.Document]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_document(
        self,
    ) -> Callable[[firestore.DeleteDocumentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_document(
        self,
    ) -> Callable[[firestore.GetDocumentRequest], document.Document]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_collection_ids(
        self,
    ) -> Callable[
        [firestore.ListCollectionIdsRequest], firestore.ListCollectionIdsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCollectionIds(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_documents(
        self,
    ) -> Callable[[firestore.ListDocumentsRequest], firestore.ListDocumentsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDocuments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def listen(self) -> Callable[[firestore.ListenRequest], firestore.ListenResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Listen(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def partition_query(
        self,
    ) -> Callable[[firestore.PartitionQueryRequest], firestore.PartitionQueryResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PartitionQuery(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rollback(self) -> Callable[[firestore.RollbackRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Rollback(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_aggregation_query(
        self,
    ) -> Callable[
        [firestore.RunAggregationQueryRequest], firestore.RunAggregationQueryResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunAggregationQuery(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_query(
        self,
    ) -> Callable[[firestore.RunQueryRequest], firestore.RunQueryResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunQuery(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_document(
        self,
    ) -> Callable[[firestore.UpdateDocumentRequest], gf_document.Document]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDocument(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def write(self) -> Callable[[firestore.WriteRequest], firestore.WriteResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Write(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(FirestoreRestStub):
        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:

            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/databases/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.loads(json.dumps(transcoded_request["body"]))
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(FirestoreRestStub):
        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:

            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/databases/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(FirestoreRestStub):
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
                    "uri": "/v1/{name=projects/*/databases/*/operations/*}",
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
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(FirestoreRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/databases/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
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

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("FirestoreRestTransport",)
