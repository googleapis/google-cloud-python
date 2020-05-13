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

"""Accesses the google.monitoring.v3 UptimeCheckService API."""

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
import google.api_core.path_template
import grpc

from google.api import metric_pb2 as api_metric_pb2
from google.api import monitored_resource_pb2
from google.cloud.monitoring_v3.gapic import enums
from google.cloud.monitoring_v3.gapic import uptime_check_service_client_config
from google.cloud.monitoring_v3.gapic.transports import (
    uptime_check_service_grpc_transport,
)
from google.cloud.monitoring_v3.proto import alert_pb2
from google.cloud.monitoring_v3.proto import alert_service_pb2
from google.cloud.monitoring_v3.proto import alert_service_pb2_grpc
from google.cloud.monitoring_v3.proto import common_pb2
from google.cloud.monitoring_v3.proto import group_pb2
from google.cloud.monitoring_v3.proto import group_service_pb2
from google.cloud.monitoring_v3.proto import group_service_pb2_grpc
from google.cloud.monitoring_v3.proto import metric_pb2 as proto_metric_pb2
from google.cloud.monitoring_v3.proto import metric_service_pb2
from google.cloud.monitoring_v3.proto import metric_service_pb2_grpc
from google.cloud.monitoring_v3.proto import notification_pb2
from google.cloud.monitoring_v3.proto import notification_service_pb2
from google.cloud.monitoring_v3.proto import notification_service_pb2_grpc
from google.cloud.monitoring_v3.proto import service_pb2
from google.cloud.monitoring_v3.proto import service_service_pb2
from google.cloud.monitoring_v3.proto import service_service_pb2_grpc
from google.cloud.monitoring_v3.proto import uptime_pb2
from google.cloud.monitoring_v3.proto import uptime_service_pb2
from google.cloud.monitoring_v3.proto import uptime_service_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-monitoring"
).version


class UptimeCheckServiceClient(object):
    """
    The UptimeCheckService API is used to manage (list, create, delete,
    edit) Uptime check configurations in the Stackdriver Monitoring product.
    An Uptime check is a piece of configuration that determines which
    resources and services to monitor for availability. These configurations
    can also be configured interactively by navigating to the [Cloud
    Console] (http://console.cloud.google.com), selecting the appropriate
    project, clicking on "Monitoring" on the left-hand side to navigate to
    Stackdriver, and then clicking on "Uptime".
    """

    SERVICE_ADDRESS = "monitoring.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.monitoring.v3.UptimeCheckService"

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
            UptimeCheckServiceClient: The constructed client.
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

    @classmethod
    def uptime_check_config_path(cls, project, uptime_check_config):
        """Return a fully-qualified uptime_check_config string."""
        return google.api_core.path_template.expand(
            "projects/{project}/uptimeCheckConfigs/{uptime_check_config}",
            project=project,
            uptime_check_config=uptime_check_config,
        )

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
            transport (Union[~.UptimeCheckServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.UptimeCheckServiceGrpcTransport]): A transport
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
            client_config = uptime_check_service_client_config.config

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
                    default_class=uptime_check_service_grpc_transport.UptimeCheckServiceGrpcTransport,
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
            self.transport = uptime_check_service_grpc_transport.UptimeCheckServiceGrpcTransport(
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
    def list_uptime_check_configs(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the existing valid Uptime check configurations for the project
        (leaving out any invalid configurations).

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_uptime_check_configs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_uptime_check_configs(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The project whose Uptime check configurations are listed.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]
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
            An iterable of :class:`~google.cloud.monitoring_v3.types.UptimeCheckConfig` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

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
        # Wrap the transport method to add retry and timeout logic.
        if "list_uptime_check_configs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_uptime_check_configs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_uptime_check_configs,
                default_retry=self._method_configs["ListUptimeCheckConfigs"].retry,
                default_timeout=self._method_configs["ListUptimeCheckConfigs"].timeout,
                client_info=self._client_info,
            )

        request = uptime_service_pb2.ListUptimeCheckConfigsRequest(
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
                self._inner_api_calls["list_uptime_check_configs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="uptime_check_configs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_uptime_check_config(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a single Uptime check configuration.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>> name = client.uptime_check_config_path('[PROJECT]', '[UPTIME_CHECK_CONFIG]')
            >>>
            >>> response = client.get_uptime_check_config(name)

        Args:
            name (str): Required. The Uptime check configuration to retrieve. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/uptimeCheckConfigs/[UPTIME_CHECK_ID]
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.UptimeCheckConfig` instance.

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
        # Wrap the transport method to add retry and timeout logic.
        if "get_uptime_check_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_uptime_check_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_uptime_check_config,
                default_retry=self._method_configs["GetUptimeCheckConfig"].retry,
                default_timeout=self._method_configs["GetUptimeCheckConfig"].timeout,
                client_info=self._client_info,
            )

        request = uptime_service_pb2.GetUptimeCheckConfigRequest(name=name)
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

        return self._inner_api_calls["get_uptime_check_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_uptime_check_config(
        self,
        parent,
        uptime_check_config,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new Uptime check configuration.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `uptime_check_config`:
            >>> uptime_check_config = {}
            >>>
            >>> response = client.create_uptime_check_config(parent, uptime_check_config)

        Args:
            parent (str): Required. The project in which to create the Uptime check. The
                format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]
            uptime_check_config (Union[dict, ~google.cloud.monitoring_v3.types.UptimeCheckConfig]): Required. The new Uptime check configuration.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.UptimeCheckConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.UptimeCheckConfig` instance.

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
        # Wrap the transport method to add retry and timeout logic.
        if "create_uptime_check_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_uptime_check_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_uptime_check_config,
                default_retry=self._method_configs["CreateUptimeCheckConfig"].retry,
                default_timeout=self._method_configs["CreateUptimeCheckConfig"].timeout,
                client_info=self._client_info,
            )

        request = uptime_service_pb2.CreateUptimeCheckConfigRequest(
            parent=parent, uptime_check_config=uptime_check_config
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

        return self._inner_api_calls["create_uptime_check_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_uptime_check_config(
        self,
        uptime_check_config,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an Uptime check configuration. You can either replace the
        entire configuration with a new one or replace only certain fields in
        the current configuration by specifying the fields to be updated via
        ``updateMask``. Returns the updated configuration.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>> # TODO: Initialize `uptime_check_config`:
            >>> uptime_check_config = {}
            >>>
            >>> response = client.update_uptime_check_config(uptime_check_config)

        Args:
            uptime_check_config (Union[dict, ~google.cloud.monitoring_v3.types.UptimeCheckConfig]): Required. If an ``updateMask`` has been specified, this field gives
                the values for the set of fields mentioned in the ``updateMask``. If an
                ``updateMask`` has not been given, this Uptime check configuration
                replaces the current configuration. If a field is mentioned in
                ``updateMask`` but the corresonding field is omitted in this partial
                Uptime check configuration, it has the effect of deleting/clearing the
                field from the configuration on the server.

                The following fields can be updated: ``display_name``, ``http_check``,
                ``tcp_check``, ``timeout``, ``content_matchers``, and
                ``selected_regions``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.UptimeCheckConfig`
            update_mask (Union[dict, ~google.cloud.monitoring_v3.types.FieldMask]): Optional. If present, only the listed fields in the current Uptime check
                configuration are updated with values from the new configuration. If this
                field is empty, then the current configuration is completely replaced with
                the new configuration.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.UptimeCheckConfig` instance.

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
        # Wrap the transport method to add retry and timeout logic.
        if "update_uptime_check_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_uptime_check_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_uptime_check_config,
                default_retry=self._method_configs["UpdateUptimeCheckConfig"].retry,
                default_timeout=self._method_configs["UpdateUptimeCheckConfig"].timeout,
                client_info=self._client_info,
            )

        request = uptime_service_pb2.UpdateUptimeCheckConfigRequest(
            uptime_check_config=uptime_check_config, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("uptime_check_config.name", uptime_check_config.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_uptime_check_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_uptime_check_config(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an Uptime check configuration. Note that this method will fail
        if the Uptime check configuration is referenced by an alert policy or
        other dependent configs that would be rendered invalid by the deletion.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>> name = client.uptime_check_config_path('[PROJECT]', '[UPTIME_CHECK_CONFIG]')
            >>>
            >>> client.delete_uptime_check_config(name)

        Args:
            name (str): Required. The Uptime check configuration to delete. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/uptimeCheckConfigs/[UPTIME_CHECK_ID]
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        # Wrap the transport method to add retry and timeout logic.
        if "delete_uptime_check_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_uptime_check_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_uptime_check_config,
                default_retry=self._method_configs["DeleteUptimeCheckConfig"].retry,
                default_timeout=self._method_configs["DeleteUptimeCheckConfig"].timeout,
                client_info=self._client_info,
            )

        request = uptime_service_pb2.DeleteUptimeCheckConfigRequest(name=name)
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

        self._inner_api_calls["delete_uptime_check_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_uptime_check_ips(
        self,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns the list of IP addresses that checkers run from

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_uptime_check_ips():
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_uptime_check_ips().pages:
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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.monitoring_v3.types.UptimeCheckIp` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

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
        # Wrap the transport method to add retry and timeout logic.
        if "list_uptime_check_ips" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_uptime_check_ips"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_uptime_check_ips,
                default_retry=self._method_configs["ListUptimeCheckIps"].retry,
                default_timeout=self._method_configs["ListUptimeCheckIps"].timeout,
                client_info=self._client_info,
            )

        request = uptime_service_pb2.ListUptimeCheckIpsRequest(page_size=page_size)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_uptime_check_ips"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="uptime_check_ips",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator
