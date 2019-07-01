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

"""Accesses the google.cloud.dataproc.v1beta2 AutoscalingPolicyService API."""

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

from google.cloud.dataproc_v1beta2.gapic import autoscaling_policy_service_client_config
from google.cloud.dataproc_v1beta2.gapic import enums
from google.cloud.dataproc_v1beta2.gapic.transports import (
    autoscaling_policy_service_grpc_transport,
)
from google.cloud.dataproc_v1beta2.proto import autoscaling_policies_pb2
from google.cloud.dataproc_v1beta2.proto import autoscaling_policies_pb2_grpc
from google.protobuf import empty_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-dataproc").version


class AutoscalingPolicyServiceClient(object):
    """
    The API interface for managing autoscaling policies in the
    Google Cloud Dataproc API.
    """

    SERVICE_ADDRESS = "dataproc.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.dataproc.v1beta2.AutoscalingPolicyService"

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
            AutoscalingPolicyServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def autoscaling_policy_path(cls, project, region, autoscaling_policy):
        """Return a fully-qualified autoscaling_policy string."""
        return google.api_core.path_template.expand(
            "projects/{project}/regions/{region}/autoscalingPolicies/{autoscaling_policy}",
            project=project,
            region=region,
            autoscaling_policy=autoscaling_policy,
        )

    @classmethod
    def region_path(cls, project, region):
        """Return a fully-qualified region string."""
        return google.api_core.path_template.expand(
            "projects/{project}/regions/{region}", project=project, region=region
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
            transport (Union[~.AutoscalingPolicyServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.AutoscalingPolicyServiceGrpcTransport]): A transport
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
            client_config = autoscaling_policy_service_client_config.config

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
                    default_class=autoscaling_policy_service_grpc_transport.AutoscalingPolicyServiceGrpcTransport,
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
            self.transport = autoscaling_policy_service_grpc_transport.AutoscalingPolicyServiceGrpcTransport(
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
    def create_autoscaling_policy(
        self,
        parent,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates new autoscaling policy.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.AutoscalingPolicyServiceClient()
            >>>
            >>> parent = client.region_path('[PROJECT]', '[REGION]')
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.create_autoscaling_policy(parent, policy)

        Args:
            parent (str): Required. The "resource name" of the region, as described in
                https://cloud.google.com/apis/design/resource\_names of the form
                ``projects/{project_id}/regions/{region}``.
            policy (Union[dict, ~google.cloud.dataproc_v1beta2.types.AutoscalingPolicy]): The autoscaling policy to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dataproc_v1beta2.types.AutoscalingPolicy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1beta2.types.AutoscalingPolicy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_autoscaling_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_autoscaling_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_autoscaling_policy,
                default_retry=self._method_configs["CreateAutoscalingPolicy"].retry,
                default_timeout=self._method_configs["CreateAutoscalingPolicy"].timeout,
                client_info=self._client_info,
            )

        request = autoscaling_policies_pb2.CreateAutoscalingPolicyRequest(
            parent=parent, policy=policy
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

        return self._inner_api_calls["create_autoscaling_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_autoscaling_policy(
        self,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates (replaces) autoscaling policy.

        Disabled check for update\_mask, because all updates will be full
        replacements.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.AutoscalingPolicyServiceClient()
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.update_autoscaling_policy(policy)

        Args:
            policy (Union[dict, ~google.cloud.dataproc_v1beta2.types.AutoscalingPolicy]): Required. The updated autoscaling policy.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dataproc_v1beta2.types.AutoscalingPolicy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1beta2.types.AutoscalingPolicy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_autoscaling_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_autoscaling_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_autoscaling_policy,
                default_retry=self._method_configs["UpdateAutoscalingPolicy"].retry,
                default_timeout=self._method_configs["UpdateAutoscalingPolicy"].timeout,
                client_info=self._client_info,
            )

        request = autoscaling_policies_pb2.UpdateAutoscalingPolicyRequest(policy=policy)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("policy.name", policy.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_autoscaling_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_autoscaling_policy(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Retrieves autoscaling policy.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.AutoscalingPolicyServiceClient()
            >>>
            >>> name = client.autoscaling_policy_path('[PROJECT]', '[REGION]', '[AUTOSCALING_POLICY]')
            >>>
            >>> response = client.get_autoscaling_policy(name)

        Args:
            name (str): Required. The "resource name" of the autoscaling policy, as described in
                https://cloud.google.com/apis/design/resource\_names of the form
                ``projects/{project_id}/regions/{region}/autoscalingPolicies/{policy_id}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1beta2.types.AutoscalingPolicy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_autoscaling_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_autoscaling_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_autoscaling_policy,
                default_retry=self._method_configs["GetAutoscalingPolicy"].retry,
                default_timeout=self._method_configs["GetAutoscalingPolicy"].timeout,
                client_info=self._client_info,
            )

        request = autoscaling_policies_pb2.GetAutoscalingPolicyRequest(name=name)
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

        return self._inner_api_calls["get_autoscaling_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_autoscaling_policies(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists autoscaling policies in the project.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.AutoscalingPolicyServiceClient()
            >>>
            >>> parent = client.region_path('[PROJECT]', '[REGION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_autoscaling_policies(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_autoscaling_policies(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The "resource name" of the region, as described in
                https://cloud.google.com/apis/design/resource\_names of the form
                ``projects/{project_id}/regions/{region}``
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.dataproc_v1beta2.types.AutoscalingPolicy` instances.
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
        if "list_autoscaling_policies" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_autoscaling_policies"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_autoscaling_policies,
                default_retry=self._method_configs["ListAutoscalingPolicies"].retry,
                default_timeout=self._method_configs["ListAutoscalingPolicies"].timeout,
                client_info=self._client_info,
            )

        request = autoscaling_policies_pb2.ListAutoscalingPoliciesRequest(
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
                self._inner_api_calls["list_autoscaling_policies"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="policies",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_autoscaling_policy(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an autoscaling policy. It is an error to delete an autoscaling
        policy that is in use by one or more clusters.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.AutoscalingPolicyServiceClient()
            >>>
            >>> name = client.autoscaling_policy_path('[PROJECT]', '[REGION]', '[AUTOSCALING_POLICY]')
            >>>
            >>> client.delete_autoscaling_policy(name)

        Args:
            name (str): Required. The "resource name" of the autoscaling policy, as described in
                https://cloud.google.com/apis/design/resource\_names of the form
                ``projects/{project_id}/regions/{region}/autoscalingPolicies/{policy_id}``.
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
        # Wrap the transport method to add retry and timeout logic.
        if "delete_autoscaling_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_autoscaling_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_autoscaling_policy,
                default_retry=self._method_configs["DeleteAutoscalingPolicy"].retry,
                default_timeout=self._method_configs["DeleteAutoscalingPolicy"].timeout,
                client_info=self._client_info,
            )

        request = autoscaling_policies_pb2.DeleteAutoscalingPolicyRequest(name=name)
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

        self._inner_api_calls["delete_autoscaling_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
