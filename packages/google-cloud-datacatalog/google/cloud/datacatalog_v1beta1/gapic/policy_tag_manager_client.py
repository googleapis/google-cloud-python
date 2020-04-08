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

"""Accesses the google.cloud.datacatalog.v1beta1 PolicyTagManager API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import grpc

from google.cloud.datacatalog_v1beta1.gapic import enums
from google.cloud.datacatalog_v1beta1.gapic import policy_tag_manager_client_config
from google.cloud.datacatalog_v1beta1.gapic.transports import (
    policy_tag_manager_grpc_transport,
)
from google.cloud.datacatalog_v1beta1.proto import datacatalog_pb2
from google.cloud.datacatalog_v1beta1.proto import datacatalog_pb2_grpc
from google.cloud.datacatalog_v1beta1.proto import policytagmanager_pb2
from google.cloud.datacatalog_v1beta1.proto import policytagmanager_pb2_grpc
from google.cloud.datacatalog_v1beta1.proto import tags_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import options_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-datacatalog"
).version


class PolicyTagManagerClient(object):
    """
    The policy tag manager API service allows clients to manage their taxonomies
    and policy tags.
    """

    SERVICE_ADDRESS = "datacatalog.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.datacatalog.v1beta1.PolicyTagManager"

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
            PolicyTagManagerClient: The constructed client.
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
            transport (Union[~.PolicyTagManagerGrpcTransport,
                    Callable[[~.Credentials, type], ~.PolicyTagManagerGrpcTransport]): A transport
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
            client_config = policy_tag_manager_client_config.config

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
                    default_class=policy_tag_manager_grpc_transport.PolicyTagManagerGrpcTransport,
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
            self.transport = policy_tag_manager_grpc_transport.PolicyTagManagerGrpcTransport(
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
    def create_taxonomy(
        self,
        parent=None,
        taxonomy=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a taxonomy in the specified project.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.create_taxonomy()

        Args:
            parent (str): Required. Resource name of the project that the taxonomy will belong to.
            taxonomy (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Taxonomy]): The taxonomy to be created.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Taxonomy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.Taxonomy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_taxonomy" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_taxonomy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_taxonomy,
                default_retry=self._method_configs["CreateTaxonomy"].retry,
                default_timeout=self._method_configs["CreateTaxonomy"].timeout,
                client_info=self._client_info,
            )

        request = policytagmanager_pb2.CreateTaxonomyRequest(
            parent=parent, taxonomy=taxonomy
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

        return self._inner_api_calls["create_taxonomy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_taxonomy(
        self,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a taxonomy. This operation will also delete all
        policy tags in this taxonomy along with their associated policies.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> client.delete_taxonomy()

        Args:
            name (str): Required. Resource name of the taxonomy to be deleted. All policy tags in
                this taxonomy will also be deleted.
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
        if "delete_taxonomy" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_taxonomy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_taxonomy,
                default_retry=self._method_configs["DeleteTaxonomy"].retry,
                default_timeout=self._method_configs["DeleteTaxonomy"].timeout,
                client_info=self._client_info,
            )

        request = policytagmanager_pb2.DeleteTaxonomyRequest(name=name)
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

        self._inner_api_calls["delete_taxonomy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_taxonomy(
        self,
        taxonomy=None,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a taxonomy.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.update_taxonomy()

        Args:
            taxonomy (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Taxonomy]): The taxonomy to update. Only description, display_name, and
                activated policy types can be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Taxonomy`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): The update mask applies to the resource. For the ``FieldMask``
                definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
                If not set, defaults to all of the fields that are allowed to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.Taxonomy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_taxonomy" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_taxonomy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_taxonomy,
                default_retry=self._method_configs["UpdateTaxonomy"].retry,
                default_timeout=self._method_configs["UpdateTaxonomy"].timeout,
                client_info=self._client_info,
            )

        request = policytagmanager_pb2.UpdateTaxonomyRequest(
            taxonomy=taxonomy, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("taxonomy.name", taxonomy.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_taxonomy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_taxonomies(
        self,
        parent=None,
        page_size=None,
        page_token=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all taxonomies in a project in a particular location that the caller
        has permission to view.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.list_taxonomies()

        Args:
            parent (str): Required. Resource name of the project to list the taxonomies of.
            page_size (int): The maximum number of items to return. Must be a value between 1 and 1000.
                If not set, defaults to 50.
            page_token (str): The next_page_token value returned from a previous list request, if
                any. If not set, defaults to an empty string.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.ListTaxonomiesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_taxonomies" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_taxonomies"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_taxonomies,
                default_retry=self._method_configs["ListTaxonomies"].retry,
                default_timeout=self._method_configs["ListTaxonomies"].timeout,
                client_info=self._client_info,
            )

        request = policytagmanager_pb2.ListTaxonomiesRequest(
            parent=parent, page_size=page_size, page_token=page_token
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

        return self._inner_api_calls["list_taxonomies"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_taxonomy(
        self,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a taxonomy.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.get_taxonomy()

        Args:
            name (str): Required. Resource name of the requested taxonomy.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.Taxonomy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_taxonomy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_taxonomy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_taxonomy,
                default_retry=self._method_configs["GetTaxonomy"].retry,
                default_timeout=self._method_configs["GetTaxonomy"].timeout,
                client_info=self._client_info,
            )

        request = policytagmanager_pb2.GetTaxonomyRequest(name=name)
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

        return self._inner_api_calls["get_taxonomy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_policy_tag(
        self,
        parent=None,
        policy_tag=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a policy tag in the specified taxonomy.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.create_policy_tag()

        Args:
            parent (str): Required. Resource name of the taxonomy that the policy tag will belong to.
            policy_tag (Union[dict, ~google.cloud.datacatalog_v1beta1.types.PolicyTag]): The policy tag to be created.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.PolicyTag`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.PolicyTag` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_policy_tag" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_policy_tag"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_policy_tag,
                default_retry=self._method_configs["CreatePolicyTag"].retry,
                default_timeout=self._method_configs["CreatePolicyTag"].timeout,
                client_info=self._client_info,
            )

        request = policytagmanager_pb2.CreatePolicyTagRequest(
            parent=parent, policy_tag=policy_tag
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

        return self._inner_api_calls["create_policy_tag"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_policy_tag(
        self,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a policy tag. Also deletes all of its descendant policy tags.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> client.delete_policy_tag()

        Args:
            name (str): Required. Resource name of the policy tag to be deleted. All of its descendant
                policy tags will also be deleted.
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
        if "delete_policy_tag" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_policy_tag"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_policy_tag,
                default_retry=self._method_configs["DeletePolicyTag"].retry,
                default_timeout=self._method_configs["DeletePolicyTag"].timeout,
                client_info=self._client_info,
            )

        request = policytagmanager_pb2.DeletePolicyTagRequest(name=name)
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

        self._inner_api_calls["delete_policy_tag"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_policy_tag(
        self,
        policy_tag=None,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a policy tag.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.update_policy_tag()

        Args:
            policy_tag (Union[dict, ~google.cloud.datacatalog_v1beta1.types.PolicyTag]): The policy tag to update. Only the description, display_name, and
                parent_policy_tag fields can be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.PolicyTag`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): The update mask applies to the resource. Only display_name,
                description and parent_policy_tag can be updated and thus can be listed
                in the mask. If update_mask is not provided, all allowed fields (i.e.
                display_name, description and parent) will be updated. For more
                information including the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
                If not set, defaults to all of the fields that are allowed to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.PolicyTag` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_policy_tag" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_policy_tag"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_policy_tag,
                default_retry=self._method_configs["UpdatePolicyTag"].retry,
                default_timeout=self._method_configs["UpdatePolicyTag"].timeout,
                client_info=self._client_info,
            )

        request = policytagmanager_pb2.UpdatePolicyTagRequest(
            policy_tag=policy_tag, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("policy_tag.name", policy_tag.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_policy_tag"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_policy_tags(
        self,
        parent=None,
        page_size=None,
        page_token=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all policy tags in a taxonomy.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.list_policy_tags()

        Args:
            parent (str): Required. Resource name of the taxonomy to list the policy tags of.
            page_size (int): The maximum number of items to return. Must be a value between 1 and 1000.
                If not set, defaults to 50.
            page_token (str): The next_page_token value returned from a previous List request, if
                any. If not set, defaults to an empty string.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.ListPolicyTagsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_policy_tags" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_policy_tags"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_policy_tags,
                default_retry=self._method_configs["ListPolicyTags"].retry,
                default_timeout=self._method_configs["ListPolicyTags"].timeout,
                client_info=self._client_info,
            )

        request = policytagmanager_pb2.ListPolicyTagsRequest(
            parent=parent, page_size=page_size, page_token=page_token
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

        return self._inner_api_calls["list_policy_tags"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_policy_tag(
        self,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a policy tag.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.get_policy_tag()

        Args:
            name (str): Required. Resource name of the requested policy tag.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.PolicyTag` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_policy_tag" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_policy_tag"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_policy_tag,
                default_retry=self._method_configs["GetPolicyTag"].retry,
                default_timeout=self._method_configs["GetPolicyTag"].timeout,
                client_info=self._client_info,
            )

        request = policytagmanager_pb2.GetPolicyTagRequest(name=name)
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

        return self._inner_api_calls["get_policy_tag"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_iam_policy(
        self,
        resource=None,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the IAM policy for a taxonomy or a policy tag.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.get_iam_policy()

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                See the operation documentation for the appropriate value for this field.
            options_ (Union[dict, ~google.cloud.datacatalog_v1beta1.types.GetPolicyOptions]): OPTIONAL: A ``GetPolicyOptions`` object for specifying options to
                ``GetIamPolicy``. This field is only used by Cloud IAM.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.GetPolicyOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_iam_policy,
                default_retry=self._method_configs["GetIamPolicy"].retry,
                default_timeout=self._method_configs["GetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.GetIamPolicyRequest(
            resource=resource, options=options_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_iam_policy(
        self,
        resource=None,
        policy=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the IAM policy for a taxonomy or a policy tag.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.set_iam_policy()

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                See the operation documentation for the appropriate value for this field.
            policy (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_iam_policy,
                default_retry=self._method_configs["SetIamPolicy"].retry,
                default_timeout=self._method_configs["SetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.SetIamPolicyRequest(resource=resource, policy=policy)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def test_iam_permissions(
        self,
        resource=None,
        permissions=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns the permissions that a caller has on the specified taxonomy or
        policy tag.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerClient()
            >>>
            >>> response = client.test_iam_permissions()

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                See the operation documentation for the appropriate value for this field.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions
                with wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "test_iam_permissions" not in self._inner_api_calls:
            self._inner_api_calls[
                "test_iam_permissions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.test_iam_permissions,
                default_retry=self._method_configs["TestIamPermissions"].retry,
                default_timeout=self._method_configs["TestIamPermissions"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["test_iam_permissions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
