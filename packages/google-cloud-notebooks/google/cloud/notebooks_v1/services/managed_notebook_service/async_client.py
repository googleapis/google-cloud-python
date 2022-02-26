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
from google.cloud.notebooks_v1.services.managed_notebook_service import pagers
from google.cloud.notebooks_v1.types import managed_service
from google.cloud.notebooks_v1.types import runtime
from google.cloud.notebooks_v1.types import runtime as gcn_runtime
from google.cloud.notebooks_v1.types import service
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import ManagedNotebookServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ManagedNotebookServiceGrpcAsyncIOTransport
from .client import ManagedNotebookServiceClient


class ManagedNotebookServiceAsyncClient:
    """API v1 service for Managed Notebooks."""

    _client: ManagedNotebookServiceClient

    DEFAULT_ENDPOINT = ManagedNotebookServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ManagedNotebookServiceClient.DEFAULT_MTLS_ENDPOINT

    runtime_path = staticmethod(ManagedNotebookServiceClient.runtime_path)
    parse_runtime_path = staticmethod(ManagedNotebookServiceClient.parse_runtime_path)
    common_billing_account_path = staticmethod(
        ManagedNotebookServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ManagedNotebookServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ManagedNotebookServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ManagedNotebookServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ManagedNotebookServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ManagedNotebookServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ManagedNotebookServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        ManagedNotebookServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        ManagedNotebookServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        ManagedNotebookServiceClient.parse_common_location_path
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
            ManagedNotebookServiceAsyncClient: The constructed client.
        """
        return ManagedNotebookServiceClient.from_service_account_info.__func__(ManagedNotebookServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ManagedNotebookServiceAsyncClient: The constructed client.
        """
        return ManagedNotebookServiceClient.from_service_account_file.__func__(ManagedNotebookServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return ManagedNotebookServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ManagedNotebookServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ManagedNotebookServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ManagedNotebookServiceClient).get_transport_class,
        type(ManagedNotebookServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ManagedNotebookServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the managed notebook service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ManagedNotebookServiceTransport]): The
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
        self._client = ManagedNotebookServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_runtimes(
        self,
        request: Union[managed_service.ListRuntimesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRuntimesAsyncPager:
        r"""Lists Runtimes in a given project and location.

        .. code-block:: python

            from google.cloud import notebooks_v1

            def sample_list_runtimes():
                # Create a client
                client = notebooks_v1.ManagedNotebookServiceClient()

                # Initialize request argument(s)
                request = notebooks_v1.ListRuntimesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_runtimes(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.notebooks_v1.types.ListRuntimesRequest, dict]):
                The request object. Request for listing Managed Notebook
                Runtimes.
            parent (:class:`str`):
                Required. Format:
                ``parent=projects/{project_id}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.notebooks_v1.services.managed_notebook_service.pagers.ListRuntimesAsyncPager:
                Response for listing Managed Notebook
                Runtimes.
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

        request = managed_service.ListRuntimesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_runtimes,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListRuntimesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_runtime(
        self,
        request: Union[managed_service.GetRuntimeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> runtime.Runtime:
        r"""Gets details of a single Runtime. The location must
        be a regional endpoint rather than zonal.


        .. code-block:: python

            from google.cloud import notebooks_v1

            def sample_get_runtime():
                # Create a client
                client = notebooks_v1.ManagedNotebookServiceClient()

                # Initialize request argument(s)
                request = notebooks_v1.GetRuntimeRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_runtime(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.notebooks_v1.types.GetRuntimeRequest, dict]):
                The request object. Request for getting a Managed
                Notebook Runtime.
            name (:class:`str`):
                Required. Format:
                ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.notebooks_v1.types.Runtime:
                The definition of a Runtime for a
                managed notebook instance.

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

        request = managed_service.GetRuntimeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_runtime,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_runtime(
        self,
        request: Union[managed_service.CreateRuntimeRequest, dict] = None,
        *,
        parent: str = None,
        runtime_id: str = None,
        runtime: gcn_runtime.Runtime = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Runtime in a given project and
        location.


        .. code-block:: python

            from google.cloud import notebooks_v1

            def sample_create_runtime():
                # Create a client
                client = notebooks_v1.ManagedNotebookServiceClient()

                # Initialize request argument(s)
                request = notebooks_v1.CreateRuntimeRequest(
                    parent="parent_value",
                    runtime_id="runtime_id_value",
                )

                # Make the request
                operation = client.create_runtime(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.notebooks_v1.types.CreateRuntimeRequest, dict]):
                The request object. Request for creating a Managed
                Notebook Runtime.
            parent (:class:`str`):
                Required. Format:
                ``parent=projects/{project_id}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            runtime_id (:class:`str`):
                Required. User-defined unique ID of
                this Runtime.

                This corresponds to the ``runtime_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            runtime (:class:`google.cloud.notebooks_v1.types.Runtime`):
                Required. The Runtime to be created.
                This corresponds to the ``runtime`` field
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
                :class:`google.cloud.notebooks_v1.types.Runtime` The
                definition of a Runtime for a managed notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, runtime_id, runtime])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = managed_service.CreateRuntimeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if runtime_id is not None:
            request.runtime_id = runtime_id
        if runtime is not None:
            request.runtime = runtime

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_runtime,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcn_runtime.Runtime,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_runtime(
        self,
        request: Union[managed_service.DeleteRuntimeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Runtime.

        .. code-block:: python

            from google.cloud import notebooks_v1

            def sample_delete_runtime():
                # Create a client
                client = notebooks_v1.ManagedNotebookServiceClient()

                # Initialize request argument(s)
                request = notebooks_v1.DeleteRuntimeRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_runtime(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.notebooks_v1.types.DeleteRuntimeRequest, dict]):
                The request object. Request for deleting a Managed
                Notebook Runtime.
            name (:class:`str`):
                Required. Format:
                ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``

                This corresponds to the ``name`` field
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = managed_service.DeleteRuntimeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_runtime,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def start_runtime(
        self,
        request: Union[managed_service.StartRuntimeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Starts a Managed Notebook Runtime.
        Perform "Start" on GPU instances; "Resume" on CPU
        instances See:
        https://cloud.google.com/compute/docs/instances/stop-start-instance
        https://cloud.google.com/compute/docs/instances/suspend-resume-instance


        .. code-block:: python

            from google.cloud import notebooks_v1

            def sample_start_runtime():
                # Create a client
                client = notebooks_v1.ManagedNotebookServiceClient()

                # Initialize request argument(s)
                request = notebooks_v1.StartRuntimeRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.start_runtime(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.notebooks_v1.types.StartRuntimeRequest, dict]):
                The request object. Request for starting a Managed
                Notebook Runtime.
            name (:class:`str`):
                Required. Format:
                ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``

                This corresponds to the ``name`` field
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
                :class:`google.cloud.notebooks_v1.types.Runtime` The
                definition of a Runtime for a managed notebook instance.

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

        request = managed_service.StartRuntimeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.start_runtime,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            runtime.Runtime,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def stop_runtime(
        self,
        request: Union[managed_service.StopRuntimeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Stops a Managed Notebook Runtime.
        Perform "Stop" on GPU instances; "Suspend" on CPU
        instances See:
        https://cloud.google.com/compute/docs/instances/stop-start-instance
        https://cloud.google.com/compute/docs/instances/suspend-resume-instance


        .. code-block:: python

            from google.cloud import notebooks_v1

            def sample_stop_runtime():
                # Create a client
                client = notebooks_v1.ManagedNotebookServiceClient()

                # Initialize request argument(s)
                request = notebooks_v1.StopRuntimeRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.stop_runtime(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.notebooks_v1.types.StopRuntimeRequest, dict]):
                The request object. Request for stopping a Managed
                Notebook Runtime.
            name (:class:`str`):
                Required. Format:
                ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``

                This corresponds to the ``name`` field
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
                :class:`google.cloud.notebooks_v1.types.Runtime` The
                definition of a Runtime for a managed notebook instance.

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

        request = managed_service.StopRuntimeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.stop_runtime,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            runtime.Runtime,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def switch_runtime(
        self,
        request: Union[managed_service.SwitchRuntimeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Switch a Managed Notebook Runtime.

        .. code-block:: python

            from google.cloud import notebooks_v1

            def sample_switch_runtime():
                # Create a client
                client = notebooks_v1.ManagedNotebookServiceClient()

                # Initialize request argument(s)
                request = notebooks_v1.SwitchRuntimeRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.switch_runtime(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.notebooks_v1.types.SwitchRuntimeRequest, dict]):
                The request object. Request for switching a Managed
                Notebook Runtime.
            name (:class:`str`):
                Required. Format:
                ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``

                This corresponds to the ``name`` field
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
                :class:`google.cloud.notebooks_v1.types.Runtime` The
                definition of a Runtime for a managed notebook instance.

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

        request = managed_service.SwitchRuntimeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.switch_runtime,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            runtime.Runtime,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def reset_runtime(
        self,
        request: Union[managed_service.ResetRuntimeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Resets a Managed Notebook Runtime.

        .. code-block:: python

            from google.cloud import notebooks_v1

            def sample_reset_runtime():
                # Create a client
                client = notebooks_v1.ManagedNotebookServiceClient()

                # Initialize request argument(s)
                request = notebooks_v1.ResetRuntimeRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.reset_runtime(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.notebooks_v1.types.ResetRuntimeRequest, dict]):
                The request object. Request for reseting a Managed
                Notebook Runtime.
            name (:class:`str`):
                Required. Format:
                ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``

                This corresponds to the ``name`` field
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
                :class:`google.cloud.notebooks_v1.types.Runtime` The
                definition of a Runtime for a managed notebook instance.

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

        request = managed_service.ResetRuntimeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.reset_runtime,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            runtime.Runtime,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def report_runtime_event(
        self,
        request: Union[managed_service.ReportRuntimeEventRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Report and process a runtime event.

        .. code-block:: python

            from google.cloud import notebooks_v1

            def sample_report_runtime_event():
                # Create a client
                client = notebooks_v1.ManagedNotebookServiceClient()

                # Initialize request argument(s)
                request = notebooks_v1.ReportRuntimeEventRequest(
                    name="name_value",
                    vm_id="vm_id_value",
                )

                # Make the request
                operation = client.report_runtime_event(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.notebooks_v1.types.ReportRuntimeEventRequest, dict]):
                The request object. Request for reporting a Managed
                Notebook Event.
            name (:class:`str`):
                Required. Format:
                ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``

                This corresponds to the ``name`` field
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
                :class:`google.cloud.notebooks_v1.types.Runtime` The
                definition of a Runtime for a managed notebook instance.

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

        request = managed_service.ReportRuntimeEventRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.report_runtime_event,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            runtime.Runtime,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-notebooks",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ManagedNotebookServiceAsyncClient",)
