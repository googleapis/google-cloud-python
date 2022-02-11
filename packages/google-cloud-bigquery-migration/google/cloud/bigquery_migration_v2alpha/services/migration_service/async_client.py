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

from google.cloud.bigquery_migration_v2alpha.services.migration_service import pagers
from google.cloud.bigquery_migration_v2alpha.types import migration_entities
from google.cloud.bigquery_migration_v2alpha.types import migration_error_details
from google.cloud.bigquery_migration_v2alpha.types import migration_metrics
from google.cloud.bigquery_migration_v2alpha.types import migration_service
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import error_details_pb2  # type: ignore
from .transports.base import MigrationServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import MigrationServiceGrpcAsyncIOTransport
from .client import MigrationServiceClient


class MigrationServiceAsyncClient:
    """Service to handle EDW migrations."""

    _client: MigrationServiceClient

    DEFAULT_ENDPOINT = MigrationServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = MigrationServiceClient.DEFAULT_MTLS_ENDPOINT

    migration_subtask_path = staticmethod(MigrationServiceClient.migration_subtask_path)
    parse_migration_subtask_path = staticmethod(
        MigrationServiceClient.parse_migration_subtask_path
    )
    migration_workflow_path = staticmethod(
        MigrationServiceClient.migration_workflow_path
    )
    parse_migration_workflow_path = staticmethod(
        MigrationServiceClient.parse_migration_workflow_path
    )
    common_billing_account_path = staticmethod(
        MigrationServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        MigrationServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(MigrationServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        MigrationServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        MigrationServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        MigrationServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(MigrationServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        MigrationServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(MigrationServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        MigrationServiceClient.parse_common_location_path
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
            MigrationServiceAsyncClient: The constructed client.
        """
        return MigrationServiceClient.from_service_account_info.__func__(MigrationServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            MigrationServiceAsyncClient: The constructed client.
        """
        return MigrationServiceClient.from_service_account_file.__func__(MigrationServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return MigrationServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> MigrationServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            MigrationServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(MigrationServiceClient).get_transport_class, type(MigrationServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, MigrationServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the migration service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.MigrationServiceTransport]): The
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
        self._client = MigrationServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_migration_workflow(
        self,
        request: Union[migration_service.CreateMigrationWorkflowRequest, dict] = None,
        *,
        parent: str = None,
        migration_workflow: migration_entities.MigrationWorkflow = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> migration_entities.MigrationWorkflow:
        r"""Creates a migration workflow.

        .. code-block::

            from google.cloud import bigquery_migration_v2alpha

            def sample_create_migration_workflow():
                # Create a client
                client = bigquery_migration_v2alpha.MigrationServiceClient()

                # Initialize request argument(s)
                request = bigquery_migration_v2alpha.CreateMigrationWorkflowRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_migration_workflow(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_migration_v2alpha.types.CreateMigrationWorkflowRequest, dict]):
                The request object. Request to create a migration
                workflow resource.
            parent (:class:`str`):
                Required. The name of the project to which this
                migration workflow belongs. Example:
                ``projects/foo/locations/bar``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            migration_workflow (:class:`google.cloud.bigquery_migration_v2alpha.types.MigrationWorkflow`):
                Required. The migration workflow to
                create.

                This corresponds to the ``migration_workflow`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_migration_v2alpha.types.MigrationWorkflow:
                A migration workflow which specifies
                what needs to be done for an EDW
                migration.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, migration_workflow])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = migration_service.CreateMigrationWorkflowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if migration_workflow is not None:
            request.migration_workflow = migration_workflow

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_migration_workflow,
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

        # Done; return the response.
        return response

    async def get_migration_workflow(
        self,
        request: Union[migration_service.GetMigrationWorkflowRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> migration_entities.MigrationWorkflow:
        r"""Gets a previously created migration workflow.

        .. code-block::

            from google.cloud import bigquery_migration_v2alpha

            def sample_get_migration_workflow():
                # Create a client
                client = bigquery_migration_v2alpha.MigrationServiceClient()

                # Initialize request argument(s)
                request = bigquery_migration_v2alpha.GetMigrationWorkflowRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_migration_workflow(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_migration_v2alpha.types.GetMigrationWorkflowRequest, dict]):
                The request object. A request to get a previously
                created migration workflow.
            name (:class:`str`):
                Required. The unique identifier for the migration
                workflow. Example:
                ``projects/123/locations/us/workflows/1234``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_migration_v2alpha.types.MigrationWorkflow:
                A migration workflow which specifies
                what needs to be done for an EDW
                migration.

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

        request = migration_service.GetMigrationWorkflowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_migration_workflow,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=120.0,
            ),
            default_timeout=120.0,
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

    async def list_migration_workflows(
        self,
        request: Union[migration_service.ListMigrationWorkflowsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMigrationWorkflowsAsyncPager:
        r"""Lists previously created migration workflow.

        .. code-block::

            from google.cloud import bigquery_migration_v2alpha

            def sample_list_migration_workflows():
                # Create a client
                client = bigquery_migration_v2alpha.MigrationServiceClient()

                # Initialize request argument(s)
                request = bigquery_migration_v2alpha.ListMigrationWorkflowsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_migration_workflows(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bigquery_migration_v2alpha.types.ListMigrationWorkflowsRequest, dict]):
                The request object. A request to list previously created
                migration workflows.
            parent (:class:`str`):
                Required. The project and location of the migration
                workflows to list. Example:
                ``projects/123/locations/us``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_migration_v2alpha.services.migration_service.pagers.ListMigrationWorkflowsAsyncPager:
                Response object for a ListMigrationWorkflows call.

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

        request = migration_service.ListMigrationWorkflowsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_migration_workflows,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=120.0,
            ),
            default_timeout=120.0,
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
        response = pagers.ListMigrationWorkflowsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_migration_workflow(
        self,
        request: Union[migration_service.DeleteMigrationWorkflowRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a migration workflow by name.

        .. code-block::

            from google.cloud import bigquery_migration_v2alpha

            def sample_delete_migration_workflow():
                # Create a client
                client = bigquery_migration_v2alpha.MigrationServiceClient()

                # Initialize request argument(s)
                request = bigquery_migration_v2alpha.DeleteMigrationWorkflowRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_migration_workflow(request=request)

        Args:
            request (Union[google.cloud.bigquery_migration_v2alpha.types.DeleteMigrationWorkflowRequest, dict]):
                The request object. A request to delete a previously
                created migration workflow.
            name (:class:`str`):
                Required. The unique identifier for the migration
                workflow. Example:
                ``projects/123/locations/us/workflows/1234``

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

        request = migration_service.DeleteMigrationWorkflowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_migration_workflow,
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
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def start_migration_workflow(
        self,
        request: Union[migration_service.StartMigrationWorkflowRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts a previously created migration workflow. I.e.,
        the state transitions from DRAFT to RUNNING. This is a
        no-op if the state is already RUNNING. An error will be
        signaled if the state is anything other than DRAFT or
        RUNNING.


        .. code-block::

            from google.cloud import bigquery_migration_v2alpha

            def sample_start_migration_workflow():
                # Create a client
                client = bigquery_migration_v2alpha.MigrationServiceClient()

                # Initialize request argument(s)
                request = bigquery_migration_v2alpha.StartMigrationWorkflowRequest(
                    name="name_value",
                )

                # Make the request
                client.start_migration_workflow(request=request)

        Args:
            request (Union[google.cloud.bigquery_migration_v2alpha.types.StartMigrationWorkflowRequest, dict]):
                The request object. A request to start a previously
                created migration workflow.
            name (:class:`str`):
                Required. The unique identifier for the migration
                workflow. Example:
                ``projects/123/locations/us/workflows/1234``

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

        request = migration_service.StartMigrationWorkflowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.start_migration_workflow,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=120.0,
            ),
            default_timeout=120.0,
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

    async def get_migration_subtask(
        self,
        request: Union[migration_service.GetMigrationSubtaskRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> migration_entities.MigrationSubtask:
        r"""Gets a previously created migration subtask.

        .. code-block::

            from google.cloud import bigquery_migration_v2alpha

            def sample_get_migration_subtask():
                # Create a client
                client = bigquery_migration_v2alpha.MigrationServiceClient()

                # Initialize request argument(s)
                request = bigquery_migration_v2alpha.GetMigrationSubtaskRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_migration_subtask(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_migration_v2alpha.types.GetMigrationSubtaskRequest, dict]):
                The request object. A request to get a previously
                created migration subtasks.
            name (:class:`str`):
                Required. The unique identifier for the migration
                subtask. Example:
                ``projects/123/locations/us/workflows/1234/subtasks/543``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_migration_v2alpha.types.MigrationSubtask:
                A subtask for a migration which
                carries details about the configuration
                of the subtask. The content of the
                details should not matter to the end
                user, but is a contract between the
                subtask creator and subtask worker.

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

        request = migration_service.GetMigrationSubtaskRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_migration_subtask,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=120.0,
            ),
            default_timeout=120.0,
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

    async def list_migration_subtasks(
        self,
        request: Union[migration_service.ListMigrationSubtasksRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMigrationSubtasksAsyncPager:
        r"""Lists previously created migration subtasks.

        .. code-block::

            from google.cloud import bigquery_migration_v2alpha

            def sample_list_migration_subtasks():
                # Create a client
                client = bigquery_migration_v2alpha.MigrationServiceClient()

                # Initialize request argument(s)
                request = bigquery_migration_v2alpha.ListMigrationSubtasksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_migration_subtasks(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bigquery_migration_v2alpha.types.ListMigrationSubtasksRequest, dict]):
                The request object. A request to list previously created
                migration subtasks.
            parent (:class:`str`):
                Required. The migration task of the subtasks to list.
                Example: ``projects/123/locations/us/workflows/1234``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_migration_v2alpha.services.migration_service.pagers.ListMigrationSubtasksAsyncPager:
                Response object for a ListMigrationSubtasks call.

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

        request = migration_service.ListMigrationSubtasksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_migration_subtasks,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=120.0,
            ),
            default_timeout=120.0,
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
        response = pagers.ListMigrationSubtasksAsyncPager(
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
            "google-cloud-bigquery-migration",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("MigrationServiceAsyncClient",)
