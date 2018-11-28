# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.api_core.grpc_helpers

from google.cloud.container_v1.proto import cluster_service_pb2_grpc


class ClusterManagerGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.container.v1 ClusterManager API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="container.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "cluster_manager_stub": cluster_service_pb2_grpc.ClusterManagerStub(channel)
        }

    @classmethod
    def create_channel(cls, address="container.googleapis.com:443", credentials=None):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_clusters(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Lists all clusters owned by a project in either the specified zone or all
        zones.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].ListClusters

    @property
    def get_cluster(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Gets the details of a specific cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].GetCluster

    @property
    def create_cluster(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Creates a cluster, consisting of the specified number and type of Google
        Compute Engine instances.

        By default, the cluster is created in the project's `default
        network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__.

        One firewall is added for the cluster. After cluster creation, the
        cluster creates routes for each node to allow the containers on that
        node to communicate with all other instances in the cluster.

        Finally, an entry is added to the project's global metadata indicating
        which CIDR range is being used by the cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].CreateCluster

    @property
    def update_cluster(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Updates the settings of a specific cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].UpdateCluster

    @property
    def update_node_pool(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Updates the version and/or image type for a specific node pool.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].UpdateNodePool

    @property
    def set_node_pool_autoscaling(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Sets the autoscaling settings for a specific node pool.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetNodePoolAutoscaling

    @property
    def set_logging_service(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Sets the logging service for a specific cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetLoggingService

    @property
    def set_monitoring_service(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Sets the monitoring service for a specific cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetMonitoringService

    @property
    def set_addons_config(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Sets the addons for a specific cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetAddonsConfig

    @property
    def set_locations(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Sets the locations for a specific cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetLocations

    @property
    def update_master(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Updates the master for a specific cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].UpdateMaster

    @property
    def set_master_auth(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Used to set master auth materials. Currently supports :-
        Changing the admin password for a specific cluster.
        This can be either via password generation or explicitly set the password.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetMasterAuth

    @property
    def delete_cluster(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Deletes the cluster, including the Kubernetes endpoint and all worker
        nodes.

        Firewalls and routes that were configured during cluster creation
        are also deleted.

        Other Google Compute Engine resources that might be in use by the cluster
        (e.g. load balancer resources) will not be deleted if they weren't present
        at the initial create time.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].DeleteCluster

    @property
    def list_operations(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Lists all operations in a project in a specific zone or all zones.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].ListOperations

    @property
    def get_operation(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Gets the specified operation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].GetOperation

    @property
    def cancel_operation(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Cancels the specified operation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].CancelOperation

    @property
    def get_server_config(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Returns configuration info about the Kubernetes Engine service.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].GetServerConfig

    @property
    def list_node_pools(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Lists the node pools for a cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].ListNodePools

    @property
    def get_node_pool(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Retrieves the node pool requested.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].GetNodePool

    @property
    def create_node_pool(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Creates a node pool for a cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].CreateNodePool

    @property
    def delete_node_pool(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Deletes a node pool from a cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].DeleteNodePool

    @property
    def rollback_node_pool_upgrade(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Roll back the previously Aborted or Failed NodePool upgrade.
        This will be an no-op if the last upgrade successfully completed.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].RollbackNodePoolUpgrade

    @property
    def set_node_pool_management(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Sets the NodeManagement options for a node pool.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetNodePoolManagement

    @property
    def set_labels(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Sets labels on a cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetLabels

    @property
    def set_legacy_abac(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Enables or disables the ABAC authorization mechanism on a cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetLegacyAbac

    @property
    def start_i_p_rotation(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Start master IP rotation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].StartIPRotation

    @property
    def complete_i_p_rotation(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Completes master IP rotation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].CompleteIPRotation

    @property
    def set_node_pool_size(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Sets the size for a specific node pool.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetNodePoolSize

    @property
    def set_network_policy(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Enables/Disables Network Policy for a cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetNetworkPolicy

    @property
    def set_maintenance_policy(self):
        """Return the gRPC stub for {$apiMethod.name}.

        Sets the maintenance policy for a cluster.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cluster_manager_stub"].SetMaintenancePolicy
