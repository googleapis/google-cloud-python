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
from google.cloud.storage_transfer_v1.services.storage_transfer_service import pagers
from google.cloud.storage_transfer_v1.types import transfer
from google.cloud.storage_transfer_v1.types import transfer_types
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import StorageTransferServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import StorageTransferServiceGrpcAsyncIOTransport
from .client import StorageTransferServiceClient


class StorageTransferServiceAsyncClient:
    """Storage Transfer Service and its protos.
    Transfers data between between Google Cloud Storage buckets or
    from a data source external to Google to a Cloud Storage bucket.
    """

    _client: StorageTransferServiceClient

    DEFAULT_ENDPOINT = StorageTransferServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = StorageTransferServiceClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        StorageTransferServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        StorageTransferServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(StorageTransferServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        StorageTransferServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        StorageTransferServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        StorageTransferServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(StorageTransferServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        StorageTransferServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        StorageTransferServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        StorageTransferServiceClient.parse_common_location_path
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
            StorageTransferServiceAsyncClient: The constructed client.
        """
        return StorageTransferServiceClient.from_service_account_info.__func__(StorageTransferServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            StorageTransferServiceAsyncClient: The constructed client.
        """
        return StorageTransferServiceClient.from_service_account_file.__func__(StorageTransferServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return StorageTransferServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> StorageTransferServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            StorageTransferServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(StorageTransferServiceClient).get_transport_class,
        type(StorageTransferServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, StorageTransferServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the storage transfer service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.StorageTransferServiceTransport]): The
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
        self._client = StorageTransferServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_google_service_account(
        self,
        request: Union[transfer.GetGoogleServiceAccountRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer_types.GoogleServiceAccount:
        r"""Returns the Google service account that is used by
        Storage Transfer Service to access buckets in the
        project where transfers run or in other projects. Each
        Google service account is associated with one Google
        Cloud Platform Console project. Users should add this
        service account to the Google Cloud Storage bucket ACLs
        to grant access to Storage Transfer Service. This
        service account is created and owned by Storage Transfer
        Service and can only be used by Storage Transfer
        Service.


        .. code-block:: python

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
        request = transfer.GetGoogleServiceAccountRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_google_service_account,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_transfer_job(
        self,
        request: Union[transfer.CreateTransferJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer_types.TransferJob:
        r"""Creates a transfer job that runs periodically.

        .. code-block:: python

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
        request = transfer.CreateTransferJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_transfer_job,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_transfer_job(
        self,
        request: Union[transfer.UpdateTransferJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
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
        request = transfer.UpdateTransferJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_transfer_job,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("job_name", request.job_name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_transfer_job(
        self,
        request: Union[transfer.GetTransferJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transfer_types.TransferJob:
        r"""Gets a transfer job.

        .. code-block:: python

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
        request = transfer.GetTransferJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_transfer_job,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("job_name", request.job_name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_transfer_jobs(
        self,
        request: Union[transfer.ListTransferJobsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTransferJobsAsyncPager:
        r"""Lists transfer jobs.

        .. code-block:: python

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
                The request object. `projectId`, `jobNames`, and
                `jobStatuses` are query parameters that can be specified
                when listing transfer jobs.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_transfer_v1.services.storage_transfer_service.pagers.ListTransferJobsAsyncPager:
                Response from ListTransferJobs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = transfer.ListTransferJobsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_transfer_jobs,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTransferJobsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def pause_transfer_operation(
        self,
        request: Union[transfer.PauseTransferOperationRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Pauses a transfer operation.

        .. code-block:: python

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
        request = transfer.PauseTransferOperationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.pause_transfer_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def resume_transfer_operation(
        self,
        request: Union[transfer.ResumeTransferOperationRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Resumes a transfer operation that is paused.

        .. code-block:: python

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
        request = transfer.ResumeTransferOperationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.resume_transfer_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def run_transfer_job(
        self,
        request: Union[transfer.RunTransferJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Attempts to start a new TransferOperation for the
        current TransferJob. A TransferJob has a maximum of one
        active TransferOperation. If this method is called while
        a TransferOperation is active, an error wil be returned.


        .. code-block:: python

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
        request = transfer.RunTransferJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_transfer_job,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("job_name", request.job_name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=transfer_types.TransferOperation,
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
            "google-cloud-storage-transfer",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("StorageTransferServiceAsyncClient",)
