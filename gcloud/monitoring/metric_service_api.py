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
# https://github.com/google/googleapis/blob/master/google/monitoring/v3/metric_service.proto,
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

from google.gax import PageDescriptor
from google.gax import api_callable
from google.gax import config
from google.gax.path_template import PathTemplate
from google.monitoring.v3 import metric_service_pb2
from google.api import metric_pb2 as api_metric_pb2
from google.api import monitored_resource_pb2
from google.monitoring.v3 import common_pb2
from google.monitoring.v3 import metric_pb2 as v3_metric_pb2


class MetricServiceApi(object):
    """
    Manages metric descriptors, monitored resource descriptors, and
    time series data.
    """

    # The default address of the logging service.
    _SERVICE_ADDRESS = 'monitoring.googleapis.com'

    # The default port of the logging service.
    _DEFAULT_SERVICE_PORT = 443

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = (
        'https://www.googleapis.com/auth/monitoring',
        'https://www.googleapis.com/auth/monitoring.write',
        'https://www.googleapis.com/auth/monitoring.read',
        'https://www.googleapis.com/auth/cloud-platform',
    )

    _LIST_MONITORED_RESOURCE_DESCRIPTORS_DESCRIPTOR = PageDescriptor(
        'page_token',
        'next_page_token',
        'resource_descriptors',
    )
    _LIST_METRIC_DESCRIPTORS_DESCRIPTOR = PageDescriptor(
        'page_token',
        'next_page_token',
        'metric_descriptors',
    )
    _LIST_TIME_SERIES_DESCRIPTOR = PageDescriptor(
        'page_token',
        'next_page_token',
        'time_series',
    )
    _LIST_MONITORED_RESOURCES_FOR_METRIC_DESCRIPTOR = PageDescriptor(
        'page_token',
        'next_page_token',
        'monitored_resources',
    )
    _LIST_METRICS_DESCRIPTOR = PageDescriptor(
        'page_token',
        'next_page_token',
        'metrics',
    )

    class Templates(object):
        """PathTemplates for resources used by MetricServiceApi."""
        PROJECT = PathTemplate.from_string(
            'projects/{project}')
        MONITORED_RESOURCE_DESCRIPTOR = PathTemplate.from_string(
            'projects/{project}/monitoredResourceDescriptors/{monitoredResourceDescriptor}')
        METRIC_DESCRIPTOR = PathTemplate.from_string(
            'projects/{project}/metricDescriptors/{metricDescriptor}')

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

        self.stub = config.create_stub(
            metric_service_pb2.beta_create_MetricService_stub,
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
    def list_monitored_resource_descriptors(
            self,
            name='',
            filter_='',
            **kwargs):
        """
        Lists monitored resource descriptors that match a filter.

        :type name: string
        :type filter: string
        """

        list_monitored_resource_descriptors_request = metric_service_pb2.ListMonitoredResourceDescriptorsRequest(
            name=name,
            filter=filter_,
            **kwargs)
        return self.list_monitored_resource_descriptors_callable()(list_monitored_resource_descriptors_request)

    def list_monitored_resource_descriptors_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_MONITORED_RESOURCE_DESCRIPTORS_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListMonitoredResourceDescriptors,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def get_monitored_resource_descriptor(
            self,
            name='',
            **kwargs):
        """
        Gets a single monitored resource descriptor.

        :type name: string
        """

        get_monitored_resource_descriptor_request = metric_service_pb2.GetMonitoredResourceDescriptorRequest(
            name=name,
            **kwargs)
        return self.get_monitored_resource_descriptor_callable()(get_monitored_resource_descriptor_request)

    def get_monitored_resource_descriptor_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.GetMonitoredResourceDescriptor,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def list_metric_descriptors(
            self,
            name='',
            filter_='',
            **kwargs):
        """
        Lists metric descriptors that match a filter.

        :type name: string
        :type filter: string
        """

        list_metric_descriptors_request = metric_service_pb2.ListMetricDescriptorsRequest(
            name=name,
            filter=filter_,
            **kwargs)
        return self.list_metric_descriptors_callable()(list_metric_descriptors_request)

    def list_metric_descriptors_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_METRIC_DESCRIPTORS_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListMetricDescriptors,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def get_metric_descriptor(
            self,
            name='',
            **kwargs):
        """
        Gets a single metric descriptor.

        :type name: string
        """

        get_metric_descriptor_request = metric_service_pb2.GetMetricDescriptorRequest(
            name=name,
            **kwargs)
        return self.get_metric_descriptor_callable()(get_metric_descriptor_request)

    def get_metric_descriptor_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.GetMetricDescriptor,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def create_metric_descriptor(
            self,
            name='',
            metric_descriptor=None,
            **kwargs):
        """
        Creates a new metric descriptor.
        User-created metric descriptors define
        [custom metrics](/monitoring/custom-metrics).

        :type name: string
        :type metric_descriptor: api_metric_pb2.MetricDescriptor
        """
        if metric_descriptor is None:
            metric_descriptor = api_metric_pb2.MetricDescriptor()
        create_metric_descriptor_request = metric_service_pb2.CreateMetricDescriptorRequest(
            name=name,
            metric_descriptor=metric_descriptor,
            **kwargs)
        return self.create_metric_descriptor_callable()(create_metric_descriptor_request)

    def create_metric_descriptor_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.CreateMetricDescriptor,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def delete_metric_descriptor(
            self,
            name='',
            **kwargs):
        """
        Deletes a metric descriptor. Only user-created
        [custom metrics](/monitoring/custom-metrics) can be deleted.

        :type name: string
        """

        delete_metric_descriptor_request = metric_service_pb2.DeleteMetricDescriptorRequest(
            name=name,
            **kwargs)
        return self.delete_metric_descriptor_callable()(delete_metric_descriptor_request)

    def delete_metric_descriptor_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.DeleteMetricDescriptor,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def list_time_series(
            self,
            name='',
            filter_='',
            interval=None,
            aggregation=None,
            order_by='',
            view=None,
            **kwargs):
        """
        Lists the time series that match a filter.

        :type name: string
        :type filter: string
        :type interval: common_pb2.TimeInterval
        :type aggregation: common_pb2.Aggregation
        :type order_by: string
        :type view: enum metric_service_pb2.ListTimeSeriesRequest.TimeSeriesView
        """
        if interval is None:
            interval = common_pb2.TimeInterval()
        if aggregation is None:
            aggregation = common_pb2.Aggregation()
        if view is None:
            view = metric_service_pb2.ListTimeSeriesRequest.FULL
        list_time_series_request = metric_service_pb2.ListTimeSeriesRequest(
            name=name,
            filter=filter_,
            interval=interval,
            aggregation=aggregation,
            order_by=order_by,
            view=view,
            **kwargs)
        return self.list_time_series_callable()(list_time_series_request)

    def list_time_series_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_TIME_SERIES_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListTimeSeries,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def create_time_series(
            self,
            name='',
            time_series=None,
            **kwargs):
        """
        Creates or adds data to one or more time series.
        You must check the response to see if any of the requests failed.

        :type name: string
        :type time_series: list of v3_metric_pb2.TimeSeries
        """
        if time_series is None:
            time_series = []
        create_time_series_request = metric_service_pb2.CreateTimeSeriesRequest(
            name=name,
            time_series=time_series,
            **kwargs)
        return self.create_time_series_callable()(create_time_series_request)

    def create_time_series_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.CreateTimeSeries,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def list_monitored_resources_for_metric(
            self,
            name='',
            metric_name='',
            interval=None,
            view=None,
            **kwargs):
        """
        Lists the monitored resources against which data is written for a specific
        metric name.

        :type name: string
        :type metric_name: string
        :type interval: common_pb2.TimeInterval
        :type view: enum metric_service_pb2.ListMonitoredResourcesForMetricRequest.MonitoredResourceView
        """
        if interval is None:
            interval = common_pb2.TimeInterval()
        if view is None:
            view = metric_service_pb2.ListMonitoredResourcesForMetricRequest.FULL
        list_monitored_resources_for_metric_request = metric_service_pb2.ListMonitoredResourcesForMetricRequest(
            name=name,
            metric_name=metric_name,
            interval=interval,
            view=view,
            **kwargs)
        return self.list_monitored_resources_for_metric_callable()(list_monitored_resources_for_metric_request)

    def list_monitored_resources_for_metric_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_MONITORED_RESOURCES_FOR_METRIC_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListMonitoredResourcesForMetric,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def list_metrics(
            self,
            name='',
            interval=None,
            monitored_resource=None,
            view=None,
            **kwargs):
        """
        Lists the metrics for which there exists data. Optionally restricts the
        metrics to a partially specified monitored resource.

        :type name: string
        :type interval: common_pb2.TimeInterval
        :type monitored_resource: monitored_resource_pb2.MonitoredResource
        :type view: enum metric_service_pb2.ListMetricsRequest.MetricView
        """
        if interval is None:
            interval = common_pb2.TimeInterval()
        if monitored_resource is None:
            monitored_resource = monitored_resource_pb2.MonitoredResource()
        if view is None:
            view = metric_service_pb2.ListMetricsRequest.FULL
        list_metrics_request = metric_service_pb2.ListMetricsRequest(
            name=name,
            interval=interval,
            monitored_resource=monitored_resource,
            view=view,
            **kwargs)
        return self.list_metrics_callable()(list_metrics_request)

    def list_metrics_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_METRICS_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListMetrics,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    # ========
    # Manually-added methods: add custom (non-generated) methods after this point.
    # ========