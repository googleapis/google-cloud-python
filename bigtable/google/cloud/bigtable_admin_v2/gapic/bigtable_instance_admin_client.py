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
"""Accesses the google.bigtable.admin.v2 BigtableInstanceAdmin API."""

import functools
import pkg_resources

from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator

from google.cloud.bigtable import paths
from google.cloud.bigtable_admin_v2.gapic import (
    bigtable_instance_admin_client_config)
from google.cloud.bigtable_admin_v2.gapic import enums
from google.cloud.bigtable_admin_v2.proto import bigtable_instance_admin_pb2
from google.cloud.bigtable_admin_v2.proto import (
    bigtable_instance_admin_pb2_grpc)
from google.cloud.bigtable_admin_v2.proto import instance_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-bigtable', ).version


class BigtableInstanceAdminClient(object):
    """
    Service for creating, configuring, and deleting Cloud Bigtable Instances and
    Clusters. Provides access to the Instance and Cluster schemas only, not the
    tables' metadata or data stored in those tables.
    """

    SERVICE_ADDRESS = 'bigtableadmin.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/bigtable.admin',
        'https://www.googleapis.com/auth/bigtable.admin.cluster',
        'https://www.googleapis.com/auth/bigtable.admin.instance',
        'https://www.googleapis.com/auth/bigtable.admin.table',
        'https://www.googleapis.com/auth/cloud-bigtable.admin',
        'https://www.googleapis.com/auth/cloud-bigtable.admin.cluster',
        'https://www.googleapis.com/auth/cloud-bigtable.admin.table',
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/cloud-platform.read-only',
    )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.bigtable.admin.v2.BigtableInstanceAdmin'

    project_path = staticmethod(paths.project_path)
    instance_path = staticmethod(paths.instance_path)
    app_profile_path = staticmethod(paths.app_profile_path)
    cluster_path = staticmethod(paths.cluster_path)
    location_path = staticmethod(paths.location_path)

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=bigtable_instance_admin_client_config.config,
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
        self.bigtable_instance_admin_stub = (
            bigtable_instance_admin_pb2_grpc.BigtableInstanceAdminStub(channel))

        # Operations client for methods that return long-running operations
        # futures.
        self.operations_client = (
            google.api_core.operations_v1.OperationsClient(channel))

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
        self._create_instance = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.CreateInstance,
            default_retry=method_configs['CreateInstance'].retry,
            default_timeout=method_configs['CreateInstance'].timeout,
            client_info=client_info,
        )
        self._get_instance = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.GetInstance,
            default_retry=method_configs['GetInstance'].retry,
            default_timeout=method_configs['GetInstance'].timeout,
            client_info=client_info,
        )
        self._list_instances = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.ListInstances,
            default_retry=method_configs['ListInstances'].retry,
            default_timeout=method_configs['ListInstances'].timeout,
            client_info=client_info,
        )
        self._update_instance = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.UpdateInstance,
            default_retry=method_configs['UpdateInstance'].retry,
            default_timeout=method_configs['UpdateInstance'].timeout,
            client_info=client_info,
        )
        self._partial_update_instance = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.PartialUpdateInstance,
            default_retry=method_configs['PartialUpdateInstance'].retry,
            default_timeout=method_configs['PartialUpdateInstance'].timeout,
            client_info=client_info,
        )
        self._delete_instance = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.DeleteInstance,
            default_retry=method_configs['DeleteInstance'].retry,
            default_timeout=method_configs['DeleteInstance'].timeout,
            client_info=client_info,
        )
        self._create_cluster = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.CreateCluster,
            default_retry=method_configs['CreateCluster'].retry,
            default_timeout=method_configs['CreateCluster'].timeout,
            client_info=client_info,
        )
        self._get_cluster = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.GetCluster,
            default_retry=method_configs['GetCluster'].retry,
            default_timeout=method_configs['GetCluster'].timeout,
            client_info=client_info,
        )
        self._list_clusters = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.ListClusters,
            default_retry=method_configs['ListClusters'].retry,
            default_timeout=method_configs['ListClusters'].timeout,
            client_info=client_info,
        )
        self._update_cluster = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.UpdateCluster,
            default_retry=method_configs['UpdateCluster'].retry,
            default_timeout=method_configs['UpdateCluster'].timeout,
            client_info=client_info,
        )
        self._delete_cluster = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.DeleteCluster,
            default_retry=method_configs['DeleteCluster'].retry,
            default_timeout=method_configs['DeleteCluster'].timeout,
            client_info=client_info,
        )
        self._create_app_profile = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.CreateAppProfile,
            default_retry=method_configs['CreateAppProfile'].retry,
            default_timeout=method_configs['CreateAppProfile'].timeout,
            client_info=client_info,
        )
        self._get_app_profile = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.GetAppProfile,
            default_retry=method_configs['GetAppProfile'].retry,
            default_timeout=method_configs['GetAppProfile'].timeout,
            client_info=client_info,
        )
        self._list_app_profiles = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.ListAppProfiles,
            default_retry=method_configs['ListAppProfiles'].retry,
            default_timeout=method_configs['ListAppProfiles'].timeout,
            client_info=client_info,
        )
        self._update_app_profile = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.UpdateAppProfile,
            default_retry=method_configs['UpdateAppProfile'].retry,
            default_timeout=method_configs['UpdateAppProfile'].timeout,
            client_info=client_info,
        )
        self._delete_app_profile = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.DeleteAppProfile,
            default_retry=method_configs['DeleteAppProfile'].retry,
            default_timeout=method_configs['DeleteAppProfile'].timeout,
            client_info=client_info,
        )
        self._get_iam_policy = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.GetIamPolicy,
            default_retry=method_configs['GetIamPolicy'].retry,
            default_timeout=method_configs['GetIamPolicy'].timeout,
            client_info=client_info,
        )
        self._set_iam_policy = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.SetIamPolicy,
            default_retry=method_configs['SetIamPolicy'].retry,
            default_timeout=method_configs['SetIamPolicy'].timeout,
            client_info=client_info,
        )
        self._test_iam_permissions = google.api_core.gapic_v1.method.wrap_method(
            self.bigtable_instance_admin_stub.TestIamPermissions,
            default_retry=method_configs['TestIamPermissions'].retry,
            default_timeout=method_configs['TestIamPermissions'].timeout,
            client_info=client_info,
        )

    # Service calls
    def create_instance(self,
                        parent,
                        instance_id,
                        instance,
                        clusters,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Create an instance within a project.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize ``instance_id``:
            >>> instance_id = ''
            >>>
            >>> # TODO: Initialize ``instance``:
            >>> instance = {}
            >>>
            >>> # TODO: Initialize ``clusters``:
            >>> clusters = {}
            >>>
            >>> response = client.create_instance(parent, instance_id, instance, clusters)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): The unique name of the project in which to create the new instance.
                Values are of the form ``projects/<project>``.
            instance_id (str): The ID to be used when referring to the new instance within its project,
                e.g., just ``myinstance`` rather than
                ``projects/myproject/instances/myinstance``.
            instance (Union[dict, ~google.cloud.bigtable_admin_v2.types.Instance]): The instance to create.
                Fields marked ``OutputOnly`` must be left blank.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Instance`
            clusters (dict[str -> Union[dict, ~google.cloud.bigtable_admin_v2.types.Cluster]]): The clusters to be created within the instance, mapped by desired
                cluster ID, e.g., just ``mycluster`` rather than
                ``projects/myproject/instances/myinstance/clusters/mycluster``.
                Fields marked ``OutputOnly`` must be left blank.
                Currently exactly one cluster must be specified.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Cluster`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.CreateInstanceRequest(
            parent=parent,
            instance_id=instance_id,
            instance=instance,
            clusters=clusters,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('parent', parent)], )
        metadata.append(routing_header)

        operation = self._create_instance(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            instance_pb2.Instance,
            metadata_type=bigtable_instance_admin_pb2.CreateInstanceMetadata,
        )

    def get_instance(self,
                     name,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT,
                     metadata=None):
        """
        Gets information about an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> name = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> response = client.get_instance(name)

        Args:
            name (str): The unique name of the requested instance. Values are of the form
                ``projects/<project>/instances/<instance>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Instance` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.GetInstanceRequest(name=name, )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('name', name)], )
        metadata.append(routing_header)

        return self._get_instance(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_instances(self,
                       parent,
                       page_token=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Lists information about instances in a project.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.list_instances(parent)

        Args:
            parent (str): The unique name of the project for which a list of instances is requested.
                Values are of the form ``projects/<project>``.
            page_token (str): The value of ``next_page_token`` returned by a previous call.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.ListInstancesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.ListInstancesRequest(
            parent=parent,
            page_token=page_token,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('parent', parent)], )
        metadata.append(routing_header)

        return self._list_instances(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_instance(self,
                        name,
                        display_name,
                        type_,
                        labels,
                        state=None,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Updates an instance within a project.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>> from google.cloud.bigtable_admin_v2 import enums
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> name = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize ``display_name``:
            >>> display_name = ''
            >>>
            >>> # TODO: Initialize ``type_``:
            >>> type_ = enums.Instance.Type.TYPE_UNSPECIFIED
            >>>
            >>> # TODO: Initialize ``labels``:
            >>> labels = {}
            >>>
            >>> response = client.update_instance(name, display_name, type_, labels)

        Args:
            name (str): (``OutputOnly``)
                The unique name of the instance. Values are of the form
                ``projects/<project>/instances/[a-z][a-z0-9\\-]+[a-z0-9]``.
            display_name (str): The descriptive name for this instance as it appears in UIs.
                Can be changed at any time, but should be kept globally unique
                to avoid confusion.
            type_ (~google.cloud.bigtable_admin_v2.types.Type): The type of the instance. Defaults to ``PRODUCTION``.
            labels (dict[str -> str]): Labels are a flexible and lightweight mechanism for organizing cloud
                resources into groups that reflect a customer's organizational needs and
                deployment strategies. They can be used to filter resources and aggregate
                metrics.

                * Label keys must be between 1 and 63 characters long and must conform to
                  the regular expression: ``[\p{Ll}\p{Lo}][\p{Ll}\p{Lo}\p{N}_-]{0,62}``.
                * Label values must be between 0 and 63 characters long and must conform to
                  the regular expression: ``[\p{Ll}\p{Lo}\p{N}_-]{0,63}``.
                * No more than 64 labels can be associated with a given resource.
                * Keys and values must both be under 128 bytes.
            state (~google.cloud.bigtable_admin_v2.types.State): (``OutputOnly``)
                The current state of the instance.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Instance` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = instance_pb2.Instance(
            name=name,
            display_name=display_name,
            type=type_,
            labels=labels,
            state=state,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('name', name)], )
        metadata.append(routing_header)

        return self._update_instance(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def partial_update_instance(
            self,
            instance,
            update_mask,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Partially updates an instance within a project.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> # TODO: Initialize ``instance``:
            >>> instance = {}
            >>>
            >>> # TODO: Initialize ``update_mask``:
            >>> update_mask = {}
            >>>
            >>> response = client.partial_update_instance(instance, update_mask)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            instance (Union[dict, ~google.cloud.bigtable_admin_v2.types.Instance]): The Instance which will (partially) replace the current value.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Instance`
            update_mask (Union[dict, ~google.cloud.bigtable_admin_v2.types.FieldMask]): The subset of Instance fields which should be replaced.
                Must be explicitly set.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.PartialUpdateInstanceRequest(
            instance=instance,
            update_mask=update_mask,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('instance.name', instance.name)], )
        metadata.append(routing_header)

        operation = self._partial_update_instance(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            instance_pb2.Instance,
            metadata_type=bigtable_instance_admin_pb2.UpdateInstanceMetadata,
        )

    def delete_instance(self,
                        name,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Delete an instance from a project.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> name = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> client.delete_instance(name)

        Args:
            name (str): The unique name of the instance to be deleted.
                Values are of the form ``projects/<project>/instances/<instance>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.DeleteInstanceRequest(
            name=name, )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('name', name)], )
        metadata.append(routing_header)

        self._delete_instance(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_cluster(self,
                       parent,
                       cluster_id,
                       cluster,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Creates a cluster within an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize ``cluster_id``:
            >>> cluster_id = ''
            >>>
            >>> # TODO: Initialize ``cluster``:
            >>> cluster = {}
            >>>
            >>> response = client.create_cluster(parent, cluster_id, cluster)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): The unique name of the instance in which to create the new cluster.
                Values are of the form
                ``projects/<project>/instances/<instance>``.
            cluster_id (str): The ID to be used when referring to the new cluster within its instance,
                e.g., just ``mycluster`` rather than
                ``projects/myproject/instances/myinstance/clusters/mycluster``.
            cluster (Union[dict, ~google.cloud.bigtable_admin_v2.types.Cluster]): The cluster to be created.
                Fields marked ``OutputOnly`` must be left blank.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Cluster`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.CreateClusterRequest(
            parent=parent,
            cluster_id=cluster_id,
            cluster=cluster,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('parent', parent)], )
        metadata.append(routing_header)

        operation = self._create_cluster(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            instance_pb2.Cluster,
            metadata_type=bigtable_instance_admin_pb2.CreateClusterMetadata,
        )

    def get_cluster(self,
                    name,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT,
                    metadata=None):
        """
        Gets information about a cluster.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> name = client.cluster_path('[PROJECT]', '[INSTANCE]', '[CLUSTER]')
            >>>
            >>> response = client.get_cluster(name)

        Args:
            name (str): The unique name of the requested cluster. Values are of the form
                ``projects/<project>/instances/<instance>/clusters/<cluster>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Cluster` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.GetClusterRequest(name=name, )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('name', name)], )
        metadata.append(routing_header)

        return self._get_cluster(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_clusters(self,
                      parent,
                      page_token=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT,
                      metadata=None):
        """
        Lists information about clusters in an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> response = client.list_clusters(parent)

        Args:
            parent (str): The unique name of the instance for which a list of clusters is requested.
                Values are of the form ``projects/<project>/instances/<instance>``.
                Use ``<instance> = '-'`` to list Clusters for all Instances in a project,
                e.g., ``projects/myproject/instances/-``.
            page_token (str): The value of ``next_page_token`` returned by a previous call.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.ListClustersResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.ListClustersRequest(
            parent=parent,
            page_token=page_token,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('parent', parent)], )
        metadata.append(routing_header)

        return self._list_clusters(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_cluster(self,
                       name,
                       location,
                       serve_nodes,
                       state=None,
                       default_storage_type=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Updates a cluster within an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> name = client.cluster_path('[PROJECT]', '[INSTANCE]', '[CLUSTER]')
            >>>
            >>> # TODO: Initialize ``location``:
            >>> location = ''
            >>>
            >>> # TODO: Initialize ``serve_nodes``:
            >>> serve_nodes = 0
            >>>
            >>> response = client.update_cluster(name, location, serve_nodes)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            name (str): (``OutputOnly``)
                The unique name of the cluster. Values are of the form
                ``projects/<project>/instances/<instance>/clusters/[a-z][-a-z0-9]*``.
            location (str): (``CreationOnly``)
                The location where this cluster's nodes and storage reside. For best
                performance, clients should be located as close as possible to this
                cluster. Currently only zones are supported, so values should be of the
                form ``projects/<project>/locations/<zone>``.
            serve_nodes (int): The number of nodes allocated to this cluster. More nodes enable higher
                throughput and more consistent performance.
            state (~google.cloud.bigtable_admin_v2.types.State): (``OutputOnly``)
                The current state of the cluster.
            default_storage_type (~google.cloud.bigtable_admin_v2.types.StorageType): (``CreationOnly``)
                The type of storage used by this cluster to serve its
                parent instance's tables, unless explicitly overridden.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = instance_pb2.Cluster(
            name=name,
            location=location,
            serve_nodes=serve_nodes,
            state=state,
            default_storage_type=default_storage_type,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('name', name)], )
        metadata.append(routing_header)

        operation = self._update_cluster(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            instance_pb2.Cluster,
            metadata_type=bigtable_instance_admin_pb2.UpdateClusterMetadata,
        )

    def delete_cluster(self,
                       name,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Deletes a cluster from an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> name = client.cluster_path('[PROJECT]', '[INSTANCE]', '[CLUSTER]')
            >>>
            >>> client.delete_cluster(name)

        Args:
            name (str): The unique name of the cluster to be deleted. Values are of the form
                ``projects/<project>/instances/<instance>/clusters/<cluster>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.DeleteClusterRequest(name=name, )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('name', name)], )
        metadata.append(routing_header)

        self._delete_cluster(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_app_profile(self,
                           parent,
                           app_profile_id,
                           app_profile,
                           ignore_warnings=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        This is a private alpha release of Cloud Bigtable replication. This feature
        is not currently available to most Cloud Bigtable customers. This feature
        might be changed in backward-incompatible ways and is not recommended for
        production use. It is not subject to any SLA or deprecation policy.

        Creates an app profile within an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize ``app_profile_id``:
            >>> app_profile_id = ''
            >>>
            >>> # TODO: Initialize ``app_profile``:
            >>> app_profile = {}
            >>>
            >>> response = client.create_app_profile(parent, app_profile_id, app_profile)

        Args:
            parent (str): The unique name of the instance in which to create the new app profile.
                Values are of the form
                ``projects/<project>/instances/<instance>``.
            app_profile_id (str): The ID to be used when referring to the new app profile within its
                instance, e.g., just ``myprofile`` rather than
                ``projects/myproject/instances/myinstance/appProfiles/myprofile``.
            app_profile (Union[dict, ~google.cloud.bigtable_admin_v2.types.AppProfile]): The app profile to be created.
                Fields marked ``OutputOnly`` will be ignored.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.AppProfile`
            ignore_warnings (bool): If true, ignore safety checks when creating the app profile.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.AppProfile` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.CreateAppProfileRequest(
            parent=parent,
            app_profile_id=app_profile_id,
            app_profile=app_profile,
            ignore_warnings=ignore_warnings,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('parent', parent)], )
        metadata.append(routing_header)

        return self._create_app_profile(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def get_app_profile(self,
                        name,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        This is a private alpha release of Cloud Bigtable replication. This feature
        is not currently available to most Cloud Bigtable customers. This feature
        might be changed in backward-incompatible ways and is not recommended for
        production use. It is not subject to any SLA or deprecation policy.

        Gets information about an app profile.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> name = client.app_profile_path('[PROJECT]', '[INSTANCE]', '[APP_PROFILE]')
            >>>
            >>> response = client.get_app_profile(name)

        Args:
            name (str): The unique name of the requested app profile. Values are of the form
                ``projects/<project>/instances/<instance>/appProfiles/<app_profile>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.AppProfile` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.GetAppProfileRequest(name=name, )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('name', name)], )
        metadata.append(routing_header)

        return self._get_app_profile(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_app_profiles(self,
                          parent,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT,
                          metadata=None):
        """
        This is a private alpha release of Cloud Bigtable replication. This feature
        is not currently available to most Cloud Bigtable customers. This feature
        might be changed in backward-incompatible ways and is not recommended for
        production use. It is not subject to any SLA or deprecation policy.

        Lists information about app profiles in an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_app_profiles(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_app_profiles(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The unique name of the instance for which a list of app profiles is
                requested. Values are of the form
                ``projects/<project>/instances/<instance>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.bigtable_admin_v2.types.AppProfile` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.ListAppProfilesRequest(
            parent=parent, )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('parent', parent)], )
        metadata.append(routing_header)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_app_profiles,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='app_profiles',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def update_app_profile(self,
                           app_profile,
                           update_mask,
                           ignore_warnings=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        This is a private alpha release of Cloud Bigtable replication. This feature
        is not currently available to most Cloud Bigtable customers. This feature
        might be changed in backward-incompatible ways and is not recommended for
        production use. It is not subject to any SLA or deprecation policy.

        Updates an app profile within an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> # TODO: Initialize ``app_profile``:
            >>> app_profile = {}
            >>>
            >>> # TODO: Initialize ``update_mask``:
            >>> update_mask = {}
            >>>
            >>> response = client.update_app_profile(app_profile, update_mask)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            app_profile (Union[dict, ~google.cloud.bigtable_admin_v2.types.AppProfile]): The app profile which will (partially) replace the current value.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.AppProfile`
            update_mask (Union[dict, ~google.cloud.bigtable_admin_v2.types.FieldMask]): The subset of app profile fields which should be replaced.
                If unset, all fields will be replaced.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.FieldMask`
            ignore_warnings (bool): If true, ignore safety checks when updating the app profile.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.UpdateAppProfileRequest(
            app_profile=app_profile,
            update_mask=update_mask,
            ignore_warnings=ignore_warnings,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('app_profile.name', app_profile.name)], )
        metadata.append(routing_header)

        operation = self._update_app_profile(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            instance_pb2.AppProfile,
            metadata_type=bigtable_instance_admin_pb2.UpdateAppProfileMetadata,
        )

    def delete_app_profile(self,
                           name,
                           ignore_warnings,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        This is a private alpha release of Cloud Bigtable replication. This feature
        is not currently available to most Cloud Bigtable customers. This feature
        might be changed in backward-incompatible ways and is not recommended for
        production use. It is not subject to any SLA or deprecation policy.

        Deletes an app profile from an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> name = client.app_profile_path('[PROJECT]', '[INSTANCE]', '[APP_PROFILE]')
            >>>
            >>> # TODO: Initialize ``ignore_warnings``:
            >>> ignore_warnings = False
            >>>
            >>> client.delete_app_profile(name, ignore_warnings)

        Args:
            name (str): The unique name of the app profile to be deleted. Values are of the form
                ``projects/<project>/instances/<instance>/appProfiles/<app_profile>``.
            ignore_warnings (bool): If true, ignore safety checks when deleting the app profile.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = bigtable_instance_admin_pb2.DeleteAppProfileRequest(
            name=name,
            ignore_warnings=ignore_warnings,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('name', name)], )
        metadata.append(routing_header)

        self._delete_app_profile(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def get_iam_policy(self,
                       resource,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        This is a private alpha release of Cloud Bigtable instance level
        permissions. This feature is not currently available to most Cloud Bigtable
        customers. This feature might be changed in backward-incompatible ways and
        is not recommended for production use. It is not subject to any SLA or
        deprecation policy.

        Gets the access control policy for an instance resource. Returns an empty
        policy if an instance exists but does not have a policy set.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> resource = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = iam_policy_pb2.GetIamPolicyRequest(resource=resource, )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('resource', resource)], )
        metadata.append(routing_header)

        return self._get_iam_policy(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def set_iam_policy(self,
                       resource,
                       policy,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        This is a private alpha release of Cloud Bigtable instance level
        permissions. This feature is not currently available to most Cloud Bigtable
        customers. This feature might be changed in backward-incompatible ways and
        is not recommended for production use. It is not subject to any SLA or
        deprecation policy.

        Sets the access control policy on an instance resource. Replaces any
        existing policy.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> resource = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize ``policy``:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            policy (Union[dict, ~google.cloud.bigtable_admin_v2.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The size of
                the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource,
            policy=policy,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('resource', resource)], )
        metadata.append(routing_header)

        return self._set_iam_policy(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def test_iam_permissions(self,
                             resource,
                             permissions,
                             retry=google.api_core.gapic_v1.method.DEFAULT,
                             timeout=google.api_core.gapic_v1.method.DEFAULT,
                             metadata=None):
        """
        This is a private alpha release of Cloud Bigtable instance level
        permissions. This feature is not currently available to most Cloud Bigtable
        customers. This feature might be changed in backward-incompatible ways and
        is not recommended for production use. It is not subject to any SLA or
        deprecation policy.

        Returns permissions that the caller has on the specified instance resource.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> resource = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize ``permissions``:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see
                `IAM Overview <https://cloud.google.com/iam/docs/overview#permissions>`_.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource,
            permissions=permissions,
        )

        routing_header = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
            [('resource', resource)], )
        metadata.append(routing_header)

        return self._test_iam_permissions(
            request, retry=retry, timeout=timeout, metadata=metadata)
