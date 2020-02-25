# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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
        Identifies which part of the FileDescriptorProto was defined at this
        location.

        Each element is a field number or an index. They form a path from the
        root FileDescriptorProto to the place where the definition. For example,
        this path: [ 4, 3, 2, 7, 1 ] refers to: file.message_type(3) // 4, 3
        .field(7) // 2, 7 .name() // 1 This is because
        FileDescriptorProto.message_type has field number 4: repeated
        DescriptorProto message_type = 4; and DescriptorProto.field has field
        number 2: repeated FieldDescriptorProto field = 2; and
        FieldDescriptorProto.name has field number 1: optional string name = 1;

        Thus, the above path gives the location of a field name. If we removed
        the last element: [ 4, 3, 2, 7 ] this path refers to the whole field
        declaration (from the beginning of the label to the terminating
        semicolon).

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
            parent (str): Input and output type names. These are resolved in the same way as
                FieldDescriptorProto.type_name, but must refer to a message type.
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
        An annotation that describes a resource definition without a
        corresponding message; see ``ResourceDescriptor``.

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
            parent (str): Reduce by computing the count of True-valued data points across time
                series for each alignment period. This reducer is valid for delta and
                gauge metrics of Boolean value type. The value type of the output is
                ``INT64``.
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
        Align and convert to a percentage change. This alignment is valid
        for gauge and delta metrics with numeric values. This alignment
        conceptually computes the equivalent of "((current -
        previous)/previous)*100" where previous value is determined based on the
        alignmentPeriod. In the event that previous is 0 the calculated value is
        infinity with the exception that if both (current - previous) and
        previous are 0 the calculated value is 0. A 10 minute moving mean is
        computed at each point of the time window prior to the above calculation
        to smooth the metric and prevent false positives from very short lived
        spikes. Only applicable for data that is >= 0. Any values < 0 are
        treated as no data. While delta metrics are accepted by this alignment
        special care should be taken that the values for the metric will always
        be positive. The output is a gauge metric with value type ``DOUBLE``.

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
            name (str): Should this field be parsed lazily? Lazy applies only to
                message-type fields. It means that when the outer message is initially
                parsed, the inner message's contents will not be parsed but instead
                stored in encoded form. The inner message will actually be parsed when
                it is first accessed.

                This is only a hint. Implementations are free to choose whether to use
                eager or lazy parsing regardless of the value of this option. However,
                setting this option true suggests that the protocol author believes that
                using lazy parsing on this field is worth the additional bookkeeping
                overhead typically needed to implement it.

                This option does not affect the public interface of any generated code;
                all method signatures remain the same. Furthermore, thread-safety of the
                interface is not affected by this option; const methods remain safe to
                call from multiple threads concurrently, while non-const methods
                continue to require exclusive access.

                Note that implementations may choose not to check required fields within
                a lazy sub-message. That is, calling IsInitialized() on the outer
                message may return true even if the inner message has missing required
                fields. This is necessary because otherwise the inner message would have
                to be parsed in order to perform the check, defeating the purpose of
                lazy parsing. An implementation which chooses not to check required
                fields must be consistent about it. That is, for any particular
                sub-message, the implementation must either *always* check its required
                fields, or *never* check its required fields, regardless of whether or
                not the message has been parsed.
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
        Protocol Buffers - Google's data interchange format Copyright 2008
        Google Inc. All rights reserved.
        https://developers.google.com/protocol-buffers/

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions are
        met:

        ::

            * Redistributions of source code must retain the above copyright

        notice, this list of conditions and the following disclaimer. \*
        Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution. \*
        Neither the name of Google Inc. nor the names of its contributors may be
        used to endorse or promote products derived from this software without
        specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
        IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
        TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
        PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
        OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
        PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
        PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
        LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
        NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
            name (str): The ``CreateDashboard`` request.
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
        Deletes an existing custom dashboard.

        This method requires the ``monitoring.dashboards.delete`` permission on
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
