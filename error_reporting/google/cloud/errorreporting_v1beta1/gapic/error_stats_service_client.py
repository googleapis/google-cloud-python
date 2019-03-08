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
"""Accesses the google.devtools.clouderrorreporting.v1beta1 ErrorStatsService API."""

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

from google.cloud.errorreporting_v1beta1.gapic import enums
from google.cloud.errorreporting_v1beta1.gapic import error_stats_service_client_config
from google.cloud.errorreporting_v1beta1.gapic.transports import (
    error_stats_service_grpc_transport,
)
from google.cloud.errorreporting_v1beta1.proto import common_pb2
from google.cloud.errorreporting_v1beta1.proto import error_group_service_pb2
from google.cloud.errorreporting_v1beta1.proto import error_group_service_pb2_grpc
from google.cloud.errorreporting_v1beta1.proto import error_stats_service_pb2
from google.cloud.errorreporting_v1beta1.proto import error_stats_service_pb2_grpc
from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-error-reporting"
).version


class ErrorStatsServiceClient(object):
    """
    An API for retrieving and managing error statistics as well as data for
    individual events.
    """

    SERVICE_ADDRESS = "clouderrorreporting.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.devtools.clouderrorreporting.v1beta1.ErrorStatsService"

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
            ErrorStatsServiceClient: The constructed client.
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
            transport (Union[~.ErrorStatsServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.ErrorStatsServiceGrpcTransport]): A transport
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
            client_config = error_stats_service_client_config.config

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
                    default_class=error_stats_service_grpc_transport.ErrorStatsServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = error_stats_service_grpc_transport.ErrorStatsServiceGrpcTransport(
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
    def list_group_stats(
        self,
        project_name,
        time_range,
        group_id=None,
        service_filter=None,
        timed_count_duration=None,
        alignment=None,
        alignment_time=None,
        order=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the specified groups.

        Example:
            >>> from google.cloud import errorreporting_v1beta1
            >>>
            >>> client = errorreporting_v1beta1.ErrorStatsServiceClient()
            >>>
            >>> project_name = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `time_range`:
            >>> time_range = {}
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_group_stats(project_name, time_range):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_group_stats(project_name, time_range).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project_name (str): [Required] The resource name of the Google Cloud Platform project.
                Written as projects/ plus the Google Cloud Platform project ID.

                Example: projects/my-project-123.
            time_range (Union[dict, ~google.cloud.errorreporting_v1beta1.types.QueryTimeRange]): [Optional] List data for the given time range. If not set a default time
                range is used. The field time\_range\_begin in the response will specify
                the beginning of this time range. Only ErrorGroupStats with a non-zero
                count in the given time range are returned, unless the request contains
                an explicit group\_id list. If a group\_id list is given, also
                ErrorGroupStats with zero occurrences are returned.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.errorreporting_v1beta1.types.QueryTimeRange`
            group_id (list[str]): [Optional] List all ErrorGroupStats with these IDs.
            service_filter (Union[dict, ~google.cloud.errorreporting_v1beta1.types.ServiceContextFilter]): [Optional] List only ErrorGroupStats which belong to a service context
                that matches the filter. Data for all service contexts is returned if
                this field is not specified.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.errorreporting_v1beta1.types.ServiceContextFilter`
            timed_count_duration (Union[dict, ~google.cloud.errorreporting_v1beta1.types.Duration]): [Optional] The preferred duration for a single returned ``TimedCount``.
                If not set, no timed counts are returned.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.errorreporting_v1beta1.types.Duration`
            alignment (~google.cloud.errorreporting_v1beta1.types.TimedCountAlignment): [Optional] The alignment of the timed counts to be returned. Default is
                ``ALIGNMENT_EQUAL_AT_END``.
            alignment_time (Union[dict, ~google.cloud.errorreporting_v1beta1.types.Timestamp]): [Optional] Time where the timed counts shall be aligned if rounded
                alignment is chosen. Default is 00:00 UTC.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.errorreporting_v1beta1.types.Timestamp`
            order (~google.cloud.errorreporting_v1beta1.types.ErrorGroupOrder): [Optional] The sort order in which the results are returned. Default is
                ``COUNT_DESC``.
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
            is an iterable of :class:`~google.cloud.errorreporting_v1beta1.types.ErrorGroupStats` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_group_stats" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_group_stats"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_group_stats,
                default_retry=self._method_configs["ListGroupStats"].retry,
                default_timeout=self._method_configs["ListGroupStats"].timeout,
                client_info=self._client_info,
            )

        request = error_stats_service_pb2.ListGroupStatsRequest(
            project_name=project_name,
            time_range=time_range,
            group_id=group_id,
            service_filter=service_filter,
            timed_count_duration=timed_count_duration,
            alignment=alignment,
            alignment_time=alignment_time,
            order=order,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_group_stats"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="error_group_stats",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def list_events(
        self,
        project_name,
        group_id,
        service_filter=None,
        time_range=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the specified events.

        Example:
            >>> from google.cloud import errorreporting_v1beta1
            >>>
            >>> client = errorreporting_v1beta1.ErrorStatsServiceClient()
            >>>
            >>> project_name = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `group_id`:
            >>> group_id = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_events(project_name, group_id):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_events(project_name, group_id).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project_name (str): [Required] The resource name of the Google Cloud Platform project.
                Written as ``projects/`` plus the `Google Cloud Platform project
                ID <https://support.google.com/cloud/answer/6158840>`__. Example:
                ``projects/my-project-123``.
            group_id (str): [Required] The group for which events shall be returned.
            service_filter (Union[dict, ~google.cloud.errorreporting_v1beta1.types.ServiceContextFilter]): [Optional] List only ErrorGroups which belong to a service context that
                matches the filter. Data for all service contexts is returned if this
                field is not specified.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.errorreporting_v1beta1.types.ServiceContextFilter`
            time_range (Union[dict, ~google.cloud.errorreporting_v1beta1.types.QueryTimeRange]): [Optional] List only data for the given time range. If not set a default
                time range is used. The field time\_range\_begin in the response will
                specify the beginning of this time range.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.errorreporting_v1beta1.types.QueryTimeRange`
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
            is an iterable of :class:`~google.cloud.errorreporting_v1beta1.types.ErrorEvent` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_events" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_events"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_events,
                default_retry=self._method_configs["ListEvents"].retry,
                default_timeout=self._method_configs["ListEvents"].timeout,
                client_info=self._client_info,
            )

        request = error_stats_service_pb2.ListEventsRequest(
            project_name=project_name,
            group_id=group_id,
            service_filter=service_filter,
            time_range=time_range,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_events"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="error_events",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_events(
        self,
        project_name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes all error events of a given project.

        Example:
            >>> from google.cloud import errorreporting_v1beta1
            >>>
            >>> client = errorreporting_v1beta1.ErrorStatsServiceClient()
            >>>
            >>> project_name = client.project_path('[PROJECT]')
            >>>
            >>> response = client.delete_events(project_name)

        Args:
            project_name (str): [Required] The resource name of the Google Cloud Platform project.
                Written as ``projects/`` plus the `Google Cloud Platform project
                ID <https://support.google.com/cloud/answer/6158840>`__. Example:
                ``projects/my-project-123``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.errorreporting_v1beta1.types.DeleteEventsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_events" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_events"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_events,
                default_retry=self._method_configs["DeleteEvents"].retry,
                default_timeout=self._method_configs["DeleteEvents"].timeout,
                client_info=self._client_info,
            )

        request = error_stats_service_pb2.DeleteEventsRequest(project_name=project_name)
        return self._inner_api_calls["delete_events"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
