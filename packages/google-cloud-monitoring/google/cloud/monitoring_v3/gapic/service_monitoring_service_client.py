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

"""Accesses the google.monitoring.v3 ServiceMonitoringService API."""

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
import google.api_core.path_template
import grpc

from google.api import metric_pb2 as api_metric_pb2
from google.api import monitored_resource_pb2
from google.cloud.monitoring_v3.gapic import enums
from google.cloud.monitoring_v3.gapic import service_monitoring_service_client_config
from google.cloud.monitoring_v3.gapic.transports import (
    service_monitoring_service_grpc_transport,
)
from google.cloud.monitoring_v3.proto import alert_pb2
from google.cloud.monitoring_v3.proto import alert_service_pb2
from google.cloud.monitoring_v3.proto import alert_service_pb2_grpc
from google.cloud.monitoring_v3.proto import common_pb2
from google.cloud.monitoring_v3.proto import group_pb2
from google.cloud.monitoring_v3.proto import group_service_pb2
from google.cloud.monitoring_v3.proto import group_service_pb2_grpc
from google.cloud.monitoring_v3.proto import metric_pb2 as proto_metric_pb2
from google.cloud.monitoring_v3.proto import metric_service_pb2
from google.cloud.monitoring_v3.proto import metric_service_pb2_grpc
from google.cloud.monitoring_v3.proto import notification_pb2
from google.cloud.monitoring_v3.proto import notification_service_pb2
from google.cloud.monitoring_v3.proto import notification_service_pb2_grpc
from google.cloud.monitoring_v3.proto import service_pb2
from google.cloud.monitoring_v3.proto import service_service_pb2
from google.cloud.monitoring_v3.proto import service_service_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-monitoring"
).version


class ServiceMonitoringServiceClient(object):
    """
    The Cloud Monitoring Service-Oriented Monitoring API has endpoints
    for managing and querying aspects of a workspace's services. These
    include the ``Service``'s monitored resources, its Service-Level
    Objectives, and a taxonomy of categorized Health Metrics.
    """

    SERVICE_ADDRESS = "monitoring.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.monitoring.v3.ServiceMonitoringService"

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
            ServiceMonitoringServiceClient: The constructed client.
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
    def service_path(cls, project, service):
        """Return a fully-qualified service string."""
        return google.api_core.path_template.expand(
            "projects/{project}/services/{service}", project=project, service=service
        )

    @classmethod
    def service_level_objective_path(cls, project, service, service_level_objective):
        """Return a fully-qualified service_level_objective string."""
        return google.api_core.path_template.expand(
            "projects/{project}/services/{service}/serviceLevelObjectives/{service_level_objective}",
            project=project,
            service=service,
            service_level_objective=service_level_objective,
        )

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
            transport (Union[~.ServiceMonitoringServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.ServiceMonitoringServiceGrpcTransport]): A transport
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
            client_config = service_monitoring_service_client_config.config

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
                    default_class=service_monitoring_service_grpc_transport.ServiceMonitoringServiceGrpcTransport,
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
            self.transport = service_monitoring_service_grpc_transport.ServiceMonitoringServiceGrpcTransport(
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
    def create_service(
        self,
        parent,
        service,
        service_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Create a ``Service``.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.ServiceMonitoringServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `service`:
            >>> service = {}
            >>>
            >>> response = client.create_service(parent, service)

        Args:
            parent (str): Required. Resource name of the parent workspace. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]
            service (Union[dict, ~google.cloud.monitoring_v3.types.Service]): Required. The ``Service`` to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.Service`
            service_id (str): Optional. The Service id to use for this Service. If omitted, an id
                will be generated instead. Must match the pattern ``[a-z0-9\-]+``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.Service` instance.

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
        # Wrap the transport method to add retry and timeout logic.
        if "create_service" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_service"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_service,
                default_retry=self._method_configs["CreateService"].retry,
                default_timeout=self._method_configs["CreateService"].timeout,
                client_info=self._client_info,
            )

        request = service_service_pb2.CreateServiceRequest(
            parent=parent, service=service, service_id=service_id
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

        return self._inner_api_calls["create_service"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_service(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Get the named ``Service``.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.ServiceMonitoringServiceClient()
            >>>
            >>> name = client.service_path('[PROJECT]', '[SERVICE]')
            >>>
            >>> response = client.get_service(name)

        Args:
            name (str): Required. Resource name of the ``Service``. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.Service` instance.

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
        # Wrap the transport method to add retry and timeout logic.
        if "get_service" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_service"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_service,
                default_retry=self._method_configs["GetService"].retry,
                default_timeout=self._method_configs["GetService"].timeout,
                client_info=self._client_info,
            )

        request = service_service_pb2.GetServiceRequest(name=name)
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

        return self._inner_api_calls["get_service"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_services(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        List ``Service``\ s for this workspace.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.ServiceMonitoringServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_services(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_services(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Resource name of the parent containing the listed
                services, either a project or a Monitoring Workspace. The formats are:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]
                    workspaces/[HOST_PROJECT_ID_OR_NUMBER]
            filter_ (str): A filter specifying what ``Service``\ s to return. The filter
                currently supports the following fields:

                ::

                    - `identifier_case`
                    - `app_engine.module_id`
                    - `cloud_endpoints.service`
                    - `cluster_istio.location`
                    - `cluster_istio.cluster_name`
                    - `cluster_istio.service_namespace`
                    - `cluster_istio.service_name`

                ``identifier_case`` refers to which option in the identifier oneof is
                populated. For example, the filter ``identifier_case = "CUSTOM"`` would
                match all services with a value for the ``custom`` field. Valid options
                are "CUSTOM", "APP_ENGINE", "CLOUD_ENDPOINTS", and "CLUSTER_ISTIO".
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
            An iterable of :class:`~google.cloud.monitoring_v3.types.Service` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

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
        # Wrap the transport method to add retry and timeout logic.
        if "list_services" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_services"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_services,
                default_retry=self._method_configs["ListServices"].retry,
                default_timeout=self._method_configs["ListServices"].timeout,
                client_info=self._client_info,
            )

        request = service_service_pb2.ListServicesRequest(
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
                self._inner_api_calls["list_services"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="services",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_service(
        self,
        service,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Update this ``Service``.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.ServiceMonitoringServiceClient()
            >>>
            >>> # TODO: Initialize `service`:
            >>> service = {}
            >>>
            >>> response = client.update_service(service)

        Args:
            service (Union[dict, ~google.cloud.monitoring_v3.types.Service]): Required. The ``Service`` to draw updates from. The given ``name``
                specifies the resource to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.Service`
            update_mask (Union[dict, ~google.cloud.monitoring_v3.types.FieldMask]): A set of field paths defining which fields to use for the update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.Service` instance.

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
        # Wrap the transport method to add retry and timeout logic.
        if "update_service" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_service"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_service,
                default_retry=self._method_configs["UpdateService"].retry,
                default_timeout=self._method_configs["UpdateService"].timeout,
                client_info=self._client_info,
            )

        request = service_service_pb2.UpdateServiceRequest(
            service=service, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("service.name", service.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_service"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_service(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Soft delete this ``Service``.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.ServiceMonitoringServiceClient()
            >>>
            >>> name = client.service_path('[PROJECT]', '[SERVICE]')
            >>>
            >>> client.delete_service(name)

        Args:
            name (str): Required. Resource name of the ``Service`` to delete. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        # Wrap the transport method to add retry and timeout logic.
        if "delete_service" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_service"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_service,
                default_retry=self._method_configs["DeleteService"].retry,
                default_timeout=self._method_configs["DeleteService"].timeout,
                client_info=self._client_info,
            )

        request = service_service_pb2.DeleteServiceRequest(name=name)
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

        self._inner_api_calls["delete_service"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_service_level_objective(
        self,
        parent,
        service_level_objective,
        service_level_objective_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Create a ``ServiceLevelObjective`` for the given ``Service``.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.ServiceMonitoringServiceClient()
            >>>
            >>> parent = client.service_path('[PROJECT]', '[SERVICE]')
            >>>
            >>> # TODO: Initialize `service_level_objective`:
            >>> service_level_objective = {}
            >>>
            >>> response = client.create_service_level_objective(parent, service_level_objective)

        Args:
            parent (str): Required. Resource name of the parent ``Service``. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]
            service_level_objective (Union[dict, ~google.cloud.monitoring_v3.types.ServiceLevelObjective]): Required. The ``ServiceLevelObjective`` to create. The provided
                ``name`` will be respected if no ``ServiceLevelObjective`` exists with
                this name.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.ServiceLevelObjective`
            service_level_objective_id (str): Optional. The ServiceLevelObjective id to use for this
                ServiceLevelObjective. If omitted, an id will be generated instead. Must
                match the pattern ``[a-z0-9\-]+``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.ServiceLevelObjective` instance.

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
        # Wrap the transport method to add retry and timeout logic.
        if "create_service_level_objective" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_service_level_objective"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_service_level_objective,
                default_retry=self._method_configs["CreateServiceLevelObjective"].retry,
                default_timeout=self._method_configs[
                    "CreateServiceLevelObjective"
                ].timeout,
                client_info=self._client_info,
            )

        request = service_service_pb2.CreateServiceLevelObjectiveRequest(
            parent=parent,
            service_level_objective=service_level_objective,
            service_level_objective_id=service_level_objective_id,
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

        return self._inner_api_calls["create_service_level_objective"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_service_level_objective(
        self,
        name,
        view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Get a ``ServiceLevelObjective`` by name.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.ServiceMonitoringServiceClient()
            >>>
            >>> name = client.service_level_objective_path('[PROJECT]', '[SERVICE]', '[SERVICE_LEVEL_OBJECTIVE]')
            >>>
            >>> response = client.get_service_level_objective(name)

        Args:
            name (str): Required. Resource name of the ``ServiceLevelObjective`` to get. The
                format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]/serviceLevelObjectives/[SLO_NAME]
            view (~google.cloud.monitoring_v3.types.View): View of the ``ServiceLevelObjective`` to return. If ``DEFAULT``,
                return the ``ServiceLevelObjective`` as originally defined. If
                ``EXPLICIT`` and the ``ServiceLevelObjective`` is defined in terms of a
                ``BasicSli``, replace the ``BasicSli`` with a ``RequestBasedSli``
                spelling out how the SLI is computed.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.ServiceLevelObjective` instance.

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
        # Wrap the transport method to add retry and timeout logic.
        if "get_service_level_objective" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_service_level_objective"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_service_level_objective,
                default_retry=self._method_configs["GetServiceLevelObjective"].retry,
                default_timeout=self._method_configs[
                    "GetServiceLevelObjective"
                ].timeout,
                client_info=self._client_info,
            )

        request = service_service_pb2.GetServiceLevelObjectiveRequest(
            name=name, view=view
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

        return self._inner_api_calls["get_service_level_objective"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_service_level_objectives(
        self,
        parent,
        filter_=None,
        page_size=None,
        view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        List the ``ServiceLevelObjective``\ s for the given ``Service``.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.ServiceMonitoringServiceClient()
            >>>
            >>> parent = client.service_path('[PROJECT]', '[SERVICE]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_service_level_objectives(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_service_level_objectives(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Resource name of the parent containing the listed SLOs,
                either a project or a Monitoring Workspace. The formats are:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]
                    workspaces/[HOST_PROJECT_ID_OR_NUMBER]/services/-
            filter_ (str): A filter specifying what ``ServiceLevelObjective``\ s to return.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            view (~google.cloud.monitoring_v3.types.View): View of the ``ServiceLevelObjective``\ s to return. If ``DEFAULT``,
                return each ``ServiceLevelObjective`` as originally defined. If
                ``EXPLICIT`` and the ``ServiceLevelObjective`` is defined in terms of a
                ``BasicSli``, replace the ``BasicSli`` with a ``RequestBasedSli``
                spelling out how the SLI is computed.
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
            An iterable of :class:`~google.cloud.monitoring_v3.types.ServiceLevelObjective` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

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
        # Wrap the transport method to add retry and timeout logic.
        if "list_service_level_objectives" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_service_level_objectives"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_service_level_objectives,
                default_retry=self._method_configs["ListServiceLevelObjectives"].retry,
                default_timeout=self._method_configs[
                    "ListServiceLevelObjectives"
                ].timeout,
                client_info=self._client_info,
            )

        request = service_service_pb2.ListServiceLevelObjectivesRequest(
            parent=parent, filter=filter_, page_size=page_size, view=view
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
                self._inner_api_calls["list_service_level_objectives"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="service_level_objectives",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_service_level_objective(
        self,
        service_level_objective,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Update the given ``ServiceLevelObjective``.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.ServiceMonitoringServiceClient()
            >>>
            >>> # TODO: Initialize `service_level_objective`:
            >>> service_level_objective = {}
            >>>
            >>> response = client.update_service_level_objective(service_level_objective)

        Args:
            service_level_objective (Union[dict, ~google.cloud.monitoring_v3.types.ServiceLevelObjective]): Required. The ``ServiceLevelObjective`` to draw updates from. The
                given ``name`` specifies the resource to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.ServiceLevelObjective`
            update_mask (Union[dict, ~google.cloud.monitoring_v3.types.FieldMask]): A set of field paths defining which fields to use for the update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.ServiceLevelObjective` instance.

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
        # Wrap the transport method to add retry and timeout logic.
        if "update_service_level_objective" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_service_level_objective"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_service_level_objective,
                default_retry=self._method_configs["UpdateServiceLevelObjective"].retry,
                default_timeout=self._method_configs[
                    "UpdateServiceLevelObjective"
                ].timeout,
                client_info=self._client_info,
            )

        request = service_service_pb2.UpdateServiceLevelObjectiveRequest(
            service_level_objective=service_level_objective, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [
                ("service_level_objective.name", service_level_objective.name)
            ]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_service_level_objective"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_service_level_objective(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Delete the given ``ServiceLevelObjective``.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.ServiceMonitoringServiceClient()
            >>>
            >>> name = client.service_level_objective_path('[PROJECT]', '[SERVICE]', '[SERVICE_LEVEL_OBJECTIVE]')
            >>>
            >>> client.delete_service_level_objective(name)

        Args:
            name (str): Required. Resource name of the ``ServiceLevelObjective`` to delete.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]/serviceLevelObjectives/[SLO_NAME]
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        # Wrap the transport method to add retry and timeout logic.
        if "delete_service_level_objective" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_service_level_objective"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_service_level_objective,
                default_retry=self._method_configs["DeleteServiceLevelObjective"].retry,
                default_timeout=self._method_configs[
                    "DeleteServiceLevelObjective"
                ].timeout,
                client_info=self._client_info,
            )

        request = service_service_pb2.DeleteServiceLevelObjectiveRequest(name=name)
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

        self._inner_api_calls["delete_service_level_objective"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
