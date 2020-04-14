# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

"""Accesses the google.container.v1 ClusterManager API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import grpc

from google.cloud.container_v1.gapic import cluster_manager_client_config
from google.cloud.container_v1.gapic import enums
from google.cloud.container_v1.gapic.transports import cluster_manager_grpc_transport
from google.cloud.container_v1.proto import cluster_service_pb2
from google.cloud.container_v1.proto import cluster_service_pb2_grpc
from google.protobuf import empty_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-container"
).version


class ClusterManagerClient(object):
    """Google Kubernetes Engine Cluster Manager v1"""

    SERVICE_ADDRESS = "container.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.container.v1.ClusterManager"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ClusterManagerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.ClusterManagerGrpcTransport,
                    Callable[[~.Credentials, type], ~.ClusterManagerGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = cluster_manager_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=cluster_manager_grpc_transport.ClusterManagerGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = cluster_manager_grpc_transport.ClusterManagerGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def list_clusters(
        self,
        project_id=None,
        zone=None,
        parent=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all clusters owned by a project in either the specified zone or all
        zones.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.list_clusters()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the parent field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides, or "-" for all zones. This field has been
                deprecated and replaced by the parent field.
            parent (str): The parent (project and location) where the clusters will be listed.
                Specified in the format ``projects/*/locations/*``. Location "-" matches
                all zones and all regions.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.ListClustersResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_clusters" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_clusters"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_clusters,
                default_retry=self._method_configs["ListClusters"].retry,
                default_timeout=self._method_configs["ListClusters"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.ListClustersRequest(
            project_id=project_id, zone=zone, parent=parent
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["list_clusters"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_cluster(
        self,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the details of a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.get_cluster()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to retrieve.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster) of the cluster to retrieve.
                Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Cluster` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_cluster" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_cluster"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_cluster,
                default_retry=self._method_configs["GetCluster"].retry,
                default_timeout=self._method_configs["GetCluster"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.GetClusterRequest(
            project_id=project_id, zone=zone, cluster_id=cluster_id, name=name
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_cluster(
        self,
        cluster,
        project_id=None,
        zone=None,
        parent=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a cluster, consisting of the specified number and type of Google
        Compute Engine instances.

        By default, the cluster is created in the project's `default
        network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__.

        One firewall is added for the cluster. After cluster creation, the
        Kubelet creates routes for each node to allow the containers on that
        node to communicate with all other instances in the cluster.

        Finally, an entry is added to the project's global metadata indicating
        which CIDR range the cluster is using.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `cluster`:
            >>> cluster = {}
            >>>
            >>> response = client.create_cluster(cluster)

        Args:
            cluster (Union[dict, ~google.cloud.container_v1.types.Cluster]): Required. A `cluster
                resource <https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters>`__

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.Cluster`
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the parent field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the parent field.
            parent (str): The parent (project and location) where the cluster will be created.
                Specified in the format ``projects/*/locations/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_cluster" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_cluster"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_cluster,
                default_retry=self._method_configs["CreateCluster"].retry,
                default_timeout=self._method_configs["CreateCluster"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.CreateClusterRequest(
            cluster=cluster, project_id=project_id, zone=zone, parent=parent
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_cluster(
        self,
        update,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates the settings of a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `update`:
            >>> update = {}
            >>>
            >>> response = client.update_cluster(update)

        Args:
            update (Union[dict, ~google.cloud.container_v1.types.ClusterUpdate]): Required. A description of the update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.ClusterUpdate`
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to upgrade.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster) of the cluster to update.
                Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_cluster" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_cluster"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_cluster,
                default_retry=self._method_configs["UpdateCluster"].retry,
                default_timeout=self._method_configs["UpdateCluster"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.UpdateClusterRequest(
            update=update,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_node_pool(
        self,
        node_version,
        image_type,
        project_id=None,
        zone=None,
        cluster_id=None,
        node_pool_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates the version and/or image type for the specified node pool.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `node_version`:
            >>> node_version = ''
            >>>
            >>> # TODO: Initialize `image_type`:
            >>> image_type = ''
            >>>
            >>> response = client.update_node_pool(node_version, image_type)

        Args:
            node_version (str): Required. The Kubernetes version to change the nodes to (typically an
                upgrade).

                Users may specify either explicit versions offered by Kubernetes Engine or
                version aliases, which have the following behavior:

                - "latest": picks the highest valid Kubernetes version
                - "1.X": picks the highest valid patch+gke.N patch in the 1.X version
                - "1.X.Y": picks the highest valid gke.N patch in the 1.X.Y version
                - "1.X.Y-gke.N": picks an explicit Kubernetes version
                - "-": picks the Kubernetes master version
            image_type (str): Required. The desired image type for the node pool.
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to upgrade.
                This field has been deprecated and replaced by the name field.
            node_pool_id (str): Deprecated. The name of the node pool to upgrade.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster, node pool) of the node pool to
                update. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_node_pool" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_node_pool"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_node_pool,
                default_retry=self._method_configs["UpdateNodePool"].retry,
                default_timeout=self._method_configs["UpdateNodePool"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.UpdateNodePoolRequest(
            node_version=node_version,
            image_type=image_type,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_node_pool"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_node_pool_autoscaling(
        self,
        autoscaling,
        project_id=None,
        zone=None,
        cluster_id=None,
        node_pool_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the autoscaling settings for the specified node pool.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `autoscaling`:
            >>> autoscaling = {}
            >>>
            >>> response = client.set_node_pool_autoscaling(autoscaling)

        Args:
            autoscaling (Union[dict, ~google.cloud.container_v1.types.NodePoolAutoscaling]): Required. Autoscaling configuration for the node pool.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.NodePoolAutoscaling`
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to upgrade.
                This field has been deprecated and replaced by the name field.
            node_pool_id (str): Deprecated. The name of the node pool to upgrade.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster, node pool) of the node pool to set
                autoscaler settings. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_node_pool_autoscaling" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_node_pool_autoscaling"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_node_pool_autoscaling,
                default_retry=self._method_configs["SetNodePoolAutoscaling"].retry,
                default_timeout=self._method_configs["SetNodePoolAutoscaling"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetNodePoolAutoscalingRequest(
            autoscaling=autoscaling,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_node_pool_autoscaling"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_logging_service(
        self,
        logging_service,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the logging service for a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `logging_service`:
            >>> logging_service = ''
            >>>
            >>> response = client.set_logging_service(logging_service)

        Args:
            logging_service (str): Required. The logging service the cluster should use to write metrics.
                Currently available options:

                -  "logging.googleapis.com" - the Google Cloud Logging service
                -  "none" - no metrics will be exported from the cluster
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to upgrade.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster) of the cluster to set logging.
                Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_logging_service" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_logging_service"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_logging_service,
                default_retry=self._method_configs["SetLoggingService"].retry,
                default_timeout=self._method_configs["SetLoggingService"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetLoggingServiceRequest(
            logging_service=logging_service,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_logging_service"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_monitoring_service(
        self,
        monitoring_service,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the monitoring service for a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `monitoring_service`:
            >>> monitoring_service = ''
            >>>
            >>> response = client.set_monitoring_service(monitoring_service)

        Args:
            monitoring_service (str): Required. The monitoring service the cluster should use to write
                metrics. Currently available options:

                -  "monitoring.googleapis.com/kubernetes" - the Google Cloud Monitoring
                   service with Kubernetes-native resource model
                -  "monitoring.googleapis.com" - the Google Cloud Monitoring service
                -  "none" - no metrics will be exported from the cluster
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to upgrade.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster) of the cluster to set monitoring.
                Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_monitoring_service" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_monitoring_service"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_monitoring_service,
                default_retry=self._method_configs["SetMonitoringService"].retry,
                default_timeout=self._method_configs["SetMonitoringService"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetMonitoringServiceRequest(
            monitoring_service=monitoring_service,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_monitoring_service"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_addons_config(
        self,
        addons_config,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the addons for a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `addons_config`:
            >>> addons_config = {}
            >>>
            >>> response = client.set_addons_config(addons_config)

        Args:
            addons_config (Union[dict, ~google.cloud.container_v1.types.AddonsConfig]): Required. The desired configurations for the various addons available to run in the
                cluster.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.AddonsConfig`
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to upgrade.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster) of the cluster to set addons.
                Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_addons_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_addons_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_addons_config,
                default_retry=self._method_configs["SetAddonsConfig"].retry,
                default_timeout=self._method_configs["SetAddonsConfig"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetAddonsConfigRequest(
            addons_config=addons_config,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_addons_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_locations(
        self,
        locations,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the locations for a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `locations`:
            >>> locations = []
            >>>
            >>> response = client.set_locations(locations)

        Args:
            locations (list[str]): Required. The desired list of Google Compute Engine
                `zones <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster's nodes should be located. Changing the locations a
                cluster is in will result in nodes being either created or removed from
                the cluster, depending on whether locations are being added or removed.

                This list must always include the cluster's primary zone.
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to upgrade.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster) of the cluster to set locations.
                Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_locations" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_locations"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_locations,
                default_retry=self._method_configs["SetLocations"].retry,
                default_timeout=self._method_configs["SetLocations"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetLocationsRequest(
            locations=locations,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_locations"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_master(
        self,
        master_version,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates the master for a specific cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `master_version`:
            >>> master_version = ''
            >>>
            >>> response = client.update_master(master_version)

        Args:
            master_version (str): Required. The Kubernetes version to change the master to.

                Users may specify either explicit versions offered by Kubernetes Engine or
                version aliases, which have the following behavior:

                - "latest": picks the highest valid Kubernetes version
                - "1.X": picks the highest valid patch+gke.N patch in the 1.X version
                - "1.X.Y": picks the highest valid gke.N patch in the 1.X.Y version
                - "1.X.Y-gke.N": picks an explicit Kubernetes version
                - "-": picks the default Kubernetes version
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to upgrade.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster) of the cluster to update.
                Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_master" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_master"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_master,
                default_retry=self._method_configs["UpdateMaster"].retry,
                default_timeout=self._method_configs["UpdateMaster"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.UpdateMasterRequest(
            master_version=master_version,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_master"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_master_auth(
        self,
        action,
        update,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets master auth materials. Currently supports changing the admin password
        or a specific cluster, either via password generation or explicitly setting
        the password.

        Example:
            >>> from google.cloud import container_v1
            >>> from google.cloud.container_v1 import enums
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `action`:
            >>> action = enums.SetMasterAuthRequest.Action.UNKNOWN
            >>>
            >>> # TODO: Initialize `update`:
            >>> update = {}
            >>>
            >>> response = client.set_master_auth(action, update)

        Args:
            action (~google.cloud.container_v1.types.Action): Required. The exact form of action to be taken on the master auth.
            update (Union[dict, ~google.cloud.container_v1.types.MasterAuth]): Required. A description of the update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.MasterAuth`
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to upgrade.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster) of the cluster to set auth.
                Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_master_auth" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_master_auth"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_master_auth,
                default_retry=self._method_configs["SetMasterAuth"].retry,
                default_timeout=self._method_configs["SetMasterAuth"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetMasterAuthRequest(
            action=action,
            update=update,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_master_auth"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_cluster(
        self,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the cluster, including the Kubernetes endpoint and all worker
        nodes.

        Firewalls and routes that were configured during cluster creation
        are also deleted.

        Other Google Compute Engine resources that might be in use by the cluster,
        such as load balancer resources, are not deleted if they weren't present
        when the cluster was initially created.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.delete_cluster()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to delete.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster) of the cluster to delete.
                Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_cluster" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_cluster"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_cluster,
                default_retry=self._method_configs["DeleteCluster"].retry,
                default_timeout=self._method_configs["DeleteCluster"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.DeleteClusterRequest(
            project_id=project_id, zone=zone, cluster_id=cluster_id, name=name
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["delete_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_operations(
        self,
        project_id=None,
        zone=None,
        parent=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all operations in a project in a specific zone or all zones.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.list_operations()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the parent field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ to
                return operations for, or ``-`` for all zones. This field has been
                deprecated and replaced by the parent field.
            parent (str): The parent (project and location) where the operations will be listed.
                Specified in the format ``projects/*/locations/*``. Location "-" matches
                all zones and all regions.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.ListOperationsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_operations" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_operations"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_operations,
                default_retry=self._method_configs["ListOperations"].retry,
                default_timeout=self._method_configs["ListOperations"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.ListOperationsRequest(
            project_id=project_id, zone=zone, parent=parent
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["list_operations"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_operation(
        self,
        project_id=None,
        zone=None,
        operation_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the specified operation.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.get_operation()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            operation_id (str): Deprecated. The server-assigned ``name`` of the operation. This field
                has been deprecated and replaced by the name field.
            name (str): The name (project, location, operation id) of the operation to get.
                Specified in the format ``projects/*/locations/*/operations/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_operation" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_operation"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_operation,
                default_retry=self._method_configs["GetOperation"].retry,
                default_timeout=self._method_configs["GetOperation"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.GetOperationRequest(
            project_id=project_id, zone=zone, operation_id=operation_id, name=name
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_operation"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def cancel_operation(
        self,
        project_id=None,
        zone=None,
        operation_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Cancels the specified operation.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> client.cancel_operation()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the operation resides. This field has been deprecated and replaced
                by the name field.
            operation_id (str): Deprecated. The server-assigned ``name`` of the operation. This field
                has been deprecated and replaced by the name field.
            name (str): The name (project, location, operation id) of the operation to cancel.
                Specified in the format ``projects/*/locations/*/operations/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "cancel_operation" not in self._inner_api_calls:
            self._inner_api_calls[
                "cancel_operation"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.cancel_operation,
                default_retry=self._method_configs["CancelOperation"].retry,
                default_timeout=self._method_configs["CancelOperation"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.CancelOperationRequest(
            project_id=project_id, zone=zone, operation_id=operation_id, name=name
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["cancel_operation"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_server_config(
        self,
        project_id=None,
        zone=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns configuration info about the Google Kubernetes Engine service.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.get_server_config()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ to
                return operations for. This field has been deprecated and replaced by
                the name field.
            name (str): The name (project and location) of the server config to get, specified
                in the format ``projects/*/locations/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.ServerConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_server_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_server_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_server_config,
                default_retry=self._method_configs["GetServerConfig"].retry,
                default_timeout=self._method_configs["GetServerConfig"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.GetServerConfigRequest(
            project_id=project_id, zone=zone, name=name
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_server_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_node_pools(
        self,
        project_id=None,
        zone=None,
        cluster_id=None,
        parent=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the node pools for a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.list_node_pools()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the parent field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the parent field.
            cluster_id (str): Deprecated. The name of the cluster.
                This field has been deprecated and replaced by the parent field.
            parent (str): The parent (project, location, cluster id) where the node pools will be
                listed. Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.ListNodePoolsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_node_pools" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_node_pools"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_node_pools,
                default_retry=self._method_configs["ListNodePools"].retry,
                default_timeout=self._method_configs["ListNodePools"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.ListNodePoolsRequest(
            project_id=project_id, zone=zone, cluster_id=cluster_id, parent=parent
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["list_node_pools"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_node_pool(
        self,
        project_id=None,
        zone=None,
        cluster_id=None,
        node_pool_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Retrieves the requested node pool.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.get_node_pool()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster.
                This field has been deprecated and replaced by the name field.
            node_pool_id (str): Deprecated. The name of the node pool.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster, node pool id) of the node pool to
                get. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.NodePool` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_node_pool" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_node_pool"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_node_pool,
                default_retry=self._method_configs["GetNodePool"].retry,
                default_timeout=self._method_configs["GetNodePool"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.GetNodePoolRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_node_pool"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_node_pool(
        self,
        node_pool,
        project_id=None,
        zone=None,
        cluster_id=None,
        parent=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a node pool for a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `node_pool`:
            >>> node_pool = {}
            >>>
            >>> response = client.create_node_pool(node_pool)

        Args:
            node_pool (Union[dict, ~google.cloud.container_v1.types.NodePool]): Required. The node pool to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.NodePool`
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the parent field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the parent field.
            cluster_id (str): Deprecated. The name of the cluster.
                This field has been deprecated and replaced by the parent field.
            parent (str): The parent (project, location, cluster id) where the node pool will be
                created. Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_node_pool" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_node_pool"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_node_pool,
                default_retry=self._method_configs["CreateNodePool"].retry,
                default_timeout=self._method_configs["CreateNodePool"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.CreateNodePoolRequest(
            node_pool=node_pool,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            parent=parent,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_node_pool"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_node_pool(
        self,
        project_id=None,
        zone=None,
        cluster_id=None,
        node_pool_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a node pool from a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.delete_node_pool()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster.
                This field has been deprecated and replaced by the name field.
            node_pool_id (str): Deprecated. The name of the node pool to delete.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster, node pool id) of the node pool to
                delete. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_node_pool" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_node_pool"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_node_pool,
                default_retry=self._method_configs["DeleteNodePool"].retry,
                default_timeout=self._method_configs["DeleteNodePool"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.DeleteNodePoolRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["delete_node_pool"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def rollback_node_pool_upgrade(
        self,
        project_id=None,
        zone=None,
        cluster_id=None,
        node_pool_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Rolls back a previously Aborted or Failed NodePool upgrade.
        This makes no changes if the last upgrade successfully completed.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.rollback_node_pool_upgrade()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to rollback.
                This field has been deprecated and replaced by the name field.
            node_pool_id (str): Deprecated. The name of the node pool to rollback.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster, node pool id) of the node poll to
                rollback upgrade. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "rollback_node_pool_upgrade" not in self._inner_api_calls:
            self._inner_api_calls[
                "rollback_node_pool_upgrade"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.rollback_node_pool_upgrade,
                default_retry=self._method_configs["RollbackNodePoolUpgrade"].retry,
                default_timeout=self._method_configs["RollbackNodePoolUpgrade"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.RollbackNodePoolUpgradeRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["rollback_node_pool_upgrade"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_node_pool_management(
        self,
        management,
        project_id=None,
        zone=None,
        cluster_id=None,
        node_pool_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the NodeManagement options for a node pool.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `management`:
            >>> management = {}
            >>>
            >>> response = client.set_node_pool_management(management)

        Args:
            management (Union[dict, ~google.cloud.container_v1.types.NodeManagement]): Required. NodeManagement configuration for the node pool.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.NodeManagement`
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to update.
                This field has been deprecated and replaced by the name field.
            node_pool_id (str): Deprecated. The name of the node pool to update.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster, node pool id) of the node pool to
                set management properties. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_node_pool_management" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_node_pool_management"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_node_pool_management,
                default_retry=self._method_configs["SetNodePoolManagement"].retry,
                default_timeout=self._method_configs["SetNodePoolManagement"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetNodePoolManagementRequest(
            management=management,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_node_pool_management"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_labels(
        self,
        resource_labels,
        label_fingerprint,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets labels on a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `resource_labels`:
            >>> resource_labels = {}
            >>>
            >>> # TODO: Initialize `label_fingerprint`:
            >>> label_fingerprint = ''
            >>>
            >>> response = client.set_labels(resource_labels, label_fingerprint)

        Args:
            resource_labels (dict[str -> str]): Required. The labels to set for that cluster.
            label_fingerprint (str): Required. The fingerprint of the previous set of labels for this resource,
                used to detect conflicts. The fingerprint is initially generated by
                Kubernetes Engine and changes after every request to modify or update
                labels. You must always provide an up-to-date fingerprint hash when
                updating or changing labels. Make a <code>get()</code> request to the
                resource to get the latest fingerprint.
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster id) of the cluster to set labels.
                Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_labels" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_labels"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_labels,
                default_retry=self._method_configs["SetLabels"].retry,
                default_timeout=self._method_configs["SetLabels"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetLabelsRequest(
            resource_labels=resource_labels,
            label_fingerprint=label_fingerprint,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_labels"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_legacy_abac(
        self,
        enabled,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Enables or disables the ABAC authorization mechanism on a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `enabled`:
            >>> enabled = False
            >>>
            >>> response = client.set_legacy_abac(enabled)

        Args:
            enabled (bool): Required. Whether ABAC authorization will be enabled in the cluster.
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to update.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster id) of the cluster to set legacy
                abac. Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_legacy_abac" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_legacy_abac"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_legacy_abac,
                default_retry=self._method_configs["SetLegacyAbac"].retry,
                default_timeout=self._method_configs["SetLegacyAbac"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetLegacyAbacRequest(
            enabled=enabled,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_legacy_abac"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def start_i_p_rotation(
        self,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        rotate_credentials=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Starts master IP rotation.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.start_i_p_rotation()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster id) of the cluster to start IP
                rotation. Specified in the format ``projects/*/locations/*/clusters/*``.
            rotate_credentials (bool): Whether to rotate credentials during IP rotation.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "start_i_p_rotation" not in self._inner_api_calls:
            self._inner_api_calls[
                "start_i_p_rotation"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.start_i_p_rotation,
                default_retry=self._method_configs["StartIPRotation"].retry,
                default_timeout=self._method_configs["StartIPRotation"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.StartIPRotationRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
            rotate_credentials=rotate_credentials,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["start_i_p_rotation"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def complete_i_p_rotation(
        self,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Completes master IP rotation.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> response = client.complete_i_p_rotation()

        Args:
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster id) of the cluster to complete IP
                rotation. Specified in the format ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "complete_i_p_rotation" not in self._inner_api_calls:
            self._inner_api_calls[
                "complete_i_p_rotation"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.complete_i_p_rotation,
                default_retry=self._method_configs["CompleteIPRotation"].retry,
                default_timeout=self._method_configs["CompleteIPRotation"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.CompleteIPRotationRequest(
            project_id=project_id, zone=zone, cluster_id=cluster_id, name=name
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["complete_i_p_rotation"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_node_pool_size(
        self,
        node_count,
        project_id=None,
        zone=None,
        cluster_id=None,
        node_pool_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the size for a specific node pool.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `node_count`:
            >>> node_count = 0
            >>>
            >>> response = client.set_node_pool_size(node_count)

        Args:
            node_count (int): Required. The desired node count for the pool.
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__. This field
                has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster to update.
                This field has been deprecated and replaced by the name field.
            node_pool_id (str): Deprecated. The name of the node pool to update.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster, node pool id) of the node pool to
                set size. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_node_pool_size" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_node_pool_size"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_node_pool_size,
                default_retry=self._method_configs["SetNodePoolSize"].retry,
                default_timeout=self._method_configs["SetNodePoolSize"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetNodePoolSizeRequest(
            node_count=node_count,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            node_pool_id=node_pool_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_node_pool_size"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_network_policy(
        self,
        network_policy,
        project_id=None,
        zone=None,
        cluster_id=None,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Enables or disables Network Policy for a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `network_policy`:
            >>> network_policy = {}
            >>>
            >>> response = client.set_network_policy(network_policy)

        Args:
            network_policy (Union[dict, ~google.cloud.container_v1.types.NetworkPolicy]): Required. Configuration options for the NetworkPolicy feature.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.NetworkPolicy`
            project_id (str): Deprecated. The Google Developers Console `project ID or project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name field.
            zone (str): Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides. This field has been deprecated and replaced
                by the name field.
            cluster_id (str): Deprecated. The name of the cluster.
                This field has been deprecated and replaced by the name field.
            name (str): The name (project, location, cluster id) of the cluster to set
                networking policy. Specified in the format
                ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_network_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_network_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_network_policy,
                default_retry=self._method_configs["SetNetworkPolicy"].retry,
                default_timeout=self._method_configs["SetNetworkPolicy"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetNetworkPolicyRequest(
            network_policy=network_policy,
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_network_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_maintenance_policy(
        self,
        project_id,
        zone,
        cluster_id,
        maintenance_policy,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the maintenance policy for a cluster.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `zone`:
            >>> zone = ''
            >>>
            >>> # TODO: Initialize `cluster_id`:
            >>> cluster_id = ''
            >>>
            >>> # TODO: Initialize `maintenance_policy`:
            >>> maintenance_policy = {}
            >>>
            >>> response = client.set_maintenance_policy(project_id, zone, cluster_id, maintenance_policy)

        Args:
            project_id (str): Required. The Google Developers Console `project ID or project
                number <https://support.google.com/cloud/answer/6158840>`__.
            zone (str): Required. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__ in
                which the cluster resides.
            cluster_id (str): Required. The name of the cluster to update.
            maintenance_policy (Union[dict, ~google.cloud.container_v1.types.MaintenancePolicy]): Required. The maintenance policy to be set for the cluster. An empty field
                clears the existing maintenance policy.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.container_v1.types.MaintenancePolicy`
            name (str): The name (project, location, cluster id) of the cluster to set
                maintenance policy. Specified in the format
                ``projects/*/locations/*/clusters/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.container_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_maintenance_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_maintenance_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_maintenance_policy,
                default_retry=self._method_configs["SetMaintenancePolicy"].retry,
                default_timeout=self._method_configs["SetMaintenancePolicy"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.SetMaintenancePolicyRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_id,
            maintenance_policy=maintenance_policy,
            name=name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_maintenance_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_usable_subnetworks(
        self,
        parent=None,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists subnetworks that are usable for creating clusters in a project.

        Example:
            >>> from google.cloud import container_v1
            >>>
            >>> client = container_v1.ClusterManagerClient()
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_usable_subnetworks():
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_usable_subnetworks().pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The parent project where subnetworks are usable. Specified in the format
                ``projects/*``.
            filter_ (str): Filtering currently only supports equality on the networkProjectId and
                must be in the form: "networkProjectId=[PROJECTID]", where
                ``networkProjectId`` is the project which owns the listed subnetworks.
                This defaults to the parent project ID.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.container_v1.types.UsableSubnetwork` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_usable_subnetworks" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_usable_subnetworks"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_usable_subnetworks,
                default_retry=self._method_configs["ListUsableSubnetworks"].retry,
                default_timeout=self._method_configs["ListUsableSubnetworks"].timeout,
                client_info=self._client_info,
            )

        request = cluster_service_pb2.ListUsableSubnetworksRequest(
            parent=parent, filter=filter_, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_usable_subnetworks"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="subnetworks",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator
