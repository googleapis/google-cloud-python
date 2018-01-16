# Copyright 2017, Google LLC All rights reserved.
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
"""Accesses the google.container.v1 ClusterManager API."""

import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers

from google.cloud.container_v1.gapic import cluster_manager_client_config
from google.cloud.container_v1.gapic import enums
from google.cloud.container_v1.proto import cluster_service_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-container', ).version


class ClusterManagerClient(object):
    """Google Container Engine Cluster Manager v1"""

    SERVICE_ADDRESS = 'container.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.container.v1.ClusterManager'

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=cluster_manager_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict): A dictionary of call options for each
                method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                'The `channel` and `credentials` arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__), )

        # Create the channel.
        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES,
            )

        # Create the gRPC stubs.
        self.cluster_manager_stub = (
            cluster_service_pb2.ClusterManagerStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Write the "inner API call" methods to the class.
        # These are wrapped versions of the gRPC stub methods, with retry and
        # timeout configuration applied, called by the public methods on
        # this class.
        self._list_clusters = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.ListClusters,
            default_retry=method_configs['ListClusters'].retry,
            default_timeout=method_configs['ListClusters'].timeout,
            client_info=client_info,
        )
        self._get_cluster = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.GetCluster,
            default_retry=method_configs['GetCluster'].retry,
            default_timeout=method_configs['GetCluster'].timeout,
            client_info=client_info,
        )
        self._create_cluster = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.CreateCluster,
            default_retry=method_configs['CreateCluster'].retry,
            default_timeout=method_configs['CreateCluster'].timeout,
            client_info=client_info,
        )
        self._update_cluster = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.UpdateCluster,
            default_retry=method_configs['UpdateCluster'].retry,
            default_timeout=method_configs['UpdateCluster'].timeout,
            client_info=client_info,
        )
        self._update_node_pool = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.UpdateNodePool,
            default_retry=method_configs['UpdateNodePool'].retry,
            default_timeout=method_configs['UpdateNodePool'].timeout,
            client_info=client_info,
        )
        self._set_node_pool_autoscaling = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetNodePoolAutoscaling,
            default_retry=method_configs['SetNodePoolAutoscaling'].retry,
            default_timeout=method_configs['SetNodePoolAutoscaling'].timeout,
            client_info=client_info,
        )
        self._set_logging_service = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetLoggingService,
            default_retry=method_configs['SetLoggingService'].retry,
            default_timeout=method_configs['SetLoggingService'].timeout,
            client_info=client_info,
        )
        self._set_monitoring_service = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetMonitoringService,
            default_retry=method_configs['SetMonitoringService'].retry,
            default_timeout=method_configs['SetMonitoringService'].timeout,
            client_info=client_info,
        )
        self._set_addons_config = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetAddonsConfig,
            default_retry=method_configs['SetAddonsConfig'].retry,
            default_timeout=method_configs['SetAddonsConfig'].timeout,
            client_info=client_info,
        )
        self._set_locations = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetLocations,
            default_retry=method_configs['SetLocations'].retry,
            default_timeout=method_configs['SetLocations'].timeout,
            client_info=client_info,
        )
        self._update_master = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.UpdateMaster,
            default_retry=method_configs['UpdateMaster'].retry,
            default_timeout=method_configs['UpdateMaster'].timeout,
            client_info=client_info,
        )
        self._set_master_auth = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetMasterAuth,
            default_retry=method_configs['SetMasterAuth'].retry,
            default_timeout=method_configs['SetMasterAuth'].timeout,
            client_info=client_info,
        )
        self._delete_cluster = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.DeleteCluster,
            default_retry=method_configs['DeleteCluster'].retry,
            default_timeout=method_configs['DeleteCluster'].timeout,
            client_info=client_info,
        )
        self._list_operations = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.ListOperations,
            default_retry=method_configs['ListOperations'].retry,
            default_timeout=method_configs['ListOperations'].timeout,
            client_info=client_info,
        )
        self._get_operation = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.GetOperation,
            default_retry=method_configs['GetOperation'].retry,
            default_timeout=method_configs['GetOperation'].timeout,
            client_info=client_info,
        )
        self._cancel_operation = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.CancelOperation,
            default_retry=method_configs['CancelOperation'].retry,
            default_timeout=method_configs['CancelOperation'].timeout,
            client_info=client_info,
        )
        self._get_server_config = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.GetServerConfig,
            default_retry=method_configs['GetServerConfig'].retry,
            default_timeout=method_configs['GetServerConfig'].timeout,
            client_info=client_info,
        )
        self._list_node_pools = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.ListNodePools,
            default_retry=method_configs['ListNodePools'].retry,
            default_timeout=method_configs['ListNodePools'].timeout,
            client_info=client_info,
        )
        self._get_node_pool = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.GetNodePool,
            default_retry=method_configs['GetNodePool'].retry,
            default_timeout=method_configs['GetNodePool'].timeout,
            client_info=client_info,
        )
        self._create_node_pool = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.CreateNodePool,
            default_retry=method_configs['CreateNodePool'].retry,
            default_timeout=method_configs['CreateNodePool'].timeout,
            client_info=client_info,
        )
        self._delete_node_pool = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.DeleteNodePool,
            default_retry=method_configs['DeleteNodePool'].retry,
            default_timeout=method_configs['DeleteNodePool'].timeout,
            client_info=client_info,
        )
        self._rollback_node_pool_upgrade = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.RollbackNodePoolUpgrade,
            default_retry=method_configs['RollbackNodePoolUpgrade'].retry,
            default_timeout=method_configs['RollbackNodePoolUpgrade'].timeout,
            client_info=client_info,
        )
        self._set_node_pool_management = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetNodePoolManagement,
            default_retry=method_configs['SetNodePoolManagement'].retry,
            default_timeout=method_configs['SetNodePoolManagement'].timeout,
            client_info=client_info,
        )
        self._set_labels = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetLabels,
            default_retry=method_configs['SetLabels'].retry,
            default_timeout=method_configs['SetLabels'].timeout,
            client_info=client_info,
        )
        self._set_legacy_abac = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetLegacyAbac,
            default_retry=method_configs['SetLegacyAbac'].retry,
            default_timeout=method_configs['SetLegacyAbac'].timeout,
            client_info=client_info,
        )
        self._start_i_p_rotation = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.StartIPRotation,
            default_retry=method_configs['StartIPRotation'].retry,
            default_timeout=method_configs['StartIPRotation'].timeout,
            client_info=client_info,
        )
        self._complete_i_p_rotation = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.CompleteIPRotation,
            default_retry=method_configs['CompleteIPRotation'].retry,
            default_timeout=method_configs['CompleteIPRotation'].timeout,
            client_info=client_info,
        )
        self._set_node_pool_size = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetNodePoolSize,
            default_retry=method_configs['SetNodePoolSize'].retry,
            default_timeout=method_configs['SetNodePoolSize'].timeout,
            client_info=client_info,
        )
        self._set_network_policy = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetNetworkPolicy,
            default_retry=method_configs['SetNetworkPolicy'].retry,
            default_timeout=method_configs['SetNetworkPolicy'].timeout,
            client_info=client_info,
        )
        self._set_maintenance_policy = google.api_core.gapic_v1.method.wrap_method(
            self.cluster_manager_stub.SetMaintenancePolicy,
            default_retry=method_configs['SetMaintenancePolicy'].retry,
            default_timeout=method_configs['SetMaintenancePolicy'].timeout,
            client_info=client_info,
        )

    # Service calls
    def list_clusters(self,
                      project_id,
                      zone,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Lists all clusters owned by a project in either the specified zone or all
        zones.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>>
            >>> response = client.list_clusters(project_id, zone)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides, or \"-\" for all zones.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.ListClustersResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.ListClustersRequest(
            project_id=project_id,
            zone=zone,
        )
        return self._list_clusters(request, retry=retry, timeout=timeout)

    def get_cluster(self,
                    project_id,
                    zone,
                    cluster_id,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Gets the details of a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>>
            >>> response = client.get_cluster(project_id, zone, cluster_id)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to retrieve.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Cluster` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.GetClusterRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
        )
        return self._get_cluster(request, retry=retry, timeout=timeout)

    def create_cluster(self,
                       project_id,
                       zone,
                       cluster,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Creates a cluster, consisting of the specified number and type of Google
        Compute Engine instances.

        By default, the cluster is created in the project's
        `default network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`_.

        One firewall is added for the cluster. After cluster creation,
        the cluster creates routes for each node to allow the containers
        on that node to communicate with all other instances in the
        cluster.

        Finally, an entry is added to the project's global metadata indicating
        which CIDR range is being used by the cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster = {}
            >>>
            >>> response = client.create_cluster(project_id, zone, cluster)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster (Union[dict, ~google.cloud.container_v1.types.Cluster]): A [cluster
                resource](/container-engine/reference/rest/v1/projects.zones.clusters)
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.Cluster`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.CreateClusterRequest(
            project_id=project_id,
            zone=zone,
            cluster=cluster,
        )
        return self._create_cluster(request, retry=retry, timeout=timeout)

    def update_cluster(self,
                       project_id,
                       zone,
                       cluster_id,
                       update,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Updates the settings of a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> update = {}
            >>>
            >>> response = client.update_cluster(project_id, zone, cluster_id, update)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to upgrade.
            update (Union[dict, ~google.cloud.container_v1.types.ClusterUpdate]): A description of the update.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.ClusterUpdate`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.UpdateClusterRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            update=update,
        )
        return self._update_cluster(request, retry=retry, timeout=timeout)

    def update_node_pool(self,
                         project_id,
                         zone,
                         cluster_id,
                         node_pool_id,
                         node_version,
                         image_type,
                         retry=google.api_core.gapic_v1.method.DEFAULT,
                         timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Updates the version and/or image type of a specific node pool.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> node_pool_id = ''
            >>> node_version = ''
            >>> image_type = ''
            >>>
            >>> response = client.update_node_pool(project_id, zone, cluster_id, node_pool_id, node_version, image_type)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to upgrade.
            node_pool_id (str): The name of the node pool to upgrade.
            node_version (str): The Kubernetes version to change the nodes to (typically an
                upgrade). Use ``-`` to upgrade to the latest version supported by
                the server.
            image_type (str): The desired image type for the node pool.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.UpdateNodePoolRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            node_version=node_version,
            image_type=image_type,
        )
        return self._update_node_pool(request, retry=retry, timeout=timeout)

    def set_node_pool_autoscaling(
            self,
            project_id,
            zone,
            cluster_id,
            node_pool_id,
            autoscaling,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets the autoscaling settings of a specific node pool.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> node_pool_id = ''
            >>> autoscaling = {}
            >>>
            >>> response = client.set_node_pool_autoscaling(project_id, zone, cluster_id, node_pool_id, autoscaling)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to upgrade.
            node_pool_id (str): The name of the node pool to upgrade.
            autoscaling (Union[dict, ~google.cloud.container_v1.types.NodePoolAutoscaling]): Autoscaling configuration for the node pool.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.NodePoolAutoscaling`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetNodePoolAutoscalingRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            autoscaling=autoscaling,
        )
        return self._set_node_pool_autoscaling(
            request, retry=retry, timeout=timeout)

    def set_logging_service(self,
                            project_id,
                            zone,
                            cluster_id,
                            logging_service,
                            retry=google.api_core.gapic_v1.method.DEFAULT,
                            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets the logging service of a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> logging_service = ''
            >>>
            >>> response = client.set_logging_service(project_id, zone, cluster_id, logging_service)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to upgrade.
            logging_service (str): The logging service the cluster should use to write metrics.
                Currently available options:

                * \"logging.googleapis.com\" - the Google Cloud Logging service
                * \"none\" - no metrics will be exported from the cluster
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetLoggingServiceRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            logging_service=logging_service,
        )
        return self._set_logging_service(request, retry=retry, timeout=timeout)

    def set_monitoring_service(
            self,
            project_id,
            zone,
            cluster_id,
            monitoring_service,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets the monitoring service of a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> monitoring_service = ''
            >>>
            >>> response = client.set_monitoring_service(project_id, zone, cluster_id, monitoring_service)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to upgrade.
            monitoring_service (str): The monitoring service the cluster should use to write metrics.
                Currently available options:

                * \"monitoring.googleapis.com\" - the Google Cloud Monitoring service
                * \"none\" - no metrics will be exported from the cluster
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetMonitoringServiceRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            monitoring_service=monitoring_service,
        )
        return self._set_monitoring_service(
            request, retry=retry, timeout=timeout)

    def set_addons_config(self,
                          project_id,
                          zone,
                          cluster_id,
                          addons_config,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets the addons of a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> addons_config = {}
            >>>
            >>> response = client.set_addons_config(project_id, zone, cluster_id, addons_config)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to upgrade.
            addons_config (Union[dict, ~google.cloud.container_v1.types.AddonsConfig]): The desired configurations for the various addons available to run in the
                cluster.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.AddonsConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetAddonsConfigRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            addons_config=addons_config,
        )
        return self._set_addons_config(request, retry=retry, timeout=timeout)

    def set_locations(self,
                      project_id,
                      zone,
                      cluster_id,
                      locations,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets the locations of a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> locations = []
            >>>
            >>> response = client.set_locations(project_id, zone, cluster_id, locations)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to upgrade.
            locations (list[str]): The desired list of Google Compute Engine
                `locations <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster's nodes
                should be located. Changing the locations a cluster is in will result
                in nodes being either created or removed from the cluster, depending on
                whether locations are being added or removed.

                This list must always include the cluster's primary zone.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetLocationsRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            locations=locations,
        )
        return self._set_locations(request, retry=retry, timeout=timeout)

    def update_master(self,
                      project_id,
                      zone,
                      cluster_id,
                      master_version,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Updates the master of a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> master_version = ''
            >>>
            >>> response = client.update_master(project_id, zone, cluster_id, master_version)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to upgrade.
            master_version (str): The Kubernetes version to change the master to. The only valid value is the
                latest supported version. Use \"-\" to have the server automatically select
                the latest version.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.UpdateMasterRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            master_version=master_version,
        )
        return self._update_master(request, retry=retry, timeout=timeout)

    def set_master_auth(self,
                        project_id,
                        zone,
                        cluster_id,
                        action,
                        update,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Used to set master auth materials. Currently supports :-
        Changing the admin password of a specific cluster.
        This can be either via password generation or explicitly set the password.

        Example:
            >>> from google.cloud import container_v1
            >>> from google.cloud.container_v1 import enums
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> action = enums.SetMasterAuthRequest.Action.UNKNOWN
            >>> update = {}
            >>>
            >>> response = client.set_master_auth(project_id, zone, cluster_id, action, update)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to upgrade.
            action (~google.cloud.container_v1.types.Action): The exact form of action to be taken on the master auth.
            update (Union[dict, ~google.cloud.container_v1.types.MasterAuth]): A description of the update.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.MasterAuth`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetMasterAuthRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            action=action,
            update=update,
        )
        return self._set_master_auth(request, retry=retry, timeout=timeout)

    def delete_cluster(self,
                       project_id,
                       zone,
                       cluster_id,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Deletes the cluster, including the Kubernetes endpoint and all worker
        nodes.

        Firewalls and routes that were configured during cluster creation
        are also deleted.

        Other Google Compute Engine resources that might be in use by the cluster
        (e.g. load balancer resources) will not be deleted if they weren't present
        at the initial create time.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>>
            >>> response = client.delete_cluster(project_id, zone, cluster_id)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to delete.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.DeleteClusterRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
        )
        return self._delete_cluster(request, retry=retry, timeout=timeout)

    def list_operations(self,
                        project_id,
                        zone,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Lists all operations in a project in a specific zone or all zones.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>>
            >>> response = client.list_operations(project_id, zone)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine `zone <https://cloud.google.com/compute/docs/zones#available>`_
                to return operations for, or ``-`` for all zones.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.ListOperationsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.ListOperationsRequest(
            project_id=project_id,
            zone=zone,
        )
        return self._list_operations(request, retry=retry, timeout=timeout)

    def get_operation(self,
                      project_id,
                      zone,
                      operation_id,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Gets the specified operation.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> operation_id = ''
            >>>
            >>> response = client.get_operation(project_id, zone, operation_id)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            operation_id (str): The server-assigned ``name`` of the operation.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.GetOperationRequest(
            project_id=project_id,
            zone=zone,
            operation_id=operation_id,
        )
        return self._get_operation(request, retry=retry, timeout=timeout)

    def cancel_operation(self,
                         project_id,
                         zone,
                         operation_id,
                         retry=google.api_core.gapic_v1.method.DEFAULT,
                         timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Cancels the specified operation.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> operation_id = ''
            >>>
            >>> client.cancel_operation(project_id, zone, operation_id)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the operation resides.
            operation_id (str): The server-assigned ``name`` of the operation.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.CancelOperationRequest(
            project_id=project_id,
            zone=zone,
            operation_id=operation_id,
        )
        self._cancel_operation(request, retry=retry, timeout=timeout)

    def get_server_config(self,
                          project_id,
                          zone,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Returns configuration info about the Container Engine service.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>>
            >>> response = client.get_server_config(project_id, zone)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine `zone <https://cloud.google.com/compute/docs/zones#available>`_
                to return operations for.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.ServerConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.GetServerConfigRequest(
            project_id=project_id,
            zone=zone,
        )
        return self._get_server_config(request, retry=retry, timeout=timeout)

    def list_node_pools(self,
                        project_id,
                        zone,
                        cluster_id,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Lists the node pools for a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>>
            >>> response = client.list_node_pools(project_id, zone, cluster_id)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://developers.google.com/console/help/new/#projectnumber).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.ListNodePoolsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.ListNodePoolsRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
        )
        return self._list_node_pools(request, retry=retry, timeout=timeout)

    def get_node_pool(self,
                      project_id,
                      zone,
                      cluster_id,
                      node_pool_id,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Retrieves the node pool requested.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> node_pool_id = ''
            >>>
            >>> response = client.get_node_pool(project_id, zone, cluster_id, node_pool_id)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://developers.google.com/console/help/new/#projectnumber).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster.
            node_pool_id (str): The name of the node pool.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.NodePool` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.GetNodePoolRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
        )
        return self._get_node_pool(request, retry=retry, timeout=timeout)

    def create_node_pool(self,
                         project_id,
                         zone,
                         cluster_id,
                         node_pool,
                         retry=google.api_core.gapic_v1.method.DEFAULT,
                         timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Creates a node pool for a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> node_pool = {}
            >>>
            >>> response = client.create_node_pool(project_id, zone, cluster_id, node_pool)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://developers.google.com/console/help/new/#projectnumber).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster.
            node_pool (Union[dict, ~google.cloud.container_v1.types.NodePool]): The node pool to create.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.NodePool`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.CreateNodePoolRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool=node_pool,
        )
        return self._create_node_pool(request, retry=retry, timeout=timeout)

    def delete_node_pool(self,
                         project_id,
                         zone,
                         cluster_id,
                         node_pool_id,
                         retry=google.api_core.gapic_v1.method.DEFAULT,
                         timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Deletes a node pool from a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> node_pool_id = ''
            >>>
            >>> response = client.delete_node_pool(project_id, zone, cluster_id, node_pool_id)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://developers.google.com/console/help/new/#projectnumber).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster.
            node_pool_id (str): The name of the node pool to delete.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.DeleteNodePoolRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
        )
        return self._delete_node_pool(request, retry=retry, timeout=timeout)

    def rollback_node_pool_upgrade(
            self,
            project_id,
            zone,
            cluster_id,
            node_pool_id,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Roll back the previously Aborted or Failed NodePool upgrade.
        This will be an no-op if the last upgrade successfully completed.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> node_pool_id = ''
            >>>
            >>> response = client.rollback_node_pool_upgrade(project_id, zone, cluster_id, node_pool_id)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to rollback.
            node_pool_id (str): The name of the node pool to rollback.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.RollbackNodePoolUpgradeRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
        )
        return self._rollback_node_pool_upgrade(
            request, retry=retry, timeout=timeout)

    def set_node_pool_management(
            self,
            project_id,
            zone,
            cluster_id,
            node_pool_id,
            management,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets the NodeManagement options for a node pool.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> node_pool_id = ''
            >>> management = {}
            >>>
            >>> response = client.set_node_pool_management(project_id, zone, cluster_id, node_pool_id, management)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to update.
            node_pool_id (str): The name of the node pool to update.
            management (Union[dict, ~google.cloud.container_v1.types.NodeManagement]): NodeManagement configuration for the node pool.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.NodeManagement`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetNodePoolManagementRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            management=management,
        )
        return self._set_node_pool_management(
            request, retry=retry, timeout=timeout)

    def set_labels(self,
                   project_id,
                   zone,
                   cluster_id,
                   resource_labels,
                   label_fingerprint,
                   retry=google.api_core.gapic_v1.method.DEFAULT,
                   timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets labels on a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> resource_labels = {}
            >>> label_fingerprint = ''
            >>>
            >>> response = client.set_labels(project_id, zone, cluster_id, resource_labels, label_fingerprint)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://developers.google.com/console/help/new/#projectnumber).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster.
            resource_labels (dict[str -> str]): The labels to set for that cluster.
            label_fingerprint (str): The fingerprint of the previous set of labels for this resource,
                used to detect conflicts. The fingerprint is initially generated by
                Container Engine and changes after every request to modify or update
                labels. You must always provide an up-to-date fingerprint hash when
                updating or changing labels. Make a <code>get()</code> request to the
                resource to get the latest fingerprint.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetLabelsRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            resource_labels=resource_labels,
            label_fingerprint=label_fingerprint,
        )
        return self._set_labels(request, retry=retry, timeout=timeout)

    def set_legacy_abac(self,
                        project_id,
                        zone,
                        cluster_id,
                        enabled,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Enables or disables the ABAC authorization mechanism on a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> enabled = False
            >>>
            >>> response = client.set_legacy_abac(project_id, zone, cluster_id, enabled)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to update.
            enabled (bool): Whether ABAC authorization will be enabled in the cluster.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetLegacyAbacRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            enabled=enabled,
        )
        return self._set_legacy_abac(request, retry=retry, timeout=timeout)

    def start_i_p_rotation(self,
                           project_id,
                           zone,
                           cluster_id,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Start master IP rotation.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>>
            >>> response = client.start_i_p_rotation(project_id, zone, cluster_id)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://developers.google.com/console/help/new/#projectnumber).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.StartIPRotationRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
        )
        return self._start_i_p_rotation(request, retry=retry, timeout=timeout)

    def complete_i_p_rotation(self,
                              project_id,
                              zone,
                              cluster_id,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Completes master IP rotation.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>>
            >>> response = client.complete_i_p_rotation(project_id, zone, cluster_id)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://developers.google.com/console/help/new/#projectnumber).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.CompleteIPRotationRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
        )
        return self._complete_i_p_rotation(
            request, retry=retry, timeout=timeout)

    def set_node_pool_size(self,
                           project_id,
                           zone,
                           cluster_id,
                           node_pool_id,
                           node_count,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets the size of a specific node pool.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> node_pool_id = ''
            >>> node_count = 0
            >>>
            >>> response = client.set_node_pool_size(project_id, zone, cluster_id, node_pool_id, node_count)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to update.
            node_pool_id (str): The name of the node pool to update.
            node_count (int): The desired node count for the pool.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetNodePoolSizeRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            node_count=node_count,
        )
        return self._set_node_pool_size(request, retry=retry, timeout=timeout)

    def set_network_policy(self,
                           project_id,
                           zone,
                           cluster_id,
                           network_policy,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Enables/Disables Network Policy for a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> network_policy = {}
            >>>
            >>> response = client.set_network_policy(project_id, zone, cluster_id, network_policy)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://developers.google.com/console/help/new/#projectnumber).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster.
            network_policy (Union[dict, ~google.cloud.container_v1.types.NetworkPolicy]): Configuration options for the NetworkPolicy feature.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.NetworkPolicy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetNetworkPolicyRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            network_policy=network_policy,
        )
        return self._set_network_policy(request, retry=retry, timeout=timeout)

    def set_maintenance_policy(
            self,
            project_id,
            zone,
            cluster_id,
            maintenance_policy,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets the maintenance policy for a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> project_id = ''
            >>> zone = ''
            >>> cluster_id = ''
            >>> maintenance_policy = {}
            >>>
            >>> response = client.set_maintenance_policy(project_id, zone, cluster_id, maintenance_policy)

        Args:
            project_id (str): The Google Developers Console [project ID or project
                number](https://support.google.com/cloud/answer/6158840).
            zone (str): The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`_ in which the cluster
                resides.
            cluster_id (str): The name of the cluster to update.
            maintenance_policy (Union[dict, ~google.cloud.container_v1.types.MaintenancePolicy]): The maintenance policy to be set for the cluster. An empty field
                clears the existing maintenance policy.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.MaintenancePolicy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = cluster_service_pb2.SetMaintenancePolicyRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            maintenance_policy=maintenance_policy,
        )
        return self._set_maintenance_policy(
            request, retry=retry, timeout=timeout)
