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
        Searches Data Catalog for multiple resources like entries, tags that
        match a query.

        This is a custom method
        (https://cloud.google.com/apis/design/custom\_methods) and does not
        return the complete resource, only the resource identifier and high
        level fields. Clients can subsequentally call Get methods.

        Note that searches do not have full recall. There may be results that
        match your query but are not returned, even in subsequent pages of
        results. These missing results may vary across repeated calls to search.
        Do not rely on this method if you need to guarantee full recall.

        See `Data Catalog Search
        Syntax <https://cloud.google.com/data-catalog/docs/how-to/search-reference>`__
        for more information.

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
            query (str): Required. The query string in search query syntax. The query must be
                non-empty.

                Query strings can be simple as "x" or more qualified as:

                -  name:x
                -  column:x
                -  description:y

                Note: Query tokens need to have a minimum of 3 characters for substring
                matching to work correctly. See `Data Catalog Search
                Syntax <https://cloud.google.com/data-catalog/docs/how-to/search-reference>`__
                for more information.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            order_by (str): Specifies the ordering of results, currently supported case-sensitive
                choices are:

                .. raw:: html

                    <ul>
                      <li> relevance </li>
                      <li> last_access_timestamp [asc|desc], defaults to descending if not
                      specified, </li>
                      <li> last_modified_timestamp [asc|desc], defaults to descending if not
                      specified. </li>
                    </ul>
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

    def update_entry(
        self,
        entry,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an existing entry.

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
            entry (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Entry]): Required. The updated Entry.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Entry`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): Optional. The fields to update on the entry. If absent or empty, all
                modifiable fields are updated.

                Modifiable fields in synced entries:

                1. schema (Pub/Sub topics only)

                Modifiable fields in native entries:

                1. display\_name
                2. description
                3. schema

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
            name (str): Required. The name of the entry. For example,
                "projects/{project\_id}/locations/{location}/entryGroups/{entry\_group\_id}/entries/{entry\_id}".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
            linked_resource (str): The full name of the Google Cloud Platform resource the Data Catalog
                entry represents. See:
                https://cloud.google.com/apis/design/resource\_names#full\_resource\_name
                Full names are case-sensitive.

                Examples:
                "//bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId".
                "//pubsub.googleapis.com/projects/projectId/topics/topicId"
            sql_resource (str): The SQL name of the entry. SQL names are case-sensitive.

                Examples:

                .. raw:: html

                    <ul>
                      <li>cloud_pubsub.project_id.topic_id</li>
                      <li>pubsub.project_id.`topic.id.with.dots`</li>
                      <li>bigquery.project_id.dataset_id.table_id</li>
                      <li>datacatalog.project_id.location_id.entry_group_id.entry_id</li>
                    </ul>
                    *_ids shoud satisfy the standard SQL rules for identifiers.
                    https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        Creates a tag template.

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
            parent (str): Required. The name of the project and the location this template is in.
                Example: "projects/{project\_id}/locations/{location}". Note that this
                TagTemplate and its child resources may not actually be stored in the
                location in this name.
            tag_template_id (str): Required. The id of the tag template to create.
            tag_template (Union[dict, ~google.cloud.datacatalog_v1beta1.types.TagTemplate]): Required. The tag template to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplate`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
            name (str): Required. The name of the tag template. For example,
                "projects/{project\_id}/locations/{location}/tagTemplates/{tag\_template\_id}".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        Updates a tag template. This method cannot be used to update the fields of
        a template. The tag template fields are represented as separate resources
        and should be updated using their own create/update/delete methods.

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
            tag_template (Union[dict, ~google.cloud.datacatalog_v1beta1.types.TagTemplate]): Required. The template to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplate`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): Optional. The field mask specifies the parts of the template to
                overwrite.

                Allowed fields:

                -  display\_name

                If update\_mask is omitted, all of the allowed fields above will be
                updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        Deletes a tag template and all tags using the template.

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
            name (str): Required. The name of the tag template to delete. For example,
                "projects/{project\_id}/locations/{location}/tagTemplates/{tag\_template\_id}".
            force (bool): Required. Currently, this field must always be set to <code>true</code>.
                This confirms the deletion of any possible tags using this template.
                <code>force = false</code> will be supported in the future.
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
        Creates a field in a tag template.

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
            parent (str): Required. The name of the project this template is in. Example:
                "projects/{project\_id}/locations/{location}/tagTemplates/{tag\_template\_id}".
                Note that this TagTemplateField may not actually be stored in the
                location in this name.
            tag_template_field_id (str): Required. The id of the tag template field to create. Field ids can
                contain letters (both uppercase and lowercase), numbers (0-9),
                underscores (\_) and dashes (-). Field ids must be at least 1 character
                long and at most 128 characters long. Field ids must also be unique to
                their template.
            tag_template_field (Union[dict, ~google.cloud.datacatalog_v1beta1.types.TagTemplateField]): Required. The tag template field to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplateField`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        Updates a field in a tag template. This method cannot be used to update the
        field type.

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
            name (str): Required. The name of the tag template field. For example,
                "projects/{project\_id}/locations/{location}/tagTemplates/{tag\_template\_id}/fields/{tag\_template\_field\_id}".
            tag_template_field (Union[dict, ~google.cloud.datacatalog_v1beta1.types.TagTemplateField]): Required. The template to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.TagTemplateField`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): Optional. The field mask specifies the parts of the template to
                overwrite. Allowed fields:

                -  display\_name
                -  type.enum\_type

                If update\_mask is omitted, all of the allowed fields above will be
                updated.

                When updating an enum type, the provided values will be merged with the
                existing values. Therefore, enum values can only be added, existing enum
                values cannot be deleted nor renamed.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        Renames a field in a tag template.

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
            name (str): Required. The name of the tag template. For example,
                "projects/{project\_id}/locations/{location}/tagTemplates/{tag\_template\_id}/fields/{tag\_template\_field\_id}".
            new_tag_template_field_id (str): Required. The new ID of this tag template field. For example,
                "my\_new\_field".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        Deletes a field in a tag template and all uses of that field.

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
            name (str): Required. The name of the tag template field to delete. For example,
                "projects/{project\_id}/locations/{location}/tagTemplates/{tag\_template\_id}/fields/{tag\_template\_field\_id}".
            force (bool): Required. Currently, this field must always be set to <code>true</code>.
                This confirms the deletion of this field from any tags using this field.
                <code>force = false</code> will be supported in the future.
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
        Creates a tag on an ``Entry``.

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
            parent (str): Required. The name of the resource to attach this tag to. Tags can be
                attached to Entries. (example:
                "projects/{project\_id}/locations/{location}/entryGroups/{entry\_group\_id}/entries/{entry\_id}").
                Note that this Tag and its child resources may not actually be stored in
                the location in this name.
            tag (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Tag]): Required. The tag to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Tag`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
            tag (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Tag]): Required. The updated tag.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Tag`
            update_mask (Union[dict, ~google.cloud.datacatalog_v1beta1.types.FieldMask]): Optional. The fields to update on the Tag. If absent or empty, all
                modifiable fields are updated. Currently the only modifiable field is
                the field ``fields``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
            name (str): Required. The name of the tag to delete. For example,
                "projects/{project\_id}/locations/{location}/entryGroups/{entry\_group\_id}/entries/{entry\_id}/tags/{tag\_id}".
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
        Lists the tags on an ``Entry``.

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
            parent (str): Required. The name of the Data Catalog resource to list the tags of. The
                resource could be an ``Entry``.
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
        Sets the access control policy for a resource. Replaces any existing
        policy. Supported resources are:

        -  Tag templates. Note, this method cannot be used to manage policies
           for BigQuery, Cloud Pub/Sub and any external Google Cloud Platform
           resources synced to Cloud Data Catalog.

        Callers must have following Google IAM permission
        ``datacatalog.tagTemplates.setIamPolicy`` to set policies on tag
        templates.

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
            policy (Union[dict, ~google.cloud.datacatalog_v1beta1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        Gets the access control policy for a resource. A ``NOT_FOUND`` error is
        returned if the resource does not exist. An empty policy is returned if
        the resource exists but does not have a policy set on it.

        Supported resources are:

        -  Tag templates. Note, this method cannot be used to manage policies
           for BigQuery, Cloud Pub/Sub and any external Google Cloud Platform
           resources synced to Cloud Data Catalog.

        Callers must have following Google IAM permission
        ``datacatalog.tagTemplates.getIamPolicy`` to get policies on tag
        templates.

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
            options_ (Union[dict, ~google.cloud.datacatalog_v1beta1.types.GetPolicyOptions]): OPTIONAL: A ``GetPolicyOptions`` object for specifying options to
                ``GetIamPolicy``. This field is only used by Cloud IAM.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datacatalog_v1beta1.types.GetPolicyOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        Returns the caller's permissions on a resource. If the resource does not
        exist, an empty set of permissions is returned (We don't return a
        ``NOT_FOUND`` error).

        Supported resource are:

        -  tag templates. Note, this method cannot be used to manage policies
           for BigQuery, Cloud Pub/Sub and any external Google Cloud Platform
           resources synced to Cloud Data Catalog.

        A caller is not required to have Google IAM permission to make this
        request.

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
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
