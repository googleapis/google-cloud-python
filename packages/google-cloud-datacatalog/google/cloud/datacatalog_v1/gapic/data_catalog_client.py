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

"""Accesses the google.cloud.datacatalog.v1 DataCatalog API."""

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
import google.api_core.protobuf_helpers
import grpc

from google.cloud.datacatalog_v1.gapic import data_catalog_client_config
from google.cloud.datacatalog_v1.gapic import enums
from google.cloud.datacatalog_v1.gapic.transports import data_catalog_grpc_transport
from google.cloud.datacatalog_v1.proto import datacatalog_pb2
from google.cloud.datacatalog_v1.proto import datacatalog_pb2_grpc
from google.cloud.datacatalog_v1.proto import tags_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import options_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-datacatalog"
).version


class DataCatalogClient(object):
    """
    Data Catalog API service allows clients to discover, understand, and manage
    their data.
    """

    SERVICE_ADDRESS = "datacatalog.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.datacatalog.v1.DataCatalog"

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
            DataCatalogClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def entry_path(cls, project, location, entry_group, entry):
        """Return a fully-qualified entry string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/entryGroups/{entry_group}/entries/{entry}",
            project=project,
            location=location,
            entry_group=entry_group,
            entry=entry,
        )

    @classmethod
    def entry_group_path(cls, project, location, entry_group):
        """Return a fully-qualified entry_group string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/entryGroups/{entry_group}",
            project=project,
            location=location,
            entry_group=entry_group,
        )

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    @classmethod
    def tag_path(cls, project, location, entry_group, entry, tag):
        """Return a fully-qualified tag string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/entryGroups/{entry_group}/entries/{entry}/tags/{tag}",
            project=project,
            location=location,
            entry_group=entry_group,
            entry=entry,
            tag=tag,
        )

    @classmethod
    def tag_template_path(cls, project, location, tag_template):
        """Return a fully-qualified tag_template string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/tagTemplates/{tag_template}",
            project=project,
            location=location,
            tag_template=tag_template,
        )

    @classmethod
    def tag_template_field_path(cls, project, location, tag_template, field):
        """Return a fully-qualified tag_template_field string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/tagTemplates/{tag_template}/fields/{field}",
            project=project,
            location=location,
            tag_template=tag_template,
            field=field,
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
            transport (Union[~.DataCatalogGrpcTransport,
                    Callable[[~.Credentials, type], ~.DataCatalogGrpcTransport]): A transport
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
            client_config = data_catalog_client_config.config

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
                    default_class=data_catalog_grpc_transport.DataCatalogGrpcTransport,
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
            self.transport = data_catalog_grpc_transport.DataCatalogGrpcTransport(
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
    def search_catalog(
        self,
        scope,
        query,
        page_size=None,
        order_by=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Request message for ``CreateEntry``.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `scope`:
            >>> scope = {}
            >>>
            >>> # TODO: Initialize `query`:
            >>> query = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_catalog(scope, query):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.search_catalog(scope, query).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            scope (Union[dict, ~google.cloud.datacatalog_v1.types.Scope]): Creates a field in a tag template. The user should enable the Data
                Catalog API in the project identified by the ``parent`` parameter (see
                `Data Catalog Resource
                Project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__
                for more information).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.Scope`
            query (str): A ``TagTemplate``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            order_by (str): Set true to use the old proto1 MessageSet wire format for
                extensions. This is provided for backwards-compatibility with the
                MessageSet wire format. You should not use this for any other reason:
                It's less efficient, has fewer features, and is more complicated.

                The message must be defined exactly as follows: message Foo { option
                message_set_wire_format = true; extensions 4 to max; } Note that the
                message cannot have any defined fields; MessageSets only have
                extensions.

                All extensions of your type must be singular messages; e.g. they cannot
                be int32s, enums, or repeated messages.

                Because this is an option, the above two restrictions are not enforced
                by the protocol compiler.
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
            An iterable of :class:`~google.cloud.datacatalog_v1.types.SearchCatalogResult` instances.
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
        if "search_catalog" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_catalog"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_catalog,
                default_retry=self._method_configs["SearchCatalog"].retry,
                default_timeout=self._method_configs["SearchCatalog"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.SearchCatalogRequest(
            scope=scope, query=query, page_size=page_size, order_by=order_by
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["search_catalog"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="results",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_entry_group(
        self,
        parent,
        entry_group_id,
        entry_group=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Required. The name of the entry group this entry is in. Example:

        -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}

        Note that this Entry and its child resources may not actually be stored
        in the location in this name.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `entry_group_id`:
            >>> entry_group_id = ''
            >>>
            >>> response = client.create_entry_group(parent, entry_group_id)

        Args:
            parent (str): Request message for ``RenameTagTemplateField``.
            entry_group_id (str): Required. The id of the entry group to create.
                The id must begin with a letter or underscore, contain only English
                letters, numbers and underscores, and be at most 64 characters.
            entry_group (Union[dict, ~google.cloud.datacatalog_v1.types.EntryGroup]): The entry group to create. Defaults to an empty entry group.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.EntryGroup`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.EntryGroup` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_entry_group" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_entry_group"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_entry_group,
                default_retry=self._method_configs["CreateEntryGroup"].retry,
                default_timeout=self._method_configs["CreateEntryGroup"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.CreateEntryGroupRequest(
            parent=parent, entry_group_id=entry_group_id, entry_group=entry_group
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

        return self._inner_api_calls["create_entry_group"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_entry_group(
        self,
        name,
        read_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets an EntryGroup.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> name = client.entry_group_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]')
            >>>
            >>> response = client.get_entry_group(name)

        Args:
            name (str): Request message for ``DeleteEntry``.
            read_mask (Union[dict, ~google.cloud.datacatalog_v1.types.FieldMask]): The fields to return. If not set or empty, all fields are returned.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.EntryGroup` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_entry_group" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_entry_group"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_entry_group,
                default_retry=self._method_configs["GetEntryGroup"].retry,
                default_timeout=self._method_configs["GetEntryGroup"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.GetEntryGroupRequest(name=name, read_mask=read_mask)
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

        return self._inner_api_calls["get_entry_group"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_entry_group(
        self,
        entry_group,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        The full name of the cloud resource the entry belongs to. See:
        https://cloud.google.com/apis/design/resource_names#full_resource_name.
        Example:

        -  ``//bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId``

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `entry_group`:
            >>> entry_group = {}
            >>>
            >>> response = client.update_entry_group(entry_group)

        Args:
            entry_group (Union[dict, ~google.cloud.datacatalog_v1.types.EntryGroup]): Required. The updated entry group. "name" field must be set.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.EntryGroup`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1.types.FieldMask]): The fields to update on the entry group. If absent or empty, all modifiable
                fields are updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.EntryGroup` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_entry_group" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_entry_group"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_entry_group,
                default_retry=self._method_configs["UpdateEntryGroup"].retry,
                default_timeout=self._method_configs["UpdateEntryGroup"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.UpdateEntryGroupRequest(
            entry_group=entry_group, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("entry_group.name", entry_group.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_entry_group"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_entry_group(
        self,
        name,
        force=None,
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
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> name = client.entry_group_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]')
            >>>
            >>> client.delete_entry_group(name)

        Args:
            name (str): Identifies which part of the FileDescriptorProto was defined at this
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
            force (bool): Optional. If true, deletes all entries in the entry group.
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
        if "delete_entry_group" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_entry_group"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_entry_group,
                default_retry=self._method_configs["DeleteEntryGroup"].retry,
                default_timeout=self._method_configs["DeleteEntryGroup"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.DeleteEntryGroupRequest(name=name, force=force)
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

        self._inner_api_calls["delete_entry_group"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_entry_groups(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists entry groups.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> parent = client.entry_group_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_entry_groups(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_entry_groups(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The resource type that the annotated field references.

                Example:

                ::

                    message Subscription {
                      string topic = 2 [(google.api.resource_reference) = {
                        type: "pubsub.googleapis.com/Topic"
                      }];
                    }
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
            An iterable of :class:`~google.cloud.datacatalog_v1.types.EntryGroup` instances.
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
        if "list_entry_groups" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_entry_groups"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_entry_groups,
                default_retry=self._method_configs["ListEntryGroups"].retry,
                default_timeout=self._method_configs["ListEntryGroups"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.ListEntryGroupsRequest(
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
                self._inner_api_calls["list_entry_groups"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="entry_groups",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_entry(
        self,
        parent,
        entry_id,
        entry,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        The name of the uninterpreted option. Each string represents a
        segment in a dot-separated name. is_extension is true iff a segment
        represents an extension (denoted with parentheses in options specs in
        .proto files). E.g.,{ ["foo", false], ["bar.baz", true], ["qux", false]
        } represents "foo.(bar.baz).qux".

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> parent = client.entry_group_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]')
            >>>
            >>> # TODO: Initialize `entry_id`:
            >>> entry_id = ''
            >>>
            >>> # TODO: Initialize `entry`:
            >>> entry = {}
            >>>
            >>> response = client.create_entry(parent, entry_id, entry)

        Args:
            parent (str): The resource type of a child collection that the annotated field
                references. This is useful for annotating the ``parent`` field that
                doesn't have a fixed resource type.

                Example:

                ::

                    message ListLogEntriesRequest {
                      string parent = 1 [(google.api.resource_reference) = {
                        child_type: "logging.googleapis.com/LogEntry"
                      };
                    }
            entry_id (str): Required. The id of the entry to create.
            entry (Union[dict, ~google.cloud.datacatalog_v1.types.Entry]): Required. The entry to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.Entry`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.Entry` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_entry" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_entry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_entry,
                default_retry=self._method_configs["CreateEntry"].retry,
                default_timeout=self._method_configs["CreateEntry"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.CreateEntryRequest(
            parent=parent, entry_id=entry_id, entry=entry
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

        return self._inner_api_calls["create_entry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_entry(
        self,
        entry,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a tag template. This method cannot be used to update the
        fields of a template. The tag template fields are represented as
        separate resources and should be updated using their own
        create/update/delete methods. Users should enable the Data Catalog API
        in the project identified by the ``tag_template.name`` parameter (see
        [Data Catalog Resource Project]
        (/data-catalog/docs/concepts/resource-project) for more information).

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `entry`:
            >>> entry = {}
            >>>
            >>> response = client.update_entry(entry)

        Args:
            entry (Union[dict, ~google.cloud.datacatalog_v1.types.Entry]): Required. The updated entry. The "name" field must be set.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.Entry`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1.types.FieldMask]): Required. The name of the entry. Example:

                -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}/entries/{entry_id}

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.Entry` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_entry" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_entry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_entry,
                default_retry=self._method_configs["UpdateEntry"].retry,
                default_timeout=self._method_configs["UpdateEntry"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.UpdateEntryRequest(
            entry=entry, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("entry.name", entry.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_entry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_entry(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        The source system of the entry. Only applicable when
        ``search_result_type`` is ENTRY.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> name = client.entry_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]', '[ENTRY]')
            >>>
            >>> client.delete_entry(name)

        Args:
            name (str): Protocol Buffers - Google's data interchange format Copyright 2008
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
        if "delete_entry" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_entry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_entry,
                default_retry=self._method_configs["DeleteEntry"].retry,
                default_timeout=self._method_configs["DeleteEntry"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.DeleteEntryRequest(name=name)
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

        self._inner_api_calls["delete_entry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_entry(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets an entry.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> name = client.entry_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]', '[ENTRY]')
            >>>
            >>> response = client.get_entry(name)

        Args:
            name (str): Whether the message is an automatically generated map entry type for
                the maps field.

                For maps fields: map<KeyType, ValueType> map_field = 1; The parsed
                descriptor looks like: message MapFieldEntry { option map_entry = true;
                optional KeyType key = 1; optional ValueType value = 2; } repeated
                MapFieldEntry map_field = 1;

                Implementations may choose not to generate the map_entry=true message,
                but use a native map in the target language to hold the keys and values.
                The reflection APIs in such implementations still need to work as if the
                field is a repeated message field.

                NOTE: Do not set the option in .proto files. Always use the maps syntax
                instead. The option should only be implicitly set by the proto compiler
                parser.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.Entry` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_entry" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_entry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_entry,
                default_retry=self._method_configs["GetEntry"].retry,
                default_timeout=self._method_configs["GetEntry"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.GetEntryRequest(name=name)
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

        return self._inner_api_calls["get_entry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def lookup_entry(
        self,
        linked_resource=None,
        sql_resource=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Get an entry by target resource name. This method allows clients to use
        the resource name from the source Google Cloud Platform service to get the
        Data Catalog Entry.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> response = client.lookup_entry()

        Args:
            linked_resource (str): Request message for ``LookupEntry``.
            sql_resource (str): Output only. The resource name of the tag template field in URL
                format. Example:

                -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template}/fields/{field}

                Note that this TagTemplateField may not actually be stored in the
                location in this name.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.Entry` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "lookup_entry" not in self._inner_api_calls:
            self._inner_api_calls[
                "lookup_entry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.lookup_entry,
                default_retry=self._method_configs["LookupEntry"].retry,
                default_timeout=self._method_configs["LookupEntry"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            linked_resource=linked_resource, sql_resource=sql_resource
        )

        request = datacatalog_pb2.LookupEntryRequest(
            linked_resource=linked_resource, sql_resource=sql_resource
        )
        return self._inner_api_calls["lookup_entry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_entries(
        self,
        parent,
        page_size=None,
        read_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists entries.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> parent = client.entry_group_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_entries(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_entries(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Request message for ``SearchCatalog``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            read_mask (Union[dict, ~google.cloud.datacatalog_v1.types.FieldMask]): Request message for ``UpdateEntryGroup``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.FieldMask`
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
            An iterable of :class:`~google.cloud.datacatalog_v1.types.Entry` instances.
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
        if "list_entries" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_entries"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_entries,
                default_retry=self._method_configs["ListEntries"].retry,
                default_timeout=self._method_configs["ListEntries"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.ListEntriesRequest(
            parent=parent, page_size=page_size, read_mask=read_mask
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
                self._inner_api_calls["list_entries"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="entries",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_tag_template(
        self,
        parent,
        tag_template_id,
        tag_template,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        The resource has one pattern, but the API owner expects to add more
        later. (This is the inverse of ORIGINALLY_SINGLE_PATTERN, and prevents
        that from being necessary once there are multiple patterns.)

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `tag_template_id`:
            >>> tag_template_id = ''
            >>>
            >>> # TODO: Initialize `tag_template`:
            >>> tag_template = {}
            >>>
            >>> response = client.create_tag_template(parent, tag_template_id, tag_template)

        Args:
            parent (str): Request message for ``GetEntry``.
            tag_template_id (str): Required. The id of the tag template to create.
            tag_template (Union[dict, ~google.cloud.datacatalog_v1.types.TagTemplate]): Required. The tag template to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.TagTemplate`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.TagTemplate` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_tag_template" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_tag_template"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_tag_template,
                default_retry=self._method_configs["CreateTagTemplate"].retry,
                default_timeout=self._method_configs["CreateTagTemplate"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.CreateTagTemplateRequest(
            parent=parent, tag_template_id=tag_template_id, tag_template=tag_template
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

        return self._inner_api_calls["create_tag_template"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_tag_template(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a tag template.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> name = client.tag_template_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]')
            >>>
            >>> response = client.get_tag_template(name)

        Args:
            name (str): Spec of a BigQuery table. This field should only be populated if
                ``table_source_type`` is ``BIGQUERY_TABLE``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.TagTemplate` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_tag_template" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_tag_template"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_tag_template,
                default_retry=self._method_configs["GetTagTemplate"].retry,
                default_timeout=self._method_configs["GetTagTemplate"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.GetTagTemplateRequest(name=name)
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

        return self._inner_api_calls["get_tag_template"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_tag_template(
        self,
        tag_template,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Request message for ``UpdateTagTemplateField``.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `tag_template`:
            >>> tag_template = {}
            >>>
            >>> response = client.update_tag_template(tag_template)

        Args:
            tag_template (Union[dict, ~google.cloud.datacatalog_v1.types.TagTemplate]): Required. The template to update. The "name" field must be set.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.TagTemplate`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1.types.FieldMask]): Number of results in the search page. If <=0 then defaults to 10.
                Max limit for page_size is 1000. Throws an invalid argument for
                page_size > 1000.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.TagTemplate` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_tag_template" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_tag_template"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_tag_template,
                default_retry=self._method_configs["UpdateTagTemplate"].retry,
                default_timeout=self._method_configs["UpdateTagTemplate"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.UpdateTagTemplateRequest(
            tag_template=tag_template, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("tag_template.name", tag_template.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_tag_template"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_tag_template(
        self,
        name,
        force,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        The resource type. It must be in the format of
        {service_name}/{resource_type_kind}. The ``resource_type_kind`` must be
        singular and must not include version numbers.

        Example: ``storage.googleapis.com/Bucket``

        The value of the resource_type_kind must follow the regular expression
        /[A-Za-z][a-zA-Z0-9]+/. It should start with an upper case character and
        should use PascalCase (UpperCamelCase). The maximum number of characters
        allowed for the ``resource_type_kind`` is 100.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> name = client.tag_template_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]')
            >>>
            >>> # TODO: Initialize `force`:
            >>> force = False
            >>>
            >>> client.delete_tag_template(name, force)

        Args:
            name (str): If this SourceCodeInfo represents a complete declaration, these are
                any comments appearing before and after the declaration which appear to
                be attached to the declaration.

                A series of line comments appearing on consecutive lines, with no other
                tokens appearing on those lines, will be treated as a single comment.

                leading_detached_comments will keep paragraphs of comments that appear
                before (but not connected to) the current element. Each paragraph,
                separated by empty lines, will be one comment element in the repeated
                field.

                Only the comment content is provided; comment markers (e.g. //) are
                stripped out. For block comments, leading whitespace and an asterisk
                will be stripped from the beginning of each line other than the first.
                Newlines are included in the output.

                Examples:

                optional int32 foo = 1; // Comment attached to foo. // Comment attached
                to bar. optional int32 bar = 2;

                optional string baz = 3; // Comment attached to baz. // Another line
                attached to baz.

                // Comment attached to qux. // // Another line attached to qux. optional
                double qux = 4;

                // Detached comment for corge. This is not leading or trailing comments
                // to qux or corge because there are blank lines separating it from //
                both.

                // Detached comment for corge paragraph 2.

                optional string corge = 5; /\* Block comment attached \* to corge.
                Leading asterisks \* will be removed. */ /* Block comment attached to \*
                grault. \*/ optional int32 grault = 6;

                // ignored detached comments.
            force (bool): Response message for ``ListTags``.
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
        if "delete_tag_template" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_tag_template"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_tag_template,
                default_retry=self._method_configs["DeleteTagTemplate"].retry,
                default_timeout=self._method_configs["DeleteTagTemplate"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.DeleteTagTemplateRequest(name=name, force=force)
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

        self._inner_api_calls["delete_tag_template"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_tag_template_field(
        self,
        parent,
        tag_template_field_id,
        tag_template_field,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Required. The name of the tag template field. Example:

        -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}/fields/{tag_template_field_id}

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> parent = client.tag_template_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]')
            >>>
            >>> # TODO: Initialize `tag_template_field_id`:
            >>> tag_template_field_id = ''
            >>>
            >>> # TODO: Initialize `tag_template_field`:
            >>> tag_template_field = {}
            >>>
            >>> response = client.create_tag_template_field(parent, tag_template_field_id, tag_template_field)

        Args:
            parent (str): Required. The name of the entry group that contains the entries,
                which can be provided in URL format. Example:

                -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}
            tag_template_field_id (str): Output only. If the table is a dated shard, i.e., with name pattern
                ``[prefix]YYYYMMDD``, ``grouped_entry`` is the Data Catalog resource
                name of the date sharded grouped entry, for example,
                ``projects/{project_id}/locations/{location}/entrygroups/{entry_group_id}/entries/{entry_id}``.
                Otherwise, ``grouped_entry`` is empty.
            tag_template_field (Union[dict, ~google.cloud.datacatalog_v1.types.TagTemplateField]): Required. The tag template field to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.TagTemplateField`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.TagTemplateField` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_tag_template_field" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_tag_template_field"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_tag_template_field,
                default_retry=self._method_configs["CreateTagTemplateField"].retry,
                default_timeout=self._method_configs["CreateTagTemplateField"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.CreateTagTemplateFieldRequest(
            parent=parent,
            tag_template_field_id=tag_template_field_id,
            tag_template_field=tag_template_field,
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

        return self._inner_api_calls["create_tag_template_field"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_tag_template_field(
        self,
        name,
        tag_template_field,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Request message for ``SetIamPolicy`` method.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> name = client.tag_template_field_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]', '[FIELD]')
            >>>
            >>> # TODO: Initialize `tag_template_field`:
            >>> tag_template_field = {}
            >>>
            >>> response = client.update_tag_template_field(name, tag_template_field)

        Args:
            name (str): This field indicates the entry's source system that Data Catalog
                does not integrate with. ``user_specified_system`` strings must begin
                with a letter or underscore and can only contain letters, numbers, and
                underscores; are case insensitive; must be at least 1 character and at
                most 64 characters long.
            tag_template_field (Union[dict, ~google.cloud.datacatalog_v1.types.TagTemplateField]): Required. The template to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.TagTemplateField`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1.types.FieldMask]): Required. The name of the tag template. Example:

                -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.TagTemplateField` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_tag_template_field" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_tag_template_field"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_tag_template_field,
                default_retry=self._method_configs["UpdateTagTemplateField"].retry,
                default_timeout=self._method_configs["UpdateTagTemplateField"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.UpdateTagTemplateFieldRequest(
            name=name, tag_template_field=tag_template_field, update_mask=update_mask
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

        return self._inner_api_calls["update_tag_template_field"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def rename_tag_template_field(
        self,
        name,
        new_tag_template_field_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        The resource name of the tag in URL format. Example:

        -  projects/{project_id}/locations/{location}/entrygroups/{entry_group_id}/entries/{entry_id}/tags/{tag_id}

        where ``tag_id`` is a system-generated identifier. Note that this Tag
        may not actually be stored in the location in this name.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> name = client.tag_template_field_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]', '[FIELD]')
            >>>
            >>> # TODO: Initialize `new_tag_template_field_id`:
            >>> new_tag_template_field_id = ''
            >>>
            >>> response = client.rename_tag_template_field(name, new_tag_template_field_id)

        Args:
            name (str): The maximum number of items to return. Default is 10. Max limit is
                1000. Throws an invalid argument for ``page_size > 1000``.
            new_tag_template_field_id (str): Gets the access control policy for a resource. A ``NOT_FOUND`` error
                is returned if the resource does not exist. An empty policy is returned
                if the resource exists but does not have a policy set on it.

                Supported resources are:

                -  Tag templates.
                -  Entries.
                -  Entry groups. Note, this method cannot be used to manage policies for
                   BigQuery, Pub/Sub and any external Google Cloud Platform resources
                   synced to Data Catalog.

                Callers must have following Google IAM permission

                -  ``datacatalog.tagTemplates.getIamPolicy`` to get policies on tag
                   templates.
                -  ``datacatalog.entries.getIamPolicy`` to get policies on entries.
                -  ``datacatalog.entryGroups.getIamPolicy`` to get policies on entry
                   groups.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.TagTemplateField` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "rename_tag_template_field" not in self._inner_api_calls:
            self._inner_api_calls[
                "rename_tag_template_field"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.rename_tag_template_field,
                default_retry=self._method_configs["RenameTagTemplateField"].retry,
                default_timeout=self._method_configs["RenameTagTemplateField"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.RenameTagTemplateFieldRequest(
            name=name, new_tag_template_field_id=new_tag_template_field_id
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

        return self._inner_api_calls["rename_tag_template_field"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_tag_template_field(
        self,
        name,
        force,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Optional. The relative resource name pattern associated with this
        resource type. The DNS prefix of the full resource name shouldn't be
        specified here.

        The path pattern must follow the syntax, which aligns with HTTP binding
        syntax:

        ::

            Template = Segment { "/" Segment } ;
            Segment = LITERAL | Variable ;
            Variable = "{" LITERAL "}" ;

        Examples:

        ::

            - "projects/{project}/topics/{topic}"
            - "projects/{project}/knowledgeBases/{knowledge_base}"

        The components in braces correspond to the IDs for each resource in the
        hierarchy. It is expected that, if multiple patterns are provided, the
        same component name (e.g. "project") refers to IDs of the same type of
        resource.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> name = client.tag_template_field_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]', '[FIELD]')
            >>>
            >>> # TODO: Initialize `force`:
            >>> force = False
            >>>
            >>> client.delete_tag_template_field(name, force)

        Args:
            name (str): ``FieldMask`` represents a set of symbolic field paths, for example:

                ::

                    paths: "f.a"
                    paths: "f.b.d"

                Here ``f`` represents a field in some root message, ``a`` and ``b``
                fields in the message found in ``f``, and ``d`` a field found in the
                message in ``f.b``.

                Field masks are used to specify a subset of fields that should be
                returned by a get operation or modified by an update operation. Field
                masks also have a custom JSON encoding (see below).

                # Field Masks in Projections

                When used in the context of a projection, a response message or
                sub-message is filtered by the API to only contain those fields as
                specified in the mask. For example, if the mask in the previous example
                is applied to a response message as follows:

                ::

                    f {
                      a : 22
                      b {
                        d : 1
                        x : 2
                      }
                      y : 13
                    }
                    z: 8

                The result will not contain specific values for fields x,y and z (their
                value will be set to the default, and omitted in proto text output):

                ::

                    f {
                      a : 22
                      b {
                        d : 1
                      }
                    }

                A repeated field is not allowed except at the last position of a paths
                string.

                If a FieldMask object is not present in a get operation, the operation
                applies to all fields (as if a FieldMask of all fields had been
                specified).

                Note that a field mask does not necessarily apply to the top-level
                response message. In case of a REST get operation, the field mask
                applies directly to the response, but in case of a REST list operation,
                the mask instead applies to each individual message in the returned
                resource list. In case of a REST custom method, other definitions may be
                used. Where the mask applies will be clearly documented together with
                its declaration in the API. In any case, the effect on the returned
                resource/resources is required behavior for APIs.

                # Field Masks in Update Operations

                A field mask in update operations specifies which fields of the targeted
                resource are going to be updated. The API is required to only change the
                values of the fields as specified in the mask and leave the others
                untouched. If a resource is passed in to describe the updated values,
                the API ignores the values of all fields not covered by the mask.

                If a repeated field is specified for an update operation, new values
                will be appended to the existing repeated field in the target resource.
                Note that a repeated field is only allowed in the last position of a
                ``paths`` string.

                If a sub-message is specified in the last position of the field mask for
                an update operation, then new value will be merged into the existing
                sub-message in the target resource.

                For example, given the target message:

                ::

                    f {
                      b {
                        d: 1
                        x: 2
                      }
                      c: [1]
                    }

                And an update message:

                ::

                    f {
                      b {
                        d: 10
                      }
                      c: [2]
                    }

                then if the field mask is:

                paths: ["f.b", "f.c"]

                then the result will be:

                ::

                    f {
                      b {
                        d: 10
                        x: 2
                      }
                      c: [1, 2]
                    }

                An implementation may provide options to override this default behavior
                for repeated and message fields.

                In order to reset a field's value to the default, the field must be in
                the mask and set to the default value in the provided resource. Hence,
                in order to reset all fields of a resource, provide a default instance
                of the resource and set all fields in the mask, or do not provide a mask
                as described below.

                If a field mask is not present on update, the operation applies to all
                fields (as if a field mask of all fields has been specified). Note that
                in the presence of schema evolution, this may mean that fields the
                client does not know and has therefore not filled into the request will
                be reset to their default. If this is unwanted behavior, a specific
                service may require a client to always specify a field mask, producing
                an error if not.

                As with get operations, the location of the resource which describes the
                updated values in the request message depends on the operation kind. In
                any case, the effect of the field mask is required to be honored by the
                API.

                ## Considerations for HTTP REST

                The HTTP kind of an update operation which uses a field mask must be set
                to PATCH instead of PUT in order to satisfy HTTP semantics (PUT must
                only be used for full updates).

                # JSON Encoding of Field Masks

                In JSON, a field mask is encoded as a single string where paths are
                separated by a comma. Fields name in each path are converted to/from
                lower-camel naming conventions.

                As an example, consider the following message declarations:

                ::

                    message Profile {
                      User user = 1;
                      Photo photo = 2;
                    }
                    message User {
                      string display_name = 1;
                      string address = 2;
                    }

                In proto a field mask for ``Profile`` may look as such:

                ::

                    mask {
                      paths: "user.display_name"
                      paths: "photo"
                    }

                In JSON, the same mask is represented as below:

                ::

                    {
                      mask: "user.displayName,photo"
                    }

                # Field Masks and Oneof Fields

                Field masks treat fields in oneofs just as regular fields. Consider the
                following message:

                ::

                    message SampleMessage {
                      oneof test_oneof {
                        string name = 4;
                        SubMessage sub_message = 9;
                      }
                    }

                The field mask can be:

                ::

                    mask {
                      paths: "name"
                    }

                Or:

                ::

                    mask {
                      paths: "sub_message"
                    }

                Note that oneof type names ("test_oneof" in this case) cannot be used in
                paths.

                ## Field Mask Verification

                The implementation of any API method which has a FieldMask type field in
                the request should verify the included field paths, and return an
                ``INVALID_ARGUMENT`` error if any path is unmappable.
            force (bool): Creates an entry. Only entries of 'FILESET' type or user-specified
                type can be created.

                Users should enable the Data Catalog API in the project identified by
                the ``parent`` parameter (see [Data Catalog Resource Project]
                (/data-catalog/docs/concepts/resource-project) for more information).

                A maximum of 100,000 entries may be created per entry group.
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
        if "delete_tag_template_field" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_tag_template_field"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_tag_template_field,
                default_retry=self._method_configs["DeleteTagTemplateField"].retry,
                default_timeout=self._method_configs["DeleteTagTemplateField"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.DeleteTagTemplateFieldRequest(name=name, force=force)
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

        self._inner_api_calls["delete_tag_template_field"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_tag(
        self,
        parent,
        tag,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a tag template and all tags using the template. Users should
        enable the Data Catalog API in the project identified by the ``name``
        parameter (see [Data Catalog Resource Project]
        (/data-catalog/docs/concepts/resource-project) for more information).

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> parent = client.tag_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]', '[ENTRY]', '[TAG]')
            >>>
            >>> # TODO: Initialize `tag`:
            >>> tag = {}
            >>>
            >>> response = client.create_tag(parent, tag)

        Args:
            parent (str): A generic empty message that you can re-use to avoid defining
                duplicated empty messages in your APIs. A typical example is to use it
                as the request or the response type of an API method. For instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON object ``{}``.
            tag (Union[dict, ~google.cloud.datacatalog_v1.types.Tag]): Required. The tag to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.Tag`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.Tag` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_tag" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_tag"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_tag,
                default_retry=self._method_configs["CreateTag"].retry,
                default_timeout=self._method_configs["CreateTag"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.CreateTagRequest(parent=parent, tag=tag)
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

        return self._inner_api_calls["create_tag"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_tag(
        self,
        tag,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an existing tag.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `tag`:
            >>> tag = {}
            >>>
            >>> response = client.update_tag(tag)

        Args:
            tag (Union[dict, ~google.cloud.datacatalog_v1.types.Tag]): Required. The updated tag. The "name" field must be set.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.Tag`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1.types.FieldMask]): Lists the tags on an ``Entry``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.Tag` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_tag" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_tag"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_tag,
                default_retry=self._method_configs["UpdateTag"].retry,
                default_timeout=self._method_configs["UpdateTag"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.UpdateTagRequest(tag=tag, update_mask=update_mask)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("tag.name", tag.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_tag"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_tag(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a tag.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> name = client.entry_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]', '[ENTRY]')
            >>>
            >>> client.delete_tag(name)

        Args:
            name (str): The full name of the Google Cloud Platform resource the Data Catalog
                entry represents. See:
                https://cloud.google.com/apis/design/resource_names#full_resource_name.
                Full names are case-sensitive.

                Examples:

                -  //bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId
                -  //pubsub.googleapis.com/projects/projectId/topics/topicId
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
        if "delete_tag" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_tag"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_tag,
                default_retry=self._method_configs["DeleteTag"].retry,
                default_timeout=self._method_configs["DeleteTag"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.DeleteTagRequest(name=name)
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

        self._inner_api_calls["delete_tag"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_tags(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        The SQL name of the entry. SQL names are case-sensitive.

        Examples:

        -  ``cloud_pubsub.project_id.topic_id``
        -  :literal:`pubsub.project_id.`topic.id.with.dots\``
        -  ``bigquery.table.project_id.dataset_id.table_id``
        -  ``bigquery.dataset.project_id.dataset_id``
        -  ``datacatalog.entry.project_id.location_id.entry_group_id.entry_id``

        ``*_id``\ s shoud satisfy the standard SQL rules for identifiers.
        https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> parent = client.entry_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]', '[ENTRY]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_tags(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_tags(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Specification that applies to a BigQuery table. This is only valid
                on entries of type ``TABLE``.
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
            An iterable of :class:`~google.cloud.datacatalog_v1.types.Tag` instances.
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
        if "list_tags" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_tags"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_tags,
                default_retry=self._method_configs["ListTags"].retry,
                default_timeout=self._method_configs["ListTags"].timeout,
                client_info=self._client_info,
            )

        request = datacatalog_pb2.ListTagsRequest(parent=parent, page_size=page_size)
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
                self._inner_api_calls["list_tags"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="tags",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def set_iam_policy(
        self,
        resource,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        ``Tag`` details.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                See the operation documentation for the appropriate value for this field.
            policy (Union[dict, ~google.cloud.datacatalog_v1.types.Policy]): Deletes an EntryGroup. Only entry groups that do not contain entries
                can be deleted. Users should enable the Data Catalog API in the project
                identified by the ``name`` parameter (see [Data Catalog Resource
                Project] (/data-catalog/docs/concepts/resource-project) for more
                information).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.Policy` instance.

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

    def get_iam_policy(
        self,
        resource,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Request message for ``UpdateEntry``.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                See the operation documentation for the appropriate value for this field.
            options_ (Union[dict, ~google.cloud.datacatalog_v1.types.GetPolicyOptions]): For extensions, this is the name of the type being extended. It is
                resolved in the same manner as type_name.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1.types.GetPolicyOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.Policy` instance.

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

    def test_iam_permissions(
        self,
        resource,
        permissions,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        REQUIRED: The complete policy to be applied to the ``resource``. The
        size of the policy is limited to a few 10s of KB. An empty policy is a
        valid policy but certain Cloud Platform services (such as Projects)
        might reject them.

        Example:
            >>> from google.cloud import datacatalog_v1
            >>>
            >>> client = datacatalog_v1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                See the operation documentation for the appropriate value for this field.
            permissions (list[str]): An annotation that describes a resource definition, see
                ``ResourceDescriptor``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1.types.TestIamPermissionsResponse` instance.

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
