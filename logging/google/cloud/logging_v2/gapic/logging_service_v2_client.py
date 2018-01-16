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
"""Accesses the google.logging.v2 LoggingServiceV2 API."""

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
from google.cloud.logging_v2.gapic import logging_service_v2_client_config
from google.cloud.logging_v2.proto import log_entry_pb2
from google.cloud.logging_v2.proto import logging_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-logging', ).version


class LoggingServiceV2Client(object):
    """Service for ingesting and querying logs."""

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
    _INTERFACE_NAME = 'google.logging.v2.LoggingServiceV2'

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project,
        )

    @classmethod
    def log_path(cls, project, log):
        """Return a fully-qualified log string."""
        return google.api_core.path_template.expand(
            'projects/{project}/logs/{log}',
            project=project,
            log=log,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=logging_service_v2_client_config.config,
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
        self.logging_service_v2_stub = (
            logging_pb2.LoggingServiceV2Stub(channel))

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
        self._delete_log = google.api_core.gapic_v1.method.wrap_method(
            self.logging_service_v2_stub.DeleteLog,
            default_retry=method_configs['DeleteLog'].retry,
            default_timeout=method_configs['DeleteLog'].timeout,
            client_info=client_info,
        )
        self._write_log_entries = google.api_core.gapic_v1.method.wrap_method(
            self.logging_service_v2_stub.WriteLogEntries,
            default_retry=method_configs['WriteLogEntries'].retry,
            default_timeout=method_configs['WriteLogEntries'].timeout,
            client_info=client_info,
        )
        self._list_log_entries = google.api_core.gapic_v1.method.wrap_method(
            self.logging_service_v2_stub.ListLogEntries,
            default_retry=method_configs['ListLogEntries'].retry,
            default_timeout=method_configs['ListLogEntries'].timeout,
            client_info=client_info,
        )
        self._list_monitored_resource_descriptors = google.api_core.gapic_v1.method.wrap_method(
            self.logging_service_v2_stub.ListMonitoredResourceDescriptors,
            default_retry=method_configs[
                'ListMonitoredResourceDescriptors'].retry,
            default_timeout=method_configs['ListMonitoredResourceDescriptors']
            .timeout,
            client_info=client_info,
        )
        self._list_logs = google.api_core.gapic_v1.method.wrap_method(
            self.logging_service_v2_stub.ListLogs,
            default_retry=method_configs['ListLogs'].retry,
            default_timeout=method_configs['ListLogs'].timeout,
            client_info=client_info,
        )

    # Service calls
    def delete_log(self,
                   log_name,
                   retry=google.api_core.gapic_v1.method.DEFAULT,
                   timeout=google.api_core.gapic_v1.method.DEFAULT,
                   metadata=None):
        """
        Deletes all the log entries in a log.
        The log reappears if it receives new entries.
        Log entries written shortly before the delete operation might not be
        deleted.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.LoggingServiceV2Client()
            >>>
            >>> log_name = client.log_path('[PROJECT]', '[LOG]')
            >>>
            >>> client.delete_log(log_name)

        Args:
            log_name (str): Required. The resource name of the log to delete:

                ::

                    \"projects/[PROJECT_ID]/logs/[LOG_ID]\"
                    \"organizations/[ORGANIZATION_ID]/logs/[LOG_ID]\"
                    \"billingAccounts/[BILLING_ACCOUNT_ID]/logs/[LOG_ID]\"
                    \"folders/[FOLDER_ID]/logs/[LOG_ID]\"

                ``[LOG_ID]`` must be URL-encoded. For example,
                ``\"projects/my-project-id/logs/syslog\"``,
                ``\"organizations/1234567890/logs/cloudresourcemanager.googleapis.com%2Factivity\"``.
                For more information about log names, see
                ``LogEntry``.
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
        request = logging_pb2.DeleteLogRequest(log_name=log_name, )
        self._delete_log(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def write_log_entries(self,
                          entries,
                          log_name=None,
                          resource=None,
                          labels=None,
                          partial_success=None,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT,
                          metadata=None):
        """
        ## Log entry resources

        Writes log entries to Stackdriver Logging. This API method is the
        only way to send log entries to Stackdriver Logging. This method
        is used, directly or indirectly, by the Stackdriver Logging agent
        (fluentd) and all logging libraries configured to use Stackdriver
        Logging.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.LoggingServiceV2Client()
            >>>
            >>> entries = []
            >>>
            >>> response = client.write_log_entries(entries)

        Args:
            entries (list[Union[dict, ~google.cloud.logging_v2.types.LogEntry]]): Required. The log entries to send to Stackdriver Logging. The order of log
                entries in this list does not matter. Values supplied in this method's
                ``log_name``, ``resource``, and ``labels`` fields are copied into those log
                entries in this list that do not include values for their corresponding
                fields. For more information, see the ``LogEntry`` type.

                If the ``timestamp`` or ``insert_id`` fields are missing in log entries, then
                this method supplies the current time or a unique identifier, respectively.
                The supplied values are chosen so that, among the log entries that did not
                supply their own values, the entries earlier in the list will sort before
                the entries later in the list. See the ``entries.list`` method.

                Log entries with timestamps that are more than the
                `logs retention period <https://cloud.google.com/logging/quota-policy>`_ in the past or more than
                24 hours in the future might be discarded. Discarding does not return
                an error.

                To improve throughput and to avoid exceeding the
                `quota limit <https://cloud.google.com/logging/quota-policy>`_ for calls to ``entries.write``,
                you should try to include several log entries in this list,
                rather than calling this method for each individual log entry.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.logging_v2.types.LogEntry`
            log_name (str): Optional. A default log resource name that is assigned to all log entries
                in ``entries`` that do not specify a value for ``log_name``:

                ::

                    \"projects/[PROJECT_ID]/logs/[LOG_ID]\"
                    \"organizations/[ORGANIZATION_ID]/logs/[LOG_ID]\"
                    \"billingAccounts/[BILLING_ACCOUNT_ID]/logs/[LOG_ID]\"
                    \"folders/[FOLDER_ID]/logs/[LOG_ID]\"

                ``[LOG_ID]`` must be URL-encoded. For example,
                ``\"projects/my-project-id/logs/syslog\"`` or
                ``\"organizations/1234567890/logs/cloudresourcemanager.googleapis.com%2Factivity\"``.
                For more information about log names, see
                ``LogEntry``.
            resource (Union[dict, ~google.cloud.logging_v2.types.MonitoredResource]): Optional. A default monitored resource object that is assigned to all log
                entries in ``entries`` that do not specify a value for ``resource``. Example:

                ::

                    { \"type\": \"gce_instance\",
                      \"labels\": {
                        \"zone\": \"us-central1-a\", \"instance_id\": \"00000000000000000000\" }}

                See ``LogEntry``.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.logging_v2.types.MonitoredResource`
            labels (dict[str -> str]): Optional. Default labels that are added to the ``labels`` field of all log
                entries in ``entries``. If a log entry already has a label with the same key
                as a label in this parameter, then the log entry's label is not changed.
                See ``LogEntry``.
            partial_success (bool): Optional. Whether valid entries should be written even if some other
                entries fail due to INVALID_ARGUMENT or PERMISSION_DENIED errors. If any
                entry is not written, then the response status is the error associated
                with one of the failed entries and the response includes error details
                keyed by the entries' zero-based index in the ``entries.write`` method.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.logging_v2.types.WriteLogEntriesResponse` instance.

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
        request = logging_pb2.WriteLogEntriesRequest(
            entries=entries,
            log_name=log_name,
            resource=resource,
            labels=labels,
            partial_success=partial_success,
        )
        return self._write_log_entries(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_log_entries(self,
                         resource_names,
                         project_ids=None,
                         filter_=None,
                         order_by=None,
                         page_size=None,
                         retry=google.api_core.gapic_v1.method.DEFAULT,
                         timeout=google.api_core.gapic_v1.method.DEFAULT,
                         metadata=None):
        """
        Lists log entries.  Use this method to retrieve log entries from
        Stackdriver Logging.  For ways to export log entries, see
        `Exporting Logs <https://cloud.google.com/logging/docs/export>`_.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.LoggingServiceV2Client()
            >>>
            >>> resource_names = []
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_log_entries(resource_names):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_log_entries(resource_names, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            resource_names (list[str]): Required. Names of one or more parent resources from which to
                retrieve log entries:

                ::

                    \"projects/[PROJECT_ID]\"
                    \"organizations/[ORGANIZATION_ID]\"
                    \"billingAccounts/[BILLING_ACCOUNT_ID]\"
                    \"folders/[FOLDER_ID]\"

                Projects listed in the ``project_ids`` field are added to this list.
            project_ids (list[str]): Deprecated. Use ``resource_names`` instead.  One or more project identifiers
                or project numbers from which to retrieve log entries.  Example:
                ``\"my-project-1A\"``. If present, these project identifiers are converted to
                resource name format and added to the list of resources in
                ``resource_names``.
            filter_ (str): Optional. A filter that chooses which log entries to return.  See [Advanced
                Logs Filters](/logging/docs/view/advanced_filters).  Only log entries that
                match the filter are returned.  An empty filter matches all log entries in
                the resources listed in ``resource_names``. Referencing a parent resource
                that is not listed in ``resource_names`` will cause the filter to return no
                results.
                The maximum length of the filter is 20000 characters.
            order_by (str): Optional. How the results should be sorted.  Presently, the only permitted
                values are ``\"timestamp asc\"`` (default) and ``\"timestamp desc\"``. The first
                option returns entries in order of increasing values of
                ``LogEntry.timestamp`` (oldest first), and the second option returns entries
                in order of decreasing timestamps (newest first).  Entries with equal
                timestamps are returned in order of their ``insert_id`` values.
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
            is an iterable of :class:`~google.cloud.logging_v2.types.LogEntry` instances.
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
        request = logging_pb2.ListLogEntriesRequest(
            resource_names=resource_names,
            project_ids=project_ids,
            filter=filter_,
            order_by=order_by,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_log_entries,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='entries',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def list_monitored_resource_descriptors(
            self,
            page_size=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Lists the descriptors for monitored resource types used by Stackdriver
        Logging.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.LoggingServiceV2Client()
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_monitored_resource_descriptors():
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_monitored_resource_descriptors(options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
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
            is an iterable of :class:`~google.cloud.logging_v2.types.MonitoredResourceDescriptor` instances.
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
        request = logging_pb2.ListMonitoredResourceDescriptorsRequest(
            page_size=page_size, )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_monitored_resource_descriptors,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='resource_descriptors',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def list_logs(self,
                  parent,
                  page_size=None,
                  retry=google.api_core.gapic_v1.method.DEFAULT,
                  timeout=google.api_core.gapic_v1.method.DEFAULT,
                  metadata=None):
        """
        Lists the logs in projects, organizations, folders, or billing accounts.
        Only logs that have entries are listed.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.LoggingServiceV2Client()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_logs(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_logs(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name that owns the logs:

                ::

                    \"projects/[PROJECT_ID]\"
                    \"organizations/[ORGANIZATION_ID]\"
                    \"billingAccounts/[BILLING_ACCOUNT_ID]\"
                    \"folders/[FOLDER_ID]\"
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
            is an iterable of :class:`str` instances.
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
        request = logging_pb2.ListLogsRequest(
            parent=parent,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_logs,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='log_names',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator
