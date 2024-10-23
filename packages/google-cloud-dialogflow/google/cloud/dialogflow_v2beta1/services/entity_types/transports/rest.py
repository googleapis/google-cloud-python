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

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dialogflow_v2beta1.types import entity_type as gcd_entity_type
from google.cloud.dialogflow_v2beta1.types import entity_type

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseEntityTypesRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class EntityTypesRestInterceptor:
    """Interceptor for EntityTypes.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the EntityTypesRestTransport.

    .. code-block:: python
        class MyCustomEntityTypesInterceptor(EntityTypesRestInterceptor):
            def pre_batch_create_entities(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_entities(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_delete_entities(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_delete_entities(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_delete_entity_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_delete_entity_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_update_entities(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_entities(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_update_entity_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_entity_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_entity_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_entity_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_entity_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_entity_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_entity_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_entity_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_entity_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_entity_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_entity_type(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = EntityTypesRestTransport(interceptor=MyCustomEntityTypesInterceptor())
        client = EntityTypesClient(transport=transport)


    """

    def pre_batch_create_entities(
        self,
        request: entity_type.BatchCreateEntitiesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[entity_type.BatchCreateEntitiesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_create_entities

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_batch_create_entities(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_create_entities

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_batch_delete_entities(
        self,
        request: entity_type.BatchDeleteEntitiesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[entity_type.BatchDeleteEntitiesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_delete_entities

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_batch_delete_entities(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_delete_entities

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_batch_delete_entity_types(
        self,
        request: entity_type.BatchDeleteEntityTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[entity_type.BatchDeleteEntityTypesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_delete_entity_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_batch_delete_entity_types(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_delete_entity_types

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_batch_update_entities(
        self,
        request: entity_type.BatchUpdateEntitiesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[entity_type.BatchUpdateEntitiesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_update_entities

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_batch_update_entities(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_update_entities

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_batch_update_entity_types(
        self,
        request: entity_type.BatchUpdateEntityTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[entity_type.BatchUpdateEntityTypesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_update_entity_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_batch_update_entity_types(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_update_entity_types

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_create_entity_type(
        self,
        request: gcd_entity_type.CreateEntityTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_entity_type.CreateEntityTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_entity_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_create_entity_type(
        self, response: gcd_entity_type.EntityType
    ) -> gcd_entity_type.EntityType:
        """Post-rpc interceptor for create_entity_type

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_delete_entity_type(
        self,
        request: entity_type.DeleteEntityTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[entity_type.DeleteEntityTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_entity_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def pre_get_entity_type(
        self,
        request: entity_type.GetEntityTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[entity_type.GetEntityTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_entity_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_get_entity_type(
        self, response: entity_type.EntityType
    ) -> entity_type.EntityType:
        """Post-rpc interceptor for get_entity_type

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_list_entity_types(
        self,
        request: entity_type.ListEntityTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[entity_type.ListEntityTypesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_entity_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_list_entity_types(
        self, response: entity_type.ListEntityTypesResponse
    ) -> entity_type.ListEntityTypesResponse:
        """Post-rpc interceptor for list_entity_types

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_update_entity_type(
        self,
        request: gcd_entity_type.UpdateEntityTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_entity_type.UpdateEntityTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_entity_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_update_entity_type(
        self, response: gcd_entity_type.EntityType
    ) -> gcd_entity_type.EntityType:
        """Post-rpc interceptor for update_entity_type

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
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
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
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
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
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
        before they are sent to the EntityTypes server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the EntityTypes server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class EntityTypesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: EntityTypesRestInterceptor


class EntityTypesRestTransport(_BaseEntityTypesRestTransport):
    """REST backend synchronous transport for EntityTypes.

    Service for managing
    [EntityTypes][google.cloud.dialogflow.v2beta1.EntityType].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[EntityTypesRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or EntityTypesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v2beta1/{name=projects/*/operations/*}:cancel",
                    },
                    {
                        "method": "post",
                        "uri": "/v2beta1/{name=projects/*/locations/*/operations/*}:cancel",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchCreateEntities(
        _BaseEntityTypesRestTransport._BaseBatchCreateEntities, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.BatchCreateEntities")

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
            request: entity_type.BatchCreateEntitiesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch create entities method over HTTP.

            Args:
                request (~.entity_type.BatchCreateEntitiesRequest):
                    The request object. The request message for
                [EntityTypes.BatchCreateEntities][google.cloud.dialogflow.v2beta1.EntityTypes.BatchCreateEntities].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseBatchCreateEntities._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_create_entities(
                request, metadata
            )
            transcoded_request = _BaseEntityTypesRestTransport._BaseBatchCreateEntities._get_transcoded_request(
                http_options, request
            )

            body = _BaseEntityTypesRestTransport._BaseBatchCreateEntities._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseBatchCreateEntities._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._BatchCreateEntities._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_create_entities(resp)
            return resp

    class _BatchDeleteEntities(
        _BaseEntityTypesRestTransport._BaseBatchDeleteEntities, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.BatchDeleteEntities")

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
            request: entity_type.BatchDeleteEntitiesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch delete entities method over HTTP.

            Args:
                request (~.entity_type.BatchDeleteEntitiesRequest):
                    The request object. The request message for
                [EntityTypes.BatchDeleteEntities][google.cloud.dialogflow.v2beta1.EntityTypes.BatchDeleteEntities].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseBatchDeleteEntities._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_delete_entities(
                request, metadata
            )
            transcoded_request = _BaseEntityTypesRestTransport._BaseBatchDeleteEntities._get_transcoded_request(
                http_options, request
            )

            body = _BaseEntityTypesRestTransport._BaseBatchDeleteEntities._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseBatchDeleteEntities._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._BatchDeleteEntities._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_delete_entities(resp)
            return resp

    class _BatchDeleteEntityTypes(
        _BaseEntityTypesRestTransport._BaseBatchDeleteEntityTypes, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.BatchDeleteEntityTypes")

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
            request: entity_type.BatchDeleteEntityTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch delete entity types method over HTTP.

            Args:
                request (~.entity_type.BatchDeleteEntityTypesRequest):
                    The request object. The request message for
                [EntityTypes.BatchDeleteEntityTypes][google.cloud.dialogflow.v2beta1.EntityTypes.BatchDeleteEntityTypes].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseBatchDeleteEntityTypes._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_delete_entity_types(
                request, metadata
            )
            transcoded_request = _BaseEntityTypesRestTransport._BaseBatchDeleteEntityTypes._get_transcoded_request(
                http_options, request
            )

            body = _BaseEntityTypesRestTransport._BaseBatchDeleteEntityTypes._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseBatchDeleteEntityTypes._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._BatchDeleteEntityTypes._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_delete_entity_types(resp)
            return resp

    class _BatchUpdateEntities(
        _BaseEntityTypesRestTransport._BaseBatchUpdateEntities, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.BatchUpdateEntities")

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
            request: entity_type.BatchUpdateEntitiesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch update entities method over HTTP.

            Args:
                request (~.entity_type.BatchUpdateEntitiesRequest):
                    The request object. The request message for
                [EntityTypes.BatchUpdateEntities][google.cloud.dialogflow.v2beta1.EntityTypes.BatchUpdateEntities].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseBatchUpdateEntities._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_update_entities(
                request, metadata
            )
            transcoded_request = _BaseEntityTypesRestTransport._BaseBatchUpdateEntities._get_transcoded_request(
                http_options, request
            )

            body = _BaseEntityTypesRestTransport._BaseBatchUpdateEntities._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseBatchUpdateEntities._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._BatchUpdateEntities._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_update_entities(resp)
            return resp

    class _BatchUpdateEntityTypes(
        _BaseEntityTypesRestTransport._BaseBatchUpdateEntityTypes, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.BatchUpdateEntityTypes")

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
            request: entity_type.BatchUpdateEntityTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch update entity types method over HTTP.

            Args:
                request (~.entity_type.BatchUpdateEntityTypesRequest):
                    The request object. The request message for
                [EntityTypes.BatchUpdateEntityTypes][google.cloud.dialogflow.v2beta1.EntityTypes.BatchUpdateEntityTypes].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseBatchUpdateEntityTypes._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_update_entity_types(
                request, metadata
            )
            transcoded_request = _BaseEntityTypesRestTransport._BaseBatchUpdateEntityTypes._get_transcoded_request(
                http_options, request
            )

            body = _BaseEntityTypesRestTransport._BaseBatchUpdateEntityTypes._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseBatchUpdateEntityTypes._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._BatchUpdateEntityTypes._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_update_entity_types(resp)
            return resp

    class _CreateEntityType(
        _BaseEntityTypesRestTransport._BaseCreateEntityType, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.CreateEntityType")

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
            request: gcd_entity_type.CreateEntityTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_entity_type.EntityType:
            r"""Call the create entity type method over HTTP.

            Args:
                request (~.gcd_entity_type.CreateEntityTypeRequest):
                    The request object. The request message for
                [EntityTypes.CreateEntityType][google.cloud.dialogflow.v2beta1.EntityTypes.CreateEntityType].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_entity_type.EntityType:
                    Each intent parameter has a type, called the entity
                type, which dictates exactly how data from an end-user
                expression is extracted.

                Dialogflow provides predefined system entities that can
                match many common types of data. For example, there are
                system entities for matching dates, times, colors, email
                addresses, and so on. You can also create your own
                custom entities for matching custom data. For example,
                you could define a vegetable entity that can match the
                types of vegetables available for purchase with a
                grocery store agent.

                For more information, see the `Entity
                guide <https://cloud.google.com/dialogflow/docs/entities-overview>`__.

            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseCreateEntityType._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_entity_type(
                request, metadata
            )
            transcoded_request = _BaseEntityTypesRestTransport._BaseCreateEntityType._get_transcoded_request(
                http_options, request
            )

            body = _BaseEntityTypesRestTransport._BaseCreateEntityType._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseCreateEntityType._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._CreateEntityType._get_response(
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
            resp = gcd_entity_type.EntityType()
            pb_resp = gcd_entity_type.EntityType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_entity_type(resp)
            return resp

    class _DeleteEntityType(
        _BaseEntityTypesRestTransport._BaseDeleteEntityType, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.DeleteEntityType")

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
            request: entity_type.DeleteEntityTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete entity type method over HTTP.

            Args:
                request (~.entity_type.DeleteEntityTypeRequest):
                    The request object. The request message for
                [EntityTypes.DeleteEntityType][google.cloud.dialogflow.v2beta1.EntityTypes.DeleteEntityType].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseDeleteEntityType._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_entity_type(
                request, metadata
            )
            transcoded_request = _BaseEntityTypesRestTransport._BaseDeleteEntityType._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseDeleteEntityType._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._DeleteEntityType._get_response(
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

    class _GetEntityType(
        _BaseEntityTypesRestTransport._BaseGetEntityType, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.GetEntityType")

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
            request: entity_type.GetEntityTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> entity_type.EntityType:
            r"""Call the get entity type method over HTTP.

            Args:
                request (~.entity_type.GetEntityTypeRequest):
                    The request object. The request message for
                [EntityTypes.GetEntityType][google.cloud.dialogflow.v2beta1.EntityTypes.GetEntityType].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.entity_type.EntityType:
                    Each intent parameter has a type, called the entity
                type, which dictates exactly how data from an end-user
                expression is extracted.

                Dialogflow provides predefined system entities that can
                match many common types of data. For example, there are
                system entities for matching dates, times, colors, email
                addresses, and so on. You can also create your own
                custom entities for matching custom data. For example,
                you could define a vegetable entity that can match the
                types of vegetables available for purchase with a
                grocery store agent.

                For more information, see the `Entity
                guide <https://cloud.google.com/dialogflow/docs/entities-overview>`__.

            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseGetEntityType._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_entity_type(request, metadata)
            transcoded_request = _BaseEntityTypesRestTransport._BaseGetEntityType._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseEntityTypesRestTransport._BaseGetEntityType._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EntityTypesRestTransport._GetEntityType._get_response(
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
            resp = entity_type.EntityType()
            pb_resp = entity_type.EntityType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_entity_type(resp)
            return resp

    class _ListEntityTypes(
        _BaseEntityTypesRestTransport._BaseListEntityTypes, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.ListEntityTypes")

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
            request: entity_type.ListEntityTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> entity_type.ListEntityTypesResponse:
            r"""Call the list entity types method over HTTP.

            Args:
                request (~.entity_type.ListEntityTypesRequest):
                    The request object. The request message for
                [EntityTypes.ListEntityTypes][google.cloud.dialogflow.v2beta1.EntityTypes.ListEntityTypes].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.entity_type.ListEntityTypesResponse:
                    The response message for
                [EntityTypes.ListEntityTypes][google.cloud.dialogflow.v2beta1.EntityTypes.ListEntityTypes].

            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseListEntityTypes._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_entity_types(
                request, metadata
            )
            transcoded_request = _BaseEntityTypesRestTransport._BaseListEntityTypes._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseListEntityTypes._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._ListEntityTypes._get_response(
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
            resp = entity_type.ListEntityTypesResponse()
            pb_resp = entity_type.ListEntityTypesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_entity_types(resp)
            return resp

    class _UpdateEntityType(
        _BaseEntityTypesRestTransport._BaseUpdateEntityType, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.UpdateEntityType")

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
            request: gcd_entity_type.UpdateEntityTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_entity_type.EntityType:
            r"""Call the update entity type method over HTTP.

            Args:
                request (~.gcd_entity_type.UpdateEntityTypeRequest):
                    The request object. The request message for
                [EntityTypes.UpdateEntityType][google.cloud.dialogflow.v2beta1.EntityTypes.UpdateEntityType].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_entity_type.EntityType:
                    Each intent parameter has a type, called the entity
                type, which dictates exactly how data from an end-user
                expression is extracted.

                Dialogflow provides predefined system entities that can
                match many common types of data. For example, there are
                system entities for matching dates, times, colors, email
                addresses, and so on. You can also create your own
                custom entities for matching custom data. For example,
                you could define a vegetable entity that can match the
                types of vegetables available for purchase with a
                grocery store agent.

                For more information, see the `Entity
                guide <https://cloud.google.com/dialogflow/docs/entities-overview>`__.

            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseUpdateEntityType._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_entity_type(
                request, metadata
            )
            transcoded_request = _BaseEntityTypesRestTransport._BaseUpdateEntityType._get_transcoded_request(
                http_options, request
            )

            body = _BaseEntityTypesRestTransport._BaseUpdateEntityType._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseUpdateEntityType._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._UpdateEntityType._get_response(
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
            resp = gcd_entity_type.EntityType()
            pb_resp = gcd_entity_type.EntityType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_entity_type(resp)
            return resp

    @property
    def batch_create_entities(
        self,
    ) -> Callable[[entity_type.BatchCreateEntitiesRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateEntities(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_delete_entities(
        self,
    ) -> Callable[[entity_type.BatchDeleteEntitiesRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchDeleteEntities(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_delete_entity_types(
        self,
    ) -> Callable[
        [entity_type.BatchDeleteEntityTypesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchDeleteEntityTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_update_entities(
        self,
    ) -> Callable[[entity_type.BatchUpdateEntitiesRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateEntities(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_update_entity_types(
        self,
    ) -> Callable[
        [entity_type.BatchUpdateEntityTypesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateEntityTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_entity_type(
        self,
    ) -> Callable[
        [gcd_entity_type.CreateEntityTypeRequest], gcd_entity_type.EntityType
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEntityType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_entity_type(
        self,
    ) -> Callable[[entity_type.DeleteEntityTypeRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEntityType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_entity_type(
        self,
    ) -> Callable[[entity_type.GetEntityTypeRequest], entity_type.EntityType]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEntityType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_entity_types(
        self,
    ) -> Callable[
        [entity_type.ListEntityTypesRequest], entity_type.ListEntityTypesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEntityTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_entity_type(
        self,
    ) -> Callable[
        [gcd_entity_type.UpdateEntityTypeRequest], gcd_entity_type.EntityType
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEntityType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseEntityTypesRestTransport._BaseGetLocation, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.GetLocation")

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
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseEntityTypesRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEntityTypesRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EntityTypesRestTransport._GetLocation._get_response(
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
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseEntityTypesRestTransport._BaseListLocations, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.ListLocations")

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
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseEntityTypesRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseEntityTypesRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseEntityTypesRestTransport._BaseListLocations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EntityTypesRestTransport._ListLocations._get_response(
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
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseEntityTypesRestTransport._BaseCancelOperation, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.CancelOperation")

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

            http_options = (
                _BaseEntityTypesRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseEntityTypesRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseEntityTypesRestTransport._BaseGetOperation, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.GetOperation")

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
                _BaseEntityTypesRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseEntityTypesRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEntityTypesRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EntityTypesRestTransport._GetOperation._get_response(
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
        _BaseEntityTypesRestTransport._BaseListOperations, EntityTypesRestStub
    ):
        def __hash__(self):
            return hash("EntityTypesRestTransport.ListOperations")

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
                _BaseEntityTypesRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseEntityTypesRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEntityTypesRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EntityTypesRestTransport._ListOperations._get_response(
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


__all__ = ("EntityTypesRestTransport",)
