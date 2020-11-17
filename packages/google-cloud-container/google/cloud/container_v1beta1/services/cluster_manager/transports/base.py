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
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.container_v1beta1.types import cluster_service
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-container",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


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
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
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
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.
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
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_clusters: gapic_v1.method.wrap_method(
                self.list_clusters,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.get_cluster: gapic_v1.method.wrap_method(
                self.get_cluster,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.create_cluster: gapic_v1.method.wrap_method(
                self.create_cluster, default_timeout=45.0, client_info=client_info,
            ),
            self.update_cluster: gapic_v1.method.wrap_method(
                self.update_cluster, default_timeout=45.0, client_info=client_info,
            ),
            self.update_node_pool: gapic_v1.method.wrap_method(
                self.update_node_pool, default_timeout=45.0, client_info=client_info,
            ),
            self.set_node_pool_autoscaling: gapic_v1.method.wrap_method(
                self.set_node_pool_autoscaling,
                default_timeout=45.0,
                client_info=client_info,
            ),
            self.set_logging_service: gapic_v1.method.wrap_method(
                self.set_logging_service, default_timeout=45.0, client_info=client_info,
            ),
            self.set_monitoring_service: gapic_v1.method.wrap_method(
                self.set_monitoring_service,
                default_timeout=45.0,
                client_info=client_info,
            ),
            self.set_addons_config: gapic_v1.method.wrap_method(
                self.set_addons_config, default_timeout=45.0, client_info=client_info,
            ),
            self.set_locations: gapic_v1.method.wrap_method(
                self.set_locations, default_timeout=45.0, client_info=client_info,
            ),
            self.update_master: gapic_v1.method.wrap_method(
                self.update_master, default_timeout=45.0, client_info=client_info,
            ),
            self.set_master_auth: gapic_v1.method.wrap_method(
                self.set_master_auth, default_timeout=45.0, client_info=client_info,
            ),
            self.delete_cluster: gapic_v1.method.wrap_method(
                self.delete_cluster,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.list_operations: gapic_v1.method.wrap_method(
                self.list_operations,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.get_operation: gapic_v1.method.wrap_method(
                self.get_operation,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.cancel_operation: gapic_v1.method.wrap_method(
                self.cancel_operation, default_timeout=45.0, client_info=client_info,
            ),
            self.get_server_config: gapic_v1.method.wrap_method(
                self.get_server_config,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.list_node_pools: gapic_v1.method.wrap_method(
                self.list_node_pools,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.get_node_pool: gapic_v1.method.wrap_method(
                self.get_node_pool,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.create_node_pool: gapic_v1.method.wrap_method(
                self.create_node_pool, default_timeout=45.0, client_info=client_info,
            ),
            self.delete_node_pool: gapic_v1.method.wrap_method(
                self.delete_node_pool,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.rollback_node_pool_upgrade: gapic_v1.method.wrap_method(
                self.rollback_node_pool_upgrade,
                default_timeout=45.0,
                client_info=client_info,
            ),
            self.set_node_pool_management: gapic_v1.method.wrap_method(
                self.set_node_pool_management,
                default_timeout=45.0,
                client_info=client_info,
            ),
            self.set_labels: gapic_v1.method.wrap_method(
                self.set_labels, default_timeout=45.0, client_info=client_info,
            ),
            self.set_legacy_abac: gapic_v1.method.wrap_method(
                self.set_legacy_abac, default_timeout=45.0, client_info=client_info,
            ),
            self.start_ip_rotation: gapic_v1.method.wrap_method(
                self.start_ip_rotation, default_timeout=45.0, client_info=client_info,
            ),
            self.complete_ip_rotation: gapic_v1.method.wrap_method(
                self.complete_ip_rotation,
                default_timeout=45.0,
                client_info=client_info,
            ),
            self.set_node_pool_size: gapic_v1.method.wrap_method(
                self.set_node_pool_size, default_timeout=45.0, client_info=client_info,
            ),
            self.set_network_policy: gapic_v1.method.wrap_method(
                self.set_network_policy, default_timeout=45.0, client_info=client_info,
            ),
            self.set_maintenance_policy: gapic_v1.method.wrap_method(
                self.set_maintenance_policy,
                default_timeout=45.0,
                client_info=client_info,
            ),
            self.list_usable_subnetworks: gapic_v1.method.wrap_method(
                self.list_usable_subnetworks,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.list_locations: gapic_v1.method.wrap_method(
                self.list_locations,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=20.0,
                client_info=client_info,
            ),
        }

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

    @property
    def list_locations(
        self,
    ) -> typing.Callable[
        [cluster_service.ListLocationsRequest],
        typing.Union[
            cluster_service.ListLocationsResponse,
            typing.Awaitable[cluster_service.ListLocationsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("ClusterManagerTransport",)
