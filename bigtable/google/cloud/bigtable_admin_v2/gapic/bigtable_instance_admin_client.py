# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client_config
from google.cloud.bigtable_admin_v2.gapic import enums
from google.cloud.bigtable_admin_v2.gapic.transports import (
    bigtable_instance_admin_grpc_transport,
)
from google.cloud.bigtable_admin_v2.proto import bigtable_instance_admin_pb2
from google.cloud.bigtable_admin_v2.proto import bigtable_instance_admin_pb2_grpc
from google.cloud.bigtable_admin_v2.proto import instance_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-bigtable").version


class BigtableInstanceAdminClient(object):
    """
    Service for creating, configuring, and deleting Cloud Bigtable Instances and
    Clusters. Provides access to the Instance and Cluster schemas only, not the
    tables' metadata or data stored in those tables.
    """

    SERVICE_ADDRESS = "bigtableadmin.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.bigtable.admin.v2.BigtableInstanceAdmin"

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
            BigtableInstanceAdminClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    @classmethod
    def instance_path(cls, project, instance):
        """Return a fully-qualified instance string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}",
            project=project,
            instance=instance,
        )

    @classmethod
    def app_profile_path(cls, project, instance, app_profile):
        """Return a fully-qualified app_profile string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}/appProfiles/{app_profile}",
            project=project,
            instance=instance,
            app_profile=app_profile,
        )

    @classmethod
    def cluster_path(cls, project, instance, cluster):
        """Return a fully-qualified cluster string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}/clusters/{cluster}",
            project=project,
            instance=instance,
            cluster=cluster,
        )

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.BigtableInstanceAdminGrpcTransport,
                    Callable[[~.Credentials, type], ~.BigtableInstanceAdminGrpcTransport]): A transport
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
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = bigtable_instance_admin_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=bigtable_instance_admin_grpc_transport.BigtableInstanceAdminGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = bigtable_instance_admin_grpc_transport.BigtableInstanceAdminGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
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
    def create_instance(
        self,
        parent,
        instance_id,
        instance,
        clusters,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Create an instance within a project.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `instance_id`:
            >>> instance_id = ''
            >>>
            >>> # TODO: Initialize `instance`:
            >>> instance = {}
            >>>
            >>> # TODO: Initialize `clusters`:
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
            instance (Union[dict, ~google.cloud.bigtable_admin_v2.types.Instance]): The instance to create. Fields marked ``OutputOnly`` must be left blank.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Instance`
            clusters (dict[str -> Union[dict, ~google.cloud.bigtable_admin_v2.types.Cluster]]): The clusters to be created within the instance, mapped by desired
                cluster ID, e.g., just ``mycluster`` rather than
                ``projects/myproject/instances/myinstance/clusters/mycluster``. Fields
                marked ``OutputOnly`` must be left blank. Currently, at most two
                clusters can be specified.

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
        # Wrap the transport method to add retry and timeout logic.
        if "create_instance" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_instance"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_instance,
                default_retry=self._method_configs["CreateInstance"].retry,
                default_timeout=self._method_configs["CreateInstance"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_instance_admin_pb2.CreateInstanceRequest(
            parent=parent, instance_id=instance_id, instance=instance, clusters=clusters
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

        operation = self._inner_api_calls["create_instance"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            instance_pb2.Instance,
            metadata_type=bigtable_instance_admin_pb2.CreateInstanceMetadata,
        )

    def get_instance(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
        # Wrap the transport method to add retry and timeout logic.
        if "get_instance" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_instance"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_instance,
                default_retry=self._method_configs["GetInstance"].retry,
                default_timeout=self._method_configs["GetInstance"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_instance_admin_pb2.GetInstanceRequest(name=name)
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

        return self._inner_api_calls["get_instance"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_instances(
        self,
        parent,
        page_token=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            parent (str): The unique name of the project for which a list of instances is
                requested. Values are of the form ``projects/<project>``.
            page_token (str): DEPRECATED: This field is unused and ignored.
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
        # Wrap the transport method to add retry and timeout logic.
        if "list_instances" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_instances"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_instances,
                default_retry=self._method_configs["ListInstances"].retry,
                default_timeout=self._method_configs["ListInstances"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_instance_admin_pb2.ListInstancesRequest(
            parent=parent, page_token=page_token
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

        return self._inner_api_calls["list_instances"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_instance(
        self,
        name,
        display_name,
        type_,
        labels,
        state=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            >>> # TODO: Initialize `display_name`:
            >>> display_name = ''
            >>>
            >>> # TODO: Initialize `type_`:
            >>> type_ = enums.Instance.Type.TYPE_UNSPECIFIED
            >>>
            >>> # TODO: Initialize `labels`:
            >>> labels = {}
            >>>
            >>> response = client.update_instance(name, display_name, type_, labels)

        Args:
            name (str): (``OutputOnly``) The unique name of the instance. Values are of the form
                ``projects/<project>/instances/[a-z][a-z0-9\\-]+[a-z0-9]``.
            display_name (str): The descriptive name for this instance as it appears in UIs.
                Can be changed at any time, but should be kept globally unique
                to avoid confusion.
            type_ (~google.cloud.bigtable_admin_v2.types.Type): The type of the instance. Defaults to ``PRODUCTION``.
            labels (dict[str -> str]): Labels are a flexible and lightweight mechanism for organizing cloud
                resources into groups that reflect a customer's organizational needs and
                deployment strategies. They can be used to filter resources and
                aggregate metrics.

                -  Label keys must be between 1 and 63 characters long and must conform
                   to the regular expression:
                   ``[\p{Ll}\p{Lo}][\p{Ll}\p{Lo}\p{N}_-]{0,62}``.
                -  Label values must be between 0 and 63 characters long and must
                   conform to the regular expression: ``[\p{Ll}\p{Lo}\p{N}_-]{0,63}``.
                -  No more than 64 labels can be associated with a given resource.
                -  Keys and values must both be under 128 bytes.
            state (~google.cloud.bigtable_admin_v2.types.State): (``OutputOnly``) The current state of the instance.
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
        # Wrap the transport method to add retry and timeout logic.
        if "update_instance" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_instance"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_instance,
                default_retry=self._method_configs["UpdateInstance"].retry,
                default_timeout=self._method_configs["UpdateInstance"].timeout,
                client_info=self._client_info,
            )

        request = instance_pb2.Instance(
            name=name, display_name=display_name, type=type_, labels=labels, state=state
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

        return self._inner_api_calls["update_instance"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def partial_update_instance(
        self,
        instance,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Partially updates an instance within a project.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> # TODO: Initialize `instance`:
            >>> instance = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
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
        # Wrap the transport method to add retry and timeout logic.
        if "partial_update_instance" not in self._inner_api_calls:
            self._inner_api_calls[
                "partial_update_instance"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.partial_update_instance,
                default_retry=self._method_configs["PartialUpdateInstance"].retry,
                default_timeout=self._method_configs["PartialUpdateInstance"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_instance_admin_pb2.PartialUpdateInstanceRequest(
            instance=instance, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("instance.name", instance.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["partial_update_instance"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            instance_pb2.Instance,
            metadata_type=bigtable_instance_admin_pb2.UpdateInstanceMetadata,
        )

    def delete_instance(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            name (str): The unique name of the instance to be deleted. Values are of the form
                ``projects/<project>/instances/<instance>``.
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
        # Wrap the transport method to add retry and timeout logic.
        if "delete_instance" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_instance"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_instance,
                default_retry=self._method_configs["DeleteInstance"].retry,
                default_timeout=self._method_configs["DeleteInstance"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_instance_admin_pb2.DeleteInstanceRequest(name=name)
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

        self._inner_api_calls["delete_instance"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_cluster(
        self,
        parent,
        cluster_id,
        cluster,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a cluster within an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize `cluster_id`:
            >>> cluster_id = ''
            >>>
            >>> # TODO: Initialize `cluster`:
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
                Values are of the form ``projects/<project>/instances/<instance>``.
            cluster_id (str): The ID to be used when referring to the new cluster within its instance,
                e.g., just ``mycluster`` rather than
                ``projects/myproject/instances/myinstance/clusters/mycluster``.
            cluster (Union[dict, ~google.cloud.bigtable_admin_v2.types.Cluster]): The cluster to be created. Fields marked ``OutputOnly`` must be left
                blank.

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

        request = bigtable_instance_admin_pb2.CreateClusterRequest(
            parent=parent, cluster_id=cluster_id, cluster=cluster
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

        operation = self._inner_api_calls["create_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            instance_pb2.Cluster,
            metadata_type=bigtable_instance_admin_pb2.CreateClusterMetadata,
        )

    def get_cluster(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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

        request = bigtable_instance_admin_pb2.GetClusterRequest(name=name)
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

    def list_clusters(
        self,
        parent,
        page_token=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            parent (str): The unique name of the instance for which a list of clusters is
                requested. Values are of the form
                ``projects/<project>/instances/<instance>``. Use ``<instance> = '-'`` to
                list Clusters for all Instances in a project, e.g.,
                ``projects/myproject/instances/-``.
            page_token (str): DEPRECATED: This field is unused and ignored.
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

        request = bigtable_instance_admin_pb2.ListClustersRequest(
            parent=parent, page_token=page_token
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

    def update_cluster(
        self,
        name,
        serve_nodes,
        location=None,
        state=None,
        default_storage_type=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a cluster within an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> name = client.cluster_path('[PROJECT]', '[INSTANCE]', '[CLUSTER]')
            >>>
            >>> # TODO: Initialize `serve_nodes`:
            >>> serve_nodes = 0
            >>>
            >>> response = client.update_cluster(name, serve_nodes)
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
            name (str): (``OutputOnly``) The unique name of the cluster. Values are of the form
                ``projects/<project>/instances/<instance>/clusters/[a-z][-a-z0-9]*``.
            serve_nodes (int): The number of nodes allocated to this cluster. More nodes enable higher
                throughput and more consistent performance.
            location (str): (``CreationOnly``) The location where this cluster's nodes and storage
                reside. For best performance, clients should be located as close as
                possible to this cluster. Currently only zones are supported, so values
                should be of the form ``projects/<project>/locations/<zone>``.
            state (~google.cloud.bigtable_admin_v2.types.State): (``OutputOnly``) The current state of the cluster.
            default_storage_type (~google.cloud.bigtable_admin_v2.types.StorageType): (``CreationOnly``) The type of storage used by this cluster to serve its
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

        request = instance_pb2.Cluster(
            name=name,
            serve_nodes=serve_nodes,
            location=location,
            state=state,
            default_storage_type=default_storage_type,
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

        operation = self._inner_api_calls["update_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            instance_pb2.Cluster,
            metadata_type=bigtable_instance_admin_pb2.UpdateClusterMetadata,
        )

    def delete_cluster(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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

        request = bigtable_instance_admin_pb2.DeleteClusterRequest(name=name)
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

        self._inner_api_calls["delete_cluster"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_app_profile(
        self,
        parent,
        app_profile_id,
        app_profile,
        ignore_warnings=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates an app profile within an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize `app_profile_id`:
            >>> app_profile_id = ''
            >>>
            >>> # TODO: Initialize `app_profile`:
            >>> app_profile = {}
            >>>
            >>> response = client.create_app_profile(parent, app_profile_id, app_profile)

        Args:
            parent (str): The unique name of the instance in which to create the new app profile.
                Values are of the form ``projects/<project>/instances/<instance>``.
            app_profile_id (str): The ID to be used when referring to the new app profile within its
                instance, e.g., just ``myprofile`` rather than
                ``projects/myproject/instances/myinstance/appProfiles/myprofile``.
            app_profile (Union[dict, ~google.cloud.bigtable_admin_v2.types.AppProfile]): The app profile to be created. Fields marked ``OutputOnly`` will be
                ignored.

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
        # Wrap the transport method to add retry and timeout logic.
        if "create_app_profile" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_app_profile"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_app_profile,
                default_retry=self._method_configs["CreateAppProfile"].retry,
                default_timeout=self._method_configs["CreateAppProfile"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_instance_admin_pb2.CreateAppProfileRequest(
            parent=parent,
            app_profile_id=app_profile_id,
            app_profile=app_profile,
            ignore_warnings=ignore_warnings,
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

        return self._inner_api_calls["create_app_profile"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_app_profile(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
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
        # Wrap the transport method to add retry and timeout logic.
        if "get_app_profile" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_app_profile"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_app_profile,
                default_retry=self._method_configs["GetAppProfile"].retry,
                default_timeout=self._method_configs["GetAppProfile"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_instance_admin_pb2.GetAppProfileRequest(name=name)
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

        return self._inner_api_calls["get_app_profile"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_app_profiles(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists information about app profiles in an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_app_profiles(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_app_profiles(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The unique name of the instance for which a list of app profiles is
                requested. Values are of the form
                ``projects/<project>/instances/<instance>``. Use ``<instance> = '-'`` to
                list AppProfiles for all Instances in a project, e.g.,
                ``projects/myproject/instances/-``.
            page_size (int): Maximum number of results per page.
                CURRENTLY UNIMPLEMENTED AND IGNORED.
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
        # Wrap the transport method to add retry and timeout logic.
        if "list_app_profiles" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_app_profiles"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_app_profiles,
                default_retry=self._method_configs["ListAppProfiles"].retry,
                default_timeout=self._method_configs["ListAppProfiles"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_instance_admin_pb2.ListAppProfilesRequest(
            parent=parent, page_size=page_size
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
                self._inner_api_calls["list_app_profiles"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="app_profiles",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_app_profile(
        self,
        app_profile,
        update_mask,
        ignore_warnings=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an app profile within an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> # TODO: Initialize `app_profile`:
            >>> app_profile = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
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
        # Wrap the transport method to add retry and timeout logic.
        if "update_app_profile" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_app_profile"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_app_profile,
                default_retry=self._method_configs["UpdateAppProfile"].retry,
                default_timeout=self._method_configs["UpdateAppProfile"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_instance_admin_pb2.UpdateAppProfileRequest(
            app_profile=app_profile,
            update_mask=update_mask,
            ignore_warnings=ignore_warnings,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("app_profile.name", app_profile.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["update_app_profile"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            instance_pb2.AppProfile,
            metadata_type=bigtable_instance_admin_pb2.UpdateAppProfileMetadata,
        )

    def delete_app_profile(
        self,
        name,
        ignore_warnings,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an app profile from an instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> name = client.app_profile_path('[PROJECT]', '[INSTANCE]', '[APP_PROFILE]')
            >>>
            >>> # TODO: Initialize `ignore_warnings`:
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
        # Wrap the transport method to add retry and timeout logic.
        if "delete_app_profile" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_app_profile"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_app_profile,
                default_retry=self._method_configs["DeleteAppProfile"].retry,
                default_timeout=self._method_configs["DeleteAppProfile"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_instance_admin_pb2.DeleteAppProfileRequest(
            name=name, ignore_warnings=ignore_warnings
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

        self._inner_api_calls["delete_app_profile"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_iam_policy(
        self,
        resource,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
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
        # Wrap the transport method to add retry and timeout logic.
        if "get_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_iam_policy,
                default_retry=self._method_configs["GetIamPolicy"].retry,
                default_timeout=self._method_configs["GetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_iam_policy(
        self,
        resource,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the access control policy on an instance resource. Replaces any
        existing policy.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> resource = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            policy (Union[dict, ~google.cloud.bigtable_admin_v2.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
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
        # Wrap the transport method to add retry and timeout logic.
        if "set_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_iam_policy,
                default_retry=self._method_configs["SetIamPolicy"].retry,
                default_timeout=self._method_configs["SetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.SetIamPolicyRequest(resource=resource, policy=policy)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def test_iam_permissions(
        self,
        resource,
        permissions,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns permissions that the caller has on the specified instance resource.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableInstanceAdminClient()
            >>>
            >>> resource = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
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
        # Wrap the transport method to add retry and timeout logic.
        if "test_iam_permissions" not in self._inner_api_calls:
            self._inner_api_calls[
                "test_iam_permissions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.test_iam_permissions,
                default_retry=self._method_configs["TestIamPermissions"].retry,
                default_timeout=self._method_configs["TestIamPermissions"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["test_iam_permissions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
