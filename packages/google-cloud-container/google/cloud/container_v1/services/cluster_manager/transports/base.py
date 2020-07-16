# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import abc
import typing

from google import auth
from google.api_core import exceptions  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.container_v1.types import cluster_service
from google.protobuf import empty_pb2 as empty  # type: ignore


class ClusterManagerTransport(abc.ABC):
    """Abstract transport class for ClusterManager."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "container.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes
            )
        elif credentials is None:
            credentials, _ = auth.default(scopes=scopes)

        # Save the credentials.
        self._credentials = credentials

    @property
    def list_clusters(
        self,
    ) -> typing.Callable[
        [cluster_service.ListClustersRequest],
        typing.Union[
            cluster_service.ListClustersResponse,
            typing.Awaitable[cluster_service.ListClustersResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_cluster(
        self,
    ) -> typing.Callable[
        [cluster_service.GetClusterRequest],
        typing.Union[
            cluster_service.Cluster, typing.Awaitable[cluster_service.Cluster]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_cluster(
        self,
    ) -> typing.Callable[
        [cluster_service.CreateClusterRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_cluster(
        self,
    ) -> typing.Callable[
        [cluster_service.UpdateClusterRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_node_pool(
        self,
    ) -> typing.Callable[
        [cluster_service.UpdateNodePoolRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_node_pool_autoscaling(
        self,
    ) -> typing.Callable[
        [cluster_service.SetNodePoolAutoscalingRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_logging_service(
        self,
    ) -> typing.Callable[
        [cluster_service.SetLoggingServiceRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_monitoring_service(
        self,
    ) -> typing.Callable[
        [cluster_service.SetMonitoringServiceRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_addons_config(
        self,
    ) -> typing.Callable[
        [cluster_service.SetAddonsConfigRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_locations(
        self,
    ) -> typing.Callable[
        [cluster_service.SetLocationsRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_master(
        self,
    ) -> typing.Callable[
        [cluster_service.UpdateMasterRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_master_auth(
        self,
    ) -> typing.Callable[
        [cluster_service.SetMasterAuthRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_cluster(
        self,
    ) -> typing.Callable[
        [cluster_service.DeleteClusterRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_operations(
        self,
    ) -> typing.Callable[
        [cluster_service.ListOperationsRequest],
        typing.Union[
            cluster_service.ListOperationsResponse,
            typing.Awaitable[cluster_service.ListOperationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_operation(
        self,
    ) -> typing.Callable[
        [cluster_service.GetOperationRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def cancel_operation(
        self,
    ) -> typing.Callable[
        [cluster_service.CancelOperationRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_server_config(
        self,
    ) -> typing.Callable[
        [cluster_service.GetServerConfigRequest],
        typing.Union[
            cluster_service.ServerConfig, typing.Awaitable[cluster_service.ServerConfig]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_node_pools(
        self,
    ) -> typing.Callable[
        [cluster_service.ListNodePoolsRequest],
        typing.Union[
            cluster_service.ListNodePoolsResponse,
            typing.Awaitable[cluster_service.ListNodePoolsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_node_pool(
        self,
    ) -> typing.Callable[
        [cluster_service.GetNodePoolRequest],
        typing.Union[
            cluster_service.NodePool, typing.Awaitable[cluster_service.NodePool]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_node_pool(
        self,
    ) -> typing.Callable[
        [cluster_service.CreateNodePoolRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_node_pool(
        self,
    ) -> typing.Callable[
        [cluster_service.DeleteNodePoolRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def rollback_node_pool_upgrade(
        self,
    ) -> typing.Callable[
        [cluster_service.RollbackNodePoolUpgradeRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_node_pool_management(
        self,
    ) -> typing.Callable[
        [cluster_service.SetNodePoolManagementRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_labels(
        self,
    ) -> typing.Callable[
        [cluster_service.SetLabelsRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_legacy_abac(
        self,
    ) -> typing.Callable[
        [cluster_service.SetLegacyAbacRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def start_ip_rotation(
        self,
    ) -> typing.Callable[
        [cluster_service.StartIPRotationRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def complete_ip_rotation(
        self,
    ) -> typing.Callable[
        [cluster_service.CompleteIPRotationRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_node_pool_size(
        self,
    ) -> typing.Callable[
        [cluster_service.SetNodePoolSizeRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_network_policy(
        self,
    ) -> typing.Callable[
        [cluster_service.SetNetworkPolicyRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_maintenance_policy(
        self,
    ) -> typing.Callable[
        [cluster_service.SetMaintenancePolicyRequest],
        typing.Union[
            cluster_service.Operation, typing.Awaitable[cluster_service.Operation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_usable_subnetworks(
        self,
    ) -> typing.Callable[
        [cluster_service.ListUsableSubnetworksRequest],
        typing.Union[
            cluster_service.ListUsableSubnetworksResponse,
            typing.Awaitable[cluster_service.ListUsableSubnetworksResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("ClusterManagerTransport",)
