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
"""Accesses the google.monitoring.v3 UptimeCheckService API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template

from google.api import metric_pb2 as api_metric_pb2
from google.api import monitored_resource_pb2
from google.cloud.monitoring_v3.gapic import enums
from google.cloud.monitoring_v3.gapic import uptime_check_service_client_config
from google.cloud.monitoring_v3.proto import alert_pb2
from google.cloud.monitoring_v3.proto import alert_service_pb2
from google.cloud.monitoring_v3.proto import common_pb2
from google.cloud.monitoring_v3.proto import group_pb2
from google.cloud.monitoring_v3.proto import group_service_pb2
from google.cloud.monitoring_v3.proto import metric_pb2 as proto_metric_pb2
from google.cloud.monitoring_v3.proto import metric_service_pb2
from google.cloud.monitoring_v3.proto import notification_pb2
from google.cloud.monitoring_v3.proto import notification_service_pb2
from google.cloud.monitoring_v3.proto import uptime_pb2
from google.cloud.monitoring_v3.proto import uptime_service_pb2
from google.cloud.monitoring_v3.proto import uptime_service_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-monitoring', ).version


class UptimeCheckServiceClient(object):
    """
    The UptimeCheckService API is used to manage (list, create, delete, edit)
    uptime check configurations in the Stackdriver Monitoring product. An uptime
    check is a piece of configuration that determines which resources and
    services to monitor for availability. These configurations can also be
    configured interactively by navigating to the [Cloud Console]
    (http://console.cloud.google.com), selecting the appropriate project,
    clicking on \"Monitoring\" on the left-hand side to navigate to Stackdriver,
    and then clicking on \"Uptime\".
    """

    SERVICE_ADDRESS = 'monitoring.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/monitoring',
        'https://www.googleapis.com/auth/monitoring.read',
        'https://www.googleapis.com/auth/monitoring.write',
    )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.monitoring.v3.UptimeCheckService'

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project,
        )

    @classmethod
    def uptime_check_config_path(cls, project, uptime_check_config):
        """Return a fully-qualified uptime_check_config string."""
        return google.api_core.path_template.expand(
            'projects/{project}/uptimeCheckConfigs/{uptime_check_config}',
            project=project,
            uptime_check_config=uptime_check_config,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=uptime_check_service_client_config.config,
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
        self.uptime_check_service_stub = (
            uptime_service_pb2_grpc.UptimeCheckServiceStub(channel))

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
        self._list_uptime_check_configs = google.api_core.gapic_v1.method.wrap_method(
            self.uptime_check_service_stub.ListUptimeCheckConfigs,
            default_retry=method_configs['ListUptimeCheckConfigs'].retry,
            default_timeout=method_configs['ListUptimeCheckConfigs'].timeout,
            client_info=client_info,
        )
        self._get_uptime_check_config = google.api_core.gapic_v1.method.wrap_method(
            self.uptime_check_service_stub.GetUptimeCheckConfig,
            default_retry=method_configs['GetUptimeCheckConfig'].retry,
            default_timeout=method_configs['GetUptimeCheckConfig'].timeout,
            client_info=client_info,
        )
        self._create_uptime_check_config = google.api_core.gapic_v1.method.wrap_method(
            self.uptime_check_service_stub.CreateUptimeCheckConfig,
            default_retry=method_configs['CreateUptimeCheckConfig'].retry,
            default_timeout=method_configs['CreateUptimeCheckConfig'].timeout,
            client_info=client_info,
        )
        self._update_uptime_check_config = google.api_core.gapic_v1.method.wrap_method(
            self.uptime_check_service_stub.UpdateUptimeCheckConfig,
            default_retry=method_configs['UpdateUptimeCheckConfig'].retry,
            default_timeout=method_configs['UpdateUptimeCheckConfig'].timeout,
            client_info=client_info,
        )
        self._delete_uptime_check_config = google.api_core.gapic_v1.method.wrap_method(
            self.uptime_check_service_stub.DeleteUptimeCheckConfig,
            default_retry=method_configs['DeleteUptimeCheckConfig'].retry,
            default_timeout=method_configs['DeleteUptimeCheckConfig'].timeout,
            client_info=client_info,
        )
        self._list_uptime_check_ips = google.api_core.gapic_v1.method.wrap_method(
            self.uptime_check_service_stub.ListUptimeCheckIps,
            default_retry=method_configs['ListUptimeCheckIps'].retry,
            default_timeout=method_configs['ListUptimeCheckIps'].timeout,
            client_info=client_info,
        )

    # Service calls
    def list_uptime_check_configs(
            self,
            parent,
            page_size=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Lists the existing valid uptime check configurations for the project,
        leaving out any invalid configurations.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_uptime_check_configs(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_uptime_check_configs(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The project whose uptime check configurations are listed. The format is

                  ``projects/[PROJECT_ID]``.
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
            is an iterable of :class:`~google.cloud.monitoring_v3.types.UptimeCheckConfig` instances.
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
        request = uptime_service_pb2.ListUptimeCheckConfigsRequest(
            parent=parent,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_uptime_check_configs,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='uptime_check_configs',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_uptime_check_config(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Gets a single uptime check configuration.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>> name = client.uptime_check_config_path('[PROJECT]', '[UPTIME_CHECK_CONFIG]')
            >>>
            >>> response = client.get_uptime_check_config(name)

        Args:
            name (str): The uptime check configuration to retrieve. The format is

                  ``projects/[PROJECT_ID]/uptimeCheckConfigs/[UPTIME_CHECK_ID]``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        request = uptime_service_pb2.GetUptimeCheckConfigRequest(name=name, )
        return self._get_uptime_check_config(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_uptime_check_config(
            self,
            parent,
            uptime_check_config,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Creates a new uptime check configuration.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize ``uptime_check_config``:
            >>> uptime_check_config = {}
            >>>
            >>> response = client.create_uptime_check_config(parent, uptime_check_config)

        Args:
            parent (str): The project in which to create the uptime check. The format is:

                  ``projects/[PROJECT_ID]``.
            uptime_check_config (Union[dict, ~google.cloud.monitoring_v3.types.UptimeCheckConfig]): The new uptime check configuration.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.UptimeCheckConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        request = uptime_service_pb2.CreateUptimeCheckConfigRequest(
            parent=parent,
            uptime_check_config=uptime_check_config,
        )
        return self._create_uptime_check_config(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def update_uptime_check_config(
            self,
            uptime_check_config,
            update_mask=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Updates an uptime check configuration. You can either replace the entire
        configuration with a new one or replace only certain fields in the current
        configuration by specifying the fields to be updated via ``\"updateMask\"``.
        Returns the updated configuration.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>> # TODO: Initialize ``uptime_check_config``:
            >>> uptime_check_config = {}
            >>>
            >>> response = client.update_uptime_check_config(uptime_check_config)

        Args:
            uptime_check_config (Union[dict, ~google.cloud.monitoring_v3.types.UptimeCheckConfig]): Required. If an ``\"updateMask\"`` has been specified, this field gives
                the values for the set of fields mentioned in the ``\"updateMask\"``. If an
                ``\"updateMask\"`` has not been given, this uptime check configuration replaces
                the current configuration. If a field is mentioned in ``\"updateMask``\" but
                the corresonding field is omitted in this partial uptime check
                configuration, it has the effect of deleting/clearing the field from the
                configuration on the server.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.UptimeCheckConfig`
            update_mask (Union[dict, ~google.cloud.monitoring_v3.types.FieldMask]): Optional. If present, only the listed fields in the current uptime check
                configuration are updated with values from the new configuration. If this
                field is empty, then the current configuration is completely replaced with
                the new configuration.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        request = uptime_service_pb2.UpdateUptimeCheckConfigRequest(
            uptime_check_config=uptime_check_config,
            update_mask=update_mask,
        )
        return self._update_uptime_check_config(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_uptime_check_config(
            self,
            name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Deletes an uptime check configuration. Note that this method will fail
        if the uptime check configuration is referenced by an alert policy or
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
            name (str): The uptime check configuration to delete. The format is

                  ``projects/[PROJECT_ID]/uptimeCheckConfigs/[UPTIME_CHECK_ID]``.
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
        request = uptime_service_pb2.DeleteUptimeCheckConfigRequest(
            name=name, )
        self._delete_uptime_check_config(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_uptime_check_ips(self,
                              page_size=None,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT,
                              metadata=None):
        """
        Returns the list of IPs that checkers run from

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.UptimeCheckServiceClient()
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_uptime_check_ips():
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_uptime_check_ips(options=CallOptions(page_token=INITIAL_PAGE)):
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
            is an iterable of :class:`~google.cloud.monitoring_v3.types.UptimeCheckIp` instances.
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
        request = uptime_service_pb2.ListUptimeCheckIpsRequest(
            page_size=page_size, )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_uptime_check_ips,
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='uptime_check_ips',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator
