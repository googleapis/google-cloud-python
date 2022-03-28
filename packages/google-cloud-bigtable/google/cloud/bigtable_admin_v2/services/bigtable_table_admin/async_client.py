# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.bigtable_admin_v2.services.bigtable_table_admin import pagers
from google.cloud.bigtable_admin_v2.types import bigtable_table_admin
from google.cloud.bigtable_admin_v2.types import table
from google.cloud.bigtable_admin_v2.types import table as gba_table
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import BigtableTableAdminTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import BigtableTableAdminGrpcAsyncIOTransport
from .client import BigtableTableAdminClient


class BigtableTableAdminAsyncClient:
    """Service for creating, configuring, and deleting Cloud
    Bigtable tables.

    Provides access to the table schemas only, not the data stored
    within the tables.
    """

    _client: BigtableTableAdminClient

    DEFAULT_ENDPOINT = BigtableTableAdminClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = BigtableTableAdminClient.DEFAULT_MTLS_ENDPOINT

    backup_path = staticmethod(BigtableTableAdminClient.backup_path)
    parse_backup_path = staticmethod(BigtableTableAdminClient.parse_backup_path)
    cluster_path = staticmethod(BigtableTableAdminClient.cluster_path)
    parse_cluster_path = staticmethod(BigtableTableAdminClient.parse_cluster_path)
    crypto_key_version_path = staticmethod(
        BigtableTableAdminClient.crypto_key_version_path
    )
    parse_crypto_key_version_path = staticmethod(
        BigtableTableAdminClient.parse_crypto_key_version_path
    )
    instance_path = staticmethod(BigtableTableAdminClient.instance_path)
    parse_instance_path = staticmethod(BigtableTableAdminClient.parse_instance_path)
    snapshot_path = staticmethod(BigtableTableAdminClient.snapshot_path)
    parse_snapshot_path = staticmethod(BigtableTableAdminClient.parse_snapshot_path)
    table_path = staticmethod(BigtableTableAdminClient.table_path)
    parse_table_path = staticmethod(BigtableTableAdminClient.parse_table_path)
    common_billing_account_path = staticmethod(
        BigtableTableAdminClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        BigtableTableAdminClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(BigtableTableAdminClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        BigtableTableAdminClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        BigtableTableAdminClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        BigtableTableAdminClient.parse_common_organization_path
    )
    common_project_path = staticmethod(BigtableTableAdminClient.common_project_path)
    parse_common_project_path = staticmethod(
        BigtableTableAdminClient.parse_common_project_path
    )
    common_location_path = staticmethod(BigtableTableAdminClient.common_location_path)
    parse_common_location_path = staticmethod(
        BigtableTableAdminClient.parse_common_location_path
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
            BigtableTableAdminAsyncClient: The constructed client.
        """
        return BigtableTableAdminClient.from_service_account_info.__func__(BigtableTableAdminAsyncClient, info, *args, **kwargs)  # type: ignore

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
            BigtableTableAdminAsyncClient: The constructed client.
        """
        return BigtableTableAdminClient.from_service_account_file.__func__(BigtableTableAdminAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return BigtableTableAdminClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> BigtableTableAdminTransport:
        """Returns the transport used by the client instance.

        Returns:
            BigtableTableAdminTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(BigtableTableAdminClient).get_transport_class,
        type(BigtableTableAdminClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, BigtableTableAdminTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the bigtable table admin client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.BigtableTableAdminTransport]): The
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
        self._client = BigtableTableAdminClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_table(
        self,
        request: Union[bigtable_table_admin.CreateTableRequest, dict] = None,
        *,
        parent: str = None,
        table_id: str = None,
        table: gba_table.Table = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gba_table.Table:
        r"""Creates a new table in the specified instance.
        The table can be created with a full set of initial
        column families, specified in the request.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.CreateTableRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.CreateTable][google.bigtable.admin.v2.BigtableTableAdmin.CreateTable]
            parent (:class:`str`):
                Required. The unique name of the instance in which to
                create the table. Values are of the form
                ``projects/{project}/instances/{instance}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            table_id (:class:`str`):
                Required. The name by which the new table should be
                referred to within the parent instance, e.g., ``foobar``
                rather than ``{parent}/tables/foobar``. Maximum 50
                characters.

                This corresponds to the ``table_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            table (:class:`google.cloud.bigtable_admin_v2.types.Table`):
                Required. The Table to create.
                This corresponds to the ``table`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.Table:
                A collection of user data indexed by
                row, column, and timestamp. Each table
                is served using the resources of its
                parent cluster.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, table_id, table])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.CreateTableRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if table_id is not None:
            request.table_id = table_id
        if table is not None:
            request.table = table

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_table,
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_table_from_snapshot(
        self,
        request: Union[
            bigtable_table_admin.CreateTableFromSnapshotRequest, dict
        ] = None,
        *,
        parent: str = None,
        table_id: str = None,
        source_snapshot: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new table from the specified snapshot. The
        target table must not exist. The snapshot and the table
        must be in the same instance.
        Note: This is a private alpha release of Cloud Bigtable
        snapshots. This feature is not currently available to
        most Cloud Bigtable customers. This feature might be
        changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any
        SLA or deprecation policy.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.CreateTableFromSnapshotRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.CreateTableFromSnapshot][google.bigtable.admin.v2.BigtableTableAdmin.CreateTableFromSnapshot]
                Note: This is a private alpha release of Cloud Bigtable
                snapshots. This feature is not currently available to
                most Cloud Bigtable customers. This feature might be
                changed in backward-incompatible ways and is not
                recommended for production use. It is not subject to any
                SLA or deprecation policy.
            parent (:class:`str`):
                Required. The unique name of the instance in which to
                create the table. Values are of the form
                ``projects/{project}/instances/{instance}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            table_id (:class:`str`):
                Required. The name by which the new table should be
                referred to within the parent instance, e.g., ``foobar``
                rather than ``{parent}/tables/foobar``.

                This corresponds to the ``table_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source_snapshot (:class:`str`):
                Required. The unique name of the snapshot from which to
                restore the table. The snapshot and the table must be in
                the same instance. Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/{snapshot}``.

                This corresponds to the ``source_snapshot`` field
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

                The result type for the operation will be :class:`google.cloud.bigtable_admin_v2.types.Table` A collection of user data indexed by row, column, and timestamp.
                   Each table is served using the resources of its
                   parent cluster.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, table_id, source_snapshot])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.CreateTableFromSnapshotRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if table_id is not None:
            request.table_id = table_id
        if source_snapshot is not None:
            request.source_snapshot = source_snapshot

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_table_from_snapshot,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            table.Table,
            metadata_type=bigtable_table_admin.CreateTableFromSnapshotMetadata,
        )

        # Done; return the response.
        return response

    async def list_tables(
        self,
        request: Union[bigtable_table_admin.ListTablesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTablesAsyncPager:
        r"""Lists all tables served from a specified instance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.ListTablesRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.ListTables][google.bigtable.admin.v2.BigtableTableAdmin.ListTables]
            parent (:class:`str`):
                Required. The unique name of the instance for which
                tables should be listed. Values are of the form
                ``projects/{project}/instances/{instance}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.services.bigtable_table_admin.pagers.ListTablesAsyncPager:
                Response message for
                   [google.bigtable.admin.v2.BigtableTableAdmin.ListTables][google.bigtable.admin.v2.BigtableTableAdmin.ListTables]

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.ListTablesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_tables,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTablesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_table(
        self,
        request: Union[bigtable_table_admin.GetTableRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> table.Table:
        r"""Gets metadata information about the specified table.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.GetTableRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.GetTable][google.bigtable.admin.v2.BigtableTableAdmin.GetTable]
            name (:class:`str`):
                Required. The unique name of the requested table. Values
                are of the form
                ``projects/{project}/instances/{instance}/tables/{table}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.Table:
                A collection of user data indexed by
                row, column, and timestamp. Each table
                is served using the resources of its
                parent cluster.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.GetTableRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_table,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_table(
        self,
        request: Union[bigtable_table_admin.DeleteTableRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Permanently deletes a specified table and all of its
        data.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.DeleteTableRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.DeleteTable][google.bigtable.admin.v2.BigtableTableAdmin.DeleteTable]
            name (:class:`str`):
                Required. The unique name of the table to be deleted.
                Values are of the form
                ``projects/{project}/instances/{instance}/tables/{table}``.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.DeleteTableRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_table,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def modify_column_families(
        self,
        request: Union[bigtable_table_admin.ModifyColumnFamiliesRequest, dict] = None,
        *,
        name: str = None,
        modifications: Sequence[
            bigtable_table_admin.ModifyColumnFamiliesRequest.Modification
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> table.Table:
        r"""Performs a series of column family modifications on
        the specified table. Either all or none of the
        modifications will occur before this method returns, but
        data requests received prior to that point may see a
        table where only some modifications have taken effect.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.ModifyColumnFamiliesRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.ModifyColumnFamilies][google.bigtable.admin.v2.BigtableTableAdmin.ModifyColumnFamilies]
            name (:class:`str`):
                Required. The unique name of the table whose families
                should be modified. Values are of the form
                ``projects/{project}/instances/{instance}/tables/{table}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            modifications (:class:`Sequence[google.cloud.bigtable_admin_v2.types.ModifyColumnFamiliesRequest.Modification]`):
                Required. Modifications to be
                atomically applied to the specified
                table's families. Entries are applied in
                order, meaning that earlier
                modifications can be masked by later
                ones (in the case of repeated updates to
                the same family, for example).

                This corresponds to the ``modifications`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.Table:
                A collection of user data indexed by
                row, column, and timestamp. Each table
                is served using the resources of its
                parent cluster.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, modifications])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.ModifyColumnFamiliesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if modifications:
            request.modifications.extend(modifications)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.modify_column_families,
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def drop_row_range(
        self,
        request: Union[bigtable_table_admin.DropRowRangeRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Permanently drop/delete a row range from a specified
        table. The request can specify whether to delete all
        rows in a table, or only those that match a particular
        prefix.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.DropRowRangeRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.DropRowRange][google.bigtable.admin.v2.BigtableTableAdmin.DropRowRange]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = bigtable_table_admin.DropRowRangeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.drop_row_range,
            default_timeout=3600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def generate_consistency_token(
        self,
        request: Union[
            bigtable_table_admin.GenerateConsistencyTokenRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable_table_admin.GenerateConsistencyTokenResponse:
        r"""Generates a consistency token for a Table, which can
        be used in CheckConsistency to check whether mutations
        to the table that finished before this call started have
        been replicated. The tokens will be available for 90
        days.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.GenerateConsistencyTokenRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken][google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken]
            name (:class:`str`):
                Required. The unique name of the Table for which to
                create a consistency token. Values are of the form
                ``projects/{project}/instances/{instance}/tables/{table}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.GenerateConsistencyTokenResponse:
                Response message for
                   [google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken][google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken]

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.GenerateConsistencyTokenRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.generate_consistency_token,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def check_consistency(
        self,
        request: Union[bigtable_table_admin.CheckConsistencyRequest, dict] = None,
        *,
        name: str = None,
        consistency_token: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable_table_admin.CheckConsistencyResponse:
        r"""Checks replication consistency based on a consistency
        token, that is, if replication has caught up based on
        the conditions specified in the token and the check
        request.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.CheckConsistencyRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency][google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency]
            name (:class:`str`):
                Required. The unique name of the Table for which to
                check replication consistency. Values are of the form
                ``projects/{project}/instances/{instance}/tables/{table}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            consistency_token (:class:`str`):
                Required. The token created using
                GenerateConsistencyToken for the Table.

                This corresponds to the ``consistency_token`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.CheckConsistencyResponse:
                Response message for
                   [google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency][google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency]

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, consistency_token])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.CheckConsistencyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if consistency_token is not None:
            request.consistency_token = consistency_token

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.check_consistency,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def snapshot_table(
        self,
        request: Union[bigtable_table_admin.SnapshotTableRequest, dict] = None,
        *,
        name: str = None,
        cluster: str = None,
        snapshot_id: str = None,
        description: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new snapshot in the specified cluster from
        the specified source table. The cluster and the table
        must be in the same instance.
        Note: This is a private alpha release of Cloud Bigtable
        snapshots. This feature is not currently available to
        most Cloud Bigtable customers. This feature might be
        changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any
        SLA or deprecation policy.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.SnapshotTableRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.SnapshotTable][google.bigtable.admin.v2.BigtableTableAdmin.SnapshotTable]
                Note: This is a private alpha release of Cloud Bigtable
                snapshots. This feature is not currently available to
                most Cloud Bigtable customers. This feature might be
                changed in backward-incompatible ways and is not
                recommended for production use. It is not subject to any
                SLA or deprecation policy.
            name (:class:`str`):
                Required. The unique name of the table to have the
                snapshot taken. Values are of the form
                ``projects/{project}/instances/{instance}/tables/{table}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster (:class:`str`):
                Required. The name of the cluster where the snapshot
                will be created in. Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}``.

                This corresponds to the ``cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            snapshot_id (:class:`str`):
                Required. The ID by which the new snapshot should be
                referred to within the parent cluster, e.g.,
                ``mysnapshot`` of the form:
                ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*`` rather than
                ``projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/mysnapshot``.

                This corresponds to the ``snapshot_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            description (:class:`str`):
                Description of the snapshot.
                This corresponds to the ``description`` field
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

                The result type for the operation will be :class:`google.cloud.bigtable_admin_v2.types.Snapshot` A snapshot of a table at a particular time. A snapshot can be used as a
                   checkpoint for data restoration or a data source for
                   a new table.

                   Note: This is a private alpha release of Cloud
                   Bigtable snapshots. This feature is not currently
                   available to most Cloud Bigtable customers. This
                   feature might be changed in backward-incompatible
                   ways and is not recommended for production use. It is
                   not subject to any SLA or deprecation policy.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, cluster, snapshot_id, description])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.SnapshotTableRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if cluster is not None:
            request.cluster = cluster
        if snapshot_id is not None:
            request.snapshot_id = snapshot_id
        if description is not None:
            request.description = description

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.snapshot_table,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            table.Snapshot,
            metadata_type=bigtable_table_admin.SnapshotTableMetadata,
        )

        # Done; return the response.
        return response

    async def get_snapshot(
        self,
        request: Union[bigtable_table_admin.GetSnapshotRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> table.Snapshot:
        r"""Gets metadata information about the specified
        snapshot.
        Note: This is a private alpha release of Cloud Bigtable
        snapshots. This feature is not currently available to
        most Cloud Bigtable customers. This feature might be
        changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any
        SLA or deprecation policy.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.GetSnapshotRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.GetSnapshot][google.bigtable.admin.v2.BigtableTableAdmin.GetSnapshot]
                Note: This is a private alpha release of Cloud Bigtable
                snapshots. This feature is not currently available to
                most Cloud Bigtable customers. This feature might be
                changed in backward-incompatible ways and is not
                recommended for production use. It is not subject to any
                SLA or deprecation policy.
            name (:class:`str`):
                Required. The unique name of the requested snapshot.
                Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/{snapshot}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.Snapshot:
                A snapshot of a table at a particular
                time. A snapshot can be used as a
                checkpoint for data restoration or a
                data source for a new table.
                Note: This is a private alpha release of
                Cloud Bigtable snapshots. This feature
                is not currently available to most Cloud
                Bigtable customers. This feature might
                be changed in backward-incompatible ways
                and is not recommended for production
                use. It is not subject to any SLA or
                deprecation policy.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.GetSnapshotRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_snapshot,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_snapshots(
        self,
        request: Union[bigtable_table_admin.ListSnapshotsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSnapshotsAsyncPager:
        r"""Lists all snapshots associated with the specified
        cluster.
        Note: This is a private alpha release of Cloud Bigtable
        snapshots. This feature is not currently available to
        most Cloud Bigtable customers. This feature might be
        changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any
        SLA or deprecation policy.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.ListSnapshotsRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots][google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots]
                Note: This is a private alpha release of Cloud Bigtable
                snapshots. This feature is not currently available to
                most Cloud Bigtable customers. This feature might be
                changed in backward-incompatible ways and is not
                recommended for production use. It is not subject to any
                SLA or deprecation policy.
            parent (:class:`str`):
                Required. The unique name of the cluster for which
                snapshots should be listed. Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}``.
                Use ``{cluster} = '-'`` to list snapshots for all
                clusters in an instance, e.g.,
                ``projects/{project}/instances/{instance}/clusters/-``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.services.bigtable_table_admin.pagers.ListSnapshotsAsyncPager:
                Response message for
                   [google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots][google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots]

                   Note: This is a private alpha release of Cloud
                   Bigtable snapshots. This feature is not currently
                   available to most Cloud Bigtable customers. This
                   feature might be changed in backward-incompatible
                   ways and is not recommended for production use. It is
                   not subject to any SLA or deprecation policy.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.ListSnapshotsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_snapshots,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListSnapshotsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_snapshot(
        self,
        request: Union[bigtable_table_admin.DeleteSnapshotRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Permanently deletes the specified snapshot.
        Note: This is a private alpha release of Cloud Bigtable
        snapshots. This feature is not currently available to
        most Cloud Bigtable customers. This feature might be
        changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any
        SLA or deprecation policy.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.DeleteSnapshotRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.DeleteSnapshot][google.bigtable.admin.v2.BigtableTableAdmin.DeleteSnapshot]
                Note: This is a private alpha release of Cloud Bigtable
                snapshots. This feature is not currently available to
                most Cloud Bigtable customers. This feature might be
                changed in backward-incompatible ways and is not
                recommended for production use. It is not subject to any
                SLA or deprecation policy.
            name (:class:`str`):
                Required. The unique name of the snapshot to be deleted.
                Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/{snapshot}``.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.DeleteSnapshotRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_snapshot,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def create_backup(
        self,
        request: Union[bigtable_table_admin.CreateBackupRequest, dict] = None,
        *,
        parent: str = None,
        backup_id: str = None,
        backup: table.Backup = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Starts creating a new Cloud Bigtable Backup. The returned backup
        [long-running operation][google.longrunning.Operation] can be
        used to track creation of the backup. The
        [metadata][google.longrunning.Operation.metadata] field type is
        [CreateBackupMetadata][google.bigtable.admin.v2.CreateBackupMetadata].
        The [response][google.longrunning.Operation.response] field type
        is [Backup][google.bigtable.admin.v2.Backup], if successful.
        Cancelling the returned operation will stop the creation and
        delete the backup.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.CreateBackupRequest, dict]):
                The request object. The request for
                [CreateBackup][google.bigtable.admin.v2.BigtableTableAdmin.CreateBackup].
            parent (:class:`str`):
                Required. This must be one of the clusters in the
                instance in which this table is located. The backup will
                be stored in this cluster. Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_id (:class:`str`):
                Required. The id of the backup to be created. The
                ``backup_id`` along with the parent ``parent`` are
                combined as {parent}/backups/{backup_id} to create the
                full backup name, of the form:
                ``projects/{project}/instances/{instance}/clusters/{cluster}/backups/{backup_id}``.
                This string must be between 1 and 50 characters in
                length and match the regex [*a-zA-Z0-9][-*.a-zA-Z0-9]*.

                This corresponds to the ``backup_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup (:class:`google.cloud.bigtable_admin_v2.types.Backup`):
                Required. The backup to create.
                This corresponds to the ``backup`` field
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

                The result type for the operation will be
                :class:`google.cloud.bigtable_admin_v2.types.Backup` A
                backup of a Cloud Bigtable table.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, backup_id, backup])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.CreateBackupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if backup_id is not None:
            request.backup_id = backup_id
        if backup is not None:
            request.backup = backup

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_backup,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            table.Backup,
            metadata_type=bigtable_table_admin.CreateBackupMetadata,
        )

        # Done; return the response.
        return response

    async def get_backup(
        self,
        request: Union[bigtable_table_admin.GetBackupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> table.Backup:
        r"""Gets metadata on a pending or completed Cloud
        Bigtable Backup.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.GetBackupRequest, dict]):
                The request object. The request for
                [GetBackup][google.bigtable.admin.v2.BigtableTableAdmin.GetBackup].
            name (:class:`str`):
                Required. Name of the backup. Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}/backups/{backup}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.Backup:
                A backup of a Cloud Bigtable table.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.GetBackupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_backup,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_backup(
        self,
        request: Union[bigtable_table_admin.UpdateBackupRequest, dict] = None,
        *,
        backup: table.Backup = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> table.Backup:
        r"""Updates a pending or completed Cloud Bigtable Backup.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.UpdateBackupRequest, dict]):
                The request object. The request for
                [UpdateBackup][google.bigtable.admin.v2.BigtableTableAdmin.UpdateBackup].
            backup (:class:`google.cloud.bigtable_admin_v2.types.Backup`):
                Required. The backup to update. ``backup.name``, and the
                fields to be updated as specified by ``update_mask`` are
                required. Other fields are ignored. Update is only
                supported for the following fields:

                -  ``backup.expire_time``.

                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. A mask specifying which fields (e.g.
                ``expire_time``) in the Backup resource should be
                updated. This mask is relative to the Backup resource,
                not to the request message. The field mask must always
                be specified; this prevents any future fields from being
                erased accidentally by clients that do not know about
                them.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.Backup:
                A backup of a Cloud Bigtable table.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([backup, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.UpdateBackupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if backup is not None:
            request.backup = backup
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_backup,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("backup.name", request.backup.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_backup(
        self,
        request: Union[bigtable_table_admin.DeleteBackupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a pending or completed Cloud Bigtable backup.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.DeleteBackupRequest, dict]):
                The request object. The request for
                [DeleteBackup][google.bigtable.admin.v2.BigtableTableAdmin.DeleteBackup].
            name (:class:`str`):
                Required. Name of the backup to delete. Values are of
                the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}/backups/{backup}``.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.DeleteBackupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_backup,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_backups(
        self,
        request: Union[bigtable_table_admin.ListBackupsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBackupsAsyncPager:
        r"""Lists Cloud Bigtable backups. Returns both completed
        and pending backups.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.ListBackupsRequest, dict]):
                The request object. The request for
                [ListBackups][google.bigtable.admin.v2.BigtableTableAdmin.ListBackups].
            parent (:class:`str`):
                Required. The cluster to list backups from. Values are
                of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}``.
                Use ``{cluster} = '-'`` to list backups for all clusters
                in an instance, e.g.,
                ``projects/{project}/instances/{instance}/clusters/-``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.services.bigtable_table_admin.pagers.ListBackupsAsyncPager:
                The response for
                [ListBackups][google.bigtable.admin.v2.BigtableTableAdmin.ListBackups].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_table_admin.ListBackupsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_backups,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListBackupsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def restore_table(
        self,
        request: Union[bigtable_table_admin.RestoreTableRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Create a new table by restoring from a completed backup. The new
        table must be in the same project as the instance containing the
        backup. The returned table [long-running
        operation][google.longrunning.Operation] can be used to track
        the progress of the operation, and to cancel it. The
        [metadata][google.longrunning.Operation.metadata] field type is
        [RestoreTableMetadata][google.bigtable.admin.RestoreTableMetadata].
        The [response][google.longrunning.Operation.response] type is
        [Table][google.bigtable.admin.v2.Table], if successful.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.RestoreTableRequest, dict]):
                The request object. The request for
                [RestoreTable][google.bigtable.admin.v2.BigtableTableAdmin.RestoreTable].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.bigtable_admin_v2.types.Table` A collection of user data indexed by row, column, and timestamp.
                   Each table is served using the resources of its
                   parent cluster.

        """
        # Create or coerce a protobuf request object.
        request = bigtable_table_admin.RestoreTableRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.restore_table,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            table.Table,
            metadata_type=bigtable_table_admin.RestoreTableMetadata,
        )

        # Done; return the response.
        return response

    async def get_iam_policy(
        self,
        request: Union[iam_policy_pb2.GetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy for a Table or Backup
        resource. Returns an empty policy if the resource exists
        but does not have a policy set.

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]):
                The request object. Request message for `GetIamPolicy`
                method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy. It is used to
                   specify access control policies for Cloud Platform
                   resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions (defined by IAM or configured by users).
                   A binding can optionally specify a condition, which
                   is a logic expression that further constrains the
                   role binding based on attributes about the request
                   and/or target resource.

                   **JSON Example**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": ["user:eve@example.com"],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ]

                      }

                   **YAML Example**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z')

                   For a description of IAM and its features, see the
                   [IAM developer's
                   guide](\ https://cloud.google.com/iam/docs).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy_pb2.GetIamPolicyRequest(
                resource=resource,
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_iam_policy,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def set_iam_policy(
        self,
        request: Union[iam_policy_pb2.SetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the access control policy on a Table or Backup
        resource. Replaces any existing policy.

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]):
                The request object. Request message for `SetIamPolicy`
                method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy. It is used to
                   specify access control policies for Cloud Platform
                   resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions (defined by IAM or configured by users).
                   A binding can optionally specify a condition, which
                   is a logic expression that further constrains the
                   role binding based on attributes about the request
                   and/or target resource.

                   **JSON Example**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": ["user:eve@example.com"],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ]

                      }

                   **YAML Example**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z')

                   For a description of IAM and its features, see the
                   [IAM developer's
                   guide](\ https://cloud.google.com/iam/docs).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy_pb2.SetIamPolicyRequest(
                resource=resource,
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_iam_policy,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def test_iam_permissions(
        self,
        request: Union[iam_policy_pb2.TestIamPermissionsRequest, dict] = None,
        *,
        resource: str = None,
        permissions: Sequence[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns permissions that the caller has on the
        specified Table or Backup resource.

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for
                `TestIamPermissions` method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (:class:`Sequence[str]`):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, permissions])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            request = iam_policy_pb2.TestIamPermissionsRequest(
                resource=resource,
                permissions=permissions,
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.test_iam_permissions,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
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
            "google-cloud-bigtable-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BigtableTableAdminAsyncClient",)
