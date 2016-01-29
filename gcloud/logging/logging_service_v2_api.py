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
# https://github.com/google/googleapis/blob/7710ead495227e80a0f06ceb66bdf3238d926f77/google/logging/v2/logging.proto,
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

from google.api import monitored_resource_pb2
from google.gax import api_callable
from google.gax import api_utils
from google.gax import page_descriptor
from google.logging.v2 import log_entry_pb2
from google.logging.v2 import logging_pb2


class LoggingServiceV2Api(object):
    """Service for ingesting and querying logs."""

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

    _LIST_LOG_ENTRIES_DESCRIPTOR = page_descriptor.PageDescriptor(
        'page_token',
        'next_page_token',
        'entries',
    )
    _LIST_MONITORED_RESOURCE_DESCRIPTORS_DESCRIPTOR = page_descriptor.PageDescriptor(
        'page_token',
        'next_page_token',
        'resource_descriptors')

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
            logging_pb2.beta_create_LoggingServiceV2_stub,
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
    def delete_log(
            self,
            log_name='',
            **kwargs):
        """
        Deletes a log and all its log entries.
        The log will reappear if it receives new entries.
        """
        delete_log_request = logging_pb2.DeleteLogRequest(
            log_name=log_name,
            **kwargs)
        return self.delete_log_callable()(delete_log_request)

    def delete_log_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.DeleteLog,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def write_log_entries(
            self,
            log_name='',
            resource=None,
            labels=None,
            entries=None,
            **kwargs):
        """
        Writes log entries to Cloud Logging.
        All log entries in Cloud Logging are written by this method.
        """
        if resource is None:
            resource = monitored_resource_pb2.MonitoredResource()
        if labels is None:
            labels = []
        if entries is None:
            entries = []
        write_log_entries_request = logging_pb2.WriteLogEntriesRequest(
            log_name=log_name,
            resource=resource,
            labels=labels,
            entries=entries,
            **kwargs)
        return self.write_log_entries_callable()(write_log_entries_request)

    def write_log_entries_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.WriteLogEntries,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def list_log_entries(
            self,
            project_ids=None,
            filter_='',
            order_by='',
            **kwargs):
        """
        Lists log entries.  Use this method to retrieve log entries from Cloud
        Logging.  For ways to export log entries, see
        [Exporting Logs](/logging/docs/export).
        """
        if project_ids is None:
            project_ids = []
        list_log_entries_request = logging_pb2.ListLogEntriesRequest(
            project_ids=project_ids,
            filter=filter_,
            order_by=order_by,
            **kwargs)
        return self.list_log_entries_callable()(list_log_entries_request)

    def list_log_entries_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_LOG_ENTRIES_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListLogEntries,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def list_monitored_resource_descriptors(self, **kwargs):
        """Lists monitored resource descriptors that are used by Cloud Logging."""
        list_monitored_resource_descriptors_request = logging_pb2.ListMonitoredResourceDescriptorsRequest(**kwargs)
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

    # ========
    # Manually-added methods: add custom (non-generated) methods after this point.
    # ========
