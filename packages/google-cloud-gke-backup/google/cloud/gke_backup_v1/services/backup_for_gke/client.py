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
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union
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
from google.cloud.gke_backup_v1.services.backup_for_gke import pagers
from google.cloud.gke_backup_v1.types import backup
from google.cloud.gke_backup_v1.types import backup as gcg_backup
from google.cloud.gke_backup_v1.types import backup_plan
from google.cloud.gke_backup_v1.types import backup_plan as gcg_backup_plan
from google.cloud.gke_backup_v1.types import common
from google.cloud.gke_backup_v1.types import gkebackup
from google.cloud.gke_backup_v1.types import restore
from google.cloud.gke_backup_v1.types import restore as gcg_restore
from google.cloud.gke_backup_v1.types import restore_plan
from google.cloud.gke_backup_v1.types import restore_plan as gcg_restore_plan
from google.cloud.gke_backup_v1.types import volume
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import BackupForGKETransport, DEFAULT_CLIENT_INFO
from .transports.grpc import BackupForGKEGrpcTransport
from .transports.grpc_asyncio import BackupForGKEGrpcAsyncIOTransport


class BackupForGKEClientMeta(type):
    """Metaclass for the BackupForGKE client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[BackupForGKETransport]]
    _transport_registry["grpc"] = BackupForGKEGrpcTransport
    _transport_registry["grpc_asyncio"] = BackupForGKEGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: str = None,
    ) -> Type[BackupForGKETransport]:
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


class BackupForGKEClient(metaclass=BackupForGKEClientMeta):
    """BackupForGKE allows Kubernetes administrators to configure,
    execute, and manage backup and restore operations for their GKE
    clusters.
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

    DEFAULT_ENDPOINT = "gkebackup.googleapis.com"
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
            BackupForGKEClient: The constructed client.
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
            BackupForGKEClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> BackupForGKETransport:
        """Returns the transport used by the client instance.

        Returns:
            BackupForGKETransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def backup_path(
        project: str,
        location: str,
        backup_plan: str,
        backup: str,
    ) -> str:
        """Returns a fully-qualified backup string."""
        return "projects/{project}/locations/{location}/backupPlans/{backup_plan}/backups/{backup}".format(
            project=project,
            location=location,
            backup_plan=backup_plan,
            backup=backup,
        )

    @staticmethod
    def parse_backup_path(path: str) -> Dict[str, str]:
        """Parses a backup path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/backupPlans/(?P<backup_plan>.+?)/backups/(?P<backup>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def backup_plan_path(
        project: str,
        location: str,
        backup_plan: str,
    ) -> str:
        """Returns a fully-qualified backup_plan string."""
        return (
            "projects/{project}/locations/{location}/backupPlans/{backup_plan}".format(
                project=project,
                location=location,
                backup_plan=backup_plan,
            )
        )

    @staticmethod
    def parse_backup_plan_path(path: str) -> Dict[str, str]:
        """Parses a backup_plan path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/backupPlans/(?P<backup_plan>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def cluster_path(
        project: str,
        location: str,
        cluster: str,
    ) -> str:
        """Returns a fully-qualified cluster string."""
        return "projects/{project}/locations/{location}/clusters/{cluster}".format(
            project=project,
            location=location,
            cluster=cluster,
        )

    @staticmethod
    def parse_cluster_path(path: str) -> Dict[str, str]:
        """Parses a cluster path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/clusters/(?P<cluster>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def crypto_key_path(
        project: str,
        location: str,
        key_ring: str,
        crypto_key: str,
    ) -> str:
        """Returns a fully-qualified crypto_key string."""
        return "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key=crypto_key,
        )

    @staticmethod
    def parse_crypto_key_path(path: str) -> Dict[str, str]:
        """Parses a crypto_key path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/keyRings/(?P<key_ring>.+?)/cryptoKeys/(?P<crypto_key>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def restore_path(
        project: str,
        location: str,
        restore_plan: str,
        restore: str,
    ) -> str:
        """Returns a fully-qualified restore string."""
        return "projects/{project}/locations/{location}/restorePlans/{restore_plan}/restores/{restore}".format(
            project=project,
            location=location,
            restore_plan=restore_plan,
            restore=restore,
        )

    @staticmethod
    def parse_restore_path(path: str) -> Dict[str, str]:
        """Parses a restore path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/restorePlans/(?P<restore_plan>.+?)/restores/(?P<restore>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def restore_plan_path(
        project: str,
        location: str,
        restore_plan: str,
    ) -> str:
        """Returns a fully-qualified restore_plan string."""
        return "projects/{project}/locations/{location}/restorePlans/{restore_plan}".format(
            project=project,
            location=location,
            restore_plan=restore_plan,
        )

    @staticmethod
    def parse_restore_plan_path(path: str) -> Dict[str, str]:
        """Parses a restore_plan path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/restorePlans/(?P<restore_plan>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def volume_backup_path(
        project: str,
        location: str,
        backup_plan: str,
        backup: str,
        volume_backup: str,
    ) -> str:
        """Returns a fully-qualified volume_backup string."""
        return "projects/{project}/locations/{location}/backupPlans/{backup_plan}/backups/{backup}/volumeBackups/{volume_backup}".format(
            project=project,
            location=location,
            backup_plan=backup_plan,
            backup=backup,
            volume_backup=volume_backup,
        )

    @staticmethod
    def parse_volume_backup_path(path: str) -> Dict[str, str]:
        """Parses a volume_backup path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/backupPlans/(?P<backup_plan>.+?)/backups/(?P<backup>.+?)/volumeBackups/(?P<volume_backup>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def volume_restore_path(
        project: str,
        location: str,
        restore_plan: str,
        restore: str,
        volume_restore: str,
    ) -> str:
        """Returns a fully-qualified volume_restore string."""
        return "projects/{project}/locations/{location}/restorePlans/{restore_plan}/restores/{restore}/volumeRestores/{volume_restore}".format(
            project=project,
            location=location,
            restore_plan=restore_plan,
            restore=restore,
            volume_restore=volume_restore,
        )

    @staticmethod
    def parse_volume_restore_path(path: str) -> Dict[str, str]:
        """Parses a volume_restore path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/restorePlans/(?P<restore_plan>.+?)/restores/(?P<restore>.+?)/volumeRestores/(?P<volume_restore>.+?)$",
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
        transport: Union[str, BackupForGKETransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the backup for gke client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, BackupForGKETransport]): The
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
        if isinstance(transport, BackupForGKETransport):
            # transport is a BackupForGKETransport instance.
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
                api_audience=client_options.api_audience,
            )

    def create_backup_plan(
        self,
        request: Union[gkebackup.CreateBackupPlanRequest, dict] = None,
        *,
        parent: str = None,
        backup_plan: gcg_backup_plan.BackupPlan = None,
        backup_plan_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new BackupPlan in a given location.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_create_backup_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                backup_plan = gke_backup_v1.BackupPlan()
                backup_plan.cluster = "cluster_value"

                request = gke_backup_v1.CreateBackupPlanRequest(
                    parent="parent_value",
                    backup_plan=backup_plan,
                    backup_plan_id="backup_plan_id_value",
                )

                # Make the request
                operation = client.create_backup_plan(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.CreateBackupPlanRequest, dict]):
                The request object. Request message for
                CreateBackupPlan.
            parent (str):
                Required. The location within which to create the
                BackupPlan. Format: ``projects/*/locations/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_plan (google.cloud.gke_backup_v1.types.BackupPlan):
                Required. The BackupPlan resource
                object to create.

                This corresponds to the ``backup_plan`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_plan_id (str):
                Required. The client-provided short
                name for the BackupPlan resource. This
                name must:
                - be between 1 and 63 characters long
                (inclusive) - consist of only lower-case
                ASCII letters, numbers, and dashes -
                start with a lower-case letter
                - end with a lower-case letter or number
                - be unique within the set of
                BackupPlans in this location

                This corresponds to the ``backup_plan_id`` field
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
                :class:`google.cloud.gke_backup_v1.types.BackupPlan`
                Defines the configuration and scheduling for a "line" of
                Backups.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, backup_plan, backup_plan_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.CreateBackupPlanRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.CreateBackupPlanRequest):
            request = gkebackup.CreateBackupPlanRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if backup_plan is not None:
                request.backup_plan = backup_plan
            if backup_plan_id is not None:
                request.backup_plan_id = backup_plan_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_backup_plan]

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
            gcg_backup_plan.BackupPlan,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_backup_plans(
        self,
        request: Union[gkebackup.ListBackupPlansRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBackupPlansPager:
        r"""Lists BackupPlans in a given location.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_list_backup_plans():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListBackupPlansRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_backup_plans(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListBackupPlansRequest, dict]):
                The request object. Request message for ListBackupPlans.
            parent (str):
                Required. The location that contains the BackupPlans to
                list. Format: ``projects/*/locations/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListBackupPlansPager:
                Response message for ListBackupPlans.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a gkebackup.ListBackupPlansRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.ListBackupPlansRequest):
            request = gkebackup.ListBackupPlansRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_backup_plans]

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
        response = pagers.ListBackupPlansPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_backup_plan(
        self,
        request: Union[gkebackup.GetBackupPlanRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> backup_plan.BackupPlan:
        r"""Retrieve the details of a single BackupPlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_get_backup_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetBackupPlanRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_backup_plan(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetBackupPlanRequest, dict]):
                The request object. Request message for GetBackupPlan.
            name (str):
                Required. Fully qualified BackupPlan name. Format:
                ``projects/*/locations/*/backupPlans/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.types.BackupPlan:
                Defines the configuration and
                scheduling for a "line" of Backups.

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
        # in a gkebackup.GetBackupPlanRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.GetBackupPlanRequest):
            request = gkebackup.GetBackupPlanRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_backup_plan]

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

    def update_backup_plan(
        self,
        request: Union[gkebackup.UpdateBackupPlanRequest, dict] = None,
        *,
        backup_plan: gcg_backup_plan.BackupPlan = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Update a BackupPlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_update_backup_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                backup_plan = gke_backup_v1.BackupPlan()
                backup_plan.cluster = "cluster_value"

                request = gke_backup_v1.UpdateBackupPlanRequest(
                    backup_plan=backup_plan,
                )

                # Make the request
                operation = client.update_backup_plan(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.UpdateBackupPlanRequest, dict]):
                The request object. Request message for
                UpdateBackupPlan.
            backup_plan (google.cloud.gke_backup_v1.types.BackupPlan):
                Required. A new version of the BackupPlan resource that
                contains updated fields. This may be sparsely populated
                if an ``update_mask`` is provided.

                This corresponds to the ``backup_plan`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                This is used to specify the fields to be overwritten in
                the BackupPlan targeted for update. The values for each
                of these updated fields will be taken from the
                ``backup_plan`` provided with this request. Field names
                are relative to the root of the resource (e.g.,
                ``description``, ``backup_config.include_volume_data``,
                etc.) If no ``update_mask`` is provided, all fields in
                ``backup_plan`` will be written to the target BackupPlan
                resource. Note that OUTPUT_ONLY and IMMUTABLE fields in
                ``backup_plan`` are ignored and are not used to update
                the target BackupPlan.

                This corresponds to the ``update_mask`` field
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
                :class:`google.cloud.gke_backup_v1.types.BackupPlan`
                Defines the configuration and scheduling for a "line" of
                Backups.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([backup_plan, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.UpdateBackupPlanRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.UpdateBackupPlanRequest):
            request = gkebackup.UpdateBackupPlanRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if backup_plan is not None:
                request.backup_plan = backup_plan
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_backup_plan]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("backup_plan.name", request.backup_plan.name),)
            ),
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
            gcg_backup_plan.BackupPlan,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_backup_plan(
        self,
        request: Union[gkebackup.DeleteBackupPlanRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes an existing BackupPlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_delete_backup_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.DeleteBackupPlanRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_backup_plan(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.DeleteBackupPlanRequest, dict]):
                The request object. Request message for
                DeleteBackupPlan.
            name (str):
                Required. Fully qualified BackupPlan name. Format:
                ``projects/*/locations/*/backupPlans/*``

                This corresponds to the ``name`` field
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.DeleteBackupPlanRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.DeleteBackupPlanRequest):
            request = gkebackup.DeleteBackupPlanRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_backup_plan]

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
            empty_pb2.Empty,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def create_backup(
        self,
        request: Union[gkebackup.CreateBackupRequest, dict] = None,
        *,
        parent: str = None,
        backup: gcg_backup.Backup = None,
        backup_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a Backup for the given BackupPlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_create_backup():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.CreateBackupRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_backup(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.CreateBackupRequest, dict]):
                The request object. Request message for CreateBackup.
            parent (str):
                Required. The BackupPlan within which to create the
                Backup. Format: ``projects/*/locations/*/backupPlans/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup (google.cloud.gke_backup_v1.types.Backup):
                The Backup resource to create.
                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_id (str):
                The client-provided short name for
                the Backup resource. This name must:

                 - be between 1 and 63 characters long (inclusive)
                 - consist of only lower-case ASCII letters, numbers, and dashes
                 - start with a lower-case letter
                 - end with a lower-case letter or number
                 - be unique within the set of Backups in this BackupPlan

                This corresponds to the ``backup_id`` field
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

                The result type for the operation will be :class:`google.cloud.gke_backup_v1.types.Backup` Represents a request to perform a single point-in-time capture of
                   some portion of the state of a GKE cluster, the
                   record of the backup operation itself, and an anchor
                   for the underlying artifacts that comprise the Backup
                   (the config backup and VolumeBackups). Next id: 28

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, backup, backup_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.CreateBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.CreateBackupRequest):
            request = gkebackup.CreateBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if backup is not None:
                request.backup = backup
            if backup_id is not None:
                request.backup_id = backup_id

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
            gcg_backup.Backup,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_backups(
        self,
        request: Union[gkebackup.ListBackupsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBackupsPager:
        r"""Lists the Backups for a given BackupPlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_list_backups():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListBackupsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_backups(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListBackupsRequest, dict]):
                The request object. Request message for ListBackups.
            parent (str):
                Required. The BackupPlan that contains the Backups to
                list. Format: ``projects/*/locations/*/backupPlans/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListBackupsPager:
                Response message for ListBackups.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a gkebackup.ListBackupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.ListBackupsRequest):
            request = gkebackup.ListBackupsRequest(request)
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

    def get_backup(
        self,
        request: Union[gkebackup.GetBackupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> backup.Backup:
        r"""Retrieve the details of a single Backup.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_get_backup():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetBackupRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_backup(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetBackupRequest, dict]):
                The request object. Request message for GetBackup.
            name (str):
                Required. Full name of the Backup resource. Format:
                ``projects/*/locations/*/backupPlans/*/backups/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.types.Backup:
                Represents a request to perform a
                single point-in-time capture of some
                portion of the state of a GKE cluster,
                the record of the backup operation
                itself, and an anchor for the underlying
                artifacts that comprise the Backup (the
                config backup and VolumeBackups). Next
                id: 28

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
        # in a gkebackup.GetBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.GetBackupRequest):
            request = gkebackup.GetBackupRequest(request)
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
        request: Union[gkebackup.UpdateBackupRequest, dict] = None,
        *,
        backup: gcg_backup.Backup = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Update a Backup.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_update_backup():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                backup = gke_backup_v1.Backup()
                backup.all_namespaces = True

                request = gke_backup_v1.UpdateBackupRequest(
                    backup=backup,
                )

                # Make the request
                operation = client.update_backup(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.UpdateBackupRequest, dict]):
                The request object. Request message for UpdateBackup.
            backup (google.cloud.gke_backup_v1.types.Backup):
                Required. A new version of the Backup resource that
                contains updated fields. This may be sparsely populated
                if an ``update_mask`` is provided.

                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                This is used to specify the fields to be overwritten in
                the Backup targeted for update. The values for each of
                these updated fields will be taken from the
                ``backup_plan`` provided with this request. Field names
                are relative to the root of the resource. If no
                ``update_mask`` is provided, all fields in ``backup``
                will be written to the target Backup resource. Note that
                OUTPUT_ONLY and IMMUTABLE fields in ``backup`` are
                ignored and are not used to update the target Backup.

                This corresponds to the ``update_mask`` field
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

                The result type for the operation will be :class:`google.cloud.gke_backup_v1.types.Backup` Represents a request to perform a single point-in-time capture of
                   some portion of the state of a GKE cluster, the
                   record of the backup operation itself, and an anchor
                   for the underlying artifacts that comprise the Backup
                   (the config backup and VolumeBackups). Next id: 28

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
        # in a gkebackup.UpdateBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.UpdateBackupRequest):
            request = gkebackup.UpdateBackupRequest(request)
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gcg_backup.Backup,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_backup(
        self,
        request: Union[gkebackup.DeleteBackupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes an existing Backup.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_delete_backup():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.DeleteBackupRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_backup(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.DeleteBackupRequest, dict]):
                The request object. Request message for DeleteBackup.
            name (str):
                Required. Name of the Backup resource. Format:
                ``projects/*/locations/*/backupPlans/*/backups/*``

                This corresponds to the ``name`` field
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.DeleteBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.DeleteBackupRequest):
            request = gkebackup.DeleteBackupRequest(request)
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
            empty_pb2.Empty,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_volume_backups(
        self,
        request: Union[gkebackup.ListVolumeBackupsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVolumeBackupsPager:
        r"""Lists the VolumeBackups for a given Backup.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_list_volume_backups():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListVolumeBackupsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_volume_backups(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListVolumeBackupsRequest, dict]):
                The request object. Request message for
                ListVolumeBackups.
            parent (str):
                Required. The Backup that contains the VolumeBackups to
                list. Format:
                ``projects/*/locations/*/backupPlans/*/backups/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListVolumeBackupsPager:
                Response message for
                ListVolumeBackups.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a gkebackup.ListVolumeBackupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.ListVolumeBackupsRequest):
            request = gkebackup.ListVolumeBackupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_volume_backups]

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
        response = pagers.ListVolumeBackupsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_volume_backup(
        self,
        request: Union[gkebackup.GetVolumeBackupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> volume.VolumeBackup:
        r"""Retrieve the details of a single VolumeBackup.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_get_volume_backup():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetVolumeBackupRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_volume_backup(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetVolumeBackupRequest, dict]):
                The request object. Request message for GetVolumeBackup.
            name (str):
                Required. Full name of the VolumeBackup resource.
                Format:
                ``projects/*/locations/*/backupPlans/*/backups/*/volumeBackups/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.types.VolumeBackup:
                Represents the backup of a specific
                persistent volume as a component of a
                Backup - both the record of the
                operation and a pointer to the
                underlying storage-specific artifacts.
                Next id: 14

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
        # in a gkebackup.GetVolumeBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.GetVolumeBackupRequest):
            request = gkebackup.GetVolumeBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_volume_backup]

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

    def create_restore_plan(
        self,
        request: Union[gkebackup.CreateRestorePlanRequest, dict] = None,
        *,
        parent: str = None,
        restore_plan: gcg_restore_plan.RestorePlan = None,
        restore_plan_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new RestorePlan in a given location.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_create_restore_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                restore_plan = gke_backup_v1.RestorePlan()
                restore_plan.backup_plan = "backup_plan_value"
                restore_plan.cluster = "cluster_value"
                restore_plan.restore_config.all_namespaces = True

                request = gke_backup_v1.CreateRestorePlanRequest(
                    parent="parent_value",
                    restore_plan=restore_plan,
                    restore_plan_id="restore_plan_id_value",
                )

                # Make the request
                operation = client.create_restore_plan(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.CreateRestorePlanRequest, dict]):
                The request object. Request message for
                CreateRestorePlan.
            parent (str):
                Required. The location within which to create the
                RestorePlan. Format: ``projects/*/locations/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            restore_plan (google.cloud.gke_backup_v1.types.RestorePlan):
                Required. The RestorePlan resource
                object to create.

                This corresponds to the ``restore_plan`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            restore_plan_id (str):
                Required. The client-provided short
                name for the RestorePlan resource. This
                name must:

                 - be between 1 and 63 characters long (inclusive)
                 - consist of only lower-case ASCII letters, numbers, and dashes
                 - start with a lower-case letter
                 - end with a lower-case letter or number
                 - be unique within the set of RestorePlans in this location

                This corresponds to the ``restore_plan_id`` field
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

                The result type for the operation will be :class:`google.cloud.gke_backup_v1.types.RestorePlan` The configuration of a potential series of Restore operations to be performed
                   against Backups belong to a particular BackupPlan.
                   Next id: 11

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, restore_plan, restore_plan_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.CreateRestorePlanRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.CreateRestorePlanRequest):
            request = gkebackup.CreateRestorePlanRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if restore_plan is not None:
                request.restore_plan = restore_plan
            if restore_plan_id is not None:
                request.restore_plan_id = restore_plan_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_restore_plan]

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
            gcg_restore_plan.RestorePlan,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_restore_plans(
        self,
        request: Union[gkebackup.ListRestorePlansRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRestorePlansPager:
        r"""Lists RestorePlans in a given location.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_list_restore_plans():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListRestorePlansRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_restore_plans(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListRestorePlansRequest, dict]):
                The request object. Request message for
                ListRestorePlans.
            parent (str):
                Required. The location that contains the RestorePlans to
                list. Format: ``projects/*/locations/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListRestorePlansPager:
                Response message for
                ListRestorePlans.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a gkebackup.ListRestorePlansRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.ListRestorePlansRequest):
            request = gkebackup.ListRestorePlansRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_restore_plans]

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
        response = pagers.ListRestorePlansPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_restore_plan(
        self,
        request: Union[gkebackup.GetRestorePlanRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> restore_plan.RestorePlan:
        r"""Retrieve the details of a single RestorePlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_get_restore_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetRestorePlanRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_restore_plan(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetRestorePlanRequest, dict]):
                The request object. Request message for GetRestorePlan.
            name (str):
                Required. Fully qualified RestorePlan name. Format:
                ``projects/*/locations/*/restorePlans/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.types.RestorePlan:
                The configuration of a potential
                series of Restore operations to be
                performed against Backups belong to a
                particular BackupPlan. Next id: 11

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
        # in a gkebackup.GetRestorePlanRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.GetRestorePlanRequest):
            request = gkebackup.GetRestorePlanRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_restore_plan]

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

    def update_restore_plan(
        self,
        request: Union[gkebackup.UpdateRestorePlanRequest, dict] = None,
        *,
        restore_plan: gcg_restore_plan.RestorePlan = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Update a RestorePlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_update_restore_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                restore_plan = gke_backup_v1.RestorePlan()
                restore_plan.backup_plan = "backup_plan_value"
                restore_plan.cluster = "cluster_value"
                restore_plan.restore_config.all_namespaces = True

                request = gke_backup_v1.UpdateRestorePlanRequest(
                    restore_plan=restore_plan,
                )

                # Make the request
                operation = client.update_restore_plan(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.UpdateRestorePlanRequest, dict]):
                The request object. Request message for
                UpdateRestorePlan.
            restore_plan (google.cloud.gke_backup_v1.types.RestorePlan):
                Required. A new version of the RestorePlan resource that
                contains updated fields. This may be sparsely populated
                if an ``update_mask`` is provided.

                This corresponds to the ``restore_plan`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                This is used to specify the fields to be overwritten in
                the RestorePlan targeted for update. The values for each
                of these updated fields will be taken from the
                ``restore_plan`` provided with this request. Field names
                are relative to the root of the resource. If no
                ``update_mask`` is provided, all fields in
                ``restore_plan`` will be written to the target
                RestorePlan resource. Note that OUTPUT_ONLY and
                IMMUTABLE fields in ``restore_plan`` are ignored and are
                not used to update the target RestorePlan.

                This corresponds to the ``update_mask`` field
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

                The result type for the operation will be :class:`google.cloud.gke_backup_v1.types.RestorePlan` The configuration of a potential series of Restore operations to be performed
                   against Backups belong to a particular BackupPlan.
                   Next id: 11

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([restore_plan, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.UpdateRestorePlanRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.UpdateRestorePlanRequest):
            request = gkebackup.UpdateRestorePlanRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if restore_plan is not None:
                request.restore_plan = restore_plan
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_restore_plan]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("restore_plan.name", request.restore_plan.name),)
            ),
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
            gcg_restore_plan.RestorePlan,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_restore_plan(
        self,
        request: Union[gkebackup.DeleteRestorePlanRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes an existing RestorePlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_delete_restore_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.DeleteRestorePlanRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_restore_plan(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.DeleteRestorePlanRequest, dict]):
                The request object. Request message for
                DeleteRestorePlan.
            name (str):
                Required. Fully qualified RestorePlan name. Format:
                ``projects/*/locations/*/restorePlans/*``

                This corresponds to the ``name`` field
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.DeleteRestorePlanRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.DeleteRestorePlanRequest):
            request = gkebackup.DeleteRestorePlanRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_restore_plan]

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
            empty_pb2.Empty,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def create_restore(
        self,
        request: Union[gkebackup.CreateRestoreRequest, dict] = None,
        *,
        parent: str = None,
        restore: gcg_restore.Restore = None,
        restore_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new Restore for the given RestorePlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_create_restore():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                restore = gke_backup_v1.Restore()
                restore.backup = "backup_value"

                request = gke_backup_v1.CreateRestoreRequest(
                    parent="parent_value",
                    restore=restore,
                    restore_id="restore_id_value",
                )

                # Make the request
                operation = client.create_restore(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.CreateRestoreRequest, dict]):
                The request object. Request message for CreateRestore.
            parent (str):
                Required. The RestorePlan within which to create the
                Restore. Format:
                ``projects/*/locations/*/restorePlans/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            restore (google.cloud.gke_backup_v1.types.Restore):
                Required. The restore resource to
                create.

                This corresponds to the ``restore`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            restore_id (str):
                Required. The client-provided short
                name for the Restore resource. This name
                must:

                 - be between 1 and 63 characters long (inclusive)
                 - consist of only lower-case ASCII letters, numbers, and dashes
                 - start with a lower-case letter
                 - end with a lower-case letter or number
                 - be unique within the set of Restores in this RestorePlan.

                This corresponds to the ``restore_id`` field
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

                The result type for the operation will be :class:`google.cloud.gke_backup_v1.types.Restore` Represents both a request to Restore some portion of a Backup into
                   a target GKE cluster and a record of the restore
                   operation itself. Next id: 18

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, restore, restore_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.CreateRestoreRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.CreateRestoreRequest):
            request = gkebackup.CreateRestoreRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if restore is not None:
                request.restore = restore
            if restore_id is not None:
                request.restore_id = restore_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_restore]

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
            gcg_restore.Restore,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_restores(
        self,
        request: Union[gkebackup.ListRestoresRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRestoresPager:
        r"""Lists the Restores for a given RestorePlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_list_restores():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListRestoresRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_restores(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListRestoresRequest, dict]):
                The request object. Request message for ListRestores.
            parent (str):
                Required. The RestorePlan that contains the Restores to
                list. Format: ``projects/*/locations/*/restorePlans/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListRestoresPager:
                Response message for ListRestores.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a gkebackup.ListRestoresRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.ListRestoresRequest):
            request = gkebackup.ListRestoresRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_restores]

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
        response = pagers.ListRestoresPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_restore(
        self,
        request: Union[gkebackup.GetRestoreRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> restore.Restore:
        r"""Retrieves the details of a single Restore.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_get_restore():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetRestoreRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_restore(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetRestoreRequest, dict]):
                The request object. Request message for GetRestore.
            name (str):
                Required. Name of the restore resource. Format:
                ``projects/*/locations/*/restorePlans/*/restores/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.types.Restore:
                Represents both a request to Restore
                some portion of a Backup into a target
                GKE cluster and a record of the restore
                operation itself. Next id: 18

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
        # in a gkebackup.GetRestoreRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.GetRestoreRequest):
            request = gkebackup.GetRestoreRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_restore]

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

    def update_restore(
        self,
        request: Union[gkebackup.UpdateRestoreRequest, dict] = None,
        *,
        restore: gcg_restore.Restore = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Update a Restore.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_update_restore():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                restore = gke_backup_v1.Restore()
                restore.backup = "backup_value"

                request = gke_backup_v1.UpdateRestoreRequest(
                    restore=restore,
                )

                # Make the request
                operation = client.update_restore(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.UpdateRestoreRequest, dict]):
                The request object. Request message for UpdateRestore.
            restore (google.cloud.gke_backup_v1.types.Restore):
                Required. A new version of the Restore resource that
                contains updated fields. This may be sparsely populated
                if an ``update_mask`` is provided.

                This corresponds to the ``restore`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                This is used to specify the fields to be overwritten in
                the Restore targeted for update. The values for each of
                these updated fields will be taken from the ``restore``
                provided with this request. Field names are relative to
                the root of the resource. If no ``update_mask`` is
                provided, all fields in ``restore`` will be written to
                the target Restore resource. Note that OUTPUT_ONLY and
                IMMUTABLE fields in ``restore`` are ignored and are not
                used to update the target Restore.

                This corresponds to the ``update_mask`` field
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

                The result type for the operation will be :class:`google.cloud.gke_backup_v1.types.Restore` Represents both a request to Restore some portion of a Backup into
                   a target GKE cluster and a record of the restore
                   operation itself. Next id: 18

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([restore, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.UpdateRestoreRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.UpdateRestoreRequest):
            request = gkebackup.UpdateRestoreRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if restore is not None:
                request.restore = restore
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_restore]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("restore.name", request.restore.name),)
            ),
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
            gcg_restore.Restore,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_restore(
        self,
        request: Union[gkebackup.DeleteRestoreRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes an existing Restore.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_delete_restore():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.DeleteRestoreRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_restore(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.DeleteRestoreRequest, dict]):
                The request object. Request message for DeleteRestore.
            name (str):
                Required. Full name of the Restore Format:
                ``projects/*/locations/*/restorePlans/*/restores/*``

                This corresponds to the ``name`` field
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gkebackup.DeleteRestoreRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.DeleteRestoreRequest):
            request = gkebackup.DeleteRestoreRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_restore]

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
            empty_pb2.Empty,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_volume_restores(
        self,
        request: Union[gkebackup.ListVolumeRestoresRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVolumeRestoresPager:
        r"""Lists the VolumeRestores for a given Restore.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_list_volume_restores():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListVolumeRestoresRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_volume_restores(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListVolumeRestoresRequest, dict]):
                The request object. Request message for
                ListVolumeRestores.
            parent (str):
                Required. The Restore that contains the VolumeRestores
                to list. Format:
                ``projects/*/locations/*/restorePlans/*/restores/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListVolumeRestoresPager:
                Response message for
                ListVolumeRestores.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a gkebackup.ListVolumeRestoresRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.ListVolumeRestoresRequest):
            request = gkebackup.ListVolumeRestoresRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_volume_restores]

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
        response = pagers.ListVolumeRestoresPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_volume_restore(
        self,
        request: Union[gkebackup.GetVolumeRestoreRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> volume.VolumeRestore:
        r"""Retrieve the details of a single VolumeRestore.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            def sample_get_volume_restore():
                # Create a client
                client = gke_backup_v1.BackupForGKEClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetVolumeRestoreRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_volume_restore(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetVolumeRestoreRequest, dict]):
                The request object. Request message for
                GetVolumeRestore.
            name (str):
                Required. Full name of the VolumeRestore resource.
                Format:
                ``projects/*/locations/*/restorePlans/*/restores/*/volumeRestores/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_backup_v1.types.VolumeRestore:
                Represents the operation of restoring
                a volume from a VolumeBackup. Next id:
                13

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
        # in a gkebackup.GetVolumeRestoreRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gkebackup.GetVolumeRestoreRequest):
            request = gkebackup.GetVolumeRestoreRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_volume_restore]

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
            "google-cloud-gke-backup",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BackupForGKEClient",)
