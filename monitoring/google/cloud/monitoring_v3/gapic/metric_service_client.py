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
"""Accesses the google.monitoring.v3 MetricService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.api import metric_pb2 as api_metric_pb2
from google.api import monitored_resource_pb2
from google.cloud.monitoring_v3.gapic import enums
from google.cloud.monitoring_v3.gapic import metric_service_client_config
from google.cloud.monitoring_v3.gapic.transports import metric_service_grpc_transport
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
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-monitoring"
).version


class MetricServiceClient(object):
    """
    Manages metric descriptors, monitored resource descriptors, and
    time series data.
    """

    SERVICE_ADDRESS = "monitoring.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.monitoring.v3.MetricService"

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
            MetricServiceClient: The constructed client.
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
    def metric_descriptor_path(cls, project, metric_descriptor):
        """Return a fully-qualified metric_descriptor string."""
        return google.api_core.path_template.expand(
            "projects/{project}/metricDescriptors/{metric_descriptor=**}",
            project=project,
            metric_descriptor=metric_descriptor,
        )

    @classmethod
    def monitored_resource_descriptor_path(cls, project, monitored_resource_descriptor):
        """Return a fully-qualified monitored_resource_descriptor string."""
        return google.api_core.path_template.expand(
            "projects/{project}/monitoredResourceDescriptors/{monitored_resource_descriptor}",
            project=project,
            monitored_resource_descriptor=monitored_resource_descriptor,
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
            transport (Union[~.MetricServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.MetricServiceGrpcTransport]): A transport
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
            client_config = metric_service_client_config.config

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
                    default_class=metric_service_grpc_transport.MetricServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = metric_service_grpc_transport.MetricServiceGrpcTransport(
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
    def list_monitored_resource_descriptors(
        self,
        name,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists monitored resource descriptors that match a filter. This method does not require a Stackdriver account.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.MetricServiceClient()
            >>>
            >>> name = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_monitored_resource_descriptors(name):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_monitored_resource_descriptors(name).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            name (str): The project on which to execute the request. The format is
                ``"projects/{project_id_or_number}"``.
            filter_ (str): An optional
                `filter <https://cloud.google.com/monitoring/api/v3/filters>`__
                describing the descriptors to be returned. The filter can reference the
                descriptor's type and labels. For example, the following filter returns
                only Google Compute Engine descriptors that have an ``id`` label:

                ::

                     resource.type = starts_with("gce_") AND resource.label:id
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
            is an iterable of :class:`~google.cloud.monitoring_v3.types.MonitoredResourceDescriptor` instances.
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
        # Wrap the transport method to add retry and timeout logic.
        if "list_monitored_resource_descriptors" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_monitored_resource_descriptors"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_monitored_resource_descriptors,
                default_retry=self._method_configs[
                    "ListMonitoredResourceDescriptors"
                ].retry,
                default_timeout=self._method_configs[
                    "ListMonitoredResourceDescriptors"
                ].timeout,
                client_info=self._client_info,
            )

        request = metric_service_pb2.ListMonitoredResourceDescriptorsRequest(
            name=name, filter=filter_, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_monitored_resource_descriptors"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="resource_descriptors",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_monitored_resource_descriptor(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a single monitored resource descriptor. This method does not require a Stackdriver account.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.MetricServiceClient()
            >>>
            >>> name = client.monitored_resource_descriptor_path('[PROJECT]', '[MONITORED_RESOURCE_DESCRIPTOR]')
            >>>
            >>> response = client.get_monitored_resource_descriptor(name)

        Args:
            name (str): The monitored resource descriptor to get. The format is
                ``"projects/{project_id_or_number}/monitoredResourceDescriptors/{resource_type}"``.
                The ``{resource_type}`` is a predefined type, such as
                ``cloudsql_database``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.MonitoredResourceDescriptor` instance.

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
        if "get_monitored_resource_descriptor" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_monitored_resource_descriptor"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_monitored_resource_descriptor,
                default_retry=self._method_configs[
                    "GetMonitoredResourceDescriptor"
                ].retry,
                default_timeout=self._method_configs[
                    "GetMonitoredResourceDescriptor"
                ].timeout,
                client_info=self._client_info,
            )

        request = metric_service_pb2.GetMonitoredResourceDescriptorRequest(name=name)
        return self._inner_api_calls["get_monitored_resource_descriptor"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_metric_descriptors(
        self,
        name,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists metric descriptors that match a filter. This method does not require a Stackdriver account.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.MetricServiceClient()
            >>>
            >>> name = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_metric_descriptors(name):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_metric_descriptors(name).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            name (str): The project on which to execute the request. The format is
                ``"projects/{project_id_or_number}"``.
            filter_ (str): If this field is empty, all custom and system-defined metric descriptors
                are returned. Otherwise, the
                `filter <https://cloud.google.com/monitoring/api/v3/filters>`__
                specifies which metric descriptors are to be returned. For example, the
                following filter matches all `custom
                metrics <https://cloud.google.com/monitoring/custom-metrics>`__:

                ::

                     metric.type = starts_with("custom.googleapis.com/")
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
            is an iterable of :class:`~google.cloud.monitoring_v3.types.MetricDescriptor` instances.
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
        # Wrap the transport method to add retry and timeout logic.
        if "list_metric_descriptors" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_metric_descriptors"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_metric_descriptors,
                default_retry=self._method_configs["ListMetricDescriptors"].retry,
                default_timeout=self._method_configs["ListMetricDescriptors"].timeout,
                client_info=self._client_info,
            )

        request = metric_service_pb2.ListMetricDescriptorsRequest(
            name=name, filter=filter_, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_metric_descriptors"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="metric_descriptors",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_metric_descriptor(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a single metric descriptor. This method does not require a Stackdriver account.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.MetricServiceClient()
            >>>
            >>> name = client.metric_descriptor_path('[PROJECT]', '[METRIC_DESCRIPTOR]')
            >>>
            >>> response = client.get_metric_descriptor(name)

        Args:
            name (str): The metric descriptor on which to execute the request. The format is
                ``"projects/{project_id_or_number}/metricDescriptors/{metric_id}"``. An
                example value of ``{metric_id}`` is
                ``"compute.googleapis.com/instance/disk/read_bytes_count"``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.MetricDescriptor` instance.

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
        if "get_metric_descriptor" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_metric_descriptor"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_metric_descriptor,
                default_retry=self._method_configs["GetMetricDescriptor"].retry,
                default_timeout=self._method_configs["GetMetricDescriptor"].timeout,
                client_info=self._client_info,
            )

        request = metric_service_pb2.GetMetricDescriptorRequest(name=name)
        return self._inner_api_calls["get_metric_descriptor"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_metric_descriptor(
        self,
        name,
        metric_descriptor,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new metric descriptor. User-created metric descriptors define
        `custom metrics <https://cloud.google.com/monitoring/custom-metrics>`__.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.MetricServiceClient()
            >>>
            >>> name = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `metric_descriptor`:
            >>> metric_descriptor = {}
            >>>
            >>> response = client.create_metric_descriptor(name, metric_descriptor)

        Args:
            name (str): The project on which to execute the request. The format is
                ``"projects/{project_id_or_number}"``.
            metric_descriptor (Union[dict, ~google.cloud.monitoring_v3.types.MetricDescriptor]): The new `custom
                metric <https://cloud.google.com/monitoring/custom-metrics>`__
                descriptor.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.MetricDescriptor`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.MetricDescriptor` instance.

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
        if "create_metric_descriptor" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_metric_descriptor"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_metric_descriptor,
                default_retry=self._method_configs["CreateMetricDescriptor"].retry,
                default_timeout=self._method_configs["CreateMetricDescriptor"].timeout,
                client_info=self._client_info,
            )

        request = metric_service_pb2.CreateMetricDescriptorRequest(
            name=name, metric_descriptor=metric_descriptor
        )
        return self._inner_api_calls["create_metric_descriptor"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_metric_descriptor(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a metric descriptor. Only user-created `custom
        metrics <https://cloud.google.com/monitoring/custom-metrics>`__ can be
        deleted.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.MetricServiceClient()
            >>>
            >>> name = client.metric_descriptor_path('[PROJECT]', '[METRIC_DESCRIPTOR]')
            >>>
            >>> client.delete_metric_descriptor(name)

        Args:
            name (str): The metric descriptor on which to execute the request. The format is
                ``"projects/{project_id_or_number}/metricDescriptors/{metric_id}"``. An
                example of ``{metric_id}`` is:
                ``"custom.googleapis.com/my_test_metric"``.
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
        # Wrap the transport method to add retry and timeout logic.
        if "delete_metric_descriptor" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_metric_descriptor"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_metric_descriptor,
                default_retry=self._method_configs["DeleteMetricDescriptor"].retry,
                default_timeout=self._method_configs["DeleteMetricDescriptor"].timeout,
                client_info=self._client_info,
            )

        request = metric_service_pb2.DeleteMetricDescriptorRequest(name=name)
        self._inner_api_calls["delete_metric_descriptor"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_time_series(
        self,
        name,
        filter_,
        interval,
        view,
        aggregation=None,
        order_by=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists time series that match a filter. This method does not require a Stackdriver account.

        Example:
            >>> from google.cloud import monitoring_v3
            >>> from google.cloud.monitoring_v3 import enums
            >>>
            >>> client = monitoring_v3.MetricServiceClient()
            >>>
            >>> name = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `filter_`:
            >>> filter_ = ''
            >>>
            >>> # TODO: Initialize `interval`:
            >>> interval = {}
            >>>
            >>> # TODO: Initialize `view`:
            >>> view = enums.ListTimeSeriesRequest.TimeSeriesView.FULL
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_time_series(name, filter_, interval, view):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_time_series(name, filter_, interval, view).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            name (str): The project on which to execute the request. The format is
                "projects/{project\_id\_or\_number}".
            filter_ (str): A `monitoring
                filter <https://cloud.google.com/monitoring/api/v3/filters>`__ that
                specifies which time series should be returned. The filter must specify
                a single metric type, and can additionally specify metric labels and
                other information. For example:

                ::

                     metric.type = "compute.googleapis.com/instance/cpu/usage_time" AND
                         metric.label.instance_name = "my-instance-name"
            interval (Union[dict, ~google.cloud.monitoring_v3.types.TimeInterval]): The time interval for which results should be returned. Only time series
                that contain data points in the specified interval are included
                in the response.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.TimeInterval`
            view (~google.cloud.monitoring_v3.types.TimeSeriesView): Specifies which information is returned about the time series.
            aggregation (Union[dict, ~google.cloud.monitoring_v3.types.Aggregation]): By default, the raw time series data is returned.
                Use this field to combine multiple time series for different
                views of the data.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.Aggregation`
            order_by (str): Unsupported: must be left blank. The points in each time series are
                returned in reverse time order.
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
            is an iterable of :class:`~google.cloud.monitoring_v3.types.TimeSeries` instances.
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
        # Wrap the transport method to add retry and timeout logic.
        if "list_time_series" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_time_series"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_time_series,
                default_retry=self._method_configs["ListTimeSeries"].retry,
                default_timeout=self._method_configs["ListTimeSeries"].timeout,
                client_info=self._client_info,
            )

        request = metric_service_pb2.ListTimeSeriesRequest(
            name=name,
            filter=filter_,
            interval=interval,
            view=view,
            aggregation=aggregation,
            order_by=order_by,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_time_series"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="time_series",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_time_series(
        self,
        name,
        time_series,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates or adds data to one or more time series.
        The response is empty if all time series in the request were written.
        If any time series could not be written, a corresponding failure message is
        included in the error response.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.MetricServiceClient()
            >>>
            >>> name = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `time_series`:
            >>> time_series = []
            >>>
            >>> client.create_time_series(name, time_series)

        Args:
            name (str): The project on which to execute the request. The format is
                ``"projects/{project_id_or_number}"``.
            time_series (list[Union[dict, ~google.cloud.monitoring_v3.types.TimeSeries]]): The new data to be added to a list of time series. Adds at most one data
                point to each of several time series. The new data point must be more
                recent than any other point in its time series. Each ``TimeSeries``
                value must fully specify a unique time series by supplying all label
                values for the metric and the monitored resource.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.TimeSeries`
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
        # Wrap the transport method to add retry and timeout logic.
        if "create_time_series" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_time_series"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_time_series,
                default_retry=self._method_configs["CreateTimeSeries"].retry,
                default_timeout=self._method_configs["CreateTimeSeries"].timeout,
                client_info=self._client_info,
            )

        request = metric_service_pb2.CreateTimeSeriesRequest(
            name=name, time_series=time_series
        )
        self._inner_api_calls["create_time_series"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
