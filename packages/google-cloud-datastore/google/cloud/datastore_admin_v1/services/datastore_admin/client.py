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
from distutils import util
import os
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

OptionalRetry = Union[retries.Retry, object]

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.datastore_admin_v1.services.datastore_admin import pagers
from google.cloud.datastore_admin_v1.types import datastore_admin
from google.cloud.datastore_admin_v1.types import index
from google.protobuf import empty_pb2  # type: ignore
from .transports.base import DatastoreAdminTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import DatastoreAdminGrpcTransport
from .transports.grpc_asyncio import DatastoreAdminGrpcAsyncIOTransport


class DatastoreAdminClientMeta(type):
    """Metaclass for the DatastoreAdmin client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[DatastoreAdminTransport]]
    _transport_registry["grpc"] = DatastoreAdminGrpcTransport
    _transport_registry["grpc_asyncio"] = DatastoreAdminGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[DatastoreAdminTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class DatastoreAdminClient(metaclass=DatastoreAdminClientMeta):
    """Google Cloud Datastore Admin API
    The Datastore Admin API provides several admin services for
    Cloud Datastore.
    ## Concepts

    Project, namespace, kind, and entity as defined in the Google
    Cloud Datastore API.

    Operation: An Operation represents work being performed in the
    background.
    EntityFilter: Allows specifying a subset of entities in a
    project. This is specified as a combination of kinds and
    namespaces (either or both of which may be all).
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

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "datastore.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
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
            DatastoreAdminClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            DatastoreAdminClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DatastoreAdminTransport:
        """Returns the transport used by the client instance.

        Returns:
            DatastoreAdminTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, DatastoreAdminTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the datastore admin client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, DatastoreAdminTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                if is_mtls:
                    api_endpoint = self.DEFAULT_MTLS_ENDPOINT
                else:
                    api_endpoint = self.DEFAULT_ENDPOINT
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, DatastoreAdminTransport):
            # transport is a DatastoreAdminTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
            )

    def export_entities(
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
    ) -> operation.Operation:
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
            project_id (str):
                Required. Project ID against which to
                make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            labels (Sequence[google.cloud.datastore_admin_v1.types.ExportEntitiesRequest.LabelsEntry]):
                Client-assigned labels.
                This corresponds to the ``labels`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entity_filter (google.cloud.datastore_admin_v1.types.EntityFilter):
                Description of what data from the
                project is included in the export.

                This corresponds to the ``entity_filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            output_url_prefix (str):
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
            google.api_core.operation.Operation:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a datastore_admin.ExportEntitiesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore_admin.ExportEntitiesRequest):
            request = datastore_admin.ExportEntitiesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if labels is not None:
                request.labels = labels
            if entity_filter is not None:
                request.entity_filter = entity_filter
            if output_url_prefix is not None:
                request.output_url_prefix = output_url_prefix

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.export_entities]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            datastore_admin.ExportEntitiesResponse,
            metadata_type=datastore_admin.ExportEntitiesMetadata,
        )

        # Done; return the response.
        return response

    def import_entities(
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
    ) -> operation.Operation:
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
            project_id (str):
                Required. Project ID against which to
                make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            labels (Sequence[google.cloud.datastore_admin_v1.types.ImportEntitiesRequest.LabelsEntry]):
                Client-assigned labels.
                This corresponds to the ``labels`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            input_url (str):
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
            entity_filter (google.cloud.datastore_admin_v1.types.EntityFilter):
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
            google.api_core.operation.Operation:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a datastore_admin.ImportEntitiesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore_admin.ImportEntitiesRequest):
            request = datastore_admin.ImportEntitiesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if labels is not None:
                request.labels = labels
            if input_url is not None:
                request.input_url = input_url
            if entity_filter is not None:
                request.entity_filter = entity_filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.import_entities]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=datastore_admin.ImportEntitiesMetadata,
        )

        # Done; return the response.
        return response

    def create_index(
        self,
        request: Union[datastore_admin.CreateIndexRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.datastore_admin_v1.types.Index`
                Datastore composite index definition.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a datastore_admin.CreateIndexRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore_admin.CreateIndexRequest):
            request = datastore_admin.CreateIndexRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_index]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            index.Index,
            metadata_type=datastore_admin.IndexOperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_index(
        self,
        request: Union[datastore_admin.DeleteIndexRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.datastore_admin_v1.types.Index`
                Datastore composite index definition.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a datastore_admin.DeleteIndexRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore_admin.DeleteIndexRequest):
            request = datastore_admin.DeleteIndexRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_index]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            index.Index,
            metadata_type=datastore_admin.IndexOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_index(
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
        # Minor optimization to avoid making a copy if the user passes
        # in a datastore_admin.GetIndexRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore_admin.GetIndexRequest):
            request = datastore_admin.GetIndexRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_index]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_indexes(
        self,
        request: Union[datastore_admin.ListIndexesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListIndexesPager:
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
            google.cloud.datastore_admin_v1.services.datastore_admin.pagers.ListIndexesPager:
                The response for
                   [google.datastore.admin.v1.DatastoreAdmin.ListIndexes][google.datastore.admin.v1.DatastoreAdmin.ListIndexes].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a datastore_admin.ListIndexesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore_admin.ListIndexesRequest):
            request = datastore_admin.ListIndexesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_indexes]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListIndexesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-datastore-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DatastoreAdminClient",)
