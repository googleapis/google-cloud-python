# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/logging/v2/logging_metrics.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.logging.v2 MetricsServiceV2 API."""

import json
import os
import pkg_resources
import platform

from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.logging.v2 import logging_metrics_pb2

_PageDesc = google.gax.PageDescriptor


class MetricsServiceV2Api(object):
    SERVICE_ADDRESS = 'logging.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    _CODE_GEN_NAME_VERSION = 'gapic/0.1.0'

    _GAX_VERSION = pkg_resources.get_distribution('google-gax').version

    _DEFAULT_TIMEOUT = 30

    _PAGE_DESCRIPTORS = {
        'list_log_metrics': _PageDesc('page_token', 'next_page_token',
                                      'metrics')
    }

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = ('https://www.googleapis.com/auth/logging.write',
                   'https://www.googleapis.com/auth/logging.admin',
                   'https://www.googleapis.com/auth/logging.read',
                   'https://www.googleapis.com/auth/cloud-platform.read-only',
                   'https://www.googleapis.com/auth/cloud-platform', )

    _PROJECT_PATH_TEMPLATE = path_template.PathTemplate('projects/{project}')
    _METRIC_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/metrics/{metric}')

    @classmethod
    def project_path(cls, project):
        """Returns a fully-qualified project resource name string."""
        return cls._PROJECT_PATH_TEMPLATE.instantiate({'project': project, })

    @classmethod
    def metric_path(cls, project, metric):
        """Returns a fully-qualified metric resource name string."""
        return cls._METRIC_PATH_TEMPLATE.instantiate({
            'project': project,
            'metric': metric,
        })

    def __init__(self,
                 service_path=SERVICE_ADDRESS,
                 port=DEFAULT_SERVICE_PORT,
                 channel=None,
                 ssl_creds=None,
                 scopes=None,
                 retrying_override=None,
                 bundling_override=None,
                 timeout=_DEFAULT_TIMEOUT,
                 app_name='gax',
                 app_version=_GAX_VERSION):
        """Constructor.

        Args:
          service_path (string): The domain name of the API remote host.
          port (int): The port on which to connect to the remote host.
          channel (:class:`grpc.beta.implementations.Channel`): A ``Channel``
            object through which to make calls.
          ssl_creds (:class:`grpc.beta.implementations.ClientCredentials`):
            A `ClientCredentials` for use with an SSL-enabled channel.
          retrying_override (dict[string, :class:`google.gax.RetryOptions`]): A
            dictionary that overrides default retrying settings.
            ``retrying_override`` maps method names (e.g., ``'list_foo'``) to
            custom RetryOptions objects, or to None. A value of None indicates
            that the method in question should not retry.
          bundling_override (dict[string, :class:`google.gax.BundleOptions`]): A
            dictionary that overrides default bundling settings.
            ``bundling_override`` maps bundling method names (e.g.,
            'publish_foo') to custom BundleOptions objects, or to None. It is
            invalid to have a key for a method that is not bundling-enabled. A
            value of None indicates that the method in question should not
            bundle.
          timeout (int): The default timeout, in seconds, for calls made
            through this client
          app_name (string): The codename of the calling service.
          app_version (string): The version of the calling service.

        Returns:
          A MetricsServiceV2Api object.
        """
        if scopes is None:
            scopes = self._ALL_SCOPES
        bundling_override = bundling_override or {}
        retrying_override = retrying_override or {}
        client_config = pkg_resources.resource_string(
            __name__, 'metrics_service_v2_client_config.json')
        self._defaults = api_callable.construct_settings(
            'google.logging.v2.MetricsServiceV2',
            json.loads(client_config),
            bundling_override,
            retrying_override,
            config.STATUS_CODE_NAMES,
            timeout,
            page_descriptors=self._PAGE_DESCRIPTORS)
        google_apis_agent = '{}/{};{};gax/{};python/{}'.format(
            app_name, app_version, self._CODE_GEN_NAME_VERSION,
            self._GAX_VERSION, platform.python_version())
        self._headers = [('x-google-apis-agent', google_apis_agent)]
        self.stub = config.create_stub(
            logging_metrics_pb2.beta_create_MetricsServiceV2_stub,
            service_path,
            port,
            ssl_creds=ssl_creds,
            channel=channel,
            scopes=scopes)

    # Service calls
    def list_log_metrics(self, project_name='', options=None):
        """
        Lists logs-based metrics.

        Args:
          project_name (string): Required. The resource name of the project containing the metrics.
            Example: `"projects/my-project-id"`.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Yields:
          Instances of :class:`google.logging.v2.logging_metrics_pb2.LogMetric`
          unless page streaming is disabled through the call options. If
          page streaming is disabled, a single
          :class:`google.logging.v2.logging_metrics_pb2.ListLogMetricsResponse` instance
          is returned.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        req = logging_metrics_pb2.ListLogMetricsRequest(
            project_name=project_name)
        settings = self._defaults['list_log_metrics'].merge(options)
        api_call = api_callable.create_api_call(self.stub.ListLogMetrics,
                                                settings=settings)
        return api_call(req, metadata=self._headers)

    def get_log_metric(self, metric_name='', options=None):
        """
        Gets a logs-based metric.

        Args:
          metric_name (string): The resource name of the desired metric.
            Example: `"projects/my-project-id/metrics/my-metric-id"`.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.logging.v2.logging_metrics_pb2.LogMetric` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        req = logging_metrics_pb2.GetLogMetricRequest(metric_name=metric_name)
        settings = self._defaults['get_log_metric'].merge(options)
        api_call = api_callable.create_api_call(self.stub.GetLogMetric,
                                                settings=settings)
        return api_call(req, metadata=self._headers)

    def create_log_metric(self, project_name='', metric=None, options=None):
        """
        Creates a logs-based metric.

        Args:
          project_name (string): The resource name of the project in which to create the metric.
            Example: `"projects/my-project-id"`.

            The new metric must be provided in the request.
          metric (:class:`google.logging.v2.logging_metrics_pb2.LogMetric`): The new logs-based metric, which must not have an identifier that
            already exists.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.logging.v2.logging_metrics_pb2.LogMetric` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        if metric is None:
            metric = logging_metrics_pb2.LogMetric()
        req = logging_metrics_pb2.CreateLogMetricRequest(
            project_name=project_name,
            metric=metric)
        settings = self._defaults['create_log_metric'].merge(options)
        api_call = api_callable.create_api_call(self.stub.CreateLogMetric,
                                                settings=settings)
        return api_call(req, metadata=self._headers)

    def update_log_metric(self, metric_name='', metric=None, options=None):
        """
        Creates or updates a logs-based metric.

        Args:
          metric_name (string): The resource name of the metric to update.
            Example: `"projects/my-project-id/metrics/my-metric-id"`.

            The updated metric must be provided in the request and have the
            same identifier that is specified in `metricName`.
            If the metric does not exist, it is created.
          metric (:class:`google.logging.v2.logging_metrics_pb2.LogMetric`): The updated metric, whose name must be the same as the
            metric identifier in `metricName`. If `metricName` does not
            exist, then a new metric is created.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.logging.v2.logging_metrics_pb2.LogMetric` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        if metric is None:
            metric = logging_metrics_pb2.LogMetric()
        req = logging_metrics_pb2.UpdateLogMetricRequest(
            metric_name=metric_name,
            metric=metric)
        settings = self._defaults['update_log_metric'].merge(options)
        api_call = api_callable.create_api_call(self.stub.UpdateLogMetric,
                                                settings=settings)
        return api_call(req, metadata=self._headers)

    def delete_log_metric(self, metric_name='', options=None):
        """
        Deletes a logs-based metric.

        Args:
          metric_name (string): The resource name of the metric to delete.
            Example: `"projects/my-project-id/metrics/my-metric-id"`.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        req = logging_metrics_pb2.DeleteLogMetricRequest(
            metric_name=metric_name)
        settings = self._defaults['delete_log_metric'].merge(options)
        api_call = api_callable.create_api_call(self.stub.DeleteLogMetric,
                                                settings=settings)
        api_call(req, metadata=self._headers)
