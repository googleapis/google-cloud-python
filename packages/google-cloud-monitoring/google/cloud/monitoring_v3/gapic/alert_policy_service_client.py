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

"""Accesses the google.monitoring.v3 AlertPolicyService API."""

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

from google.cloud.monitoring_v3.gapic import alert_policy_service_client_config
from google.cloud.monitoring_v3.gapic import enums
from google.cloud.monitoring_v3.gapic.transports import (
    alert_policy_service_grpc_transport,
)
from google.cloud.monitoring_v3.proto import alert_pb2
from google.cloud.monitoring_v3.proto import alert_service_pb2
from google.cloud.monitoring_v3.proto import alert_service_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-monitoring"
).version


class AlertPolicyServiceClient(object):
    """
    The AlertPolicyService API is used to manage (list, create, delete,
    edit) alert policies in Stackdriver Monitoring. An alerting policy is a
    description of the conditions under which some aspect of your system is
    considered to be "unhealthy" and the ways to notify people or services
    about this state. In addition to using this API, alert policies can also
    be managed through `Stackdriver
    Monitoring <https://cloud.google.com/monitoring/docs/>`__, which can be
    reached by clicking the "Monitoring" tab in `Cloud
    Console <https://console.cloud.google.com/>`__.
    """

    SERVICE_ADDRESS = "monitoring.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.monitoring.v3.AlertPolicyService"

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
            AlertPolicyServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def alert_policy_path(cls, project, alert_policy):
        """Return a fully-qualified alert_policy string."""
        return google.api_core.path_template.expand(
            "projects/{project}/alertPolicies/{alert_policy}",
            project=project,
            alert_policy=alert_policy,
        )

    @classmethod
    def alert_policy_condition_path(cls, project, alert_policy, condition):
        """Return a fully-qualified alert_policy_condition string."""
        return google.api_core.path_template.expand(
            "projects/{project}/alertPolicies/{alert_policy}/conditions/{condition}",
            project=project,
            alert_policy=alert_policy,
            condition=condition,
        )

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
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.AlertPolicyServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.AlertPolicyServiceGrpcTransport]): A transport
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
            client_config = alert_policy_service_client_config.config

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
                    default_class=alert_policy_service_grpc_transport.AlertPolicyServiceGrpcTransport,
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
            self.transport = alert_policy_service_grpc_transport.AlertPolicyServiceGrpcTransport(
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
    def list_alert_policies(
        self,
        name,
        filter_=None,
        order_by=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the existing alerting policies for the project.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.AlertPolicyServiceClient()
            >>>
            >>> name = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_alert_policies(name):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_alert_policies(name).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            name (str): Required. The project whose alert policies are to be listed. The
                format is:

                    projects/[PROJECT_ID_OR_NUMBER]

                Note that this field names the parent container in which the alerting
                policies to be listed are stored. To retrieve a single alerting policy
                by name, use the ``GetAlertPolicy`` operation, instead.
            filter_ (str): If provided, this field specifies the criteria that must be met by
                alert policies to be included in the response.

                For more details, see `sorting and
                filtering <https://cloud.google.com/monitoring/api/v3/sorting-and-filtering>`__.
            order_by (str): A comma-separated list of fields by which to sort the result.
                Supports the same set of field references as the ``filter`` field.
                Entries can be prefixed with a minus sign to sort by the field in
                descending order.

                For more details, see `sorting and
                filtering <https://cloud.google.com/monitoring/api/v3/sorting-and-filtering>`__.
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
            An iterable of :class:`~google.cloud.monitoring_v3.types.AlertPolicy` instances.
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
        if "list_alert_policies" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_alert_policies"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_alert_policies,
                default_retry=self._method_configs["ListAlertPolicies"].retry,
                default_timeout=self._method_configs["ListAlertPolicies"].timeout,
                client_info=self._client_info,
            )

        request = alert_service_pb2.ListAlertPoliciesRequest(
            name=name, filter=filter_, order_by=order_by, page_size=page_size
        )
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

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_alert_policies"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="alert_policies",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_alert_policy(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a single alerting policy.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.AlertPolicyServiceClient()
            >>>
            >>> name = client.alert_policy_path('[PROJECT]', '[ALERT_POLICY]')
            >>>
            >>> response = client.get_alert_policy(name)

        Args:
            name (str): Required. The alerting policy to retrieve. The format is:

                    projects/[PROJECT_ID_OR_NUMBER]/alertPolicies/[ALERT_POLICY_ID]
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.AlertPolicy` instance.

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
        if "get_alert_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_alert_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_alert_policy,
                default_retry=self._method_configs["GetAlertPolicy"].retry,
                default_timeout=self._method_configs["GetAlertPolicy"].timeout,
                client_info=self._client_info,
            )

        request = alert_service_pb2.GetAlertPolicyRequest(name=name)
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

        return self._inner_api_calls["get_alert_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_alert_policy(
        self,
        name,
        alert_policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new alerting policy.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.AlertPolicyServiceClient()
            >>>
            >>> name = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `alert_policy`:
            >>> alert_policy = {}
            >>>
            >>> response = client.create_alert_policy(name, alert_policy)

        Args:
            name (str): Required. The project in which to create the alerting policy. The
                format is:

                    projects/[PROJECT_ID_OR_NUMBER]

                Note that this field names the parent container in which the alerting
                policy will be written, not the name of the created policy. The alerting
                policy that is returned will have a name that contains a normalized
                representation of this name as a prefix but adds a suffix of the form
                ``/alertPolicies/[ALERT_POLICY_ID]``, identifying the policy in the
                container.
            alert_policy (Union[dict, ~google.cloud.monitoring_v3.types.AlertPolicy]): Required. The requested alerting policy. You should omit the
                ``name`` field in this policy. The name will be returned in the new
                policy, including a new ``[ALERT_POLICY_ID]`` value.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.AlertPolicy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.monitoring_v3.types.AlertPolicy` instance.

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
        if "create_alert_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_alert_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_alert_policy,
                default_retry=self._method_configs["CreateAlertPolicy"].retry,
                default_timeout=self._method_configs["CreateAlertPolicy"].timeout,
                client_info=self._client_info,
            )

        request = alert_service_pb2.CreateAlertPolicyRequest(
            name=name, alert_policy=alert_policy
        )
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

        return self._inner_api_calls["create_alert_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_alert_policy(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an alerting policy.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.AlertPolicyServiceClient()
            >>>
            >>> name = client.alert_policy_path('[PROJECT]', '[ALERT_POLICY]')
            >>>
            >>> client.delete_alert_policy(name)

        Args:
            name (str): Required. The alerting policy to delete. The format is:

                    projects/[PROJECT_ID_OR_NUMBER]/alertPolicies/[ALERT_POLICY_ID]

                For more information, see ``AlertPolicy``.
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
        if "delete_alert_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_alert_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_alert_policy,
                default_retry=self._method_configs["DeleteAlertPolicy"].retry,
                default_timeout=self._method_configs["DeleteAlertPolicy"].timeout,
                client_info=self._client_info,
            )

        request = alert_service_pb2.DeleteAlertPolicyRequest(name=name)
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

        self._inner_api_calls["delete_alert_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_alert_policy(
        self,
        alert_policy,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an alerting policy. You can either replace the entire policy
        with a new one or replace only certain fields in the current alerting
        policy by specifying the fields to be updated via ``updateMask``.
        Returns the updated alerting policy.

        Example:
            >>> from google.cloud import monitoring_v3
            >>>
            >>> client = monitoring_v3.AlertPolicyServiceClient()
            >>>
            >>> # TODO: Initialize `alert_policy`:
            >>> alert_policy = {}
            >>>
            >>> response = client.update_alert_policy(alert_policy)

        Args:
            alert_policy (Union[dict, ~google.cloud.monitoring_v3.types.AlertPolicy]): Required. The updated alerting policy or the updated values for the
                fields listed in ``update_mask``. If ``update_mask`` is not empty, any
                fields in this policy that are not in ``update_mask`` are ignored.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.monitoring_v3.types.AlertPolicy`
            update_mask (Union[dict, ~google.cloud.monitoring_v3.types.FieldMask]): Optional. A list of alerting policy field names. If this field is
                not empty, each listed field in the existing alerting policy is set to
                the value of the corresponding field in the supplied policy
                (``alert_policy``), or to the field's default value if the field is not
                in the supplied alerting policy. Fields not listed retain their previous
                value.

                Examples of valid field masks include ``display_name``,
                ``documentation``, ``documentation.content``,
                ``documentation.mime_type``, ``user_labels``, ``user_label.nameofkey``,
                ``enabled``, ``conditions``, ``combiner``, etc.

                If this field is empty, then the supplied alerting policy replaces the
                existing policy. It is the same as deleting the existing policy and
                adding the supplied policy, except for the following:

                -  The new policy will have the same ``[ALERT_POLICY_ID]`` as the former
                   policy. This gives you continuity with the former policy in your
                   notifications and incidents.
                -  Conditions in the new policy will keep their former
                   ``[CONDITION_ID]`` if the supplied condition includes the ``name``
                   field with that ``[CONDITION_ID]``. If the supplied condition omits
                   the ``name`` field, then a new ``[CONDITION_ID]`` is created.

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
            A :class:`~google.cloud.monitoring_v3.types.AlertPolicy` instance.

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
        if "update_alert_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_alert_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_alert_policy,
                default_retry=self._method_configs["UpdateAlertPolicy"].retry,
                default_timeout=self._method_configs["UpdateAlertPolicy"].timeout,
                client_info=self._client_info,
            )

        request = alert_service_pb2.UpdateAlertPolicyRequest(
            alert_policy=alert_policy, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("alert_policy.name", alert_policy.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_alert_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
