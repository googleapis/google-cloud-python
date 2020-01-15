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

"""Accesses the google.monitoring.dashboard.v1 DashboardsService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import grpc

from google.cloud.monitoring_dashboard.v1.gapic import dashboards_service_client_config
from google.cloud.monitoring_dashboard.v1.gapic import enums
from google.cloud.monitoring_dashboard.v1.gapic.transports import (
    dashboards_service_grpc_transport,
)
from google.cloud.monitoring_dashboard.v1.proto import dashboard_pb2
from google.cloud.monitoring_dashboard.v1.proto import dashboards_service_pb2
from google.cloud.monitoring_dashboard.v1.proto import dashboards_service_pb2_grpc
from google.protobuf import empty_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-monitoring-dashboards"
).version


class DashboardsServiceClient(object):
    """
    Manages Stackdriver dashboards. A dashboard is an arrangement of data display
    widgets in a specific layout.
    """

    SERVICE_ADDRESS = "monitoring.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.monitoring.dashboard.v1.DashboardsService"

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
            DashboardsServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.DashboardsServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.DashboardsServiceGrpcTransport]): A transport
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
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = dashboards_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=dashboards_service_grpc_transport.DashboardsServiceGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = dashboards_service_grpc_transport.DashboardsServiceGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
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
    def create_dashboard(
        self,
        parent,
        dashboard,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new custom dashboard.

        This method requires the ``monitoring.dashboards.create`` permission on
        the specified project. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Example:
            >>> from google.cloud.monitoring_dashboard import v1
            >>>
            >>> client = v1.DashboardsServiceClient()
            >>>
            >>> # TODO: Initialize `parent`:
            >>> parent = ''
            >>>
            >>> # TODO: Initialize `dashboard`:
            >>> dashboard = {}
            >>>
            >>> response = client.create_dashboard(parent, dashboard)

        Args:
            parent (str): Required. The project on which to execute the request. The format is
                ``"projects/{project_id_or_number}"``. The {project_id_or_number} must
                match the dashboard resource name.
            dashboard (Union[dict, ~google.cloud.monitoring_dashboard.v1.types.Dashboard]): Required. The initial dashboard specification.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_dashboard.v1.types.Dashboard`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_dashboard.v1.types.Dashboard` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_dashboard" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_dashboard"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_dashboard,
                default_retry=self._method_configs["CreateDashboard"].retry,
                default_timeout=self._method_configs["CreateDashboard"].timeout,
                client_info=self._client_info,
            )

        request = dashboards_service_pb2.CreateDashboardRequest(
            parent=parent, dashboard=dashboard
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_dashboard"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_dashboards(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the existing dashboards.

        This method requires the ``monitoring.dashboards.list`` permission on
        the specified project. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Example:
            >>> from google.cloud.monitoring_dashboard import v1
            >>>
            >>> client = v1.DashboardsServiceClient()
            >>>
            >>> # TODO: Initialize `parent`:
            >>> parent = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_dashboards(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_dashboards(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The scope of the dashboards to list. A project scope must
                be specified in the form of ``"projects/{project_id_or_number}"``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.monitoring_dashboard.v1.types.Dashboard` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_dashboards" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_dashboards"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_dashboards,
                default_retry=self._method_configs["ListDashboards"].retry,
                default_timeout=self._method_configs["ListDashboards"].timeout,
                client_info=self._client_info,
            )

        request = dashboards_service_pb2.ListDashboardsRequest(
            parent=parent, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_dashboards"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="dashboards",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_dashboard(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Fetches a specific dashboard.

        This method requires the ``monitoring.dashboards.get`` permission on the
        specified dashboard. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Example:
            >>> from google.cloud.monitoring_dashboard import v1
            >>>
            >>> client = v1.DashboardsServiceClient()
            >>>
            >>> # TODO: Initialize `name`:
            >>> name = ''
            >>>
            >>> response = client.get_dashboard(name)

        Args:
            name (str): Required. The resource name of the Dashboard. The format is one of
                ``"dashboards/{dashboard_id}"`` (for system dashboards) or
                ``"projects/{project_id_or_number}/dashboards/{dashboard_id}"`` (for
                custom dashboards).
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_dashboard.v1.types.Dashboard` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_dashboard" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_dashboard"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_dashboard,
                default_retry=self._method_configs["GetDashboard"].retry,
                default_timeout=self._method_configs["GetDashboard"].timeout,
                client_info=self._client_info,
            )

        request = dashboards_service_pb2.GetDashboardRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_dashboard"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_dashboard(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an existing custom dashboard.

        This method requires the ``monitoring.dashboards.delete`` permission on
        the specified dashboard. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Example:
            >>> from google.cloud.monitoring_dashboard import v1
            >>>
            >>> client = v1.DashboardsServiceClient()
            >>>
            >>> # TODO: Initialize `name`:
            >>> name = ''
            >>>
            >>> client.delete_dashboard(name)

        Args:
            name (str): Required. The resource name of the Dashboard. The format is
                ``"projects/{project_id_or_number}/dashboards/{dashboard_id}"``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        # Wrap the transport method to add retry and timeout logic.
        if "delete_dashboard" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_dashboard"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_dashboard,
                default_retry=self._method_configs["DeleteDashboard"].retry,
                default_timeout=self._method_configs["DeleteDashboard"].timeout,
                client_info=self._client_info,
            )

        request = dashboards_service_pb2.DeleteDashboardRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_dashboard"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_dashboard(
        self,
        dashboard,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Replaces an existing custom dashboard with a new definition.

        This method requires the ``monitoring.dashboards.update`` permission on
        the specified dashboard. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Example:
            >>> from google.cloud.monitoring_dashboard import v1
            >>>
            >>> client = v1.DashboardsServiceClient()
            >>>
            >>> # TODO: Initialize `dashboard`:
            >>> dashboard = {}
            >>>
            >>> response = client.update_dashboard(dashboard)

        Args:
            dashboard (Union[dict, ~google.cloud.monitoring_dashboard.v1.types.Dashboard]): Required. The dashboard that will replace the existing dashboard.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_dashboard.v1.types.Dashboard`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_dashboard.v1.types.Dashboard` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_dashboard" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_dashboard"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_dashboard,
                default_retry=self._method_configs["UpdateDashboard"].retry,
                default_timeout=self._method_configs["UpdateDashboard"].timeout,
                client_info=self._client_info,
            )

        request = dashboards_service_pb2.UpdateDashboardRequest(dashboard=dashboard)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("dashboard.name", dashboard.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_dashboard"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
