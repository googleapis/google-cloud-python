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
# https://github.com/google/googleapis/blob/master/google/monitoring/v3/agent_service.proto,
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
from google.monitoring.v3 import agent_service_pb2
from google.api import monitored_resource_pb2
from google.monitoring.v3 import agent_pb2


class AgentTranslationServiceApi(object):
    """
    The AgentTranslation API allows `collectd`-based agents to
    write time series data to Cloud Monitoring.
    See [google.monitoring.v3.MetricService.CreateTimeSeries] instead.
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



    class Templates(object):
        """PathTemplates for resources used by AgentTranslationServiceApi."""
        PROJECT = PathTemplate.from_string(
            'projects/{project}')

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
            agent_service_pb2.beta_create_AgentTranslationService_stub,
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
    def create_collectd_time_series(
            self,
            name='',
            resource=None,
            collectd_version='',
            collectd_payloads=None,
            **kwargs):
        """
        Creates a new time series with the given data points.  This method
        is only for use in `collectd`-related code, including the Google
        Monitoring Agent. See
        [google.monitoring.v3.MetricService.CreateTimeSeries] instead.

        :type name: string
        :type resource: monitored_resource_pb2.MonitoredResource
        :type collectd_version: string
        :type collectd_payloads: list of agent_pb2.CollectdPayload
        """
        if resource is None:
            resource = monitored_resource_pb2.MonitoredResource()
        if collectd_payloads is None:
            collectd_payloads = []
        create_collectd_time_series_request = agent_service_pb2.CreateCollectdTimeSeriesRequest(
            name=name,
            resource=resource,
            collectd_version=collectd_version,
            collectd_payloads=collectd_payloads,
            **kwargs)
        return self.create_collectd_time_series_callable()(create_collectd_time_series_request)

    def create_collectd_time_series_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.CreateCollectdTimeSeries,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    # ========
    # Manually-added methods: add custom (non-generated) methods after this point.
    # ========