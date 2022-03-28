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
import os
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
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
from .transports.grpc import BigtableTableAdminGrpcTransport
from .transports.grpc_asyncio import BigtableTableAdminGrpcAsyncIOTransport


class BigtableTableAdminClientMeta(type):
    """Metaclass for the BigtableTableAdmin client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[BigtableTableAdminTransport]]
    _transport_registry["grpc"] = BigtableTableAdminGrpcTransport
    _transport_registry["grpc_asyncio"] = BigtableTableAdminGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: str = None,
    ) -> Type[BigtableTableAdminTransport]:
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


class BigtableTableAdminClient(metaclass=BigtableTableAdminClientMeta):
    """Service for creating, configuring, and deleting Cloud
    Bigtable tables.

    Provides access to the table schemas only, not the data stored
    within the tables.
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

    DEFAULT_ENDPOINT = "bigtableadmin.googleapis.com"
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
            BigtableTableAdminClient: The constructed client.
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
            BigtableTableAdminClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> BigtableTableAdminTransport:
        """Returns the transport used by the client instance.

        Returns:
            BigtableTableAdminTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def backup_path(
        project: str,
        instance: str,
        cluster: str,
        backup: str,
    ) -> str:
        """Returns a fully-qualified backup string."""
        return "projects/{project}/instances/{instance}/clusters/{cluster}/backups/{backup}".format(
            project=project,
            instance=instance,
            cluster=cluster,
            backup=backup,
        )

    @staticmethod
    def parse_backup_path(path: str) -> Dict[str, str]:
        """Parses a backup path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)/clusters/(?P<cluster>.+?)/backups/(?P<backup>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def cluster_path(
        project: str,
        instance: str,
        cluster: str,
    ) -> str:
        """Returns a fully-qualified cluster string."""
        return "projects/{project}/instances/{instance}/clusters/{cluster}".format(
            project=project,
            instance=instance,
            cluster=cluster,
        )

    @staticmethod
    def parse_cluster_path(path: str) -> Dict[str, str]:
        """Parses a cluster path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)/clusters/(?P<cluster>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def crypto_key_version_path(
        project: str,
        location: str,
        key_ring: str,
        crypto_key: str,
        crypto_key_version: str,
    ) -> str:
        """Returns a fully-qualified crypto_key_version string."""
        return "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}".format(
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key=crypto_key,
            crypto_key_version=crypto_key_version,
        )

    @staticmethod
    def parse_crypto_key_version_path(path: str) -> Dict[str, str]:
        """Parses a crypto_key_version path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/keyRings/(?P<key_ring>.+?)/cryptoKeys/(?P<crypto_key>.+?)/cryptoKeyVersions/(?P<crypto_key_version>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def instance_path(
        project: str,
        instance: str,
    ) -> str:
        """Returns a fully-qualified instance string."""
        return "projects/{project}/instances/{instance}".format(
            project=project,
            instance=instance,
        )

    @staticmethod
    def parse_instance_path(path: str) -> Dict[str, str]:
        """Parses a instance path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def snapshot_path(
        project: str,
        instance: str,
        cluster: str,
        snapshot: str,
    ) -> str:
        """Returns a fully-qualified snapshot string."""
        return "projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/{snapshot}".format(
            project=project,
            instance=instance,
            cluster=cluster,
            snapshot=snapshot,
        )

    @staticmethod
    def parse_snapshot_path(path: str) -> Dict[str, str]:
        """Parses a snapshot path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)/clusters/(?P<cluster>.+?)/snapshots/(?P<snapshot>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def table_path(
        project: str,
        instance: str,
        table: str,
    ) -> str:
        """Returns a fully-qualified table string."""
        return "projects/{project}/instances/{instance}/tables/{table}".format(
            project=project,
            instance=instance,
            table=table,
        )

    @staticmethod
    def parse_table_path(path: str) -> Dict[str, str]:
        """Parses a table path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)/tables/(?P<table>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
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
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
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
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, BigtableTableAdminTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the bigtable table admin client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, BigtableTableAdminTransport]): The
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

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, BigtableTableAdminTransport):
            # transport is a BigtableTableAdminTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
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
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

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

    def create_table(
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
            parent (str):
                Required. The unique name of the instance in which to
                create the table. Values are of the form
                ``projects/{project}/instances/{instance}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            table_id (str):
                Required. The name by which the new table should be
                referred to within the parent instance, e.g., ``foobar``
                rather than ``{parent}/tables/foobar``. Maximum 50
                characters.

                This corresponds to the ``table_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            table (google.cloud.bigtable_admin_v2.types.Table):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.CreateTableRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.CreateTableRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.create_table]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_table_from_snapshot(
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
    ) -> operation.Operation:
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
            parent (str):
                Required. The unique name of the instance in which to
                create the table. Values are of the form
                ``projects/{project}/instances/{instance}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            table_id (str):
                Required. The name by which the new table should be
                referred to within the parent instance, e.g., ``foobar``
                rather than ``{parent}/tables/foobar``.

                This corresponds to the ``table_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source_snapshot (str):
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
            google.api_core.operation.Operation:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.CreateTableFromSnapshotRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.CreateTableFromSnapshotRequest):
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
        rpc = self._transport._wrapped_methods[
            self._transport.create_table_from_snapshot
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            table.Table,
            metadata_type=bigtable_table_admin.CreateTableFromSnapshotMetadata,
        )

        # Done; return the response.
        return response

    def list_tables(
        self,
        request: Union[bigtable_table_admin.ListTablesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTablesPager:
        r"""Lists all tables served from a specified instance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.ListTablesRequest, dict]):
                The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.ListTables][google.bigtable.admin.v2.BigtableTableAdmin.ListTables]
            parent (str):
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
            google.cloud.bigtable_admin_v2.services.bigtable_table_admin.pagers.ListTablesPager:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.ListTablesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.ListTablesRequest):
            request = bigtable_table_admin.ListTablesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_tables]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTablesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_table(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.GetTableRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.GetTableRequest):
            request = bigtable_table_admin.GetTableRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_table]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_table(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.DeleteTableRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.DeleteTableRequest):
            request = bigtable_table_admin.DeleteTableRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_table]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def modify_column_families(
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
            name (str):
                Required. The unique name of the table whose families
                should be modified. Values are of the form
                ``projects/{project}/instances/{instance}/tables/{table}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            modifications (Sequence[google.cloud.bigtable_admin_v2.types.ModifyColumnFamiliesRequest.Modification]):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.ModifyColumnFamiliesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.ModifyColumnFamiliesRequest):
            request = bigtable_table_admin.ModifyColumnFamiliesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if modifications is not None:
                request.modifications = modifications

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.modify_column_families]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def drop_row_range(
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
        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.DropRowRangeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.DropRowRangeRequest):
            request = bigtable_table_admin.DropRowRangeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.drop_row_range]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def generate_consistency_token(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.GenerateConsistencyTokenRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, bigtable_table_admin.GenerateConsistencyTokenRequest
        ):
            request = bigtable_table_admin.GenerateConsistencyTokenRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.generate_consistency_token
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def check_consistency(
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
            name (str):
                Required. The unique name of the Table for which to
                check replication consistency. Values are of the form
                ``projects/{project}/instances/{instance}/tables/{table}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            consistency_token (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.CheckConsistencyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.CheckConsistencyRequest):
            request = bigtable_table_admin.CheckConsistencyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if consistency_token is not None:
                request.consistency_token = consistency_token

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.check_consistency]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def snapshot_table(
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
    ) -> operation.Operation:
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
            name (str):
                Required. The unique name of the table to have the
                snapshot taken. Values are of the form
                ``projects/{project}/instances/{instance}/tables/{table}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster (str):
                Required. The name of the cluster where the snapshot
                will be created in. Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}``.

                This corresponds to the ``cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            snapshot_id (str):
                Required. The ID by which the new snapshot should be
                referred to within the parent cluster, e.g.,
                ``mysnapshot`` of the form:
                ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*`` rather than
                ``projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/mysnapshot``.

                This corresponds to the ``snapshot_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            description (str):
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
            google.api_core.operation.Operation:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.SnapshotTableRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.SnapshotTableRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.snapshot_table]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            table.Snapshot,
            metadata_type=bigtable_table_admin.SnapshotTableMetadata,
        )

        # Done; return the response.
        return response

    def get_snapshot(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.GetSnapshotRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.GetSnapshotRequest):
            request = bigtable_table_admin.GetSnapshotRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_snapshot]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_snapshots(
        self,
        request: Union[bigtable_table_admin.ListSnapshotsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSnapshotsPager:
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
            parent (str):
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
            google.cloud.bigtable_admin_v2.services.bigtable_table_admin.pagers.ListSnapshotsPager:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.ListSnapshotsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.ListSnapshotsRequest):
            request = bigtable_table_admin.ListSnapshotsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_snapshots]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSnapshotsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_snapshot(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.DeleteSnapshotRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.DeleteSnapshotRequest):
            request = bigtable_table_admin.DeleteSnapshotRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_snapshot]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_backup(
        self,
        request: Union[bigtable_table_admin.CreateBackupRequest, dict] = None,
        *,
        parent: str = None,
        backup_id: str = None,
        backup: table.Backup = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
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
            parent (str):
                Required. This must be one of the clusters in the
                instance in which this table is located. The backup will
                be stored in this cluster. Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_id (str):
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
            backup (google.cloud.bigtable_admin_v2.types.Backup):
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
            google.api_core.operation.Operation:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.CreateBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.CreateBackupRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.create_backup]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            table.Backup,
            metadata_type=bigtable_table_admin.CreateBackupMetadata,
        )

        # Done; return the response.
        return response

    def get_backup(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.GetBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.GetBackupRequest):
            request = bigtable_table_admin.GetBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_backup]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_backup(
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
            backup (google.cloud.bigtable_admin_v2.types.Backup):
                Required. The backup to update. ``backup.name``, and the
                fields to be updated as specified by ``update_mask`` are
                required. Other fields are ignored. Update is only
                supported for the following fields:

                -  ``backup.expire_time``.

                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.UpdateBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.UpdateBackupRequest):
            request = bigtable_table_admin.UpdateBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if backup is not None:
                request.backup = backup
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_backup]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("backup.name", request.backup.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_backup(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.DeleteBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.DeleteBackupRequest):
            request = bigtable_table_admin.DeleteBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_backup]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_backups(
        self,
        request: Union[bigtable_table_admin.ListBackupsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBackupsPager:
        r"""Lists Cloud Bigtable backups. Returns both completed
        and pending backups.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.ListBackupsRequest, dict]):
                The request object. The request for
                [ListBackups][google.bigtable.admin.v2.BigtableTableAdmin.ListBackups].
            parent (str):
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
            google.cloud.bigtable_admin_v2.services.bigtable_table_admin.pagers.ListBackupsPager:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.ListBackupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.ListBackupsRequest):
            request = bigtable_table_admin.ListBackupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_backups]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBackupsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def restore_table(
        self,
        request: Union[bigtable_table_admin.RestoreTableRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.bigtable_admin_v2.types.Table` A collection of user data indexed by row, column, and timestamp.
                   Each table is served using the resources of its
                   parent cluster.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable_table_admin.RestoreTableRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable_table_admin.RestoreTableRequest):
            request = bigtable_table_admin.RestoreTableRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.restore_table]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            table.Table,
            metadata_type=bigtable_table_admin.RestoreTableMetadata,
        )

        # Done; return the response.
        return response

    def get_iam_policy(
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
            resource (str):
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

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.GetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_iam_policy(
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
            resource (str):
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

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.SetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def test_iam_permissions(
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
            resource (str):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (Sequence[str]):
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

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.TestIamPermissionsRequest()
            if resource is not None:
                request.resource = resource
            if permissions:
                request.permissions.extend(permissions)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
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
            "google-cloud-bigtable-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BigtableTableAdminClient",)
