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
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.storage_transfer_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.storage_transfer_v1.services.storage_transfer_service import pagers
from google.cloud.storage_transfer_v1.types import transfer, transfer_types

from .transports.base import DEFAULT_CLIENT_INFO, StorageTransferServiceTransport
from .transports.grpc import StorageTransferServiceGrpcTransport
from .transports.grpc_asyncio import StorageTransferServiceGrpcAsyncIOTransport
from .transports.rest import StorageTransferServiceRestTransport


class StorageTransferServiceClientMeta(type):
    """Metaclass for the StorageTransferService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[StorageTransferServiceTransport]]
    _transport_registry["grpc"] = StorageTransferServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = StorageTransferServiceGrpcAsyncIOTransport
    _transport_registry["rest"] = StorageTransferServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[StorageTransferServiceTransport]:
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


class StorageTransferServiceClient(metaclass=StorageTransferServiceClientMeta):
    """Storage Transfer Service and its protos.
    Transfers data between between Google Cloud Storage buckets or
    from a data source external to Google to a Cloud Storage bucket.
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

    DEFAULT_ENDPOINT = "storagetransfer.googleapis.com"
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
            StorageTransferServiceClient: The constructed client.
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
            StorageTransferServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> StorageTransferServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            StorageTransferServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def agent_pools_path(
        project_id: str,
        agent_pool_id: str,
    ) -> str:
        """Returns a fully-qualified agent_pools string."""
        return "projects/{project_id}/agentPools/{agent_pool_id}".format(
            project_id=project_id,
            agent_pool_id=agent_pool_id,
        )

    @staticmethod
    def parse_agent_pools_path(path: str) -> Dict[str, str]:
        """Parses a agent_pools path into its component segments."""
        m = re.match(
            r"^projects/(?P<project_id>.+?)/agentPools/(?P<agent_pool_id>.+?)$", path
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
        default mTLS endpoint; if the environment variable is "never", use the default API
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
        transport: Optional[Union[str, StorageTransferServiceTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the storage transfer service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, StorageTransferServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
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
        client_options = cast(client_options_lib.ClientOptions, client_options)

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
        if isinstance(transport, StorageTransferServiceTransport):
            # transport is a StorageTransferServiceTransport instance.
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

    def get_google_service_account(
        self,
        request: Optional[Union[transfer.GetGoogleServiceAccountRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer_types.GoogleServiceAccount:
        r"""Returns the Google service account that is used by
        Storage Transfer Service to access buckets in the
        project where transfers run or in other projects. Each
        Google service account is associated with one Google
        Cloud project. Users
        should add this service account to the Google Cloud
        Storage bucket ACLs to grant access to Storage Transfer
        Service. This service account is created and owned by
        Storage Transfer Service and can only be used by Storage
        Transfer Service.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_get_google_service_account():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.GetGoogleServiceAccountRequest(
                    project_id="project_id_value",
                )

                # Make the request
                response = client.get_google_service_account(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.GetGoogleServiceAccountRequest, dict]):
                The request object. Request passed to
                GetGoogleServiceAccount.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_transfer_v1.types.GoogleServiceAccount:
                Google service account
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.GetGoogleServiceAccountRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.GetGoogleServiceAccountRequest):
            request = transfer.GetGoogleServiceAccountRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_google_service_account
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("project_id", request.project_id),)
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

    def create_transfer_job(
        self,
        request: Optional[Union[transfer.CreateTransferJobRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer_types.TransferJob:
        r"""Creates a transfer job that runs periodically.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_create_transfer_job():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.CreateTransferJobRequest(
                )

                # Make the request
                response = client.create_transfer_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.CreateTransferJobRequest, dict]):
                The request object. Request passed to CreateTransferJob.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_transfer_v1.types.TransferJob:
                This resource represents the
                configuration of a transfer job that
                runs periodically.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.CreateTransferJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.CreateTransferJobRequest):
            request = transfer.CreateTransferJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_transfer_job]

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_transfer_job(
        self,
        request: Optional[Union[transfer.UpdateTransferJobRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer_types.TransferJob:
        r"""Updates a transfer job. Updating a job's transfer spec does not
        affect transfer operations that are running already.

        **Note:** The job's
        [status][google.storagetransfer.v1.TransferJob.status] field can
        be modified using this RPC (for example, to set a job's status
        to
        [DELETED][google.storagetransfer.v1.TransferJob.Status.DELETED],
        [DISABLED][google.storagetransfer.v1.TransferJob.Status.DISABLED],
        or
        [ENABLED][google.storagetransfer.v1.TransferJob.Status.ENABLED]).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_update_transfer_job():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.UpdateTransferJobRequest(
                    job_name="job_name_value",
                    project_id="project_id_value",
                )

                # Make the request
                response = client.update_transfer_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.UpdateTransferJobRequest, dict]):
                The request object. Request passed to UpdateTransferJob.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_transfer_v1.types.TransferJob:
                This resource represents the
                configuration of a transfer job that
                runs periodically.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.UpdateTransferJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.UpdateTransferJobRequest):
            request = transfer.UpdateTransferJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_transfer_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("job_name", request.job_name),)),
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

    def get_transfer_job(
        self,
        request: Optional[Union[transfer.GetTransferJobRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer_types.TransferJob:
        r"""Gets a transfer job.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_get_transfer_job():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.GetTransferJobRequest(
                    job_name="job_name_value",
                    project_id="project_id_value",
                )

                # Make the request
                response = client.get_transfer_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.GetTransferJobRequest, dict]):
                The request object. Request passed to GetTransferJob.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_transfer_v1.types.TransferJob:
                This resource represents the
                configuration of a transfer job that
                runs periodically.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.GetTransferJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.GetTransferJobRequest):
            request = transfer.GetTransferJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_transfer_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("job_name", request.job_name),)),
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

    def list_transfer_jobs(
        self,
        request: Optional[Union[transfer.ListTransferJobsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTransferJobsPager:
        r"""Lists transfer jobs.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_list_transfer_jobs():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.ListTransferJobsRequest(
                    filter="filter_value",
                )

                # Make the request
                page_result = client.list_transfer_jobs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.ListTransferJobsRequest, dict]):
                The request object. ``projectId``, ``jobNames``, and ``jobStatuses`` are
                query parameters that can be specified when listing
                transfer jobs.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_transfer_v1.services.storage_transfer_service.pagers.ListTransferJobsPager:
                Response from ListTransferJobs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.ListTransferJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.ListTransferJobsRequest):
            request = transfer.ListTransferJobsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_transfer_jobs]

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTransferJobsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def pause_transfer_operation(
        self,
        request: Optional[Union[transfer.PauseTransferOperationRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Pauses a transfer operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_pause_transfer_operation():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.PauseTransferOperationRequest(
                    name="name_value",
                )

                # Make the request
                client.pause_transfer_operation(request=request)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.PauseTransferOperationRequest, dict]):
                The request object. Request passed to
                PauseTransferOperation.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.PauseTransferOperationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.PauseTransferOperationRequest):
            request = transfer.PauseTransferOperationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.pause_transfer_operation]

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

    def resume_transfer_operation(
        self,
        request: Optional[Union[transfer.ResumeTransferOperationRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Resumes a transfer operation that is paused.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_resume_transfer_operation():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.ResumeTransferOperationRequest(
                    name="name_value",
                )

                # Make the request
                client.resume_transfer_operation(request=request)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.ResumeTransferOperationRequest, dict]):
                The request object. Request passed to
                ResumeTransferOperation.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.ResumeTransferOperationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.ResumeTransferOperationRequest):
            request = transfer.ResumeTransferOperationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.resume_transfer_operation
        ]

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

    def run_transfer_job(
        self,
        request: Optional[Union[transfer.RunTransferJobRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Starts a new operation for the specified transfer job. A
        ``TransferJob`` has a maximum of one active
        ``TransferOperation``. If this method is called while a
        ``TransferOperation`` is active, an error is returned.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_run_transfer_job():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.RunTransferJobRequest(
                    job_name="job_name_value",
                    project_id="project_id_value",
                )

                # Make the request
                operation = client.run_transfer_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.RunTransferJobRequest, dict]):
                The request object. Request passed to RunTransferJob.
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

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.RunTransferJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.RunTransferJobRequest):
            request = transfer.RunTransferJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_transfer_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("job_name", request.job_name),)),
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
            metadata_type=transfer_types.TransferOperation,
        )

        # Done; return the response.
        return response

    def delete_transfer_job(
        self,
        request: Optional[Union[transfer.DeleteTransferJobRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a transfer job. Deleting a transfer job sets its status
        to
        [DELETED][google.storagetransfer.v1.TransferJob.Status.DELETED].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_delete_transfer_job():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.DeleteTransferJobRequest(
                    job_name="job_name_value",
                    project_id="project_id_value",
                )

                # Make the request
                client.delete_transfer_job(request=request)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.DeleteTransferJobRequest, dict]):
                The request object. Request passed to DeleteTransferJob.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.DeleteTransferJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.DeleteTransferJobRequest):
            request = transfer.DeleteTransferJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_transfer_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("job_name", request.job_name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_agent_pool(
        self,
        request: Optional[Union[transfer.CreateAgentPoolRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        agent_pool: Optional[transfer_types.AgentPool] = None,
        agent_pool_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer_types.AgentPool:
        r"""Creates an agent pool resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_create_agent_pool():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                agent_pool = storage_transfer_v1.AgentPool()
                agent_pool.name = "name_value"

                request = storage_transfer_v1.CreateAgentPoolRequest(
                    project_id="project_id_value",
                    agent_pool=agent_pool,
                    agent_pool_id="agent_pool_id_value",
                )

                # Make the request
                response = client.create_agent_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.CreateAgentPoolRequest, dict]):
                The request object. Specifies the request passed to
                CreateAgentPool.
            project_id (str):
                Required. The ID of the Google Cloud
                project that owns the agent pool.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            agent_pool (google.cloud.storage_transfer_v1.types.AgentPool):
                Required. The agent pool to create.
                This corresponds to the ``agent_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            agent_pool_id (str):
                Required. The ID of the agent pool to create.

                The ``agent_pool_id`` must meet the following
                requirements:

                -  Length of 128 characters or less.
                -  Not start with the string ``goog``.
                -  Start with a lowercase ASCII character, followed by:

                   -  Zero or more: lowercase Latin alphabet characters,
                      numerals, hyphens (``-``), periods (``.``),
                      underscores (``_``), or tildes (``~``).
                   -  One or more numerals or lowercase ASCII
                      characters.

                As expressed by the regular expression:
                ``^(?!goog)[a-z]([a-z0-9-._~]*[a-z0-9])?$``.

                This corresponds to the ``agent_pool_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_transfer_v1.types.AgentPool:
                Represents an On-Premises Agent pool.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, agent_pool, agent_pool_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.CreateAgentPoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.CreateAgentPoolRequest):
            request = transfer.CreateAgentPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if agent_pool is not None:
                request.agent_pool = agent_pool
            if agent_pool_id is not None:
                request.agent_pool_id = agent_pool_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_agent_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("project_id", request.project_id),)
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

    def update_agent_pool(
        self,
        request: Optional[Union[transfer.UpdateAgentPoolRequest, dict]] = None,
        *,
        agent_pool: Optional[transfer_types.AgentPool] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer_types.AgentPool:
        r"""Updates an existing agent pool resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_update_agent_pool():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                agent_pool = storage_transfer_v1.AgentPool()
                agent_pool.name = "name_value"

                request = storage_transfer_v1.UpdateAgentPoolRequest(
                    agent_pool=agent_pool,
                )

                # Make the request
                response = client.update_agent_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.UpdateAgentPoolRequest, dict]):
                The request object. Specifies the request passed to
                UpdateAgentPool.
            agent_pool (google.cloud.storage_transfer_v1.types.AgentPool):
                Required. The agent pool to update. ``agent_pool`` is
                expected to specify following fields:

                -  [name][google.storagetransfer.v1.AgentPool.name]

                -  [display_name][google.storagetransfer.v1.AgentPool.display_name]

                -  [bandwidth_limit][google.storagetransfer.v1.AgentPool.bandwidth_limit]
                   An ``UpdateAgentPoolRequest`` with any other fields
                   is rejected with the error
                   [INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT].

                This corresponds to the ``agent_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The [field mask]
                (https://developers.google.com/protocol-buffers/docs/reference/google.protobuf)
                of the fields in ``agentPool`` to update in this
                request. The following ``agentPool`` fields can be
                updated:

                -  [display_name][google.storagetransfer.v1.AgentPool.display_name]

                -  [bandwidth_limit][google.storagetransfer.v1.AgentPool.bandwidth_limit]

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_transfer_v1.types.AgentPool:
                Represents an On-Premises Agent pool.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([agent_pool, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.UpdateAgentPoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.UpdateAgentPoolRequest):
            request = transfer.UpdateAgentPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if agent_pool is not None:
                request.agent_pool = agent_pool
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_agent_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("agent_pool.name", request.agent_pool.name),)
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

    def get_agent_pool(
        self,
        request: Optional[Union[transfer.GetAgentPoolRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer_types.AgentPool:
        r"""Gets an agent pool.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_get_agent_pool():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.GetAgentPoolRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_agent_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.GetAgentPoolRequest, dict]):
                The request object. Specifies the request passed to
                GetAgentPool.
            name (str):
                Required. The name of the agent pool
                to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_transfer_v1.types.AgentPool:
                Represents an On-Premises Agent pool.
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
        # in a transfer.GetAgentPoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.GetAgentPoolRequest):
            request = transfer.GetAgentPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_agent_pool]

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

    def list_agent_pools(
        self,
        request: Optional[Union[transfer.ListAgentPoolsRequest, dict]] = None,
        *,
        project_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAgentPoolsPager:
        r"""Lists agent pools.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_list_agent_pools():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.ListAgentPoolsRequest(
                    project_id="project_id_value",
                )

                # Make the request
                page_result = client.list_agent_pools(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.ListAgentPoolsRequest, dict]):
                The request object. The request passed to ListAgentPools.
            project_id (str):
                Required. The ID of the Google Cloud
                project that owns the job.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_transfer_v1.services.storage_transfer_service.pagers.ListAgentPoolsPager:
                Response from ListAgentPools.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a transfer.ListAgentPoolsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.ListAgentPoolsRequest):
            request = transfer.ListAgentPoolsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_agent_pools]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("project_id", request.project_id),)
            ),
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
        response = pagers.ListAgentPoolsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_agent_pool(
        self,
        request: Optional[Union[transfer.DeleteAgentPoolRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an agent pool.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_transfer_v1

            def sample_delete_agent_pool():
                # Create a client
                client = storage_transfer_v1.StorageTransferServiceClient()

                # Initialize request argument(s)
                request = storage_transfer_v1.DeleteAgentPoolRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_agent_pool(request=request)

        Args:
            request (Union[google.cloud.storage_transfer_v1.types.DeleteAgentPoolRequest, dict]):
                The request object. Specifies the request passed to
                DeleteAgentPool.
            name (str):
                Required. The name of the agent pool
                to delete.

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
        # in a transfer.DeleteAgentPoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, transfer.DeleteAgentPoolRequest):
            request = transfer.DeleteAgentPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_agent_pool]

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

    def __enter__(self) -> "StorageTransferServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_operations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.cancel_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

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


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("StorageTransferServiceClient",)
