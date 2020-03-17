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

"""Accesses the google.cloud.asset.v1 AssetService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.path_template
import grpc

from google.cloud.asset_v1.gapic import asset_service_client_config
from google.cloud.asset_v1.gapic import enums
from google.cloud.asset_v1.gapic.transports import asset_service_grpc_transport
from google.cloud.asset_v1.proto import asset_service_pb2
from google.cloud.asset_v1.proto import asset_service_pb2_grpc
from google.cloud.asset_v1.proto import assets_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-asset").version


class AssetServiceClient(object):
    """Asset service definition."""

    SERVICE_ADDRESS = "cloudasset.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.asset.v1.AssetService"

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
            AssetServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def feed_path(cls, project, feed):
        """Return a fully-qualified feed string."""
        return google.api_core.path_template.expand(
            "projects/{project}/feeds/{feed}", project=project, feed=feed
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
            transport (Union[~.AssetServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.AssetServiceGrpcTransport]): A transport
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
            client_config = asset_service_client_config.config

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
                    default_class=asset_service_grpc_transport.AssetServiceGrpcTransport,
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
            self.transport = asset_service_grpc_transport.AssetServiceGrpcTransport(
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
    def export_assets(
        self,
        parent,
        output_config,
        read_time=None,
        asset_types=None,
        content_type=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Additional information regarding long-running operations. In
        particular, this specifies the types that are returned from long-running
        operations.

        Required for methods that return ``google.longrunning.Operation``;
        invalid otherwise.

        Example:
            >>> from google.cloud import asset_v1
            >>>
            >>> client = asset_v1.AssetServiceClient()
            >>>
            >>> # TODO: Initialize `parent`:
            >>> parent = ''
            >>>
            >>> # TODO: Initialize `output_config`:
            >>> output_config = {}
            >>>
            >>> response = client.export_assets(parent, output_config)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): Required. The relative name of the root asset. This can only be an
                organization number (such as "organizations/123"), a project ID (such as
                "projects/my-project-id"), or a project number (such as "projects/12345"),
                or a folder number (such as "folders/123").
            output_config (Union[dict, ~google.cloud.asset_v1.types.OutputConfig]): Required. Output configuration indicating where the results will be output
                to. All results will be in newline delimited JSON format.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.asset_v1.types.OutputConfig`
            read_time (Union[dict, ~google.cloud.asset_v1.types.Timestamp]): Timestamp to take an asset snapshot. This can only be set to a timestamp
                between 2018-10-02 UTC (inclusive) and the current time. If not specified,
                the current time will be used. Due to delays in resource data collection
                and indexing, there is a volatile window during which running the same
                query may get different results.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.asset_v1.types.Timestamp`
            asset_types (list[str]): A list of asset types of which to take a snapshot for. For example:
                "compute.googleapis.com/Disk". If specified, only matching assets will
                be returned. See `Introduction to Cloud Asset
                Inventory <https://cloud.google.com/asset-inventory/docs/overview>`__
                for all supported asset types.
            content_type (~google.cloud.asset_v1.types.ContentType): Asset content type. If not specified, no content but the asset name will be
                returned.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.asset_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "export_assets" not in self._inner_api_calls:
            self._inner_api_calls[
                "export_assets"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.export_assets,
                default_retry=self._method_configs["ExportAssets"].retry,
                default_timeout=self._method_configs["ExportAssets"].timeout,
                client_info=self._client_info,
            )

        request = asset_service_pb2.ExportAssetsRequest(
            parent=parent,
            output_config=output_config,
            read_time=read_time,
            asset_types=asset_types,
            content_type=content_type,
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

        operation = self._inner_api_calls["export_assets"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            asset_service_pb2.ExportAssetsResponse,
            metadata_type=asset_service_pb2.ExportAssetsRequest,
        )

    def batch_get_assets_history(
        self,
        parent,
        content_type,
        read_time_window,
        asset_names=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        JSON name of this field. The value is set by protocol compiler. If
        the user has set a "json_name" option on this field, that option's value
        will be used. Otherwise, it's deduced from the field's name by
        converting it to camelCase.

        Example:
            >>> from google.cloud import asset_v1
            >>> from google.cloud.asset_v1 import enums
            >>>
            >>> client = asset_v1.AssetServiceClient()
            >>>
            >>> # TODO: Initialize `parent`:
            >>> parent = ''
            >>>
            >>> # TODO: Initialize `content_type`:
            >>> content_type = enums.ContentType.CONTENT_TYPE_UNSPECIFIED
            >>>
            >>> # TODO: Initialize `read_time_window`:
            >>> read_time_window = {}
            >>>
            >>> response = client.batch_get_assets_history(parent, content_type, read_time_window)

        Args:
            parent (str): Required. The relative name of the root asset. It can only be an
                organization number (such as "organizations/123"), a project ID (such as
                "projects/my-project-id")", or a project number (such as "projects/12345").
            content_type (~google.cloud.asset_v1.types.ContentType): Optional. The content type.
            read_time_window (Union[dict, ~google.cloud.asset_v1.types.TimeWindow]): Manages long-running operations with an API service.

                When an API method normally takes long time to complete, it can be
                designed to return ``Operation`` to the client, and the client can use
                this interface to receive the real response asynchronously by polling
                the operation resource, or pass the operation resource to another API
                (such as Google Cloud Pub/Sub API) to receive the response. Any API
                service that returns long-running operations should implement the
                ``Operations`` interface so developers can have a consistent client
                experience.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.asset_v1.types.TimeWindow`
            asset_names (list[str]): The resource has one pattern, but the API owner expects to add more
                later. (This is the inverse of ORIGINALLY_SINGLE_PATTERN, and prevents
                that from being necessary once there are multiple patterns.)
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.asset_v1.types.BatchGetAssetsHistoryResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_get_assets_history" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_get_assets_history"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_get_assets_history,
                default_retry=self._method_configs["BatchGetAssetsHistory"].retry,
                default_timeout=self._method_configs["BatchGetAssetsHistory"].timeout,
                client_info=self._client_info,
            )

        request = asset_service_pb2.BatchGetAssetsHistoryRequest(
            parent=parent,
            content_type=content_type,
            read_time_window=read_time_window,
            asset_names=asset_names,
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

        return self._inner_api_calls["batch_get_assets_history"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_feed(
        self,
        parent,
        feed_id,
        feed,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a feed in a parent project/folder/organization to listen to its
        asset updates.

        Example:
            >>> from google.cloud import asset_v1
            >>>
            >>> client = asset_v1.AssetServiceClient()
            >>>
            >>> # TODO: Initialize `parent`:
            >>> parent = ''
            >>>
            >>> # TODO: Initialize `feed_id`:
            >>> feed_id = ''
            >>>
            >>> # TODO: Initialize `feed`:
            >>> feed = {}
            >>>
            >>> response = client.create_feed(parent, feed_id, feed)

        Args:
            parent (str): Required. The name of the project/folder/organization where this feed
                should be created in. It can only be an organization number (such as
                "organizations/123"), a folder number (such as "folders/123"), a project ID
                (such as "projects/my-project-id")", or a project number (such as
                "projects/12345").
            feed_id (str): Required. This is the client-assigned asset feed identifier and it needs to
                be unique under a specific parent project/folder/organization.
            feed (Union[dict, ~google.cloud.asset_v1.types.Feed]): Each of the definitions above may have "options" attached. These are
                just annotations which may cause code to be generated slightly
                differently or may contain hints for code that manipulates protocol
                messages.

                Clients may define custom options as extensions of the \*Options
                messages. These extensions may not yet be known at parsing time, so the
                parser cannot store the values in them. Instead it stores them in a
                field in the \*Options message called uninterpreted_option. This field
                must have the same name across all \*Options messages. We then use this
                field to populate the extensions when we build a descriptor, at which
                point all protos have been parsed and so all extensions are known.

                Extension numbers for custom options may be chosen as follows:

                -  For options which will only be used within a single application or
                   organization, or for experimental options, use field numbers 50000
                   through 99999. It is up to you to ensure that you do not use the same
                   number for multiple options.
                -  For options which will be published and used publicly by multiple
                   independent entities, e-mail
                   protobuf-global-extension-registry@google.com to reserve extension
                   numbers. Simply provide your project name (e.g. Objective-C plugin)
                   and your project website (if available) -- there's no need to explain
                   how you intend to use them. Usually you only need one extension
                   number. You can declare multiple options with only one extension
                   number by putting them in a sub-message. See the Custom Options
                   section of the docs for examples:
                   https://developers.google.com/protocol-buffers/docs/proto#options If
                   this turns out to be popular, a web service will be set up to
                   automatically assign option numbers.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.asset_v1.types.Feed`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.asset_v1.types.Feed` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_feed" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_feed"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_feed,
                default_retry=self._method_configs["CreateFeed"].retry,
                default_timeout=self._method_configs["CreateFeed"].timeout,
                client_info=self._client_info,
            )

        request = asset_service_pb2.CreateFeedRequest(
            parent=parent, feed_id=feed_id, feed=feed
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

        return self._inner_api_calls["create_feed"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_feed(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets details about an asset feed.

        Example:
            >>> from google.cloud import asset_v1
            >>>
            >>> client = asset_v1.AssetServiceClient()
            >>>
            >>> name = client.feed_path('[PROJECT]', '[FEED]')
            >>>
            >>> response = client.get_feed(name)

        Args:
            name (str): The resource type. It must be in the format of
                {service_name}/{resource_type_kind}. The ``resource_type_kind`` must be
                singular and must not include version numbers.

                Example: ``storage.googleapis.com/Bucket``

                The value of the resource_type_kind must follow the regular expression
                /[A-Za-z][a-zA-Z0-9]+/. It should start with an upper case character and
                should use PascalCase (UpperCamelCase). The maximum number of characters
                allowed for the ``resource_type_kind`` is 100.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.asset_v1.types.Feed` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_feed" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_feed"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_feed,
                default_retry=self._method_configs["GetFeed"].retry,
                default_timeout=self._method_configs["GetFeed"].timeout,
                client_info=self._client_info,
            )

        request = asset_service_pb2.GetFeedRequest(name=name)
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

        return self._inner_api_calls["get_feed"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_feeds(
        self,
        parent,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all asset feeds in a parent project/folder/organization.

        Example:
            >>> from google.cloud import asset_v1
            >>>
            >>> client = asset_v1.AssetServiceClient()
            >>>
            >>> # TODO: Initialize `parent`:
            >>> parent = ''
            >>>
            >>> response = client.list_feeds(parent)

        Args:
            parent (str): Required. The parent project/folder/organization whose feeds are to be
                listed. It can only be using project/folder/organization number (such as
                "folders/12345")", or a project ID (such as "projects/my-project-id").
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.asset_v1.types.ListFeedsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_feeds" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_feeds"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_feeds,
                default_retry=self._method_configs["ListFeeds"].retry,
                default_timeout=self._method_configs["ListFeeds"].timeout,
                client_info=self._client_info,
            )

        request = asset_service_pb2.ListFeedsRequest(parent=parent)
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

        return self._inner_api_calls["list_feeds"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_feed(
        self,
        feed,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an asset feed configuration.

        Example:
            >>> from google.cloud import asset_v1
            >>>
            >>> client = asset_v1.AssetServiceClient()
            >>>
            >>> # TODO: Initialize `feed`:
            >>> feed = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_feed(feed, update_mask)

        Args:
            feed (Union[dict, ~google.cloud.asset_v1.types.Feed]): See ``HttpRule``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.asset_v1.types.Feed`
            update_mask (Union[dict, ~google.cloud.asset_v1.types.FieldMask]): A URL/resource name that uniquely identifies the type of the
                serialized protocol buffer message. This string must contain at least
                one "/" character. The last segment of the URL's path must represent the
                fully qualified name of the type (as in
                ``path/google.protobuf.Duration``). The name should be in a canonical
                form (e.g., leading "." is not accepted).

                In practice, teams usually precompile into the binary all types that
                they expect it to use in the context of Any. However, for URLs which use
                the scheme ``http``, ``https``, or no scheme, one can optionally set up
                a type server that maps type URLs to message definitions as follows:

                -  If no scheme is provided, ``https`` is assumed.
                -  An HTTP GET on the URL must yield a ``google.protobuf.Type`` value in
                   binary format, or produce an error.
                -  Applications are allowed to cache lookup results based on the URL, or
                   have them precompiled into a binary to avoid any lookup. Therefore,
                   binary compatibility needs to be preserved on changes to types. (Use
                   versioned type names to manage breaking changes.)

                Note: this functionality is not currently available in the official
                protobuf release, and it is not used for type URLs beginning with
                type.googleapis.com.

                Schemes other than ``http``, ``https`` (or the empty scheme) might be
                used with implementation specific semantics.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.asset_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.asset_v1.types.Feed` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_feed" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_feed"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_feed,
                default_retry=self._method_configs["UpdateFeed"].retry,
                default_timeout=self._method_configs["UpdateFeed"].timeout,
                client_info=self._client_info,
            )

        request = asset_service_pb2.UpdateFeedRequest(
            feed=feed, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("feed.name", feed.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_feed"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_feed(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an asset feed.

        Example:
            >>> from google.cloud import asset_v1
            >>>
            >>> client = asset_v1.AssetServiceClient()
            >>>
            >>> name = client.feed_path('[PROJECT]', '[FEED]')
            >>>
            >>> client.delete_feed(name)

        Args:
            name (str): A list of the full names of the assets. For example:
                ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.
                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
                and `Resource Name
                Format <https://cloud.google.com/asset-inventory/docs/resource-name-format>`__
                for more info.

                The request becomes a no-op if the asset name list is empty, and the max
                size of the asset name list is 100 in one request.
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
        if "delete_feed" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_feed"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_feed,
                default_retry=self._method_configs["DeleteFeed"].retry,
                default_timeout=self._method_configs["DeleteFeed"].timeout,
                client_info=self._client_info,
            )

        request = asset_service_pb2.DeleteFeedRequest(name=name)
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

        self._inner_api_calls["delete_feed"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
