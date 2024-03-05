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
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.gke_multicloud_v1.types import azure_resources, azure_service

from .base import AzureClustersTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AzureClustersRestInterceptor:
    """Interceptor for AzureClusters.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AzureClustersRestTransport.

    .. code-block:: python
        class MyCustomAzureClustersInterceptor(AzureClustersRestInterceptor):
            def pre_create_azure_client(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_azure_client(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_azure_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_azure_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_azure_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_azure_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_azure_client(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_azure_client(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_azure_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_azure_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_azure_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_azure_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_azure_access_token(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_azure_access_token(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_azure_cluster_agent_token(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_azure_cluster_agent_token(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_azure_client(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_azure_client(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_azure_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_azure_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_azure_json_web_keys(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_azure_json_web_keys(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_azure_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_azure_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_azure_open_id_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_azure_open_id_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_azure_server_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_azure_server_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_azure_clients(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_azure_clients(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_azure_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_azure_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_azure_node_pools(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_azure_node_pools(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_azure_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_azure_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_azure_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_azure_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AzureClustersRestTransport(interceptor=MyCustomAzureClustersInterceptor())
        client = AzureClustersClient(transport=transport)


    """

    def pre_create_azure_client(
        self,
        request: azure_service.CreateAzureClientRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.CreateAzureClientRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_azure_client

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_create_azure_client(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_azure_client

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_create_azure_cluster(
        self,
        request: azure_service.CreateAzureClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.CreateAzureClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_azure_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_create_azure_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_azure_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_create_azure_node_pool(
        self,
        request: azure_service.CreateAzureNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.CreateAzureNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_azure_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_create_azure_node_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_azure_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_delete_azure_client(
        self,
        request: azure_service.DeleteAzureClientRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.DeleteAzureClientRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_azure_client

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_delete_azure_client(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_azure_client

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_delete_azure_cluster(
        self,
        request: azure_service.DeleteAzureClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.DeleteAzureClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_azure_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_delete_azure_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_azure_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_delete_azure_node_pool(
        self,
        request: azure_service.DeleteAzureNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.DeleteAzureNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_azure_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_delete_azure_node_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_azure_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_generate_azure_access_token(
        self,
        request: azure_service.GenerateAzureAccessTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        azure_service.GenerateAzureAccessTokenRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for generate_azure_access_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_generate_azure_access_token(
        self, response: azure_service.GenerateAzureAccessTokenResponse
    ) -> azure_service.GenerateAzureAccessTokenResponse:
        """Post-rpc interceptor for generate_azure_access_token

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_generate_azure_cluster_agent_token(
        self,
        request: azure_service.GenerateAzureClusterAgentTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        azure_service.GenerateAzureClusterAgentTokenRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for generate_azure_cluster_agent_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_generate_azure_cluster_agent_token(
        self, response: azure_service.GenerateAzureClusterAgentTokenResponse
    ) -> azure_service.GenerateAzureClusterAgentTokenResponse:
        """Post-rpc interceptor for generate_azure_cluster_agent_token

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_azure_client(
        self,
        request: azure_service.GetAzureClientRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.GetAzureClientRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_azure_client

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_get_azure_client(
        self, response: azure_resources.AzureClient
    ) -> azure_resources.AzureClient:
        """Post-rpc interceptor for get_azure_client

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_azure_cluster(
        self,
        request: azure_service.GetAzureClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.GetAzureClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_azure_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_get_azure_cluster(
        self, response: azure_resources.AzureCluster
    ) -> azure_resources.AzureCluster:
        """Post-rpc interceptor for get_azure_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_azure_json_web_keys(
        self,
        request: azure_service.GetAzureJsonWebKeysRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.GetAzureJsonWebKeysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_azure_json_web_keys

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_get_azure_json_web_keys(
        self, response: azure_resources.AzureJsonWebKeys
    ) -> azure_resources.AzureJsonWebKeys:
        """Post-rpc interceptor for get_azure_json_web_keys

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_azure_node_pool(
        self,
        request: azure_service.GetAzureNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.GetAzureNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_azure_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_get_azure_node_pool(
        self, response: azure_resources.AzureNodePool
    ) -> azure_resources.AzureNodePool:
        """Post-rpc interceptor for get_azure_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_azure_open_id_config(
        self,
        request: azure_service.GetAzureOpenIdConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.GetAzureOpenIdConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_azure_open_id_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_get_azure_open_id_config(
        self, response: azure_resources.AzureOpenIdConfig
    ) -> azure_resources.AzureOpenIdConfig:
        """Post-rpc interceptor for get_azure_open_id_config

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_azure_server_config(
        self,
        request: azure_service.GetAzureServerConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.GetAzureServerConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_azure_server_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_get_azure_server_config(
        self, response: azure_resources.AzureServerConfig
    ) -> azure_resources.AzureServerConfig:
        """Post-rpc interceptor for get_azure_server_config

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_list_azure_clients(
        self,
        request: azure_service.ListAzureClientsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.ListAzureClientsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_azure_clients

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_list_azure_clients(
        self, response: azure_service.ListAzureClientsResponse
    ) -> azure_service.ListAzureClientsResponse:
        """Post-rpc interceptor for list_azure_clients

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_list_azure_clusters(
        self,
        request: azure_service.ListAzureClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.ListAzureClustersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_azure_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_list_azure_clusters(
        self, response: azure_service.ListAzureClustersResponse
    ) -> azure_service.ListAzureClustersResponse:
        """Post-rpc interceptor for list_azure_clusters

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_list_azure_node_pools(
        self,
        request: azure_service.ListAzureNodePoolsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.ListAzureNodePoolsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_azure_node_pools

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_list_azure_node_pools(
        self, response: azure_service.ListAzureNodePoolsResponse
    ) -> azure_service.ListAzureNodePoolsResponse:
        """Post-rpc interceptor for list_azure_node_pools

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_update_azure_cluster(
        self,
        request: azure_service.UpdateAzureClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.UpdateAzureClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_azure_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_update_azure_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_azure_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response

    def pre_update_azure_node_pool(
        self,
        request: azure_service.UpdateAzureNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[azure_service.UpdateAzureNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_azure_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_update_azure_node_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_azure_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
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
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
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
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
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
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
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
        before they are sent to the AzureClusters server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the AzureClusters server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AzureClustersRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AzureClustersRestInterceptor


class AzureClustersRestTransport(AzureClustersTransport):
    """REST backend transport for AzureClusters.

    The AzureClusters API provides a single centrally managed
    service to create and manage Anthos clusters that run on Azure
    infrastructure.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    NOTE: This REST transport functionality is currently in a beta
    state (preview). We welcome your feedback via an issue in this
    library's source repository. Thank you!
    """

    def __init__(
        self,
        *,
        host: str = "gkemulticloud.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AzureClustersRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to (default: 'gkemulticloud.googleapis.com').
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
        self._interceptor = interceptor or AzureClustersRestInterceptor()
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
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateAzureClient(AzureClustersRestStub):
        def __hash__(self):
            return hash("CreateAzureClient")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "azureClientId": "",
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
            request: azure_service.CreateAzureClientRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create azure client method over HTTP.

            Args:
                request (~.azure_service.CreateAzureClientRequest):
                    The request object. Request message for ``AzureClusters.CreateAzureClient``
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
                    "uri": "/v1/{parent=projects/*/locations/*}/azureClients",
                    "body": "azure_client",
                },
            ]
            request, metadata = self._interceptor.pre_create_azure_client(
                request, metadata
            )
            pb_request = azure_service.CreateAzureClientRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_create_azure_client(resp)
            return resp

    class _CreateAzureCluster(AzureClustersRestStub):
        def __hash__(self):
            return hash("CreateAzureCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "azureClusterId": "",
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
            request: azure_service.CreateAzureClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create azure cluster method over HTTP.

            Args:
                request (~.azure_service.CreateAzureClusterRequest):
                    The request object. Request message for ``AzureClusters.CreateAzureCluster``
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
                    "uri": "/v1/{parent=projects/*/locations/*}/azureClusters",
                    "body": "azure_cluster",
                },
            ]
            request, metadata = self._interceptor.pre_create_azure_cluster(
                request, metadata
            )
            pb_request = azure_service.CreateAzureClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_create_azure_cluster(resp)
            return resp

    class _CreateAzureNodePool(AzureClustersRestStub):
        def __hash__(self):
            return hash("CreateAzureNodePool")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "azureNodePoolId": "",
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
            request: azure_service.CreateAzureNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create azure node pool method over HTTP.

            Args:
                request (~.azure_service.CreateAzureNodePoolRequest):
                    The request object. Response message for
                ``AzureClusters.CreateAzureNodePool`` method.
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
                    "uri": "/v1/{parent=projects/*/locations/*/azureClusters/*}/azureNodePools",
                    "body": "azure_node_pool",
                },
            ]
            request, metadata = self._interceptor.pre_create_azure_node_pool(
                request, metadata
            )
            pb_request = azure_service.CreateAzureNodePoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_create_azure_node_pool(resp)
            return resp

    class _DeleteAzureClient(AzureClustersRestStub):
        def __hash__(self):
            return hash("DeleteAzureClient")

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
            request: azure_service.DeleteAzureClientRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete azure client method over HTTP.

            Args:
                request (~.azure_service.DeleteAzureClientRequest):
                    The request object. Request message for ``AzureClusters.DeleteAzureClient``
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
                    "uri": "/v1/{name=projects/*/locations/*/azureClients/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_azure_client(
                request, metadata
            )
            pb_request = azure_service.DeleteAzureClientRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_delete_azure_client(resp)
            return resp

    class _DeleteAzureCluster(AzureClustersRestStub):
        def __hash__(self):
            return hash("DeleteAzureCluster")

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
            request: azure_service.DeleteAzureClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete azure cluster method over HTTP.

            Args:
                request (~.azure_service.DeleteAzureClusterRequest):
                    The request object. Request message for ``AzureClusters.DeleteAzureCluster``
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
                    "uri": "/v1/{name=projects/*/locations/*/azureClusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_azure_cluster(
                request, metadata
            )
            pb_request = azure_service.DeleteAzureClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_delete_azure_cluster(resp)
            return resp

    class _DeleteAzureNodePool(AzureClustersRestStub):
        def __hash__(self):
            return hash("DeleteAzureNodePool")

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
            request: azure_service.DeleteAzureNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete azure node pool method over HTTP.

            Args:
                request (~.azure_service.DeleteAzureNodePoolRequest):
                    The request object. Request message for
                ``AzureClusters.DeleteAzureNodePool`` method.
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
                    "uri": "/v1/{name=projects/*/locations/*/azureClusters/*/azureNodePools/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_azure_node_pool(
                request, metadata
            )
            pb_request = azure_service.DeleteAzureNodePoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_delete_azure_node_pool(resp)
            return resp

    class _GenerateAzureAccessToken(AzureClustersRestStub):
        def __hash__(self):
            return hash("GenerateAzureAccessToken")

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
            request: azure_service.GenerateAzureAccessTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_service.GenerateAzureAccessTokenResponse:
            r"""Call the generate azure access
            token method over HTTP.

                Args:
                    request (~.azure_service.GenerateAzureAccessTokenRequest):
                        The request object. Request message for
                    ``AzureClusters.GenerateAzureAccessToken`` method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.azure_service.GenerateAzureAccessTokenResponse:
                        Response message for
                    ``AzureClusters.GenerateAzureAccessToken`` method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{azure_cluster=projects/*/locations/*/azureClusters/*}:generateAzureAccessToken",
                },
            ]
            request, metadata = self._interceptor.pre_generate_azure_access_token(
                request, metadata
            )
            pb_request = azure_service.GenerateAzureAccessTokenRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_service.GenerateAzureAccessTokenResponse()
            pb_resp = azure_service.GenerateAzureAccessTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_azure_access_token(resp)
            return resp

    class _GenerateAzureClusterAgentToken(AzureClustersRestStub):
        def __hash__(self):
            return hash("GenerateAzureClusterAgentToken")

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
            request: azure_service.GenerateAzureClusterAgentTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_service.GenerateAzureClusterAgentTokenResponse:
            r"""Call the generate azure cluster
            agent token method over HTTP.

                Args:
                    request (~.azure_service.GenerateAzureClusterAgentTokenRequest):
                        The request object.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.azure_service.GenerateAzureClusterAgentTokenResponse:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{azure_cluster=projects/*/locations/*/azureClusters/*}:generateAzureClusterAgentToken",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_generate_azure_cluster_agent_token(
                request, metadata
            )
            pb_request = azure_service.GenerateAzureClusterAgentTokenRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_service.GenerateAzureClusterAgentTokenResponse()
            pb_resp = azure_service.GenerateAzureClusterAgentTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_azure_cluster_agent_token(resp)
            return resp

    class _GetAzureClient(AzureClustersRestStub):
        def __hash__(self):
            return hash("GetAzureClient")

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
            request: azure_service.GetAzureClientRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_resources.AzureClient:
            r"""Call the get azure client method over HTTP.

            Args:
                request (~.azure_service.GetAzureClientRequest):
                    The request object. Request message for ``AzureClusters.GetAzureClient``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.azure_resources.AzureClient:
                    ``AzureClient`` resources hold client authentication
                information needed by the Anthos Multi-Cloud API to
                manage Azure resources on your Azure subscription.

                When an
                [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                is created, an ``AzureClient`` resource needs to be
                provided and all operations on Azure resources
                associated to that cluster will authenticate to Azure
                services using the given client.

                ``AzureClient`` resources are immutable and cannot be
                modified upon creation.

                Each ``AzureClient`` resource is bound to a single Azure
                Active Directory Application and tenant.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/azureClients/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_azure_client(
                request, metadata
            )
            pb_request = azure_service.GetAzureClientRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_resources.AzureClient()
            pb_resp = azure_resources.AzureClient.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_azure_client(resp)
            return resp

    class _GetAzureCluster(AzureClustersRestStub):
        def __hash__(self):
            return hash("GetAzureCluster")

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
            request: azure_service.GetAzureClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_resources.AzureCluster:
            r"""Call the get azure cluster method over HTTP.

            Args:
                request (~.azure_service.GetAzureClusterRequest):
                    The request object. Request message for ``AzureClusters.GetAzureCluster``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.azure_resources.AzureCluster:
                    An Anthos cluster running on Azure.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/azureClusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_azure_cluster(
                request, metadata
            )
            pb_request = azure_service.GetAzureClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_resources.AzureCluster()
            pb_resp = azure_resources.AzureCluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_azure_cluster(resp)
            return resp

    class _GetAzureJsonWebKeys(AzureClustersRestStub):
        def __hash__(self):
            return hash("GetAzureJsonWebKeys")

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
            request: azure_service.GetAzureJsonWebKeysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_resources.AzureJsonWebKeys:
            r"""Call the get azure json web keys method over HTTP.

            Args:
                request (~.azure_service.GetAzureJsonWebKeysRequest):
                    The request object. GetAzureJsonWebKeysRequest gets the public component of
                the keys used by the cluster to sign token requests.
                This will be the jwks_uri for the discover document
                returned by getOpenIDConfig. See the OpenID Connect
                Discovery 1.0 specification for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.azure_resources.AzureJsonWebKeys:
                    AzureJsonWebKeys is a valid JSON Web
                Key Set as specififed in RFC 7517.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{azure_cluster=projects/*/locations/*/azureClusters/*}/jwks",
                },
            ]
            request, metadata = self._interceptor.pre_get_azure_json_web_keys(
                request, metadata
            )
            pb_request = azure_service.GetAzureJsonWebKeysRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_resources.AzureJsonWebKeys()
            pb_resp = azure_resources.AzureJsonWebKeys.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_azure_json_web_keys(resp)
            return resp

    class _GetAzureNodePool(AzureClustersRestStub):
        def __hash__(self):
            return hash("GetAzureNodePool")

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
            request: azure_service.GetAzureNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_resources.AzureNodePool:
            r"""Call the get azure node pool method over HTTP.

            Args:
                request (~.azure_service.GetAzureNodePoolRequest):
                    The request object. Request message for ``AzureClusters.GetAzureNodePool``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.azure_resources.AzureNodePool:
                    An Anthos node pool running on Azure.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/azureClusters/*/azureNodePools/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_azure_node_pool(
                request, metadata
            )
            pb_request = azure_service.GetAzureNodePoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_resources.AzureNodePool()
            pb_resp = azure_resources.AzureNodePool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_azure_node_pool(resp)
            return resp

    class _GetAzureOpenIdConfig(AzureClustersRestStub):
        def __hash__(self):
            return hash("GetAzureOpenIdConfig")

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
            request: azure_service.GetAzureOpenIdConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_resources.AzureOpenIdConfig:
            r"""Call the get azure open id config method over HTTP.

            Args:
                request (~.azure_service.GetAzureOpenIdConfigRequest):
                    The request object. GetAzureOpenIdConfigRequest gets the
                OIDC discovery document for the cluster.
                See the OpenID Connect Discovery 1.0
                specification for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.azure_resources.AzureOpenIdConfig:
                    AzureOpenIdConfig is an OIDC
                discovery document for the cluster. See
                the OpenID Connect Discovery 1.0
                specification for details.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{azure_cluster=projects/*/locations/*/azureClusters/*}/.well-known/openid-configuration",
                },
            ]
            request, metadata = self._interceptor.pre_get_azure_open_id_config(
                request, metadata
            )
            pb_request = azure_service.GetAzureOpenIdConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_resources.AzureOpenIdConfig()
            pb_resp = azure_resources.AzureOpenIdConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_azure_open_id_config(resp)
            return resp

    class _GetAzureServerConfig(AzureClustersRestStub):
        def __hash__(self):
            return hash("GetAzureServerConfig")

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
            request: azure_service.GetAzureServerConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_resources.AzureServerConfig:
            r"""Call the get azure server config method over HTTP.

            Args:
                request (~.azure_service.GetAzureServerConfigRequest):
                    The request object. GetAzureServerConfigRequest gets the
                server config of GKE cluster on Azure.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.azure_resources.AzureServerConfig:
                    AzureServerConfig contains
                information about a Google Cloud
                location, such as supported Azure
                regions and Kubernetes versions.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/azureServerConfig}",
                },
            ]
            request, metadata = self._interceptor.pre_get_azure_server_config(
                request, metadata
            )
            pb_request = azure_service.GetAzureServerConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_resources.AzureServerConfig()
            pb_resp = azure_resources.AzureServerConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_azure_server_config(resp)
            return resp

    class _ListAzureClients(AzureClustersRestStub):
        def __hash__(self):
            return hash("ListAzureClients")

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
            request: azure_service.ListAzureClientsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_service.ListAzureClientsResponse:
            r"""Call the list azure clients method over HTTP.

            Args:
                request (~.azure_service.ListAzureClientsRequest):
                    The request object. Request message for ``AzureClusters.ListAzureClients``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.azure_service.ListAzureClientsResponse:
                    Response message for ``AzureClusters.ListAzureClients``
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/azureClients",
                },
            ]
            request, metadata = self._interceptor.pre_list_azure_clients(
                request, metadata
            )
            pb_request = azure_service.ListAzureClientsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_service.ListAzureClientsResponse()
            pb_resp = azure_service.ListAzureClientsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_azure_clients(resp)
            return resp

    class _ListAzureClusters(AzureClustersRestStub):
        def __hash__(self):
            return hash("ListAzureClusters")

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
            request: azure_service.ListAzureClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_service.ListAzureClustersResponse:
            r"""Call the list azure clusters method over HTTP.

            Args:
                request (~.azure_service.ListAzureClustersRequest):
                    The request object. Request message for ``AzureClusters.ListAzureClusters``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.azure_service.ListAzureClustersResponse:
                    Response message for ``AzureClusters.ListAzureClusters``
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/azureClusters",
                },
            ]
            request, metadata = self._interceptor.pre_list_azure_clusters(
                request, metadata
            )
            pb_request = azure_service.ListAzureClustersRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_service.ListAzureClustersResponse()
            pb_resp = azure_service.ListAzureClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_azure_clusters(resp)
            return resp

    class _ListAzureNodePools(AzureClustersRestStub):
        def __hash__(self):
            return hash("ListAzureNodePools")

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
            request: azure_service.ListAzureNodePoolsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> azure_service.ListAzureNodePoolsResponse:
            r"""Call the list azure node pools method over HTTP.

            Args:
                request (~.azure_service.ListAzureNodePoolsRequest):
                    The request object. Request message for ``AzureClusters.ListAzureNodePools``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.azure_service.ListAzureNodePoolsResponse:
                    Response message for
                ``AzureClusters.ListAzureNodePools`` method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/azureClusters/*}/azureNodePools",
                },
            ]
            request, metadata = self._interceptor.pre_list_azure_node_pools(
                request, metadata
            )
            pb_request = azure_service.ListAzureNodePoolsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = azure_service.ListAzureNodePoolsResponse()
            pb_resp = azure_service.ListAzureNodePoolsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_azure_node_pools(resp)
            return resp

    class _UpdateAzureCluster(AzureClustersRestStub):
        def __hash__(self):
            return hash("UpdateAzureCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: azure_service.UpdateAzureClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update azure cluster method over HTTP.

            Args:
                request (~.azure_service.UpdateAzureClusterRequest):
                    The request object. Request message for ``AzureClusters.UpdateAzureCluster``
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
                    "method": "patch",
                    "uri": "/v1/{azure_cluster.name=projects/*/locations/*/azureClusters/*}",
                    "body": "azure_cluster",
                },
            ]
            request, metadata = self._interceptor.pre_update_azure_cluster(
                request, metadata
            )
            pb_request = azure_service.UpdateAzureClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_update_azure_cluster(resp)
            return resp

    class _UpdateAzureNodePool(AzureClustersRestStub):
        def __hash__(self):
            return hash("UpdateAzureNodePool")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: azure_service.UpdateAzureNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update azure node pool method over HTTP.

            Args:
                request (~.azure_service.UpdateAzureNodePoolRequest):
                    The request object. Request message for
                ``AzureClusters.UpdateAzureNodePool`` method.
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
                    "method": "patch",
                    "uri": "/v1/{azure_node_pool.name=projects/*/locations/*/azureClusters/*/azureNodePools/*}",
                    "body": "azure_node_pool",
                },
            ]
            request, metadata = self._interceptor.pre_update_azure_node_pool(
                request, metadata
            )
            pb_request = azure_service.UpdateAzureNodePoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_update_azure_node_pool(resp)
            return resp

    @property
    def create_azure_client(
        self,
    ) -> Callable[[azure_service.CreateAzureClientRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAzureClient(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_azure_cluster(
        self,
    ) -> Callable[[azure_service.CreateAzureClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAzureCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_azure_node_pool(
        self,
    ) -> Callable[[azure_service.CreateAzureNodePoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAzureNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_azure_client(
        self,
    ) -> Callable[[azure_service.DeleteAzureClientRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAzureClient(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_azure_cluster(
        self,
    ) -> Callable[[azure_service.DeleteAzureClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAzureCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_azure_node_pool(
        self,
    ) -> Callable[[azure_service.DeleteAzureNodePoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAzureNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_azure_access_token(
        self,
    ) -> Callable[
        [azure_service.GenerateAzureAccessTokenRequest],
        azure_service.GenerateAzureAccessTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateAzureAccessToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_azure_cluster_agent_token(
        self,
    ) -> Callable[
        [azure_service.GenerateAzureClusterAgentTokenRequest],
        azure_service.GenerateAzureClusterAgentTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateAzureClusterAgentToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_azure_client(
        self,
    ) -> Callable[[azure_service.GetAzureClientRequest], azure_resources.AzureClient]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAzureClient(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_azure_cluster(
        self,
    ) -> Callable[[azure_service.GetAzureClusterRequest], azure_resources.AzureCluster]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAzureCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_azure_json_web_keys(
        self,
    ) -> Callable[
        [azure_service.GetAzureJsonWebKeysRequest], azure_resources.AzureJsonWebKeys
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAzureJsonWebKeys(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_azure_node_pool(
        self,
    ) -> Callable[
        [azure_service.GetAzureNodePoolRequest], azure_resources.AzureNodePool
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAzureNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_azure_open_id_config(
        self,
    ) -> Callable[
        [azure_service.GetAzureOpenIdConfigRequest], azure_resources.AzureOpenIdConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAzureOpenIdConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_azure_server_config(
        self,
    ) -> Callable[
        [azure_service.GetAzureServerConfigRequest], azure_resources.AzureServerConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAzureServerConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_azure_clients(
        self,
    ) -> Callable[
        [azure_service.ListAzureClientsRequest], azure_service.ListAzureClientsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAzureClients(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_azure_clusters(
        self,
    ) -> Callable[
        [azure_service.ListAzureClustersRequest],
        azure_service.ListAzureClustersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAzureClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_azure_node_pools(
        self,
    ) -> Callable[
        [azure_service.ListAzureNodePoolsRequest],
        azure_service.ListAzureNodePoolsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAzureNodePools(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_azure_cluster(
        self,
    ) -> Callable[[azure_service.UpdateAzureClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAzureCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_azure_node_pool(
        self,
    ) -> Callable[[azure_service.UpdateAzureNodePoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAzureNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(AzureClustersRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
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
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(AzureClustersRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
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

    class _GetOperation(AzureClustersRestStub):
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
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(AzureClustersRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
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


__all__ = ("AzureClustersRestTransport",)
