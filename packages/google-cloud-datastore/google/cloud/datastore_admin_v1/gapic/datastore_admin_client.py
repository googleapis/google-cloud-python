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

"""Accesses the google.datastore.admin.v1 DatastoreAdmin API."""

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
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import grpc

from google.cloud.datastore_admin_v1.gapic import datastore_admin_client_config
from google.cloud.datastore_admin_v1.gapic import enums
from google.cloud.datastore_admin_v1.gapic.transports import (
    datastore_admin_grpc_transport,
)
from google.cloud.datastore_admin_v1.proto import datastore_admin_pb2
from google.cloud.datastore_admin_v1.proto import datastore_admin_pb2_grpc
from google.cloud.datastore_admin_v1.proto import index_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-datastore",
).version


class DatastoreAdminClient(object):
    """
    Google Cloud Datastore Admin API


    The Datastore Admin API provides several admin services for Cloud Datastore.

    ## Concepts

    Project, namespace, kind, and entity as defined in the Google Cloud Datastore
    API.

    Operation: An Operation represents work being performed in the background.

    EntityFilter: Allows specifying a subset of entities in a project. This is
    specified as a combination of kinds and namespaces (either or both of which
    may be all).

    ## Services

    # Export/Import

    The Export/Import service provides the ability to copy all or a subset of
    entities to/from Google Cloud Storage.

    Exported data may be imported into Cloud Datastore for any Google Cloud
    Platform project. It is not restricted to the export source project. It is
    possible to export from one project and then import into another.

    Exported data can also be loaded into Google BigQuery for analysis.

    Exports and imports are performed asynchronously. An Operation resource is
    created for each export/import. The state (including any errors encountered)
    of the export/import may be queried via the Operation resource.

    # Index

    The index service manages Cloud Datastore composite indexes.

    Index creation and deletion are performed asynchronously.
    An Operation resource is created for each such asynchronous operation.
    The state of the operation (including any errors encountered)
    may be queried via the Operation resource.

    # Operation

    The Operations collection provides a record of actions performed for the
    specified project (including any operations in progress). Operations are not
    created directly but through calls on other collections or resources.

    An operation that is not yet done may be cancelled. The request to cancel is
    asynchronous and the operation may continue to run for some time after the
    request to cancel is made.

    An operation that is done may be deleted so that it is no longer listed as
    part of the Operation collection.

    ListOperations returns all pending operations, but not completed operations.

    Operations are created by service DatastoreAdmin,
    but are accessed via service google.longrunning.Operations.
    """

    SERVICE_ADDRESS = "datastore.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.datastore.admin.v1.DatastoreAdmin"

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
            DatastoreAdminClient: The constructed client.
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
            transport (Union[~.DatastoreAdminGrpcTransport,
                    Callable[[~.Credentials, type], ~.DatastoreAdminGrpcTransport]): A transport
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
            client_config = datastore_admin_client_config.config

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
                    default_class=datastore_admin_grpc_transport.DatastoreAdminGrpcTransport,
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
            self.transport = datastore_admin_grpc_transport.DatastoreAdminGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials,
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION,
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME],
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def export_entities(
        self,
        project_id,
        output_url_prefix,
        labels=None,
        entity_filter=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Exports a copy of all or a subset of entities from Google Cloud Datastore
        to another storage system, such as Google Cloud Storage. Recent updates to
        entities may not be reflected in the export. The export occurs in the
        background and its progress can be monitored and managed via the
        Operation resource that is created. The output of an export may only be
        used once the associated operation is done. If an export operation is
        cancelled before completion it may leave partial data behind in Google
        Cloud Storage.

        Example:
            >>> from google.cloud import datastore_admin_v1
            >>>
            >>> client = datastore_admin_v1.DatastoreAdminClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `output_url_prefix`:
            >>> output_url_prefix = ''
            >>>
            >>> response = client.export_entities(project_id, output_url_prefix)
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
            project_id (str): Required. Project ID against which to make the request.
            output_url_prefix (str): Required. Location for the export metadata and data files.

                The full resource URL of the external storage location. Currently, only
                Google Cloud Storage is supported. So output_url_prefix should be of the
                form: ``gs://BUCKET_NAME[/NAMESPACE_PATH]``, where ``BUCKET_NAME`` is
                the name of the Cloud Storage bucket and ``NAMESPACE_PATH`` is an
                optional Cloud Storage namespace path (this is not a Cloud Datastore
                namespace). For more information about Cloud Storage namespace paths,
                see `Object name
                considerations <https://cloud.google.com/storage/docs/naming#object-considerations>`__.

                The resulting files will be nested deeper than the specified URL prefix.
                The final output URL will be provided in the
                ``google.datastore.admin.v1.ExportEntitiesResponse.output_url`` field.
                That value should be used for subsequent ImportEntities operations.

                By nesting the data files deeper, the same Cloud Storage bucket can be
                used in multiple ExportEntities operations without conflict.
            labels (dict[str -> str]): Client-assigned labels.
            entity_filter (Union[dict, ~google.cloud.datastore_admin_v1.types.EntityFilter]): Description of what data from the project is included in the export.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_admin_v1.types.EntityFilter`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datastore_admin_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "export_entities" not in self._inner_api_calls:
            self._inner_api_calls[
                "export_entities"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.export_entities,
                default_retry=self._method_configs["ExportEntities"].retry,
                default_timeout=self._method_configs["ExportEntities"].timeout,
                client_info=self._client_info,
            )

        request = datastore_admin_pb2.ExportEntitiesRequest(
            project_id=project_id,
            output_url_prefix=output_url_prefix,
            labels=labels,
            entity_filter=entity_filter,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project_id", project_id)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["export_entities"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            datastore_admin_pb2.ExportEntitiesResponse,
            metadata_type=datastore_admin_pb2.ExportEntitiesMetadata,
        )

    def import_entities(
        self,
        project_id,
        input_url,
        labels=None,
        entity_filter=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Imports entities into Google Cloud Datastore. Existing entities with the
        same key are overwritten. The import occurs in the background and its
        progress can be monitored and managed via the Operation resource that is
        created. If an ImportEntities operation is cancelled, it is possible
        that a subset of the data has already been imported to Cloud Datastore.

        Example:
            >>> from google.cloud import datastore_admin_v1
            >>>
            >>> client = datastore_admin_v1.DatastoreAdminClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `input_url`:
            >>> input_url = ''
            >>>
            >>> response = client.import_entities(project_id, input_url)
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
            project_id (str): Required. Project ID against which to make the request.
            input_url (str): Required. The full resource URL of the external storage location.
                Currently, only Google Cloud Storage is supported. So input_url should
                be of the form:
                ``gs://BUCKET_NAME[/NAMESPACE_PATH]/OVERALL_EXPORT_METADATA_FILE``,
                where ``BUCKET_NAME`` is the name of the Cloud Storage bucket,
                ``NAMESPACE_PATH`` is an optional Cloud Storage namespace path (this is
                not a Cloud Datastore namespace), and ``OVERALL_EXPORT_METADATA_FILE``
                is the metadata file written by the ExportEntities operation. For more
                information about Cloud Storage namespace paths, see `Object name
                considerations <https://cloud.google.com/storage/docs/naming#object-considerations>`__.

                For more information, see
                ``google.datastore.admin.v1.ExportEntitiesResponse.output_url``.
            labels (dict[str -> str]): Client-assigned labels.
            entity_filter (Union[dict, ~google.cloud.datastore_admin_v1.types.EntityFilter]): Optionally specify which kinds/namespaces are to be imported. If
                provided, the list must be a subset of the EntityFilter used in creating
                the export, otherwise a FAILED_PRECONDITION error will be returned. If
                no filter is specified then all entities from the export are imported.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_admin_v1.types.EntityFilter`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datastore_admin_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "import_entities" not in self._inner_api_calls:
            self._inner_api_calls[
                "import_entities"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.import_entities,
                default_retry=self._method_configs["ImportEntities"].retry,
                default_timeout=self._method_configs["ImportEntities"].timeout,
                client_info=self._client_info,
            )

        request = datastore_admin_pb2.ImportEntitiesRequest(
            project_id=project_id,
            input_url=input_url,
            labels=labels,
            entity_filter=entity_filter,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project_id", project_id)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["import_entities"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=datastore_admin_pb2.ImportEntitiesMetadata,
        )

    def get_index(
        self,
        project_id=None,
        index_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets an index.

        Example:
            >>> from google.cloud import datastore_admin_v1
            >>>
            >>> client = datastore_admin_v1.DatastoreAdminClient()
            >>>
            >>> response = client.get_index()

        Args:
            project_id (str): Project ID against which to make the request.
            index_id (str): The resource ID of the index to get.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datastore_admin_v1.types.Index` instance.

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

        request = datastore_admin_pb2.GetIndexRequest(
            project_id=project_id, index_id=index_id,
        )
        return self._inner_api_calls["get_index"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_indexes(
        self,
        project_id=None,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the indexes that match the specified filters.  Datastore uses an
        eventually consistent query to fetch the list of indexes and may
        occasionally return stale results.

        Example:
            >>> from google.cloud import datastore_admin_v1
            >>>
            >>> client = datastore_admin_v1.DatastoreAdminClient()
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_indexes():
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_indexes().pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project_id (str): Project ID against which to make the request.
            filter_ (str)
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
            An iterable of :class:`~google.cloud.datastore_admin_v1.types.Index` instances.
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

        request = datastore_admin_pb2.ListIndexesRequest(
            project_id=project_id, filter=filter_, page_size=page_size,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project_id", project_id)]
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
