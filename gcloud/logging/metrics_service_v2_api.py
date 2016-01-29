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
# https://github.com/google/googleapis/blob/7710ead495227e80a0f06ceb66bdf3238d926f77/google/logging/v2/logging_metrics.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
# Manual additions are allowed because the refresh process performs
# a 3-way merge in order to preserve those manual additions. In order to not
# break the refresh process, only certain types of modifications are
# allowed.
#
# Allowed modifications:
# 1. New methods (these should be added to the end of the class)
#
# Happy editing!

from google.gax import api_callable
from google.gax import api_utils
from google.gax import page_descriptor
from google.logging.v2 import logging_metrics_pb2


class MetricsServiceV2Api(object):

    # The default address of the logging service.
    _SERVICE_ADDRESS = 'logging.googleapis.com'

    # The default port of the logging service.
    _DEFAULT_SERVICE_PORT = 443

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = (
        'https://www.googleapis.com/auth/logging.write',
        'https://www.googleapis.com/auth/logging.admin',
        'https://www.googleapis.com/auth/logging.read',
        'https://www.googleapis.com/auth/cloud-platform.read-only',
        'https://www.googleapis.com/auth/cloud-platform',
    )

    _LIST_LOG_METRICS_DESCRIPTOR = page_descriptor.PageDescriptor(
        'page_token',
        'next_page_token',
        'metrics',
    )

    def __init__(
            self,
            service_path=_SERVICE_ADDRESS,
            port=_DEFAULT_SERVICE_PORT,
            channel=None,
            ssl_creds=None,
            scopes=_ALL_SCOPES,
            is_idempotent_retrying=True,
            max_attempts=3,
            timeout=30):
        self.defaults = api_callable.ApiCallableDefaults(
            timeout=timeout,
            max_attempts=max_attempts,
            is_idempotent_retrying=is_idempotent_retrying)
        self.stub = api_utils.create_stub(
            logging_metrics_pb2.beta_create_MetricsServiceV2_stub,
            service_path,
            port,
            ssl_creds=ssl_creds,
            channel=channel,
            scopes=scopes)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        del self.stub

    # Service calls
    def list_log_metrics(
            self,
            project_name='',
            **kwargs):
        """Lists logs-based metrics."""
        list_log_metrics_request = logging_metrics_pb2.ListLogMetricsRequest(
            project_name=project_name,
            **kwargs)
        return self.list_log_metrics_callable()(list_log_metrics_request)

    def list_log_metrics_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_LOG_METRICS_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListLogMetrics,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def get_log_metric(
            self,
            metric_name='',
            **kwargs):
        """Gets a logs-based metric."""
        get_log_metric_request = logging_metrics_pb2.GetLogMetricRequest(
            metric_name=metric_name,
            **kwargs)
        return self.get_log_metric_callable()(get_log_metric_request)

    def get_log_metric_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.GetLogMetric,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def create_log_metric(
            self,
            project_name='',
            metric=None,
            **kwargs):
        """Creates a logs-based metric."""
        if metric is None:
            metric = logging_metrics_pb2.LogMetric()
        create_log_metric_request = logging_metrics_pb2.CreateLogMetricRequest(
            project_name=project_name,
            metric=metric,
            **kwargs)
        return self.create_log_metric_callable()(create_log_metric_request)

    def create_log_metric_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.CreateLogMetric,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def update_log_metric(
            self,
            metric_name='',
            metric=None,
            **kwargs):
        """Creates or updates a logs-based metric."""
        if metric is None:
            metric = logging_metrics_pb2.LogMetric()
        update_log_metric_request = logging_metrics_pb2.UpdateLogMetricRequest(
            metric_name=metric_name,
            metric=metric,
            **kwargs)
        return self.update_log_metric_callable()(update_log_metric_request)

    def update_log_metric_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.UpdateLogMetric,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def delete_log_metric(
            self,
            metric_name='',
            **kwargs):
        """Deletes a logs-based metric."""
        delete_log_metric_request = logging_metrics_pb2.DeleteLogMetricRequest(
            metric_name=metric_name,
            **kwargs)
        return self.delete_log_metric_callable()(delete_log_metric_request)

    def delete_log_metric_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.DeleteLogMetric,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    # ========
    # Manually-added methods: add custom (non-generated) methods after this point.
    # ========
