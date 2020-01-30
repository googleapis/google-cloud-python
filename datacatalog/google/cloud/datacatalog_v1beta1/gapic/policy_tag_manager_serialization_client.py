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

"""Accesses the google.cloud.datacatalog.v1beta1 PolicyTagManagerSerialization API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.protobuf_helpers
import grpc

from google.cloud.datacatalog_v1beta1.gapic import enums
from google.cloud.datacatalog_v1beta1.gapic import (
    policy_tag_manager_serialization_client_config,
)
from google.cloud.datacatalog_v1beta1.gapic.transports import (
    policy_tag_manager_serialization_grpc_transport,
)
from google.cloud.datacatalog_v1beta1.proto import datacatalog_pb2
from google.cloud.datacatalog_v1beta1.proto import datacatalog_pb2_grpc
from google.cloud.datacatalog_v1beta1.proto import policytagmanager_pb2
from google.cloud.datacatalog_v1beta1.proto import policytagmanager_pb2_grpc
from google.cloud.datacatalog_v1beta1.proto import policytagmanagerserialization_pb2
from google.cloud.datacatalog_v1beta1.proto import (
    policytagmanagerserialization_pb2_grpc,
)
from google.cloud.datacatalog_v1beta1.proto import tags_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import options_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-datacatalog"
).version


class PolicyTagManagerSerializationClient(object):
    """
    Policy tag manager serialization API service allows clients to manipulate
    their taxonomies and policy tags data with serialized format.
    """

    SERVICE_ADDRESS = "datacatalog.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.datacatalog.v1beta1.PolicyTagManagerSerialization"

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
            PolicyTagManagerSerializationClient: The constructed client.
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
            transport (Union[~.PolicyTagManagerSerializationGrpcTransport,
                    Callable[[~.Credentials, type], ~.PolicyTagManagerSerializationGrpcTransport]): A transport
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
            client_config = policy_tag_manager_serialization_client_config.config

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
                    default_class=policy_tag_manager_serialization_grpc_transport.PolicyTagManagerSerializationGrpcTransport,
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
            self.transport = policy_tag_manager_serialization_grpc_transport.PolicyTagManagerSerializationGrpcTransport(
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
    def import_taxonomies(
        self,
        parent=None,
        inline_source=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Imports all taxonomies and their policy tags to a project as new
        taxonomies.

        This method provides a bulk taxonomy / policy tag creation using nested
        proto structure.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerSerializationClient()
            >>>
            >>> response = client.import_taxonomies()

        Args:
            parent (str): Required. Resource name of project that the newly created taxonomies will
                belong to.
            inline_source (Union[dict, ~google.cloud.datacatalog_v1beta1.types.InlineSource]): Inline source used for taxonomies import

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.InlineSource`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.ImportTaxonomiesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "import_taxonomies" not in self._inner_api_calls:
            self._inner_api_calls[
                "import_taxonomies"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.import_taxonomies,
                default_retry=self._method_configs["ImportTaxonomies"].retry,
                default_timeout=self._method_configs["ImportTaxonomies"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(inline_source=inline_source)

        request = policytagmanagerserialization_pb2.ImportTaxonomiesRequest(
            parent=parent, inline_source=inline_source
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

        return self._inner_api_calls["import_taxonomies"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def export_taxonomies(
        self,
        parent=None,
        taxonomies=None,
        serialized_taxonomies=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Exports all taxonomies and their policy tags in a project.

        This method generates SerializedTaxonomy protos with nested policy tags
        that can be used as an input for future ImportTaxonomies calls.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.PolicyTagManagerSerializationClient()
            >>>
            >>> response = client.export_taxonomies()

        Args:
            parent (str): Required. Resource name of the project that taxonomies to be exported
                will share.
            taxonomies (list[str]): Required. Resource names of the taxonomies to be exported.
            serialized_taxonomies (bool): Export taxonomies as serialized taxonomies.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.ExportTaxonomiesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "export_taxonomies" not in self._inner_api_calls:
            self._inner_api_calls[
                "export_taxonomies"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.export_taxonomies,
                default_retry=self._method_configs["ExportTaxonomies"].retry,
                default_timeout=self._method_configs["ExportTaxonomies"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            serialized_taxonomies=serialized_taxonomies
        )

        request = policytagmanagerserialization_pb2.ExportTaxonomiesRequest(
            parent=parent,
            taxonomies=taxonomies,
            serialized_taxonomies=serialized_taxonomies,
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

        return self._inner_api_calls["export_taxonomies"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
