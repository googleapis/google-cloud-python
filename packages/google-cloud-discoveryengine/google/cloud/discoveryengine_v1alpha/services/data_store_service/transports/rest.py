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

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.discoveryengine_v1alpha.types import data_store as gcd_data_store
from google.cloud.discoveryengine_v1alpha.types import document_processing_config
from google.cloud.discoveryengine_v1alpha.types import (
    document_processing_config as gcd_document_processing_config,
)
from google.cloud.discoveryengine_v1alpha.types import data_store
from google.cloud.discoveryengine_v1alpha.types import data_store_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import DataStoreServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class DataStoreServiceRestInterceptor:
    """Interceptor for DataStoreService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DataStoreServiceRestTransport.

    .. code-block:: python
        class MyCustomDataStoreServiceInterceptor(DataStoreServiceRestInterceptor):
            def pre_create_data_store(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_data_store(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_data_store(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_data_store(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_data_store(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_store(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_document_processing_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_document_processing_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_data_stores(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_data_stores(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_data_store(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_data_store(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_document_processing_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_document_processing_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DataStoreServiceRestTransport(interceptor=MyCustomDataStoreServiceInterceptor())
        client = DataStoreServiceClient(transport=transport)


    """

    def pre_create_data_store(
        self,
        request: data_store_service.CreateDataStoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[data_store_service.CreateDataStoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_data_store

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataStoreService server.
        """
        return request, metadata

    def post_create_data_store(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_data_store

        Override in a subclass to manipulate the response
        after it is returned by the DataStoreService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_data_store(
        self,
        request: data_store_service.DeleteDataStoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[data_store_service.DeleteDataStoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_data_store

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataStoreService server.
        """
        return request, metadata

    def post_delete_data_store(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_data_store

        Override in a subclass to manipulate the response
        after it is returned by the DataStoreService server but before
        it is returned to user code.
        """
        return response

    def pre_get_data_store(
        self,
        request: data_store_service.GetDataStoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[data_store_service.GetDataStoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_data_store

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataStoreService server.
        """
        return request, metadata

    def post_get_data_store(
        self, response: data_store.DataStore
    ) -> data_store.DataStore:
        """Post-rpc interceptor for get_data_store

        Override in a subclass to manipulate the response
        after it is returned by the DataStoreService server but before
        it is returned to user code.
        """
        return response

    def pre_get_document_processing_config(
        self,
        request: data_store_service.GetDocumentProcessingConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        data_store_service.GetDocumentProcessingConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_document_processing_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataStoreService server.
        """
        return request, metadata

    def post_get_document_processing_config(
        self, response: document_processing_config.DocumentProcessingConfig
    ) -> document_processing_config.DocumentProcessingConfig:
        """Post-rpc interceptor for get_document_processing_config

        Override in a subclass to manipulate the response
        after it is returned by the DataStoreService server but before
        it is returned to user code.
        """
        return response

    def pre_list_data_stores(
        self,
        request: data_store_service.ListDataStoresRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[data_store_service.ListDataStoresRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_data_stores

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataStoreService server.
        """
        return request, metadata

    def post_list_data_stores(
        self, response: data_store_service.ListDataStoresResponse
    ) -> data_store_service.ListDataStoresResponse:
        """Post-rpc interceptor for list_data_stores

        Override in a subclass to manipulate the response
        after it is returned by the DataStoreService server but before
        it is returned to user code.
        """
        return response

    def pre_update_data_store(
        self,
        request: data_store_service.UpdateDataStoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[data_store_service.UpdateDataStoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_data_store

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataStoreService server.
        """
        return request, metadata

    def post_update_data_store(
        self, response: gcd_data_store.DataStore
    ) -> gcd_data_store.DataStore:
        """Post-rpc interceptor for update_data_store

        Override in a subclass to manipulate the response
        after it is returned by the DataStoreService server but before
        it is returned to user code.
        """
        return response

    def pre_update_document_processing_config(
        self,
        request: data_store_service.UpdateDocumentProcessingConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        data_store_service.UpdateDocumentProcessingConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_document_processing_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataStoreService server.
        """
        return request, metadata

    def post_update_document_processing_config(
        self, response: gcd_document_processing_config.DocumentProcessingConfig
    ) -> gcd_document_processing_config.DocumentProcessingConfig:
        """Post-rpc interceptor for update_document_processing_config

        Override in a subclass to manipulate the response
        after it is returned by the DataStoreService server but before
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
        before they are sent to the DataStoreService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the DataStoreService server but before
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
        before they are sent to the DataStoreService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the DataStoreService server but before
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
        before they are sent to the DataStoreService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the DataStoreService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DataStoreServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DataStoreServiceRestInterceptor


class DataStoreServiceRestTransport(DataStoreServiceTransport):
    """REST backend transport for DataStoreService.

    Service for managing
    [DataStore][google.cloud.discoveryengine.v1alpha.DataStore]
    configuration.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "discoveryengine.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DataStoreServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'discoveryengine.googleapis.com').
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or DataStoreServiceRestInterceptor()
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
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}:cancel",
                        "body": "*",
                    },
                    {
                        "method": "post",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataConnector/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/models/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/engines/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/models/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/evaluations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/sampleQuerySets/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataConnector}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/models/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/engines/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/collections/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/branches/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/models/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*/locations/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha/{name=projects/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1alpha",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateDataStore(DataStoreServiceRestStub):
        def __hash__(self):
            return hash("CreateDataStore")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "dataStoreId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: data_store_service.CreateDataStoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create data store method over HTTP.

            Args:
                request (~.data_store_service.CreateDataStoreRequest):
                    The request object. Request for
                [DataStoreService.CreateDataStore][google.cloud.discoveryengine.v1alpha.DataStoreService.CreateDataStore]
                method.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/dataStores",
                    "body": "data_store",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/collections/*}/dataStores",
                    "body": "data_store",
                },
            ]
            request, metadata = self._interceptor.pre_create_data_store(
                request, metadata
            )
            pb_request = data_store_service.CreateDataStoreRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_data_store(resp)
            return resp

    class _DeleteDataStore(DataStoreServiceRestStub):
        def __hash__(self):
            return hash("DeleteDataStore")

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
            request: data_store_service.DeleteDataStoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete data store method over HTTP.

            Args:
                request (~.data_store_service.DeleteDataStoreRequest):
                    The request object. Request message for
                [DataStoreService.DeleteDataStore][google.cloud.discoveryengine.v1alpha.DataStoreService.DeleteDataStore]
                method.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_data_store(
                request, metadata
            )
            pb_request = data_store_service.DeleteDataStoreRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

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
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_data_store(resp)
            return resp

    class _GetDataStore(DataStoreServiceRestStub):
        def __hash__(self):
            return hash("GetDataStore")

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
            request: data_store_service.GetDataStoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> data_store.DataStore:
            r"""Call the get data store method over HTTP.

            Args:
                request (~.data_store_service.GetDataStoreRequest):
                    The request object. Request message for
                [DataStoreService.GetDataStore][google.cloud.discoveryengine.v1alpha.DataStoreService.GetDataStore]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.data_store.DataStore:
                    DataStore captures global settings
                and configs at the DataStore level.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_data_store(request, metadata)
            pb_request = data_store_service.GetDataStoreRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

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
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = data_store.DataStore()
            pb_resp = data_store.DataStore.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_data_store(resp)
            return resp

    class _GetDocumentProcessingConfig(DataStoreServiceRestStub):
        def __hash__(self):
            return hash("GetDocumentProcessingConfig")

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
            request: data_store_service.GetDocumentProcessingConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> document_processing_config.DocumentProcessingConfig:
            r"""Call the get document processing
            config method over HTTP.

                Args:
                    request (~.data_store_service.GetDocumentProcessingConfigRequest):
                        The request object. Request for
                    [DataStoreService.GetDocumentProcessingConfig][google.cloud.discoveryengine.v1alpha.DataStoreService.GetDocumentProcessingConfig]
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.document_processing_config.DocumentProcessingConfig:
                        A singleton resource of
                    [DataStore][google.cloud.discoveryengine.v1alpha.DataStore].
                    It's empty when
                    [DataStore][google.cloud.discoveryengine.v1alpha.DataStore]
                    is created, which defaults to digital parser. The first
                    call to
                    [DataStoreService.UpdateDocumentProcessingConfig][google.cloud.discoveryengine.v1alpha.DataStoreService.UpdateDocumentProcessingConfig]
                    method will initialize the config.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/documentProcessingConfig}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/documentProcessingConfig}",
                },
            ]
            request, metadata = self._interceptor.pre_get_document_processing_config(
                request, metadata
            )
            pb_request = data_store_service.GetDocumentProcessingConfigRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

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
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = document_processing_config.DocumentProcessingConfig()
            pb_resp = document_processing_config.DocumentProcessingConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_document_processing_config(resp)
            return resp

    class _ListDataStores(DataStoreServiceRestStub):
        def __hash__(self):
            return hash("ListDataStores")

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
            request: data_store_service.ListDataStoresRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> data_store_service.ListDataStoresResponse:
            r"""Call the list data stores method over HTTP.

            Args:
                request (~.data_store_service.ListDataStoresRequest):
                    The request object. Request message for
                [DataStoreService.ListDataStores][google.cloud.discoveryengine.v1alpha.DataStoreService.ListDataStores]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.data_store_service.ListDataStoresResponse:
                    Response message for
                [DataStoreService.ListDataStores][google.cloud.discoveryengine.v1alpha.DataStoreService.ListDataStores]
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*}/dataStores",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=projects/*/locations/*/collections/*}/dataStores",
                },
            ]
            request, metadata = self._interceptor.pre_list_data_stores(
                request, metadata
            )
            pb_request = data_store_service.ListDataStoresRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

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
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = data_store_service.ListDataStoresResponse()
            pb_resp = data_store_service.ListDataStoresResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_data_stores(resp)
            return resp

    class _UpdateDataStore(DataStoreServiceRestStub):
        def __hash__(self):
            return hash("UpdateDataStore")

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
            request: data_store_service.UpdateDataStoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_data_store.DataStore:
            r"""Call the update data store method over HTTP.

            Args:
                request (~.data_store_service.UpdateDataStoreRequest):
                    The request object. Request message for
                [DataStoreService.UpdateDataStore][google.cloud.discoveryengine.v1alpha.DataStoreService.UpdateDataStore]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_data_store.DataStore:
                    DataStore captures global settings
                and configs at the DataStore level.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{data_store.name=projects/*/locations/*/dataStores/*}",
                    "body": "data_store",
                },
                {
                    "method": "patch",
                    "uri": "/v1alpha/{data_store.name=projects/*/locations/*/collections/*/dataStores/*}",
                    "body": "data_store",
                },
            ]
            request, metadata = self._interceptor.pre_update_data_store(
                request, metadata
            )
            pb_request = data_store_service.UpdateDataStoreRequest.pb(request)
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
            resp = gcd_data_store.DataStore()
            pb_resp = gcd_data_store.DataStore.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_data_store(resp)
            return resp

    class _UpdateDocumentProcessingConfig(DataStoreServiceRestStub):
        def __hash__(self):
            return hash("UpdateDocumentProcessingConfig")

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
            request: data_store_service.UpdateDocumentProcessingConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_document_processing_config.DocumentProcessingConfig:
            r"""Call the update document
            processing config method over HTTP.

                Args:
                    request (~.data_store_service.UpdateDocumentProcessingConfigRequest):
                        The request object. Request for
                    [DataStoreService.UpdateDocumentProcessingConfig][google.cloud.discoveryengine.v1alpha.DataStoreService.UpdateDocumentProcessingConfig]
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcd_document_processing_config.DocumentProcessingConfig:
                        A singleton resource of
                    [DataStore][google.cloud.discoveryengine.v1alpha.DataStore].
                    It's empty when
                    [DataStore][google.cloud.discoveryengine.v1alpha.DataStore]
                    is created, which defaults to digital parser. The first
                    call to
                    [DataStoreService.UpdateDocumentProcessingConfig][google.cloud.discoveryengine.v1alpha.DataStoreService.UpdateDocumentProcessingConfig]
                    method will initialize the config.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{document_processing_config.name=projects/*/locations/*/dataStores/*/documentProcessingConfig}",
                    "body": "document_processing_config",
                },
                {
                    "method": "patch",
                    "uri": "/v1alpha/{document_processing_config.name=projects/*/locations/*/collections/*/dataStores/*/documentProcessingConfig}",
                    "body": "document_processing_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_document_processing_config(
                request, metadata
            )
            pb_request = data_store_service.UpdateDocumentProcessingConfigRequest.pb(
                request
            )
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
            resp = gcd_document_processing_config.DocumentProcessingConfig()
            pb_resp = gcd_document_processing_config.DocumentProcessingConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_document_processing_config(resp)
            return resp

    @property
    def create_data_store(
        self,
    ) -> Callable[
        [data_store_service.CreateDataStoreRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDataStore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_data_store(
        self,
    ) -> Callable[
        [data_store_service.DeleteDataStoreRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDataStore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_data_store(
        self,
    ) -> Callable[[data_store_service.GetDataStoreRequest], data_store.DataStore]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataStore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_document_processing_config(
        self,
    ) -> Callable[
        [data_store_service.GetDocumentProcessingConfigRequest],
        document_processing_config.DocumentProcessingConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDocumentProcessingConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_data_stores(
        self,
    ) -> Callable[
        [data_store_service.ListDataStoresRequest],
        data_store_service.ListDataStoresResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDataStores(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_data_store(
        self,
    ) -> Callable[
        [data_store_service.UpdateDataStoreRequest], gcd_data_store.DataStore
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDataStore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_document_processing_config(
        self,
    ) -> Callable[
        [data_store_service.UpdateDocumentProcessingConfigRequest],
        gcd_document_processing_config.DocumentProcessingConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDocumentProcessingConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(DataStoreServiceRestStub):
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}:cancel",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
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
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(DataStoreServiceRestStub):
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataConnector/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/models/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/engines/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/branches/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/models/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/evaluations/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/sampleQuerySets/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/operations/*}",
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

    class _ListOperations(DataStoreServiceRestStub):
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
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataConnector}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/branches/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/models/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/schemas/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine/targetSites}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/dataStores/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*/engines/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/collections/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/branches/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*/models/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*/dataStores/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*/locations/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=projects/*}/operations",
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


__all__ = ("DataStoreServiceRestTransport",)
