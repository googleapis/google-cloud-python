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

"""Accesses the google.cloud.datacatalog.v1beta1 DataCatalog API."""

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

from google.cloud.datacatalog_v1beta1.gapic import data_catalog_client_config
from google.cloud.datacatalog_v1beta1.gapic import enums
from google.cloud.datacatalog_v1beta1.gapic.transports import (
    data_catalog_grpc_transport,
)
from google.cloud.datacatalog_v1beta1.proto import datacatalog_pb2
from google.cloud.datacatalog_v1beta1.proto import datacatalog_pb2_grpc
from google.cloud.datacatalog_v1beta1.proto import tags_pb2
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
    _INTERFACE_NAME = "google.cloud.datacatalog.v1beta1.DataCatalog"

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
    def field_path(cls, project, location, tag_template, field):
        """Return a fully-qualified field string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/tagTemplates/{tag_template}/fields/{field}",
            project=project,
            location=location,
            tag_template=tag_template,
            field=field,
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
        Output only. Resource name of this policy tag, whose format is:
        "projects/{project_number}/locations/{location_id}/taxonomies/{taxonomy_id}/policyTags/{id}".

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
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
            scope (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Scope]): Required. The scope of this search request.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Scope`
            query (str): The Data Catalog resource name of the entry in URL format. Example:

                -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}/entries/{entry_id}

                Note that this Entry and its child resources may not actually be stored
                in the location in this name.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            order_by (str): ``etag`` is used for optimistic concurrency control as a way to help
                prevent simultaneous updates of a policy from overwriting each other. It
                is strongly suggested that systems make use of the ``etag`` in the
                read-modify-write cycle to perform policy updates in order to avoid race
                conditions: An ``etag`` is returned in the response to ``getIamPolicy``,
                and systems are expected to put that etag in the request to
                ``setIamPolicy`` to ensure that their change will be applied to the same
                version of the policy.

                If no ``etag`` is provided in the call to ``setIamPolicy``, then the
                existing policy is overwritten. Due to blind-set semantics of an
                etag-less policy, 'setIamPolicy' will not fail even if the incoming
                policy version does not meet the requirements for modifying the stored
                policy.
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
            An iterable of :class:`~google.cloud.datacatalog_v1beta1.types.SearchCatalogResult` instances.
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
        entry_group,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Request message for ``LookupEntry``.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `entry_group_id`:
            >>> entry_group_id = ''
            >>>
            >>> # TODO: Initialize `entry_group`:
            >>> entry_group = {}
            >>>
            >>> response = client.create_entry_group(parent, entry_group_id, entry_group)

        Args:
            parent (str): The resource this metadata entry refers to.

                For Google Cloud Platform resources, ``linked_resource`` is the `full
                name of the
                resource <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__.
                For example, the ``linked_resource`` for a table resource from BigQuery
                is:

                -  //bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId

                Output only when Entry is of type in the EntryType enum. For entries
                with user_specified_type, this field is optional and defaults to an
                empty string.
            entry_group_id (str): Required. The id of the entry group to create.
                The id must begin with a letter or underscore, contain only English
                letters, numbers and underscores, and be at most 64 characters.
            entry_group (Union[dict, ~google.cloud.datacatalog_v1beta1.types.EntryGroup]): The entry group to create. Defaults to an empty entry group.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.EntryGroup`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.EntryGroup` instance.

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
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> name = client.entry_group_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]')
            >>>
            >>> response = client.get_entry_group(name)

        Args:
            name (str): Optional. The relative resource name pattern associated with this
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
            read_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): The fields to return. If not set or empty, all fields are returned.

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
            A :class:`~google.cloud.datacatalog_v1beta1.types.EntryGroup` instance.

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

    def delete_entry_group(
        self,
        name,
        force=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Request message for ``GetEntry``.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> name = client.entry_group_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]')
            >>>
            >>> client.delete_entry_group(name)

        Args:
            name (str): The full name of the cloud resource the entry belongs to. See:
                https://cloud.google.com/apis/design/resource_names#full_resource_name.
                Example:

                -  ``//bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId``
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
        For extensions, this is the name of the type being extended. It is
        resolved in the same manner as type_name.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
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
            parent (str): Spec of a BigQuery table. This field should only be populated if
                ``table_source_type`` is ``BIGQUERY_TABLE``.
            entry_id (str): Required. The id of the entry to create.
            entry (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Entry]): Required. The entry to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Entry`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.Entry` instance.

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
        A ``TagTemplate``.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `entry`:
            >>> entry = {}
            >>>
            >>> response = client.update_entry(entry)

        Args:
            entry (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Entry]): Required. The updated entry. The "name" field must be set.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Entry`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): The plural name used in the resource name, such as 'projects' for
                the name of 'projects/{project}'. It is the same concept of the
                ``plural`` field in k8s CRD spec
                https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/

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
            A :class:`~google.cloud.datacatalog_v1beta1.types.Entry` instance.

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
        The full name of the Google Cloud Platform resource the Data Catalog
        entry represents. See:
        https://cloud.google.com/apis/design/resource_names#full_resource_name.
        Full names are case-sensitive.

        Examples:

        -  //bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId
        -  //pubsub.googleapis.com/projects/projectId/topics/topicId

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> name = client.entry_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]', '[ENTRY]')
            >>>
            >>> client.delete_entry(name)

        Args:
            name (str): Set true to use the old proto1 MessageSet wire format for
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
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> name = client.entry_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]', '[ENTRY]')
            >>>
            >>> response = client.get_entry(name)

        Args:
            name (str): The same concept of the ``singular`` field in k8s CRD spec
                https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/
                Such as "project" for the ``resourcemanager.googleapis.com/Project``
                type.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.Entry` instance.

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
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> response = client.lookup_entry()

        Args:
            linked_resource (str): Gets the access control policy for a resource. A ``NOT_FOUND`` error
                is returned if the resource does not exist. An empty policy is returned
                if the resource exists but does not have a policy set on it.

                Supported resources are:

                -  Tag templates.
                -  Entries.
                -  Entry groups. Note, this method cannot be used to manage policies for
                   BigQuery, Cloud Pub/Sub and any external Google Cloud Platform
                   resources synced to Cloud Data Catalog.

                Callers must have following Google IAM permission

                -  ``datacatalog.tagTemplates.getIamPolicy`` to get policies on tag
                   templates.
                -  ``datacatalog.entries.getIamPolicy`` to get policies on entries.
                -  ``datacatalog.entryGroups.getIamPolicy`` to get policies on entry
                   groups.
            sql_resource (str): Request message for ``UpdateTaxonomy``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.Entry` instance.

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

    def list_entry_groups(
        self,
        parent,
        page_size=None,
        page_token=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists entry groups.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> response = client.list_entry_groups(parent)

        Args:
            parent (str): Entry type if it does not fit any of the input-allowed values listed
                in ``EntryType`` enum above. When creating an entry, users should check
                the enum values first, if nothing matches the entry to be created, then
                provide a custom value, for example "my_special_type".
                ``user_specified_type`` strings must begin with a letter or underscore
                and can only contain letters, numbers, and underscores; are case
                insensitive; must be at least 1 character and at most 64 characters
                long.

                Currently, only FILESET enum value is allowed. All other entries created
                through Data Catalog must use ``user_specified_type``.
            page_size (int): Lists the tags on an ``Entry``.
            page_token (str): Optional. Token that specifies which page is requested. If empty, the first
                page is returned.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.ListEntryGroupsResponse` instance.

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

        return self._inner_api_calls["list_entry_groups"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_entries(
        self,
        parent,
        page_size=None,
        page_token=None,
        read_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists entries.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> parent = client.entry_group_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]')
            >>>
            >>> response = client.list_entries(parent)

        Args:
            parent (str): Creates an EntryGroup.

                An entry group contains logically related entries together with Cloud
                Identity and Access Management policies that specify the users who can
                create, edit, and view entries within the entry group.

                Data Catalog automatically creates an entry group for BigQuery entries
                ("@bigquery") and Pub/Sub topics ("@pubsub"). Users create their own
                entry group to contain Cloud Storage fileset entries or custom type
                entries, and the IAM policies associated with those entries. Entry
                groups, like entries, can be searched.

                A maximum of 10,000 entry groups may be created per organization across
                all locations.

                Users should enable the Data Catalog API in the project identified by
                the ``parent`` parameter (see [Data Catalog Resource Project]
                (/data-catalog/docs/concepts/resource-project) for more information).
            page_size (int): Required. The name of the project and the template location
                `region <https://cloud.google.com/compute/docs/regions-zones/#available>`__.
                NOTE: Currently, only the ``us-central1 region`` is supported.

                Example:

                -  projects/{project_id}/locations/us-central1
            page_token (str): Token that specifies which page is requested. If empty, the first page is
                returned.
            read_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): Tags are used to attach custom metadata to Data Catalog resources.
                Tags conform to the specifications within their tag template.

                See `Data Catalog
                IAM <https://cloud.google.com/data-catalog/docs/concepts/iam>`__ for
                information on the permissions needed to create or view tags.

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
            A :class:`~google.cloud.datacatalog_v1beta1.types.ListEntriesResponse` instance.

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
            parent=parent,
            page_size=page_size,
            page_token=page_token,
            read_mask=read_mask,
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

        return self._inner_api_calls["list_entries"](
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
        An ``Entry``.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `entry_group`:
            >>> entry_group = {}
            >>>
            >>> response = client.update_entry_group(entry_group)

        Args:
            entry_group (Union[dict, ~google.cloud.datacatalog_v1beta1.types.EntryGroup]): Required. The updated entry group. "name" field must be set.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.EntryGroup`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): The fields to update on the entry group. If absent or empty, all modifiable
                fields are updated.

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
            A :class:`~google.cloud.datacatalog_v1beta1.types.EntryGroup` instance.

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
        The set of permissions to check for the ``resource``. Permissions
        with wildcards (such as '*' or 'storage.*') are not allowed. For more
        information see `IAM
        Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
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
            parent (str): Request message for ``SearchCatalog``.
            tag_template_id (str): Required. The id of the tag template to create.
            tag_template (Union[dict, ~google.cloud.datacatalog_v1beta1.types.TagTemplate]): Required. The tag template to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplate`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplate` instance.

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
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> name = client.tag_template_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]')
            >>>
            >>> response = client.get_tag_template(name)

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
            A :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplate` instance.

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
        An annotation that describes a resource definition, see
        ``ResourceDescriptor``.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `tag_template`:
            >>> tag_template = {}
            >>>
            >>> response = client.update_tag_template(tag_template)

        Args:
            tag_template (Union[dict, ~google.cloud.datacatalog_v1beta1.types.TagTemplate]): Required. The template to update. The "name" field must be set.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplate`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): Specifies the identities requesting access for a Cloud Platform
                resource. ``members`` can have the following values:

                -  ``allUsers``: A special identifier that represents anyone who is on
                   the internet; with or without a Google account.

                -  ``allAuthenticatedUsers``: A special identifier that represents
                   anyone who is authenticated with a Google account or a service
                   account.

                -  ``user:{emailid}``: An email address that represents a specific
                   Google account. For example, ``alice@example.com`` .

                -  ``serviceAccount:{emailid}``: An email address that represents a
                   service account. For example,
                   ``my-other-app@appspot.gserviceaccount.com``.

                -  ``group:{emailid}``: An email address that represents a Google group.
                   For example, ``admins@example.com``.

                -  ``domain:{domain}``: The G Suite domain (primary) that represents all
                   the users of that domain. For example, ``google.com`` or
                   ``example.com``.

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
            A :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplate` instance.

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
        The relative resource name of the resource in URL format. Examples:

        -  ``projects/{project_id}/locations/{location_id}/entryGroups/{entry_group_id}/entries/{entry_id}``
        -  ``projects/{project_id}/tagTemplates/{tag_template_id}``

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> name = client.tag_template_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]')
            >>>
            >>> # TODO: Initialize `force`:
            >>> force = False
            >>>
            >>> client.delete_tag_template(name, force)

        Args:
            name (str): A Location identifies a piece of source code in a .proto file which
                corresponds to a particular definition. This information is intended to
                be useful to IDEs, code indexers, documentation generators, and similar
                tools.

                For example, say we have a file like: message Foo { optional string foo
                = 1; } Let's look at just the field definition: optional string foo = 1;
                ^ ^^ ^^ ^ ^^^ a bc de f ghi We have the following locations: span path
                represents [a,i) [ 4, 0, 2, 0 ] The whole field definition. [a,b) [ 4,
                0, 2, 0, 4 ] The label (optional). [c,d) [ 4, 0, 2, 0, 5 ] The type
                (string). [e,f) [ 4, 0, 2, 0, 1 ] The name (foo). [g,h) [ 4, 0, 2, 0, 3
                ] The number (1).

                Notes:

                -  A location may refer to a repeated field itself (i.e. not to any
                   particular index within it). This is used whenever a set of elements
                   are logically enclosed in a single code segment. For example, an
                   entire extend block (possibly containing multiple extension
                   definitions) will have an outer location whose path refers to the
                   "extensions" repeated field without an index.
                -  Multiple locations may have the same path. This happens when a single
                   logical declaration is spread out across multiple places. The most
                   obvious example is the "extend" block again -- there may be multiple
                   extend blocks in the same scope, each of which will have the same
                   path.
                -  A location's span is not always a subset of its parent's span. For
                   example, the "extendee" of an extension declaration appears at the
                   beginning of the "extend" block and is shared by all extensions
                   within the block.
                -  Just because a location's span is a subset of some other location's
                   span does not mean that it is a descendant. For example, a "group"
                   defines both a type and a field in a single declaration. Thus, the
                   locations corresponding to the type and field and their components
                   will overlap.
                -  Code which tries to interpret locations should probably be designed
                   to ignore those that it doesn't understand, as more types of
                   locations could be recorded in the future.
            force (bool): Spec for a group of BigQuery tables with name pattern
                ``[prefix]YYYYMMDD``. Context:
                https://cloud.google.com/bigquery/docs/partitioned-tables#partitioning_versus_sharding
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
        An ``EntryGroup``.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
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
            parent (str): Required. Currently, this field must always be set to ``true``. This
                confirms the deletion of any possible tags using this template.
                ``force = false`` will be supported in the future.
            tag_template_field_id (str): Output only. The table name prefix of the shards. The name of any
                given shard is ``[table_prefix]YYYYMMDD``, for example, for shard
                ``MyTable20180101``, the ``table_prefix`` is ``MyTable``.
            tag_template_field (Union[dict, ~google.cloud.datacatalog_v1beta1.types.TagTemplateField]): Required. The tag template field to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplateField`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplateField` instance.

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
        Creates a tag on an ``Entry``. Note: The project identified by the
        ``parent`` parameter for the
        `tag <https://cloud.google.com/data-catalog/docs/reference/rest/v1beta1/projects.locations.entryGroups.entries.tags/create#path-parameters>`__
        and the `tag
        template <https://cloud.google.com/data-catalog/docs/reference/rest/v1beta1/projects.locations.tagTemplates/create#path-parameters>`__
        used to create the tag must be from the same organization.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> name = client.field_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]', '[FIELD]')
            >>>
            >>> # TODO: Initialize `tag_template_field`:
            >>> tag_template_field = {}
            >>>
            >>> response = client.update_tag_template_field(name, tag_template_field)

        Args:
            name (str): Required. The name of the tag template. Example:

                -  projects/{project_id}/locations/{location}/tagTemplates/{tag_template_id}/fields/{tag_template_field_id}
            tag_template_field (Union[dict, ~google.cloud.datacatalog_v1beta1.types.TagTemplateField]): Required. The template to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplateField`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): Required. The query string in search query syntax. The query must be
                non-empty.

                Query strings can be simple as "x" or more qualified as:

                -  name:x
                -  column:x
                -  description:y

                Note: Query tokens need to have a minimum of 3 characters for substring
                matching to work correctly. See `Data Catalog Search
                Syntax <https://cloud.google.com/data-catalog/docs/how-to/search-reference>`__
                for more information.

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
            A :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplateField` instance.

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
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> name = client.field_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]', '[FIELD]')
            >>>
            >>> # TODO: Initialize `new_tag_template_field_id`:
            >>> new_tag_template_field_id = ''
            >>>
            >>> response = client.rename_tag_template_field(name, new_tag_template_field_id)

        Args:
            name (str): Required. The name of the entry group that contains the entries,
                which can be provided in URL format. Example:

                -  projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}
            new_tag_template_field_id (str): Output only. Resource name of this taxonomy, whose format is:
                "projects/{project_number}/locations/{location_id}/taxonomies/{id}".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplateField` instance.

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
        A simple descriptor of a resource type.

        ResourceDescriptor annotates a resource message (either by means of a
        protobuf annotation or use in the service config), and associates the
        resource's schema, the resource type, and the pattern of the resource
        name.

        Example:

        ::

            message Topic {
              // Indicates this message defines a resource schema.
              // Declares the resource type in the format of {service}/{kind}.
              // For Kubernetes resources, the format is {api group}/{kind}.
              option (google.api.resource) = {
                type: "pubsub.googleapis.com/Topic"
                name_descriptor: {
                  pattern: "projects/{project}/topics/{topic}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                  parent_name_extractor: "projects/{project}"
                }
              };
            }

        The ResourceDescriptor Yaml config will look like:

        ::

            resources:
            - type: "pubsub.googleapis.com/Topic"
              name_descriptor:
                - pattern: "projects/{project}/topics/{topic}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                  parent_name_extractor: "projects/{project}"

        Sometimes, resources have multiple patterns, typically because they can
        live under multiple parents.

        Example:

        ::

            message LogEntry {
              option (google.api.resource) = {
                type: "logging.googleapis.com/LogEntry"
                name_descriptor: {
                  pattern: "projects/{project}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                  parent_name_extractor: "projects/{project}"
                }
                name_descriptor: {
                  pattern: "folders/{folder}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Folder"
                  parent_name_extractor: "folders/{folder}"
                }
                name_descriptor: {
                  pattern: "organizations/{organization}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Organization"
                  parent_name_extractor: "organizations/{organization}"
                }
                name_descriptor: {
                  pattern: "billingAccounts/{billing_account}/logs/{log}"
                  parent_type: "billing.googleapis.com/BillingAccount"
                  parent_name_extractor: "billingAccounts/{billing_account}"
                }
              };
            }

        The ResourceDescriptor Yaml config will look like:

        ::

            resources:
            - type: 'logging.googleapis.com/LogEntry'
              name_descriptor:
                - pattern: "projects/{project}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                  parent_name_extractor: "projects/{project}"
                - pattern: "folders/{folder}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Folder"
                  parent_name_extractor: "folders/{folder}"
                - pattern: "organizations/{organization}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Organization"
                  parent_name_extractor: "organizations/{organization}"
                - pattern: "billingAccounts/{billing_account}/logs/{log}"
                  parent_type: "billing.googleapis.com/BillingAccount"
                  parent_name_extractor: "billingAccounts/{billing_account}"

        For flexible resources, the resource name doesn't contain parent names,
        but the resource itself has parents for policy evaluation.

        Example:

        ::

            message Shelf {
              option (google.api.resource) = {
                type: "library.googleapis.com/Shelf"
                name_descriptor: {
                  pattern: "shelves/{shelf}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                }
                name_descriptor: {
                  pattern: "shelves/{shelf}"
                  parent_type: "cloudresourcemanager.googleapis.com/Folder"
                }
              };
            }

        The ResourceDescriptor Yaml config will look like:

        ::

            resources:
            - type: 'library.googleapis.com/Shelf'
              name_descriptor:
                - pattern: "shelves/{shelf}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                - pattern: "shelves/{shelf}"
                  parent_type: "cloudresourcemanager.googleapis.com/Folder"

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> name = client.field_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]', '[FIELD]')
            >>>
            >>> # TODO: Initialize `force`:
            >>> force = False
            >>>
            >>> client.delete_tag_template_field(name, force)

        Args:
            name (str): A taxonomy is a collection of policy tags that classify data along a
                common axis. For instance a data *sensitivity* taxonomy could contain
                policy tags denoting PII such as age, zipcode, and SSN. A data *origin*
                taxonomy could contain policy tags to distinguish user data, employee
                data, partner data, public data.
            force (bool): Number of results in the search page. If <=0 then defaults to 10.
                Max limit for page_size is 1000. Throws an invalid argument for
                page_size > 1000.
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
        Response message for ``ListTags``.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> parent = client.entry_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]', '[ENTRY]')
            >>>
            >>> # TODO: Initialize `tag`:
            >>> tag = {}
            >>>
            >>> response = client.create_tag(parent, tag)

        Args:
            parent (str): The next_page_token value returned from a previous list request, if
                any. If not set, defaults to an empty string.
            tag (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Tag]): Required. The tag to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Tag`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datacatalog_v1beta1.types.Tag` instance.

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
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> # TODO: Initialize `tag`:
            >>> tag = {}
            >>>
            >>> response = client.update_tag(tag)

        Args:
            tag (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Tag]): Required. The updated tag. The "name" field must be set.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Tag`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): If ``true``, include Google Cloud Platform (GCP) public datasets in
                the search results. Info on GCP public datasets is available at
                https://cloud.google.com/public-datasets/. By default, GCP public
                datasets are excluded.

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
            A :class:`~google.cloud.datacatalog_v1beta1.types.Tag` instance.

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
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> name = client.tag_path('[PROJECT]', '[LOCATION]', '[ENTRY_GROUP]', '[ENTRY]', '[TAG]')
            >>>
            >>> client.delete_tag(name)

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
        Request message for ``ExportTaxonomies``.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
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
            parent (str): Searches Data Catalog for multiple resources like entries, tags that
                match a query.

                This is a custom method
                (https://cloud.google.com/apis/design/custom_methods) and does not
                return the complete resource, only the resource identifier and high
                level fields. Clients can subsequentally call ``Get`` methods.

                Note that Data Catalog search queries do not guarantee full recall.
                Query results that match your query may not be returned, even in
                subsequent result pages. Also note that results returned (and not
                returned) can vary across repeated search queries.

                See `Data Catalog Search
                Syntax <https://cloud.google.com/data-catalog/docs/how-to/search-reference>`__
                for more information.
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
            An iterable of :class:`~google.cloud.datacatalog_v1beta1.types.Tag` instances.
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
        Response message for ``TestIamPermissions`` method.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> resource = client.tag_template_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]')
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                See the operation documentation for the appropriate value for this field.
            policy (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Policy]): Required. The name of the entry group. For example,
                ``projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}``.

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

    def get_iam_policy(
        self,
        resource,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Entry Metadata. A Data Catalog Entry resource represents another
        resource in Google Cloud Platform (such as a BigQuery dataset or a Cloud
        Pub/Sub topic), or outside of Google Cloud Platform. Clients can use the
        ``linked_resource`` field in the Entry resource to refer to the original
        resource ID of the source system.

        An Entry resource contains resource details, such as its schema. An
        Entry can also be used to attach flexible metadata, such as a ``Tag``.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> resource = client.tag_template_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]')
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                See the operation documentation for the appropriate value for this field.
            options_ (Union[dict, ~google.cloud.datacatalog_v1beta1.types.GetPolicyOptions]): Renames a field in a tag template. The user should enable the Data
                Catalog API in the project identified by the ``name`` parameter (see
                `Data Catalog Resource
                Project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__
                for more information).

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

    def test_iam_permissions(
        self,
        resource,
        permissions,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        If set, gives the index of a oneof in the containing type's
        oneof_decl list. This field is a member of that oneof.

        Example:
            >>> from google.cloud import datacatalog_v1beta1
            >>>
            >>> client = datacatalog_v1beta1.DataCatalogClient()
            >>>
            >>> resource = client.tag_template_path('[PROJECT]', '[LOCATION]', '[TAG_TEMPLATE]')
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                See the operation documentation for the appropriate value for this field.
            permissions (list[str]): An annotation that describes a resource reference, see
                ``ResourceReference``.
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
