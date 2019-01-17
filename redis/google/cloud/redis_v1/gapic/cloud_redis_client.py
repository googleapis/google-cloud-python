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
"""Accesses the google.cloud.redis.v1 CloudRedis API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.redis_v1.gapic import cloud_redis_client_config
from google.cloud.redis_v1.gapic import enums
from google.cloud.redis_v1.gapic.transports import cloud_redis_grpc_transport
from google.cloud.redis_v1.proto import cloud_redis_pb2
from google.cloud.redis_v1.proto import cloud_redis_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-redis").version


class CloudRedisClient(object):
    """
    Configures and manages Cloud Memorystore for Redis instances

    Google Cloud Memorystore for Redis v1

    The ``redis.googleapis.com`` service implements the Google Cloud
    Memorystore for Redis API and defines the following resource model for
    managing Redis instances: \* The service works with a collection of
    cloud projects, named: ``/projects/*`` \* Each project has a collection
    of available locations, named: ``/locations/*`` \* Each location has a
    collection of Redis instances, named: ``/instances/*`` \* As such, Redis
    instances are resources of the form:
    ``/projects/{project_id}/locations/{location_id}/instances/{instance_id}``

    Note that location\_id must be refering to a GCP ``region``; for
    example: \*
    ``projects/redpepper-1290/locations/us-central1/instances/my-redis``
    """

    SERVICE_ADDRESS = "redis.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.redis.v1.CloudRedis"

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
            CloudRedisClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    @classmethod
    def instance_path(cls, project, location, instance):
        """Return a fully-qualified instance string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/instances/{instance}",
            project=project,
            location=location,
            instance=instance,
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
            transport (Union[~.CloudRedisGrpcTransport,
                    Callable[[~.Credentials, type], ~.CloudRedisGrpcTransport]): A transport
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
            client_config = cloud_redis_client_config.config

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
                    default_class=cloud_redis_grpc_transport.CloudRedisGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = cloud_redis_grpc_transport.CloudRedisGrpcTransport(
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
    def list_instances(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all Redis instances owned by a project in either the specified
        location (region) or all locations.

        The location should have the following format: \*
        ``projects/{project_id}/locations/{location_id}``

        If ``location_id`` is specified as ``-`` (wildcard), then all regions
        available to the project are queried, and the results are aggregated.

        Example:
            >>> from google.cloud import redis_v1
            >>>
            >>> client = redis_v1.CloudRedisClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_instances(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_instances(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the instance location using the form:
                ``projects/{project_id}/locations/{location_id}`` where ``location_id``
                refers to a GCP region
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
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
            is an iterable of :class:`~google.cloud.redis_v1.types.Instance` instances.
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
        if "list_instances" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_instances"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_instances,
                default_retry=self._method_configs["ListInstances"].retry,
                default_timeout=self._method_configs["ListInstances"].timeout,
                client_info=self._client_info,
            )

        request = cloud_redis_pb2.ListInstancesRequest(
            parent=parent, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_instances"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="instances",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_instance(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the details of a specific Redis instance.

        Example:
            >>> from google.cloud import redis_v1
            >>>
            >>> client = redis_v1.CloudRedisClient()
            >>>
            >>> name = client.instance_path('[PROJECT]', '[LOCATION]', '[INSTANCE]')
            >>>
            >>> response = client.get_instance(name)

        Args:
            name (str): Required. Redis instance resource name using the form:
                ``projects/{project_id}/locations/{location_id}/instances/{instance_id}``
                where ``location_id`` refers to a GCP region
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.redis_v1.types.Instance` instance.

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

        request = cloud_redis_pb2.GetInstanceRequest(name=name)
        return self._inner_api_calls["get_instance"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_instance(
        self,
        parent,
        instance_id,
        instance,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a Redis instance based on the specified tier and memory size.

        By default, the instance is accessible from the project's `default
        network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__.

        The creation is executed asynchronously and callers may check the
        returned operation to track its progress. Once the operation is
        completed the Redis instance will be fully functional. Completed
        longrunning.Operation will contain the new instance object in the
        response field.

        The returned operation is automatically deleted after a few hours, so
        there is no need to call DeleteOperation.

        Example:
            >>> from google.cloud import redis_v1
            >>> from google.cloud.redis_v1 import enums
            >>>
            >>> client = redis_v1.CloudRedisClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>> instance_id = 'test_instance'
            >>> tier = enums.Instance.Tier.BASIC
            >>> memory_size_gb = 1
            >>> instance = {'tier': tier, 'memory_size_gb': memory_size_gb}
            >>>
            >>> response = client.create_instance(parent, instance_id, instance)
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
            parent (str): Required. The resource name of the instance location using the form:
                ``projects/{project_id}/locations/{location_id}`` where ``location_id``
                refers to a GCP region
            instance_id (str): Required. The logical name of the Redis instance in the customer project
                with the following restrictions:

                -  Must contain only lowercase letters, numbers, and hyphens.
                -  Must start with a letter.
                -  Must be between 1-40 characters.
                -  Must end with a number or a letter.
                -  Must be unique within the customer project / location
            instance (Union[dict, ~google.cloud.redis_v1.types.Instance]): Required. A Redis [Instance] resource

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.redis_v1.types.Instance`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.redis_v1.types._OperationFuture` instance.

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

        request = cloud_redis_pb2.CreateInstanceRequest(
            parent=parent, instance_id=instance_id, instance=instance
        )
        operation = self._inner_api_calls["create_instance"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            cloud_redis_pb2.Instance,
            metadata_type=cloud_redis_pb2.OperationMetadata,
        )

    def update_instance(
        self,
        update_mask,
        instance,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates the metadata and configuration of a specific Redis instance.

        Completed longrunning.Operation will contain the new instance object
        in the response field. The returned operation is automatically deleted
        after a few hours, so there is no need to call DeleteOperation.

        Example:
            >>> from google.cloud import redis_v1
            >>>
            >>> client = redis_v1.CloudRedisClient()
            >>>
            >>> paths_element = 'display_name'
            >>> paths_element_2 = 'memory_size_gb'
            >>> paths = [paths_element, paths_element_2]
            >>> update_mask = {'paths': paths}
            >>> display_name = 'UpdatedDisplayName'
            >>> memory_size_gb = 4
            >>> instance = {'display_name': display_name, 'memory_size_gb': memory_size_gb}
            >>>
            >>> response = client.update_instance(update_mask, instance)
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
            update_mask (Union[dict, ~google.cloud.redis_v1.types.FieldMask]): Required. Mask of fields to update. At least one path must be supplied
                in this field. The elements of the repeated paths field may only include
                these fields from ``Instance``:

                -  ``displayName``
                -  ``labels``
                -  ``memorySizeGb``
                -  ``redisConfig``

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.redis_v1.types.FieldMask`
            instance (Union[dict, ~google.cloud.redis_v1.types.Instance]): Required. Update description. Only fields specified in update\_mask are
                updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.redis_v1.types.Instance`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.redis_v1.types._OperationFuture` instance.

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

        request = cloud_redis_pb2.UpdateInstanceRequest(
            update_mask=update_mask, instance=instance
        )
        operation = self._inner_api_calls["update_instance"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            cloud_redis_pb2.Instance,
            metadata_type=cloud_redis_pb2.OperationMetadata,
        )

    def delete_instance(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a specific Redis instance.  Instance stops serving and data is
        deleted.

        Example:
            >>> from google.cloud import redis_v1
            >>>
            >>> client = redis_v1.CloudRedisClient()
            >>>
            >>> name = client.instance_path('[PROJECT]', '[LOCATION]', '[INSTANCE]')
            >>>
            >>> response = client.delete_instance(name)
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
            name (str): Required. Redis instance resource name using the form:
                ``projects/{project_id}/locations/{location_id}/instances/{instance_id}``
                where ``location_id`` refers to a GCP region
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.redis_v1.types._OperationFuture` instance.

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

        request = cloud_redis_pb2.DeleteInstanceRequest(name=name)
        operation = self._inner_api_calls["delete_instance"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=cloud_redis_pb2.OperationMetadata,
        )
