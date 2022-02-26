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
from google.cloud.clouddms_v1.services.data_migration_service import pagers
from google.cloud.clouddms_v1.types import clouddms
from google.cloud.clouddms_v1.types import clouddms_resources
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import DataMigrationServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import DataMigrationServiceGrpcTransport
from .transports.grpc_asyncio import DataMigrationServiceGrpcAsyncIOTransport


class DataMigrationServiceClientMeta(type):
    """Metaclass for the DataMigrationService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[DataMigrationServiceTransport]]
    _transport_registry["grpc"] = DataMigrationServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = DataMigrationServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[DataMigrationServiceTransport]:
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


class DataMigrationServiceClient(metaclass=DataMigrationServiceClientMeta):
    """Database Migration service"""

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

    DEFAULT_ENDPOINT = "datamigration.googleapis.com"
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
            DataMigrationServiceClient: The constructed client.
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
            DataMigrationServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DataMigrationServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            DataMigrationServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def connection_profile_path(
        project: str, location: str, connection_profile: str,
    ) -> str:
        """Returns a fully-qualified connection_profile string."""
        return "projects/{project}/locations/{location}/connectionProfiles/{connection_profile}".format(
            project=project, location=location, connection_profile=connection_profile,
        )

    @staticmethod
    def parse_connection_profile_path(path: str) -> Dict[str, str]:
        """Parses a connection_profile path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/connectionProfiles/(?P<connection_profile>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def migration_job_path(project: str, location: str, migration_job: str,) -> str:
        """Returns a fully-qualified migration_job string."""
        return "projects/{project}/locations/{location}/migrationJobs/{migration_job}".format(
            project=project, location=location, migration_job=migration_job,
        )

    @staticmethod
    def parse_migration_job_path(path: str) -> Dict[str, str]:
        """Parses a migration_job path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/migrationJobs/(?P<migration_job>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

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
        transport: Union[str, DataMigrationServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the data migration service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, DataMigrationServiceTransport]): The
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
        if isinstance(transport, DataMigrationServiceTransport):
            # transport is a DataMigrationServiceTransport instance.
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

    def list_migration_jobs(
        self,
        request: Union[clouddms.ListMigrationJobsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMigrationJobsPager:
        r"""Lists migration jobs in a given project and location.

        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_list_migration_jobs():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.ListMigrationJobsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_migration_jobs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.ListMigrationJobsRequest, dict]):
                The request object. Retrieve a list of all migration
                jobs in a given project and location.
            parent (str):
                Required. The parent, which owns this
                collection of migrationJobs.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.clouddms_v1.services.data_migration_service.pagers.ListMigrationJobsPager:
                Response message for
                'ListMigrationJobs' request.
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
        # in a clouddms.ListMigrationJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.ListMigrationJobsRequest):
            request = clouddms.ListMigrationJobsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_migration_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListMigrationJobsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_migration_job(
        self,
        request: Union[clouddms.GetMigrationJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> clouddms_resources.MigrationJob:
        r"""Gets details of a single migration job.

        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_get_migration_job():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.GetMigrationJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_migration_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.GetMigrationJobRequest, dict]):
                The request object. Request message for
                'GetMigrationJob' request.
            name (str):
                Required. Name of the migration job
                resource to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.clouddms_v1.types.MigrationJob:
                Represents a Database Migration
                Service migration job object.

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
        # in a clouddms.GetMigrationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.GetMigrationJobRequest):
            request = clouddms.GetMigrationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_migration_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_migration_job(
        self,
        request: Union[clouddms.CreateMigrationJobRequest, dict] = None,
        *,
        parent: str = None,
        migration_job: clouddms_resources.MigrationJob = None,
        migration_job_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new migration job in a given project and
        location.


        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_create_migration_job():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                migration_job = clouddms_v1.MigrationJob()
                migration_job.reverse_ssh_connectivity.vm_ip = "vm_ip_value"
                migration_job.reverse_ssh_connectivity.vm_port = 775
                migration_job.type_ = "CONTINUOUS"
                migration_job.source = "source_value"
                migration_job.destination = "destination_value"

                request = clouddms_v1.CreateMigrationJobRequest(
                    parent="parent_value",
                    migration_job_id="migration_job_id_value",
                    migration_job=migration_job,
                )

                # Make the request
                operation = client.create_migration_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.CreateMigrationJobRequest, dict]):
                The request object. Request message to create a new
                Database Migration Service migration job in the
                specified project and region.
            parent (str):
                Required. The parent, which owns this
                collection of migration jobs.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            migration_job (google.cloud.clouddms_v1.types.MigrationJob):
                Required. Represents a `migration
                job <https://cloud.google.com/database-migration/docs/reference/rest/v1/projects.locations.migrationJobs>`__
                object.

                This corresponds to the ``migration_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            migration_job_id (str):
                Required. The ID of the instance to
                create.

                This corresponds to the ``migration_job_id`` field
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
                :class:`google.cloud.clouddms_v1.types.MigrationJob`
                Represents a Database Migration Service migration job
                object.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, migration_job, migration_job_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.CreateMigrationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.CreateMigrationJobRequest):
            request = clouddms.CreateMigrationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if migration_job is not None:
                request.migration_job = migration_job
            if migration_job_id is not None:
                request.migration_job_id = migration_job_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_migration_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clouddms_resources.MigrationJob,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_migration_job(
        self,
        request: Union[clouddms.UpdateMigrationJobRequest, dict] = None,
        *,
        migration_job: clouddms_resources.MigrationJob = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the parameters of a single migration job.

        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_update_migration_job():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                migration_job = clouddms_v1.MigrationJob()
                migration_job.reverse_ssh_connectivity.vm_ip = "vm_ip_value"
                migration_job.reverse_ssh_connectivity.vm_port = 775
                migration_job.type_ = "CONTINUOUS"
                migration_job.source = "source_value"
                migration_job.destination = "destination_value"

                request = clouddms_v1.UpdateMigrationJobRequest(
                    migration_job=migration_job,
                )

                # Make the request
                operation = client.update_migration_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.UpdateMigrationJobRequest, dict]):
                The request object. Request message for
                'UpdateMigrationJob' request.
            migration_job (google.cloud.clouddms_v1.types.MigrationJob):
                Required. The migration job
                parameters to update.

                This corresponds to the ``migration_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to
                specify the fields to be overwritten in
                the migration job resource by the
                update.

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
                :class:`google.cloud.clouddms_v1.types.MigrationJob`
                Represents a Database Migration Service migration job
                object.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([migration_job, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.UpdateMigrationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.UpdateMigrationJobRequest):
            request = clouddms.UpdateMigrationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if migration_job is not None:
                request.migration_job = migration_job
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_migration_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("migration_job.name", request.migration_job.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clouddms_resources.MigrationJob,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_migration_job(
        self,
        request: Union[clouddms.DeleteMigrationJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single migration job.

        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_delete_migration_job():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.DeleteMigrationJobRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_migration_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.DeleteMigrationJobRequest, dict]):
                The request object. Request message for
                'DeleteMigrationJob' request.
            name (str):
                Required. Name of the migration job
                resource to delete.

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
        # in a clouddms.DeleteMigrationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.DeleteMigrationJobRequest):
            request = clouddms.DeleteMigrationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_migration_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def start_migration_job(
        self,
        request: Union[clouddms.StartMigrationJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Start an already created migration job.

        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_start_migration_job():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.StartMigrationJobRequest(
                )

                # Make the request
                operation = client.start_migration_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.StartMigrationJobRequest, dict]):
                The request object. Request message for
                'StartMigrationJob' request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.clouddms_v1.types.MigrationJob`
                Represents a Database Migration Service migration job
                object.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.StartMigrationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.StartMigrationJobRequest):
            request = clouddms.StartMigrationJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start_migration_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clouddms_resources.MigrationJob,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def stop_migration_job(
        self,
        request: Union[clouddms.StopMigrationJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Stops a running migration job.

        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_stop_migration_job():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.StopMigrationJobRequest(
                )

                # Make the request
                operation = client.stop_migration_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.StopMigrationJobRequest, dict]):
                The request object. Request message for
                'StopMigrationJob' request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.clouddms_v1.types.MigrationJob`
                Represents a Database Migration Service migration job
                object.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.StopMigrationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.StopMigrationJobRequest):
            request = clouddms.StopMigrationJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.stop_migration_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clouddms_resources.MigrationJob,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def resume_migration_job(
        self,
        request: Union[clouddms.ResumeMigrationJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Resume a migration job that is currently stopped and
        is resumable (was stopped during CDC phase).


        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_resume_migration_job():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.ResumeMigrationJobRequest(
                )

                # Make the request
                operation = client.resume_migration_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.ResumeMigrationJobRequest, dict]):
                The request object. Request message for
                'ResumeMigrationJob' request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.clouddms_v1.types.MigrationJob`
                Represents a Database Migration Service migration job
                object.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.ResumeMigrationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.ResumeMigrationJobRequest):
            request = clouddms.ResumeMigrationJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resume_migration_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clouddms_resources.MigrationJob,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def promote_migration_job(
        self,
        request: Union[clouddms.PromoteMigrationJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Promote a migration job, stopping replication to the
        destination and promoting the destination to be a
        standalone database.


        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_promote_migration_job():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.PromoteMigrationJobRequest(
                )

                # Make the request
                operation = client.promote_migration_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.PromoteMigrationJobRequest, dict]):
                The request object. Request message for
                'PromoteMigrationJob' request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.clouddms_v1.types.MigrationJob`
                Represents a Database Migration Service migration job
                object.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.PromoteMigrationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.PromoteMigrationJobRequest):
            request = clouddms.PromoteMigrationJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.promote_migration_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clouddms_resources.MigrationJob,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def verify_migration_job(
        self,
        request: Union[clouddms.VerifyMigrationJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Verify a migration job, making sure the destination
        can reach the source and that all configuration and
        prerequisites are met.


        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_verify_migration_job():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.VerifyMigrationJobRequest(
                )

                # Make the request
                operation = client.verify_migration_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.VerifyMigrationJobRequest, dict]):
                The request object. Request message for
                'VerifyMigrationJob' request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.clouddms_v1.types.MigrationJob`
                Represents a Database Migration Service migration job
                object.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.VerifyMigrationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.VerifyMigrationJobRequest):
            request = clouddms.VerifyMigrationJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.verify_migration_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clouddms_resources.MigrationJob,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def restart_migration_job(
        self,
        request: Union[clouddms.RestartMigrationJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Restart a stopped or failed migration job, resetting
        the destination instance to its original state and
        starting the migration process from scratch.


        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_restart_migration_job():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.RestartMigrationJobRequest(
                )

                # Make the request
                operation = client.restart_migration_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.RestartMigrationJobRequest, dict]):
                The request object. Request message for
                'RestartMigrationJob' request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.clouddms_v1.types.MigrationJob`
                Represents a Database Migration Service migration job
                object.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.RestartMigrationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.RestartMigrationJobRequest):
            request = clouddms.RestartMigrationJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.restart_migration_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clouddms_resources.MigrationJob,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def generate_ssh_script(
        self,
        request: Union[clouddms.GenerateSshScriptRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> clouddms.SshScript:
        r"""Generate a SSH configuration script to configure the
        reverse SSH connectivity.


        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_generate_ssh_script():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                vm_creation_config = clouddms_v1.VmCreationConfig()
                vm_creation_config.vm_machine_type = "vm_machine_type_value"

                request = clouddms_v1.GenerateSshScriptRequest(
                    vm_creation_config=vm_creation_config,
                    vm="vm_value",
                )

                # Make the request
                response = client.generate_ssh_script(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.GenerateSshScriptRequest, dict]):
                The request object. Request message for
                'GenerateSshScript' request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.clouddms_v1.types.SshScript:
                Response message for
                'GenerateSshScript' request.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.GenerateSshScriptRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.GenerateSshScriptRequest):
            request = clouddms.GenerateSshScriptRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.generate_ssh_script]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("migration_job", request.migration_job),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_connection_profiles(
        self,
        request: Union[clouddms.ListConnectionProfilesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConnectionProfilesPager:
        r"""Retrieve a list of all connection profiles in a given
        project and location.


        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_list_connection_profiles():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.ListConnectionProfilesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_connection_profiles(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.ListConnectionProfilesRequest, dict]):
                The request object. Request message for
                'ListConnectionProfiles' request.
            parent (str):
                Required. The parent, which owns this
                collection of connection profiles.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.clouddms_v1.services.data_migration_service.pagers.ListConnectionProfilesPager:
                Response message for
                'ListConnectionProfiles' request.
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
        # in a clouddms.ListConnectionProfilesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.ListConnectionProfilesRequest):
            request = clouddms.ListConnectionProfilesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_connection_profiles]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListConnectionProfilesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_connection_profile(
        self,
        request: Union[clouddms.GetConnectionProfileRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> clouddms_resources.ConnectionProfile:
        r"""Gets details of a single connection profile.

        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_get_connection_profile():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.GetConnectionProfileRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_connection_profile(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.GetConnectionProfileRequest, dict]):
                The request object. Request message for
                'GetConnectionProfile' request.
            name (str):
                Required. Name of the connection
                profile resource to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.clouddms_v1.types.ConnectionProfile:
                A connection profile definition.
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
        # in a clouddms.GetConnectionProfileRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.GetConnectionProfileRequest):
            request = clouddms.GetConnectionProfileRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_connection_profile]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_connection_profile(
        self,
        request: Union[clouddms.CreateConnectionProfileRequest, dict] = None,
        *,
        parent: str = None,
        connection_profile: clouddms_resources.ConnectionProfile = None,
        connection_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new connection profile in a given project
        and location.


        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_create_connection_profile():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                connection_profile = clouddms_v1.ConnectionProfile()
                connection_profile.mysql.host = "host_value"
                connection_profile.mysql.port = 453
                connection_profile.mysql.username = "username_value"
                connection_profile.mysql.password = "password_value"

                request = clouddms_v1.CreateConnectionProfileRequest(
                    parent="parent_value",
                    connection_profile_id="connection_profile_id_value",
                    connection_profile=connection_profile,
                )

                # Make the request
                operation = client.create_connection_profile(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.CreateConnectionProfileRequest, dict]):
                The request object. Request message for
                'CreateConnectionProfile' request.
            parent (str):
                Required. The parent, which owns this
                collection of connection profiles.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            connection_profile (google.cloud.clouddms_v1.types.ConnectionProfile):
                Required. The create request body
                including the connection profile data

                This corresponds to the ``connection_profile`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            connection_profile_id (str):
                Required. The connection profile
                identifier.

                This corresponds to the ``connection_profile_id`` field
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
                :class:`google.cloud.clouddms_v1.types.ConnectionProfile`
                A connection profile definition.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, connection_profile, connection_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.CreateConnectionProfileRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.CreateConnectionProfileRequest):
            request = clouddms.CreateConnectionProfileRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if connection_profile is not None:
                request.connection_profile = connection_profile
            if connection_profile_id is not None:
                request.connection_profile_id = connection_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_connection_profile
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clouddms_resources.ConnectionProfile,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_connection_profile(
        self,
        request: Union[clouddms.UpdateConnectionProfileRequest, dict] = None,
        *,
        connection_profile: clouddms_resources.ConnectionProfile = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Update the configuration of a single connection
        profile.


        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_update_connection_profile():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                connection_profile = clouddms_v1.ConnectionProfile()
                connection_profile.mysql.host = "host_value"
                connection_profile.mysql.port = 453
                connection_profile.mysql.username = "username_value"
                connection_profile.mysql.password = "password_value"

                request = clouddms_v1.UpdateConnectionProfileRequest(
                    connection_profile=connection_profile,
                )

                # Make the request
                operation = client.update_connection_profile(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.UpdateConnectionProfileRequest, dict]):
                The request object. Request message for
                'UpdateConnectionProfile' request.
            connection_profile (google.cloud.clouddms_v1.types.ConnectionProfile):
                Required. The connection profile
                parameters to update.

                This corresponds to the ``connection_profile`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to
                specify the fields to be overwritten in
                the connection profile resource by the
                update.

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
                :class:`google.cloud.clouddms_v1.types.ConnectionProfile`
                A connection profile definition.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([connection_profile, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a clouddms.UpdateConnectionProfileRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.UpdateConnectionProfileRequest):
            request = clouddms.UpdateConnectionProfileRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if connection_profile is not None:
                request.connection_profile = connection_profile
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_connection_profile
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("connection_profile.name", request.connection_profile.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            clouddms_resources.ConnectionProfile,
            metadata_type=clouddms.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_connection_profile(
        self,
        request: Union[clouddms.DeleteConnectionProfileRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single Database Migration Service
        connection profile. A connection profile can only be
        deleted if it is not in use by any active migration
        jobs.


        .. code-block:: python

            from google.cloud import clouddms_v1

            def sample_delete_connection_profile():
                # Create a client
                client = clouddms_v1.DataMigrationServiceClient()

                # Initialize request argument(s)
                request = clouddms_v1.DeleteConnectionProfileRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_connection_profile(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.clouddms_v1.types.DeleteConnectionProfileRequest, dict]):
                The request object. Request message for
                'DeleteConnectionProfile' request.
            name (str):
                Required. Name of the connection
                profile resource to delete.

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
        # in a clouddms.DeleteConnectionProfileRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, clouddms.DeleteConnectionProfileRequest):
            request = clouddms.DeleteConnectionProfileRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_connection_profile
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=clouddms.OperationMetadata,
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
        gapic_version=pkg_resources.get_distribution("google-cloud-dms",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DataMigrationServiceClient",)
