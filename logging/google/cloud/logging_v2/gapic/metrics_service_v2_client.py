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
"""Accesses the google.logging.v2 MetricsServiceV2 API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template

from google.api import monitored_resource_pb2
from google.cloud.logging_v2.gapic import enums
from google.cloud.logging_v2.gapic import metrics_service_v2_client_config
from google.cloud.logging_v2.proto import log_entry_pb2
from google.cloud.logging_v2.proto import logging_config_pb2
from google.cloud.logging_v2.proto import logging_metrics_pb2
from google.cloud.logging_v2.proto import logging_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-logging', ).version


class MetricsServiceV2Client(object):
    """Service for configuring logs-based metrics."""

    SERVICE_ADDRESS = 'logging.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/cloud-platform.read-only',
        'https://www.googleapis.com/auth/logging.admin',
        'https://www.googleapis.com/auth/logging.read',
        'https://www.googleapis.com/auth/logging.write',
    )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.logging.v2.MetricsServiceV2'

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project,
        )

    @classmethod
    def metric_path(cls, project, metric):
        """Return a fully-qualified metric string."""
        return google.api_core.path_template.expand(
            'projects/{project}/metrics/{metric}',
            project=project,
            metric=metric,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=metrics_service_v2_client_config.config,
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
        self.metrics_service_v2_stub = (
            logging_metrics_pb2.MetricsServiceV2Stub(channel))

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
        self._list_log_metrics = google.api_core.gapic_v1.method.wrap_method(
            self.metrics_service_v2_stub.ListLogMetrics,
            default_retry=method_configs['ListLogMetrics'].retry,
            default_timeout=method_configs['ListLogMetrics'].timeout,
            client_info=client_info,
        )
        self._get_log_metric = google.api_core.gapic_v1.method.wrap_method(
            self.metrics_service_v2_stub.GetLogMetric,
            default_retry=method_configs['GetLogMetric'].retry,
            default_timeout=method_configs['GetLogMetric'].timeout,
            client_info=client_info,
        )
        self._create_log_metric = google.api_core.gapic_v1.method.wrap_method(
            self.metrics_service_v2_stub.CreateLogMetric,
            default_retry=method_configs['CreateLogMetric'].retry,
            default_timeout=method_configs['CreateLogMetric'].timeout,
            client_info=client_info,
        )
        self._update_log_metric = google.api_core.gapic_v1.method.wrap_method(
            self.metrics_service_v2_stub.UpdateLogMetric,
            default_retry=method_configs['UpdateLogMetric'].retry,
            default_timeout=method_configs['UpdateLogMetric'].timeout,
            client_info=client_info,
        )
        self._delete_log_metric = google.api_core.gapic_v1.method.wrap_method(
            self.metrics_service_v2_stub.DeleteLogMetric,
            default_retry=method_configs['DeleteLogMetric'].retry,
            default_timeout=method_configs['DeleteLogMetric'].timeout,
            client_info=client_info,
        )

    # Service calls
    def list_log_metrics(self,
                         parent,
                         page_size=None,
                         retry=google.api_core.gapic_v1.method.DEFAULT,
                         timeout=google.api_core.gapic_v1.method.DEFAULT,
                         metadata=None):
        """
        Lists logs-based metrics.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.MetricsServiceV2Client()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_log_metrics(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_log_metrics(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The name of the project containing the metrics:

                ::

                    \"projects/[PROJECT_ID]\"
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
            is an iterable of :class:`~google.cloud.logging_v2.types.LogMetric` instances.
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
        request = logging_metrics_pb2.ListLogMetricsRequest(
            parent=parent,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_log_metrics,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='metrics',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_log_metric(self,
                       metric_name,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Gets a logs-based metric.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.MetricsServiceV2Client()
            >>>
            >>> metric_name = client.metric_path('[PROJECT]', '[METRIC]')
            >>>
            >>> response = client.get_log_metric(metric_name)

        Args:
            metric_name (str): The resource name of the desired metric:

                ::

                    \"projects/[PROJECT_ID]/metrics/[METRIC_ID]\"
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.logging_v2.types.LogMetric` instance.

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
        request = logging_metrics_pb2.GetLogMetricRequest(
            metric_name=metric_name, )
        return self._get_log_metric(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_log_metric(self,
                          parent,
                          metric,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT,
                          metadata=None):
        """
        Creates a logs-based metric.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.MetricsServiceV2Client()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>> metric = {}
            >>>
            >>> response = client.create_log_metric(parent, metric)

        Args:
            parent (str): The resource name of the project in which to create the metric:

                ::

                    \"projects/[PROJECT_ID]\"

                The new metric must be provided in the request.
            metric (Union[dict, ~google.cloud.logging_v2.types.LogMetric]): The new logs-based metric, which must not have an identifier that
                already exists.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.logging_v2.types.LogMetric`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.logging_v2.types.LogMetric` instance.

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
        request = logging_metrics_pb2.CreateLogMetricRequest(
            parent=parent,
            metric=metric,
        )
        return self._create_log_metric(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_log_metric(self,
                          metric_name,
                          metric,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT,
                          metadata=None):
        """
        Creates or updates a logs-based metric.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.MetricsServiceV2Client()
            >>>
            >>> metric_name = client.metric_path('[PROJECT]', '[METRIC]')
            >>> metric = {}
            >>>
            >>> response = client.update_log_metric(metric_name, metric)

        Args:
            metric_name (str): The resource name of the metric to update:

                ::

                    \"projects/[PROJECT_ID]/metrics/[METRIC_ID]\"

                The updated metric must be provided in the request and it's
                ``name`` field must be the same as ``[METRIC_ID]`` If the metric
                does not exist in ``[PROJECT_ID]``, then a new metric is created.
            metric (Union[dict, ~google.cloud.logging_v2.types.LogMetric]): The updated metric.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.logging_v2.types.LogMetric`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.logging_v2.types.LogMetric` instance.

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
        request = logging_metrics_pb2.UpdateLogMetricRequest(
            metric_name=metric_name,
            metric=metric,
        )
        return self._update_log_metric(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_log_metric(self,
                          metric_name,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT,
                          metadata=None):
        """
        Deletes a logs-based metric.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.MetricsServiceV2Client()
            >>>
            >>> metric_name = client.metric_path('[PROJECT]', '[METRIC]')
            >>>
            >>> client.delete_log_metric(metric_name)

        Args:
            metric_name (str): The resource name of the metric to delete:

                ::

                    \"projects/[PROJECT_ID]/metrics/[METRIC_ID]\"
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
        request = logging_metrics_pb2.DeleteLogMetricRequest(
            metric_name=metric_name, )
        self._delete_log_metric(
            request, retry=retry, timeout=timeout, metadata=metadata)
