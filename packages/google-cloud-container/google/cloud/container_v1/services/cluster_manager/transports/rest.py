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


from google.protobuf import empty_pb2  # type: ignore

from google.cloud.container_v1.types import cluster_service

from .base import ClusterManagerTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ClusterManagerRestInterceptor:
    """Interceptor for ClusterManager.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ClusterManagerRestTransport.

    .. code-block:: python
        class MyCustomClusterManagerInterceptor(ClusterManagerRestInterceptor):
            def pre_cancel_operation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_check_autopilot_compatibility(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_check_autopilot_compatibility(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_complete_ip_rotation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_complete_ip_rotation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_complete_node_pool_upgrade(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_create_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_json_web_keys(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_json_web_keys(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_operation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_operation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_server_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_server_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_node_pools(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_node_pools(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_operations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_operations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_usable_subnetworks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_usable_subnetworks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rollback_node_pool_upgrade(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rollback_node_pool_upgrade(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_addons_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_addons_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_labels(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_labels(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_legacy_abac(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_legacy_abac(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_locations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_locations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_logging_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_logging_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_maintenance_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_maintenance_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_master_auth(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_master_auth(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_monitoring_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_monitoring_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_network_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_network_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_node_pool_autoscaling(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_node_pool_autoscaling(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_node_pool_management(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_node_pool_management(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_node_pool_size(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_node_pool_size(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_ip_rotation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_ip_rotation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_master(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_master(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ClusterManagerRestTransport(interceptor=MyCustomClusterManagerInterceptor())
        client = ClusterManagerClient(transport=transport)


    """

    def pre_cancel_operation(
        self,
        request: cluster_service.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def pre_check_autopilot_compatibility(
        self,
        request: cluster_service.CheckAutopilotCompatibilityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        cluster_service.CheckAutopilotCompatibilityRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for check_autopilot_compatibility

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_check_autopilot_compatibility(
        self, response: cluster_service.CheckAutopilotCompatibilityResponse
    ) -> cluster_service.CheckAutopilotCompatibilityResponse:
        """Post-rpc interceptor for check_autopilot_compatibility

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_complete_ip_rotation(
        self,
        request: cluster_service.CompleteIPRotationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.CompleteIPRotationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for complete_ip_rotation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_complete_ip_rotation(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for complete_ip_rotation

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_complete_node_pool_upgrade(
        self,
        request: cluster_service.CompleteNodePoolUpgradeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        cluster_service.CompleteNodePoolUpgradeRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for complete_node_pool_upgrade

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def pre_create_cluster(
        self,
        request: cluster_service.CreateClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.CreateClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_create_cluster(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for create_cluster

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_node_pool(
        self,
        request: cluster_service.CreateNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.CreateNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_create_node_pool(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for create_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_cluster(
        self,
        request: cluster_service.DeleteClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.DeleteClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_delete_cluster(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for delete_cluster

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_node_pool(
        self,
        request: cluster_service.DeleteNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.DeleteNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_delete_node_pool(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for delete_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_cluster(
        self,
        request: cluster_service.GetClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.GetClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_get_cluster(
        self, response: cluster_service.Cluster
    ) -> cluster_service.Cluster:
        """Post-rpc interceptor for get_cluster

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_json_web_keys(
        self,
        request: cluster_service.GetJSONWebKeysRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.GetJSONWebKeysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_json_web_keys

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_get_json_web_keys(
        self, response: cluster_service.GetJSONWebKeysResponse
    ) -> cluster_service.GetJSONWebKeysResponse:
        """Post-rpc interceptor for get_json_web_keys

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_node_pool(
        self,
        request: cluster_service.GetNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.GetNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_get_node_pool(
        self, response: cluster_service.NodePool
    ) -> cluster_service.NodePool:
        """Post-rpc interceptor for get_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: cluster_service.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_get_operation(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_server_config(
        self,
        request: cluster_service.GetServerConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.GetServerConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_server_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_get_server_config(
        self, response: cluster_service.ServerConfig
    ) -> cluster_service.ServerConfig:
        """Post-rpc interceptor for get_server_config

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_clusters(
        self,
        request: cluster_service.ListClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.ListClustersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_list_clusters(
        self, response: cluster_service.ListClustersResponse
    ) -> cluster_service.ListClustersResponse:
        """Post-rpc interceptor for list_clusters

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_node_pools(
        self,
        request: cluster_service.ListNodePoolsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.ListNodePoolsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_node_pools

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_list_node_pools(
        self, response: cluster_service.ListNodePoolsResponse
    ) -> cluster_service.ListNodePoolsResponse:
        """Post-rpc interceptor for list_node_pools

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: cluster_service.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_list_operations(
        self, response: cluster_service.ListOperationsResponse
    ) -> cluster_service.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_usable_subnetworks(
        self,
        request: cluster_service.ListUsableSubnetworksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.ListUsableSubnetworksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_usable_subnetworks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_list_usable_subnetworks(
        self, response: cluster_service.ListUsableSubnetworksResponse
    ) -> cluster_service.ListUsableSubnetworksResponse:
        """Post-rpc interceptor for list_usable_subnetworks

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_rollback_node_pool_upgrade(
        self,
        request: cluster_service.RollbackNodePoolUpgradeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        cluster_service.RollbackNodePoolUpgradeRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for rollback_node_pool_upgrade

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_rollback_node_pool_upgrade(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for rollback_node_pool_upgrade

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_addons_config(
        self,
        request: cluster_service.SetAddonsConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetAddonsConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_addons_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_addons_config(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_addons_config

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_labels(
        self,
        request: cluster_service.SetLabelsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetLabelsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_labels

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_labels(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_labels

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_legacy_abac(
        self,
        request: cluster_service.SetLegacyAbacRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetLegacyAbacRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_legacy_abac

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_legacy_abac(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_legacy_abac

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_locations(
        self,
        request: cluster_service.SetLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_locations(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_locations

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_logging_service(
        self,
        request: cluster_service.SetLoggingServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetLoggingServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_logging_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_logging_service(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_logging_service

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_maintenance_policy(
        self,
        request: cluster_service.SetMaintenancePolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetMaintenancePolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_maintenance_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_maintenance_policy(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_maintenance_policy

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_master_auth(
        self,
        request: cluster_service.SetMasterAuthRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetMasterAuthRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_master_auth

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_master_auth(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_master_auth

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_monitoring_service(
        self,
        request: cluster_service.SetMonitoringServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetMonitoringServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_monitoring_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_monitoring_service(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_monitoring_service

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_network_policy(
        self,
        request: cluster_service.SetNetworkPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetNetworkPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_network_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_network_policy(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_network_policy

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_node_pool_autoscaling(
        self,
        request: cluster_service.SetNodePoolAutoscalingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        cluster_service.SetNodePoolAutoscalingRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for set_node_pool_autoscaling

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_node_pool_autoscaling(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_node_pool_autoscaling

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_node_pool_management(
        self,
        request: cluster_service.SetNodePoolManagementRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetNodePoolManagementRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_node_pool_management

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_node_pool_management(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_node_pool_management

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_node_pool_size(
        self,
        request: cluster_service.SetNodePoolSizeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.SetNodePoolSizeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_node_pool_size

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_set_node_pool_size(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for set_node_pool_size

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_start_ip_rotation(
        self,
        request: cluster_service.StartIPRotationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.StartIPRotationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for start_ip_rotation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_start_ip_rotation(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for start_ip_rotation

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_cluster(
        self,
        request: cluster_service.UpdateClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.UpdateClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_update_cluster(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for update_cluster

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_master(
        self,
        request: cluster_service.UpdateMasterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.UpdateMasterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_master

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_update_master(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for update_master

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_node_pool(
        self,
        request: cluster_service.UpdateNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cluster_service.UpdateNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ClusterManager server.
        """
        return request, metadata

    def post_update_node_pool(
        self, response: cluster_service.Operation
    ) -> cluster_service.Operation:
        """Post-rpc interceptor for update_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the ClusterManager server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ClusterManagerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ClusterManagerRestInterceptor


class ClusterManagerRestTransport(ClusterManagerTransport):
    """REST backend transport for ClusterManager.

    Google Kubernetes Engine Cluster Manager v1

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "container.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ClusterManagerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'container.googleapis.com').
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
        self._interceptor = interceptor or ClusterManagerRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CancelOperation(ClusterManagerRestStub):
        def __hash__(self):
            return hash("CancelOperation")

        def __call__(
            self,
            request: cluster_service.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the cancel operation method over HTTP.

            Args:
                request (~.cluster_service.CancelOperationRequest):
                    The request object. CancelOperationRequest cancels a
                single operation.
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
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/operations/{operation_id}:cancel",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            pb_request = cluster_service.CancelOperationRequest.pb(request)
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

    class _CheckAutopilotCompatibility(ClusterManagerRestStub):
        def __hash__(self):
            return hash("CheckAutopilotCompatibility")

        def __call__(
            self,
            request: cluster_service.CheckAutopilotCompatibilityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.CheckAutopilotCompatibilityResponse:
            r"""Call the check autopilot
            compatibility method over HTTP.

                Args:
                    request (~.cluster_service.CheckAutopilotCompatibilityRequest):
                        The request object. CheckAutopilotCompatibilityRequest
                    requests getting the blockers for the
                    given operation in the cluster.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.cluster_service.CheckAutopilotCompatibilityResponse:
                        CheckAutopilotCompatibilityResponse
                    has a list of compatibility issues.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:checkAutopilotCompatibility",
                },
            ]
            request, metadata = self._interceptor.pre_check_autopilot_compatibility(
                request, metadata
            )
            pb_request = cluster_service.CheckAutopilotCompatibilityRequest.pb(request)
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
            resp = cluster_service.CheckAutopilotCompatibilityResponse()
            pb_resp = cluster_service.CheckAutopilotCompatibilityResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_check_autopilot_compatibility(resp)
            return resp

    class _CompleteIPRotation(ClusterManagerRestStub):
        def __hash__(self):
            return hash("CompleteIPRotation")

        def __call__(
            self,
            request: cluster_service.CompleteIPRotationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the complete ip rotation method over HTTP.

            Args:
                request (~.cluster_service.CompleteIPRotationRequest):
                    The request object. CompleteIPRotationRequest moves the
                cluster master back into single-IP mode.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:completeIpRotation",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}:completeIpRotation",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_complete_ip_rotation(
                request, metadata
            )
            pb_request = cluster_service.CompleteIPRotationRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_complete_ip_rotation(resp)
            return resp

    class _CompleteNodePoolUpgrade(ClusterManagerRestStub):
        def __hash__(self):
            return hash("CompleteNodePoolUpgrade")

        def __call__(
            self,
            request: cluster_service.CompleteNodePoolUpgradeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the complete node pool
            upgrade method over HTTP.

                Args:
                    request (~.cluster_service.CompleteNodePoolUpgradeRequest):
                        The request object. CompleteNodePoolUpgradeRequest sets
                    the name of target node pool to complete
                    upgrade.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/nodePools/*}:completeUpgrade",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_complete_node_pool_upgrade(
                request, metadata
            )
            pb_request = cluster_service.CompleteNodePoolUpgradeRequest.pb(request)
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

    class _CreateCluster(ClusterManagerRestStub):
        def __hash__(self):
            return hash("CreateCluster")

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
            request: cluster_service.CreateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the create cluster method over HTTP.

            Args:
                request (~.cluster_service.CreateClusterRequest):
                    The request object. CreateClusterRequest creates a
                cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/clusters",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_create_cluster(request, metadata)
            pb_request = cluster_service.CreateClusterRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_cluster(resp)
            return resp

    class _CreateNodePool(ClusterManagerRestStub):
        def __hash__(self):
            return hash("CreateNodePool")

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
            request: cluster_service.CreateNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the create node pool method over HTTP.

            Args:
                request (~.cluster_service.CreateNodePoolRequest):
                    The request object. CreateNodePoolRequest creates a node
                pool for a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/clusters/*}/nodePools",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/nodePools",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_create_node_pool(
                request, metadata
            )
            pb_request = cluster_service.CreateNodePoolRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_node_pool(resp)
            return resp

    class _DeleteCluster(ClusterManagerRestStub):
        def __hash__(self):
            return hash("DeleteCluster")

        def __call__(
            self,
            request: cluster_service.DeleteClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the delete cluster method over HTTP.

            Args:
                request (~.cluster_service.DeleteClusterRequest):
                    The request object. DeleteClusterRequest deletes a
                cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_cluster(request, metadata)
            pb_request = cluster_service.DeleteClusterRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_cluster(resp)
            return resp

    class _DeleteNodePool(ClusterManagerRestStub):
        def __hash__(self):
            return hash("DeleteNodePool")

        def __call__(
            self,
            request: cluster_service.DeleteNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the delete node pool method over HTTP.

            Args:
                request (~.cluster_service.DeleteNodePoolRequest):
                    The request object. DeleteNodePoolRequest deletes a node
                pool for a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/nodePools/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/nodePools/{node_pool_id}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_node_pool(
                request, metadata
            )
            pb_request = cluster_service.DeleteNodePoolRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_node_pool(resp)
            return resp

    class _GetCluster(ClusterManagerRestStub):
        def __hash__(self):
            return hash("GetCluster")

        def __call__(
            self,
            request: cluster_service.GetClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Cluster:
            r"""Call the get cluster method over HTTP.

            Args:
                request (~.cluster_service.GetClusterRequest):
                    The request object. GetClusterRequest gets the settings
                of a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Cluster:
                    A Google Kubernetes Engine cluster.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}",
                },
            ]
            request, metadata = self._interceptor.pre_get_cluster(request, metadata)
            pb_request = cluster_service.GetClusterRequest.pb(request)
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
            resp = cluster_service.Cluster()
            pb_resp = cluster_service.Cluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_cluster(resp)
            return resp

    class _GetJSONWebKeys(ClusterManagerRestStub):
        def __hash__(self):
            return hash("GetJSONWebKeys")

        def __call__(
            self,
            request: cluster_service.GetJSONWebKeysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.GetJSONWebKeysResponse:
            r"""Call the get json web keys method over HTTP.

            Args:
                request (~.cluster_service.GetJSONWebKeysRequest):
                    The request object. GetJSONWebKeysRequest gets the public component of the
                keys used by the cluster to sign token requests. This
                will be the jwks_uri for the discover document returned
                by getOpenIDConfig. See the OpenID Connect Discovery 1.0
                specification for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.GetJSONWebKeysResponse:
                    GetJSONWebKeysResponse is a valid
                JSON Web Key Set as specififed in rfc
                7517

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/clusters/*}/jwks",
                },
            ]
            request, metadata = self._interceptor.pre_get_json_web_keys(
                request, metadata
            )
            pb_request = cluster_service.GetJSONWebKeysRequest.pb(request)
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
            resp = cluster_service.GetJSONWebKeysResponse()
            pb_resp = cluster_service.GetJSONWebKeysResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_json_web_keys(resp)
            return resp

    class _GetNodePool(ClusterManagerRestStub):
        def __hash__(self):
            return hash("GetNodePool")

        def __call__(
            self,
            request: cluster_service.GetNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.NodePool:
            r"""Call the get node pool method over HTTP.

            Args:
                request (~.cluster_service.GetNodePoolRequest):
                    The request object. GetNodePoolRequest retrieves a node
                pool for a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.NodePool:
                    NodePool contains the name and
                configuration for a cluster's node pool.
                Node pools are a set of nodes (i.e.
                VM's), with a common configuration and
                specification, under the control of the
                cluster master. They may have a set of
                Kubernetes labels applied to them, which
                may be used to reference them during pod
                scheduling. They may also be resized up
                or down, to accommodate the workload.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/nodePools/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/nodePools/{node_pool_id}",
                },
            ]
            request, metadata = self._interceptor.pre_get_node_pool(request, metadata)
            pb_request = cluster_service.GetNodePoolRequest.pb(request)
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
            resp = cluster_service.NodePool()
            pb_resp = cluster_service.NodePool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_node_pool(resp)
            return resp

    class _GetOperation(ClusterManagerRestStub):
        def __hash__(self):
            return hash("GetOperation")

        def __call__(
            self,
            request: cluster_service.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (~.cluster_service.GetOperationRequest):
                    The request object. GetOperationRequest gets a single
                operation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/operations/{operation_id}",
                },
            ]
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            pb_request = cluster_service.GetOperationRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    class _GetServerConfig(ClusterManagerRestStub):
        def __hash__(self):
            return hash("GetServerConfig")

        def __call__(
            self,
            request: cluster_service.GetServerConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.ServerConfig:
            r"""Call the get server config method over HTTP.

            Args:
                request (~.cluster_service.GetServerConfigRequest):
                    The request object. Gets the current Kubernetes Engine
                service configuration.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.ServerConfig:
                    Kubernetes Engine service
                configuration.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}/serverConfig",
                },
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/serverconfig",
                },
            ]
            request, metadata = self._interceptor.pre_get_server_config(
                request, metadata
            )
            pb_request = cluster_service.GetServerConfigRequest.pb(request)
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
            resp = cluster_service.ServerConfig()
            pb_resp = cluster_service.ServerConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_server_config(resp)
            return resp

    class _ListClusters(ClusterManagerRestStub):
        def __hash__(self):
            return hash("ListClusters")

        def __call__(
            self,
            request: cluster_service.ListClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.ListClustersResponse:
            r"""Call the list clusters method over HTTP.

            Args:
                request (~.cluster_service.ListClustersRequest):
                    The request object. ListClustersRequest lists clusters.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.ListClustersResponse:
                    ListClustersResponse is the result of
                ListClustersRequest.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/clusters",
                },
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters",
                },
            ]
            request, metadata = self._interceptor.pre_list_clusters(request, metadata)
            pb_request = cluster_service.ListClustersRequest.pb(request)
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
            resp = cluster_service.ListClustersResponse()
            pb_resp = cluster_service.ListClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_clusters(resp)
            return resp

    class _ListNodePools(ClusterManagerRestStub):
        def __hash__(self):
            return hash("ListNodePools")

        def __call__(
            self,
            request: cluster_service.ListNodePoolsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.ListNodePoolsResponse:
            r"""Call the list node pools method over HTTP.

            Args:
                request (~.cluster_service.ListNodePoolsRequest):
                    The request object. ListNodePoolsRequest lists the node
                pool(s) for a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.ListNodePoolsResponse:
                    ListNodePoolsResponse is the result
                of ListNodePoolsRequest.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/clusters/*}/nodePools",
                },
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/nodePools",
                },
            ]
            request, metadata = self._interceptor.pre_list_node_pools(request, metadata)
            pb_request = cluster_service.ListNodePoolsRequest.pb(request)
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
            resp = cluster_service.ListNodePoolsResponse()
            pb_resp = cluster_service.ListNodePoolsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_node_pools(resp)
            return resp

    class _ListOperations(ClusterManagerRestStub):
        def __hash__(self):
            return hash("ListOperations")

        def __call__(
            self,
            request: cluster_service.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (~.cluster_service.ListOperationsRequest):
                    The request object. ListOperationsRequest lists
                operations.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.ListOperationsResponse:
                    ListOperationsResponse is the result
                of ListOperationsRequest.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/operations",
                },
            ]
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            pb_request = cluster_service.ListOperationsRequest.pb(request)
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
            resp = cluster_service.ListOperationsResponse()
            pb_resp = cluster_service.ListOperationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    class _ListUsableSubnetworks(ClusterManagerRestStub):
        def __hash__(self):
            return hash("ListUsableSubnetworks")

        def __call__(
            self,
            request: cluster_service.ListUsableSubnetworksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.ListUsableSubnetworksResponse:
            r"""Call the list usable subnetworks method over HTTP.

            Args:
                request (~.cluster_service.ListUsableSubnetworksRequest):
                    The request object. ListUsableSubnetworksRequest requests
                the list of usable subnetworks available
                to a user for creating clusters.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.ListUsableSubnetworksResponse:
                    ListUsableSubnetworksResponse is the
                response of
                ListUsableSubnetworksRequest.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/aggregated/usableSubnetworks",
                },
            ]
            request, metadata = self._interceptor.pre_list_usable_subnetworks(
                request, metadata
            )
            pb_request = cluster_service.ListUsableSubnetworksRequest.pb(request)
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
            resp = cluster_service.ListUsableSubnetworksResponse()
            pb_resp = cluster_service.ListUsableSubnetworksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_usable_subnetworks(resp)
            return resp

    class _RollbackNodePoolUpgrade(ClusterManagerRestStub):
        def __hash__(self):
            return hash("RollbackNodePoolUpgrade")

        def __call__(
            self,
            request: cluster_service.RollbackNodePoolUpgradeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the rollback node pool
            upgrade method over HTTP.

                Args:
                    request (~.cluster_service.RollbackNodePoolUpgradeRequest):
                        The request object. RollbackNodePoolUpgradeRequest
                    rollbacks the previously Aborted or
                    Failed NodePool upgrade. This will be an
                    no-op if the last upgrade successfully
                    completed.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.cluster_service.Operation:
                        This operation resource represents
                    operations that may have happened or are
                    happening on the cluster. All fields are
                    output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/nodePools/*}:rollback",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/nodePools/{node_pool_id}:rollback",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rollback_node_pool_upgrade(
                request, metadata
            )
            pb_request = cluster_service.RollbackNodePoolUpgradeRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_rollback_node_pool_upgrade(resp)
            return resp

    class _SetAddonsConfig(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetAddonsConfig")

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
            request: cluster_service.SetAddonsConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set addons config method over HTTP.

            Args:
                request (~.cluster_service.SetAddonsConfigRequest):
                    The request object. SetAddonsConfigRequest sets the
                addons associated with the cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:setAddons",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/addons",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_addons_config(
                request, metadata
            )
            pb_request = cluster_service.SetAddonsConfigRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_addons_config(resp)
            return resp

    class _SetLabels(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetLabels")

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
            request: cluster_service.SetLabelsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set labels method over HTTP.

            Args:
                request (~.cluster_service.SetLabelsRequest):
                    The request object. SetLabelsRequest sets the Google
                Cloud Platform labels on a Google
                Container Engine cluster, which will in
                turn set them for Google Compute Engine
                resources used by that cluster
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:setResourceLabels",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/resourceLabels",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_labels(request, metadata)
            pb_request = cluster_service.SetLabelsRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_labels(resp)
            return resp

    class _SetLegacyAbac(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetLegacyAbac")

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
            request: cluster_service.SetLegacyAbacRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set legacy abac method over HTTP.

            Args:
                request (~.cluster_service.SetLegacyAbacRequest):
                    The request object. SetLegacyAbacRequest enables or
                disables the ABAC authorization
                mechanism for a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:setLegacyAbac",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/legacyAbac",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_legacy_abac(request, metadata)
            pb_request = cluster_service.SetLegacyAbacRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_legacy_abac(resp)
            return resp

    class _SetLocations(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetLocations")

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
            request: cluster_service.SetLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set locations method over HTTP.

            Args:
                request (~.cluster_service.SetLocationsRequest):
                    The request object. SetLocationsRequest sets the
                locations of the cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:setLocations",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/locations",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_locations(request, metadata)
            pb_request = cluster_service.SetLocationsRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_locations(resp)
            return resp

    class _SetLoggingService(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetLoggingService")

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
            request: cluster_service.SetLoggingServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set logging service method over HTTP.

            Args:
                request (~.cluster_service.SetLoggingServiceRequest):
                    The request object. SetLoggingServiceRequest sets the
                logging service of a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:setLogging",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/logging",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_logging_service(
                request, metadata
            )
            pb_request = cluster_service.SetLoggingServiceRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_logging_service(resp)
            return resp

    class _SetMaintenancePolicy(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetMaintenancePolicy")

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
            request: cluster_service.SetMaintenancePolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set maintenance policy method over HTTP.

            Args:
                request (~.cluster_service.SetMaintenancePolicyRequest):
                    The request object. SetMaintenancePolicyRequest sets the
                maintenance policy for a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:setMaintenancePolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}:setMaintenancePolicy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_maintenance_policy(
                request, metadata
            )
            pb_request = cluster_service.SetMaintenancePolicyRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_maintenance_policy(resp)
            return resp

    class _SetMasterAuth(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetMasterAuth")

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
            request: cluster_service.SetMasterAuthRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set master auth method over HTTP.

            Args:
                request (~.cluster_service.SetMasterAuthRequest):
                    The request object. SetMasterAuthRequest updates the
                admin password of a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:setMasterAuth",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}:setMasterAuth",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_master_auth(request, metadata)
            pb_request = cluster_service.SetMasterAuthRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_master_auth(resp)
            return resp

    class _SetMonitoringService(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetMonitoringService")

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
            request: cluster_service.SetMonitoringServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set monitoring service method over HTTP.

            Args:
                request (~.cluster_service.SetMonitoringServiceRequest):
                    The request object. SetMonitoringServiceRequest sets the
                monitoring service of a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:setMonitoring",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/monitoring",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_monitoring_service(
                request, metadata
            )
            pb_request = cluster_service.SetMonitoringServiceRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_monitoring_service(resp)
            return resp

    class _SetNetworkPolicy(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetNetworkPolicy")

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
            request: cluster_service.SetNetworkPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set network policy method over HTTP.

            Args:
                request (~.cluster_service.SetNetworkPolicyRequest):
                    The request object. SetNetworkPolicyRequest
                enables/disables network policy for a
                cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:setNetworkPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}:setNetworkPolicy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_network_policy(
                request, metadata
            )
            pb_request = cluster_service.SetNetworkPolicyRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_network_policy(resp)
            return resp

    class _SetNodePoolAutoscaling(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetNodePoolAutoscaling")

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
            request: cluster_service.SetNodePoolAutoscalingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set node pool autoscaling method over HTTP.

            Args:
                request (~.cluster_service.SetNodePoolAutoscalingRequest):
                    The request object. SetNodePoolAutoscalingRequest sets
                the autoscaler settings of a node pool.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/nodePools/*}:setAutoscaling",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/nodePools/{node_pool_id}/autoscaling",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_node_pool_autoscaling(
                request, metadata
            )
            pb_request = cluster_service.SetNodePoolAutoscalingRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_node_pool_autoscaling(resp)
            return resp

    class _SetNodePoolManagement(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetNodePoolManagement")

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
            request: cluster_service.SetNodePoolManagementRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set node pool management method over HTTP.

            Args:
                request (~.cluster_service.SetNodePoolManagementRequest):
                    The request object. SetNodePoolManagementRequest sets the
                node management properties of a node
                pool.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/nodePools/*}:setManagement",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/nodePools/{node_pool_id}/setManagement",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_node_pool_management(
                request, metadata
            )
            pb_request = cluster_service.SetNodePoolManagementRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_node_pool_management(resp)
            return resp

    class _SetNodePoolSize(ClusterManagerRestStub):
        def __hash__(self):
            return hash("SetNodePoolSize")

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
            request: cluster_service.SetNodePoolSizeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the set node pool size method over HTTP.

            Args:
                request (~.cluster_service.SetNodePoolSizeRequest):
                    The request object. SetNodePoolSizeRequest sets the size
                of a node pool.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/nodePools/*}:setSize",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/nodePools/{node_pool_id}/setSize",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_node_pool_size(
                request, metadata
            )
            pb_request = cluster_service.SetNodePoolSizeRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_node_pool_size(resp)
            return resp

    class _StartIPRotation(ClusterManagerRestStub):
        def __hash__(self):
            return hash("StartIPRotation")

        def __call__(
            self,
            request: cluster_service.StartIPRotationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the start ip rotation method over HTTP.

            Args:
                request (~.cluster_service.StartIPRotationRequest):
                    The request object. StartIPRotationRequest creates a new
                IP for the cluster and then performs a
                node upgrade on each node pool to point
                to the new IP.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:startIpRotation",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}:startIpRotation",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_start_ip_rotation(
                request, metadata
            )
            pb_request = cluster_service.StartIPRotationRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_start_ip_rotation(resp)
            return resp

    class _UpdateCluster(ClusterManagerRestStub):
        def __hash__(self):
            return hash("UpdateCluster")

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
            request: cluster_service.UpdateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the update cluster method over HTTP.

            Args:
                request (~.cluster_service.UpdateClusterRequest):
                    The request object. UpdateClusterRequest updates the
                settings of a cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "put",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}",
                    "body": "*",
                },
                {
                    "method": "put",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_update_cluster(request, metadata)
            pb_request = cluster_service.UpdateClusterRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_cluster(resp)
            return resp

    class _UpdateMaster(ClusterManagerRestStub):
        def __hash__(self):
            return hash("UpdateMaster")

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
            request: cluster_service.UpdateMasterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the update master method over HTTP.

            Args:
                request (~.cluster_service.UpdateMasterRequest):
                    The request object. UpdateMasterRequest updates the
                master of the cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*}:updateMaster",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/master",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_update_master(request, metadata)
            pb_request = cluster_service.UpdateMasterRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_master(resp)
            return resp

    class _UpdateNodePool(ClusterManagerRestStub):
        def __hash__(self):
            return hash("UpdateNodePool")

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
            request: cluster_service.UpdateNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cluster_service.Operation:
            r"""Call the update node pool method over HTTP.

            Args:
                request (~.cluster_service.UpdateNodePoolRequest):
                    The request object. UpdateNodePoolRequests update a node
                pool's image and/or version.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cluster_service.Operation:
                    This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "put",
                    "uri": "/v1/{name=projects/*/locations/*/clusters/*/nodePools/*}",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_id}/nodePools/{node_pool_id}/update",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_update_node_pool(
                request, metadata
            )
            pb_request = cluster_service.UpdateNodePoolRequest.pb(request)
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
            resp = cluster_service.Operation()
            pb_resp = cluster_service.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_node_pool(resp)
            return resp

    @property
    def cancel_operation(
        self,
    ) -> Callable[[cluster_service.CancelOperationRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def check_autopilot_compatibility(
        self,
    ) -> Callable[
        [cluster_service.CheckAutopilotCompatibilityRequest],
        cluster_service.CheckAutopilotCompatibilityResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CheckAutopilotCompatibility(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def complete_ip_rotation(
        self,
    ) -> Callable[
        [cluster_service.CompleteIPRotationRequest], cluster_service.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CompleteIPRotation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def complete_node_pool_upgrade(
        self,
    ) -> Callable[[cluster_service.CompleteNodePoolUpgradeRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CompleteNodePoolUpgrade(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_cluster(
        self,
    ) -> Callable[[cluster_service.CreateClusterRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_node_pool(
        self,
    ) -> Callable[[cluster_service.CreateNodePoolRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_cluster(
        self,
    ) -> Callable[[cluster_service.DeleteClusterRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_node_pool(
        self,
    ) -> Callable[[cluster_service.DeleteNodePoolRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cluster(
        self,
    ) -> Callable[[cluster_service.GetClusterRequest], cluster_service.Cluster]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_json_web_keys(
        self,
    ) -> Callable[
        [cluster_service.GetJSONWebKeysRequest], cluster_service.GetJSONWebKeysResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetJSONWebKeys(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_node_pool(
        self,
    ) -> Callable[[cluster_service.GetNodePoolRequest], cluster_service.NodePool]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(
        self,
    ) -> Callable[[cluster_service.GetOperationRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_server_config(
        self,
    ) -> Callable[
        [cluster_service.GetServerConfigRequest], cluster_service.ServerConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetServerConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_clusters(
        self,
    ) -> Callable[
        [cluster_service.ListClustersRequest], cluster_service.ListClustersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_node_pools(
        self,
    ) -> Callable[
        [cluster_service.ListNodePoolsRequest], cluster_service.ListNodePoolsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNodePools(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_operations(
        self,
    ) -> Callable[
        [cluster_service.ListOperationsRequest], cluster_service.ListOperationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_usable_subnetworks(
        self,
    ) -> Callable[
        [cluster_service.ListUsableSubnetworksRequest],
        cluster_service.ListUsableSubnetworksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListUsableSubnetworks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rollback_node_pool_upgrade(
        self,
    ) -> Callable[
        [cluster_service.RollbackNodePoolUpgradeRequest], cluster_service.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RollbackNodePoolUpgrade(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_addons_config(
        self,
    ) -> Callable[[cluster_service.SetAddonsConfigRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetAddonsConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_labels(
        self,
    ) -> Callable[[cluster_service.SetLabelsRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetLabels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_legacy_abac(
        self,
    ) -> Callable[[cluster_service.SetLegacyAbacRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetLegacyAbac(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_locations(
        self,
    ) -> Callable[[cluster_service.SetLocationsRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetLocations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_logging_service(
        self,
    ) -> Callable[
        [cluster_service.SetLoggingServiceRequest], cluster_service.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetLoggingService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_maintenance_policy(
        self,
    ) -> Callable[
        [cluster_service.SetMaintenancePolicyRequest], cluster_service.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetMaintenancePolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_master_auth(
        self,
    ) -> Callable[[cluster_service.SetMasterAuthRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetMasterAuth(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_monitoring_service(
        self,
    ) -> Callable[
        [cluster_service.SetMonitoringServiceRequest], cluster_service.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetMonitoringService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_network_policy(
        self,
    ) -> Callable[[cluster_service.SetNetworkPolicyRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetNetworkPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_node_pool_autoscaling(
        self,
    ) -> Callable[
        [cluster_service.SetNodePoolAutoscalingRequest], cluster_service.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetNodePoolAutoscaling(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_node_pool_management(
        self,
    ) -> Callable[
        [cluster_service.SetNodePoolManagementRequest], cluster_service.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetNodePoolManagement(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_node_pool_size(
        self,
    ) -> Callable[[cluster_service.SetNodePoolSizeRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetNodePoolSize(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def start_ip_rotation(
        self,
    ) -> Callable[[cluster_service.StartIPRotationRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartIPRotation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_cluster(
        self,
    ) -> Callable[[cluster_service.UpdateClusterRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_master(
        self,
    ) -> Callable[[cluster_service.UpdateMasterRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateMaster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_node_pool(
        self,
    ) -> Callable[[cluster_service.UpdateNodePoolRequest], cluster_service.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ClusterManagerRestTransport",)
