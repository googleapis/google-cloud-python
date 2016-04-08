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
# https://github.com/google/googleapis/blob/master/google/logging/v2/logging.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.logging.v2 LoggingServiceV2 API."""

import json
import os
import pkg_resources
import platform

from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.api import monitored_resource_pb2
from google.logging.v2 import log_entry_pb2
from google.logging.v2 import logging_pb2

_PageDesc = google.gax.PageDescriptor


class LoggingServiceV2Api(object):
    """Service for ingesting and querying logs."""

    SERVICE_ADDRESS = 'logging.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    _CODE_GEN_NAME_VERSION = 'gapic/0.1.0'

    _GAX_VERSION = pkg_resources.get_distribution('google-gax').version

    _DEFAULT_TIMEOUT = 30

    _PAGE_DESCRIPTORS = {
        'list_log_entries': _PageDesc('page_token', 'next_page_token',
                                      'entries'),
        'list_monitored_resource_descriptors': _PageDesc(
            'page_token', 'next_page_token', 'resource_descriptors')
    }

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = ('https://www.googleapis.com/auth/logging.write',
                   'https://www.googleapis.com/auth/logging.admin',
                   'https://www.googleapis.com/auth/logging.read',
                   'https://www.googleapis.com/auth/cloud-platform.read-only',
                   'https://www.googleapis.com/auth/cloud-platform', )

    _PROJECT_PATH_TEMPLATE = path_template.PathTemplate('projects/{project}')
    _LOG_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/logs/{log}')

    @classmethod
    def project_path(cls, project):
        """Returns a fully-qualified project resource name string."""
        return cls._PROJECT_PATH_TEMPLATE.instantiate({'project': project, })

    @classmethod
    def log_path(cls, project, log):
        """Returns a fully-qualified log resource name string."""
        return cls._LOG_PATH_TEMPLATE.instantiate({
            'project': project,
            'log': log,
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
          A LoggingServiceV2Api object.
        """
        if scopes is None:
            scopes = self._ALL_SCOPES
        bundling_override = bundling_override or {}
        retrying_override = retrying_override or {}
        client_config = pkg_resources.resource_string(
            __name__, 'logging_service_v2_client_config.json')
        self._defaults = api_callable.construct_settings(
            'google.logging.v2.LoggingServiceV2',
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
            logging_pb2.beta_create_LoggingServiceV2_stub,
            service_path,
            port,
            ssl_creds=ssl_creds,
            channel=channel,
            scopes=scopes)

    # Service calls
    def delete_log(self, log_name='', options=None):
        """
        Deletes a log and all its log entries.
        The log will reappear if it receives new entries.

        Args:
          log_name (string): Required. The resource name of the log to delete.  Example:
            `"projects/my-project/logs/syslog"`.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        req = logging_pb2.DeleteLogRequest(log_name=log_name)
        settings = self._defaults['delete_log'].merge(options)
        api_call = api_callable.create_api_call(self.stub.DeleteLog,
                                                settings=settings)
        api_call(req, metadata=self._headers)

    def write_log_entries(self,
                          log_name='',
                          resource=None,
                          labels=None,
                          entries=None,
                          options=None):
        """
        Writes log entries to Cloud Logging.
        All log entries in Cloud Logging are written by this method.

        Args:
          log_name (string): Optional. A default log resource name for those log entries in `entries`
            that do not specify their own `logName`.  Example:
            `"projects/my-project/logs/syslog"`.  See
            [LogEntry][google.logging.v2.LogEntry].
          resource (:class:`google.api.monitored_resource_pb2.MonitoredResource`): Optional. A default monitored resource for those log entries in `entries`
            that do not specify their own `resource`.
          labels (list[:class:`google.logging.v2.logging_pb2.WriteLogEntriesRequest.LabelsEntry`]): Optional. User-defined `key:value` items that are added to
            the `labels` field of each log entry in `entries`, except when a log
            entry specifies its own `key:value` item with the same key.
            Example: `{ "size": "large", "color":"red" }`
          entries (list[:class:`google.logging.v2.log_entry_pb2.LogEntry`]): Required. The log entries to write. The log entries must have values for
            all required fields.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        if resource is None:
            resource = monitored_resource_pb2.MonitoredResource()
        if labels is None:
            labels = []
        if entries is None:
            entries = []
        req = logging_pb2.WriteLogEntriesRequest(log_name=log_name,
                                                 resource=resource,
                                                 labels=labels,
                                                 entries=entries)
        settings = self._defaults['write_log_entries'].merge(options)
        api_call = api_callable.create_api_call(self.stub.WriteLogEntries,
                                                settings=settings)
        api_call(req, metadata=self._headers)

    def list_log_entries(self,
                         project_ids=None,
                         filter_='',
                         order_by='',
                         options=None):
        """
        Lists log entries.  Use this method to retrieve log entries from Cloud
        Logging.  For ways to export log entries, see
        `Exporting Logs <https://cloud.google.com/logging/docs/export>`_.

        Args:
          project_ids (list[string]): Required. One or more project IDs or project numbers from which to retrieve
            log entries.  Examples of a project ID: `"my-project-1A"`, `"1234567890"`.
          filter (string): Optional. An [advanced logs filter](/logging/docs/view/advanced_filters).
            The filter is compared against all log entries in the projects specified by
            `projectIds`.  Only entries that match the filter are retrieved.  An empty
            filter matches all log entries.
          order_by (string): Optional. How the results should be sorted.  Presently, the only permitted
            values are `"timestamp"` (default) and `"timestamp desc"`.  The first
            option returns entries in order of increasing values of
            `LogEntry.timestamp` (oldest first), and the second option returns entries
            in order of decreasing timestamps (newest first).  Entries with equal
            timestamps are returned in order of `LogEntry.insertId`.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Yields:
          Instances of :class:`google.logging.v2.log_entry_pb2.LogEntry`
          unless page streaming is disabled through the call options. If
          page streaming is disabled, a single
          :class:`google.logging.v2.logging_pb2.ListLogEntriesResponse` instance
          is returned.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        if project_ids is None:
            project_ids = []
        req = logging_pb2.ListLogEntriesRequest(project_ids=project_ids,
                                                filter=filter_,
                                                order_by=order_by)
        settings = self._defaults['list_log_entries'].merge(options)
        api_call = api_callable.create_api_call(self.stub.ListLogEntries,
                                                settings=settings)
        return api_call(req, metadata=self._headers)

    def list_monitored_resource_descriptors(self, options=None):
        """
        Lists monitored resource descriptors that are used by Cloud Logging.

        Args:
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Yields:
          Instances of :class:`google.api.monitored_resource_pb2.MonitoredResourceDescriptor`
          unless page streaming is disabled through the call options. If
          page streaming is disabled, a single
          :class:`google.logging.v2.logging_pb2.ListMonitoredResourceDescriptorsResponse` instance
          is returned.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        req = logging_pb2.ListMonitoredResourceDescriptorsRequest()
        settings = self._defaults['list_monitored_resource_descriptors'].merge(
            options)
        api_call = api_callable.create_api_call(
            self.stub.ListMonitoredResourceDescriptors,
            settings=settings)
        return api_call(req, metadata=self._headers)
