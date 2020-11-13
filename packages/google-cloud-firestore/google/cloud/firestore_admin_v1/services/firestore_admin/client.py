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
from typing import Callable, Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation as ga_operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.firestore_admin_v1.services.firestore_admin import pagers
from google.cloud.firestore_admin_v1.types import field
from google.cloud.firestore_admin_v1.types import field as gfa_field
from google.cloud.firestore_admin_v1.types import firestore_admin
from google.cloud.firestore_admin_v1.types import index
from google.cloud.firestore_admin_v1.types import index as gfa_index
from google.cloud.firestore_admin_v1.types import operation as gfa_operation
from google.protobuf import empty_pb2 as empty  # type: ignore

from .transports.base import FirestoreAdminTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import FirestoreAdminGrpcTransport
from .transports.grpc_asyncio import FirestoreAdminGrpcAsyncIOTransport


class FirestoreAdminClientMeta(type):
    """Metaclass for the FirestoreAdmin client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[FirestoreAdminTransport]]
    _transport_registry["grpc"] = FirestoreAdminGrpcTransport
    _transport_registry["grpc_asyncio"] = FirestoreAdminGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[FirestoreAdminTransport]:
        """Return an appropriate transport class.

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


class FirestoreAdminClient(metaclass=FirestoreAdminClientMeta):
    """Operations are created by service ``FirestoreAdmin``, but are
    accessed via service ``google.longrunning.Operations``.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
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

    DEFAULT_ENDPOINT = "firestore.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

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
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> FirestoreAdminTransport:
        """Return the transport used by the client instance.

        Returns:
            FirestoreAdminTransport: The transport used by the client instance.
        """
        return self._transport

    @staticmethod
    def collection_group_path(project: str, database: str, collection: str,) -> str:
        """Return a fully-qualified collection_group string."""
        return "projects/{project}/databases/{database}/collectionGroups/{collection}".format(
            project=project, database=database, collection=collection,
        )

    @staticmethod
    def parse_collection_group_path(path: str) -> Dict[str, str]:
        """Parse a collection_group path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/databases/(?P<database>.+?)/collectionGroups/(?P<collection>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def database_path(project: str, database: str,) -> str:
        """Return a fully-qualified database string."""
        return "projects/{project}/databases/{database}".format(
            project=project, database=database,
        )

    @staticmethod
    def parse_database_path(path: str) -> Dict[str, str]:
        """Parse a database path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/databases/(?P<database>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def field_path(project: str, database: str, collection: str, field: str,) -> str:
        """Return a fully-qualified field string."""
        return "projects/{project}/databases/{database}/collectionGroups/{collection}/fields/{field}".format(
            project=project, database=database, collection=collection, field=field,
        )

    @staticmethod
    def parse_field_path(path: str) -> Dict[str, str]:
        """Parse a field path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/databases/(?P<database>.+?)/collectionGroups/(?P<collection>.+?)/fields/(?P<field>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def index_path(project: str, database: str, collection: str, index: str,) -> str:
        """Return a fully-qualified index string."""
        return "projects/{project}/databases/{database}/collectionGroups/{collection}/indexes/{index}".format(
            project=project, database=database, collection=collection, index=index,
        )

    @staticmethod
    def parse_index_path(path: str) -> Dict[str, str]:
        """Parse a index path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/databases/(?P<database>.+?)/collectionGroups/(?P<collection>.+?)/indexes/(?P<index>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Return a fully-qualified billing_account string."""
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
        """Return a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Return a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Return a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Return a fully-qualified location string."""
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
        credentials: Optional[credentials.Credentials] = None,
        transport: Union[str, FirestoreAdminTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the firestore admin client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.FirestoreAdminTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (client_options_lib.ClientOptions): Custom options for the
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

        ssl_credentials = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                import grpc  # type: ignore

                cert, key = client_options.client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
                is_mtls = True
            else:
                creds = SslCredentials()
                is_mtls = creds.is_mtls
                ssl_credentials = creds.ssl_credentials if is_mtls else None

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
                api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT if is_mtls else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, FirestoreAdminTransport):
            # transport is a FirestoreAdminTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                ssl_channel_credentials=ssl_credentials,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def create_index(
        self,
        request: firestore_admin.CreateIndexRequest = None,
        *,
        parent: str = None,
        index: gfa_index.Index = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Creates a composite index. This returns a
        [google.longrunning.Operation][google.longrunning.Operation]
        which may be used to track the status of the creation. The
        metadata for the operation will be the type
        [IndexOperationMetadata][google.firestore.admin.v1.IndexOperationMetadata].

        Args:
            request (:class:`~.firestore_admin.CreateIndexRequest`):
                The request object. The request for
                [FirestoreAdmin.CreateIndex][google.firestore.admin.v1.FirestoreAdmin.CreateIndex].
            parent (:class:`str`):
                Required. A parent name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            index (:class:`~.gfa_index.Index`):
                Required. The composite index to
                create.
                This corresponds to the ``index`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.ga_operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.gfa_index.Index``: Cloud Firestore indexes
                enable simple and complex queries against documents in a
                database.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, index])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a firestore_admin.CreateIndexRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, firestore_admin.CreateIndexRequest):
            request = firestore_admin.CreateIndexRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if index is not None:
                request.index = index

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_index]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = ga_operation.from_gapic(
            response,
            self._transport.operations_client,
            gfa_index.Index,
            metadata_type=gfa_operation.IndexOperationMetadata,
        )

        # Done; return the response.
        return response

    def list_indexes(
        self,
        request: firestore_admin.ListIndexesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListIndexesPager:
        r"""Lists composite indexes.

        Args:
            request (:class:`~.firestore_admin.ListIndexesRequest`):
                The request object. The request for
                [FirestoreAdmin.ListIndexes][google.firestore.admin.v1.FirestoreAdmin.ListIndexes].
            parent (:class:`str`):
                Required. A parent name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListIndexesPager:
                The response for
                [FirestoreAdmin.ListIndexes][google.firestore.admin.v1.FirestoreAdmin.ListIndexes].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a firestore_admin.ListIndexesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, firestore_admin.ListIndexesRequest):
            request = firestore_admin.ListIndexesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_indexes]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListIndexesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_index(
        self,
        request: firestore_admin.GetIndexRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> index.Index:
        r"""Gets a composite index.

        Args:
            request (:class:`~.firestore_admin.GetIndexRequest`):
                The request object. The request for
                [FirestoreAdmin.GetIndex][google.firestore.admin.v1.FirestoreAdmin.GetIndex].
            name (:class:`str`):
                Required. A name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/indexes/{index_id}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.index.Index:
                Cloud Firestore indexes enable simple
                and complex queries against documents in
                a database.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a firestore_admin.GetIndexRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, firestore_admin.GetIndexRequest):
            request = firestore_admin.GetIndexRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_index]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_index(
        self,
        request: firestore_admin.DeleteIndexRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a composite index.

        Args:
            request (:class:`~.firestore_admin.DeleteIndexRequest`):
                The request object. The request for
                [FirestoreAdmin.DeleteIndex][google.firestore.admin.v1.FirestoreAdmin.DeleteIndex].
            name (:class:`str`):
                Required. A name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/indexes/{index_id}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a firestore_admin.DeleteIndexRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, firestore_admin.DeleteIndexRequest):
            request = firestore_admin.DeleteIndexRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_index]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def get_field(
        self,
        request: firestore_admin.GetFieldRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> field.Field:
        r"""Gets the metadata and configuration for a Field.

        Args:
            request (:class:`~.firestore_admin.GetFieldRequest`):
                The request object. The request for
                [FirestoreAdmin.GetField][google.firestore.admin.v1.FirestoreAdmin.GetField].
            name (:class:`str`):
                Required. A name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/fields/{field_id}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.field.Field:
                Represents a single field in the
                database.
                Fields are grouped by their "Collection
                Group", which represent all collections
                in the database with the same id.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a firestore_admin.GetFieldRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, firestore_admin.GetFieldRequest):
            request = firestore_admin.GetFieldRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_field]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_field(
        self,
        request: firestore_admin.UpdateFieldRequest = None,
        *,
        field: gfa_field.Field = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Updates a field configuration. Currently, field updates apply
        only to single field index configuration. However, calls to
        [FirestoreAdmin.UpdateField][google.firestore.admin.v1.FirestoreAdmin.UpdateField]
        should provide a field mask to avoid changing any configuration
        that the caller isn't aware of. The field mask should be
        specified as: ``{ paths: "index_config" }``.

        This call returns a
        [google.longrunning.Operation][google.longrunning.Operation]
        which may be used to track the status of the field update. The
        metadata for the operation will be the type
        [FieldOperationMetadata][google.firestore.admin.v1.FieldOperationMetadata].

        To configure the default field settings for the database, use
        the special ``Field`` with resource name:
        ``projects/{project_id}/databases/{database_id}/collectionGroups/__default__/fields/*``.

        Args:
            request (:class:`~.firestore_admin.UpdateFieldRequest`):
                The request object. The request for
                [FirestoreAdmin.UpdateField][google.firestore.admin.v1.FirestoreAdmin.UpdateField].
            field (:class:`~.gfa_field.Field`):
                Required. The field to be updated.
                This corresponds to the ``field`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.ga_operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.gfa_field.Field``: Represents a single field
                in the database.

                Fields are grouped by their "Collection Group", which
                represent all collections in the database with the same
                id.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([field])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a firestore_admin.UpdateFieldRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, firestore_admin.UpdateFieldRequest):
            request = firestore_admin.UpdateFieldRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if field is not None:
                request.field = field

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_field]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("field.name", request.field.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = ga_operation.from_gapic(
            response,
            self._transport.operations_client,
            gfa_field.Field,
            metadata_type=gfa_operation.FieldOperationMetadata,
        )

        # Done; return the response.
        return response

    def list_fields(
        self,
        request: firestore_admin.ListFieldsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListFieldsPager:
        r"""Lists the field configuration and metadata for this database.

        Currently,
        [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields]
        only supports listing fields that have been explicitly
        overridden. To issue this query, call
        [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields]
        with the filter set to ``indexConfig.usesAncestorConfig:false``.

        Args:
            request (:class:`~.firestore_admin.ListFieldsRequest`):
                The request object. The request for
                [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields].
            parent (:class:`str`):
                Required. A parent name of the form
                ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListFieldsPager:
                The response for
                [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a firestore_admin.ListFieldsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, firestore_admin.ListFieldsRequest):
            request = firestore_admin.ListFieldsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_fields]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListFieldsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def export_documents(
        self,
        request: firestore_admin.ExportDocumentsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Exports a copy of all or a subset of documents from
        Google Cloud Firestore to another storage system, such
        as Google Cloud Storage. Recent updates to documents may
        not be reflected in the export. The export occurs in the
        background and its progress can be monitored and managed
        via the Operation resource that is created. The output
        of an export may only be used once the associated
        operation is done. If an export operation is cancelled
        before completion it may leave partial data behind in
        Google Cloud Storage.

        Args:
            request (:class:`~.firestore_admin.ExportDocumentsRequest`):
                The request object. The request for
                [FirestoreAdmin.ExportDocuments][google.firestore.admin.v1.FirestoreAdmin.ExportDocuments].
            name (:class:`str`):
                Required. Database to export. Should be of the form:
                ``projects/{project_id}/databases/{database_id}``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.ga_operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.gfa_operation.ExportDocumentsResponse``:
                Returned in the
                [google.longrunning.Operation][google.longrunning.Operation]
                response field.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a firestore_admin.ExportDocumentsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, firestore_admin.ExportDocumentsRequest):
            request = firestore_admin.ExportDocumentsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.export_documents]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = ga_operation.from_gapic(
            response,
            self._transport.operations_client,
            gfa_operation.ExportDocumentsResponse,
            metadata_type=gfa_operation.ExportDocumentsMetadata,
        )

        # Done; return the response.
        return response

    def import_documents(
        self,
        request: firestore_admin.ImportDocumentsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_operation.Operation:
        r"""Imports documents into Google Cloud Firestore.
        Existing documents with the same name are overwritten.
        The import occurs in the background and its progress can
        be monitored and managed via the Operation resource that
        is created. If an ImportDocuments operation is
        cancelled, it is possible that a subset of the data has
        already been imported to Cloud Firestore.

        Args:
            request (:class:`~.firestore_admin.ImportDocumentsRequest`):
                The request object. The request for
                [FirestoreAdmin.ImportDocuments][google.firestore.admin.v1.FirestoreAdmin.ImportDocuments].
            name (:class:`str`):
                Required. Database to import into. Should be of the
                form: ``projects/{project_id}/databases/{database_id}``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.ga_operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a firestore_admin.ImportDocumentsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, firestore_admin.ImportDocumentsRequest):
            request = firestore_admin.ImportDocumentsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.import_documents]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = ga_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty.Empty,
            metadata_type=gfa_operation.ImportDocumentsMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-firestore-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("FirestoreAdminClient",)
