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
"""Accesses the google.cloud.tasks.v2beta2 CloudTasks API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.tasks_v2beta2.gapic import cloud_tasks_client_config
from google.cloud.tasks_v2beta2.gapic import enums
from google.cloud.tasks_v2beta2.gapic.transports import cloud_tasks_grpc_transport
from google.cloud.tasks_v2beta2.proto import cloudtasks_pb2
from google.cloud.tasks_v2beta2.proto import cloudtasks_pb2_grpc
from google.cloud.tasks_v2beta2.proto import queue_pb2
from google.cloud.tasks_v2beta2.proto import task_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-tasks").version


class CloudTasksClient(object):
    """
    Cloud Tasks allows developers to manage the execution of background
    work in their applications.
    """

    SERVICE_ADDRESS = "cloudtasks.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.tasks.v2beta2.CloudTasks"

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
            CloudTasksClient: The constructed client.
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
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    @classmethod
    def queue_path(cls, project, location, queue):
        """Return a fully-qualified queue string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/queues/{queue}",
            project=project,
            location=location,
            queue=queue,
        )

    @classmethod
    def task_path(cls, project, location, queue, task):
        """Return a fully-qualified task string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/queues/{queue}/tasks/{task}",
            project=project,
            location=location,
            queue=queue,
            task=task,
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
            transport (Union[~.CloudTasksGrpcTransport,
                    Callable[[~.Credentials, type], ~.CloudTasksGrpcTransport]): A transport
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
            client_config = cloud_tasks_client_config.config

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
                    default_class=cloud_tasks_grpc_transport.CloudTasksGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = cloud_tasks_grpc_transport.CloudTasksGrpcTransport(
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
    def list_queues(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists queues.

        Queues are returned in lexicographical order.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_queues(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_queues(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required.

                The location name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``
            filter_ (str): ``filter`` can be used to specify a subset of queues. Any ``Queue``
                field can be used as a filter and several operators as supported. For
                example: ``<=, <, >=, >, !=, =, :``. The filter syntax is the same as
                described in `Stackdriver's Advanced Logs
                Filters <https://cloud.google.com/logging/docs/view/advanced_filters>`__.

                Sample filter "app\_engine\_http\_target: \*".

                Note that using filters might cause fewer queues than the
                requested\_page size to be returned.
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
            is an iterable of :class:`~google.cloud.tasks_v2beta2.types.Queue` instances.
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
        if "list_queues" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_queues"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_queues,
                default_retry=self._method_configs["ListQueues"].retry,
                default_timeout=self._method_configs["ListQueues"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.ListQueuesRequest(
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
                self._inner_api_calls["list_queues"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="queues",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_queue(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a queue.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
            >>>
            >>> response = client.get_queue(name)

        Args:
            name (str): Required.

                The resource name of the queue. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Queue` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_queue" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_queue"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_queue,
                default_retry=self._method_configs["GetQueue"].retry,
                default_timeout=self._method_configs["GetQueue"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.GetQueueRequest(name=name)
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

        return self._inner_api_calls["get_queue"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_queue(
        self,
        parent,
        queue,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a queue.

        Queues created with this method allow tasks to live for a maximum of 31
        days. After a task is 31 days old, the task will be deleted regardless
        of whether it was dispatched or not.

        WARNING: Using this method may have unintended side effects if you are
        using an App Engine ``queue.yaml`` or ``queue.xml`` file to manage your
        queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__ before
        using this method.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `queue`:
            >>> queue = {}
            >>>
            >>> response = client.create_queue(parent, queue)

        Args:
            parent (str): Required.

                The location name in which the queue will be created. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``

                The list of allowed locations can be obtained by calling Cloud Tasks'
                implementation of ``ListLocations``.
            queue (Union[dict, ~google.cloud.tasks_v2beta2.types.Queue]): Required.

                The queue to create.

                ``Queue's name`` cannot be the same as an existing queue.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.tasks_v2beta2.types.Queue`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Queue` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_queue" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_queue"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_queue,
                default_retry=self._method_configs["CreateQueue"].retry,
                default_timeout=self._method_configs["CreateQueue"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.CreateQueueRequest(parent=parent, queue=queue)
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

        return self._inner_api_calls["create_queue"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_queue(
        self,
        queue,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a queue.

        This method creates the queue if it does not exist and updates the queue
        if it does exist.

        Queues created with this method allow tasks to live for a maximum of 31
        days. After a task is 31 days old, the task will be deleted regardless
        of whether it was dispatched or not.

        WARNING: Using this method may have unintended side effects if you are
        using an App Engine ``queue.yaml`` or ``queue.xml`` file to manage your
        queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__ before
        using this method.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> # TODO: Initialize `queue`:
            >>> queue = {}
            >>>
            >>> response = client.update_queue(queue)

        Args:
            queue (Union[dict, ~google.cloud.tasks_v2beta2.types.Queue]): Required.

                The queue to create or update.

                The queue's ``name`` must be specified.

                Output only fields cannot be modified using UpdateQueue. Any value
                specified for an output only field will be ignored. The queue's ``name``
                cannot be changed.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.tasks_v2beta2.types.Queue`
            update_mask (Union[dict, ~google.cloud.tasks_v2beta2.types.FieldMask]): A mask used to specify which fields of the queue are being updated.

                If empty, then all fields will be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.tasks_v2beta2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Queue` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_queue" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_queue"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_queue,
                default_retry=self._method_configs["UpdateQueue"].retry,
                default_timeout=self._method_configs["UpdateQueue"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.UpdateQueueRequest(
            queue=queue, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("queue.name", queue.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_queue"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_queue(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a queue.

        This command will delete the queue even if it has tasks in it.

        Note: If you delete a queue, a queue with the same name can't be created
        for 7 days.

        WARNING: Using this method may have unintended side effects if you are
        using an App Engine ``queue.yaml`` or ``queue.xml`` file to manage your
        queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__ before
        using this method.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
            >>>
            >>> client.delete_queue(name)

        Args:
            name (str): Required.

                The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``
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
        if "delete_queue" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_queue"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_queue,
                default_retry=self._method_configs["DeleteQueue"].retry,
                default_timeout=self._method_configs["DeleteQueue"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.DeleteQueueRequest(name=name)
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

        self._inner_api_calls["delete_queue"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def purge_queue(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Purges a queue by deleting all of its tasks.

        All tasks created before this method is called are permanently deleted.

        Purge operations can take up to one minute to take effect. Tasks
        might be dispatched before the purge takes effect. A purge is irreversible.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
            >>>
            >>> response = client.purge_queue(name)

        Args:
            name (str): Required.

                The queue name. For example:
                ``projects/PROJECT_ID/location/LOCATION_ID/queues/QUEUE_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Queue` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "purge_queue" not in self._inner_api_calls:
            self._inner_api_calls[
                "purge_queue"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.purge_queue,
                default_retry=self._method_configs["PurgeQueue"].retry,
                default_timeout=self._method_configs["PurgeQueue"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.PurgeQueueRequest(name=name)
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

        return self._inner_api_calls["purge_queue"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def pause_queue(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Pauses the queue.

        If a queue is paused then the system will stop dispatching tasks until
        the queue is resumed via ``ResumeQueue``. Tasks can still be added when
        the queue is paused. A queue is paused if its ``state`` is ``PAUSED``.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
            >>>
            >>> response = client.pause_queue(name)

        Args:
            name (str): Required.

                The queue name. For example:
                ``projects/PROJECT_ID/location/LOCATION_ID/queues/QUEUE_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Queue` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "pause_queue" not in self._inner_api_calls:
            self._inner_api_calls[
                "pause_queue"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.pause_queue,
                default_retry=self._method_configs["PauseQueue"].retry,
                default_timeout=self._method_configs["PauseQueue"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.PauseQueueRequest(name=name)
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

        return self._inner_api_calls["pause_queue"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def resume_queue(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Resume a queue.

        This method resumes a queue after it has been ``PAUSED`` or
        ``DISABLED``. The state of a queue is stored in the queue's ``state``;
        after calling this method it will be set to ``RUNNING``.

        WARNING: Resuming many high-QPS queues at the same time can lead to
        target overloading. If you are resuming high-QPS queues, follow the
        500/50/5 pattern described in `Managing Cloud Tasks Scaling
        Risks <https://cloud.google.com/tasks/docs/manage-cloud-task-scaling>`__.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
            >>>
            >>> response = client.resume_queue(name)

        Args:
            name (str): Required.

                The queue name. For example:
                ``projects/PROJECT_ID/location/LOCATION_ID/queues/QUEUE_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Queue` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "resume_queue" not in self._inner_api_calls:
            self._inner_api_calls[
                "resume_queue"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.resume_queue,
                default_retry=self._method_configs["ResumeQueue"].retry,
                default_timeout=self._method_configs["ResumeQueue"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.ResumeQueueRequest(name=name)
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

        return self._inner_api_calls["resume_queue"](
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
        Gets the access control policy for a ``Queue``. Returns an empty policy
        if the resource exists and does not have a policy set.

        Authorization requires the following `Google
        IAM <https://cloud.google.com/iam>`__ permission on the specified
        resource parent:

        -  ``cloudtasks.queues.getIamPolicy``

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> resource = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
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
            A :class:`~google.cloud.tasks_v2beta2.types.Policy` instance.

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
        Sets the access control policy for a ``Queue``. Replaces any existing
        policy.

        Note: The Cloud Console does not check queue-level IAM permissions yet.
        Project-level permissions are required to use the Cloud Console.

        Authorization requires the following `Google
        IAM <https://cloud.google.com/iam>`__ permission on the specified
        resource parent:

        -  ``cloudtasks.queues.setIamPolicy``

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> resource = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            policy (Union[dict, ~google.cloud.tasks_v2beta2.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.tasks_v2beta2.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Policy` instance.

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
        Returns permissions that a caller has on a ``Queue``. If the resource
        does not exist, this will return an empty set of permissions, not a
        ``NOT_FOUND`` error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for authorization
        checking. This operation may "fail open" without warning.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> resource = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
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
            A :class:`~google.cloud.tasks_v2beta2.types.TestIamPermissionsResponse` instance.

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

    def list_tasks(
        self,
        parent,
        response_view=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the tasks in a queue.

        By default, only the ``BASIC`` view is retrieved due to performance
        considerations; ``response_view`` controls the subset of information
        which is returned.

        The tasks may be returned in any order. The ordering may change at any
        time.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> parent = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_tasks(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_tasks(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required.

                The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``
            response_view (~google.cloud.tasks_v2beta2.types.View): The response\_view specifies which subset of the ``Task`` will be
                returned.

                By default response\_view is ``BASIC``; not all information is retrieved
                by default because some data, such as payloads, might be desirable to
                return only when needed because of its large size or because of the
                sensitivity of data that it contains.

                Authorization for ``FULL`` requires ``cloudtasks.tasks.fullView``
                `Google IAM <https://cloud.google.com/iam/>`___ permission on the
                ``Task`` resource.
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
            is an iterable of :class:`~google.cloud.tasks_v2beta2.types.Task` instances.
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
        if "list_tasks" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_tasks"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_tasks,
                default_retry=self._method_configs["ListTasks"].retry,
                default_timeout=self._method_configs["ListTasks"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.ListTasksRequest(
            parent=parent, response_view=response_view, page_size=page_size
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
                self._inner_api_calls["list_tasks"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="tasks",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_task(
        self,
        name,
        response_view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a task.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.task_path('[PROJECT]', '[LOCATION]', '[QUEUE]', '[TASK]')
            >>>
            >>> response = client.get_task(name)

        Args:
            name (str): Required.

                The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``
            response_view (~google.cloud.tasks_v2beta2.types.View): The response\_view specifies which subset of the ``Task`` will be
                returned.

                By default response\_view is ``BASIC``; not all information is retrieved
                by default because some data, such as payloads, might be desirable to
                return only when needed because of its large size or because of the
                sensitivity of data that it contains.

                Authorization for ``FULL`` requires ``cloudtasks.tasks.fullView``
                `Google IAM <https://cloud.google.com/iam/>`___ permission on the
                ``Task`` resource.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Task` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_task" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_task"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_task,
                default_retry=self._method_configs["GetTask"].retry,
                default_timeout=self._method_configs["GetTask"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.GetTaskRequest(name=name, response_view=response_view)
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

        return self._inner_api_calls["get_task"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_task(
        self,
        parent,
        task,
        response_view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a task and adds it to a queue.

        Tasks cannot be updated after creation; there is no UpdateTask command.

        -  For ``App Engine queues``, the maximum task size is 100KB.
        -  For ``pull queues``, the maximum task size is 1MB.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> parent = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
            >>>
            >>> # TODO: Initialize `task`:
            >>> task = {}
            >>>
            >>> response = client.create_task(parent, task)

        Args:
            parent (str): Required.

                The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``

                The queue must already exist.
            task (Union[dict, ~google.cloud.tasks_v2beta2.types.Task]): Required.

                The task to add.

                Task names have the following format:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``.
                The user can optionally specify a task ``name``. If a name is not
                specified then the system will generate a random unique task id, which
                will be set in the task returned in the ``response``.

                If ``schedule_time`` is not set or is in the past then Cloud Tasks will
                set it to the current time.

                Task De-duplication:

                Explicitly specifying a task ID enables task de-duplication. If a task's
                ID is identical to that of an existing task or a task that was deleted
                or completed recently then the call will fail with ``ALREADY_EXISTS``.
                If the task's queue was created using Cloud Tasks, then another task
                with the same name can't be created for ~1hour after the original task
                was deleted or completed. If the task's queue was created using
                queue.yaml or queue.xml, then another task with the same name can't be
                created for ~9days after the original task was deleted or completed.

                Because there is an extra lookup cost to identify duplicate task names,
                these ``CreateTask`` calls have significantly increased latency. Using
                hashed strings for the task id or for the prefix of the task id is
                recommended. Choosing task ids that are sequential or have sequential
                prefixes, for example using a timestamp, causes an increase in latency
                and error rates in all task commands. The infrastructure relies on an
                approximately uniform distribution of task ids to store and serve tasks
                efficiently.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.tasks_v2beta2.types.Task`
            response_view (~google.cloud.tasks_v2beta2.types.View): The response\_view specifies which subset of the ``Task`` will be
                returned.

                By default response\_view is ``BASIC``; not all information is retrieved
                by default because some data, such as payloads, might be desirable to
                return only when needed because of its large size or because of the
                sensitivity of data that it contains.

                Authorization for ``FULL`` requires ``cloudtasks.tasks.fullView``
                `Google IAM <https://cloud.google.com/iam/>`___ permission on the
                ``Task`` resource.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Task` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_task" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_task"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_task,
                default_retry=self._method_configs["CreateTask"].retry,
                default_timeout=self._method_configs["CreateTask"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.CreateTaskRequest(
            parent=parent, task=task, response_view=response_view
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

        return self._inner_api_calls["create_task"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_task(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a task.

        A task can be deleted if it is scheduled or dispatched. A task
        cannot be deleted if it has completed successfully or permanently
        failed.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.task_path('[PROJECT]', '[LOCATION]', '[QUEUE]', '[TASK]')
            >>>
            >>> client.delete_task(name)

        Args:
            name (str): Required.

                The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``
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
        if "delete_task" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_task"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_task,
                default_retry=self._method_configs["DeleteTask"].retry,
                default_timeout=self._method_configs["DeleteTask"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.DeleteTaskRequest(name=name)
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

        self._inner_api_calls["delete_task"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def lease_tasks(
        self,
        parent,
        lease_duration,
        max_tasks=None,
        response_view=None,
        filter_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Leases tasks from a pull queue for ``lease_duration``.

        This method is invoked by the worker to obtain a lease. The worker must
        acknowledge the task via ``AcknowledgeTask`` after they have performed
        the work associated with the task.

        The ``payload`` is intended to store data that the worker needs to
        perform the work associated with the task. To return the payloads in the
        ``response``, set ``response_view`` to ``FULL``.

        A maximum of 10 qps of ``LeaseTasks`` requests are allowed per queue.
        ``RESOURCE_EXHAUSTED`` is returned when this limit is exceeded.
        ``RESOURCE_EXHAUSTED`` is also returned when
        ``max_tasks_dispatched_per_second`` is exceeded.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> parent = client.queue_path('[PROJECT]', '[LOCATION]', '[QUEUE]')
            >>>
            >>> # TODO: Initialize `lease_duration`:
            >>> lease_duration = {}
            >>>
            >>> response = client.lease_tasks(parent, lease_duration)

        Args:
            parent (str): Required.

                The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``
            lease_duration (Union[dict, ~google.cloud.tasks_v2beta2.types.Duration]): After the worker has successfully finished the work associated with the
                task, the worker must call via ``AcknowledgeTask`` before the
                ``schedule_time``. Otherwise the task will be returned to a later
                ``LeaseTasks`` call so that another worker can retry it.

                The maximum lease duration is 1 week. ``lease_duration`` will be
                truncated to the nearest second.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.tasks_v2beta2.types.Duration`
            max_tasks (int): The maximum number of tasks to lease.

                The system will make a best effort to return as close to as
                ``max_tasks`` as possible.

                The largest that ``max_tasks`` can be is 1000.
            response_view (~google.cloud.tasks_v2beta2.types.View): The response\_view specifies which subset of the ``Task`` will be
                returned.

                By default response\_view is ``BASIC``; not all information is retrieved
                by default because some data, such as payloads, might be desirable to
                return only when needed because of its large size or because of the
                sensitivity of data that it contains.

                Authorization for ``FULL`` requires ``cloudtasks.tasks.fullView``
                `Google IAM <https://cloud.google.com/iam/>`___ permission on the
                ``Task`` resource.
            filter_ (str): ``filter`` can be used to specify a subset of tasks to lease.

                When ``filter`` is set to ``tag=<my-tag>`` then the ``response`` will
                contain only tasks whose ``tag`` is equal to ``<my-tag>``. ``<my-tag>``
                must be less than 500 characters.

                When ``filter`` is set to ``tag_function=oldest_tag()``, only tasks
                which have the same tag as the task with the oldest ``schedule_time``
                will be returned.

                Grammar Syntax:

                -  ``filter = "tag=" tag | "tag_function=" function``

                -  ``tag = string``

                -  ``function = "oldest_tag()"``

                The ``oldest_tag()`` function returns tasks which have the same tag as
                the oldest task (ordered by schedule time).

                SDK compatibility: Although the SDK allows tags to be either string or
                `bytes <https://cloud.google.com/appengine/docs/standard/java/javadoc/com/google/appengine/api/taskqueue/TaskOptions.html#tag-byte:A->`__,
                only UTF-8 encoded tags can be used in Cloud Tasks. Tag which aren't
                UTF-8 encoded can't be used in the ``filter`` and the task's ``tag``
                will be displayed as empty in Cloud Tasks.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.LeaseTasksResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "lease_tasks" not in self._inner_api_calls:
            self._inner_api_calls[
                "lease_tasks"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.lease_tasks,
                default_retry=self._method_configs["LeaseTasks"].retry,
                default_timeout=self._method_configs["LeaseTasks"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.LeaseTasksRequest(
            parent=parent,
            lease_duration=lease_duration,
            max_tasks=max_tasks,
            response_view=response_view,
            filter=filter_,
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

        return self._inner_api_calls["lease_tasks"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def acknowledge_task(
        self,
        name,
        schedule_time,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Acknowledges a pull task.

        The worker, that is, the entity that ``leased`` this task must call this
        method to indicate that the work associated with the task has finished.

        The worker must acknowledge a task within the ``lease_duration`` or the
        lease will expire and the task will become available to be leased again.
        After the task is acknowledged, it will not be returned by a later
        ``LeaseTasks``, ``GetTask``, or ``ListTasks``.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.task_path('[PROJECT]', '[LOCATION]', '[QUEUE]', '[TASK]')
            >>>
            >>> # TODO: Initialize `schedule_time`:
            >>> schedule_time = {}
            >>>
            >>> client.acknowledge_task(name, schedule_time)

        Args:
            name (str): Required.

                The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``
            schedule_time (Union[dict, ~google.cloud.tasks_v2beta2.types.Timestamp]): Required.

                The task's current schedule time, available in the ``schedule_time``
                returned by ``LeaseTasks`` response or ``RenewLease`` response. This
                restriction is to ensure that your worker currently holds the lease.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.tasks_v2beta2.types.Timestamp`
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
        if "acknowledge_task" not in self._inner_api_calls:
            self._inner_api_calls[
                "acknowledge_task"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.acknowledge_task,
                default_retry=self._method_configs["AcknowledgeTask"].retry,
                default_timeout=self._method_configs["AcknowledgeTask"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.AcknowledgeTaskRequest(
            name=name, schedule_time=schedule_time
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

        self._inner_api_calls["acknowledge_task"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def renew_lease(
        self,
        name,
        schedule_time,
        lease_duration,
        response_view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Renew the current lease of a pull task.

        The worker can use this method to extend the lease by a new duration,
        starting from now. The new task lease will be returned in the task's
        ``schedule_time``.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.task_path('[PROJECT]', '[LOCATION]', '[QUEUE]', '[TASK]')
            >>>
            >>> # TODO: Initialize `schedule_time`:
            >>> schedule_time = {}
            >>>
            >>> # TODO: Initialize `lease_duration`:
            >>> lease_duration = {}
            >>>
            >>> response = client.renew_lease(name, schedule_time, lease_duration)

        Args:
            name (str): Required.

                The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``
            schedule_time (Union[dict, ~google.cloud.tasks_v2beta2.types.Timestamp]): Required.

                The task's current schedule time, available in the ``schedule_time``
                returned by ``LeaseTasks`` response or ``RenewLease`` response. This
                restriction is to ensure that your worker currently holds the lease.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.tasks_v2beta2.types.Timestamp`
            lease_duration (Union[dict, ~google.cloud.tasks_v2beta2.types.Duration]): Required.

                The desired new lease duration, starting from now.

                The maximum lease duration is 1 week. ``lease_duration`` will be
                truncated to the nearest second.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.tasks_v2beta2.types.Duration`
            response_view (~google.cloud.tasks_v2beta2.types.View): The response\_view specifies which subset of the ``Task`` will be
                returned.

                By default response\_view is ``BASIC``; not all information is retrieved
                by default because some data, such as payloads, might be desirable to
                return only when needed because of its large size or because of the
                sensitivity of data that it contains.

                Authorization for ``FULL`` requires ``cloudtasks.tasks.fullView``
                `Google IAM <https://cloud.google.com/iam/>`___ permission on the
                ``Task`` resource.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Task` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "renew_lease" not in self._inner_api_calls:
            self._inner_api_calls[
                "renew_lease"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.renew_lease,
                default_retry=self._method_configs["RenewLease"].retry,
                default_timeout=self._method_configs["RenewLease"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.RenewLeaseRequest(
            name=name,
            schedule_time=schedule_time,
            lease_duration=lease_duration,
            response_view=response_view,
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

        return self._inner_api_calls["renew_lease"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def cancel_lease(
        self,
        name,
        schedule_time,
        response_view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Cancel a pull task's lease.

        The worker can use this method to cancel a task's lease by setting its
        ``schedule_time`` to now. This will make the task available to be leased
        to the next caller of ``LeaseTasks``.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.task_path('[PROJECT]', '[LOCATION]', '[QUEUE]', '[TASK]')
            >>>
            >>> # TODO: Initialize `schedule_time`:
            >>> schedule_time = {}
            >>>
            >>> response = client.cancel_lease(name, schedule_time)

        Args:
            name (str): Required.

                The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``
            schedule_time (Union[dict, ~google.cloud.tasks_v2beta2.types.Timestamp]): Required.

                The task's current schedule time, available in the ``schedule_time``
                returned by ``LeaseTasks`` response or ``RenewLease`` response. This
                restriction is to ensure that your worker currently holds the lease.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.tasks_v2beta2.types.Timestamp`
            response_view (~google.cloud.tasks_v2beta2.types.View): The response\_view specifies which subset of the ``Task`` will be
                returned.

                By default response\_view is ``BASIC``; not all information is retrieved
                by default because some data, such as payloads, might be desirable to
                return only when needed because of its large size or because of the
                sensitivity of data that it contains.

                Authorization for ``FULL`` requires ``cloudtasks.tasks.fullView``
                `Google IAM <https://cloud.google.com/iam/>`___ permission on the
                ``Task`` resource.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Task` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "cancel_lease" not in self._inner_api_calls:
            self._inner_api_calls[
                "cancel_lease"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.cancel_lease,
                default_retry=self._method_configs["CancelLease"].retry,
                default_timeout=self._method_configs["CancelLease"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.CancelLeaseRequest(
            name=name, schedule_time=schedule_time, response_view=response_view
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

        return self._inner_api_calls["cancel_lease"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def run_task(
        self,
        name,
        response_view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Forces a task to run now.

        When this method is called, Cloud Tasks will dispatch the task, even if
        the task is already running, the queue has reached its ``RateLimits`` or
        is ``PAUSED``.

        This command is meant to be used for manual debugging. For example,
        ``RunTask`` can be used to retry a failed task after a fix has been made
        or to manually force a task to be dispatched now.

        The dispatched task is returned. That is, the task that is returned
        contains the ``status`` after the task is dispatched but before the task
        is received by its target.

        If Cloud Tasks receives a successful response from the task's target,
        then the task will be deleted; otherwise the task's ``schedule_time``
        will be reset to the time that ``RunTask`` was called plus the retry
        delay specified in the queue's ``RetryConfig``.

        ``RunTask`` returns ``NOT_FOUND`` when it is called on a task that has
        already succeeded or permanently failed.

        ``RunTask`` cannot be called on a ``pull task``.

        Example:
            >>> from google.cloud import tasks_v2beta2
            >>>
            >>> client = tasks_v2beta2.CloudTasksClient()
            >>>
            >>> name = client.task_path('[PROJECT]', '[LOCATION]', '[QUEUE]', '[TASK]')
            >>>
            >>> response = client.run_task(name)

        Args:
            name (str): Required.

                The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``
            response_view (~google.cloud.tasks_v2beta2.types.View): The response\_view specifies which subset of the ``Task`` will be
                returned.

                By default response\_view is ``BASIC``; not all information is retrieved
                by default because some data, such as payloads, might be desirable to
                return only when needed because of its large size or because of the
                sensitivity of data that it contains.

                Authorization for ``FULL`` requires ``cloudtasks.tasks.fullView``
                `Google IAM <https://cloud.google.com/iam/>`___ permission on the
                ``Task`` resource.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.tasks_v2beta2.types.Task` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "run_task" not in self._inner_api_calls:
            self._inner_api_calls[
                "run_task"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.run_task,
                default_retry=self._method_configs["RunTask"].retry,
                default_timeout=self._method_configs["RunTask"].timeout,
                client_info=self._client_info,
            )

        request = cloudtasks_pb2.RunTaskRequest(name=name, response_view=response_view)
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

        return self._inner_api_calls["run_task"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
