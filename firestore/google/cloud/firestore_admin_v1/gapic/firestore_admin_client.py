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

"""Accesses the google.firestore.admin.v1 FirestoreAdmin API."""

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

from google.cloud.firestore_admin_v1.gapic import enums
from google.cloud.firestore_admin_v1.gapic import firestore_admin_client_config
from google.cloud.firestore_admin_v1.gapic.transports import (
    firestore_admin_grpc_transport,
)
from google.cloud.firestore_admin_v1.proto import field_pb2
from google.cloud.firestore_admin_v1.proto import firestore_admin_pb2
from google.cloud.firestore_admin_v1.proto import firestore_admin_pb2_grpc
from google.cloud.firestore_admin_v1.proto import index_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-firestore"
).version


class FirestoreAdminClient(object):
    """
    Operations are created by service ``FirestoreAdmin``, but are accessed
    via service ``google.longrunning.Operations``.
    """

    SERVICE_ADDRESS = "firestore.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.firestore.admin.v1.FirestoreAdmin"

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
            FirestoreAdminClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def database_path(cls, project, database):
        """Return a fully-qualified database string."""
        return google.api_core.path_template.expand(
            "projects/{project}/databases/{database}",
            project=project,
            database=database,
        )

    @classmethod
    def field_path(cls, project, database, collection_id, field_id):
        """Return a fully-qualified field string."""
        return google.api_core.path_template.expand(
            "projects/{project}/databases/{database}/collectionGroups/{collection_id}/fields/{field_id}",
            project=project,
            database=database,
            collection_id=collection_id,
            field_id=field_id,
        )

    @classmethod
    def index_path(cls, project, database, collection_id, index_id):
        """Return a fully-qualified index string."""
        return google.api_core.path_template.expand(
            "projects/{project}/databases/{database}/collectionGroups/{collection_id}/indexes/{index_id}",
            project=project,
            database=database,
            collection_id=collection_id,
            index_id=index_id,
        )

    @classmethod
    def parent_path(cls, project, database, collection_id):
        """Return a fully-qualified parent string."""
        return google.api_core.path_template.expand(
            "projects/{project}/databases/{database}/collectionGroups/{collection_id}",
            project=project,
            database=database,
            collection_id=collection_id,
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
            transport (Union[~.FirestoreAdminGrpcTransport,
                    Callable[[~.Credentials, type], ~.FirestoreAdminGrpcTransport]): A transport
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
            client_config = firestore_admin_client_config.config

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
                    default_class=firestore_admin_grpc_transport.FirestoreAdminGrpcTransport,
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
            self.transport = firestore_admin_grpc_transport.FirestoreAdminGrpcTransport(
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
    def create_index(
        self,
        parent,
        index,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a composite index. This returns a
        ``google.longrunning.Operation`` which may be used to track the status
        of the creation. The metadata for the operation will be the type
        ``IndexOperationMetadata``.

        Example:
            >>> from google.cloud import firestore_admin_v1
            >>>
            >>> client = firestore_admin_v1.FirestoreAdminClient()
            >>>
            >>> parent = client.parent_path('[PROJECT]', '[DATABASE]', '[COLLECTION_ID]')
            >>>
            >>> # TODO: Initialize `index`:
            >>> index = {}
            >>>
            >>> response = client.create_index(parent, index)

        Args:
            parent (str): Required. A parent name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}``
            index (Union[dict, ~google.cloud.firestore_admin_v1.types.Index]): Required. The composite index to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_admin_v1.types.Index`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_admin_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_index" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_index"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_index,
                default_retry=self._method_configs["CreateIndex"].retry,
                default_timeout=self._method_configs["CreateIndex"].timeout,
                client_info=self._client_info,
            )

        request = firestore_admin_pb2.CreateIndexRequest(parent=parent, index=index)
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

        return self._inner_api_calls["create_index"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_indexes(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists composite indexes.

        Example:
            >>> from google.cloud import firestore_admin_v1
            >>>
            >>> client = firestore_admin_v1.FirestoreAdminClient()
            >>>
            >>> parent = client.parent_path('[PROJECT]', '[DATABASE]', '[COLLECTION_ID]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_indexes(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_indexes(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. A parent name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}``
            filter_ (str): The filter to apply to list results.
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
            An iterable of :class:`~google.cloud.firestore_admin_v1.types.Index` instances.
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
        if "list_indexes" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_indexes"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_indexes,
                default_retry=self._method_configs["ListIndexes"].retry,
                default_timeout=self._method_configs["ListIndexes"].timeout,
                client_info=self._client_info,
            )

        request = firestore_admin_pb2.ListIndexesRequest(
            parent=parent, filter=filter_, page_size=page_size
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
                self._inner_api_calls["list_indexes"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="indexes",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_index(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a composite index.

        Example:
            >>> from google.cloud import firestore_admin_v1
            >>>
            >>> client = firestore_admin_v1.FirestoreAdminClient()
            >>>
            >>> name = client.index_path('[PROJECT]', '[DATABASE]', '[COLLECTION_ID]', '[INDEX_ID]')
            >>>
            >>> response = client.get_index(name)

        Args:
            name (str): Required. A name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/indexes/{index_id}``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_admin_v1.types.Index` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_index" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_index"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_index,
                default_retry=self._method_configs["GetIndex"].retry,
                default_timeout=self._method_configs["GetIndex"].timeout,
                client_info=self._client_info,
            )

        request = firestore_admin_pb2.GetIndexRequest(name=name)
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

        return self._inner_api_calls["get_index"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_index(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a composite index.

        Example:
            >>> from google.cloud import firestore_admin_v1
            >>>
            >>> client = firestore_admin_v1.FirestoreAdminClient()
            >>>
            >>> name = client.index_path('[PROJECT]', '[DATABASE]', '[COLLECTION_ID]', '[INDEX_ID]')
            >>>
            >>> client.delete_index(name)

        Args:
            name (str): Required. A name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/indexes/{index_id}``
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
        if "delete_index" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_index"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_index,
                default_retry=self._method_configs["DeleteIndex"].retry,
                default_timeout=self._method_configs["DeleteIndex"].timeout,
                client_info=self._client_info,
            )

        request = firestore_admin_pb2.DeleteIndexRequest(name=name)
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

        self._inner_api_calls["delete_index"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def import_documents(
        self,
        name,
        collection_ids=None,
        input_uri_prefix=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Imports documents into Google Cloud Firestore. Existing documents with the
        same name are overwritten. The import occurs in the background and its
        progress can be monitored and managed via the Operation resource that is
        created. If an ImportDocuments operation is cancelled, it is possible
        that a subset of the data has already been imported to Cloud Firestore.

        Example:
            >>> from google.cloud import firestore_admin_v1
            >>>
            >>> client = firestore_admin_v1.FirestoreAdminClient()
            >>>
            >>> name = client.database_path('[PROJECT]', '[DATABASE]')
            >>>
            >>> response = client.import_documents(name)

        Args:
            name (str): Required. Database to import into. Should be of the form:
                ``projects/{project_id}/databases/{database_id}``.
            collection_ids (list[str]): Which collection ids to import. Unspecified means all collections included
                in the import.
            input_uri_prefix (str): Location of the exported files. This must match the output\_uri\_prefix
                of an ExportDocumentsResponse from an export that has completed
                successfully. See:
                ``google.firestore.admin.v1.ExportDocumentsResponse.output_uri_prefix``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_admin_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "import_documents" not in self._inner_api_calls:
            self._inner_api_calls[
                "import_documents"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.import_documents,
                default_retry=self._method_configs["ImportDocuments"].retry,
                default_timeout=self._method_configs["ImportDocuments"].timeout,
                client_info=self._client_info,
            )

        request = firestore_admin_pb2.ImportDocumentsRequest(
            name=name, collection_ids=collection_ids, input_uri_prefix=input_uri_prefix
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

        return self._inner_api_calls["import_documents"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def export_documents(
        self,
        name,
        collection_ids=None,
        output_uri_prefix=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Exports a copy of all or a subset of documents from Google Cloud Firestore
        to another storage system, such as Google Cloud Storage. Recent updates to
        documents may not be reflected in the export. The export occurs in the
        background and its progress can be monitored and managed via the
        Operation resource that is created. The output of an export may only be
        used once the associated operation is done. If an export operation is
        cancelled before completion it may leave partial data behind in Google
        Cloud Storage.

        Example:
            >>> from google.cloud import firestore_admin_v1
            >>>
            >>> client = firestore_admin_v1.FirestoreAdminClient()
            >>>
            >>> name = client.database_path('[PROJECT]', '[DATABASE]')
            >>>
            >>> response = client.export_documents(name)

        Args:
            name (str): Required. Database to export. Should be of the form:
                ``projects/{project_id}/databases/{database_id}``.
            collection_ids (list[str]): Which collection ids to export. Unspecified means all collections.
            output_uri_prefix (str): The output URI. Currently only supports Google Cloud Storage URIs of the
                form: ``gs://BUCKET_NAME[/NAMESPACE_PATH]``, where ``BUCKET_NAME`` is
                the name of the Google Cloud Storage bucket and ``NAMESPACE_PATH`` is an
                optional Google Cloud Storage namespace path. When choosing a name, be
                sure to consider Google Cloud Storage naming guidelines:
                https://cloud.google.com/storage/docs/naming. If the URI is a bucket
                (without a namespace path), a prefix will be generated based on the
                start time.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_admin_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "export_documents" not in self._inner_api_calls:
            self._inner_api_calls[
                "export_documents"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.export_documents,
                default_retry=self._method_configs["ExportDocuments"].retry,
                default_timeout=self._method_configs["ExportDocuments"].timeout,
                client_info=self._client_info,
            )

        request = firestore_admin_pb2.ExportDocumentsRequest(
            name=name,
            collection_ids=collection_ids,
            output_uri_prefix=output_uri_prefix,
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

        return self._inner_api_calls["export_documents"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_field(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the metadata and configuration for a Field.

        Example:
            >>> from google.cloud import firestore_admin_v1
            >>>
            >>> client = firestore_admin_v1.FirestoreAdminClient()
            >>>
            >>> name = client.field_path('[PROJECT]', '[DATABASE]', '[COLLECTION_ID]', '[FIELD_ID]')
            >>>
            >>> response = client.get_field(name)

        Args:
            name (str): Required. A name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/fields/{field_id}``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_admin_v1.types.Field` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_field" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_field"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_field,
                default_retry=self._method_configs["GetField"].retry,
                default_timeout=self._method_configs["GetField"].timeout,
                client_info=self._client_info,
            )

        request = firestore_admin_pb2.GetFieldRequest(name=name)
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

        return self._inner_api_calls["get_field"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_fields(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the field configuration and metadata for this database.

        Currently, ``FirestoreAdmin.ListFields`` only supports listing fields
        that have been explicitly overridden. To issue this query, call
        ``FirestoreAdmin.ListFields`` with the filter set to
        ``indexConfig.usesAncestorConfig:false``.

        Example:
            >>> from google.cloud import firestore_admin_v1
            >>>
            >>> client = firestore_admin_v1.FirestoreAdminClient()
            >>>
            >>> parent = client.parent_path('[PROJECT]', '[DATABASE]', '[COLLECTION_ID]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_fields(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_fields(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. A parent name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}``
            filter_ (str): The filter to apply to list results. Currently,
                ``FirestoreAdmin.ListFields`` only supports listing fields that have
                been explicitly overridden. To issue this query, call
                ``FirestoreAdmin.ListFields`` with the filter set to
                ``indexConfig.usesAncestorConfig:false``.
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
            An iterable of :class:`~google.cloud.firestore_admin_v1.types.Field` instances.
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
        if "list_fields" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_fields"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_fields,
                default_retry=self._method_configs["ListFields"].retry,
                default_timeout=self._method_configs["ListFields"].timeout,
                client_info=self._client_info,
            )

        request = firestore_admin_pb2.ListFieldsRequest(
            parent=parent, filter=filter_, page_size=page_size
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
                self._inner_api_calls["list_fields"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="fields",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_field(
        self,
        field,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a field configuration. Currently, field updates apply only to
        single field index configuration. However, calls to
        ``FirestoreAdmin.UpdateField`` should provide a field mask to avoid
        changing any configuration that the caller isn't aware of. The field
        mask should be specified as: ``{ paths: "index_config" }``.

        This call returns a ``google.longrunning.Operation`` which may be used
        to track the status of the field update. The metadata for the operation
        will be the type ``FieldOperationMetadata``.

        To configure the default field settings for the database, use the
        special ``Field`` with resource name:
        ``projects/{project_id}/databases/{database_id}/collectionGroups/__default__/fields/*``.

        Example:
            >>> from google.cloud import firestore_admin_v1
            >>>
            >>> client = firestore_admin_v1.FirestoreAdminClient()
            >>>
            >>> # TODO: Initialize `field`:
            >>> field = {}
            >>>
            >>> response = client.update_field(field)

        Args:
            field (Union[dict, ~google.cloud.firestore_admin_v1.types.Field]): Required. The field to be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_admin_v1.types.Field`
            update_mask (Union[dict, ~google.cloud.firestore_admin_v1.types.FieldMask]): A mask, relative to the field. If specified, only configuration
                specified by this field\_mask will be updated in the field.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_admin_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.firestore_admin_v1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_field" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_field"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_field,
                default_retry=self._method_configs["UpdateField"].retry,
                default_timeout=self._method_configs["UpdateField"].timeout,
                client_info=self._client_info,
            )

        request = firestore_admin_pb2.UpdateFieldRequest(
            field=field, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("field.name", field.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_field"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
