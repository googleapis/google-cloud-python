# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

OptionalRetry = Union[retries.Retry, object]

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.datastore_admin_v1.services.datastore_admin import pagers
from google.cloud.datastore_admin_v1.types import datastore_admin
from google.cloud.datastore_admin_v1.types import index
from google.protobuf import empty_pb2  # type: ignore
from .transports.base import DatastoreAdminTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import DatastoreAdminGrpcAsyncIOTransport
from .client import DatastoreAdminClient


class DatastoreAdminAsyncClient:
    """Google Cloud Datastore Admin API
    The Datastore Admin API provides several admin services for
    Cloud Datastore.
    -----------------------------------------------------------------------------
    ## Concepts

    Project, namespace, kind, and entity as defined in the Google
    Cloud Datastore API.

    Operation: An Operation represents work being performed in the
    background.
    EntityFilter: Allows specifying a subset of entities in a
    project. This is specified as a combination of kinds and
    namespaces (either or both of which may be all).

    -----------------------------------------------------------------------------
    ## Services

    # Export/Import

    The Export/Import service provides the ability to copy all or a
    subset of entities to/from Google Cloud Storage.

    Exported data may be imported into Cloud Datastore for any
    Google Cloud Platform project. It is not restricted to the
    export source project. It is possible to export from one project
    and then import into another.
    Exported data can also be loaded into Google BigQuery for
    analysis.
    Exports and imports are performed asynchronously. An Operation
    resource is created for each export/import. The state (including
    any errors encountered) of the export/import may be queried via
    the Operation resource.
    # Index

    The index service manages Cloud Datastore composite indexes.
    Index creation and deletion are performed asynchronously. An
    Operation resource is created for each such asynchronous
    operation. The state of the operation (including any errors
    encountered) may be queried via the Operation resource.

    # Operation

    The Operations collection provides a record of actions performed
    for the specified project (including any operations in
    progress). Operations are not created directly but through calls
    on other collections or resources.
    An operation that is not yet done may be cancelled. The request
    to cancel is asynchronous and the operation may continue to run
    for some time after the request to cancel is made.

    An operation that is done may be deleted so that it is no longer
    listed as part of the Operation collection.

    ListOperations returns all pending operations, but not completed
    operations.
    Operations are created by service DatastoreAdmin,
    but are accessed via service google.longrunning.Operations.
    """

    _client: DatastoreAdminClient

    DEFAULT_ENDPOINT = DatastoreAdminClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DatastoreAdminClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        DatastoreAdminClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        DatastoreAdminClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(DatastoreAdminClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        DatastoreAdminClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        DatastoreAdminClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        DatastoreAdminClient.parse_common_organization_path
    )
    common_project_path = staticmethod(DatastoreAdminClient.common_project_path)
    parse_common_project_path = staticmethod(
        DatastoreAdminClient.parse_common_project_path
    )
    common_location_path = staticmethod(DatastoreAdminClient.common_location_path)
    parse_common_location_path = staticmethod(
        DatastoreAdminClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DatastoreAdminAsyncClient: The constructed client.
        """
        return DatastoreAdminClient.from_service_account_info.__func__(DatastoreAdminAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DatastoreAdminAsyncClient: The constructed client.
        """
        return DatastoreAdminClient.from_service_account_file.__func__(DatastoreAdminAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DatastoreAdminTransport:
        """Returns the transport used by the client instance.

        Returns:
            DatastoreAdminTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(DatastoreAdminClient).get_transport_class, type(DatastoreAdminClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, DatastoreAdminTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the datastore admin client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.DatastoreAdminTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = DatastoreAdminClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def export_entities(
        self,
        request: Union[datastore_admin.ExportEntitiesRequest, dict] = None,
        *,
        project_id: str = None,
        labels: Sequence[datastore_admin.ExportEntitiesRequest.LabelsEntry] = None,
        entity_filter: datastore_admin.EntityFilter = None,
        output_url_prefix: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Exports a copy of all or a subset of entities from
        Google Cloud Datastore to another storage system, such
        as Google Cloud Storage. Recent updates to entities may
        not be reflected in the export. The export occurs in the
        background and its progress can be monitored and managed
        via the Operation resource that is created. The output
        of an export may only be used once the associated
        operation is done. If an export operation is cancelled
        before completion it may leave partial data behind in
        Google Cloud Storage.

        Args:
            request (Union[google.cloud.datastore_admin_v1.types.ExportEntitiesRequest, dict]):
                The request object. The request for
                [google.datastore.admin.v1.DatastoreAdmin.ExportEntities][google.datastore.admin.v1.DatastoreAdmin.ExportEntities].
            project_id (:class:`str`):
                Required. Project ID against which to
                make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            labels (:class:`Sequence[google.cloud.datastore_admin_v1.types.ExportEntitiesRequest.LabelsEntry]`):
                Client-assigned labels.
                This corresponds to the ``labels`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entity_filter (:class:`google.cloud.datastore_admin_v1.types.EntityFilter`):
                Description of what data from the
                project is included in the export.

                This corresponds to the ``entity_filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            output_url_prefix (:class:`str`):
                Required. Location for the export metadata and data
                files.

                The full resource URL of the external storage location.
                Currently, only Google Cloud Storage is supported. So
                output_url_prefix should be of the form:
                ``gs://BUCKET_NAME[/NAMESPACE_PATH]``, where
                ``BUCKET_NAME`` is the name of the Cloud Storage bucket
                and ``NAMESPACE_PATH`` is an optional Cloud Storage
                namespace path (this is not a Cloud Datastore
                namespace). For more information about Cloud Storage
                namespace paths, see `Object name
                considerations <https://cloud.google.com/storage/docs/naming#object-considerations>`__.

                The resulting files will be nested deeper than the
                specified URL prefix. The final output URL will be
                provided in the
                [google.datastore.admin.v1.ExportEntitiesResponse.output_url][google.datastore.admin.v1.ExportEntitiesResponse.output_url]
                field. That value should be used for subsequent
                ImportEntities operations.

                By nesting the data files deeper, the same Cloud Storage
                bucket can be used in multiple ExportEntities operations
                without conflict.

                This corresponds to the ``output_url_prefix`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.datastore_admin_v1.types.ExportEntitiesResponse` The response for
                   [google.datastore.admin.v1.DatastoreAdmin.ExportEntities][google.datastore.admin.v1.DatastoreAdmin.ExportEntities].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project_id, labels, entity_filter, output_url_prefix]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datastore_admin.ExportEntitiesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if entity_filter is not None:
            request.entity_filter = entity_filter
        if output_url_prefix is not None:
            request.output_url_prefix = output_url_prefix

        if labels:
            request.labels.update(labels)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.export_entities,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            datastore_admin.ExportEntitiesResponse,
            metadata_type=datastore_admin.ExportEntitiesMetadata,
        )

        # Done; return the response.
        return response

    async def import_entities(
        self,
        request: Union[datastore_admin.ImportEntitiesRequest, dict] = None,
        *,
        project_id: str = None,
        labels: Sequence[datastore_admin.ImportEntitiesRequest.LabelsEntry] = None,
        input_url: str = None,
        entity_filter: datastore_admin.EntityFilter = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Imports entities into Google Cloud Datastore.
        Existing entities with the same key are overwritten. The
        import occurs in the background and its progress can be
        monitored and managed via the Operation resource that is
        created. If an ImportEntities operation is cancelled, it
        is possible that a subset of the data has already been
        imported to Cloud Datastore.

        Args:
            request (Union[google.cloud.datastore_admin_v1.types.ImportEntitiesRequest, dict]):
                The request object. The request for
                [google.datastore.admin.v1.DatastoreAdmin.ImportEntities][google.datastore.admin.v1.DatastoreAdmin.ImportEntities].
            project_id (:class:`str`):
                Required. Project ID against which to
                make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            labels (:class:`Sequence[google.cloud.datastore_admin_v1.types.ImportEntitiesRequest.LabelsEntry]`):
                Client-assigned labels.
                This corresponds to the ``labels`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            input_url (:class:`str`):
                Required. The full resource URL of the external storage
                location. Currently, only Google Cloud Storage is
                supported. So input_url should be of the form:
                ``gs://BUCKET_NAME[/NAMESPACE_PATH]/OVERALL_EXPORT_METADATA_FILE``,
                where ``BUCKET_NAME`` is the name of the Cloud Storage
                bucket, ``NAMESPACE_PATH`` is an optional Cloud Storage
                namespace path (this is not a Cloud Datastore
                namespace), and ``OVERALL_EXPORT_METADATA_FILE`` is the
                metadata file written by the ExportEntities operation.
                For more information about Cloud Storage namespace
                paths, see `Object name
                considerations <https://cloud.google.com/storage/docs/naming#object-considerations>`__.

                For more information, see
                [google.datastore.admin.v1.ExportEntitiesResponse.output_url][google.datastore.admin.v1.ExportEntitiesResponse.output_url].

                This corresponds to the ``input_url`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entity_filter (:class:`google.cloud.datastore_admin_v1.types.EntityFilter`):
                Optionally specify which kinds/namespaces are to be
                imported. If provided, the list must be a subset of the
                EntityFilter used in creating the export, otherwise a
                FAILED_PRECONDITION error will be returned. If no filter
                is specified then all entities from the export are
                imported.

                This corresponds to the ``entity_filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, labels, input_url, entity_filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datastore_admin.ImportEntitiesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if input_url is not None:
            request.input_url = input_url
        if entity_filter is not None:
            request.entity_filter = entity_filter

        if labels:
            request.labels.update(labels)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_entities,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=datastore_admin.ImportEntitiesMetadata,
        )

        # Done; return the response.
        return response

    async def create_index(
        self,
        request: Union[datastore_admin.CreateIndexRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates the specified index. A newly created index's initial
        state is ``CREATING``. On completion of the returned
        [google.longrunning.Operation][google.longrunning.Operation],
        the state will be ``READY``. If the index already exists, the
        call will return an ``ALREADY_EXISTS`` status.

        During index creation, the process could result in an error, in
        which case the index will move to the ``ERROR`` state. The
        process can be recovered by fixing the data that caused the
        error, removing the index with
        [delete][google.datastore.admin.v1.DatastoreAdmin.DeleteIndex],
        then re-creating the index with [create]
        [google.datastore.admin.v1.DatastoreAdmin.CreateIndex].

        Indexes with a single property cannot be created.

        Args:
            request (Union[google.cloud.datastore_admin_v1.types.CreateIndexRequest, dict]):
                The request object. The request for
                [google.datastore.admin.v1.DatastoreAdmin.CreateIndex][google.datastore.admin.v1.DatastoreAdmin.CreateIndex].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.datastore_admin_v1.types.Index`
                Datastore composite index definition.

        """
        # Create or coerce a protobuf request object.
        request = datastore_admin.CreateIndexRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_index,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            index.Index,
            metadata_type=datastore_admin.IndexOperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_index(
        self,
        request: Union[datastore_admin.DeleteIndexRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes an existing index. An index can only be deleted if it is
        in a ``READY`` or ``ERROR`` state. On successful execution of
        the request, the index will be in a ``DELETING``
        [state][google.datastore.admin.v1.Index.State]. And on
        completion of the returned
        [google.longrunning.Operation][google.longrunning.Operation],
        the index will be removed.

        During index deletion, the process could result in an error, in
        which case the index will move to the ``ERROR`` state. The
        process can be recovered by fixing the data that caused the
        error, followed by calling
        [delete][google.datastore.admin.v1.DatastoreAdmin.DeleteIndex]
        again.

        Args:
            request (Union[google.cloud.datastore_admin_v1.types.DeleteIndexRequest, dict]):
                The request object. The request for
                [google.datastore.admin.v1.DatastoreAdmin.DeleteIndex][google.datastore.admin.v1.DatastoreAdmin.DeleteIndex].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.datastore_admin_v1.types.Index`
                Datastore composite index definition.

        """
        # Create or coerce a protobuf request object.
        request = datastore_admin.DeleteIndexRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_index,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            index.Index,
            metadata_type=datastore_admin.IndexOperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_index(
        self,
        request: Union[datastore_admin.GetIndexRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> index.Index:
        r"""Gets an index.

        Args:
            request (Union[google.cloud.datastore_admin_v1.types.GetIndexRequest, dict]):
                The request object. The request for
                [google.datastore.admin.v1.DatastoreAdmin.GetIndex][google.datastore.admin.v1.DatastoreAdmin.GetIndex].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datastore_admin_v1.types.Index:
                Datastore composite index definition.
        """
        # Create or coerce a protobuf request object.
        request = datastore_admin.GetIndexRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_index,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_indexes(
        self,
        request: Union[datastore_admin.ListIndexesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListIndexesAsyncPager:
        r"""Lists the indexes that match the specified filters.
        Datastore uses an eventually consistent query to fetch
        the list of indexes and may occasionally return stale
        results.

        Args:
            request (Union[google.cloud.datastore_admin_v1.types.ListIndexesRequest, dict]):
                The request object. The request for
                [google.datastore.admin.v1.DatastoreAdmin.ListIndexes][google.datastore.admin.v1.DatastoreAdmin.ListIndexes].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datastore_admin_v1.services.datastore_admin.pagers.ListIndexesAsyncPager:
                The response for
                   [google.datastore.admin.v1.DatastoreAdmin.ListIndexes][google.datastore.admin.v1.DatastoreAdmin.ListIndexes].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = datastore_admin.ListIndexesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_indexes,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListIndexesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-datastore-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DatastoreAdminAsyncClient",)
