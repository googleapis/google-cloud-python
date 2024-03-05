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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.vmwareengine_v1.types import vmwareengine, vmwareengine_resources

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import VmwareEngineTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class VmwareEngineRestInterceptor:
    """Interceptor for VmwareEngine.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the VmwareEngineRestTransport.

    .. code-block:: python
        class MyCustomVmwareEngineInterceptor(VmwareEngineRestInterceptor):
            def pre_create_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_external_access_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_external_access_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_external_address(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_external_address(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_hcx_activation_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_hcx_activation_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_logging_server(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_logging_server(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_management_dns_zone_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_management_dns_zone_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_network_peering(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_network_peering(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_network_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_network_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_private_cloud(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_private_cloud(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_private_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_private_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_vmware_engine_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_vmware_engine_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_external_access_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_external_access_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_external_address(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_external_address(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_logging_server(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_logging_server(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_management_dns_zone_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_management_dns_zone_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_network_peering(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_network_peering(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_network_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_network_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_private_cloud(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_private_cloud(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_private_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_private_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_vmware_engine_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_vmware_engine_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_network_policy_external_addresses(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_network_policy_external_addresses(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_dns_bind_permission(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_dns_bind_permission(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_dns_forwarding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_dns_forwarding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_external_access_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_external_access_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_external_address(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_external_address(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_hcx_activation_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_hcx_activation_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_logging_server(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_logging_server(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_management_dns_zone_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_management_dns_zone_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_network_peering(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_network_peering(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_network_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_network_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_node(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_node(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_node_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_node_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_private_cloud(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_private_cloud(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_private_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_private_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_subnet(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_subnet(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_vmware_engine_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_vmware_engine_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_grant_dns_bind_permission(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_grant_dns_bind_permission(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_external_access_rules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_external_access_rules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_external_addresses(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_external_addresses(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_hcx_activation_keys(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_hcx_activation_keys(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_logging_servers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_logging_servers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_management_dns_zone_bindings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_management_dns_zone_bindings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_network_peerings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_network_peerings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_network_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_network_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_nodes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_nodes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_node_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_node_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_peering_routes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_peering_routes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_private_clouds(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_private_clouds(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_private_connection_peering_routes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_private_connection_peering_routes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_private_connections(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_private_connections(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_subnets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_subnets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_vmware_engine_networks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_vmware_engine_networks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_repair_management_dns_zone_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_repair_management_dns_zone_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_reset_nsx_credentials(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_reset_nsx_credentials(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_reset_vcenter_credentials(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_reset_vcenter_credentials(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_revoke_dns_bind_permission(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_revoke_dns_bind_permission(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_show_nsx_credentials(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_show_nsx_credentials(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_show_vcenter_credentials(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_show_vcenter_credentials(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_private_cloud(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undelete_private_cloud(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_dns_forwarding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_dns_forwarding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_external_access_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_external_access_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_external_address(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_external_address(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_logging_server(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_logging_server(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_management_dns_zone_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_management_dns_zone_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_network_peering(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_network_peering(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_network_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_network_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_private_cloud(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_private_cloud(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_private_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_private_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_subnet(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_subnet(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_vmware_engine_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_vmware_engine_network(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = VmwareEngineRestTransport(interceptor=MyCustomVmwareEngineInterceptor())
        client = VmwareEngineClient(transport=transport)


    """

    def pre_create_cluster(
        self,
        request: vmwareengine.CreateClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.CreateClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_cluster

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_create_external_access_rule(
        self,
        request: vmwareengine.CreateExternalAccessRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.CreateExternalAccessRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_external_access_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_external_access_rule(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_external_access_rule

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_create_external_address(
        self,
        request: vmwareengine.CreateExternalAddressRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.CreateExternalAddressRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_external_address

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_external_address(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_external_address

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_create_hcx_activation_key(
        self,
        request: vmwareengine.CreateHcxActivationKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.CreateHcxActivationKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_hcx_activation_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_hcx_activation_key(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_hcx_activation_key

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_create_logging_server(
        self,
        request: vmwareengine.CreateLoggingServerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.CreateLoggingServerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_logging_server

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_logging_server(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_logging_server

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_create_management_dns_zone_binding(
        self,
        request: vmwareengine.CreateManagementDnsZoneBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.CreateManagementDnsZoneBindingRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_management_dns_zone_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_management_dns_zone_binding(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_management_dns_zone_binding

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_create_network_peering(
        self,
        request: vmwareengine.CreateNetworkPeeringRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.CreateNetworkPeeringRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_network_peering

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_network_peering(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_network_peering

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_create_network_policy(
        self,
        request: vmwareengine.CreateNetworkPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.CreateNetworkPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_network_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_network_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_network_policy

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_create_private_cloud(
        self,
        request: vmwareengine.CreatePrivateCloudRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.CreatePrivateCloudRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_private_cloud

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_private_cloud(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_private_cloud

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_create_private_connection(
        self,
        request: vmwareengine.CreatePrivateConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.CreatePrivateConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_private_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_private_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_private_connection

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_create_vmware_engine_network(
        self,
        request: vmwareengine.CreateVmwareEngineNetworkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.CreateVmwareEngineNetworkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_vmware_engine_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_create_vmware_engine_network(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_vmware_engine_network

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_delete_cluster(
        self,
        request: vmwareengine.DeleteClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.DeleteClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_cluster

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_delete_external_access_rule(
        self,
        request: vmwareengine.DeleteExternalAccessRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.DeleteExternalAccessRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_external_access_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_external_access_rule(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_external_access_rule

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_delete_external_address(
        self,
        request: vmwareengine.DeleteExternalAddressRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.DeleteExternalAddressRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_external_address

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_external_address(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_external_address

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_delete_logging_server(
        self,
        request: vmwareengine.DeleteLoggingServerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.DeleteLoggingServerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_logging_server

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_logging_server(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_logging_server

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_delete_management_dns_zone_binding(
        self,
        request: vmwareengine.DeleteManagementDnsZoneBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.DeleteManagementDnsZoneBindingRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_management_dns_zone_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_management_dns_zone_binding(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_management_dns_zone_binding

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_delete_network_peering(
        self,
        request: vmwareengine.DeleteNetworkPeeringRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.DeleteNetworkPeeringRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_network_peering

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_network_peering(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_network_peering

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_delete_network_policy(
        self,
        request: vmwareengine.DeleteNetworkPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.DeleteNetworkPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_network_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_network_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_network_policy

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_delete_private_cloud(
        self,
        request: vmwareengine.DeletePrivateCloudRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.DeletePrivateCloudRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_private_cloud

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_private_cloud(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_private_cloud

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_delete_private_connection(
        self,
        request: vmwareengine.DeletePrivateConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.DeletePrivateConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_private_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_private_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_private_connection

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_delete_vmware_engine_network(
        self,
        request: vmwareengine.DeleteVmwareEngineNetworkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.DeleteVmwareEngineNetworkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_vmware_engine_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_vmware_engine_network(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_vmware_engine_network

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_network_policy_external_addresses(
        self,
        request: vmwareengine.FetchNetworkPolicyExternalAddressesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.FetchNetworkPolicyExternalAddressesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for fetch_network_policy_external_addresses

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_fetch_network_policy_external_addresses(
        self, response: vmwareengine.FetchNetworkPolicyExternalAddressesResponse
    ) -> vmwareengine.FetchNetworkPolicyExternalAddressesResponse:
        """Post-rpc interceptor for fetch_network_policy_external_addresses

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_cluster(
        self,
        request: vmwareengine.GetClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_cluster(
        self, response: vmwareengine_resources.Cluster
    ) -> vmwareengine_resources.Cluster:
        """Post-rpc interceptor for get_cluster

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_dns_bind_permission(
        self,
        request: vmwareengine.GetDnsBindPermissionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetDnsBindPermissionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_dns_bind_permission

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_dns_bind_permission(
        self, response: vmwareengine_resources.DnsBindPermission
    ) -> vmwareengine_resources.DnsBindPermission:
        """Post-rpc interceptor for get_dns_bind_permission

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_dns_forwarding(
        self,
        request: vmwareengine.GetDnsForwardingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetDnsForwardingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_dns_forwarding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_dns_forwarding(
        self, response: vmwareengine_resources.DnsForwarding
    ) -> vmwareengine_resources.DnsForwarding:
        """Post-rpc interceptor for get_dns_forwarding

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_external_access_rule(
        self,
        request: vmwareengine.GetExternalAccessRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetExternalAccessRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_external_access_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_external_access_rule(
        self, response: vmwareengine_resources.ExternalAccessRule
    ) -> vmwareengine_resources.ExternalAccessRule:
        """Post-rpc interceptor for get_external_access_rule

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_external_address(
        self,
        request: vmwareengine.GetExternalAddressRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetExternalAddressRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_external_address

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_external_address(
        self, response: vmwareengine_resources.ExternalAddress
    ) -> vmwareengine_resources.ExternalAddress:
        """Post-rpc interceptor for get_external_address

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_hcx_activation_key(
        self,
        request: vmwareengine.GetHcxActivationKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetHcxActivationKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_hcx_activation_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_hcx_activation_key(
        self, response: vmwareengine_resources.HcxActivationKey
    ) -> vmwareengine_resources.HcxActivationKey:
        """Post-rpc interceptor for get_hcx_activation_key

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_logging_server(
        self,
        request: vmwareengine.GetLoggingServerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetLoggingServerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_logging_server

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_logging_server(
        self, response: vmwareengine_resources.LoggingServer
    ) -> vmwareengine_resources.LoggingServer:
        """Post-rpc interceptor for get_logging_server

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_management_dns_zone_binding(
        self,
        request: vmwareengine.GetManagementDnsZoneBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.GetManagementDnsZoneBindingRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_management_dns_zone_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_management_dns_zone_binding(
        self, response: vmwareengine_resources.ManagementDnsZoneBinding
    ) -> vmwareengine_resources.ManagementDnsZoneBinding:
        """Post-rpc interceptor for get_management_dns_zone_binding

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_network_peering(
        self,
        request: vmwareengine.GetNetworkPeeringRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetNetworkPeeringRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_network_peering

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_network_peering(
        self, response: vmwareengine_resources.NetworkPeering
    ) -> vmwareengine_resources.NetworkPeering:
        """Post-rpc interceptor for get_network_peering

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_network_policy(
        self,
        request: vmwareengine.GetNetworkPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetNetworkPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_network_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_network_policy(
        self, response: vmwareengine_resources.NetworkPolicy
    ) -> vmwareengine_resources.NetworkPolicy:
        """Post-rpc interceptor for get_network_policy

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_node(
        self, request: vmwareengine.GetNodeRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[vmwareengine.GetNodeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_node

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_node(
        self, response: vmwareengine_resources.Node
    ) -> vmwareengine_resources.Node:
        """Post-rpc interceptor for get_node

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_node_type(
        self,
        request: vmwareengine.GetNodeTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetNodeTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_node_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_node_type(
        self, response: vmwareengine_resources.NodeType
    ) -> vmwareengine_resources.NodeType:
        """Post-rpc interceptor for get_node_type

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_private_cloud(
        self,
        request: vmwareengine.GetPrivateCloudRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetPrivateCloudRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_private_cloud

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_private_cloud(
        self, response: vmwareengine_resources.PrivateCloud
    ) -> vmwareengine_resources.PrivateCloud:
        """Post-rpc interceptor for get_private_cloud

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_private_connection(
        self,
        request: vmwareengine.GetPrivateConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetPrivateConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_private_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_private_connection(
        self, response: vmwareengine_resources.PrivateConnection
    ) -> vmwareengine_resources.PrivateConnection:
        """Post-rpc interceptor for get_private_connection

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_subnet(
        self,
        request: vmwareengine.GetSubnetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetSubnetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_subnet

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_subnet(
        self, response: vmwareengine_resources.Subnet
    ) -> vmwareengine_resources.Subnet:
        """Post-rpc interceptor for get_subnet

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_vmware_engine_network(
        self,
        request: vmwareengine.GetVmwareEngineNetworkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GetVmwareEngineNetworkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_vmware_engine_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_vmware_engine_network(
        self, response: vmwareengine_resources.VmwareEngineNetwork
    ) -> vmwareengine_resources.VmwareEngineNetwork:
        """Post-rpc interceptor for get_vmware_engine_network

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_grant_dns_bind_permission(
        self,
        request: vmwareengine.GrantDnsBindPermissionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.GrantDnsBindPermissionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for grant_dns_bind_permission

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_grant_dns_bind_permission(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for grant_dns_bind_permission

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_clusters(
        self,
        request: vmwareengine.ListClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListClustersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_clusters(
        self, response: vmwareengine.ListClustersResponse
    ) -> vmwareengine.ListClustersResponse:
        """Post-rpc interceptor for list_clusters

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_external_access_rules(
        self,
        request: vmwareengine.ListExternalAccessRulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListExternalAccessRulesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_external_access_rules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_external_access_rules(
        self, response: vmwareengine.ListExternalAccessRulesResponse
    ) -> vmwareengine.ListExternalAccessRulesResponse:
        """Post-rpc interceptor for list_external_access_rules

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_external_addresses(
        self,
        request: vmwareengine.ListExternalAddressesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListExternalAddressesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_external_addresses

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_external_addresses(
        self, response: vmwareengine.ListExternalAddressesResponse
    ) -> vmwareengine.ListExternalAddressesResponse:
        """Post-rpc interceptor for list_external_addresses

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_hcx_activation_keys(
        self,
        request: vmwareengine.ListHcxActivationKeysRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListHcxActivationKeysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_hcx_activation_keys

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_hcx_activation_keys(
        self, response: vmwareengine.ListHcxActivationKeysResponse
    ) -> vmwareengine.ListHcxActivationKeysResponse:
        """Post-rpc interceptor for list_hcx_activation_keys

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_logging_servers(
        self,
        request: vmwareengine.ListLoggingServersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListLoggingServersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_logging_servers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_logging_servers(
        self, response: vmwareengine.ListLoggingServersResponse
    ) -> vmwareengine.ListLoggingServersResponse:
        """Post-rpc interceptor for list_logging_servers

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_management_dns_zone_bindings(
        self,
        request: vmwareengine.ListManagementDnsZoneBindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.ListManagementDnsZoneBindingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_management_dns_zone_bindings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_management_dns_zone_bindings(
        self, response: vmwareengine.ListManagementDnsZoneBindingsResponse
    ) -> vmwareengine.ListManagementDnsZoneBindingsResponse:
        """Post-rpc interceptor for list_management_dns_zone_bindings

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_network_peerings(
        self,
        request: vmwareengine.ListNetworkPeeringsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListNetworkPeeringsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_network_peerings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_network_peerings(
        self, response: vmwareengine.ListNetworkPeeringsResponse
    ) -> vmwareengine.ListNetworkPeeringsResponse:
        """Post-rpc interceptor for list_network_peerings

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_network_policies(
        self,
        request: vmwareengine.ListNetworkPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListNetworkPoliciesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_network_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_network_policies(
        self, response: vmwareengine.ListNetworkPoliciesResponse
    ) -> vmwareengine.ListNetworkPoliciesResponse:
        """Post-rpc interceptor for list_network_policies

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_nodes(
        self,
        request: vmwareengine.ListNodesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListNodesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_nodes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_nodes(
        self, response: vmwareengine.ListNodesResponse
    ) -> vmwareengine.ListNodesResponse:
        """Post-rpc interceptor for list_nodes

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_node_types(
        self,
        request: vmwareengine.ListNodeTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListNodeTypesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_node_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_node_types(
        self, response: vmwareengine.ListNodeTypesResponse
    ) -> vmwareengine.ListNodeTypesResponse:
        """Post-rpc interceptor for list_node_types

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_peering_routes(
        self,
        request: vmwareengine.ListPeeringRoutesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListPeeringRoutesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_peering_routes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_peering_routes(
        self, response: vmwareengine.ListPeeringRoutesResponse
    ) -> vmwareengine.ListPeeringRoutesResponse:
        """Post-rpc interceptor for list_peering_routes

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_private_clouds(
        self,
        request: vmwareengine.ListPrivateCloudsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListPrivateCloudsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_private_clouds

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_private_clouds(
        self, response: vmwareengine.ListPrivateCloudsResponse
    ) -> vmwareengine.ListPrivateCloudsResponse:
        """Post-rpc interceptor for list_private_clouds

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_private_connection_peering_routes(
        self,
        request: vmwareengine.ListPrivateConnectionPeeringRoutesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.ListPrivateConnectionPeeringRoutesRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_private_connection_peering_routes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_private_connection_peering_routes(
        self, response: vmwareengine.ListPrivateConnectionPeeringRoutesResponse
    ) -> vmwareengine.ListPrivateConnectionPeeringRoutesResponse:
        """Post-rpc interceptor for list_private_connection_peering_routes

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_private_connections(
        self,
        request: vmwareengine.ListPrivateConnectionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListPrivateConnectionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_private_connections

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_private_connections(
        self, response: vmwareengine.ListPrivateConnectionsResponse
    ) -> vmwareengine.ListPrivateConnectionsResponse:
        """Post-rpc interceptor for list_private_connections

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_subnets(
        self,
        request: vmwareengine.ListSubnetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListSubnetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_subnets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_subnets(
        self, response: vmwareengine.ListSubnetsResponse
    ) -> vmwareengine.ListSubnetsResponse:
        """Post-rpc interceptor for list_subnets

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_list_vmware_engine_networks(
        self,
        request: vmwareengine.ListVmwareEngineNetworksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ListVmwareEngineNetworksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_vmware_engine_networks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_vmware_engine_networks(
        self, response: vmwareengine.ListVmwareEngineNetworksResponse
    ) -> vmwareengine.ListVmwareEngineNetworksResponse:
        """Post-rpc interceptor for list_vmware_engine_networks

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_repair_management_dns_zone_binding(
        self,
        request: vmwareengine.RepairManagementDnsZoneBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.RepairManagementDnsZoneBindingRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for repair_management_dns_zone_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_repair_management_dns_zone_binding(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for repair_management_dns_zone_binding

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_reset_nsx_credentials(
        self,
        request: vmwareengine.ResetNsxCredentialsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ResetNsxCredentialsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for reset_nsx_credentials

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_reset_nsx_credentials(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for reset_nsx_credentials

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_reset_vcenter_credentials(
        self,
        request: vmwareengine.ResetVcenterCredentialsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ResetVcenterCredentialsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for reset_vcenter_credentials

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_reset_vcenter_credentials(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for reset_vcenter_credentials

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_revoke_dns_bind_permission(
        self,
        request: vmwareengine.RevokeDnsBindPermissionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.RevokeDnsBindPermissionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for revoke_dns_bind_permission

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_revoke_dns_bind_permission(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for revoke_dns_bind_permission

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_show_nsx_credentials(
        self,
        request: vmwareengine.ShowNsxCredentialsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ShowNsxCredentialsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for show_nsx_credentials

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_show_nsx_credentials(
        self, response: vmwareengine_resources.Credentials
    ) -> vmwareengine_resources.Credentials:
        """Post-rpc interceptor for show_nsx_credentials

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_show_vcenter_credentials(
        self,
        request: vmwareengine.ShowVcenterCredentialsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.ShowVcenterCredentialsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for show_vcenter_credentials

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_show_vcenter_credentials(
        self, response: vmwareengine_resources.Credentials
    ) -> vmwareengine_resources.Credentials:
        """Post-rpc interceptor for show_vcenter_credentials

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_undelete_private_cloud(
        self,
        request: vmwareengine.UndeletePrivateCloudRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UndeletePrivateCloudRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undelete_private_cloud

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_undelete_private_cloud(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undelete_private_cloud

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_cluster(
        self,
        request: vmwareengine.UpdateClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UpdateClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_cluster

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_dns_forwarding(
        self,
        request: vmwareengine.UpdateDnsForwardingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UpdateDnsForwardingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_dns_forwarding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_dns_forwarding(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_dns_forwarding

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_external_access_rule(
        self,
        request: vmwareengine.UpdateExternalAccessRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UpdateExternalAccessRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_external_access_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_external_access_rule(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_external_access_rule

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_external_address(
        self,
        request: vmwareengine.UpdateExternalAddressRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UpdateExternalAddressRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_external_address

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_external_address(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_external_address

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_logging_server(
        self,
        request: vmwareengine.UpdateLoggingServerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UpdateLoggingServerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_logging_server

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_logging_server(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_logging_server

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_management_dns_zone_binding(
        self,
        request: vmwareengine.UpdateManagementDnsZoneBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.UpdateManagementDnsZoneBindingRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_management_dns_zone_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_management_dns_zone_binding(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_management_dns_zone_binding

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_network_peering(
        self,
        request: vmwareengine.UpdateNetworkPeeringRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UpdateNetworkPeeringRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_network_peering

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_network_peering(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_network_peering

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_network_policy(
        self,
        request: vmwareengine.UpdateNetworkPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UpdateNetworkPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_network_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_network_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_network_policy

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_private_cloud(
        self,
        request: vmwareengine.UpdatePrivateCloudRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UpdatePrivateCloudRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_private_cloud

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_private_cloud(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_private_cloud

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_private_connection(
        self,
        request: vmwareengine.UpdatePrivateConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UpdatePrivateConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_private_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_private_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_private_connection

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_subnet(
        self,
        request: vmwareengine.UpdateSubnetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmwareengine.UpdateSubnetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_subnet

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_subnet(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_subnet

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_update_vmware_engine_network(
        self,
        request: vmwareengine.UpdateVmwareEngineNetworkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        vmwareengine.UpdateVmwareEngineNetworkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_vmware_engine_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_update_vmware_engine_network(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_vmware_engine_network

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
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
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
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
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
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
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
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
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
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
        before they are sent to the VmwareEngine server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the VmwareEngine server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class VmwareEngineRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: VmwareEngineRestInterceptor


class VmwareEngineRestTransport(VmwareEngineTransport):
    """REST backend transport for VmwareEngine.

    VMwareEngine manages VMware's private clusters in the Cloud.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "vmwareengine.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[VmwareEngineRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'vmwareengine.googleapis.com').
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
        self._interceptor = interceptor or VmwareEngineRestInterceptor()
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

    class _CreateCluster(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreateCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "clusterId": "",
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
            request: vmwareengine.CreateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create cluster method over HTTP.

            Args:
                request (~.vmwareengine.CreateClusterRequest):
                    The request object. Request message for
                [VmwareEngine.CreateCluster][google.cloud.vmwareengine.v1.VmwareEngine.CreateCluster]
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
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/clusters",
                    "body": "cluster",
                },
            ]
            request, metadata = self._interceptor.pre_create_cluster(request, metadata)
            pb_request = vmwareengine.CreateClusterRequest.pb(request)
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
            resp = self._interceptor.post_create_cluster(resp)
            return resp

    class _CreateExternalAccessRule(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreateExternalAccessRule")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "externalAccessRuleId": "",
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
            request: vmwareengine.CreateExternalAccessRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create external access
            rule method over HTTP.

                Args:
                    request (~.vmwareengine.CreateExternalAccessRuleRequest):
                        The request object. Request message for
                    [VmwareEngine.CreateExternalAccessRule][google.cloud.vmwareengine.v1.VmwareEngine.CreateExternalAccessRule]
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
                    "uri": "/v1/{parent=projects/*/locations/*/networkPolicies/*}/externalAccessRules",
                    "body": "external_access_rule",
                },
            ]
            request, metadata = self._interceptor.pre_create_external_access_rule(
                request, metadata
            )
            pb_request = vmwareengine.CreateExternalAccessRuleRequest.pb(request)
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
            resp = self._interceptor.post_create_external_access_rule(resp)
            return resp

    class _CreateExternalAddress(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreateExternalAddress")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "externalAddressId": "",
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
            request: vmwareengine.CreateExternalAddressRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create external address method over HTTP.

            Args:
                request (~.vmwareengine.CreateExternalAddressRequest):
                    The request object. Request message for
                [VmwareEngine.CreateExternalAddress][google.cloud.vmwareengine.v1.VmwareEngine.CreateExternalAddress]
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
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/externalAddresses",
                    "body": "external_address",
                },
            ]
            request, metadata = self._interceptor.pre_create_external_address(
                request, metadata
            )
            pb_request = vmwareengine.CreateExternalAddressRequest.pb(request)
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
            resp = self._interceptor.post_create_external_address(resp)
            return resp

    class _CreateHcxActivationKey(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreateHcxActivationKey")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "hcxActivationKeyId": "",
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
            request: vmwareengine.CreateHcxActivationKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create hcx activation key method over HTTP.

            Args:
                request (~.vmwareengine.CreateHcxActivationKeyRequest):
                    The request object. Request message for
                [VmwareEngine.CreateHcxActivationKey][google.cloud.vmwareengine.v1.VmwareEngine.CreateHcxActivationKey]
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
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/hcxActivationKeys",
                    "body": "hcx_activation_key",
                },
            ]
            request, metadata = self._interceptor.pre_create_hcx_activation_key(
                request, metadata
            )
            pb_request = vmwareengine.CreateHcxActivationKeyRequest.pb(request)
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
            resp = self._interceptor.post_create_hcx_activation_key(resp)
            return resp

    class _CreateLoggingServer(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreateLoggingServer")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "loggingServerId": "",
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
            request: vmwareengine.CreateLoggingServerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create logging server method over HTTP.

            Args:
                request (~.vmwareengine.CreateLoggingServerRequest):
                    The request object. Request message for
                [VmwareEngine.CreateLoggingServer][google.cloud.vmwareengine.v1.VmwareEngine.CreateLoggingServer]
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
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/loggingServers",
                    "body": "logging_server",
                },
            ]
            request, metadata = self._interceptor.pre_create_logging_server(
                request, metadata
            )
            pb_request = vmwareengine.CreateLoggingServerRequest.pb(request)
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
            resp = self._interceptor.post_create_logging_server(resp)
            return resp

    class _CreateManagementDnsZoneBinding(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreateManagementDnsZoneBinding")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "managementDnsZoneBindingId": "",
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
            request: vmwareengine.CreateManagementDnsZoneBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create management dns
            zone binding method over HTTP.

                Args:
                    request (~.vmwareengine.CreateManagementDnsZoneBindingRequest):
                        The request object. Request message for
                    [VmwareEngine.CreateManagementDnsZoneBindings][]
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
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/managementDnsZoneBindings",
                    "body": "management_dns_zone_binding",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_create_management_dns_zone_binding(
                request, metadata
            )
            pb_request = vmwareengine.CreateManagementDnsZoneBindingRequest.pb(request)
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
            resp = self._interceptor.post_create_management_dns_zone_binding(resp)
            return resp

    class _CreateNetworkPeering(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreateNetworkPeering")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "networkPeeringId": "",
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
            request: vmwareengine.CreateNetworkPeeringRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create network peering method over HTTP.

            Args:
                request (~.vmwareengine.CreateNetworkPeeringRequest):
                    The request object. Request message for
                [VmwareEngine.CreateNetworkPeering][google.cloud.vmwareengine.v1.VmwareEngine.CreateNetworkPeering]
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
                    "uri": "/v1/{parent=projects/*/locations/*}/networkPeerings",
                    "body": "network_peering",
                },
            ]
            request, metadata = self._interceptor.pre_create_network_peering(
                request, metadata
            )
            pb_request = vmwareengine.CreateNetworkPeeringRequest.pb(request)
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
            resp = self._interceptor.post_create_network_peering(resp)
            return resp

    class _CreateNetworkPolicy(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreateNetworkPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "networkPolicyId": "",
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
            request: vmwareengine.CreateNetworkPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create network policy method over HTTP.

            Args:
                request (~.vmwareengine.CreateNetworkPolicyRequest):
                    The request object. Request message for
                [VmwareEngine.CreateNetworkPolicy][google.cloud.vmwareengine.v1.VmwareEngine.CreateNetworkPolicy]
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
                    "uri": "/v1/{parent=projects/*/locations/*}/networkPolicies",
                    "body": "network_policy",
                },
            ]
            request, metadata = self._interceptor.pre_create_network_policy(
                request, metadata
            )
            pb_request = vmwareengine.CreateNetworkPolicyRequest.pb(request)
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
            resp = self._interceptor.post_create_network_policy(resp)
            return resp

    class _CreatePrivateCloud(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreatePrivateCloud")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "privateCloudId": "",
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
            request: vmwareengine.CreatePrivateCloudRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create private cloud method over HTTP.

            Args:
                request (~.vmwareengine.CreatePrivateCloudRequest):
                    The request object. Request message for
                [VmwareEngine.CreatePrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.CreatePrivateCloud]
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
                    "uri": "/v1/{parent=projects/*/locations/*}/privateClouds",
                    "body": "private_cloud",
                },
            ]
            request, metadata = self._interceptor.pre_create_private_cloud(
                request, metadata
            )
            pb_request = vmwareengine.CreatePrivateCloudRequest.pb(request)
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
            resp = self._interceptor.post_create_private_cloud(resp)
            return resp

    class _CreatePrivateConnection(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreatePrivateConnection")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "privateConnectionId": "",
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
            request: vmwareengine.CreatePrivateConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create private connection method over HTTP.

            Args:
                request (~.vmwareengine.CreatePrivateConnectionRequest):
                    The request object. Request message for
                [VmwareEngine.CreatePrivateConnection][google.cloud.vmwareengine.v1.VmwareEngine.CreatePrivateConnection]
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
                    "uri": "/v1/{parent=projects/*/locations/*}/privateConnections",
                    "body": "private_connection",
                },
            ]
            request, metadata = self._interceptor.pre_create_private_connection(
                request, metadata
            )
            pb_request = vmwareengine.CreatePrivateConnectionRequest.pb(request)
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
            resp = self._interceptor.post_create_private_connection(resp)
            return resp

    class _CreateVmwareEngineNetwork(VmwareEngineRestStub):
        def __hash__(self):
            return hash("CreateVmwareEngineNetwork")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "vmwareEngineNetworkId": "",
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
            request: vmwareengine.CreateVmwareEngineNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create vmware engine
            network method over HTTP.

                Args:
                    request (~.vmwareengine.CreateVmwareEngineNetworkRequest):
                        The request object. Request message for
                    [VmwareEngine.CreateVmwareEngineNetwork][google.cloud.vmwareengine.v1.VmwareEngine.CreateVmwareEngineNetwork]
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
                    "uri": "/v1/{parent=projects/*/locations/*}/vmwareEngineNetworks",
                    "body": "vmware_engine_network",
                },
            ]
            request, metadata = self._interceptor.pre_create_vmware_engine_network(
                request, metadata
            )
            pb_request = vmwareengine.CreateVmwareEngineNetworkRequest.pb(request)
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
            resp = self._interceptor.post_create_vmware_engine_network(resp)
            return resp

    class _DeleteCluster(VmwareEngineRestStub):
        def __hash__(self):
            return hash("DeleteCluster")

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
            request: vmwareengine.DeleteClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete cluster method over HTTP.

            Args:
                request (~.vmwareengine.DeleteClusterRequest):
                    The request object. Request message for
                [VmwareEngine.DeleteCluster][google.cloud.vmwareengine.v1.VmwareEngine.DeleteCluster]
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
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/clusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_cluster(request, metadata)
            pb_request = vmwareengine.DeleteClusterRequest.pb(request)
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
            resp = self._interceptor.post_delete_cluster(resp)
            return resp

    class _DeleteExternalAccessRule(VmwareEngineRestStub):
        def __hash__(self):
            return hash("DeleteExternalAccessRule")

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
            request: vmwareengine.DeleteExternalAccessRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete external access
            rule method over HTTP.

                Args:
                    request (~.vmwareengine.DeleteExternalAccessRuleRequest):
                        The request object. Request message for
                    [VmwareEngine.DeleteExternalAccessRule][google.cloud.vmwareengine.v1.VmwareEngine.DeleteExternalAccessRule]
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
                    "uri": "/v1/{name=projects/*/locations/*/networkPolicies/*/externalAccessRules/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_external_access_rule(
                request, metadata
            )
            pb_request = vmwareengine.DeleteExternalAccessRuleRequest.pb(request)
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
            resp = self._interceptor.post_delete_external_access_rule(resp)
            return resp

    class _DeleteExternalAddress(VmwareEngineRestStub):
        def __hash__(self):
            return hash("DeleteExternalAddress")

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
            request: vmwareengine.DeleteExternalAddressRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete external address method over HTTP.

            Args:
                request (~.vmwareengine.DeleteExternalAddressRequest):
                    The request object. Request message for
                [VmwareEngine.DeleteExternalAddress][google.cloud.vmwareengine.v1.VmwareEngine.DeleteExternalAddress]
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
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/externalAddresses/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_external_address(
                request, metadata
            )
            pb_request = vmwareengine.DeleteExternalAddressRequest.pb(request)
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
            resp = self._interceptor.post_delete_external_address(resp)
            return resp

    class _DeleteLoggingServer(VmwareEngineRestStub):
        def __hash__(self):
            return hash("DeleteLoggingServer")

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
            request: vmwareengine.DeleteLoggingServerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete logging server method over HTTP.

            Args:
                request (~.vmwareengine.DeleteLoggingServerRequest):
                    The request object. Request message for
                [VmwareEngine.DeleteLoggingServer][google.cloud.vmwareengine.v1.VmwareEngine.DeleteLoggingServer]
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
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/loggingServers/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_logging_server(
                request, metadata
            )
            pb_request = vmwareengine.DeleteLoggingServerRequest.pb(request)
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
            resp = self._interceptor.post_delete_logging_server(resp)
            return resp

    class _DeleteManagementDnsZoneBinding(VmwareEngineRestStub):
        def __hash__(self):
            return hash("DeleteManagementDnsZoneBinding")

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
            request: vmwareengine.DeleteManagementDnsZoneBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete management dns
            zone binding method over HTTP.

                Args:
                    request (~.vmwareengine.DeleteManagementDnsZoneBindingRequest):
                        The request object. Request message for
                    [VmwareEngine.DeleteManagementDnsZoneBinding][google.cloud.vmwareengine.v1.VmwareEngine.DeleteManagementDnsZoneBinding]
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
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/managementDnsZoneBindings/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_management_dns_zone_binding(
                request, metadata
            )
            pb_request = vmwareengine.DeleteManagementDnsZoneBindingRequest.pb(request)
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
            resp = self._interceptor.post_delete_management_dns_zone_binding(resp)
            return resp

    class _DeleteNetworkPeering(VmwareEngineRestStub):
        def __hash__(self):
            return hash("DeleteNetworkPeering")

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
            request: vmwareengine.DeleteNetworkPeeringRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete network peering method over HTTP.

            Args:
                request (~.vmwareengine.DeleteNetworkPeeringRequest):
                    The request object. Request message for
                [VmwareEngine.DeleteNetworkPeering][google.cloud.vmwareengine.v1.VmwareEngine.DeleteNetworkPeering]
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
                    "uri": "/v1/{name=projects/*/locations/*/networkPeerings/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_network_peering(
                request, metadata
            )
            pb_request = vmwareengine.DeleteNetworkPeeringRequest.pb(request)
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
            resp = self._interceptor.post_delete_network_peering(resp)
            return resp

    class _DeleteNetworkPolicy(VmwareEngineRestStub):
        def __hash__(self):
            return hash("DeleteNetworkPolicy")

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
            request: vmwareengine.DeleteNetworkPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete network policy method over HTTP.

            Args:
                request (~.vmwareengine.DeleteNetworkPolicyRequest):
                    The request object. Request message for
                [VmwareEngine.DeleteNetworkPolicy][google.cloud.vmwareengine.v1.VmwareEngine.DeleteNetworkPolicy]
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
                    "uri": "/v1/{name=projects/*/locations/*/networkPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_network_policy(
                request, metadata
            )
            pb_request = vmwareengine.DeleteNetworkPolicyRequest.pb(request)
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
            resp = self._interceptor.post_delete_network_policy(resp)
            return resp

    class _DeletePrivateCloud(VmwareEngineRestStub):
        def __hash__(self):
            return hash("DeletePrivateCloud")

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
            request: vmwareengine.DeletePrivateCloudRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete private cloud method over HTTP.

            Args:
                request (~.vmwareengine.DeletePrivateCloudRequest):
                    The request object. Request message for
                [VmwareEngine.DeletePrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.DeletePrivateCloud]
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
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_private_cloud(
                request, metadata
            )
            pb_request = vmwareengine.DeletePrivateCloudRequest.pb(request)
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
            resp = self._interceptor.post_delete_private_cloud(resp)
            return resp

    class _DeletePrivateConnection(VmwareEngineRestStub):
        def __hash__(self):
            return hash("DeletePrivateConnection")

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
            request: vmwareengine.DeletePrivateConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete private connection method over HTTP.

            Args:
                request (~.vmwareengine.DeletePrivateConnectionRequest):
                    The request object. Request message for
                [VmwareEngine.DeletePrivateConnection][google.cloud.vmwareengine.v1.VmwareEngine.DeletePrivateConnection]
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
                    "uri": "/v1/{name=projects/*/locations/*/privateConnections/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_private_connection(
                request, metadata
            )
            pb_request = vmwareengine.DeletePrivateConnectionRequest.pb(request)
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
            resp = self._interceptor.post_delete_private_connection(resp)
            return resp

    class _DeleteVmwareEngineNetwork(VmwareEngineRestStub):
        def __hash__(self):
            return hash("DeleteVmwareEngineNetwork")

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
            request: vmwareengine.DeleteVmwareEngineNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete vmware engine
            network method over HTTP.

                Args:
                    request (~.vmwareengine.DeleteVmwareEngineNetworkRequest):
                        The request object. Request message for
                    [VmwareEngine.DeleteVmwareEngineNetwork][google.cloud.vmwareengine.v1.VmwareEngine.DeleteVmwareEngineNetwork]
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
                    "uri": "/v1/{name=projects/*/locations/*/vmwareEngineNetworks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_vmware_engine_network(
                request, metadata
            )
            pb_request = vmwareengine.DeleteVmwareEngineNetworkRequest.pb(request)
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
            resp = self._interceptor.post_delete_vmware_engine_network(resp)
            return resp

    class _FetchNetworkPolicyExternalAddresses(VmwareEngineRestStub):
        def __hash__(self):
            return hash("FetchNetworkPolicyExternalAddresses")

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
            request: vmwareengine.FetchNetworkPolicyExternalAddressesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.FetchNetworkPolicyExternalAddressesResponse:
            r"""Call the fetch network policy
            external addresses method over HTTP.

                Args:
                    request (~.vmwareengine.FetchNetworkPolicyExternalAddressesRequest):
                        The request object. Request message for
                    [VmwareEngine.FetchNetworkPolicyExternalAddresses][google.cloud.vmwareengine.v1.VmwareEngine.FetchNetworkPolicyExternalAddresses]
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.vmwareengine.FetchNetworkPolicyExternalAddressesResponse:
                        Response message for
                    [VmwareEngine.FetchNetworkPolicyExternalAddresses][google.cloud.vmwareengine.v1.VmwareEngine.FetchNetworkPolicyExternalAddresses]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{network_policy=projects/*/locations/*/networkPolicies/*}:fetchExternalAddresses",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_fetch_network_policy_external_addresses(
                request, metadata
            )
            pb_request = vmwareengine.FetchNetworkPolicyExternalAddressesRequest.pb(
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
            resp = vmwareengine.FetchNetworkPolicyExternalAddressesResponse()
            pb_resp = vmwareengine.FetchNetworkPolicyExternalAddressesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_network_policy_external_addresses(resp)
            return resp

    class _GetCluster(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetCluster")

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
            request: vmwareengine.GetClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.Cluster:
            r"""Call the get cluster method over HTTP.

            Args:
                request (~.vmwareengine.GetClusterRequest):
                    The request object. Request message for
                [VmwareEngine.GetCluster][google.cloud.vmwareengine.v1.VmwareEngine.GetCluster]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.Cluster:
                    A cluster in a private cloud.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/clusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_cluster(request, metadata)
            pb_request = vmwareengine.GetClusterRequest.pb(request)
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
            resp = vmwareengine_resources.Cluster()
            pb_resp = vmwareengine_resources.Cluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_cluster(resp)
            return resp

    class _GetDnsBindPermission(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetDnsBindPermission")

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
            request: vmwareengine.GetDnsBindPermissionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.DnsBindPermission:
            r"""Call the get dns bind permission method over HTTP.

            Args:
                request (~.vmwareengine.GetDnsBindPermissionRequest):
                    The request object. Request message for
                [VmwareEngine.GetDnsBindPermission][google.cloud.vmwareengine.v1.VmwareEngine.GetDnsBindPermission]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.DnsBindPermission:
                    DnsBindPermission resource that
                contains the accounts having the
                consumer DNS bind permission on the
                corresponding intranet VPC of the
                consumer project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/dnsBindPermission}",
                },
            ]
            request, metadata = self._interceptor.pre_get_dns_bind_permission(
                request, metadata
            )
            pb_request = vmwareengine.GetDnsBindPermissionRequest.pb(request)
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
            resp = vmwareengine_resources.DnsBindPermission()
            pb_resp = vmwareengine_resources.DnsBindPermission.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_dns_bind_permission(resp)
            return resp

    class _GetDnsForwarding(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetDnsForwarding")

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
            request: vmwareengine.GetDnsForwardingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.DnsForwarding:
            r"""Call the get dns forwarding method over HTTP.

            Args:
                request (~.vmwareengine.GetDnsForwardingRequest):
                    The request object. Request message for
                [VmwareEngine.GetDnsForwarding][google.cloud.vmwareengine.v1.VmwareEngine.GetDnsForwarding]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.DnsForwarding:
                    DNS forwarding config.
                This config defines a list of domain to
                name server mappings, and is attached to
                the private cloud for custom domain
                resolution.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/dnsForwarding}",
                },
            ]
            request, metadata = self._interceptor.pre_get_dns_forwarding(
                request, metadata
            )
            pb_request = vmwareengine.GetDnsForwardingRequest.pb(request)
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
            resp = vmwareengine_resources.DnsForwarding()
            pb_resp = vmwareengine_resources.DnsForwarding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_dns_forwarding(resp)
            return resp

    class _GetExternalAccessRule(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetExternalAccessRule")

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
            request: vmwareengine.GetExternalAccessRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.ExternalAccessRule:
            r"""Call the get external access rule method over HTTP.

            Args:
                request (~.vmwareengine.GetExternalAccessRuleRequest):
                    The request object. Request message for
                [VmwareEngine.GetExternalAccessRule][google.cloud.vmwareengine.v1.VmwareEngine.GetExternalAccessRule]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.ExternalAccessRule:
                    External access firewall rules for filtering incoming
                traffic destined to ``ExternalAddress`` resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/networkPolicies/*/externalAccessRules/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_external_access_rule(
                request, metadata
            )
            pb_request = vmwareengine.GetExternalAccessRuleRequest.pb(request)
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
            resp = vmwareengine_resources.ExternalAccessRule()
            pb_resp = vmwareengine_resources.ExternalAccessRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_external_access_rule(resp)
            return resp

    class _GetExternalAddress(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetExternalAddress")

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
            request: vmwareengine.GetExternalAddressRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.ExternalAddress:
            r"""Call the get external address method over HTTP.

            Args:
                request (~.vmwareengine.GetExternalAddressRequest):
                    The request object. Request message for
                [VmwareEngine.GetExternalAddress][google.cloud.vmwareengine.v1.VmwareEngine.GetExternalAddress]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.ExternalAddress:
                    Represents an allocated external IP
                address and its corresponding internal
                IP address in a private cloud.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/externalAddresses/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_external_address(
                request, metadata
            )
            pb_request = vmwareengine.GetExternalAddressRequest.pb(request)
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
            resp = vmwareengine_resources.ExternalAddress()
            pb_resp = vmwareengine_resources.ExternalAddress.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_external_address(resp)
            return resp

    class _GetHcxActivationKey(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetHcxActivationKey")

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
            request: vmwareengine.GetHcxActivationKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.HcxActivationKey:
            r"""Call the get hcx activation key method over HTTP.

            Args:
                request (~.vmwareengine.GetHcxActivationKeyRequest):
                    The request object. Request message for
                [VmwareEngine.GetHcxActivationKeys][]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.HcxActivationKey:
                    HCX activation key. A default key is created during
                private cloud provisioning, but this behavior is subject
                to change and you should always verify active keys. Use
                [VmwareEngine.ListHcxActivationKeys][google.cloud.vmwareengine.v1.VmwareEngine.ListHcxActivationKeys]
                to retrieve existing keys and
                [VmwareEngine.CreateHcxActivationKey][google.cloud.vmwareengine.v1.VmwareEngine.CreateHcxActivationKey]
                to create new ones.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/hcxActivationKeys/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_hcx_activation_key(
                request, metadata
            )
            pb_request = vmwareengine.GetHcxActivationKeyRequest.pb(request)
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
            resp = vmwareengine_resources.HcxActivationKey()
            pb_resp = vmwareengine_resources.HcxActivationKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_hcx_activation_key(resp)
            return resp

    class _GetLoggingServer(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetLoggingServer")

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
            request: vmwareengine.GetLoggingServerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.LoggingServer:
            r"""Call the get logging server method over HTTP.

            Args:
                request (~.vmwareengine.GetLoggingServerRequest):
                    The request object. Request message for
                [VmwareEngine.GetLoggingServer][google.cloud.vmwareengine.v1.VmwareEngine.GetLoggingServer]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.LoggingServer:
                    Logging server to receive vCenter or
                ESXi logs.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/loggingServers/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_logging_server(
                request, metadata
            )
            pb_request = vmwareengine.GetLoggingServerRequest.pb(request)
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
            resp = vmwareengine_resources.LoggingServer()
            pb_resp = vmwareengine_resources.LoggingServer.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_logging_server(resp)
            return resp

    class _GetManagementDnsZoneBinding(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetManagementDnsZoneBinding")

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
            request: vmwareengine.GetManagementDnsZoneBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.ManagementDnsZoneBinding:
            r"""Call the get management dns zone
            binding method over HTTP.

                Args:
                    request (~.vmwareengine.GetManagementDnsZoneBindingRequest):
                        The request object. Request message for
                    [VmwareEngine.GetManagementDnsZoneBinding][google.cloud.vmwareengine.v1.VmwareEngine.GetManagementDnsZoneBinding]
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.vmwareengine_resources.ManagementDnsZoneBinding:
                        Represents a binding between a
                    network and the management DNS zone. A
                    management DNS zone is the Cloud DNS
                    cross-project binding zone that VMware
                    Engine creates for each private cloud.
                    It contains FQDNs and corresponding IP
                    addresses for the private cloud's ESXi
                    hosts and management VM appliances like
                    vCenter and NSX Manager.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/managementDnsZoneBindings/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_management_dns_zone_binding(
                request, metadata
            )
            pb_request = vmwareengine.GetManagementDnsZoneBindingRequest.pb(request)
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
            resp = vmwareengine_resources.ManagementDnsZoneBinding()
            pb_resp = vmwareengine_resources.ManagementDnsZoneBinding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_management_dns_zone_binding(resp)
            return resp

    class _GetNetworkPeering(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetNetworkPeering")

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
            request: vmwareengine.GetNetworkPeeringRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.NetworkPeering:
            r"""Call the get network peering method over HTTP.

            Args:
                request (~.vmwareengine.GetNetworkPeeringRequest):
                    The request object. Request message for
                [VmwareEngine.GetNetworkPeering][google.cloud.vmwareengine.v1.VmwareEngine.GetNetworkPeering]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.NetworkPeering:
                    Details of a network peering.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/networkPeerings/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_network_peering(
                request, metadata
            )
            pb_request = vmwareengine.GetNetworkPeeringRequest.pb(request)
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
            resp = vmwareengine_resources.NetworkPeering()
            pb_resp = vmwareengine_resources.NetworkPeering.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_network_peering(resp)
            return resp

    class _GetNetworkPolicy(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetNetworkPolicy")

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
            request: vmwareengine.GetNetworkPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.NetworkPolicy:
            r"""Call the get network policy method over HTTP.

            Args:
                request (~.vmwareengine.GetNetworkPolicyRequest):
                    The request object. Request message for
                [VmwareEngine.GetNetworkPolicy][google.cloud.vmwareengine.v1.VmwareEngine.GetNetworkPolicy]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.NetworkPolicy:
                    Represents a network policy resource.
                Network policies are regional resources.
                You can use a network policy to enable
                or disable internet access and external
                IP access. Network policies are
                associated with a VMware Engine network,
                which might span across regions. For a
                given region, a network policy applies
                to all private clouds in the VMware
                Engine network associated with the
                policy.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/networkPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_network_policy(
                request, metadata
            )
            pb_request = vmwareengine.GetNetworkPolicyRequest.pb(request)
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
            resp = vmwareengine_resources.NetworkPolicy()
            pb_resp = vmwareengine_resources.NetworkPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_network_policy(resp)
            return resp

    class _GetNode(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetNode")

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
            request: vmwareengine.GetNodeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.Node:
            r"""Call the get node method over HTTP.

            Args:
                request (~.vmwareengine.GetNodeRequest):
                    The request object. Request message for
                [VmwareEngine.GetNode][google.cloud.vmwareengine.v1.VmwareEngine.GetNode]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.Node:
                    Node in a cluster.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/clusters/*/nodes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_node(request, metadata)
            pb_request = vmwareengine.GetNodeRequest.pb(request)
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
            resp = vmwareengine_resources.Node()
            pb_resp = vmwareengine_resources.Node.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_node(resp)
            return resp

    class _GetNodeType(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetNodeType")

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
            request: vmwareengine.GetNodeTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.NodeType:
            r"""Call the get node type method over HTTP.

            Args:
                request (~.vmwareengine.GetNodeTypeRequest):
                    The request object. Request message for
                [VmwareEngine.GetNodeType][google.cloud.vmwareengine.v1.VmwareEngine.GetNodeType]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.NodeType:
                    Describes node type.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/nodeTypes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_node_type(request, metadata)
            pb_request = vmwareengine.GetNodeTypeRequest.pb(request)
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
            resp = vmwareengine_resources.NodeType()
            pb_resp = vmwareengine_resources.NodeType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_node_type(resp)
            return resp

    class _GetPrivateCloud(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetPrivateCloud")

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
            request: vmwareengine.GetPrivateCloudRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.PrivateCloud:
            r"""Call the get private cloud method over HTTP.

            Args:
                request (~.vmwareengine.GetPrivateCloudRequest):
                    The request object. Request message for
                [VmwareEngine.GetPrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.GetPrivateCloud]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.PrivateCloud:
                    Represents a private cloud resource. Private clouds of
                type ``STANDARD`` and ``TIME_LIMITED`` are zonal
                resources, ``STRETCHED`` private clouds are regional.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_private_cloud(
                request, metadata
            )
            pb_request = vmwareengine.GetPrivateCloudRequest.pb(request)
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
            resp = vmwareengine_resources.PrivateCloud()
            pb_resp = vmwareengine_resources.PrivateCloud.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_private_cloud(resp)
            return resp

    class _GetPrivateConnection(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetPrivateConnection")

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
            request: vmwareengine.GetPrivateConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.PrivateConnection:
            r"""Call the get private connection method over HTTP.

            Args:
                request (~.vmwareengine.GetPrivateConnectionRequest):
                    The request object. Request message for
                [VmwareEngine.GetPrivateConnection][google.cloud.vmwareengine.v1.VmwareEngine.GetPrivateConnection]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.PrivateConnection:
                    Private connection resource that
                provides connectivity for VMware Engine
                private clouds.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/privateConnections/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_private_connection(
                request, metadata
            )
            pb_request = vmwareengine.GetPrivateConnectionRequest.pb(request)
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
            resp = vmwareengine_resources.PrivateConnection()
            pb_resp = vmwareengine_resources.PrivateConnection.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_private_connection(resp)
            return resp

    class _GetSubnet(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetSubnet")

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
            request: vmwareengine.GetSubnetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.Subnet:
            r"""Call the get subnet method over HTTP.

            Args:
                request (~.vmwareengine.GetSubnetRequest):
                    The request object. Request message for
                [VmwareEngine.GetSubnet][google.cloud.vmwareengine.v1.VmwareEngine.GetSubnet]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.Subnet:
                    Subnet in a private cloud. Either ``management`` subnets
                (such as vMotion) that are read-only, or
                ``userDefined``, which can also be updated.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/subnets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_subnet(request, metadata)
            pb_request = vmwareengine.GetSubnetRequest.pb(request)
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
            resp = vmwareengine_resources.Subnet()
            pb_resp = vmwareengine_resources.Subnet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_subnet(resp)
            return resp

    class _GetVmwareEngineNetwork(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GetVmwareEngineNetwork")

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
            request: vmwareengine.GetVmwareEngineNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.VmwareEngineNetwork:
            r"""Call the get vmware engine network method over HTTP.

            Args:
                request (~.vmwareengine.GetVmwareEngineNetworkRequest):
                    The request object. Request message for
                [VmwareEngine.GetVmwareEngineNetwork][google.cloud.vmwareengine.v1.VmwareEngine.GetVmwareEngineNetwork]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.VmwareEngineNetwork:
                    VMware Engine network resource that
                provides connectivity for VMware Engine
                private clouds.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/vmwareEngineNetworks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_vmware_engine_network(
                request, metadata
            )
            pb_request = vmwareengine.GetVmwareEngineNetworkRequest.pb(request)
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
            resp = vmwareengine_resources.VmwareEngineNetwork()
            pb_resp = vmwareengine_resources.VmwareEngineNetwork.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_vmware_engine_network(resp)
            return resp

    class _GrantDnsBindPermission(VmwareEngineRestStub):
        def __hash__(self):
            return hash("GrantDnsBindPermission")

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
            request: vmwareengine.GrantDnsBindPermissionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the grant dns bind permission method over HTTP.

            Args:
                request (~.vmwareengine.GrantDnsBindPermissionRequest):
                    The request object. Request message for
                [VmwareEngine.GrantDnsBindPermission][google.cloud.vmwareengine.v1.VmwareEngine.GrantDnsBindPermission]
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
                    "uri": "/v1/{name=projects/*/locations/*/dnsBindPermission}:grant",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_grant_dns_bind_permission(
                request, metadata
            )
            pb_request = vmwareengine.GrantDnsBindPermissionRequest.pb(request)
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
            resp = self._interceptor.post_grant_dns_bind_permission(resp)
            return resp

    class _ListClusters(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListClusters")

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
            request: vmwareengine.ListClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListClustersResponse:
            r"""Call the list clusters method over HTTP.

            Args:
                request (~.vmwareengine.ListClustersRequest):
                    The request object. Request message for
                [VmwareEngine.ListClusters][google.cloud.vmwareengine.v1.VmwareEngine.ListClusters]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListClustersResponse:
                    Response message for
                [VmwareEngine.ListClusters][google.cloud.vmwareengine.v1.VmwareEngine.ListClusters]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/clusters",
                },
            ]
            request, metadata = self._interceptor.pre_list_clusters(request, metadata)
            pb_request = vmwareengine.ListClustersRequest.pb(request)
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
            resp = vmwareengine.ListClustersResponse()
            pb_resp = vmwareengine.ListClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_clusters(resp)
            return resp

    class _ListExternalAccessRules(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListExternalAccessRules")

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
            request: vmwareengine.ListExternalAccessRulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListExternalAccessRulesResponse:
            r"""Call the list external access
            rules method over HTTP.

                Args:
                    request (~.vmwareengine.ListExternalAccessRulesRequest):
                        The request object. Request message for
                    [VmwareEngine.ListExternalAccessRules][google.cloud.vmwareengine.v1.VmwareEngine.ListExternalAccessRules]
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.vmwareengine.ListExternalAccessRulesResponse:
                        Response message for
                    [VmwareEngine.ListExternalAccessRules][google.cloud.vmwareengine.v1.VmwareEngine.ListExternalAccessRules]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/networkPolicies/*}/externalAccessRules",
                },
            ]
            request, metadata = self._interceptor.pre_list_external_access_rules(
                request, metadata
            )
            pb_request = vmwareengine.ListExternalAccessRulesRequest.pb(request)
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
            resp = vmwareengine.ListExternalAccessRulesResponse()
            pb_resp = vmwareengine.ListExternalAccessRulesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_external_access_rules(resp)
            return resp

    class _ListExternalAddresses(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListExternalAddresses")

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
            request: vmwareengine.ListExternalAddressesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListExternalAddressesResponse:
            r"""Call the list external addresses method over HTTP.

            Args:
                request (~.vmwareengine.ListExternalAddressesRequest):
                    The request object. Request message for
                [VmwareEngine.ListExternalAddresses][google.cloud.vmwareengine.v1.VmwareEngine.ListExternalAddresses]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListExternalAddressesResponse:
                    Response message for
                [VmwareEngine.ListExternalAddresses][google.cloud.vmwareengine.v1.VmwareEngine.ListExternalAddresses]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/externalAddresses",
                },
            ]
            request, metadata = self._interceptor.pre_list_external_addresses(
                request, metadata
            )
            pb_request = vmwareengine.ListExternalAddressesRequest.pb(request)
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
            resp = vmwareengine.ListExternalAddressesResponse()
            pb_resp = vmwareengine.ListExternalAddressesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_external_addresses(resp)
            return resp

    class _ListHcxActivationKeys(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListHcxActivationKeys")

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
            request: vmwareengine.ListHcxActivationKeysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListHcxActivationKeysResponse:
            r"""Call the list hcx activation keys method over HTTP.

            Args:
                request (~.vmwareengine.ListHcxActivationKeysRequest):
                    The request object. Request message for
                [VmwareEngine.ListHcxActivationKeys][google.cloud.vmwareengine.v1.VmwareEngine.ListHcxActivationKeys]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListHcxActivationKeysResponse:
                    Response message for
                [VmwareEngine.ListHcxActivationKeys][google.cloud.vmwareengine.v1.VmwareEngine.ListHcxActivationKeys]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/hcxActivationKeys",
                },
            ]
            request, metadata = self._interceptor.pre_list_hcx_activation_keys(
                request, metadata
            )
            pb_request = vmwareengine.ListHcxActivationKeysRequest.pb(request)
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
            resp = vmwareengine.ListHcxActivationKeysResponse()
            pb_resp = vmwareengine.ListHcxActivationKeysResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_hcx_activation_keys(resp)
            return resp

    class _ListLoggingServers(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListLoggingServers")

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
            request: vmwareengine.ListLoggingServersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListLoggingServersResponse:
            r"""Call the list logging servers method over HTTP.

            Args:
                request (~.vmwareengine.ListLoggingServersRequest):
                    The request object. Request message for
                [VmwareEngine.ListLoggingServers][google.cloud.vmwareengine.v1.VmwareEngine.ListLoggingServers]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListLoggingServersResponse:
                    Response message for
                [VmwareEngine.ListLoggingServers][google.cloud.vmwareengine.v1.VmwareEngine.ListLoggingServers]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/loggingServers",
                },
            ]
            request, metadata = self._interceptor.pre_list_logging_servers(
                request, metadata
            )
            pb_request = vmwareengine.ListLoggingServersRequest.pb(request)
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
            resp = vmwareengine.ListLoggingServersResponse()
            pb_resp = vmwareengine.ListLoggingServersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_logging_servers(resp)
            return resp

    class _ListManagementDnsZoneBindings(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListManagementDnsZoneBindings")

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
            request: vmwareengine.ListManagementDnsZoneBindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListManagementDnsZoneBindingsResponse:
            r"""Call the list management dns zone
            bindings method over HTTP.

                Args:
                    request (~.vmwareengine.ListManagementDnsZoneBindingsRequest):
                        The request object. Request message for
                    [VmwareEngine.ListManagementDnsZoneBindings][google.cloud.vmwareengine.v1.VmwareEngine.ListManagementDnsZoneBindings]
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.vmwareengine.ListManagementDnsZoneBindingsResponse:
                        Response message for
                    [VmwareEngine.ListManagementDnsZoneBindings][google.cloud.vmwareengine.v1.VmwareEngine.ListManagementDnsZoneBindings]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/managementDnsZoneBindings",
                },
            ]
            request, metadata = self._interceptor.pre_list_management_dns_zone_bindings(
                request, metadata
            )
            pb_request = vmwareengine.ListManagementDnsZoneBindingsRequest.pb(request)
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
            resp = vmwareengine.ListManagementDnsZoneBindingsResponse()
            pb_resp = vmwareengine.ListManagementDnsZoneBindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_management_dns_zone_bindings(resp)
            return resp

    class _ListNetworkPeerings(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListNetworkPeerings")

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
            request: vmwareengine.ListNetworkPeeringsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListNetworkPeeringsResponse:
            r"""Call the list network peerings method over HTTP.

            Args:
                request (~.vmwareengine.ListNetworkPeeringsRequest):
                    The request object. Request message for
                [VmwareEngine.ListNetworkPeerings][google.cloud.vmwareengine.v1.VmwareEngine.ListNetworkPeerings]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListNetworkPeeringsResponse:
                    Response message for
                [VmwareEngine.ListNetworkPeerings][google.cloud.vmwareengine.v1.VmwareEngine.ListNetworkPeerings]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/networkPeerings",
                },
            ]
            request, metadata = self._interceptor.pre_list_network_peerings(
                request, metadata
            )
            pb_request = vmwareengine.ListNetworkPeeringsRequest.pb(request)
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
            resp = vmwareengine.ListNetworkPeeringsResponse()
            pb_resp = vmwareengine.ListNetworkPeeringsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_network_peerings(resp)
            return resp

    class _ListNetworkPolicies(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListNetworkPolicies")

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
            request: vmwareengine.ListNetworkPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListNetworkPoliciesResponse:
            r"""Call the list network policies method over HTTP.

            Args:
                request (~.vmwareengine.ListNetworkPoliciesRequest):
                    The request object. Request message for
                [VmwareEngine.ListNetworkPolicies][google.cloud.vmwareengine.v1.VmwareEngine.ListNetworkPolicies]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListNetworkPoliciesResponse:
                    Response message for
                [VmwareEngine.ListNetworkPolicies][google.cloud.vmwareengine.v1.VmwareEngine.ListNetworkPolicies]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/networkPolicies",
                },
            ]
            request, metadata = self._interceptor.pre_list_network_policies(
                request, metadata
            )
            pb_request = vmwareengine.ListNetworkPoliciesRequest.pb(request)
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
            resp = vmwareengine.ListNetworkPoliciesResponse()
            pb_resp = vmwareengine.ListNetworkPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_network_policies(resp)
            return resp

    class _ListNodes(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListNodes")

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
            request: vmwareengine.ListNodesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListNodesResponse:
            r"""Call the list nodes method over HTTP.

            Args:
                request (~.vmwareengine.ListNodesRequest):
                    The request object. Request message for
                [VmwareEngine.ListNodes][google.cloud.vmwareengine.v1.VmwareEngine.ListNodes]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListNodesResponse:
                    Response message for
                [VmwareEngine.ListNodes][google.cloud.vmwareengine.v1.VmwareEngine.ListNodes]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*/clusters/*}/nodes",
                },
            ]
            request, metadata = self._interceptor.pre_list_nodes(request, metadata)
            pb_request = vmwareengine.ListNodesRequest.pb(request)
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
            resp = vmwareengine.ListNodesResponse()
            pb_resp = vmwareengine.ListNodesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_nodes(resp)
            return resp

    class _ListNodeTypes(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListNodeTypes")

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
            request: vmwareengine.ListNodeTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListNodeTypesResponse:
            r"""Call the list node types method over HTTP.

            Args:
                request (~.vmwareengine.ListNodeTypesRequest):
                    The request object. Request message for
                [VmwareEngine.ListNodeTypes][google.cloud.vmwareengine.v1.VmwareEngine.ListNodeTypes]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListNodeTypesResponse:
                    Response message for
                [VmwareEngine.ListNodeTypes][google.cloud.vmwareengine.v1.VmwareEngine.ListNodeTypes]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/nodeTypes",
                },
            ]
            request, metadata = self._interceptor.pre_list_node_types(request, metadata)
            pb_request = vmwareengine.ListNodeTypesRequest.pb(request)
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
            resp = vmwareengine.ListNodeTypesResponse()
            pb_resp = vmwareengine.ListNodeTypesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_node_types(resp)
            return resp

    class _ListPeeringRoutes(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListPeeringRoutes")

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
            request: vmwareengine.ListPeeringRoutesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListPeeringRoutesResponse:
            r"""Call the list peering routes method over HTTP.

            Args:
                request (~.vmwareengine.ListPeeringRoutesRequest):
                    The request object. Request message for
                [VmwareEngine.ListPeeringRoutes][google.cloud.vmwareengine.v1.VmwareEngine.ListPeeringRoutes]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListPeeringRoutesResponse:
                    Response message for
                [VmwareEngine.ListPeeringRoutes][google.cloud.vmwareengine.v1.VmwareEngine.ListPeeringRoutes]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/networkPeerings/*}/peeringRoutes",
                },
            ]
            request, metadata = self._interceptor.pre_list_peering_routes(
                request, metadata
            )
            pb_request = vmwareengine.ListPeeringRoutesRequest.pb(request)
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
            resp = vmwareengine.ListPeeringRoutesResponse()
            pb_resp = vmwareengine.ListPeeringRoutesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_peering_routes(resp)
            return resp

    class _ListPrivateClouds(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListPrivateClouds")

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
            request: vmwareengine.ListPrivateCloudsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListPrivateCloudsResponse:
            r"""Call the list private clouds method over HTTP.

            Args:
                request (~.vmwareengine.ListPrivateCloudsRequest):
                    The request object. Request message for
                [VmwareEngine.ListPrivateClouds][google.cloud.vmwareengine.v1.VmwareEngine.ListPrivateClouds]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListPrivateCloudsResponse:
                    Response message for
                [VmwareEngine.ListPrivateClouds][google.cloud.vmwareengine.v1.VmwareEngine.ListPrivateClouds]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/privateClouds",
                },
            ]
            request, metadata = self._interceptor.pre_list_private_clouds(
                request, metadata
            )
            pb_request = vmwareengine.ListPrivateCloudsRequest.pb(request)
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
            resp = vmwareengine.ListPrivateCloudsResponse()
            pb_resp = vmwareengine.ListPrivateCloudsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_private_clouds(resp)
            return resp

    class _ListPrivateConnectionPeeringRoutes(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListPrivateConnectionPeeringRoutes")

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
            request: vmwareengine.ListPrivateConnectionPeeringRoutesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListPrivateConnectionPeeringRoutesResponse:
            r"""Call the list private connection
            peering routes method over HTTP.

                Args:
                    request (~.vmwareengine.ListPrivateConnectionPeeringRoutesRequest):
                        The request object. Request message for
                    [VmwareEngine.ListPrivateConnectionPeeringRoutes][google.cloud.vmwareengine.v1.VmwareEngine.ListPrivateConnectionPeeringRoutes]
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.vmwareengine.ListPrivateConnectionPeeringRoutesResponse:
                        Response message for
                    [VmwareEngine.ListPrivateConnectionPeeringRoutes][google.cloud.vmwareengine.v1.VmwareEngine.ListPrivateConnectionPeeringRoutes]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/privateConnections/*}/peeringRoutes",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_private_connection_peering_routes(
                request, metadata
            )
            pb_request = vmwareengine.ListPrivateConnectionPeeringRoutesRequest.pb(
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
            resp = vmwareengine.ListPrivateConnectionPeeringRoutesResponse()
            pb_resp = vmwareengine.ListPrivateConnectionPeeringRoutesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_private_connection_peering_routes(resp)
            return resp

    class _ListPrivateConnections(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListPrivateConnections")

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
            request: vmwareengine.ListPrivateConnectionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListPrivateConnectionsResponse:
            r"""Call the list private connections method over HTTP.

            Args:
                request (~.vmwareengine.ListPrivateConnectionsRequest):
                    The request object. Request message for
                [VmwareEngine.ListPrivateConnections][google.cloud.vmwareengine.v1.VmwareEngine.ListPrivateConnections]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListPrivateConnectionsResponse:
                    Response message for
                [VmwareEngine.ListPrivateConnections][google.cloud.vmwareengine.v1.VmwareEngine.ListPrivateConnections]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/privateConnections",
                },
            ]
            request, metadata = self._interceptor.pre_list_private_connections(
                request, metadata
            )
            pb_request = vmwareengine.ListPrivateConnectionsRequest.pb(request)
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
            resp = vmwareengine.ListPrivateConnectionsResponse()
            pb_resp = vmwareengine.ListPrivateConnectionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_private_connections(resp)
            return resp

    class _ListSubnets(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListSubnets")

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
            request: vmwareengine.ListSubnetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListSubnetsResponse:
            r"""Call the list subnets method over HTTP.

            Args:
                request (~.vmwareengine.ListSubnetsRequest):
                    The request object. Request message for
                [VmwareEngine.ListSubnets][google.cloud.vmwareengine.v1.VmwareEngine.ListSubnets]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine.ListSubnetsResponse:
                    Response message for
                [VmwareEngine.ListSubnets][google.cloud.vmwareengine.v1.VmwareEngine.ListSubnets]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/privateClouds/*}/subnets",
                },
            ]
            request, metadata = self._interceptor.pre_list_subnets(request, metadata)
            pb_request = vmwareengine.ListSubnetsRequest.pb(request)
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
            resp = vmwareengine.ListSubnetsResponse()
            pb_resp = vmwareengine.ListSubnetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_subnets(resp)
            return resp

    class _ListVmwareEngineNetworks(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ListVmwareEngineNetworks")

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
            request: vmwareengine.ListVmwareEngineNetworksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine.ListVmwareEngineNetworksResponse:
            r"""Call the list vmware engine
            networks method over HTTP.

                Args:
                    request (~.vmwareengine.ListVmwareEngineNetworksRequest):
                        The request object. Request message for
                    [VmwareEngine.ListVmwareEngineNetworks][google.cloud.vmwareengine.v1.VmwareEngine.ListVmwareEngineNetworks]
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.vmwareengine.ListVmwareEngineNetworksResponse:
                        Response message for
                    [VmwareEngine.ListVmwareEngineNetworks][google.cloud.vmwareengine.v1.VmwareEngine.ListVmwareEngineNetworks]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/vmwareEngineNetworks",
                },
            ]
            request, metadata = self._interceptor.pre_list_vmware_engine_networks(
                request, metadata
            )
            pb_request = vmwareengine.ListVmwareEngineNetworksRequest.pb(request)
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
            resp = vmwareengine.ListVmwareEngineNetworksResponse()
            pb_resp = vmwareengine.ListVmwareEngineNetworksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_vmware_engine_networks(resp)
            return resp

    class _RepairManagementDnsZoneBinding(VmwareEngineRestStub):
        def __hash__(self):
            return hash("RepairManagementDnsZoneBinding")

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
            request: vmwareengine.RepairManagementDnsZoneBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the repair management dns
            zone binding method over HTTP.

                Args:
                    request (~.vmwareengine.RepairManagementDnsZoneBindingRequest):
                        The request object. Request message for
                    [VmwareEngine.RepairManagementDnsZoneBindings][]
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
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*/managementDnsZoneBindings/*}:repair",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_repair_management_dns_zone_binding(
                request, metadata
            )
            pb_request = vmwareengine.RepairManagementDnsZoneBindingRequest.pb(request)
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
            resp = self._interceptor.post_repair_management_dns_zone_binding(resp)
            return resp

    class _ResetNsxCredentials(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ResetNsxCredentials")

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
            request: vmwareengine.ResetNsxCredentialsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the reset nsx credentials method over HTTP.

            Args:
                request (~.vmwareengine.ResetNsxCredentialsRequest):
                    The request object. Request message for
                [VmwareEngine.ResetNsxCredentials][google.cloud.vmwareengine.v1.VmwareEngine.ResetNsxCredentials]
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
                    "uri": "/v1/{private_cloud=projects/*/locations/*/privateClouds/*}:resetNsxCredentials",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_reset_nsx_credentials(
                request, metadata
            )
            pb_request = vmwareengine.ResetNsxCredentialsRequest.pb(request)
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
            resp = self._interceptor.post_reset_nsx_credentials(resp)
            return resp

    class _ResetVcenterCredentials(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ResetVcenterCredentials")

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
            request: vmwareengine.ResetVcenterCredentialsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the reset vcenter credentials method over HTTP.

            Args:
                request (~.vmwareengine.ResetVcenterCredentialsRequest):
                    The request object. Request message for
                [VmwareEngine.ResetVcenterCredentials][google.cloud.vmwareengine.v1.VmwareEngine.ResetVcenterCredentials]
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
                    "uri": "/v1/{private_cloud=projects/*/locations/*/privateClouds/*}:resetVcenterCredentials",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_reset_vcenter_credentials(
                request, metadata
            )
            pb_request = vmwareengine.ResetVcenterCredentialsRequest.pb(request)
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
            resp = self._interceptor.post_reset_vcenter_credentials(resp)
            return resp

    class _RevokeDnsBindPermission(VmwareEngineRestStub):
        def __hash__(self):
            return hash("RevokeDnsBindPermission")

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
            request: vmwareengine.RevokeDnsBindPermissionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the revoke dns bind
            permission method over HTTP.

                Args:
                    request (~.vmwareengine.RevokeDnsBindPermissionRequest):
                        The request object. Request message for
                    [VmwareEngine.RevokeDnsBindPermission][google.cloud.vmwareengine.v1.VmwareEngine.RevokeDnsBindPermission]
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
                    "uri": "/v1/{name=projects/*/locations/*/dnsBindPermission}:revoke",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_revoke_dns_bind_permission(
                request, metadata
            )
            pb_request = vmwareengine.RevokeDnsBindPermissionRequest.pb(request)
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
            resp = self._interceptor.post_revoke_dns_bind_permission(resp)
            return resp

    class _ShowNsxCredentials(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ShowNsxCredentials")

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
            request: vmwareengine.ShowNsxCredentialsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.Credentials:
            r"""Call the show nsx credentials method over HTTP.

            Args:
                request (~.vmwareengine.ShowNsxCredentialsRequest):
                    The request object. Request message for
                [VmwareEngine.ShowNsxCredentials][google.cloud.vmwareengine.v1.VmwareEngine.ShowNsxCredentials]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.Credentials:
                    Credentials for a private cloud.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{private_cloud=projects/*/locations/*/privateClouds/*}:showNsxCredentials",
                },
            ]
            request, metadata = self._interceptor.pre_show_nsx_credentials(
                request, metadata
            )
            pb_request = vmwareengine.ShowNsxCredentialsRequest.pb(request)
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
            resp = vmwareengine_resources.Credentials()
            pb_resp = vmwareengine_resources.Credentials.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_show_nsx_credentials(resp)
            return resp

    class _ShowVcenterCredentials(VmwareEngineRestStub):
        def __hash__(self):
            return hash("ShowVcenterCredentials")

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
            request: vmwareengine.ShowVcenterCredentialsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmwareengine_resources.Credentials:
            r"""Call the show vcenter credentials method over HTTP.

            Args:
                request (~.vmwareengine.ShowVcenterCredentialsRequest):
                    The request object. Request message for
                [VmwareEngine.ShowVcenterCredentials][google.cloud.vmwareengine.v1.VmwareEngine.ShowVcenterCredentials]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmwareengine_resources.Credentials:
                    Credentials for a private cloud.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{private_cloud=projects/*/locations/*/privateClouds/*}:showVcenterCredentials",
                },
            ]
            request, metadata = self._interceptor.pre_show_vcenter_credentials(
                request, metadata
            )
            pb_request = vmwareengine.ShowVcenterCredentialsRequest.pb(request)
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
            resp = vmwareengine_resources.Credentials()
            pb_resp = vmwareengine_resources.Credentials.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_show_vcenter_credentials(resp)
            return resp

    class _UndeletePrivateCloud(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UndeletePrivateCloud")

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
            request: vmwareengine.UndeletePrivateCloudRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undelete private cloud method over HTTP.

            Args:
                request (~.vmwareengine.UndeletePrivateCloudRequest):
                    The request object. Request message for
                [VmwareEngine.UndeletePrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.UndeletePrivateCloud]
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
                    "uri": "/v1/{name=projects/*/locations/*/privateClouds/*}:undelete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_undelete_private_cloud(
                request, metadata
            )
            pb_request = vmwareengine.UndeletePrivateCloudRequest.pb(request)
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
            resp = self._interceptor.post_undelete_private_cloud(resp)
            return resp

    class _UpdateCluster(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdateCluster")

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
            request: vmwareengine.UpdateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update cluster method over HTTP.

            Args:
                request (~.vmwareengine.UpdateClusterRequest):
                    The request object. Request message for
                [VmwareEngine.UpdateCluster][google.cloud.vmwareengine.v1.VmwareEngine.UpdateCluster]
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
                    "uri": "/v1/{cluster.name=projects/*/locations/*/privateClouds/*/clusters/*}",
                    "body": "cluster",
                },
            ]
            request, metadata = self._interceptor.pre_update_cluster(request, metadata)
            pb_request = vmwareengine.UpdateClusterRequest.pb(request)
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
            resp = self._interceptor.post_update_cluster(resp)
            return resp

    class _UpdateDnsForwarding(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdateDnsForwarding")

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
            request: vmwareengine.UpdateDnsForwardingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update dns forwarding method over HTTP.

            Args:
                request (~.vmwareengine.UpdateDnsForwardingRequest):
                    The request object. Request message for
                [VmwareEngine.UpdateDnsForwarding][google.cloud.vmwareengine.v1.VmwareEngine.UpdateDnsForwarding]
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
                    "uri": "/v1/{dns_forwarding.name=projects/*/locations/*/privateClouds/*/dnsForwarding}",
                    "body": "dns_forwarding",
                },
            ]
            request, metadata = self._interceptor.pre_update_dns_forwarding(
                request, metadata
            )
            pb_request = vmwareengine.UpdateDnsForwardingRequest.pb(request)
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
            resp = self._interceptor.post_update_dns_forwarding(resp)
            return resp

    class _UpdateExternalAccessRule(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdateExternalAccessRule")

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
            request: vmwareengine.UpdateExternalAccessRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update external access
            rule method over HTTP.

                Args:
                    request (~.vmwareengine.UpdateExternalAccessRuleRequest):
                        The request object. Request message for
                    [VmwareEngine.UpdateExternalAccessRule][google.cloud.vmwareengine.v1.VmwareEngine.UpdateExternalAccessRule]
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
                    "uri": "/v1/{external_access_rule.name=projects/*/locations/*/networkPolicies/*/externalAccessRules/*}",
                    "body": "external_access_rule",
                },
            ]
            request, metadata = self._interceptor.pre_update_external_access_rule(
                request, metadata
            )
            pb_request = vmwareengine.UpdateExternalAccessRuleRequest.pb(request)
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
            resp = self._interceptor.post_update_external_access_rule(resp)
            return resp

    class _UpdateExternalAddress(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdateExternalAddress")

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
            request: vmwareengine.UpdateExternalAddressRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update external address method over HTTP.

            Args:
                request (~.vmwareengine.UpdateExternalAddressRequest):
                    The request object. Request message for
                [VmwareEngine.UpdateExternalAddress][google.cloud.vmwareengine.v1.VmwareEngine.UpdateExternalAddress]
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
                    "uri": "/v1/{external_address.name=projects/*/locations/*/privateClouds/*/externalAddresses/*}",
                    "body": "external_address",
                },
            ]
            request, metadata = self._interceptor.pre_update_external_address(
                request, metadata
            )
            pb_request = vmwareengine.UpdateExternalAddressRequest.pb(request)
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
            resp = self._interceptor.post_update_external_address(resp)
            return resp

    class _UpdateLoggingServer(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdateLoggingServer")

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
            request: vmwareengine.UpdateLoggingServerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update logging server method over HTTP.

            Args:
                request (~.vmwareengine.UpdateLoggingServerRequest):
                    The request object. Request message for
                [VmwareEngine.UpdateLoggingServer][google.cloud.vmwareengine.v1.VmwareEngine.UpdateLoggingServer]
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
                    "uri": "/v1/{logging_server.name=projects/*/locations/*/privateClouds/*/loggingServers/*}",
                    "body": "logging_server",
                },
            ]
            request, metadata = self._interceptor.pre_update_logging_server(
                request, metadata
            )
            pb_request = vmwareengine.UpdateLoggingServerRequest.pb(request)
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
            resp = self._interceptor.post_update_logging_server(resp)
            return resp

    class _UpdateManagementDnsZoneBinding(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdateManagementDnsZoneBinding")

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
            request: vmwareengine.UpdateManagementDnsZoneBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update management dns
            zone binding method over HTTP.

                Args:
                    request (~.vmwareengine.UpdateManagementDnsZoneBindingRequest):
                        The request object. Request message for
                    [VmwareEngine.UpdateManagementDnsZoneBinding][google.cloud.vmwareengine.v1.VmwareEngine.UpdateManagementDnsZoneBinding]
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
                    "uri": "/v1/{management_dns_zone_binding.name=projects/*/locations/*/privateClouds/*/managementDnsZoneBindings/*}",
                    "body": "management_dns_zone_binding",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_update_management_dns_zone_binding(
                request, metadata
            )
            pb_request = vmwareengine.UpdateManagementDnsZoneBindingRequest.pb(request)
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
            resp = self._interceptor.post_update_management_dns_zone_binding(resp)
            return resp

    class _UpdateNetworkPeering(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdateNetworkPeering")

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
            request: vmwareengine.UpdateNetworkPeeringRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update network peering method over HTTP.

            Args:
                request (~.vmwareengine.UpdateNetworkPeeringRequest):
                    The request object. Request message for
                [VmwareEngine.UpdateNetworkPeering][google.cloud.vmwareengine.v1.VmwareEngine.UpdateNetworkPeering]
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
                    "uri": "/v1/{network_peering.name=projects/*/locations/*/networkPeerings/*}",
                    "body": "network_peering",
                },
            ]
            request, metadata = self._interceptor.pre_update_network_peering(
                request, metadata
            )
            pb_request = vmwareengine.UpdateNetworkPeeringRequest.pb(request)
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
            resp = self._interceptor.post_update_network_peering(resp)
            return resp

    class _UpdateNetworkPolicy(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdateNetworkPolicy")

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
            request: vmwareengine.UpdateNetworkPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update network policy method over HTTP.

            Args:
                request (~.vmwareengine.UpdateNetworkPolicyRequest):
                    The request object. Request message for
                [VmwareEngine.UpdateNetworkPolicy][google.cloud.vmwareengine.v1.VmwareEngine.UpdateNetworkPolicy]
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
                    "uri": "/v1/{network_policy.name=projects/*/locations/*/networkPolicies/*}",
                    "body": "network_policy",
                },
            ]
            request, metadata = self._interceptor.pre_update_network_policy(
                request, metadata
            )
            pb_request = vmwareengine.UpdateNetworkPolicyRequest.pb(request)
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
            resp = self._interceptor.post_update_network_policy(resp)
            return resp

    class _UpdatePrivateCloud(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdatePrivateCloud")

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
            request: vmwareengine.UpdatePrivateCloudRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update private cloud method over HTTP.

            Args:
                request (~.vmwareengine.UpdatePrivateCloudRequest):
                    The request object. Request message for
                [VmwareEngine.UpdatePrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.UpdatePrivateCloud]
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
                    "uri": "/v1/{private_cloud.name=projects/*/locations/*/privateClouds/*}",
                    "body": "private_cloud",
                },
            ]
            request, metadata = self._interceptor.pre_update_private_cloud(
                request, metadata
            )
            pb_request = vmwareengine.UpdatePrivateCloudRequest.pb(request)
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
            resp = self._interceptor.post_update_private_cloud(resp)
            return resp

    class _UpdatePrivateConnection(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdatePrivateConnection")

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
            request: vmwareengine.UpdatePrivateConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update private connection method over HTTP.

            Args:
                request (~.vmwareengine.UpdatePrivateConnectionRequest):
                    The request object. Request message for
                [VmwareEngine.UpdatePrivateConnection][google.cloud.vmwareengine.v1.VmwareEngine.UpdatePrivateConnection]
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
                    "uri": "/v1/{private_connection.name=projects/*/locations/*/privateConnections/*}",
                    "body": "private_connection",
                },
            ]
            request, metadata = self._interceptor.pre_update_private_connection(
                request, metadata
            )
            pb_request = vmwareengine.UpdatePrivateConnectionRequest.pb(request)
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
            resp = self._interceptor.post_update_private_connection(resp)
            return resp

    class _UpdateSubnet(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdateSubnet")

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
            request: vmwareengine.UpdateSubnetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update subnet method over HTTP.

            Args:
                request (~.vmwareengine.UpdateSubnetRequest):
                    The request object. Request message for
                [VmwareEngine.UpdateSubnet][google.cloud.vmwareengine.v1.VmwareEngine.UpdateSubnet]
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
                    "uri": "/v1/{subnet.name=projects/*/locations/*/privateClouds/*/subnets/*}",
                    "body": "subnet",
                },
            ]
            request, metadata = self._interceptor.pre_update_subnet(request, metadata)
            pb_request = vmwareengine.UpdateSubnetRequest.pb(request)
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
            resp = self._interceptor.post_update_subnet(resp)
            return resp

    class _UpdateVmwareEngineNetwork(VmwareEngineRestStub):
        def __hash__(self):
            return hash("UpdateVmwareEngineNetwork")

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
            request: vmwareengine.UpdateVmwareEngineNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update vmware engine
            network method over HTTP.

                Args:
                    request (~.vmwareengine.UpdateVmwareEngineNetworkRequest):
                        The request object. Request message for
                    [VmwareEngine.UpdateVmwareEngineNetwork][google.cloud.vmwareengine.v1.VmwareEngine.UpdateVmwareEngineNetwork]
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
                    "uri": "/v1/{vmware_engine_network.name=projects/*/locations/*/vmwareEngineNetworks/*}",
                    "body": "vmware_engine_network",
                },
            ]
            request, metadata = self._interceptor.pre_update_vmware_engine_network(
                request, metadata
            )
            pb_request = vmwareengine.UpdateVmwareEngineNetworkRequest.pb(request)
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
            resp = self._interceptor.post_update_vmware_engine_network(resp)
            return resp

    @property
    def create_cluster(
        self,
    ) -> Callable[[vmwareengine.CreateClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_external_access_rule(
        self,
    ) -> Callable[
        [vmwareengine.CreateExternalAccessRuleRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateExternalAccessRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_external_address(
        self,
    ) -> Callable[
        [vmwareengine.CreateExternalAddressRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateExternalAddress(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_hcx_activation_key(
        self,
    ) -> Callable[
        [vmwareengine.CreateHcxActivationKeyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateHcxActivationKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_logging_server(
        self,
    ) -> Callable[[vmwareengine.CreateLoggingServerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateLoggingServer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_management_dns_zone_binding(
        self,
    ) -> Callable[
        [vmwareengine.CreateManagementDnsZoneBindingRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateManagementDnsZoneBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_network_peering(
        self,
    ) -> Callable[[vmwareengine.CreateNetworkPeeringRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateNetworkPeering(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_network_policy(
        self,
    ) -> Callable[[vmwareengine.CreateNetworkPolicyRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateNetworkPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_private_cloud(
        self,
    ) -> Callable[[vmwareengine.CreatePrivateCloudRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreatePrivateCloud(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_private_connection(
        self,
    ) -> Callable[
        [vmwareengine.CreatePrivateConnectionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreatePrivateConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_vmware_engine_network(
        self,
    ) -> Callable[
        [vmwareengine.CreateVmwareEngineNetworkRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateVmwareEngineNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_cluster(
        self,
    ) -> Callable[[vmwareengine.DeleteClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_external_access_rule(
        self,
    ) -> Callable[
        [vmwareengine.DeleteExternalAccessRuleRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteExternalAccessRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_external_address(
        self,
    ) -> Callable[
        [vmwareengine.DeleteExternalAddressRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteExternalAddress(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_logging_server(
        self,
    ) -> Callable[[vmwareengine.DeleteLoggingServerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteLoggingServer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_management_dns_zone_binding(
        self,
    ) -> Callable[
        [vmwareengine.DeleteManagementDnsZoneBindingRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteManagementDnsZoneBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_network_peering(
        self,
    ) -> Callable[[vmwareengine.DeleteNetworkPeeringRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteNetworkPeering(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_network_policy(
        self,
    ) -> Callable[[vmwareengine.DeleteNetworkPolicyRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteNetworkPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_private_cloud(
        self,
    ) -> Callable[[vmwareengine.DeletePrivateCloudRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePrivateCloud(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_private_connection(
        self,
    ) -> Callable[
        [vmwareengine.DeletePrivateConnectionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePrivateConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_vmware_engine_network(
        self,
    ) -> Callable[
        [vmwareengine.DeleteVmwareEngineNetworkRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteVmwareEngineNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_network_policy_external_addresses(
        self,
    ) -> Callable[
        [vmwareengine.FetchNetworkPolicyExternalAddressesRequest],
        vmwareengine.FetchNetworkPolicyExternalAddressesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchNetworkPolicyExternalAddresses(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cluster(
        self,
    ) -> Callable[[vmwareengine.GetClusterRequest], vmwareengine_resources.Cluster]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_dns_bind_permission(
        self,
    ) -> Callable[
        [vmwareengine.GetDnsBindPermissionRequest],
        vmwareengine_resources.DnsBindPermission,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDnsBindPermission(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_dns_forwarding(
        self,
    ) -> Callable[
        [vmwareengine.GetDnsForwardingRequest], vmwareengine_resources.DnsForwarding
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDnsForwarding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_external_access_rule(
        self,
    ) -> Callable[
        [vmwareengine.GetExternalAccessRuleRequest],
        vmwareengine_resources.ExternalAccessRule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetExternalAccessRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_external_address(
        self,
    ) -> Callable[
        [vmwareengine.GetExternalAddressRequest], vmwareengine_resources.ExternalAddress
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetExternalAddress(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_hcx_activation_key(
        self,
    ) -> Callable[
        [vmwareengine.GetHcxActivationKeyRequest],
        vmwareengine_resources.HcxActivationKey,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetHcxActivationKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_logging_server(
        self,
    ) -> Callable[
        [vmwareengine.GetLoggingServerRequest], vmwareengine_resources.LoggingServer
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetLoggingServer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_management_dns_zone_binding(
        self,
    ) -> Callable[
        [vmwareengine.GetManagementDnsZoneBindingRequest],
        vmwareengine_resources.ManagementDnsZoneBinding,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetManagementDnsZoneBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_network_peering(
        self,
    ) -> Callable[
        [vmwareengine.GetNetworkPeeringRequest], vmwareengine_resources.NetworkPeering
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNetworkPeering(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_network_policy(
        self,
    ) -> Callable[
        [vmwareengine.GetNetworkPolicyRequest], vmwareengine_resources.NetworkPolicy
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNetworkPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_node(
        self,
    ) -> Callable[[vmwareengine.GetNodeRequest], vmwareengine_resources.Node]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNode(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_node_type(
        self,
    ) -> Callable[[vmwareengine.GetNodeTypeRequest], vmwareengine_resources.NodeType]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNodeType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_private_cloud(
        self,
    ) -> Callable[
        [vmwareengine.GetPrivateCloudRequest], vmwareengine_resources.PrivateCloud
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPrivateCloud(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_private_connection(
        self,
    ) -> Callable[
        [vmwareengine.GetPrivateConnectionRequest],
        vmwareengine_resources.PrivateConnection,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPrivateConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_subnet(
        self,
    ) -> Callable[[vmwareengine.GetSubnetRequest], vmwareengine_resources.Subnet]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSubnet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_vmware_engine_network(
        self,
    ) -> Callable[
        [vmwareengine.GetVmwareEngineNetworkRequest],
        vmwareengine_resources.VmwareEngineNetwork,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVmwareEngineNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def grant_dns_bind_permission(
        self,
    ) -> Callable[
        [vmwareengine.GrantDnsBindPermissionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GrantDnsBindPermission(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_clusters(
        self,
    ) -> Callable[
        [vmwareengine.ListClustersRequest], vmwareengine.ListClustersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_external_access_rules(
        self,
    ) -> Callable[
        [vmwareengine.ListExternalAccessRulesRequest],
        vmwareengine.ListExternalAccessRulesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListExternalAccessRules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_external_addresses(
        self,
    ) -> Callable[
        [vmwareengine.ListExternalAddressesRequest],
        vmwareengine.ListExternalAddressesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListExternalAddresses(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_hcx_activation_keys(
        self,
    ) -> Callable[
        [vmwareengine.ListHcxActivationKeysRequest],
        vmwareengine.ListHcxActivationKeysResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListHcxActivationKeys(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_logging_servers(
        self,
    ) -> Callable[
        [vmwareengine.ListLoggingServersRequest],
        vmwareengine.ListLoggingServersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListLoggingServers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_management_dns_zone_bindings(
        self,
    ) -> Callable[
        [vmwareengine.ListManagementDnsZoneBindingsRequest],
        vmwareengine.ListManagementDnsZoneBindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListManagementDnsZoneBindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_network_peerings(
        self,
    ) -> Callable[
        [vmwareengine.ListNetworkPeeringsRequest],
        vmwareengine.ListNetworkPeeringsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNetworkPeerings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_network_policies(
        self,
    ) -> Callable[
        [vmwareengine.ListNetworkPoliciesRequest],
        vmwareengine.ListNetworkPoliciesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNetworkPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_nodes(
        self,
    ) -> Callable[[vmwareengine.ListNodesRequest], vmwareengine.ListNodesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNodes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_node_types(
        self,
    ) -> Callable[
        [vmwareengine.ListNodeTypesRequest], vmwareengine.ListNodeTypesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNodeTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_peering_routes(
        self,
    ) -> Callable[
        [vmwareengine.ListPeeringRoutesRequest], vmwareengine.ListPeeringRoutesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPeeringRoutes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_private_clouds(
        self,
    ) -> Callable[
        [vmwareengine.ListPrivateCloudsRequest], vmwareengine.ListPrivateCloudsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPrivateClouds(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_private_connection_peering_routes(
        self,
    ) -> Callable[
        [vmwareengine.ListPrivateConnectionPeeringRoutesRequest],
        vmwareengine.ListPrivateConnectionPeeringRoutesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPrivateConnectionPeeringRoutes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_private_connections(
        self,
    ) -> Callable[
        [vmwareengine.ListPrivateConnectionsRequest],
        vmwareengine.ListPrivateConnectionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPrivateConnections(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_subnets(
        self,
    ) -> Callable[[vmwareengine.ListSubnetsRequest], vmwareengine.ListSubnetsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSubnets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_vmware_engine_networks(
        self,
    ) -> Callable[
        [vmwareengine.ListVmwareEngineNetworksRequest],
        vmwareengine.ListVmwareEngineNetworksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVmwareEngineNetworks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def repair_management_dns_zone_binding(
        self,
    ) -> Callable[
        [vmwareengine.RepairManagementDnsZoneBindingRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RepairManagementDnsZoneBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def reset_nsx_credentials(
        self,
    ) -> Callable[[vmwareengine.ResetNsxCredentialsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResetNsxCredentials(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def reset_vcenter_credentials(
        self,
    ) -> Callable[
        [vmwareengine.ResetVcenterCredentialsRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResetVcenterCredentials(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def revoke_dns_bind_permission(
        self,
    ) -> Callable[
        [vmwareengine.RevokeDnsBindPermissionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RevokeDnsBindPermission(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def show_nsx_credentials(
        self,
    ) -> Callable[
        [vmwareengine.ShowNsxCredentialsRequest], vmwareengine_resources.Credentials
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ShowNsxCredentials(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def show_vcenter_credentials(
        self,
    ) -> Callable[
        [vmwareengine.ShowVcenterCredentialsRequest], vmwareengine_resources.Credentials
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ShowVcenterCredentials(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undelete_private_cloud(
        self,
    ) -> Callable[[vmwareengine.UndeletePrivateCloudRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeletePrivateCloud(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_cluster(
        self,
    ) -> Callable[[vmwareengine.UpdateClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_dns_forwarding(
        self,
    ) -> Callable[[vmwareengine.UpdateDnsForwardingRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDnsForwarding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_external_access_rule(
        self,
    ) -> Callable[
        [vmwareengine.UpdateExternalAccessRuleRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateExternalAccessRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_external_address(
        self,
    ) -> Callable[
        [vmwareengine.UpdateExternalAddressRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateExternalAddress(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_logging_server(
        self,
    ) -> Callable[[vmwareengine.UpdateLoggingServerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateLoggingServer(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_management_dns_zone_binding(
        self,
    ) -> Callable[
        [vmwareengine.UpdateManagementDnsZoneBindingRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateManagementDnsZoneBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_network_peering(
        self,
    ) -> Callable[[vmwareengine.UpdateNetworkPeeringRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateNetworkPeering(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_network_policy(
        self,
    ) -> Callable[[vmwareengine.UpdateNetworkPolicyRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateNetworkPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_private_cloud(
        self,
    ) -> Callable[[vmwareengine.UpdatePrivateCloudRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePrivateCloud(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_private_connection(
        self,
    ) -> Callable[
        [vmwareengine.UpdatePrivateConnectionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePrivateConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_subnet(
        self,
    ) -> Callable[[vmwareengine.UpdateSubnetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSubnet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_vmware_engine_network(
        self,
    ) -> Callable[
        [vmwareengine.UpdateVmwareEngineNetworkRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateVmwareEngineNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(VmwareEngineRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
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

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(VmwareEngineRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
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

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(VmwareEngineRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/privateClouds/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/privateClouds/*/clusters/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/privateClouds/*/hcxActivationKeys/*}:getIamPolicy",
                },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(VmwareEngineRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/privateClouds/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/privateClouds/*/clusters/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/privateClouds/*/hcxActivationKeys/*}:setIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(VmwareEngineRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/privateClouds/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/privateClouds/*/clusters/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/privateClouds/*/hcxActivationKeys/*}:testIamPermissions",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(
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

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(VmwareEngineRestStub):
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

    class _GetOperation(VmwareEngineRestStub):
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

    class _ListOperations(VmwareEngineRestStub):
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


__all__ = ("VmwareEngineRestTransport",)
